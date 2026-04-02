from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class CodeParams:
    n: int
    k: int
    is_css: bool
    d: Optional[int] = None


@dataclass
class ExtractedCode:
    """Code check matrices extracted from a circuit via Pauli propagation."""

    Hx: np.ndarray  # X-check matrix (RREF, zero rows stripped)
    Hz: np.ndarray  # Z-check matrix (RREF, zero rows stripped)
    n: int
    k: int
    is_css: bool


@dataclass
class CircuitProperties:
    qubit_count: int
    depth: int
    gate_count: int


@dataclass
class TagEntry:
    name: str
    status: str  # "confirmed" | "suggested"
