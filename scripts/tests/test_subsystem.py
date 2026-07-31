"""Tests for the gauge-group arithmetic behind subsystem codes."""

import numpy as np
import pytest

from scripts.add_circuit.code_identify import gf2_rank
from scripts.add_circuit.subsystem import (
    check_stabilizers_are_central,
    describe,
    gauge_qubits,
    logical_qubits,
)

# Bacon-Shor [[9,1,3]] on a 3x3 grid, built here rather than imported so the test
# does not need qLDPC. The gauge group is the weight-2 XX pairs in each row and
# ZZ pairs in each column; the stabilizer group is the pairs of adjacent full
# rows/columns. Four gauge qubits sit between them, which is exactly what made
# this code unstorable: n - rank(S) = 5, not 1.
#
# It spans different groups from `qldpc.codes.BaconShorCode(3)` — a different
# qubit convention — but `describe` gives (k=1, 4 gauge qubits) for both, which
# is what is under test.
_ROWS = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
_COLS = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]


def _op(x_support, z_support, n=9):
    row = np.zeros(2 * n, dtype=int)
    for q in x_support:
        row[q] = 1
    for q in z_support:
        row[n + q] = 1
    return row


def _bacon_shor():
    gauge = []
    for row in _ROWS:  # XX on horizontally adjacent pairs
        for a, b in zip(row, row[1:]):
            gauge.append(_op([a, b], []))
    for col in _COLS:  # ZZ on vertically adjacent pairs
        for a, b in zip(col, col[1:]):
            gauge.append(_op([], [a, b]))
    stabilizers = []
    # The X gauge operators run along rows, so their products that commute with
    # everything span two adjacent *columns* — and the Z ones the other way.
    # Getting this pair the wrong way round gives a set that anticommutes with
    # the gauge group, which `check_stabilizers_are_central` catches.
    for a, b in zip(_COLS, _COLS[1:]):  # X on two adjacent columns
        stabilizers.append(_op(a + b, []))
    for a, b in zip(_ROWS, _ROWS[1:]):  # Z on two adjacent rows
        stabilizers.append(_op([], a + b))
    return np.array(gauge), np.array(stabilizers)


STEANE_H = np.array(
    [
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    ]
)


class TestBaconShor:
    def test_k_is_one_not_five(self):
        """The bug this exists to fix: counting gauge qubits as logical ones
        stored [[9,1,3]] as [[9,5,3]]."""
        gauge, stabilizers = _bacon_shor()
        assert logical_qubits(gauge, stabilizers, 9) == 1
        assert 9 - gf2_rank(stabilizers) == 5  # what the old formula gave

    def test_four_gauge_qubits(self):
        gauge, stabilizers = _bacon_shor()
        assert gauge_qubits(gauge, stabilizers, 9) == 4

    def test_the_stabilizers_are_central(self):
        gauge, stabilizers = _bacon_shor()
        check_stabilizers_are_central(gauge, stabilizers, 9)  # does not raise

    def test_describe_reports_the_gauge_group_for_storage(self):
        gauge, stabilizers = _bacon_shor()
        k, count, to_store = describe(gauge, stabilizers, 9)
        assert (k, count) == (1, 4)
        assert to_store is not None and to_store.shape == gauge.shape


class TestStabilizerCodesAreUnaffected:
    """`G == S` must give exactly the number the library computed before, by the
    same formula rather than a special case."""

    def test_no_gauge_group_at_all(self):
        k, count, to_store = describe(None, STEANE_H, 7)
        assert (k, count, to_store) == (1, 0, None)

    def test_a_gauge_group_equal_to_the_stabilizers(self):
        k, count, to_store = describe(STEANE_H, STEANE_H, 7)
        assert (k, count) == (1, 0)
        assert to_store is None, "nothing extra to store when the groups coincide"

    def test_a_redundant_generating_set_is_still_the_same_code(self):
        """Rank, not row count — a repeated generator adds no gauge qubit."""
        redundant = np.vstack([STEANE_H, STEANE_H[0]])
        assert describe(redundant, STEANE_H, 7)[:2] == (1, 0)


class TestRefusals:
    def test_a_non_central_stabilizer_is_refused(self):
        """X0 and Z0 anticommute, so calling Z0 a stabilizer of a gauge group
        containing X0 is incoherent — better to refuse than to derive a k."""
        gauge = np.array([_op([0], [])])
        stabilizers = np.array([_op([], [0])])
        with pytest.raises(ValueError, match="not central"):
            check_stabilizers_are_central(gauge, stabilizers, 9)

    def test_an_odd_rank_gap_is_refused(self):
        """Gauge qubits come in anticommuting pairs, so the gap is always even.
        An odd one means the two matrices are not one code."""
        gauge = np.array([_op([0], [])])  # rank 1 over an empty stabilizer group
        stabilizers = np.zeros((0, 18), dtype=int)
        with pytest.raises(ValueError, match="odd"):
            gauge_qubits(gauge, stabilizers, 9)

    def test_a_stabilizer_group_outranking_the_gauge_group_is_refused(self):
        with pytest.raises(ValueError, match="cannot outrank"):
            gauge_qubits(np.array([_op([0, 1], [])]), _bacon_shor()[1], 9)

    def test_mismatched_widths_are_refused(self):
        with pytest.raises(ValueError, match="columns"):
            describe(np.zeros((2, 10), dtype=int), STEANE_H, 7)


class TestItReachesStorage:
    """The arithmetic is only useful if it survives into the stored YAML."""

    def _computed(self):
        from scripts.add_circuit.compute import compute_code_data_h

        gauge, stabilizers = _bacon_shor()
        return compute_code_data_h(stabilizers, 9, 3, code_name="Bacon-Shor", gauge=gauge)

    def test_the_stored_parameters_are_the_code_s_own(self):
        code = self._computed()["code"]
        assert (code["n"], code["k"], code["d"]) == (9, 1, 3)
        assert code["gauge_qubits"] == 4

    def test_the_gauge_group_is_stored_and_the_stabilizers_stay_in_h(self):
        code = self._computed()["code"]
        assert code["gauge"] is not None
        assert gf2_rank(np.array(code["h"])) == 4, "h is still the stabilizer group"
        assert gf2_rank(np.array(code["gauge"])) == 12

    def test_it_is_tagged_so_the_page_can_explain_itself(self):
        code = self._computed()["code"]
        assert "subsystem" in [t["name"] for t in code["tags"]]

    def test_the_yaml_carries_both_matrices(self):
        from scripts.add_circuit.yaml_helpers import build_code_yaml, dump_yaml, load_yaml

        doc = load_yaml(dump_yaml(build_code_yaml(self._computed()["code"])))
        assert doc["k"] == 1 and doc["gauge_qubits"] == 4
        assert doc["h"] and doc["gauge"]

    def test_a_stabilizer_code_gains_no_new_fields(self):
        """The change has to be invisible to the 38 codes already stored."""
        from scripts.add_circuit.compute import compute_code_data_h
        from scripts.add_circuit.yaml_helpers import build_code_yaml

        five_qubit = np.array(
            [
                [1, 0, 0, 1, 0, 0, 1, 1, 0, 0],
                [0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
                [1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
                [0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
            ]
        )
        doc = build_code_yaml(compute_code_data_h(five_qubit, 5, 3)["code"])
        assert "gauge" not in doc and "gauge_qubits" not in doc

    def test_a_css_subsystem_code_is_still_tagged_css(self):
        """Bacon-Shor's stabilizer group is CSS; it takes the symplectic path
        only because k cannot be derived the CSS way. Losing the tag would hide
        it from a CSS search while its page rendered an X/Z split anyway."""
        from scripts.add_circuit.code_identify import split_h_to_css

        _, stabilizers = _bacon_shor()
        assert split_h_to_css(stabilizers, 9) is not None, "fixture must be CSS"
        code = self._computed()["code"]
        assert code["is_css"] is True
        assert "CSS" in [t["name"] for t in code["tags"]]
