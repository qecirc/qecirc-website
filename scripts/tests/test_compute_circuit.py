"""
Tests for compute_circuit.py — circuit-level computation.
"""

import pytest

from scripts.add_circuit.compute_circuit import compute_circuit_data

try:
    import mqt.qecc  # noqa: F401

    _mqt_available = True
except (ImportError, ModuleNotFoundError):
    _mqt_available = False


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

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
# compute_circuit_data
# ---------------------------------------------------------------------------


class TestComputeCircuitData:
    def test_basic_output_structure(self):
        result = compute_circuit_data(
            STEANE_STIM,
            circuit_name="Standard Encoding",
        )
        assert result["name"] == "Standard Encoding"
        assert result["slug"] == "standard-encoding"
        assert result["qubit_count"] == 7
        assert result["two_qubit_gate_count"] == 9

    def test_bodies_has_stim(self):
        result = compute_circuit_data(STEANE_STIM)
        formats = [b["format"] for b in result["bodies"]]
        assert "stim" in formats
        stim_body = next(b for b in result["bodies"] if b["format"] == "stim")
        assert len(stim_body["body"]) > 0

    def test_qasm_output(self):
        result = compute_circuit_data(STEANE_STIM)
        formats = [b["format"] for b in result["bodies"]]
        assert "qasm" in formats
        qasm_body = next(b for b in result["bodies"] if b["format"] == "qasm")
        assert "OPENQASM 2.0" in qasm_body["body"]

    def test_crumble_url(self):
        result = compute_circuit_data(STEANE_STIM)
        assert result["crumble_url"].startswith("https://algassert.com/crumble")

    def test_quirk_url(self):
        result = compute_circuit_data(STEANE_STIM)
        assert result["quirk_url"].startswith("https://algassert.com/quirk")

    def test_no_permutation_stores_original(self):
        result = compute_circuit_data(STEANE_STIM)
        assert isinstance(result["original_stim"], str)
        assert len(result["original_stim"]) > 0

    @pytest.mark.skipif(not _mqt_available, reason="mqt-qecc not available")
    def test_with_permutation_stores_original(self):
        perm = [0, 1, 2, 3, 4, 5, 6]  # identity permutation
        result = compute_circuit_data(
            STEANE_STIM,
            qubit_permutation=perm,
        )
        assert result["original_stim"] is not None
        assert len(result["original_stim"]) > 0

    def test_metadata_fields(self):
        result = compute_circuit_data(
            STEANE_STIM,
            circuit_name="Test",
            source="doi:test",
            tool="mqt-qecc",
            notes="A test circuit",
        )
        assert result["source"] == "doi:test"
        assert result["tool"] == "mqt-qecc"
        assert result["notes"] == "A test circuit"


def test_ticked_circuit_skips_compaction():
    """A submitted TICK schedule survives ingestion: compaction (which strips
    TICKs and re-packs) is skipped for circuits containing TICKs."""
    from scripts.add_circuit.compute_circuit import compute_circuit_data

    data = compute_circuit_data("H 0\nTICK\nCX 0 1\nTICK\nCX 2 3\n")
    stim_body = next(b["body"] for b in data["bodies"] if b["format"] == "stim")
    assert stim_body.count("TICK") == 2
    assert data["depth"] == 2  # TICK layers authoritative


def test_relabel_preserves_measurement_record_targets():
    """Classically-controlled Paulis (CX rec[-k] q) must survive relabeling."""
    from scripts.add_circuit.compute_circuit import _relabel_qubits
    import stim

    circ = stim.Circuit("H 0\nCX 0 1\nMR 2\nCX rec[-1] 1")
    out = _relabel_qubits(circ, [1, 0])  # swap qubits 0 and 1
    assert str(out).splitlines() == ["H 1", "CX 1 0", "MR 2", "CX rec[-1] 0"]
