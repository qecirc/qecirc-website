"""
Code identification: canonicalization, DB lookup, and qubit permutation finding.

Heavy computation (ldpc.mod2, mqt_qecc) is isolated to functions that can be
replaced or mocked independently.
"""

import hashlib
from typing import Optional

import numpy as np

from .models import CodeParams

# ---------------------------------------------------------------------------
# GF(2) linear algebra
# ---------------------------------------------------------------------------


def gf2_rref(M: np.ndarray) -> np.ndarray:
    """Reduced row echelon form over GF(2)."""
    M = M.copy().astype(int) % 2
    rows, cols = M.shape
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if M[r, col]), None)
        if pivot is None:
            continue
        M[[pivot_row, pivot]] = M[[pivot, pivot_row]]
        for row in range(rows):
            if row != pivot_row and M[row, col]:
                M[row] = (M[row] + M[pivot_row]) % 2
        pivot_row += 1
    return M


def gf2_rank(M: np.ndarray) -> int:
    """Rank of a matrix over GF(2)."""
    return int(np.any(gf2_rref(M), axis=1).sum())


# ---------------------------------------------------------------------------
# Code classification
# ---------------------------------------------------------------------------


def is_css(Hx: np.ndarray, Hz: np.ndarray) -> bool:
    """CSS codes satisfy Hx*Hz^T = 0 mod 2 (X and Z generators commute independently)."""
    return bool(np.all((Hx @ Hz.T) % 2 == 0))


def extract_params(Hx: np.ndarray, Hz: np.ndarray) -> CodeParams:
    """Extract (n, k) and detect CSS vs general stabilizer.

    For CSS codes, Hx and Hz are independent X/Z generator sets:
        k = n - rank(Hx) - rank(Hz)
    For non-CSS codes, row i of Hx/Hz are the X/Z parts of generator i:
        k = n - rank([Hx | Hz])  (symplectic matrix)
    """
    n = Hx.shape[1]
    css = is_css(Hx, Hz)
    if css:
        k = n - gf2_rank(Hx) - gf2_rank(Hz)
    else:
        k = n - gf2_rank(np.hstack([Hx, Hz]))
    return CodeParams(n=n, k=k, is_css=css)


# ---------------------------------------------------------------------------
# Canonicalization
# ---------------------------------------------------------------------------


def canonical_form(Hx: np.ndarray, Hz: np.ndarray) -> tuple[np.ndarray, np.ndarray, list[int]]:
    """
    Compute the canonical representation of a code given by (Hx, Hz).

    Steps:
    1. RREF of [Hx | Hz] to canonicalize row space
    2. Sort qubit columns by their joint (X_col, Z_col) profile so that
       column permutations of the same code produce the same result

    Returns (canon_Hx, canon_Hz, column_permutation) where the permutation
    maps canonical column index -> original column index.
    """
    n = Hx.shape[1]
    symplectic = np.hstack([Hx, Hz])
    rref = gf2_rref(symplectic)
    # Remove all-zero rows
    rref = rref[np.any(rref, axis=1)]
    # Sort qubits by their joint X and Z column profile.
    # Column j in X part and column j+n in Z part belong to the same qubit.
    joint_cols = np.vstack([rref[:, :n], rref[:, n:]])  # shape (2*rows, n)
    joint_keys = [(tuple(joint_cols[:, j].tolist()), j) for j in range(n)]
    joint_keys.sort()
    qubit_perm = [k[1] for k in joint_keys]

    canon_Hx = gf2_rref(Hx[:, qubit_perm])
    canon_Hz = gf2_rref(Hz[:, qubit_perm])
    # Remove all-zero rows
    canon_Hx = canon_Hx[np.any(canon_Hx, axis=1)]
    canon_Hz = canon_Hz[np.any(canon_Hz, axis=1)]

    return canon_Hx, canon_Hz, qubit_perm


def canonical_hash(Hx: np.ndarray, Hz: np.ndarray) -> str:
    """
    Stable hash for code identity. Invariant under row operations and column
    (qubit) permutations, so equivalent codes always produce the same hash.

    Includes Hx/Hz row counts in the hash input to avoid collisions between
    codes with different generator splits but same concatenated bytes.
    """
    canon_Hx, canon_Hz, _ = canonical_form(Hx, Hz)
    prefix = f"{canon_Hx.shape[0]}:{canon_Hz.shape[0]}:".encode()
    combined = np.hstack([canon_Hx, canon_Hz])
    return hashlib.sha256(prefix + combined.tobytes()).hexdigest()


# ---------------------------------------------------------------------------
# Qubit permutation
# ---------------------------------------------------------------------------


def find_qubit_permutation(
    Hx_new: np.ndarray,
    Hz_new: np.ndarray,
    Hx_ref: np.ndarray,
    Hz_ref: np.ndarray,
) -> Optional[list[int]]:
    """
    Find a column permutation mapping (Hx_new, Hz_new) to (Hx_ref, Hz_ref).

    Both codes must have the same canonical hash for this to succeed. The
    permutation is computed by canonicalizing both and composing:
        new_qubit_order -> canonical -> ref_qubit_order (inverse)

    Returns a permutation list p such that Hx_new[:, p] is row-equivalent to
    Hx_ref (and same for Hz), or None if no permutation exists.
    """
    n = Hx_new.shape[1]
    if Hx_ref.shape[1] != n:
        return None

    _, _, perm_new = canonical_form(Hx_new, Hz_new)
    _, _, perm_ref = canonical_form(Hx_ref, Hz_ref)

    # perm_new maps canonical position -> original new qubit
    # perm_ref maps canonical position -> original ref qubit
    # We want p such that new[:, p] ~ ref, i.e. for each ref qubit position j,
    # find which new qubit maps to the same canonical position.
    # inv_perm_ref[ref_qubit] = canonical_position
    inv_perm_ref = [0] * n
    for canon_pos, ref_qubit in enumerate(perm_ref):
        inv_perm_ref[ref_qubit] = canon_pos

    # result[ref_qubit_j] = new_qubit that maps to same canonical position
    result = [0] * n
    for ref_qubit in range(n):
        canon_pos = inv_perm_ref[ref_qubit]
        result[ref_qubit] = perm_new[canon_pos]

    # Verify the permutation actually works (RREF equivalence)
    if not np.array_equal(gf2_rref(Hx_new[:, result]), gf2_rref(Hx_ref)):
        return None
    if not np.array_equal(gf2_rref(Hz_new[:, result]), gf2_rref(Hz_ref)):
        return None

    return result
