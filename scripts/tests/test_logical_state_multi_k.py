"""logical_state_of / logical_basis_of for codes with k > 1 logical qubits."""

import numpy as np

from scripts.add_circuit.state_prep import logical_basis_of, logical_state_of

# [[4,2,2]] code: Hx = Hz = [1 1 1 1], k = 2.
H422 = np.array([[1, 1, 1, 1]])

# |00>_L = (|0000> + |1111>)/sqrt(2)
ZERO_CIRCUIT = """
H 0
CX 0 1 0 2 0 3
"""

# |++>_L = transversal H of |00>_L
PLUS_CIRCUIT = """
H 0
CX 0 1 0 2 0 3
H 0 1 2 3
"""


def test_zero_state_k2():
    assert logical_state_of(ZERO_CIRCUIT, 4, 2, Hx=H422, Hz=H422) == "zero"
    assert logical_basis_of(ZERO_CIRCUIT, 4, 2, Hx=H422, Hz=H422) == "z"


def test_plus_state_k2():
    assert logical_state_of(PLUS_CIRCUIT, 4, 2, Hx=H422, Hz=H422) == "plus"
    assert logical_basis_of(PLUS_CIRCUIT, 4, 2, Hx=H422, Hz=H422) == "x"


def test_basis_survives_mixed_logical_signs():
    """The 0/1 label needs the Z-bar signs to be unanimous; the basis does not.

    Flipping one logical qubit gives |01>_L — still unambiguously a Z-basis
    eigenstate, but with one Z-bar at -1. logical_state_of must fall through to
    'unknown', while logical_basis_of must still say 'z'. This is the case the
    old wrapper implementation got wrong, and it is not exotic: because the
    logicals are recomputed from sign-free matrices, a genuine |0...0>_L on a
    multi-k code lands here routinely.
    """
    from scripts.add_circuit.compute import _compute_logicals_css

    # Apply a logical X to one of the two logical qubits of |00>_L.
    lx, _ = _compute_logicals_css(H422, H422, 2)
    flip = "".join(f"X {i}\n" for i in range(4) if lx[0][i])
    mixed = ZERO_CIRCUIT + flip

    assert logical_state_of(mixed, 4, 2, Hx=H422, Hz=H422) == "unknown"
    assert logical_basis_of(mixed, 4, 2, Hx=H422, Hz=H422) == "z"


def test_no_uniform_basis_is_unknown():
    """A state with no uniform single-basis logical label must still report
    'unknown' — the sign tolerance must not swallow this case into 'z'/'x'."""
    # A physical Hadamard on one data qubit leaves the codespace entirely.
    assert logical_basis_of(ZERO_CIRCUIT + "H 0\n", 4, 2, Hx=H422, Hz=H422) == "unknown"


def test_k0_has_no_logical_state():
    """With no logical qubits there is no logical state; the all() guards would
    otherwise be vacuously true and report 'zero'/'z'."""
    # [[2,0,?]]: Hx = Hz = [1 1] leaves k = 0.
    h = np.array([[1, 1]])
    assert logical_state_of("H 0\nCX 0 1", 2, 1, Hx=h, Hz=h) == "unknown"
    assert logical_basis_of("H 0\nCX 0 1", 2, 1, Hx=h, Hz=h) == "unknown"
