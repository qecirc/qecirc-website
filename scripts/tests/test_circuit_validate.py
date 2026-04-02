"""
Tests for circuit_validate.py.
"""

import numpy as np
import pytest

from scripts.add_circuit.circuit_validate import (
    circuit_properties,
    extract_code,
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


# ---------------------------------------------------------------------------
# extract_code
# ---------------------------------------------------------------------------

STEANE_STATE_PREP = """\
H 0 3 5
CX 3 1 5 4 0 2 4 3 1 0 1 6 2 4 4 6
"""


class TestExtractCode:
    def test_encoding_steane(self):
        result = extract_code(STEANE_STIM, circuit_type="encoding", k=1)
        assert result.n == 7
        assert result.k == 1
        assert result.is_css is True
        # Should have 3 X-stabilizer generators and 3 Z-stabilizer generators
        from scripts.add_circuit.code_identify import gf2_rank, is_css

        assert result.Hx.shape == (3, 7)
        assert result.Hz.shape == (3, 7)
        assert gf2_rank(result.Hx) == 3
        assert gf2_rank(result.Hz) == 3
        assert is_css(result.Hx, result.Hz)

    def test_state_prep_steane(self):
        result = extract_code(STEANE_STATE_PREP, circuit_type="state_prep", k=1)
        assert result.n == 7
        assert result.k == 1
        assert result.is_css is True
        assert result.Hx.shape[0] == 3  # rank(Hx) = 3
        assert result.Hz.shape[0] == 3  # rank(Hz) = 3

    def test_round_trip_encoding(self):
        """Extract code from circuit, then validate the circuit against extracted matrices."""
        result = extract_code(STEANE_STIM, circuit_type="encoding", k=1)
        assert validate_encoding(STEANE_STIM, result.Hx, result.Hz) == "passed"

    def test_round_trip_state_prep(self):
        """Extract code from state-prep circuit, then validate against extracted matrices."""
        result = extract_code(STEANE_STATE_PREP, circuit_type="state_prep", k=1)
        assert validate_state_prep(STEANE_STATE_PREP, result.Hx, result.Hz) == "passed"

    def test_trivial_k0(self):
        """k=0 encoding: all qubits are ancilla, all Z stabilizers."""
        # 2-qubit identity circuit (no gates) with k=0
        result = extract_code("I 0\nI 1", circuit_type="encoding", k=0)
        assert result.n == 2
        assert result.k == 0
        assert result.is_css is True
        # Z on each qubit → Hz = identity, Hx = empty
        assert result.Hz.shape == (2, 2)
        assert result.Hx.shape[0] == 0

    def test_invalid_circuit_type(self):
        with pytest.raises(ValueError, match="Unknown circuit_type"):
            extract_code(STEANE_STIM, circuit_type="invalid", k=1)

    def test_encoding_wrong_k(self):
        with pytest.raises(ValueError, match="k=.*must satisfy"):
            extract_code(STEANE_STIM, circuit_type="encoding", k=8)
