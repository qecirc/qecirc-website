"""
Tag extraction from code parameters.

Only mathematically verifiable tags are auto-assigned.
"""

from .models import CodeParams, TagEntry


def suggest_code_tags(params: CodeParams) -> list[TagEntry]:
    tags: list[TagEntry] = []

    if params.is_css:
        tags.append(TagEntry(name="CSS", status="confirmed"))

    return tags
