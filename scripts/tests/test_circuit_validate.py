"""
Tests for circuit_validate.py.
"""

import pytest

from scripts.add_circuit.circuit_validate import (
    circuit_properties,
    classify_functionality,
)

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

CIRCUIT_WITH_REPEAT = """\
H 0
TICK
REPEAT 10 {
    CNOT 0 1
    TICK
    CNOT 0 2
    TICK
}
H 1
"""

CIRCUIT_NESTED_REPEAT = """\
REPEAT 5 {
    H 0
    TICK
    REPEAT 3 {
        CNOT 0 1
        TICK
    }
}
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
        assert props.qubit_count == 4

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
        assert props.qubit_count == 0
        assert props.gate_count == 0

    def test_repeat_gate_count(self):
        props = circuit_properties(CIRCUIT_WITH_REPEAT)
        # H(1) + 10*(CNOT + CNOT) + H(1) = 22
        assert props.gate_count == 22

    def test_repeat_depth(self):
        props = circuit_properties(CIRCUIT_WITH_REPEAT)
        # 1 TICK before REPEAT + 10 * 2 TICKs inside = 21
        assert props.depth == 21

    def test_repeat_qubit_count(self):
        props = circuit_properties(CIRCUIT_WITH_REPEAT)
        # Qubits 0, 1, 2
        assert props.qubit_count == 3

    def test_nested_repeat_gate_count(self):
        props = circuit_properties(CIRCUIT_NESTED_REPEAT)
        # 5*(H) + 5*3*(CNOT) = 20
        assert props.gate_count == 20

    def test_nested_repeat_depth(self):
        props = circuit_properties(CIRCUIT_NESTED_REPEAT)
        # 5*(1 TICK + 3*1 TICK) = 20
        assert props.depth == 20
