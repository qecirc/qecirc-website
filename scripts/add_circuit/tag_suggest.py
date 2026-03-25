"""
Heuristic tag extraction from code parameters and circuit properties.

Produces a list of TagEntry objects for the agent to review and refine.
"""

from .models import CircuitProperties, CodeParams, TagEntry


def suggest_code_tags(params: CodeParams) -> list[TagEntry]:
    tags: list[TagEntry] = []

    if params.is_css:
        tags.append(TagEntry(name="CSS", status="confirmed"))

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

    # No REPEAT blocks -> likely single-shot
    if detected_functionality == "syndrome-extraction" and circuit_text.upper().count("REPEAT") == 0:
        tags.append(TagEntry(name="single-shot", status="suggested"))

    return tags


def suggest_circuit_tags(props: CircuitProperties, params: CodeParams) -> list[TagEntry]:
    tags: list[TagEntry] = []

    if props.depth > 0:
        tags.append(TagEntry(name=f"depth:{props.depth}", status="confirmed"))

    return tags
