"""
Code identification: canonicalization, DB lookup, and qubit permutation finding.

Heavy computation (mqt_qecc) is isolated to functions that can be
replaced or mocked independently.
"""

import hashlib
from typing import Optional

import numpy as np

from .models import CodeParams

# ---------------------------------------------------------------------------
# GF(2) linear algebra
# ---------------------------------------------------------------------------


def gf2_rref_pivots(M: np.ndarray) -> tuple[np.ndarray, list[int]]:
    """Reduced row echelon form over GF(2), also returning pivot column indices."""
    M = M.copy().astype(int) % 2
    rows, cols = M.shape
    pivot_row = 0
    pivots: list[int] = []
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if M[r, col]), None)
        if pivot is None:
            continue
        M[[pivot_row, pivot]] = M[[pivot, pivot_row]]
        for row in range(rows):
            if row != pivot_row and M[row, col]:
                M[row] = (M[row] + M[pivot_row]) % 2
        pivots.append(col)
        pivot_row += 1
    return M, pivots


def gf2_rref(M: np.ndarray) -> np.ndarray:
    """Reduced row echelon form over GF(2)."""
    return gf2_rref_pivots(M)[0]


def gf2_rank(M: np.ndarray) -> int:
    """Rank of a matrix over GF(2)."""
    _, pivots = gf2_rref_pivots(M)
    return len(pivots)


def gf2_nullspace(M: np.ndarray) -> np.ndarray:
    """Basis for the kernel of M over GF(2). Returns a k-by-n matrix."""
    M = np.atleast_2d(M).astype(int) % 2
    _rows, n = M.shape
    R, pivots = gf2_rref_pivots(M)
    pivot_set = set(pivots)
    free_cols = [c for c in range(n) if c not in pivot_set]
    if not free_cols:
        return np.empty((0, n), dtype=int)
    pivot_to_row = {col: i for i, col in enumerate(pivots)}
    basis = np.zeros((len(free_cols), n), dtype=int)
    for idx, f in enumerate(free_cols):
        basis[idx, f] = 1
        for pc in pivots:
            basis[idx, pc] = R[pivot_to_row[pc], f]
    return basis % 2


def gf2_row_basis(M: np.ndarray) -> np.ndarray:
    """Basis for the row space of M over GF(2). Returns non-zero rows of RREF."""
    R = gf2_rref(M)
    return R[np.any(R, axis=1)]


# ---------------------------------------------------------------------------
# Code classification
# ---------------------------------------------------------------------------


def is_css(Hx: np.ndarray, Hz: np.ndarray) -> bool:
    """CSS codes satisfy Hx*Hz^T = 0 mod 2 (X and Z generators commute independently)."""
    return bool(np.all((Hx @ Hz.T) % 2 == 0))


# ---------------------------------------------------------------------------
# Symplectic <-> CSS conversion
# ---------------------------------------------------------------------------


def build_symplectic_h(Hx: np.ndarray, Hz: np.ndarray) -> np.ndarray:
    """Build the block-diagonal symplectic h for a CSS code.

    Hx (m_x x n) and Hz (m_z x n) describe independent X- and Z-type
    stabilizer sets:
        h = [[Hx, 0], [0, Hz]]   shape (m_x + m_z) x 2n
    """
    Hx = np.asarray(Hx, dtype=int) % 2
    Hz = np.asarray(Hz, dtype=int) % 2
    m_x, n = Hx.shape
    m_z, n_z = Hz.shape
    if n_z != n:
        raise ValueError(f"Hx and Hz have different qubit counts: {n} vs {n_z}")
    top = np.hstack([Hx, np.zeros((m_x, n), dtype=int)])
    bot = np.hstack([np.zeros((m_z, n), dtype=int), Hz])
    return np.vstack([top, bot])


def build_symplectic_logical(
    Lx: np.ndarray, Lz: np.ndarray, n: int, k: int
) -> np.ndarray:
    """Build the symplectic logical matrix for a CSS code.

    Returns shape (2k, 2n): rows 0..k-1 are X-bar logicals (pure X),
    rows k..2k-1 are Z-bar logicals (pure Z). Non-CSS codes use
    :func:`_compute_symplectic_logicals` and skip this function.
    """
    Lx = np.asarray(Lx, dtype=int) % 2
    Lz = np.asarray(Lz, dtype=int) % 2
    if Lx.shape != (k, n) or Lz.shape != (k, n):
        raise ValueError(f"Expected Lx, Lz of shape ({k}, {n}); got {Lx.shape}, {Lz.shape}")
    top = np.hstack([Lx, np.zeros((k, n), dtype=int)])
    bot = np.hstack([np.zeros((k, n), dtype=int), Lz])
    return np.vstack([top, bot])


def split_h_to_css(H: np.ndarray, n: int) -> Optional[tuple[np.ndarray, np.ndarray]]:
    """Detect CSS structure in a symplectic h matrix and split into (Hx, Hz).

    Returns (Hx, Hz) when every RREF row of H is either pure-X (Z-half zero)
    or pure-Z (X-half zero); otherwise returns None.

    RREF processes columns left-to-right, so the X-half pivots come before
    the Z-half pivots. If the row space is CSS-decomposable this yields a
    basis where each row is purely in one half.
    """
    H = np.asarray(H, dtype=int) % 2
    if H.shape[1] != 2 * n:
        raise ValueError(f"Expected H with 2n={2 * n} columns, got {H.shape[1]}")
    rref = gf2_rref(H)
    rref = rref[np.any(rref, axis=1)]
    pure_x: list[np.ndarray] = []
    pure_z: list[np.ndarray] = []
    for row in rref:
        x_part = row[:n]
        z_part = row[n:]
        if not z_part.any():
            pure_x.append(x_part)
        elif not x_part.any():
            pure_z.append(z_part)
        else:
            return None
    Hx = np.array(pure_x, dtype=int) if pure_x else np.zeros((0, n), dtype=int)
    Hz = np.array(pure_z, dtype=int) if pure_z else np.zeros((0, n), dtype=int)
    return Hx, Hz


def is_h_css(H: np.ndarray, n: int) -> bool:
    """True iff H is CSS-decomposable (see :func:`split_h_to_css`)."""
    return split_h_to_css(H, n) is not None


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


def canonical_form_h(H: np.ndarray, n: int) -> tuple[np.ndarray, list[int]]:
    """Canonicalize a symplectic stabilizer matrix H of shape (m, 2n).

    Mirrors :func:`canonical_form` but operates on a single H matrix without
    splitting into Hx/Hz halves — required for non-CSS codes where each row
    mixes X and Z.

    Steps:
    1. RREF of H over GF(2), drop zero rows.
    2. Sort qubits by their joint (X_col, Z_col) profile.
    3. Reapply the qubit permutation to both halves and re-RREF.

    Returns (canon_H, qubit_perm) where qubit_perm maps canonical column
    index -> original column index.
    """
    H = np.asarray(H, dtype=int) % 2
    if H.shape[1] != 2 * n:
        raise ValueError(f"Expected H with 2n={2 * n} columns, got {H.shape[1]}")

    rref = gf2_rref(H)
    rref = rref[np.any(rref, axis=1)]
    # Sort qubits by joint X/Z column profile (qubit j has X-col rref[:, j]
    # and Z-col rref[:, j+n]).
    joint_cols = np.vstack([rref[:, :n], rref[:, n:]])
    joint_keys = [(tuple(joint_cols[:, j].tolist()), j) for j in range(n)]
    joint_keys.sort()
    qubit_perm = [k[1] for k in joint_keys]

    z_indices = [n + p for p in qubit_perm]
    permuted = np.hstack([H[:, qubit_perm], H[:, z_indices]])
    canon = gf2_rref(permuted)
    canon = canon[np.any(canon, axis=1)]
    return canon, qubit_perm


def canonical_hash_h(H: np.ndarray, n: int) -> str:
    """Stable hash for any stabilizer code given by a single symplectic H matrix.

    Hashes the output of :func:`canonical_form_h`, which preserves the row
    pairing between X and Z parts (unlike halves-canonicalization) and works
    when X-half and Z-half row spaces have different ranks.

    Prefixed with ``sym:<n>:`` so it cannot collide with the CSS hash format
    (``<m_x>:<m_z>:``).
    """
    H = np.asarray(H, dtype=int) % 2
    if H.shape[1] != 2 * n:
        raise ValueError(f"Expected H with 2n={2 * n} columns, got {H.shape[1]}")
    canon, _ = canonical_form_h(H, n)
    prefix = f"sym:{n}:{canon.shape[0]}:".encode()
    return hashlib.sha256(prefix + canon.tobytes()).hexdigest()


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
