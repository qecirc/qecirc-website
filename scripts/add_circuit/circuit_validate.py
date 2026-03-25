"""
Circuit validation: parse a STIM circuit and classify its functionality.
"""

import re
from pathlib import Path
from typing import Optional

from .models import CircuitProperties

# STIM instruction sets used for heuristic classification
_MEASURE_OPS = {"M", "MX", "MY", "MZ", "MR", "MRX", "MRY", "MRZ"}
_ENTANGLE_OPS = {"CNOT", "CX", "CZ", "CY", "SWAP", "ISWAP"}
_RESET_OPS = {"R", "RX", "RY", "RZ"}
_META_OPS = {"QUBIT_COORDS", "DETECTOR", "OBSERVABLE_INCLUDE", "TICK", "REPEAT"}


def load_circuit(path: str | Path) -> str:
    return Path(path).read_text()


def _parse_op(line: str) -> Optional[str]:
    """Extract the operation name from a STIM instruction line, or None for non-ops."""
    line = line.strip()
    if not line or line.startswith("#") or line in ("{", "}"):
        return None
    return line.split()[0].split("(")[0].upper()


def _instructions(circuit_text: str) -> set[str]:
    ops = set()
    for line in circuit_text.splitlines():
        op = _parse_op(line)
        if op and op not in _META_OPS:
            ops.add(op)
    return ops


def classify_functionality(circuit_text: str) -> Optional[str]:
    """
    Heuristic classification based on instruction types present.

    Returns one of: "encoding", "syndrome-extraction", "state-preparation", or None.
    """
    ops = _instructions(circuit_text)
    has_measure = bool(ops & _MEASURE_OPS)
    has_entangle = bool(ops & _ENTANGLE_OPS)
    has_reset = bool(ops & _RESET_OPS)

    if has_measure and has_entangle:
        return "syndrome-extraction"
    if has_entangle and not has_measure:
        return "encoding"
    if has_reset and not has_entangle and not has_measure:
        return "state-preparation"
    return None


def _parse_repeat_blocks(circuit_text: str) -> list[tuple[int, str]]:
    """
    Parse REPEAT blocks recursively, returning (repeat_count, block_body) pairs.
    Non-repeated lines get repeat_count=1. Nested REPEAT blocks multiply counts.
    """
    blocks: list[tuple[int, str]] = []
    lines = circuit_text.splitlines()
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        m = re.match(r"REPEAT\s+(\d+)\s*\{?", stripped, re.IGNORECASE)
        if m:
            count = int(m.group(1))
            # Collect lines until matching closing brace
            brace_depth = 1 if "{" in stripped else 0
            body_lines = []
            i += 1
            while i < len(lines):
                cur = lines[i].strip()
                if cur == "{":
                    if brace_depth == 0:
                        brace_depth = 1
                        i += 1
                        continue
                    brace_depth += 1
                elif cur == "}" or cur.endswith("}"):
                    brace_depth -= 1
                    if brace_depth == 0:
                        i += 1
                        break
                if brace_depth >= 1:
                    body_lines.append(lines[i])
                i += 1
            # Recurse into body to handle nested REPEAT blocks
            for inner_count, inner_body in _parse_repeat_blocks("\n".join(body_lines)):
                blocks.append((count * inner_count, inner_body))
        else:
            blocks.append((1, lines[i]))
            i += 1
    return blocks


def circuit_properties(circuit_text: str) -> CircuitProperties:
    """Extract basic structural properties, correctly accounting for REPEAT blocks."""
    max_qubit = -1
    gate_count = 0
    depth = 0

    for repeat_count, block in _parse_repeat_blocks(circuit_text):
        block_depth = 0
        for line in block.splitlines():
            op = _parse_op(line)
            if op is None:
                continue
            if op == "TICK":
                block_depth += 1
                continue
            if op in _META_OPS:
                continue
            # Count this gate (multiplied by repeat count)
            gate_count += repeat_count
            parts = line.strip().split()
            for token in parts[1:]:
                try:
                    q = int(token)
                    max_qubit = max(max_qubit, q)
                except ValueError:
                    pass
        depth += block_depth * repeat_count

    return CircuitProperties(
        qubit_count=max_qubit + 1 if max_qubit >= 0 else 0,
        depth=depth,
        gate_count=gate_count,
        detected_functionality=classify_functionality(circuit_text),
    )
