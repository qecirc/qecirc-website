"""
Code-level computation: parameters, logicals, canonicalization, tags, DB dedup.
"""

import json
import re
import sqlite3
from typing import Optional

import numpy as np

from .code_identify import (
    canonical_form,
    canonical_hash,
    extract_params,
    find_qubit_permutation,
    gf2_rref,
    is_css,
)
from .models import CodeParams, TagEntry
from .tag_suggest import suggest_code_tags


def compute_code_data(
    Hx: np.ndarray,
    Hz: np.ndarray,
    d: Optional[int] = None,
    code_name: str = "",
    zoo_url: str = "",
    db_path: Optional[str] = None,
) -> dict:
    """
    Compute all code-level data from Hx, Hz matrices.

    Returns a dict with keys "code" (matching YAML code section) and
    "qubit_permutation" (mapping to canonical form, or None for new codes).
    """
    # 1. Parameters
    params = extract_params(Hx, Hz)
    if d is None:
        d = _compute_distance(Hx, Hz, params.is_css)

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

    # 6. DB dedup
    code_status = "new"
    code_id = None
    db_qubit_perm = None
    if db_path:
        code_id, db_qubit_perm = _check_db_dedup(db_path, c_hash, Hx, Hz)
        if code_id is not None:
            code_status = "existing"

    return {
        "code": {
            "status": code_status,
            "id": code_id,
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
            "canonical_hash": c_hash,
            "tags": [{"name": t.name, "status": t.status} for t in tags],
        },
        "qubit_permutation": db_qubit_perm if db_qubit_perm is not None else qubit_perm,
    }


def _compute_distance(Hx, Hz, code_is_css, timeout=2.0):
    """Use ldpc to estimate code distance."""
    from ldpc.code_util import compute_code_parameters

    if code_is_css:
        _, _, dx = compute_code_parameters(Hx, timeout_seconds=timeout)
        _, _, dz = compute_code_parameters(Hz, timeout_seconds=timeout)
        return min(dx, dz)
    else:
        H = np.vstack([Hx, Hz])
        _, _, d = compute_code_parameters(H, timeout_seconds=timeout)
        return d


def _compute_logicals(Hx, Hz, code_is_css, d):
    """Compute logical operators. Try MQT QECC first, fall back to ldpc.mod2."""
    if code_is_css:
        try:
            from mqt.qecc.codes import CSSCode

            code = CSSCode(distance=d, Hx=Hx, Hz=Hz)
            return np.array(code.Lx), np.array(code.Lz)
        except Exception:
            pass
    # Fallback: ldpc.mod2
    Lx = _compute_logical_mod2(Hz, Hx)
    Lz = _compute_logical_mod2(Hx, Hz)
    return Lx, Lz


def _compute_logical_mod2(m1, m2):
    """Logical operators in ker(m1) not in rowspace(m2). Uses ldpc.mod2."""
    from ldpc import mod2

    m1_u8 = m1.astype(np.uint8)
    m2_u8 = m2.astype(np.uint8)
    ker = mod2.nullspace(m1_u8)
    im = mod2.row_basis(m2_u8)
    stacked = np.vstack([im, ker])
    pivots = mod2.row_echelon(stacked.T)[3]
    offset = im.shape[0]
    indices = [i for i in range(offset, stacked.shape[0]) if i in pivots]
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


def _check_db_dedup(db_path, c_hash, Hx, Hz):
    """Check if code exists in DB. Returns (code_id, qubit_permutation) or (None, None)."""
    conn = sqlite3.connect(db_path)
    row = conn.execute(
        "SELECT id, hx, hz FROM codes WHERE canonical_hash = ?", (c_hash,)
    ).fetchone()
    conn.close()
    if row is None:
        return None, None
    code_id, hx_json, hz_json = row
    ref_Hx = np.array(json.loads(hx_json))
    ref_Hz = np.array(json.loads(hz_json))
    perm = find_qubit_permutation(Hx, Hz, ref_Hx, ref_Hz)
    return code_id, perm


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
