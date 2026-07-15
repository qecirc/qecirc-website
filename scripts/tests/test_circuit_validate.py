"""
Tests for circuit_validate.py.
"""

import numpy as np
import pytest

from scripts.add_circuit.circuit_validate import (
    circuit_properties,
    extract_code,
    validate_encoding,
    validate_encoding_h,
    validate_state_prep,
    validate_state_prep_h,
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
        # 2q-entangling depth (TICKs ignored): CNOT(0,1) layer 1, CNOT(0,2) layer 2.
        props = circuit_properties(CIRCUIT_WITH_TICKS)
        assert props.depth == 2

    def test_depth_no_ticks(self):
        props = circuit_properties(ENCODING_CIRCUIT)
        # 2q-entangling depth (single-qubit H ignored): CNOT(0,1) layer 1,
        # CNOT(0,2) layer 2, CNOT(0,3) layer 3.
        assert props.depth == 3

    def test_gate_count(self):
        props = circuit_properties(ENCODING_CIRCUIT)
        # H + 3 x CNOT = 4 gates (QUBIT_COORDS excluded)
        assert props.gate_count == 4

    def test_two_qubit_gate_count(self):
        props = circuit_properties(ENCODING_CIRCUIT)
        # 3 x CNOT (H is single-qubit, not counted)
        assert props.two_qubit_gate_count == 3

    def test_empty_circuit(self):
        props = circuit_properties(EMPTY_CIRCUIT)
        assert props.qubit_count == 0
        assert props.gate_count == 0
        assert props.two_qubit_gate_count == 0

    def test_repeat_gate_count(self):
        props = circuit_properties(CIRCUIT_WITH_REPEAT)
        # H(1) + 10*(CNOT + CNOT) + H(1) = 22
        assert props.gate_count == 22

    def test_repeat_two_qubit_gate_count(self):
        props = circuit_properties(CIRCUIT_WITH_REPEAT)
        # 10*(CNOT + CNOT) = 20
        assert props.two_qubit_gate_count == 20

    def test_repeat_depth(self):
        props = circuit_properties(CIRCUIT_WITH_REPEAT)
        # 2q-entangling depth: 10 * (CNOT(0,1) layer 1, CNOT(0,2) layer 2) = 20
        assert props.depth == 20

    def test_repeat_qubit_count(self):
        props = circuit_properties(CIRCUIT_WITH_REPEAT)
        # Qubits 0, 1, 2
        assert props.qubit_count == 3

    def test_nested_repeat_gate_count(self):
        props = circuit_properties(CIRCUIT_NESTED_REPEAT)
        # 5*(H) + 5*3*(CNOT) = 20
        assert props.gate_count == 20

    def test_nested_repeat_two_qubit_gate_count(self):
        props = circuit_properties(CIRCUIT_NESTED_REPEAT)
        # 5*3*(CNOT) = 15
        assert props.two_qubit_gate_count == 15

    def test_nested_repeat_depth(self):
        props = circuit_properties(CIRCUIT_NESTED_REPEAT)
        # 2q-entangling depth: 5 * (3 * CNOT(0,1) layer 1) = 15
        assert props.depth == 15


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

    def test_reset_encoder_passes_via_simulation(self):
        # Ancilla-initialising encoders contain resets and have no unitary
        # tableau; validate_encoding must fall back to simulation. Prepending
        # a reset of all qubits is a no-op on |0...0> but forces that path.
        reset_encoder = "R 0 1 2 3 4 5 6\n" + STEANE_STIM
        assert validate_encoding(reset_encoder, STEANE_H, STEANE_H) == "passed"

    def test_reset_encoder_bad_fails(self):
        # A reset-containing circuit that does not prepare a codeword must
        # still be reported as failed (not error out) via the fallback.
        result = validate_encoding("R 0 1 2 3 4 5 6\nH 0\n", STEANE_H, STEANE_H)
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
# Symplectic (non-CSS-capable) validators
# ---------------------------------------------------------------------------

# The five-qubit perfect code: non-CSS, so it has no Hx/Hz split at all.
FIVE_QUBIT_H = np.array(
    [
        [1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
        [0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
    ]
)

FIVE_QUBIT_ENCODER = """\
S 4
X 0
S_DAG 1
H 2
Z 3
H 4 0 1
SWAP 4 0 1 3
S_DAG 0
SWAP 4 2
H 3 1
S_DAG 2 4
S 3
S_DAG 1
H 3
CZ 1 0
H 0
S_DAG 1
CZ 3 4
S 0
S_DAG 4
Y 3
H 0
S_DAG 3
H 3
CZ 2 0 3 1
H 0
S_DAG 2
H 1 3
CZ 2 4
S_DAG 3
CZ 3 0
"""


class TestSymplecticValidators:
    def test_non_css_encoder_passes(self):
        assert validate_encoding_h(FIVE_QUBIT_ENCODER, FIVE_QUBIT_H, 5) == "passed"

    def test_non_css_bad_encoder_fails(self):
        assert validate_encoding_h("I 0 1 2 3 4", FIVE_QUBIT_H, 5).startswith("failed:")

    def test_non_css_state_prep_fails_on_product_state(self):
        assert validate_state_prep_h("I 0 1 2 3 4", FIVE_QUBIT_H, 5).startswith("failed:")

    def test_css_wrapper_agrees_with_symplectic(self):
        # Steane via the CSS wrapper and via an explicitly assembled h.
        zeros = np.zeros_like(STEANE_H)
        h = np.vstack([np.hstack([STEANE_H, zeros]), np.hstack([zeros, STEANE_H])])
        assert validate_encoding_h(STEANE_STIM, h, 7) == "passed"
        assert validate_encoding(STEANE_STIM, STEANE_H, STEANE_H) == "passed"

    def test_wrong_h_width_raises(self):
        with pytest.raises(ValueError, match="columns"):
            validate_encoding_h(FIVE_QUBIT_ENCODER, FIVE_QUBIT_H, 4)

    def test_circuit_narrower_than_code_is_padded(self):
        # stim sizes a circuit by its highest touched qubit, so an encoder that
        # never touches the last data qubits is narrower than n. That must not
        # be mistaken for a width mismatch.
        h = np.array([[0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]])
        assert validate_state_prep_h("I 0", h, 3) == "passed"


class TestSignTolerance:
    """``codes.h`` is sign-free, so a codeword prepared in a different Pauli
    frame is still a valid preparation of the same code and must pass."""

    def test_state_prep_accepts_negative_frame(self):
        # |1> is stabilized by -Z; h names the sign-free row "Z".
        h = np.array([[0, 1]])
        assert validate_state_prep_h("X 0", h, 1) == "passed"

    def test_state_prep_rejects_non_eigenstate(self):
        # |+> is not a Z eigenstate at all: expectation 0, not ±1.
        assert validate_state_prep_h("H 0", np.array([[0, 1]]), 1).startswith("failed:")

    def test_encoding_accepts_negative_frame(self):
        # Same for the reset-fallback path (X 0 after a reset -> -Z frame).
        h = np.array([[0, 1]])
        assert validate_encoding_h("R 0\nX 0", h, 1) == "passed"

    def test_negative_frame_steane_state_prep(self):
        # Flipping a data qubit of a Steane |0_L> prep lands in the codespace
        # with some stabilizer signs flipped — still a codeword of the same code.
        flipped = STEANE_STATE_PREP + "Z 0\n"
        zeros = np.zeros_like(STEANE_H)
        h = np.vstack([np.hstack([STEANE_H, zeros]), np.hstack([zeros, STEANE_H])])
        assert validate_state_prep_h(flipped, h, 7) == "passed"


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


class TestTickAuthoritativeDepth:
    def test_tick_layers_not_repacked(self):
        """Two CNOTs on disjoint qubits in separate TICK layers: the given
        schedule is authoritative (depth 2), even though ASAP packing would
        merge them into one layer."""
        props = circuit_properties("CX 0 1\nTICK\nCX 2 3\n")
        assert props.depth == 2

    def test_same_circuit_without_ticks_is_repacked(self):
        props = circuit_properties("CX 0 1\nCX 2 3\n")
        assert props.depth == 1

    def test_single_qubit_only_tick_layers_dont_count(self):
        """TICK layers with no entangling gate contribute no depth."""
        props = circuit_properties("H 0\nTICK\nCX 0 1\nTICK\nS 1\n")
        assert props.depth == 1
