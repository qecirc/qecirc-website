"""
Notebook-friendly helper functions for inspecting codes and circuits.
"""

from dataclasses import dataclass
from typing import Optional, Union

import numpy as np
import stim

from .circuit_validate import circuit_properties
from .code_identify import (
    canonical_hash,
    canonical_hash_h,
    extract_params,
    gf2_rank,
    is_h_css,
    split_h_to_css,
)
from .compute import _check_yaml_dedup, _check_yaml_dedup_h, _is_self_dual


@dataclass
class ExistingCodeMatch:
    """Result of matching a code against the existing library.

    Attributes:
        slug: Code slug in the library (e.g. 'steane-code').
        qubit_permutation: Column-reindexing array such that
            ``Hx_user[:, perm]`` is row-equivalent to the stored Hx
            (and likewise for Hz). None when orderings already match.
            When not None, ``add_circuit()`` relabels the circuit
            to align with the stored qubit ordering.
    """

    slug: str
    qubit_permutation: list[int] | None


def check_code(Hx: np.ndarray, Hz: np.ndarray, d: Optional[int] = None) -> dict:
    """Quick summary of a code from its check matrices.

    Args:
        Hx: X-check matrix.
        Hz: Z-check matrix.
        d: Code distance (optional).

    Returns:
        Dict with keys: n, k, d (if provided), is_css, is_self_dual, canonical_hash.
    """
    Hx = np.asarray(Hx, dtype=int)
    Hz = np.asarray(Hz, dtype=int)

    params = extract_params(Hx, Hz)
    result = {
        "n": params.n,
        "k": params.k,
        "is_css": params.is_css,
        "is_self_dual": _is_self_dual(Hx, Hz),
        "canonical_hash": canonical_hash(Hx, Hz),
    }
    if d is not None:
        result["d"] = d
    return result


def find_existing_code_full(
    Hx: np.ndarray, Hz: np.ndarray, data_dir: str = "data_yaml"
) -> Optional[ExistingCodeMatch]:
    """Check if this code already exists in data_yaml/, with permutation info.

    Args:
        Hx: X-check matrix.
        Hz: Z-check matrix.
        data_dir: Path to data_yaml directory.

    Returns:
        ExistingCodeMatch with slug and qubit_permutation, or None if not found.
        qubit_permutation is None when orderings match, or a list when the
        circuit will need relabeling to match the stored code.
    """
    Hx = np.asarray(Hx, dtype=int)
    Hz = np.asarray(Hz, dtype=int)

    c_hash = canonical_hash(Hx, Hz)
    slug, perm = _check_yaml_dedup(data_dir, c_hash, Hx, Hz)
    if slug is None:
        return None
    return ExistingCodeMatch(slug=slug, qubit_permutation=perm)


def find_existing_code(
    Hx: np.ndarray, Hz: np.ndarray, data_dir: str = "data_yaml"
) -> Optional[str]:
    """Check if this code already exists in data_yaml/.

    Args:
        Hx: X-check matrix.
        Hz: Z-check matrix.
        data_dir: Path to data_yaml directory.

    Returns:
        The code slug if found, None otherwise.
    """
    match = find_existing_code_full(Hx, Hz, data_dir)
    return match.slug if match else None


def check_code_h(H: np.ndarray, n: int, d: Optional[int] = None) -> dict:
    """Quick summary of a code from its symplectic stabilizer matrix H.

    Args:
        H: Symplectic stabilizer matrix of shape (m, 2n). Columns 0..n-1 are
            the X-half, columns n..2n-1 are the Z-half.
        n: Number of physical qubits.
        d: Code distance (optional).

    Returns:
        Dict with keys: n, k, d (if provided), is_css, is_self_dual, canonical_hash.
    """
    H = np.asarray(H, dtype=int) % 2
    if H.shape[1] != 2 * n:
        raise ValueError(f"Expected H with 2n={2 * n} columns, got {H.shape[1]}")

    css = is_h_css(H, n)
    k = n - gf2_rank(H)

    if css:
        Hx, Hz = split_h_to_css(H, n)
        result = {
            "n": n,
            "k": k,
            "is_css": True,
            "is_self_dual": _is_self_dual(Hx, Hz),
            "canonical_hash": canonical_hash(Hx, Hz),
        }
    else:
        result = {
            "n": n,
            "k": k,
            "is_css": False,
            "is_self_dual": False,
            "canonical_hash": canonical_hash_h(H, n),
        }
    if d is not None:
        result["d"] = d
    return result


def find_existing_code_h(
    H: np.ndarray, n: int, data_dir: str = "data_yaml"
) -> Optional[ExistingCodeMatch]:
    """Check if a code given by H already exists in data_yaml/.

    For CSS-decomposable H this delegates to :func:`find_existing_code_full`
    after recovering (Hx, Hz). For genuinely non-CSS H it matches by
    ``canonical_hash_h`` only and reports ``qubit_permutation=None`` (callers
    that need a permutation should use the CSS path).
    """
    H = np.asarray(H, dtype=int) % 2
    css_split = split_h_to_css(H, n)
    if css_split is not None:
        Hx, Hz = css_split
        return find_existing_code_full(Hx, Hz, data_dir)

    c_hash = canonical_hash_h(H, n)
    slug = _check_yaml_dedup_h(data_dir, c_hash, H, n)
    if slug is None:
        return None
    return ExistingCodeMatch(slug=slug, qubit_permutation=None)


def summarize_circuit(circuit: Union[stim.Circuit, str]) -> dict:
    """Quick notebook-friendly circuit summary.

    Args:
        circuit: STIM circuit (stim.Circuit object or string).

    Returns:
        Dict with keys: qubit_count, gate_count, two_qubit_gate_count, depth,
        crumble_url, quirk_url.
    """
    if isinstance(circuit, str):
        circ = stim.Circuit(circuit)
    else:
        circ = circuit

    props = circuit_properties(str(circ))
    return {
        "qubit_count": props.qubit_count,
        "gate_count": props.gate_count,
        "two_qubit_gate_count": props.two_qubit_gate_count,
        "depth": props.depth,
        "crumble_url": circ.to_crumble_url(),
        "quirk_url": circ.to_quirk_url(),
    }


def preview_circuit(
    Hx: np.ndarray,
    Hz: np.ndarray,
    circuit: Union[stim.Circuit, str],
    circuit_name: str,
    d: int,
    **kwargs,
):
    """Dry-run preview of what add_circuit would generate.

    Accepts the same arguments as add_circuit. Returns an AddCircuitResult
    without writing any files.
    """
    from . import add_circuit

    return add_circuit(
        Hx=Hx,
        Hz=Hz,
        circuit=circuit,
        circuit_name=circuit_name,
        d=d,
        dry_run=True,
        **kwargs,
    )
