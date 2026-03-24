from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CodeParams:
    n: int
    k: int
    is_css: bool
    d: Optional[int] = None


@dataclass
class CircuitProperties:
    qubit_count: int
    depth: int
    gate_count: int
    detected_functionality: Optional[str] = None


@dataclass
class TagEntry:
    name: str
    status: str  # "confirmed" | "suggested"


@dataclass
class ValidationResult:
    valid: bool
    detected_functionality: Optional[str] = None
    mismatch_details: Optional[str] = None


@dataclass
class IngestionPayload:
    code_status: str  # "existing" | "new"
    code_id: Optional[int]
    code_name: str
    code_slug: str
    code_tags: list[TagEntry] = field(default_factory=list)
    qubit_permutation: Optional[list[int]] = None
    circuit_name: str = ""
    circuit_slug: str = ""
    circuit_description: str = ""
    circuit_source: str = ""
    circuit_tags: list[TagEntry] = field(default_factory=list)
    circuit_body: str = ""
