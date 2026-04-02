"""
Heuristic tag extraction from code parameters and circuit properties.

Produces a list of TagEntry objects for the agent to review and refine.
"""

import re

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

    # Strip comments for instruction-level checks (REPEAT detection)
    non_comment_lines = [
        line for line in circuit_text.splitlines() if not line.strip().startswith("#")
    ]
    text_no_comments = "\n".join(non_comment_lines)

    # Flag qubits suggest fault-tolerant syndrome extraction.
    # "flag" typically appears in comments/annotations, so search full text.
    if detected_functionality == "syndrome-extraction" and re.search(
        r"\bflag\b", circuit_text, re.IGNORECASE
    ):
        tags.append(TagEntry(name="fault-tolerant", status="suggested"))

    # No REPEAT blocks in actual instructions -> single round of measurement
    is_syndrome = detected_functionality == "syndrome-extraction"
    if is_syndrome and "REPEAT" not in text_no_comments.upper():
        tags.append(TagEntry(name="single-round", status="suggested"))

    return tags


def suggest_circuit_tags(props: CircuitProperties, params: CodeParams) -> list[TagEntry]:
    tags: list[TagEntry] = []

    if props.depth > 0:
        tags.append(TagEntry(name=f"depth:{props.depth}", status="confirmed"))

    return tags
