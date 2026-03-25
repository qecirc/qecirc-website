from dataclasses import dataclass
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
