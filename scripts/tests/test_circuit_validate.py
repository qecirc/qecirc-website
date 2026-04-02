"""
Tests for circuit_validate.py.
"""

import numpy as np

from scripts.add_circuit.circuit_validate import (
    circuit_properties,
    validate_encoding,
    validate_state_prep,
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

# Steane code fixtures for validation tests
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

STEANE_H = np.array(
    [
        [1, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 1, 1],
    ]
)


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


# ---------------------------------------------------------------------------
# validate_encoding
# ---------------------------------------------------------------------------


class TestValidateEncoding:
    def test_steane_encoding_passes(self):
        result = validate_encoding(STEANE_STIM, STEANE_H, STEANE_H)
        assert result == "passed"

    def test_steane_encoding_accepts_stim_circuit(self):
        import stim

        circ = stim.Circuit(STEANE_STIM)
        result = validate_encoding(circ, STEANE_H, STEANE_H)
        assert result == "passed"

    def test_bad_encoding_fails(self):
        # A circuit on 7 qubits that doesn't actually encode the Steane code
        bad_circuit = "H 0\nCNOT 0 1\nCNOT 0 2\nCNOT 0 3\nCNOT 0 4\nCNOT 0 5\nCNOT 0 6\n"
        result = validate_encoding(bad_circuit, STEANE_H, STEANE_H)
        assert result.startswith("failed:")


# ---------------------------------------------------------------------------
# validate_state_prep
# ---------------------------------------------------------------------------


class TestValidateStatePrep:
    def test_trivial_state_prep(self):
        # |00> is stabilized by ZI and IZ (Hx=0, Hz=identity)
        Hx = np.array([[0, 0], [0, 0]])
        Hz = np.array([[1, 0], [0, 1]])
        # Empty circuit (no gates) leaves |00> which is stabilized by Z
        result = validate_state_prep("", Hx, Hz)
        # Empty circuit has no instructions, so TableauSimulator stays at |0>
        assert result == "passed"
