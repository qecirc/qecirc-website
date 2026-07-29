"""Syndrome-extraction validation.

Every negative case here is a circuit that *looks* right — every check applied
exactly once, on the right qubits, with the right ancillas — and is still not a
syndrome extraction. That is the point: applying the checks is easy, and the
things that go wrong (a lost stabilizer, an operator measured outside the group,
two ancillas left entangled by a bad interleaving) are invisible to any test that
only counts gates.

Steane is the workhorse: self-dual CSS, so the same three rows serve as Hx and
Hz, and its weight-4 stabilizers overlap enough for the interleaving case to be
constructible by hand.
"""

import numpy as np
import pytest
import stim

from scripts.add_circuit.annotate import build_annotated_se, strip_readout, validate_annotated
from scripts.add_circuit.circuit_validate import (
    circuit_properties,
    measured_stabilizers,
    round_check_matrix,
    validate_syndrome_extraction,
    validate_syndrome_extraction_h,
)
from scripts.add_circuit.syndrome_extraction import build_se_round

N = 7
STEANE_CHECKS = np.array(
    [
        [1, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 1, 1],
    ]
)
_Z = np.zeros_like(STEANE_CHECKS)
STEANE_H = np.vstack([np.hstack([STEANE_CHECKS, _Z]), np.hstack([_Z, STEANE_CHECKS])])
# X-bar and Z-bar: the all-ones operator in each basis.
STEANE_LOGICAL = np.array([[1] * N + [0] * N, [0] * N + [1] * N])

# Ancillas: 7,8,9 read the X-checks, 10,11,12 the Z-checks.
_X_ANCILLAS = [7, 8, 9]
_Z_ANCILLAS = [10, 11, 12]


def steane_round(drop: int | None = None, spurious: bool = False) -> stim.Circuit:
    """One Steane syndrome-extraction round, checks taken one ancilla at a time.

    Sequential rather than scheduled, so it is correct by construction and the
    negative cases below differ from it in exactly one respect.

    ``drop`` omits one ancilla's checks entirely; ``spurious`` adds a seventh
    ancilla that copies a bare ``Z0`` — an operator that is not in the stabilizer
    group and anticommutes with the X-checks.
    """
    ancillas = _X_ANCILLAS + _Z_ANCILLAS + ([13] if spurious else [])
    circ = stim.Circuit()
    circ.append("R", ancillas)
    for anc, row in zip(_X_ANCILLAS, STEANE_CHECKS):
        if anc == drop:
            continue
        circ.append("H", [anc])
        for q in np.flatnonzero(row):
            circ.append("CX", [anc, int(q)])
        circ.append("H", [anc])
    for anc, row in zip(_Z_ANCILLAS, STEANE_CHECKS):
        if anc == drop:
            continue
        for q in np.flatnonzero(row):
            circ.append("CX", [int(q), anc])
    if spurious:
        circ.append("CX", [0, 13])
    circ.append("M", ancillas)
    return circ


class TestValidRound:
    def test_sequential_round_passes(self):
        assert validate_syndrome_extraction_h(steane_round(), STEANE_H, N) == "passed"

    def test_logicals_are_checked_and_preserved(self):
        assert (
            validate_syndrome_extraction_h(steane_round(), STEANE_H, N, logical=STEANE_LOGICAL)
            == "passed"
        )

    def test_css_wrapper_agrees(self):
        """The Hx/Hz entry point is the same check, not a parallel implementation."""
        assert (
            validate_syndrome_extraction(steane_round(), STEANE_CHECKS, STEANE_CHECKS) == "passed"
        )

    def test_accepts_circuit_as_text(self):
        assert validate_syndrome_extraction_h(str(steane_round()), STEANE_H, N) == "passed"

    def test_measured_group_is_the_stabilizer_group(self):
        measured = measured_stabilizers(steane_round(), N)
        assert measured.shape[1] == 2 * N
        assert np.linalg.matrix_rank(measured) == 6


class TestRejects:
    def test_missing_stabilizer(self):
        """Five of six checks read is not a syndrome extraction."""
        outcome = validate_syndrome_extraction_h(steane_round(drop=8), STEANE_H, N)
        assert outcome.startswith("failed:")
        assert "rank 5" in outcome and "1 not measured" in outcome

    def test_operator_outside_the_stabilizer_group(self):
        """A bare Z0 anticommutes with the X-checks: it both measures something
        the code does not stabilize and destroys an X-check's determinism."""
        outcome = validate_syndrome_extraction_h(steane_round(spurious=True), STEANE_H, N)
        assert outcome.startswith("failed:")
        assert "1 measured outside the stabilizer group" in outcome

    def test_no_measurements(self):
        gates_only = stim.Circuit("H 7\nCX 7 0 7 2 7 4 7 6\nH 7")
        outcome = validate_syndrome_extraction_h(gates_only, STEANE_H, N)
        assert outcome == "failed: circuit has no measurements, so it extracts no syndrome"

    def test_operator_not_preserved_is_reported_as_such(self):
        """A single-qubit X is not a logical of the code, and the Z-checks do not
        preserve it — so the logical branch fires rather than the measured one."""
        not_a_logical = np.array([[1] + [0] * (2 * N - 1)])
        outcome = validate_syndrome_extraction_h(steane_round(), STEANE_H, N, logical=not_a_logical)
        assert "is not preserved by the round" in outcome

    def test_wrong_width_raises(self):
        try:
            validate_syndrome_extraction_h(steane_round(), STEANE_H, 5)
        except ValueError as e:
            assert "columns" in str(e)
        else:
            raise AssertionError("expected ValueError for an h of the wrong width")


class TestInterleaving:
    """The failure a gate-counting check cannot see.

    An X-check and a Z-check sharing data qubits commute as operators, but their
    CNOTs do not: reverse the relative order on an odd number of the shared
    qubits and the two ancillas come out entangled. Every check is still applied
    exactly once, so the round looks perfect and measures nothing.
    """

    @staticmethod
    def _pair(inverted: set[int]) -> stim.Circuit:
        """X-check and Z-check on qubits 0,2,4,6, with ancillas 7 and 10.

        ``inverted`` names the shared qubits where the Z-check goes first.
        """
        circ = stim.Circuit()
        circ.append("R", [7, 10])
        circ.append("H", [7])
        for q in (0, 2, 4, 6):
            if q in inverted:
                circ.append("CX", [q, 10])
                circ.append("CX", [7, q])
            else:
                circ.append("CX", [7, q])
                circ.append("CX", [q, 10])
        circ.append("H", [7])
        circ.append("M", [7, 10])
        return circ

    _H_PAIR = np.vstack(
        [
            np.hstack([STEANE_CHECKS[:1], _Z[:1]]),
            np.hstack([_Z[:1], STEANE_CHECKS[:1]]),
        ]
    )

    def test_consistent_order_passes(self):
        assert validate_syndrome_extraction_h(self._pair(set()), self._H_PAIR, N) == "passed"

    def test_even_number_of_inversions_still_passes(self):
        assert validate_syndrome_extraction_h(self._pair({0, 2}), self._H_PAIR, N) == "passed"

    def test_odd_number_of_inversions_measures_nothing(self):
        outcome = validate_syndrome_extraction_h(self._pair({0}), self._H_PAIR, N)
        assert outcome.startswith("failed:")
        assert "rank 0" in outcome


def _greedy_schedule() -> list[list[tuple[int, int, str]]]:
    """Pack Steane's checks into ticks, X-checks first and Z-checks after.

    Earliest-free-tick greedy; separating the two phases sidesteps interleaving
    entirely, which is what makes this a fixture rather than a subject.
    """
    ticks: list[list[tuple[int, int, str]]] = []
    used: list[set[int]] = []
    for pauli, base in (("X", 7), ("Z", 10)):
        floor = len(ticks)
        for i, row in enumerate(STEANE_CHECKS):
            for q in np.flatnonzero(row):
                t = floor
                while t < len(ticks) and ({int(q), base + i} & used[t]):
                    t += 1
                if t == len(ticks):
                    ticks.append([])
                    used.append(set())
                ticks[t].append((int(q), base + i, pauli))
                used[t] |= {int(q), base + i}
    return ticks


class TestBuildRound:
    """The emitter: a schedule in, a round out, and the two Hadamard styles must
    describe the same physics."""

    # A valid parallel schedule for Steane: greedily packed, X-phase then
    # Z-phase, so no data qubit ever takes an X- and a Z-check in the same tick.
    _TICKS = _greedy_schedule()

    def test_round_is_valid(self):
        circ = build_se_round(self._TICKS, N)
        assert validate_syndrome_extraction_h(circ, STEANE_H, N, logical=STEANE_LOGICAL) == "passed"

    def test_hadamard_styles_are_equivalent(self):
        """per-check wrapping is the same round with the cancelling H pairs left
        in; only the single-qubit gate count differs."""
        basis = build_se_round(self._TICKS, N, hadamards="basis")
        per_check = build_se_round(self._TICKS, N, hadamards="per-check")
        assert validate_syndrome_extraction_h(per_check, STEANE_H, N) == "passed"
        assert basis.num_measurements == per_check.num_measurements
        assert circuit_properties(str(basis)).two_qubit_gate_count == (
            circuit_properties(str(per_check)).two_qubit_gate_count
        )
        assert circuit_properties(str(basis)).gate_count < (
            circuit_properties(str(per_check)).gate_count
        )

    def test_measurement_order_is_ascending_ancilla(self):
        circ = build_se_round(self._TICKS, N)
        checks = round_check_matrix(circ, N)
        # Ancillas 7,8,9 read the X-checks and 10,11,12 the Z-checks, in that order.
        assert np.array_equal(checks[:3, :N], STEANE_CHECKS)
        assert not checks[:3, N:].any()
        assert np.array_equal(checks[3:, N:], STEANE_CHECKS)

    def test_ticks_are_preserved_not_repacked(self):
        """The tick assignment is the whole content of a scheduling result, so
        the emitter must not compress it."""
        spread = [[(0, 7, "Z")], [], [(1, 7, "Z")]]
        assert str(build_se_round(spread, N)).count("TICK") == 4  # reset + 3 ticks

    def test_rejects_a_tick_that_reuses_a_qubit(self):
        with pytest.raises(ValueError, match="parallel"):
            build_se_round([[(0, 7, "Z"), (0, 8, "Z")]], N)

    def test_rejects_an_ancilla_inside_the_data_range(self):
        with pytest.raises(ValueError, match="data range"):
            build_se_round([[(0, 3, "Z")]], N)

    def test_rejects_a_mixed_basis_ancilla(self):
        with pytest.raises(ValueError, match="both X and Z"):
            build_se_round([[(0, 7, "X")], [(1, 7, "Z")]], N)


class TestRoundCheckMatrix:
    def test_returns_none_for_a_shape_it_cannot_read(self):
        """Deliberately narrow: no map is better than a wrong one, and nothing in
        validation depends on it."""
        assert round_check_matrix("R 7\nM 7\nR 7\nM 7", N) is None  # reset after measure
        assert round_check_matrix("H 0", N) is None  # no measurements

    def test_returns_none_when_ancillas_are_entangled(self):
        """The interleaving failure again: the outcome is not a function of the
        data, so there is no operator to report."""
        bad = TestInterleaving._pair({0})
        assert round_check_matrix(bad, N) is None

    def test_reads_a_round_that_holds_its_ancillas_in_the_x_basis(self):
        """`RX` … `MX` with `CZ` for the Z-checks is the same construction in a
        different frame — it is what qLDPC emits — and it has to be readable, or
        those rounds silently lose their annotated memory experiment."""
        circ = stim.Circuit()
        circ.append("RX", [7, 8, 9, 10, 11, 12])
        for row, anc in enumerate((7, 8, 9)):  # X-checks: ancilla controls a CX
            for q in np.flatnonzero(STEANE_CHECKS[row]):
                circ.append("CX", [anc, int(q)])
        for row, anc in enumerate((10, 11, 12)):  # Z-checks: CZ from the X-basis ancilla
            for q in np.flatnonzero(STEANE_CHECKS[row]):
                circ.append("CZ", [anc, int(q)])
        circ.append("MX", [7, 8, 9, 10, 11, 12])

        assert validate_syndrome_extraction_h(circ, STEANE_H, N, logical=STEANE_LOGICAL) == "passed"
        checks = round_check_matrix(circ, N)
        assert checks is not None
        assert np.array_equal(checks[:3, :N], STEANE_CHECKS)
        assert not checks[:3, N:].any()
        assert np.array_equal(checks[3:, N:], STEANE_CHECKS)
        assert not checks[3:, :N].any()

    def test_returns_none_when_an_ancilla_changes_basis_between_reset_and_measure(self):
        """Reset in X and read in Z and the outcome is random, however correct
        the check pattern in between looks."""
        circ = stim.Circuit()
        circ.append("RX", [7])
        circ.append("CX", [7, 0])
        circ.append("M", [7])
        assert round_check_matrix(circ, N) is None


class TestAnnotatedMemoryExperiment:
    @staticmethod
    def _round():
        return str(build_se_round(TestBuildRound._TICKS, N))

    def test_detectors_are_deterministic(self):
        ann = build_annotated_se(self._round(), STEANE_H, STEANE_LOGICAL, N, rounds=3)
        assert validate_annotated(ann) is None

    def test_shape(self):
        ann = build_annotated_se(self._round(), STEANE_H, STEANE_LOGICAL, N, rounds=3)
        text = str(ann)
        assert text.startswith("R 0 1 2 3 4 5 6\n")  # the data, reset to |0...0>
        assert "REPEAT 2 {" in text  # first round explicit, the rest repeated
        assert ann.num_observables == 1
        # 3 first-round Z-checks + 2 x 6 inter-round + 3 terminal
        assert ann.num_detectors == 3 + 12 + 3

    def test_single_round_has_no_repeat_block(self):
        ann = build_annotated_se(self._round(), STEANE_H, STEANE_LOGICAL, N, rounds=1)
        assert "REPEAT" not in str(ann)
        assert validate_annotated(ann) is None

    def test_detectors_off_view_drops_the_ones_inside_the_repeat(self):
        """The Detectors switch subtracts from the annotated body, so a detector
        left inside the REPEAT block would survive being switched off."""
        ann = build_annotated_se(self._round(), STEANE_H, STEANE_LOGICAL, N, rounds=3)
        plain = strip_readout(ann)
        assert plain.num_detectors == 0
        assert plain.num_observables == 0
        assert "REPEAT 2 {" in str(plain)  # the rounds themselves stay

    def test_mixed_pauli_checks_get_no_body(self):
        """A round whose checks mix X and Z on one qubit — the non-CSS case — has
        no terminal basis, so no readout, no observable and no first-round
        detector. An experiment with no outcome is not worth emitting."""
        mixed = "R 7\nH 7\nCY 7 0\nH 7\nM 7"  # reads Y0
        assert round_check_matrix(mixed, N) is not None  # the map is fine; the basis is not
        assert build_annotated_se(mixed, STEANE_H, STEANE_LOGICAL, N, rounds=3) is None

    def test_no_map_no_body(self):
        """A round whose ancillas come out entangled cannot be annotated — and
        must not be annotated wrongly."""
        assert (
            build_annotated_se(str(TestInterleaving._pair({0})), STEANE_H, STEANE_LOGICAL, N, 3)
            is None
        )
