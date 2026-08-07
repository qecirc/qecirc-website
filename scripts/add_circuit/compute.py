"""
Code-level computation: parameters, logicals, canonicalization, tags, YAML dedup.
"""

import re
from pathlib import Path
from typing import Literal, NamedTuple, Optional

import numpy as np

from . import subsystem
from .code_identify import (
    build_symplectic_h,
    build_symplectic_logical,
    canonical_form,
    canonical_form_h,
    canonical_hash,
    canonical_hash_h,
    extract_params,
    find_qubit_permutation,
    gf2_nullspace,
    gf2_rank,
    gf2_row_basis,
    gf2_rref,
    gf2_rref_pivots,
    is_css,
    is_permutation_equivalent,
    split_h_to_css,
)
from .matrix_format import decode as decode_matrix
from .models import CodeParams, TagEntry
from .tag_suggest import suggest_code_tags
from .yaml_helpers import load_yaml

# Wall-clock budget (seconds) for the Phase-2 permutation-equivalence scan
# against each candidate code in the library. Surfaced as a constant so tests
# can override via monkeypatch when needed.
DEDUP_BUDGET_SECONDS = 10.0


class DedupResult(NamedTuple):
    """Result of YAML-based dedup against the stored library.

    status:
        "match"     — an existing code matched (hash or permutation-equivalent).
        "uncertain" — invariants agree with one or more stored codes but
                      permutation-equivalence could not be confirmed within
                      DEDUP_BUDGET_SECONDS. The caller should surface this to
                      the user rather than silently adding a duplicate.
        "new"       — no match.
    slug, qubit_permutation: set when status == "match".
    uncertain_candidates: stored slugs that look like possible matches but
        could not be confirmed; populated when status == "uncertain".
    """

    status: Literal["match", "uncertain", "new"]
    slug: Optional[str]
    qubit_permutation: Optional[list[int]]
    uncertain_candidates: list[str]


def compute_code_data(
    Hx: np.ndarray,
    Hz: np.ndarray,
    d: int,
    code_name: str = "",
    zoo_url: str = "",
    data_dir: Optional[str] = None,
    code_slug: str = "",
    code_tags: Optional[list[str]] = None,
) -> dict:
    """
    Compute all code-level data from Hx, Hz matrices.

    This entry point requires the input to be CSS (Hx · Hzᵀ = 0 mod 2). For
    general non-CSS codes, callers must use :func:`compute_code_data_h` with a
    single symplectic stabilizer matrix.

    Returns a dict with keys "code" (matching YAML code section) and
    "qubit_permutation" (mapping user qubits to canonical form, or None
    when the permutation is identity).
    """
    # 1. Parameters
    params = extract_params(Hx, Hz)
    if not params.is_css:
        raise ValueError(
            "Hx/Hz input requires a CSS code (Hx · Hzᵀ = 0 mod 2). For non-CSS "
            "codes, provide H directly via compute_code_data_h or "
            "add_circuit(H=..., n=...)."
        )

    # 2. Canonicalization
    canon_Hx, canon_Hz, qubit_perm = canonical_form(Hx, Hz)
    c_hash = canonical_hash(Hx, Hz)

    # 3. Logical operators (use canonical matrices so logicals match stored Hx/Hz)
    Lx, Lz = _compute_logicals_css(canon_Hx, canon_Hz, d)

    # 3b. The same logical operators, in the labelling they were submitted in.
    #     `canonical_form` only permutes columns and row-reduces, neither of
    #     which changes the code, so permuting the canonical logicals back is
    #     exact — and it makes the two sets agree about which logical qubit is
    #     which, where computing a second set from scratch would pick some other
    #     equally valid basis. It is also ~25 s cheaper per circuit on a
    #     [[544,80]] code. Verified rather than assumed; recomputation is the
    #     fallback if the permuted operators are not valid logicals.
    orig_Lx, orig_Lz = _logicals_in_original_order(Lx, Lz, qubit_perm, Hx, Hz)
    if orig_Lx is None:
        orig_Lx, orig_Lz = _compute_logicals_css(Hx, Hz, d)

    # 3c. Symplectic forms (always populated alongside the CSS view)
    h = build_symplectic_h(canon_Hx, canon_Hz)
    logical = build_symplectic_logical(Lx, Lz, n=params.n, k=params.k)
    orig_h = build_symplectic_h(Hx, Hz)
    orig_logical = build_symplectic_logical(orig_Lx, orig_Lz, n=params.n, k=params.k)

    # 4. Tags
    params_with_d = CodeParams(n=params.n, k=params.k, is_css=params.is_css, d=d)
    tags = suggest_code_tags(params_with_d)
    if _is_self_dual(Hx, Hz):
        tags.append(TagEntry(name="self-dual", status="confirmed"))
    # Caller-supplied family tags (e.g. "surface-code") — the pipeline only
    # auto-derives the mathematically verified ones (CSS, self-dual).
    for name in code_tags or []:
        tags.append(TagEntry(name=name, status="provided"))
    # Deduplicate by name (suggest_code_tags already adds CSS)
    seen = set()
    unique_tags = []
    for t in tags:
        if t.name not in seen:
            seen.add(t.name)
            unique_tags.append(t)
    tags = unique_tags

    # 5. Slug — an explicit code_slug wins so new codes can use the numeric
    # `n-k-d` convention (decoupled from the display name, which may repeat
    # across sizes, e.g. multiple "Color Code" entries).
    slug = code_slug or (slugify(code_name) if code_name else "")

    # 6. YAML dedup
    code_status = "new"
    dedup_status: Literal["match", "uncertain", "new"] = "new"
    uncertain_candidates: list[str] = []
    yaml_qubit_perm: Optional[list[int]] = None
    if data_dir:
        dedup = _check_yaml_dedup(data_dir, c_hash, Hx, Hz)
        dedup_status = dedup.status
        uncertain_candidates = dedup.uncertain_candidates
        if dedup.status == "match":
            code_status = "existing"
            yaml_qubit_perm = dedup.qubit_permutation
            # The existing code's stored slug is authoritative. A circuit for an
            # existing code must file under that slug (e.g. `23-1-7`) regardless
            # of any `code_name` passed in — otherwise it lands under
            # `slugify(code_name)`, which has no matching code YAML and is
            # rejected by the DB build ("code '<slug>' not found"). This is why
            # you may omit `code_name` for existing codes: it is ignored for
            # slug purposes on a match either way.
            slug = dedup.slug

    # For existing codes, use the yaml dedup permutation (maps user qubits to
    # the stored canonical form). For new codes, use the canonical_form
    # permutation (maps user qubits to the new canonical form). In both cases
    # the circuit must be relabeled to match the stored Hx/Hz.
    if code_status == "existing":
        final_perm = yaml_qubit_perm  # already normalized to None for identity
    else:
        final_perm = qubit_perm
        # Normalize identity permutation to None (no relabeling needed)
        if final_perm == list(range(len(final_perm))):
            final_perm = None

    return {
        "code": {
            "status": code_status,
            "id": None,
            "name": code_name,
            "slug": slug,
            "n": params.n,
            "k": params.k,
            "d": d,
            "zoo_url": zoo_url or None,
            "h": h.tolist(),
            "logical": logical.tolist(),
            "is_css": params.is_css,
            "canonical_hash": c_hash,
            "tags": [{"name": t.name, "status": t.status} for t in tags],
        },
        "qubit_permutation": final_perm,
        "original_matrices": {
            "h": orig_h.tolist(),
            "logical": orig_logical.tolist(),
        },
        "dedup_status": dedup_status,
        "uncertain_candidates": uncertain_candidates,
    }


def compute_code_data_h(
    H: np.ndarray,
    n: int,
    d: int,
    code_name: str = "",
    zoo_url: str = "",
    data_dir: Optional[str] = None,
    code_slug: str = "",
    code_tags: Optional[list[str]] = None,
    gauge: Optional[np.ndarray] = None,
) -> dict:
    """
    Compute all code-level data from a single symplectic stabilizer matrix H.

    H has shape (m, 2n): the first n columns are the X-half, the last n the
    Z-half. Auto-detects CSS structure: if H is CSS-decomposable (every RREF
    row is purely X or purely Z), delegates to :func:`compute_code_data` with
    the recovered (Hx, Hz) so the result picks up the `CSS` tag and the
    canonical CSS-form h/logical. Storage is always symplectic-only
    (h, logical); the Hx/Hz/Lx/Lz view is derived in the UI at render time.
    """
    H = np.asarray(H, dtype=int) % 2
    if H.shape[1] != 2 * n:
        raise ValueError(f"Expected H with 2n={2 * n} columns, got {H.shape[1]}")

    # A subsystem code takes the symplectic path whatever its stabilizer group
    # looks like. The CSS route below re-derives k as n - rank, which is the
    # very thing the gauge group is here to correct — Bacon-Shor's stabilizer
    # group *is* CSS, so it would take that route and store [[9,5,3]].
    gauge_k, gauge_qubit_count, gauge_to_store = subsystem.describe(gauge, H, n)
    if css_split := (None if gauge_to_store is not None else split_h_to_css(H, n)):
        Hx, Hz = css_split
        result = compute_code_data(
            Hx,
            Hz,
            d=d,
            code_name=code_name,
            zoo_url=zoo_url,
            data_dir=data_dir,
            code_slug=code_slug,
            code_tags=code_tags,
        )
        # split_h_to_css row-reduces to *detect* CSS structure, so the (Hx, Hz)
        # passed above is an RREF basis of the submission — fine for
        # canonicalization, dedup and logicals (same row space), but not for
        # provenance. The stored original must be the matrix the circuit was
        # submitted against, verbatim: RREF destroys the natural low-weight
        # check structure an LDPC code is defined by (issue #138). The
        # original logicals are unaffected — they are expressed in the
        # submitted column order, which no row operation changes.
        result["original_matrices"]["h"] = H.tolist()
        return result

    # Non-CSS path — and the subsystem path, which is the same one.
    k = gauge_k
    canon_H, qubit_perm = canonical_form_h(H, n)
    # Identity is the *gauge* group's when there is one: two subsystem codes can
    # share a stabilizer group and differ in what a decoder may measure, and
    # hashing only the centre would merge them. The gauge group determines the
    # stabilizer group as its centre, so it is the more informative of the two.
    c_hash = canonical_hash_h(gauge_to_store if gauge_to_store is not None else H, n)

    # The canonical form permutes qubits, so the gauge group has to follow it —
    # logicals that commute with the gauge group in one labelling do not in
    # another. `qubit_perm` maps canonical column -> original column, which is
    # exactly the gather these two halves need.
    gauge_canon = (
        None
        if gauge_to_store is None
        else np.hstack(
            [gauge_to_store[:, list(qubit_perm)], gauge_to_store[:, [q + n for q in qubit_perm]]]
        )
    )
    logical = _compute_symplectic_logicals(canon_H, n, k, gauge=gauge_canon)
    orig_logical = _compute_symplectic_logicals(H, n, k, gauge=gauge_to_store)

    # CSS-ness is a property of the stabilizer group, and a subsystem code can
    # have a CSS one — Bacon-Shor does. It only reaches this path because k
    # cannot be derived the CSS way, so the tag would otherwise be lost and the
    # code would not be findable as CSS while the page rendered its X/Z split.
    is_css = gauge_to_store is not None and split_h_to_css(H, n) is not None
    params_with_d = CodeParams(n=n, k=k, is_css=is_css, d=d)
    tags = suggest_code_tags(params_with_d)
    if gauge_to_store is not None:
        # Worth surfacing: a reader who sees [[9,1,3]] over a rank-4 `h` should
        # be told why the two do not line up, not left to think it a bug.
        tags.append(TagEntry(name="subsystem", status="derived"))
    # Caller-supplied family tags (only CSS/self-dual are auto-derived).
    tags += [TagEntry(name=name, status="provided") for name in code_tags or []]
    seen = set()
    unique_tags: list[TagEntry] = []
    for t in tags:
        if t.name not in seen:
            seen.add(t.name)
            unique_tags.append(t)
    tags = unique_tags

    slug = code_slug or (slugify(code_name) if code_name else "")

    code_status = "new"
    dedup_status: Literal["match", "uncertain", "new"] = "new"
    uncertain_candidates: list[str] = []
    existing_perm: Optional[list[int]] = None
    if data_dir:
        dedup = _check_yaml_dedup_h(data_dir, c_hash, H, n, gauge=gauge_to_store)
        dedup_status = dedup.status
        uncertain_candidates = dedup.uncertain_candidates
        if dedup.status == "match":
            code_status = "existing"
            existing_perm = dedup.qubit_permutation
            # The stored slug is authoritative, exactly as on the CSS path above.
            # This used to be `if not slug`, which let `code_slug` — or a slug
            # derived from `code_name` — win over the code the submission
            # actually matched: a five-qubit-code circuit passed
            # `code_name="Five-Qubit Perfect Code"` was written as
            # `five-qubit-perfect-code--<circuit>.yaml` while the code itself
            # lives at `five-qubit-code`, so the circuit referenced a code entry
            # that is never written and `db:create` rejected it. `code_slug` is
            # documented as naming a *new* code, and on a match there is no new
            # code to name.
            slug = dedup.slug

    if code_status == "existing":
        # Use the perm from _check_yaml_dedup_h (already normalized to None for
        # identity). This is the correct relabeling from user qubits to the
        # stored canonical ordering.
        final_perm: Optional[list[int]] = existing_perm
    else:
        final_perm = qubit_perm
        # Normalize identity permutation to None (no relabeling needed)
        if final_perm == list(range(len(final_perm))):
            final_perm = None

    return {
        "code": {
            "status": code_status,
            "id": None,
            "name": code_name,
            "slug": slug,
            "n": n,
            "k": k,
            "d": d,
            "zoo_url": zoo_url or None,
            "h": canon_H.tolist(),
            "logical": logical.tolist(),
            "is_css": is_css,
            "gauge": None if gauge_canon is None else gauge_canon.tolist(),
            "gauge_qubits": gauge_qubit_count or None,
            "canonical_hash": c_hash,
            "tags": [{"name": t.name, "status": t.status} for t in tags],
        },
        "qubit_permutation": final_perm,
        "original_matrices": {
            "h": H.tolist(),
            "logical": orig_logical.tolist(),
        },
        "dedup_status": dedup_status,
        "uncertain_candidates": uncertain_candidates,
    }


def _logicals_in_original_order(Lx, Lz, perm, Hx, Hz):
    """Canonical logicals expressed in the submitted column order, or (None, None).

    ``perm`` maps canonical column index -> original column index, so undoing it
    is a scatter. The result is checked against the *submitted* matrices before
    being returned: each logical must commute with the checks of the other type
    and the two sets must pair up symplectically. If any of that fails the
    caller falls back to computing them, so a future change to `canonical_form`
    degrades to the slow path rather than to wrong operators.
    """
    perm = list(perm)
    if len(perm) != Lx.shape[1]:
        return None, None
    orig_Lx = np.zeros_like(Lx)
    orig_Lz = np.zeros_like(Lz)
    orig_Lx[:, perm] = Lx
    orig_Lz[:, perm] = Lz

    k = orig_Lx.shape[0]
    if (orig_Lx @ np.asarray(Hz).T % 2).any() or (orig_Lz @ np.asarray(Hx).T % 2).any():
        return None, None
    if not np.array_equal(orig_Lx @ orig_Lz.T % 2, np.eye(k, dtype=int)):
        return None, None
    return orig_Lx, orig_Lz


def _compute_logicals_css(Hx, Hz, d):
    """CSS logical operators. Try MQT QECC first, fall back to GF(2)."""
    try:
        from mqt.qecc.codes import CSSCode

        code = CSSCode(distance=d, Hx=Hx, Hz=Hz)
        return np.array(code.Lx), np.array(code.Lz)
    except Exception:
        pass
    Lx = _compute_logical_mod2(Hz, Hx)
    Lz = _compute_logical_mod2(Hx, Hz)
    return Lx, Lz


def _symplectic_weight(row: np.ndarray, n: int) -> int:
    """Count of non-identity Paulis in a 2n-vector (X or Z half nonzero)."""
    return int(sum(1 for i in range(n) if row[i] or row[i + n]))


def _reduce_logical_weight(L: np.ndarray, H: np.ndarray, n: int) -> np.ndarray:
    """Replace each row of L with the minimum-weight element of L_i + rowspace(H).

    Brute-forces over all 2^m stabilizer combinations (m = rows of H). Skips
    reduction for m > 16 (would take >= 65k iterations per logical, which we
    don't expect to encounter in practice).
    """
    L = L.astype(int) % 2
    H = H.astype(int) % 2
    m = H.shape[0]
    if m > 16:
        return L  # leave as-is for large codes

    reduced = np.empty_like(L)
    for i, log_row in enumerate(L):
        best = log_row
        best_w = _symplectic_weight(best, n)
        for combo in range(1, 1 << m):
            mask = np.array([(combo >> j) & 1 for j in range(m)], dtype=int)
            stabilizer_sum = (mask @ H) % 2
            candidate = (log_row + stabilizer_sum) % 2
            w = _symplectic_weight(candidate, n)
            if w < best_w:
                best, best_w = candidate, w
        reduced[i] = best
    return reduced


def _compute_symplectic_logicals(
    H: np.ndarray,
    n: int,
    k: int,
    minimize: bool = True,
    gauge: Optional[np.ndarray] = None,
) -> np.ndarray:
    """Compute logical operators for any stabilizer code in symplectic form.

    Returns shape (2k, 2n). Rows 0..k-1 are X-bar logicals, rows k..2k-1 are
    Z-bar logicals; ``L[i] · Λ · L[k+j]ᵀ = δ_{ij}`` and the X-bar/Z-bar blocks
    each commute internally.

    Algorithm:
    1. ker(H · Λ) = vectors that symplectically commute with all stabilizers
       (Λ is the symplectic form: swaps X and Z halves).
    2. Mod out rowspace(H) → 2k logical generators.
    3. Symplectic Gram-Schmidt to pair them into k X-bar / Z-bar pairs.

    ``minimize`` (default True) reduces each logical to a minimum-weight
    representative — a brute-force over ``2^m`` stabilizer combinations that is
    purely cosmetic. Pass ``minimize=False`` when any valid logical suffices
    (adding a circuit to an existing code, or a logical expectation) to skip it.

    ``gauge`` makes these the **bare** logicals of a subsystem code: step 1 takes
    the kernel of the *gauge* group rather than of ``H``, so the result commutes
    with everything a decoder may measure, while step 2 still quotients by the
    stabilizers. For a stabilizer code the two groups coincide and passing it
    changes nothing, which is why there is one implementation and not two.
    """
    if k == 0:
        return np.zeros((0, 2 * n), dtype=int)
    H = np.asarray(H, dtype=int) % 2
    if H.shape[1] != 2 * n:
        raise ValueError(f"Expected H with 2n={2 * n} columns, got {H.shape[1]}")

    # H @ Lambda swaps the X and Z halves of each row. For a subsystem code the
    # operators that must be commuted with are the gauge group's, not H's.
    centralize = H if gauge is None else np.asarray(gauge, dtype=int) % 2
    swapped = np.hstack([centralize[:, n:], centralize[:, :n]])
    ker = gf2_nullspace(swapped)
    im = gf2_row_basis(H)

    stacked = np.vstack([im, ker]).astype(int) % 2
    _R, pivots = gf2_rref_pivots(stacked.T)
    pivot_set = set(pivots)
    offset = im.shape[0]
    indep_indices = [i for i in range(offset, stacked.shape[0]) if i in pivot_set]
    if len(indep_indices) != 2 * k:
        raise ValueError(
            f"Expected 2k={2 * k} logical operators independent of stabilizers, "
            f"got {len(indep_indices)}; check that n={n} and k={k} match H."
        )
    L = stacked[indep_indices]
    paired = _symplectic_pair_basis(L, n)
    return _reduce_logical_weight(paired, H, n) if minimize else paired


def _symplectic_inner(u: np.ndarray, v: np.ndarray, n: int) -> int:
    """Symplectic inner product over GF(2): u · Λ · vᵀ = u_X·v_Z + u_Z·v_X mod 2."""
    return int((u[:n] @ v[n:] + u[n:] @ v[:n]) % 2)


def _symplectic_pair_basis(vecs: np.ndarray, n: int) -> np.ndarray:
    """Reorder 2k symplectic vectors into k X-bar / Z-bar pairs.

    Input: any basis of a non-degenerate 2k-dim symplectic subspace of GF(2)^{2n}.
    Output: shape (2k, 2n) where rows 0..k-1 commute among themselves (X-bars),
    rows k..2k-1 commute among themselves (Z-bars), and ``X_i · Λ · Z_jᵀ = δ_{ij}``.
    """
    L = [v.astype(int) % 2 for v in vecs]
    x_bars: list[np.ndarray] = []
    z_bars: list[np.ndarray] = []

    while L:
        x = L[0]
        partner_idx: Optional[int] = None
        for i in range(1, len(L)):
            if _symplectic_inner(x, L[i], n) == 1:
                partner_idx = i
                break
        if partner_idx is None:
            raise AssertionError(
                "Logical subspace is degenerate under the symplectic form; "
                "input vectors do not span 2k commuting/anticommuting pairs"
            )
        y = L[partner_idx]
        remaining = [L[i] for i in range(len(L)) if i != 0 and i != partner_idx]
        # Project remaining vectors onto the symplectic complement of span{x, y}.
        # z' = z + (z·Λ·yᵀ)·x + (z·Λ·xᵀ)·y satisfies z'·Λ·xᵀ = z'·Λ·yᵀ = 0.
        cleaned = []
        for z in remaining:
            zy = _symplectic_inner(z, y, n)
            zx = _symplectic_inner(z, x, n)
            cleaned.append((z + zy * x + zx * y) % 2)
        x_bars.append(x)
        z_bars.append(y)
        L = cleaned

    return np.vstack([np.array(x_bars, dtype=int), np.array(z_bars, dtype=int)])


def _compute_logical_mod2(m1, m2):
    """Logical operators in ker(m1) not in rowspace(m2). Pure numpy over GF(2)."""
    ker = gf2_nullspace(m1.astype(int))
    im = gf2_row_basis(m2.astype(int))

    if ker.shape[0] == 0:
        return np.empty((0, m1.shape[1]), dtype=int)

    # Stack [im; ker] and find which ker rows are linearly independent from im
    # by doing RREF on the transpose and checking pivot row indices.
    stacked = np.vstack([im, ker]).astype(int)
    _R, pivots = gf2_rref_pivots(stacked.T)
    pivot_set = set(pivots)
    offset = im.shape[0]
    indices = [i for i in range(offset, stacked.shape[0]) if i in pivot_set]
    return stacked[indices]


def _is_self_dual(Hx, Hz):
    """CSS code is self-dual if Hx and Hz have same row space."""
    if not is_css(Hx, Hz):
        return False
    rref_x = gf2_rref(Hx)
    rref_z = gf2_rref(Hz)
    rref_x = rref_x[np.any(rref_x, axis=1)]
    rref_z = rref_z[np.any(rref_z, axis=1)]
    return np.array_equal(rref_x, rref_z)


# Parsed `data_yaml/codes/*.yaml`, keyed by path, with the stat that produced it.
# Dedup compares a submission against every stored code, so without this a bulk
# import re-parses the entire library once per circuit: for a 69-circuit import
# into a 74-code library that was 61 s of PyYAML per circuit, and the cost grows
# with the product of the two — adding a circuit should not get slower because
# the library got bigger.
#
# The cache cannot simply be filled once, because `add_circuit` *writes* code
# files as it goes and the next circuit has to see them. Keying each entry on
# (mtime_ns, size) means a new or rewritten file is re-parsed and everything else
# costs a stat — which is what makes it safe to keep across calls at all.
_CODE_CACHE: dict[Path, tuple[tuple[int, int], dict]] = {}


def _load_stored_codes(codes_dir: Path) -> list[tuple[str, dict]]:
    """Every stored code as (slug, parsed YAML), re-reading only what changed."""
    stored: list[tuple[str, dict]] = []
    for code_file in sorted(codes_dir.glob("*.yaml")):
        st = code_file.stat()
        stamp = (st.st_mtime_ns, st.st_size)
        cached = _CODE_CACHE.get(code_file)
        if cached is None or cached[0] != stamp:
            parsed = load_yaml(code_file.read_text(encoding="utf-8"))
            _CODE_CACHE[code_file] = (stamp, parsed)
        else:
            parsed = cached[1]
        stored.append((code_file.stem, parsed))
    return stored


def _check_yaml_dedup(data_dir, c_hash, Hx, Hz) -> DedupResult:
    """Two-phase dedup against data_yaml/codes/ for a CSS submission.

    Phase 1 — fast: scan for canonical_hash match. On hit, run
    find_qubit_permutation to recover the relabeling σ.

    Phase 2 — slower fallback: on hash miss, scan stored codes with matching
    (n, k, rank) and run is_permutation_equivalent. Returns "match" on a
    confirmed permutation, "uncertain" when invariants agree but the search
    times out, or "new" when nothing plausibly matches.
    """
    codes_dir = Path(data_dir) / "codes"
    if not codes_dir.exists():
        return DedupResult("new", None, None, [])

    n = Hx.shape[1]
    H_user = build_symplectic_h(Hx, Hz)
    rank_user = gf2_rank(H_user)

    stored = _load_stored_codes(codes_dir)

    # Phase 1: hash match.
    for slug, data in stored:
        if data.get("canonical_hash") != c_hash:
            continue
        if data.get("h") is None:
            raise ValueError(f"Code '{slug}' has CSS-format canonical_hash but missing h")
        n_stored = data.get("n")
        if n_stored is None:
            raise ValueError(f"Code '{slug}' is missing required field 'n'")
        H_stored = decode_matrix(data["h"])
        css_split = split_h_to_css(H_stored, n_stored)
        if css_split is None:
            raise ValueError(
                f"Code '{slug}' has CSS-format canonical_hash but stored h is not "
                f"row-CSS decomposable"
            )
        ref_Hx, ref_Hz = css_split
        perm = find_qubit_permutation(Hx, Hz, ref_Hx, ref_Hz)
        if perm is None:
            raise ValueError(
                f"Code '{slug}' has matching canonical hash but no valid qubit "
                f"permutation could be found. This indicates a hash collision or "
                f"a bug in canonical_form."
            )
        if perm == list(range(len(perm))):
            perm = None
        return DedupResult("match", slug, perm, [])

    return _phase2_permutation_scan(stored, H_user, n, rank_user)


def _gauge_agrees(
    gauge_user: np.ndarray, gauge_stored: np.ndarray, n: int, sigma: list[int]
) -> bool:
    """Do the two gauge groups span the same row space under `sigma`?

    `sigma` is the permutation `is_permutation_equivalent` returned, whose
    contract is that gathering columns `sigma + [s + n for s in sigma]` from the
    user's matrix reproduces the stored one's row space. The gauge group has to
    survive the same gather, or the two codes differ in what a decoder may
    measure even though their centres coincide.
    """
    gauge_user = np.asarray(gauge_user, dtype=int) % 2
    gauge_stored = np.asarray(gauge_stored, dtype=int) % 2
    permuted = gauge_user[:, list(sigma) + [s + n for s in sigma]]
    return np.array_equal(gf2_row_basis(permuted), gf2_row_basis(gauge_stored))


def _phase2_permutation_scan(
    stored: list[tuple[str, dict]],
    H_user: np.ndarray,
    n: int,
    rank_user: int,
    gauge_user: Optional[np.ndarray] = None,
) -> DedupResult:
    """Common Phase-2 scan shared by the CSS and non-CSS dedup paths.

    For each stored code with matching (n, rank), run is_permutation_equivalent
    against the user's symplectic H. Returns "match" on the first equivalent,
    "uncertain" if any candidate timed out and none matched, else "new".

    `H_user` is the *stabilizer* group, which for a subsystem code is only the
    centre of the gauge group — and two subsystem codes can share a centre while
    differing in what a decoder may measure. That is exactly why
    `compute_code_data_h` hashes the gauge group rather than `h`, so Phase 1
    separates such codes; comparing only `h` here merged them again, absorbing a
    [[9,4,3]] into the stored Bacon-Shor [[9,1,3]] and discarding the computed k.
    So a permutation match must carry the gauge group over too, and `gauge_user`
    is passed whenever the submission has one (`None` for a plain stabilizer
    code, including every CSS submission).
    """
    uncertain: list[str] = []
    for slug, data in stored:
        if data.get("n") != n or data.get("h") is None:
            continue
        H_stored = decode_matrix(data["h"])
        if H_stored.shape[1] != 2 * n or gf2_rank(H_stored) != rank_user:
            continue
        gauge_stored = decode_matrix(data["gauge"]) if data.get("gauge") is not None else None
        # A subsystem code is not the stabilizer code sitting at its centre:
        # same `h`, different k. Cheap and definite, so it runs before the
        # permutation search rather than after it.
        if (gauge_user is None) != (gauge_stored is None):
            continue
        if gauge_user is not None and gf2_rank(gauge_user) != gf2_rank(gauge_stored):
            continue  # different gauge-qubit counts, so different k
        status, sigma = is_permutation_equivalent(
            H_user, H_stored, n, budget_seconds=DEDUP_BUDGET_SECONDS
        )
        if status == "equivalent":
            if gauge_user is not None and not _gauge_agrees(gauge_user, gauge_stored, n, sigma):
                # The centres coincide under this sigma but the gauge groups do
                # not. Another sigma might carry both — the search returns the
                # first that fits the centre and does not enumerate the rest —
                # so this is genuinely unresolved, and gets the same answer a
                # budget timeout does rather than a silent merge or a silent
                # duplicate.
                uncertain.append(slug)
                continue
            perm = sigma if sigma != list(range(n)) else None
            return DedupResult("match", slug, perm, [])
        if status == "uncertain":
            uncertain.append(slug)
    if uncertain:
        return DedupResult("uncertain", None, None, uncertain)
    return DedupResult("new", None, None, [])


def _check_yaml_dedup_h(data_dir, c_hash, H, n, gauge=None) -> DedupResult:
    """Two-phase dedup against data_yaml/codes/ for a non-CSS submission.

    Same shape as :func:`_check_yaml_dedup`: hash lookup, then a permutation-
    equivalence scan against same-shape candidates.

    `gauge` is the submission's gauge group when it has one (subsystem codes).
    Phase 1 already accounts for it — `c_hash` is taken over the gauge group in
    that case — and Phase 2 needs it explicitly.
    """
    codes_dir = Path(data_dir) / "codes"
    if not codes_dir.exists():
        return DedupResult("new", None, None, [])

    canon_user, perm_to_canon = canonical_form_h(H, n)
    rank_user = gf2_rank(H)
    H = np.asarray(H, dtype=int) % 2

    stored = _load_stored_codes(codes_dir)

    # Phase 1: hash match.
    for slug, data in stored:
        if data.get("canonical_hash") != c_hash:
            continue
        if data.get("h") is None:
            raise ValueError(f"Code '{slug}' matches non-CSS hash but has no 'h' field")
        canon_stored = decode_matrix(data["h"])
        if canon_stored.shape == canon_user.shape and np.array_equal(canon_stored, canon_user):
            perm = perm_to_canon if perm_to_canon != list(range(n)) else None
            return DedupResult("match", slug, perm, [])
        raise ValueError(
            f"Hash collision: code '{slug}' has matching canonical_hash but different canonical H."
        )

    return _phase2_permutation_scan(stored, H, n, rank_user, gauge_user=gauge)


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
