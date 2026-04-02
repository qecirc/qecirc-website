"""
Circuit-level computation: compact stim, links, format conversions.
"""

from typing import Optional

import stim

from .circuit_validate import circuit_properties
from .compute import slugify


def compute_circuit_data(
    circuit_text: str,
    qubit_permutation: Optional[list[int]] = None,
    circuit_name: str = "",
    source: str = "",
    tool: str = "",
    description: str = "",
) -> dict:
    """
    Compute all circuit-level data.

    Returns a dict matching one entry in the YAML `circuits` list.
    """
    circ = stim.Circuit(circuit_text)
    original_stim = None

    # 1. Apply qubit permutation if code already exists in DB
    if qubit_permutation is not None:
        original_stim = str(circ)
        circ = _relabel_qubits(circ, qubit_permutation)

    # 2. Compact STIM
    circ = _compact_circuit(circ)

    # 3. Metrics
    props = circuit_properties(str(circ))

    # 4. Links
    crumble_url = circ.to_crumble_url()
    quirk_url = circ.to_quirk_url()

    # 5. Format conversions
    stim_body = str(circ)
    qasm_body = _to_qasm(circ)
    cirq_body = _to_cirq_str(circ)

    # 6. Slug
    slug = slugify(circuit_name) if circuit_name else ""

    # Build bodies list, omitting empty conversions
    bodies = [{"format": "stim", "body": stim_body}]
    if qasm_body:
        bodies.append({"format": "qasm", "body": qasm_body})
    if cirq_body:
        bodies.append({"format": "cirq", "body": cirq_body})

    return {
        "name": circuit_name,
        "slug": slug,
        "description": description or "",
        "source": source or "",
        "tool": tool or "",
        "qubit_count": props.qubit_count,
        "depth": props.depth,
        "gate_count": props.gate_count,
        "crumble_url": crumble_url,
        "quirk_url": quirk_url,
        "original_stim": original_stim,
        "bodies": bodies,
    }


def _relabel_qubits(circ, permutation):
    """Relabel qubits using MQT QECC."""
    from mqt.qecc.circuit_synthesis.circuit_utils import relabel_qubits

    mapping = {old: new for new, old in enumerate(permutation)}
    return relabel_qubits(circ, mapping)


def _compact_circuit(circ):
    """Compact a stim circuit using MQT QECC."""
    try:
        from mqt.qecc.circuit_synthesis.circuit_utils import compact_stim_circuit

        return compact_stim_circuit(circ)
    except Exception:
        return circ


def _to_qasm(circ):
    """Convert stim circuit to OpenQASM 2.0 string."""
    try:
        return circ.to_qasm(open_qasm_version=2, skip_dets_and_obs=True)
    except Exception:
        return ""


def _to_cirq_str(circ):
    """Convert stim circuit to cirq string representation."""
    try:
        from stimcirq import stim_circuit_to_cirq_circuit

        cirq_circ = stim_circuit_to_cirq_circuit(circ)
        return str(cirq_circ)
    except Exception:
        return ""
