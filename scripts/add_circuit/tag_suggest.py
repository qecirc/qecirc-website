"""
Heuristic tag extraction from code parameters and circuit properties.

Produces a list of TagEntry objects for the agent to review and refine.
"""

import numpy as np

from .models import CircuitProperties, CodeParams, TagEntry


def suggest_code_tags(params: CodeParams, Hx: np.ndarray, Hz: np.ndarray) -> list[TagEntry]:
    tags: list[TagEntry] = []

    if params.is_css:
        tags.append(TagEntry(name="CSS", status="confirmed"))

    # [[n,k,d]] label
    if params.d is not None:
        tags.append(TagEntry(name=f"[[{params.n},{params.k},{params.d}]]", status="confirmed"))
    else:
        tags.append(TagEntry(name=f"[[{params.n},{params.k},?]]", status="suggested"))

    # Heuristic family detection
    if _is_repetition_code(Hx, Hz, params):
        tags.append(TagEntry(name="repetition-code", status="suggested"))
    elif _is_surface_code_candidate(params):
        tags.append(TagEntry(name="surface-code", status="suggested"))

    return tags


def suggest_classification_tags(detected_functionality: str, circuit_text: str) -> list[TagEntry]:
    """Suggest circuit tags based on detected functionality classification."""
    tags: list[TagEntry] = []

    # Add the detected functionality itself as a tag
    if detected_functionality:
        tags.append(TagEntry(name=detected_functionality, status="suggested"))

    text_lower = circuit_text.lower()

    # Flag qubits suggest fault-tolerant syndrome extraction
    if detected_functionality == "syndrome-extraction" and "flag" in text_lower:
        tags.append(TagEntry(name="fault-tolerant", status="suggested"))

    # No repeated REPEAT blocks → likely single-shot
    if detected_functionality == "syndrome-extraction" and circuit_text.upper().count("REPEAT") == 0:
        tags.append(TagEntry(name="single-shot", status="suggested"))

    return tags


def suggest_circuit_tags(props: CircuitProperties, params: CodeParams) -> list[TagEntry]:
    tags: list[TagEntry] = []

    if props.depth > 0:
        tags.append(TagEntry(name=f"depth:{props.depth}", status="confirmed"))

    if params.d is not None:
        tags.append(TagEntry(name=f"distance:{params.d}", status="confirmed"))

    return tags


# ---------------------------------------------------------------------------
# Heuristics (private)
# ---------------------------------------------------------------------------

def _is_repetition_code(Hx: np.ndarray, Hz: np.ndarray, params: CodeParams) -> bool:
    """Repetition codes have k=1 and a tridiagonal parity check structure."""
    if params.k != 1:
        return False
    H = Hx if np.any(Hx) else Hz
    row_weights = H.sum(axis=1)
    return bool(np.all(row_weights == 2))


def _is_surface_code_candidate(params: CodeParams) -> bool:
    """Surface codes typically have n = d² or n = 2d²-1 for rotated variants."""
    if not params.is_css or params.k != 1:
        return False
    import math
    d = round(math.sqrt(params.n))
    return d * d == params.n or 2 * d * d - 1 == params.n
