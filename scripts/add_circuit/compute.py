"""
Code-level computation: parameters, logicals, canonicalization, tags, YAML dedup.
"""

import re
from pathlib import Path
from typing import Optional

import numpy as np
import yaml

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
    split_h_to_css,
)
from .models import CodeParams, TagEntry
from .tag_suggest import suggest_code_tags


def compute_code_data(
    Hx: np.ndarray,
    Hz: np.ndarray,
    d: int,
    code_name: str = "",
    zoo_url: str = "",
    data_dir: Optional[str] = None,
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
    Lx, Lz = _compute_logicals(canon_Hx, canon_Hz, params.is_css, d)

    # 3b. Original logical operators (from pre-canonicalization matrices)
    orig_Lx, orig_Lz = _compute_logicals(Hx, Hz, params.is_css, d)

    # 3c. Symplectic forms (always populated alongside the CSS view)
    h = build_symplectic_h(canon_Hx, canon_Hz, css_code=True)
    logical = build_symplectic_logical(Lx, Lz, css_code=True, n=params.n, k=params.k)
    orig_h = build_symplectic_h(Hx, Hz, css_code=True)
    orig_logical = build_symplectic_logical(orig_Lx, orig_Lz, css_code=True, n=params.n, k=params.k)

    # 4. Tags
    params_with_d = CodeParams(n=params.n, k=params.k, is_css=params.is_css, d=d)
    tags = suggest_code_tags(params_with_d)
    if _is_self_dual(Hx, Hz):
        tags.append(TagEntry(name="self-dual", status="confirmed"))
    # Deduplicate by name (suggest_code_tags already adds CSS)
    seen = set()
    unique_tags = []
    for t in tags:
        if t.name not in seen:
            seen.add(t.name)
            unique_tags.append(t)
    tags = unique_tags

    # 5. Slug
    slug = slugify(code_name) if code_name else ""

    # 6. YAML dedup
    code_status = "new"
    existing_slug = None
    yaml_qubit_perm = None
    if data_dir:
        existing_slug, yaml_qubit_perm = _check_yaml_dedup(data_dir, c_hash, Hx, Hz)
        if existing_slug is not None:
            code_status = "existing"
            # Use existing slug if no name was provided
            if not slug:
                slug = existing_slug

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
            "hx": canon_Hx.tolist(),
            "hz": canon_Hz.tolist(),
            "logical_x": Lx.tolist(),
            "logical_z": Lz.tolist(),
            "h": h.tolist(),
            "logical": logical.tolist(),
            "is_css": params.is_css,
            "canonical_hash": c_hash,
            "tags": [{"name": t.name, "status": t.status} for t in tags],
        },
        "qubit_permutation": final_perm,
        "original_matrices": {
            "hx": Hx.tolist(),
            "hz": Hz.tolist(),
            "logical_x": orig_Lx.tolist(),
            "logical_z": orig_Lz.tolist(),
            "h": orig_h.tolist(),
            "logical": orig_logical.tolist(),
        },
    }


def compute_code_data_h(
    H: np.ndarray,
    n: int,
    d: int,
    code_name: str = "",
    zoo_url: str = "",
    data_dir: Optional[str] = None,
) -> dict:
    """
    Compute all code-level data from a single symplectic stabilizer matrix H.

    H has shape (m, 2n): the first n columns are the X-half, the last n the
    Z-half. Auto-detects CSS structure: if H is CSS-decomposable (every RREF
    row is purely X or purely Z), delegates to :func:`compute_code_data` with
    the recovered (Hx, Hz) so the returned dict carries the full CSS view and
    the `CSS` tag. Otherwise stores only the symplectic h/logical fields.
    """
    H = np.asarray(H, dtype=int) % 2
    if H.shape[1] != 2 * n:
        raise ValueError(f"Expected H with 2n={2 * n} columns, got {H.shape[1]}")

    # Try CSS detection first; if the row space is CSS-decomposable, route
    # through the CSS path so we get hx/hz/lx/lz populated and the CSS tag.
    css_split = split_h_to_css(H, n)
    if css_split is not None:
        Hx, Hz = css_split
        return compute_code_data(
            Hx, Hz, d=d, code_name=code_name, zoo_url=zoo_url, data_dir=data_dir
        )

    # Non-CSS path
    k = n - gf2_rank(H)
    canon_H, qubit_perm = canonical_form_h(H, n)
    c_hash = canonical_hash_h(H, n)

    logical = _compute_symplectic_logicals(canon_H, n, k)
    orig_logical = _compute_symplectic_logicals(H, n, k)

    params_with_d = CodeParams(n=n, k=k, is_css=False, d=d)
    tags = suggest_code_tags(params_with_d)
    seen = set()
    unique_tags: list[TagEntry] = []
    for t in tags:
        if t.name not in seen:
            seen.add(t.name)
            unique_tags.append(t)
    tags = unique_tags

    slug = slugify(code_name) if code_name else ""

    code_status = "new"
    existing_slug = None
    if data_dir:
        existing_slug = _check_yaml_dedup_h(data_dir, c_hash, H, n)
        if existing_slug is not None:
            code_status = "existing"
            if not slug:
                slug = existing_slug

    final_perm: Optional[list[int]] = qubit_perm
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
            "hx": None,
            "hz": None,
            "logical_x": None,
            "logical_z": None,
            "h": canon_H.tolist(),
            "logical": logical.tolist(),
            "is_css": False,
            "canonical_hash": c_hash,
            "tags": [{"name": t.name, "status": t.status} for t in tags],
        },
        "qubit_permutation": final_perm,
        "original_matrices": {
            "hx": None,
            "hz": None,
            "logical_x": None,
            "logical_z": None,
            "h": H.tolist(),
            "logical": orig_logical.tolist(),
        },
    }


def _compute_logicals(Hx, Hz, code_is_css, d):
    """CSS-only logical computation. Tries MQT QECC, falls back to pure GF(2).

    For non-CSS codes the GF(2) fallback below is mathematically wrong (Hz
    rows are the Z-halves of mixed stabilizers, not pure-Z stabilizers), so
    we hard-fail rather than return nonsense; non-CSS code paths use
    :func:`_compute_symplectic_logicals` instead.
    """
    if not code_is_css:
        raise AssertionError(
            "Non-CSS path must use _compute_symplectic_logicals, not _compute_logicals"
        )
    try:
        from mqt.qecc.codes import CSSCode

        code = CSSCode(distance=d, Hx=Hx, Hz=Hz)
        return np.array(code.Lx), np.array(code.Lz)
    except Exception:
        pass
    # CSS fallback: pure-numpy GF(2) linear algebra. Lx in ker(Hz) \ im(Hx),
    # Lz in ker(Hx) \ im(Hz) — valid because Hx, Hz are pure-X and pure-Z
    # stabilizer matrices in the CSS case.
    Lx = _compute_logical_mod2(Hz, Hx)
    Lz = _compute_logical_mod2(Hx, Hz)
    return Lx, Lz


def _compute_symplectic_logicals(H: np.ndarray, n: int, k: int) -> np.ndarray:
    """Compute logical operators for any stabilizer code in symplectic form.

    Returns shape (2k, 2n). Rows 0..k-1 are X-bar logicals, rows k..2k-1 are
    Z-bar logicals; ``L[i] · Λ · L[k+j]ᵀ = δ_{ij}`` and the X-bar/Z-bar blocks
    each commute internally.

    Algorithm:
    1. ker(H · Λ) = vectors that symplectically commute with all stabilizers
       (Λ is the symplectic form: swaps X and Z halves).
    2. Mod out rowspace(H) → 2k logical generators.
    3. Symplectic Gram-Schmidt to pair them into k X-bar / Z-bar pairs.
    """
    if k == 0:
        return np.zeros((0, 2 * n), dtype=int)
    H = np.asarray(H, dtype=int) % 2
    if H.shape[1] != 2 * n:
        raise ValueError(f"Expected H with 2n={2 * n} columns, got {H.shape[1]}")

    # H @ Lambda swaps the X and Z halves of each row.
    H_swap = np.hstack([H[:, n:], H[:, :n]])
    ker = gf2_nullspace(H_swap)
    im = gf2_row_basis(H)

    if ker.shape[0] == 0:
        if k != 0:
            raise ValueError(f"ker(H·Λ) is empty but k={k}; check H consistency")
        return np.zeros((0, 2 * n), dtype=int)

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
    return _symplectic_pair_basis(L, n)


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


def _check_yaml_dedup(data_dir, c_hash, Hx, Hz):
    """Check data_yaml/codes/ for existing CSS code. Returns (slug, permutation) or (None, None)."""
    codes_dir = Path(data_dir) / "codes"
    if not codes_dir.exists():
        return None, None
    for code_file in sorted(codes_dir.glob("*.yaml")):
        data = yaml.safe_load(code_file.read_text(encoding="utf-8"))
        if data.get("canonical_hash") == c_hash:
            slug = code_file.stem
            if data.get("hx") is None or data.get("hz") is None:
                raise ValueError(
                    f"Code '{slug}' has CSS-format canonical_hash but missing hx/hz"
                )
            ref_Hx = np.array(data["hx"])
            ref_Hz = np.array(data["hz"])
            perm = find_qubit_permutation(Hx, Hz, ref_Hx, ref_Hz)
            if perm is None:
                raise ValueError(
                    f"Code '{slug}' has matching canonical hash but no valid qubit "
                    f"permutation could be found. This indicates a hash collision or "
                    f"a bug in canonical_form."
                )
            # Normalize identity permutation to None (no relabeling needed)
            if perm == list(range(len(perm))):
                perm = None
            return slug, perm
    return None, None


def _check_yaml_dedup_h(data_dir, c_hash, H, n):
    """Look up a non-CSS code by ``canonical_hash_h`` and verify by canonical form.

    Hash collisions are astronomically unlikely with the new SHA256-of-canonical
    hash, but we still verify the stored canonical form matches the user's to
    rule out malformed YAML or future hash bugs.
    """
    codes_dir = Path(data_dir) / "codes"
    if not codes_dir.exists():
        return None
    canon_user, _ = canonical_form_h(H, n)
    for code_file in sorted(codes_dir.glob("*.yaml")):
        data = yaml.safe_load(code_file.read_text(encoding="utf-8"))
        if data.get("canonical_hash") != c_hash:
            continue
        if data.get("h") is None:
            raise ValueError(
                f"Code '{code_file.stem}' matches non-CSS hash but has no 'h' field"
            )
        canon_stored = np.array(data["h"], dtype=int) % 2
        if canon_stored.shape == canon_user.shape and np.array_equal(canon_stored, canon_user):
            return code_file.stem
        raise ValueError(
            f"Hash collision: code '{code_file.stem}' has matching canonical_hash "
            f"but different canonical H. Stored shape {canon_stored.shape}, "
            f"user shape {canon_user.shape}."
        )
    return None


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
