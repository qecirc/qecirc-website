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

def check_commutativity(Hx: np.ndarray, Hz: np.ndarray) -> bool:
    """Verify all stabilizer generators mutually commute: Hx·Hz^T + Hz·Hx^T = 0 mod 2."""
    return bool(np.all((Hx @ Hz.T + Hz @ Hx.T) % 2 == 0))


def is_css(Hx: np.ndarray, Hz: np.ndarray) -> bool:
    """CSS codes satisfy Hx·Hz^T = 0 mod 2 (X and Z generators commute independently)."""
    return bool(np.all((Hx @ Hz.T) % 2 == 0))


def extract_params(Hx: np.ndarray, Hz: np.ndarray) -> CodeParams:
    """Extract (n, k) and detect CSS vs general stabilizer."""
    n = Hx.shape[1]
    css = is_css(Hx, Hz)
    if css:
        k = n - gf2_rank(Hx) - gf2_rank(Hz)
    else:
        k = n - gf2_rank(np.vstack([Hx, Hz]))
    return CodeParams(n=n, k=k, is_css=css)


# ---------------------------------------------------------------------------
# Canonicalization
# ---------------------------------------------------------------------------

def canonical_hash(Hx: np.ndarray, Hz: np.ndarray) -> str:
    """
    Stable hash for code identity. Uses RREF of the combined symplectic matrix
    [Hx | Hz] so that equivalent generator sets produce the same hash.
    """
    symplectic = np.hstack([Hx, Hz])
    canonical = gf2_rref(symplectic)
    return hashlib.sha256(canonical.tobytes()).hexdigest()


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

    Uses a column-weight-profile prefilter then tries candidate permutations.
    Returns None if no permutation is found (codes may be inequivalent, or the
    search space was too large).

    NOTE: This is a best-effort heuristic. For large codes it may not find a
    permutation even when one exists.
    """
    n = Hx_new.shape[1]
    if Hx_ref.shape[1] != n:
        return None

    # Prefilter: column weight profiles must match
    def col_weights(Hx, Hz):
        return sorted(
            (int(Hx[:, i].sum()), int(Hz[:, i].sum())) for i in range(Hx.shape[1])
        )

    if col_weights(Hx_new, Hz_new) != col_weights(Hx_ref, Hz_ref):
        return None

    # For small codes, try all permutations (n <= 12 only to stay fast)
    if n > 12:
        return None

    from itertools import permutations

    target_Hx = gf2_rref(Hx_ref)
    target_Hz = gf2_rref(Hz_ref)

    for perm in permutations(range(n)):
        perm = list(perm)
        if np.array_equal(gf2_rref(Hx_new[:, perm]), target_Hx) and np.array_equal(
            gf2_rref(Hz_new[:, perm]), target_Hz
        ):
            return perm

    return None
