"""
Circuit validation: parse a STIM circuit and classify its functionality.

Uses stim.Circuit built-ins and stim.gate_data() for gate classification
instead of hand-rolled text parsing.
"""

from pathlib import Path
from typing import Optional

import stim

from .models import CircuitProperties

# Gate classification sets derived from stim.gate_data()
_ALL_GATES = stim.gate_data()
_MEASURE_GATES = {name for name, gd in _ALL_GATES.items() if gd.produces_measurements}
_RESET_GATES = {name for name, gd in _ALL_GATES.items() if gd.is_reset}
_ENTANGLE_GATES = {
    name
    for name, gd in _ALL_GATES.items()
    if gd.is_two_qubit_gate and gd.is_unitary and not gd.is_reset
}


def load_circuit(path: str | Path) -> str:
    return Path(path).read_text()


def classify_functionality(circuit_text: str) -> Optional[str]:
    """
    Heuristic classification based on instruction types present.

    Returns one of: "encoding", "syndrome-extraction", "state-preparation", or None.
    """
    if not circuit_text.strip():
        return None
    return _classify_circuit(stim.Circuit(circuit_text))


def _classify_circuit(circ: stim.Circuit) -> Optional[str]:
    """Classify a parsed stim.Circuit by its gate types."""
    gate_names = {instr.name for instr in circ.flattened()}

    has_measure = bool(gate_names & _MEASURE_GATES)
    has_entangle = bool(gate_names & _ENTANGLE_GATES)
    has_reset = bool(gate_names & _RESET_GATES)

    if has_measure and has_entangle:
        return "syndrome-extraction"
    if has_entangle and not has_measure:
        return "encoding"
    if has_reset and not has_entangle and not has_measure:
        return "state-preparation"
    return None


def _count_gates(instr: stim.CircuitInstruction) -> int:
    """Count the number of gate applications in an instruction.

    Multi-target lines like 'CX 0 1 2 3' apply 2 gates.
    """
    return len(instr.target_groups())


def _compute_depth_and_gates(circ: stim.Circuit, repeat_multiplier: int = 1) -> tuple[int, int]:
    """Recursively compute depth (TICK count) and gate count, respecting REPEAT blocks."""
    depth = 0
    gate_count = 0

    for item in circ:
        if isinstance(item, stim.CircuitRepeatBlock):
            inner_depth, inner_gates = _compute_depth_and_gates(
                item.body_copy(), repeat_multiplier * item.repeat_count
            )
            depth += inner_depth
            gate_count += inner_gates
        else:
            name = item.name
            if name == "TICK":
                depth += repeat_multiplier
            elif name in _ALL_GATES and _ALL_GATES[name].is_unitary:
                gate_count += _count_gates(item) * repeat_multiplier

    return depth, gate_count


def circuit_properties(circuit_text: str) -> CircuitProperties:
    """Extract basic structural properties, correctly accounting for REPEAT blocks."""
    if not circuit_text.strip():
        return CircuitProperties(
            qubit_count=0,
            depth=0,
            gate_count=0,
            detected_functionality=None,
        )

    circ = stim.Circuit(circuit_text)
    depth, gate_count = _compute_depth_and_gates(circ)

    return CircuitProperties(
        qubit_count=circ.num_qubits,
        depth=depth,
        gate_count=gate_count,
        detected_functionality=_classify_circuit(circ),
    )
