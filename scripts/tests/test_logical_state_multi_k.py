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
