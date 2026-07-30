"""Check-matrix anchors for the ILP flag-based state-prep import (arXiv:2607.22498).

The generator supports below are extracted mechanically from the paper's
"Stabilizer Tableaux" appendix (``HighDistanceStatePrep.tex``) — see README.
They are in the paper's own qubit numbering, which the paper's circuits use
directly (verified: every generator has expectation +1 on the corresponding
simulated prep state).  The [[16,1,4]] rotated-surface-code anchor is not in
the paper; it is the textbook d=4 rotated surface layout in row-major order,
which the paper also uses (verified the same way).

The extraction splits generator lists on line breaks as well as commas (one
generator per tex line, some lines holding two), which keeps it robust to the
tex's formatting — the [[24,10,4]] Z block parses to its intended 7
generators this way.
"""

import numpy as np

# --- verbatim from the paper appendix (1-based qubit indices) -------------

# [[16,4,4]] "low-weight" code (weight-six stabilizers, from projecting the
# [[16,6,4]] Reed-Muller code onto a logical Bell pair). Self-dual: X and Z
# generators share supports.
S_16_4_4_X = [
    [3, 4, 6, 8, 10, 11],
    [1, 2, 6, 8, 9, 12],
    [6, 7, 10, 12, 15, 16],
    [6, 7, 9, 11, 13, 14],
    [1, 3, 5, 6, 14, 15],
    [1, 2, 5, 7, 10, 11],
]
S_16_4_4_Z = [
    [3, 4, 6, 8, 10, 11],
    [1, 2, 6, 8, 9, 12],
    [6, 7, 10, 12, 15, 16],
    [6, 7, 9, 11, 13, 14],
    [1, 3, 5, 6, 14, 15],
    [1, 2, 5, 7, 10, 11],
]

# [[24,10,4]] two-block group algebra code
S_24_10_4_X = [
    [1, 3, 6, 8, 13, 17, 18, 23],
    [2, 4, 5, 11, 14, 18, 20, 23],
    [3, 7, 10, 11, 15, 18, 22, 24],
    [4, 6, 9, 12, 16, 22, 23, 24],
    [2, 3, 5, 6, 13, 15, 16, 17],
    [4, 6, 7, 10, 15, 18, 19, 21],
    [1, 5, 7, 12, 13, 14, 19, 22],
]
S_24_10_4_Z = [
    [1, 5, 7, 9, 13, 19, 20, 22],
    [2, 7, 8, 9, 14, 17, 21, 24],
    [3, 5, 6, 8, 13, 15, 17, 23],
    [4, 5, 8, 11, 14, 16, 18, 20],
    [1, 5, 10, 12, 14, 17, 19, 22],
    [1, 2, 3, 6, 13, 16, 17, 18],
    [6, 7, 10, 11, 15, 18, 19, 24],
]

# [[24,4,5]] two-block group algebra code
S_24_4_5_X = [
    [6, 9, 13, 18, 19, 20, 21, 22],
    [7, 11, 14, 17, 19, 21, 23, 24],
    [8, 10, 13, 15, 17, 20, 22, 23],
    [5, 12, 14, 16, 17, 18, 20, 24],
    [3, 12, 14, 15, 17, 19, 22, 24],
    [2, 7, 13, 14, 16, 17, 18, 19],
    [1, 11, 13, 15, 18, 19, 23, 24],
    [4, 10, 13, 16, 20, 21, 22, 24],
    [2, 6, 14, 16, 18, 21, 22, 23],
    [4, 5, 15, 16, 17, 18, 21, 22],
]
S_24_4_5_Z = [
    [1, 3, 6, 7, 8, 11, 19, 23],
    [2, 4, 5, 6, 9, 11, 18, 21],
    [3, 5, 7, 10, 11, 12, 17, 24],
    [4, 6, 8, 9, 10, 12, 20, 22],
    [2, 3, 4, 5, 6, 10, 16, 22],
    [1, 4, 6, 7, 9, 10, 13, 21],
    [1, 2, 5, 6, 7, 12, 14, 18],
    [1, 3, 4, 8, 11, 12, 15, 24],
    [1, 2, 8, 9, 10, 11, 13, 23],
    [1, 3, 5, 8, 9, 10, 15, 20],
]

# [[42,10,6]] two-block group algebra code
S_42_10_6_X = [
    [4, 12, 19, 26, 32, 33, 35, 40],
    [6, 16, 20, 27, 31, 40, 41, 42],
    [5, 15, 19, 26, 37, 39, 40, 41],
    [7, 10, 21, 28, 32, 34, 41, 42],
    [8, 11, 13, 22, 29, 33, 34, 42],
    [1, 3, 12, 22, 24, 34, 35, 38],
    [2, 14, 17, 22, 23, 30, 38, 39],
    [4, 9, 18, 25, 36, 38, 39, 40],
    [1, 6, 10, 26, 27, 28, 31, 38],
    [3, 14, 19, 23, 24, 29, 35, 41],
    [2, 9, 20, 23, 24, 25, 30, 42],
    [4, 15, 21, 23, 25, 26, 34, 36],
    [2, 11, 18, 25, 31, 32, 33, 39],
    [5, 13, 16, 22, 25, 26, 27, 37],
    [7, 11, 17, 27, 28, 29, 32, 39],
    [5, 14, 20, 27, 30, 33, 35, 41],
]
S_42_10_6_Z = [
    [5, 6, 7, 14, 20, 27, 30, 41],
    [7, 10, 11, 12, 21, 28, 32, 34],
    [6, 10, 11, 16, 20, 27, 31, 42],
    [8, 11, 12, 13, 14, 22, 29, 33],
    [1, 3, 9, 12, 14, 24, 35, 38],
    [2, 9, 14, 15, 17, 23, 30, 39],
    [4, 9, 15, 16, 18, 25, 36, 40],
    [5, 10, 15, 16, 19, 26, 37, 41],
    [7, 11, 17, 18, 19, 29, 32, 39],
    [2, 9, 13, 20, 21, 25, 30, 42],
    [1, 4, 13, 15, 21, 26, 34, 36],
    [1, 5, 13, 16, 17, 22, 27, 37],
    [4, 5, 6, 12, 19, 26, 35, 40],
    [1, 6, 10, 17, 18, 28, 31, 38],
    [3, 14, 19, 20, 21, 23, 35, 41],
    [6, 7, 8, 9, 21, 28, 36, 42],
]


def _rows(supports, n, half):
    """Binary rows of shape (len(supports), 2n); half=0 -> X half, 1 -> Z half."""
    out = np.zeros((len(supports), 2 * n), dtype=int)
    for i, sup in enumerate(supports):
        for q in sup:
            out[i, half * n + q - 1] = 1
    return out


def symplectic(x_supports, z_supports, n):
    """Symplectic H from 1-based X- and Z-generator supports."""
    return np.vstack([_rows(x_supports, n, 0), _rows(z_supports, n, 1)])


def rotated_surface_d4():
    """Hx/Hz-derived symplectic H of the d=4 rotated surface code, row-major
    4x4 grid (qubit (r,c) -> 4r+c), X interior plaquettes at (r+c) even —
    exactly the paper's [[16,1,4]] labeling (verified against the circuit)."""
    D = 4
    xs, zs = [], []
    for r in range(D - 1):
        for c in range(D - 1):
            sup = [4 * r + c + 1, 4 * r + c + 2, 4 * (r + 1) + c + 1, 4 * (r + 1) + c + 2]
            (xs if (r + c) % 2 == 0 else zs).append(sup)
    for c in range(D - 1):
        if (-1 + c) % 2 == 0:
            xs.append([c + 1, c + 2])
        if (D - 1 + c) % 2 == 0:
            xs.append([4 * (D - 1) + c + 1, 4 * (D - 1) + c + 2])
    for r in range(D - 1):
        if (r - 1) % 2 == 1:
            zs.append([4 * r + 1, 4 * (r + 1) + 1])
        if (r + D - 1) % 2 == 1:
            zs.append([4 * r + D, 4 * (r + 1) + D])
    return symplectic(xs, zs, 16)


ANCHORS = {
    "16-1-4": rotated_surface_d4(),
    "16-4-4-low-weight": symplectic(S_16_4_4_X, S_16_4_4_Z, 16),
    "24-10-4": symplectic(S_24_10_4_X, S_24_10_4_Z, 24),
    "24-4-5": symplectic(S_24_4_5_X, S_24_4_5_Z, 24),
    "42-10-6": symplectic(S_42_10_6_X, S_42_10_6_Z, 42),
}
