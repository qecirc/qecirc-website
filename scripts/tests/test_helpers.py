"""
Tests for helpers.py — notebook-friendly helper functions.
"""

import tempfile
from pathlib import Path

import numpy as np
import yaml

from scripts.add_circuit.code_identify import canonical_hash
from scripts.add_circuit.helpers import (
    ExistingCodeMatch,
    check_code,
    find_existing_code,
    find_existing_code_full,
    preview_circuit,
    summarize_circuit,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

STEANE_H = np.array(
    [
        [1, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 1, 1],
    ]
)

STEANE_STIM = """\
H 4 5 6
TICK
CX 5 1
TICK
CX 1 2 4 0
TICK
CX 6 4 5 3 2 0
TICK
CX 6 3 4 5 0 1
"""


# ---------------------------------------------------------------------------
# check_code
# ---------------------------------------------------------------------------


class TestCheckCode:
    def test_steane_code(self):
        result = check_code(STEANE_H, STEANE_H, d=3)
        assert result["n"] == 7
        assert result["k"] == 1
        assert result["d"] == 3
        assert result["is_css"] is True
        assert result["is_self_dual"] is True
        assert len(result["canonical_hash"]) == 64

    def test_without_distance(self):
        result = check_code(STEANE_H, STEANE_H)
        assert "d" not in result
        assert result["n"] == 7

    def test_non_css_code(self):
        Hx = np.array([[1, 0, 0, 1, 0], [0, 1, 0, 0, 1], [1, 0, 1, 0, 0], [0, 1, 0, 1, 0]])
        Hz = np.array([[0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 1, 1], [1, 0, 0, 0, 1]])
        result = check_code(Hx, Hz, d=3)
        assert result["is_css"] is False
        assert result["n"] == 5
        assert result["k"] == 1


# ---------------------------------------------------------------------------
# find_existing_code
# ---------------------------------------------------------------------------


class TestFindExistingCode:
    def test_finds_existing(self):
        c_hash = canonical_hash(STEANE_H, STEANE_H)
        with tempfile.TemporaryDirectory() as tmpdir:
            codes_dir = Path(tmpdir) / "codes"
            codes_dir.mkdir()
            code_yaml = {
                "name": "Steane Code",
                "canonical_hash": c_hash,
                "hx": STEANE_H.tolist(),
                "hz": STEANE_H.tolist(),
            }
            (codes_dir / "steane-code.yaml").write_text(yaml.dump(code_yaml))
            assert find_existing_code(STEANE_H, STEANE_H, data_dir=tmpdir) == "steane-code"

    def test_returns_none_for_unknown(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            codes_dir = Path(tmpdir) / "codes"
            codes_dir.mkdir()
            assert find_existing_code(STEANE_H, STEANE_H, data_dir=tmpdir) is None


# ---------------------------------------------------------------------------
# find_existing_code_full
# ---------------------------------------------------------------------------


class TestFindExistingCodeFull:
    def _make_code_dir(self, tmpdir, Hx, Hz):
        """Helper: write a Steane code YAML into a temp data_yaml/codes/ dir."""
        codes_dir = Path(tmpdir) / "codes"
        codes_dir.mkdir()
        c_hash = canonical_hash(Hx, Hz)
        code_yaml = {
            "name": "Steane Code",
            "canonical_hash": c_hash,
            "hx": Hx.tolist(),
            "hz": Hz.tolist(),
        }
        (codes_dir / "steane-code.yaml").write_text(yaml.dump(code_yaml))

    def test_returns_match_with_no_permutation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._make_code_dir(tmpdir, STEANE_H, STEANE_H)
            match = find_existing_code_full(STEANE_H, STEANE_H, data_dir=tmpdir)
            assert match is not None
            assert isinstance(match, ExistingCodeMatch)
            assert match.slug == "steane-code"
            assert match.qubit_permutation is None  # orderings match

    def test_returns_match_with_permutation(self):
        perm = [3, 1, 5, 0, 6, 2, 4]
        Hx_perm = STEANE_H[:, perm]
        Hz_perm = STEANE_H[:, perm]
        with tempfile.TemporaryDirectory() as tmpdir:
            self._make_code_dir(tmpdir, STEANE_H, STEANE_H)
            match = find_existing_code_full(Hx_perm, Hz_perm, data_dir=tmpdir)
            assert match is not None
            assert match.slug == "steane-code"
            assert match.qubit_permutation is not None
            # Applying the permutation to the queried matrices should recover stored matrices
            from scripts.add_circuit.code_identify import gf2_rref

            assert np.array_equal(
                gf2_rref(Hx_perm[:, match.qubit_permutation]), gf2_rref(STEANE_H)
            )

    def test_returns_none_for_unknown(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            codes_dir = Path(tmpdir) / "codes"
            codes_dir.mkdir()
            assert find_existing_code_full(STEANE_H, STEANE_H, data_dir=tmpdir) is None


# ---------------------------------------------------------------------------
# summarize_circuit
# ---------------------------------------------------------------------------


class TestSummarizeCircuit:
    def test_basic_summary(self):
        result = summarize_circuit(STEANE_STIM)
        assert result["qubit_count"] == 7
        assert result["gate_count"] > 0
        assert result["depth"] > 0
        assert "crumble" in result["crumble_url"]
        assert "quirk" in result["quirk_url"]

    def test_accepts_stim_circuit(self):
        import stim

        circ = stim.Circuit(STEANE_STIM)
        result = summarize_circuit(circ)
        assert result["qubit_count"] == 7


# ---------------------------------------------------------------------------
# preview_circuit
# ---------------------------------------------------------------------------


class TestPreviewCircuit:
    def test_preview_is_dry_run(self):
        # Use a code not in data_yaml/ to avoid qubit relabeling (mqt-qecc dep)
        Hx = np.array([[1, 1, 1, 1]])
        Hz = np.array([[1, 1, 1, 1]])
        circuit = "H 0\nCNOT 0 1\nCNOT 0 2\nCNOT 0 3\n"
        result = preview_circuit(
            Hx=Hx,
            Hz=Hz,
            circuit=circuit,
            circuit_name="Test Encoding",
            d=2,
            code_name="Test Code",
        )
        assert result.dry_run is True
        assert len(result.files_written) > 0
        assert result.code_name == "Test Code"
        assert result.circuit_name == "Test Encoding"
