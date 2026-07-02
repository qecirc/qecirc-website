"""
Code identification: canonicalization, DB lookup, and qubit permutation finding.

Heavy computation (mqt_qecc) is isolated to functions that can be
replaced or mocked independently.
"""

import hashlib
import time
from typing import Literal, Optional

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


def build_symplectic_logical(Lx: np.ndarray, Lz: np.ndarray, n: int, k: int) -> np.ndarray:
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


def _pad_to_equal_rows(A: np.ndarray, B: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Zero-pad the row-shorter of two equal-width matrices so both have the
    same row count.

    A no-op when the row counts already match, so symmetric / self-dual CSS
    codes (``rank(Hx) == rank(Hz)``) are byte-for-byte unchanged and keep their
    existing :func:`canonical_hash`. For asymmetric CSS codes
    (``rank(Hx) != rank(Hz)``, e.g. the Shor code's 2 X- vs 6 Z-generators) it
    makes the ``np.hstack`` below well-defined; the padding rows are all-zero
    and are stripped again by the RREF zero-row removal, so they don't affect
    the canonicalization.
    """
    ra, rb = A.shape[0], B.shape[0]
    if ra == rb:
        return A, B
    r = max(ra, rb)
    if ra < r:
        A = np.vstack([A, np.zeros((r - ra, A.shape[1]), dtype=A.dtype)])
    if rb < r:
        B = np.vstack([B, np.zeros((r - rb, B.shape[1]), dtype=B.dtype)])
    return A, B


def canonical_form(Hx: np.ndarray, Hz: np.ndarray) -> tuple[np.ndarray, np.ndarray, list[int]]:
    """
    Compute the canonical representation of a code given by (Hx, Hz).

    Steps:
    1. RREF of [Hx | Hz] to canonicalize row space
    2. Sort qubit columns by their joint (X_col, Z_col) profile so that
       column permutations of the same code produce the same result

    Returns (canon_Hx, canon_Hz, column_permutation) where the permutation
    maps canonical column index -> original column index.

    ``Hx`` and ``Hz`` may have different row counts (CSS codes with
    ``rank(Hx) != rank(Hz)``); they are zero-padded to a common height before
    the joint RREF (a no-op for symmetric codes — see
    :func:`_pad_to_equal_rows`).
    """
    n = Hx.shape[1]
    Hx, Hz = _pad_to_equal_rows(Hx, Hz)
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
    Deterministic fingerprint of the (Hx, Hz) representation after RREF and
    sorting columns by joint column profile.

    Invariant under row operations and under **joint** row permutation of
    (Hx, Hz). Approximately invariant under qubit permutations for codes
    without non-trivial automorphisms, but **not** a true permutation
    invariant in general — codes with non-trivial qubit symmetries (e.g.
    bicycle-style LDPC codes like [[108,8,10]]) can yield different hashes
    for two qubit-permuted forms of the same code. Use
    :func:`is_permutation_equivalent` when you need a true equivalence test.

    Includes Hx/Hz row counts in the hash input to avoid collisions between
    codes with different generator splits but same concatenated bytes.
    """
    canon_Hx, canon_Hz, _ = canonical_form(Hx, Hz)
    # Row counts (before padding) go in the prefix so asymmetric codes keep a
    # distinct fingerprint; padding to equal heights makes the hstack valid and
    # is a no-op for symmetric codes (preserving their existing hash).
    prefix = f"{canon_Hx.shape[0]}:{canon_Hz.shape[0]}:".encode()
    canon_Hx, canon_Hz = _pad_to_equal_rows(canon_Hx, canon_Hz)
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
    """Deterministic fingerprint of a symplectic stabilizer matrix H.

    Hashes the output of :func:`canonical_form_h`. Like :func:`canonical_hash`,
    this is a stable fingerprint of the canonicalized representation, not a
    true permutation invariant — equivalent codes under different qubit
    orderings may hash differently when the code has non-trivial automorphisms.
    Use :func:`is_permutation_equivalent` for a real equivalence test.

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

    # Use gf2_row_basis (RREF with zero rows dropped) rather than gf2_rref so
    # the comparison works when Hx_new/Hz_new carry linearly dependent rows
    # that the stored reference matrices (post split_h_to_css) have already
    # shed.
    def _matches(perm: list[int]) -> bool:
        return np.array_equal(
            gf2_row_basis(Hx_new[:, perm]), gf2_row_basis(Hx_ref)
        ) and np.array_equal(gf2_row_basis(Hz_new[:, perm]), gf2_row_basis(Hz_ref))

    # Prefer identity when the orderings already match — callers rely on this
    # to skip circuit relabeling.
    identity = list(range(n))
    if _matches(identity):
        return identity

    _, _, perm_new = canonical_form(Hx_new, Hz_new)

    # When (Hx_ref, Hz_ref) is already in canonical form (how _check_yaml_dedup
    # builds it from the stored canonical h), perm_new alone is the relabeling
    # we want. This also sidesteps non-idempotency of canonical_form on its own
    # output for high-symmetry codes (e.g. [[108,8,10]]).
    if _matches(perm_new):
        return perm_new

    # General path: compose perm_new with the inverse of canonical_form(ref).
    # Required when ref is not in canonical form (e.g. test inputs that pass
    # the original textbook matrices as the reference).
    _, _, perm_ref = canonical_form(Hx_ref, Hz_ref)
    inv_perm_ref = [0] * n
    for canon_pos, ref_qubit in enumerate(perm_ref):
        inv_perm_ref[ref_qubit] = canon_pos
    result = [perm_new[inv_perm_ref[r]] for r in range(n)]
    if _matches(result):
        return result

    return None


# ---------------------------------------------------------------------------
# Permutation equivalence with bounded search
# ---------------------------------------------------------------------------


PermEquivStatus = Literal["equivalent", "uncertain", "inequivalent"]


def _apply_qubit_perm_symplectic(H: np.ndarray, sigma: list[int], n: int) -> np.ndarray:
    """Apply qubit permutation σ to both X and Z halves of a symplectic H."""
    cols = list(sigma) + [s + n for s in sigma]
    return H[:, cols]


def _symplectic_self_orthogonal(H: np.ndarray, n: int) -> bool:
    """Check H · Λ · Hᵀ ≡ 0 (mod 2) where Λ = [[0, I_n], [I_n, 0]]."""
    H = H.astype(int) % 2
    # H · Λ swaps the X and Z halves of each row.
    H_lambda = np.hstack([H[:, n:], H[:, :n]])
    return bool(np.all((H_lambda @ H.T) % 2 == 0))


def _pauli_subspace_signature(B: np.ndarray, n: int) -> list[tuple]:
    """Per-qubit signature invariant under both row operations and column
    permutation (when paired with the same column permutation on j and j+n).

    For each qubit j, the row-space projected onto coords (j, j+n) is a
    subspace of F_2^2 — one of {0}, ⟨X⟩, ⟨Z⟩, ⟨Y⟩, or F_2^2. The sorted
    tuple of its non-zero elements uniquely identifies it.
    """
    sigs: list[tuple] = []
    for j in range(n):
        # The row-span is at most 4 vectors; enumerate by closure.
        seen: set[tuple[int, int]] = {(0, 0)}
        for r in range(B.shape[0]):
            v = (int(B[r, j]), int(B[r, j + n]))
            if v == (0, 0):
                continue
            seen = seen | {(a ^ v[0], b ^ v[1]) for (a, b) in seen}
            if len(seen) == 4:
                break
        sigs.append(tuple(sorted(v for v in seen if v != (0, 0))))
    return sigs


def _refine_partition(
    B1: np.ndarray, B2: np.ndarray, n: int
) -> Optional[tuple[list[list[int]], list[list[int]]]]:
    """Partition qubits by a column-permutation-invariant signature.

    Initial signature: per-qubit Pauli subspace of the row space (which Paulis
    appear at qubit j across all codewords). One refinement round using
    sorted pair-signatures with other qubits is applied to break symmetries.

    Returns (classes_1, classes_2) where classes_k[i] is the list of qubits
    in code k that share colour i, paired across the two codes. Returns None
    if the multisets of colours differ — codes are inequivalent.
    """
    sig1 = _pauli_subspace_signature(B1, n)
    sig2 = _pauli_subspace_signature(B2, n)
    if sorted(sig1) != sorted(sig2):
        return None

    # One-round pair refinement: for each qubit q, augment its colour with the
    # sorted multiset of pair-signatures (sig(q), sig(p), joint-dim(q, p)) for
    # all other qubits p. Joint-dim is the dimension of the row-space
    # projection onto (q, q+n, p, p+n) — a column-perm-invariant.
    def _joint_dim(B: np.ndarray, q: int, p: int) -> int:
        cols = np.stack([B[:, q], B[:, q + n], B[:, p], B[:, p + n]], axis=1).astype(int) % 2
        return gf2_rank(cols)

    def _augment(B: np.ndarray, base_sig: list[tuple]) -> list[tuple]:
        out = []
        for q in range(n):
            joint = sorted((base_sig[p], _joint_dim(B, q, p)) for p in range(n) if p != q)
            out.append((base_sig[q], tuple(joint)))
        return out

    aug1 = _augment(B1, sig1)
    aug2 = _augment(B2, sig2)
    if sorted(aug1) != sorted(aug2):
        return None

    colours = sorted(set(aug1) | set(aug2))
    classes_1 = [[q for q in range(n) if aug1[q] == c] for c in colours]
    classes_2 = [[q for q in range(n) if aug2[q] == c] for c in colours]
    # Drop empty classes (a colour might exist in one but not the other if the
    # multisets only differ in cardinality — but we already checked sorted equality).
    classes_1 = [cls for cls in classes_1 if cls]
    classes_2 = [cls for cls in classes_2 if cls]
    if any(len(a) != len(b) for a, b in zip(classes_1, classes_2)):
        return None
    return classes_1, classes_2


def is_permutation_equivalent(
    H1: np.ndarray,
    H2: np.ndarray,
    n: int,
    *,
    budget_seconds: float = 10.0,
) -> tuple[PermEquivStatus, Optional[list[int]]]:
    """Test whether two symplectic stabilizer matrices describe the same code
    up to qubit permutation σ ∈ S_n.

    Returns:
        ("equivalent", σ)     — H1 with qubits permuted by σ has the same row
                                space as H2 (σ applied to both X and Z halves).
        ("uncertain", None)   — cheap invariants agree but the search exhausted
                                its wall-clock budget. The codes may or may not
                                be equivalent.
        ("inequivalent", None) — cheap invariants prove inequivalence.
    """
    H1 = np.asarray(H1, dtype=int) % 2
    H2 = np.asarray(H2, dtype=int) % 2
    if H1.shape[1] != 2 * n or H2.shape[1] != 2 * n:
        return ("inequivalent", None)

    # Cheap rejection 1: rank (= n - k).
    if gf2_rank(H1) != gf2_rank(H2):
        return ("inequivalent", None)
    # Cheap rejection 2: symplectic self-orthogonality on both inputs.
    if not _symplectic_self_orthogonal(H1, n) or not _symplectic_self_orthogonal(H2, n):
        return ("inequivalent", None)

    # Reduce row-op ambiguity once: same row space ⇔ same matrix (for fixed
    # qubit ordering) after this normalization.
    B1 = gf2_row_basis(H1)
    B2 = gf2_row_basis(H2)
    if B1.shape != B2.shape:
        return ("inequivalent", None)

    # Identity shortcut.
    if np.array_equal(B1, B2):
        return ("equivalent", list(range(n)))

    # Cheap rejection via column-perm-invariant per-qubit signatures + one-round
    # pair refinement. _refine_partition returns None on multiset mismatch.
    parts = _refine_partition(B1, B2, n)
    if parts is None:
        return ("inequivalent", None)
    classes_1, classes_2 = parts

    # Backtracking: assign each qubit q1 in code 1 to a qubit q2 in code 2
    # within the same paired colour class. Order classes smallest-first so
    # forced assignments fire early.
    order = sorted(range(len(classes_1)), key=lambda i: len(classes_1[i]))
    classes_1 = [classes_1[i] for i in order]
    classes_2 = [classes_2[i] for i in order]

    # Precompute joint-dim tables: joint_dim_k[a][b] = dim of the projection
    # of code k's row space onto coords (a, a+n, b, b+n). This is a
    # column-perm-invariant pair signature, used to prune the backtracking.
    def _joint_dims(B: np.ndarray) -> np.ndarray:
        table = np.zeros((n, n), dtype=int)
        for a in range(n):
            for b in range(a, n):
                cols = (
                    np.stack([B[:, a], B[:, a + n], B[:, b], B[:, b + n]], axis=1).astype(int) % 2
                )
                d = gf2_rank(cols)
                table[a, b] = d
                table[b, a] = d
        return table

    jd1 = _joint_dims(B1)
    jd2 = _joint_dims(B2)

    # Flatten: for each qubit in code 1, what's its allowed set in code 2?
    allowed: list[list[int]] = [list() for _ in range(n)]
    qubit_order: list[int] = []  # order in which we assign qubits-of-code-1
    for c1, c2 in zip(classes_1, classes_2):
        for q1 in c1:
            allowed[q1] = list(c2)
            qubit_order.append(q1)

    sigma_1_to_2: list[int] = [-1] * n  # sigma_1_to_2[q1] = q2
    used: list[bool] = [False] * n
    assigned: list[int] = []  # ordered list of q1's already assigned
    start = time.monotonic()

    def _final_check() -> Optional[list[int]]:
        # σ_for_return[j] = qubit of code 1 that maps to position j in code 2,
        # i.e. inverse of sigma_1_to_2.
        sigma_for_return = [0] * n
        for q1, q2 in enumerate(sigma_1_to_2):
            sigma_for_return[q2] = q1
        permuted = _apply_qubit_perm_symplectic(B1, sigma_for_return, n)
        if np.array_equal(gf2_row_basis(permuted), B2):
            return list(sigma_for_return)
        return None

    def _recurse(idx: int) -> Optional[list[int]]:
        if time.monotonic() - start > budget_seconds:
            return None
        if idx == n:
            return _final_check()
        q1 = qubit_order[idx]
        for q2 in allowed[q1]:
            if used[q2]:
                continue
            # Pair-consistency prune: joint-dim with every already-assigned
            # qubit must match across the two codes.
            consistent = True
            for q1p in assigned:
                if jd1[q1, q1p] != jd2[q2, sigma_1_to_2[q1p]]:
                    consistent = False
                    break
            if not consistent:
                continue
            sigma_1_to_2[q1] = q2
            used[q2] = True
            assigned.append(q1)
            got = _recurse(idx + 1)
            if got is not None:
                return got
            assigned.pop()
            if time.monotonic() - start > budget_seconds:
                return None
            used[q2] = False
            sigma_1_to_2[q1] = -1
        return None

    found = _recurse(0)
    if found is not None:
        return ("equivalent", found)
    if time.monotonic() - start > budget_seconds:
        return ("uncertain", None)
    # Exhausted search → codes are inequivalent despite signatures matching.
    return ("inequivalent", None)
