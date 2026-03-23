"""
Tests for circuit_validate.py.

Stim-dependent checks (check_circuit_vs_matrices) are tested with stim mocked
so the suite runs without the stim package installed.
"""

from unittest.mock import patch

import pytest

from scripts.add_circuit.circuit_validate import (
    circuit_properties,
    classify_functionality,
    check_circuit_vs_matrices,
)

import numpy as np

# ---------------------------------------------------------------------------
# Sample circuits (minimal STIM snippets)
# ---------------------------------------------------------------------------

ENCODING_CIRCUIT = """\
QUBIT_COORDS(0, 0) 0
QUBIT_COORDS(1, 0) 1
QUBIT_COORDS(2, 0) 2
QUBIT_COORDS(3, 0) 3
H 0
CNOT 0 1
CNOT 0 2
CNOT 0 3
"""

SYNDROME_CIRCUIT = """\
H 4
CNOT 4 0
CNOT 4 1
M 4
"""

STATE_PREP_CIRCUIT = """\
R 0
R 1
R 2
"""

EMPTY_CIRCUIT = ""

CIRCUIT_WITH_TICKS = """\
H 0
TICK
CNOT 0 1
TICK
CNOT 0 2
"""


# ---------------------------------------------------------------------------
# classify_functionality
# ---------------------------------------------------------------------------

class TestClassifyFunctionality:
    def test_encoding_detected(self):
        assert classify_functionality(ENCODING_CIRCUIT) == "encoding"

    def test_syndrome_extraction_detected(self):
        assert classify_functionality(SYNDROME_CIRCUIT) == "syndrome-extraction"

    def test_state_preparation_detected(self):
        assert classify_functionality(STATE_PREP_CIRCUIT) == "state-preparation"

    def test_empty_circuit_returns_none(self):
        assert classify_functionality(EMPTY_CIRCUIT) is None

    def test_comments_ignored(self):
        circuit = "# This is a comment\nCNOT 0 1\n"
        assert classify_functionality(circuit) == "encoding"

    def test_case_insensitive(self):
        circuit = "cnot 0 1\n"
        assert classify_functionality(circuit) == "encoding"


# ---------------------------------------------------------------------------
# circuit_properties
# ---------------------------------------------------------------------------

class TestCircuitProperties:
    def test_qubit_count(self):
        props = circuit_properties(ENCODING_CIRCUIT)
        assert props.n_qubits == 4

    def test_depth_from_ticks(self):
        props = circuit_properties(CIRCUIT_WITH_TICKS)
        assert props.depth == 2

    def test_gate_count(self):
        props = circuit_properties(ENCODING_CIRCUIT)
        # H + 3 x CNOT = 4 gates (QUBIT_COORDS excluded)
        assert props.gate_count == 4

    def test_functionality_populated(self):
        props = circuit_properties(ENCODING_CIRCUIT)
        assert props.detected_functionality == "encoding"

    def test_empty_circuit(self):
        props = circuit_properties(EMPTY_CIRCUIT)
        assert props.n_qubits == 0
        assert props.gate_count == 0


# ---------------------------------------------------------------------------
# check_circuit_vs_matrices (stim mocked)
# ---------------------------------------------------------------------------

class TestCheckCircuitVsMatrices:
    def test_stim_not_installed_returns_invalid(self):
        Hx = np.array([[1, 1, 1, 1]])
        Hz = np.array([[1, 1, 1, 1]])
        with patch.dict("sys.modules", {"stim": None}):
            result = check_circuit_vs_matrices(ENCODING_CIRCUIT, Hx, Hz)
        assert not result.valid
        assert "stim" in result.mismatch_details.lower()

    def test_stim_parse_error_returns_invalid(self):
        Hx = np.array([[1, 1, 1, 1]])
        Hz = np.array([[1, 1, 1, 1]])
        # Pass gibberish that stim cannot parse
        try:
            import stim  # noqa: F401
            result = check_circuit_vs_matrices("NOT_A_VALID_STIM_INSTRUCTION 0", Hx, Hz)
            assert not result.valid
        except ImportError:
            pytest.skip("stim not installed")

    def test_too_few_qubits_returns_invalid(self):
        Hx = np.ones((1, 10), dtype=int)
        Hz = np.ones((1, 10), dtype=int)
        try:
            import stim  # noqa: F401
            # Circuit only touches 4 qubits, code needs 10
            result = check_circuit_vs_matrices(ENCODING_CIRCUIT, Hx, Hz)
            assert not result.valid
            assert "qubits" in result.mismatch_details
        except ImportError:
            pytest.skip("stim not installed")
