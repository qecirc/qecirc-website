"""
Code-level computation: parameters, logicals, canonicalization, tags, YAML dedup.
"""

import re
from pathlib import Path
from typing import Optional

import numpy as np
import yaml

from .code_identify import (
    canonical_form,
    canonical_hash,
    extract_params,
    find_qubit_permutation,
    gf2_nullspace,
    gf2_row_basis,
    gf2_rref,
    gf2_rref_pivots,
    is_css,
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

    Returns a dict with keys "code" (matching YAML code section) and
    "qubit_permutation" (mapping to canonical form, or None for new codes).
    """
    # 1. Parameters
    params = extract_params(Hx, Hz)

    # 2. Canonicalization
    canon_Hx, canon_Hz, qubit_perm = canonical_form(Hx, Hz)
    c_hash = canonical_hash(Hx, Hz)

    # 3. Logical operators
    Lx, Lz = _compute_logicals(Hx, Hz, params.is_css, d)

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
            "is_css": params.is_css,
            "canonical_hash": c_hash,
            "tags": [{"name": t.name, "status": t.status} for t in tags],
        },
        # Only pass qubit_permutation when the code already exists in YAML
        # (circuits need relabeling to match the stored canonical form).
        # For new codes the canonical matrices are stored directly, no relabeling needed.
        "qubit_permutation": yaml_qubit_perm,
    }


def _compute_logicals(Hx, Hz, code_is_css, d):
    """Compute logical operators. Try MQT QECC first, fall back to pure-numpy GF(2)."""
    if code_is_css:
        try:
            from mqt.qecc.codes import CSSCode

            code = CSSCode(distance=d, Hx=Hx, Hz=Hz)
            return np.array(code.Lx), np.array(code.Lz)
        except Exception:
            pass
    # Fallback: pure-numpy GF(2) linear algebra
    Lx = _compute_logical_mod2(Hz, Hx)
    Lz = _compute_logical_mod2(Hx, Hz)
    return Lx, Lz


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
    """Check data_yaml/codes/ for existing code. Returns (slug, permutation) or (None, None)."""
    codes_dir = Path(data_dir) / "codes"
    if not codes_dir.exists():
        return None, None
    for code_file in sorted(codes_dir.glob("*.yaml")):
        data = yaml.safe_load(code_file.read_text())
        if data.get("canonical_hash") == c_hash:
            slug = code_file.stem
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


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
