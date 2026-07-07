"""
Circuit-level computation: compact stim, links, format conversions.
"""

import warnings
from typing import Optional

import stim

from .circuit_validate import circuit_properties, has_ticks
from .compute import slugify

# Above this qubit count a circuit is too wide for the per-qubit artifacts to be
# useful, and they bloat the repo: the Crumble/Quirk URLs and the Cirq ASCII
# grid all scale with width (a 475-qubit prep yields a ~700 KB URL and a ~9 MB
# Cirq string). Past the threshold we keep only STIM (canonical) + QASM.
LARGE_CIRCUIT_MAX_QUBITS = 40


def compute_circuit_data(
    circuit_text: str,
    qubit_permutation: Optional[list[int]] = None,
    circuit_name: str = "",
    source: str = "",
    tool: str = "",
    notes: str = "",
    tags: Optional[list[str]] = None,
) -> dict:
    """
    Compute all circuit-level data.

    Returns a dict matching one entry in the YAML `circuits` list.
    """
    circ = stim.Circuit(circuit_text)
    original_stim = str(circ)

    # 1. Apply qubit permutation if code already exists in DB
    if qubit_permutation is not None:
        circ = _relabel_qubits(circ, qubit_permutation)

    # 2. Compact STIM — but only for circuits WITHOUT TICKs. A submitted TICK
    # schedule is authoritative (e.g. AOD-compatible circuits guarantee
    # non-nesting per TICK layer); compaction re-packs the gates and strips
    # the TICKs, silently destroying such per-layer guarantees. The same TICK
    # layers drive the stored depth metric (see circuit_validate).
    if not has_ticks(circ):
        circ = _compact_circuit(circ)

    # 3. Metrics
    props = circuit_properties(str(circ))

    # 4. Links (omitted for large circuits — unusable and bloat the YAML)
    if props.qubit_count <= LARGE_CIRCUIT_MAX_QUBITS:
        crumble_url = circ.to_crumble_url()
        quirk_url = circ.to_quirk_url()
    else:
        crumble_url = ""
        quirk_url = ""

    # 5. Format conversions. Cirq's text form is a per-moment ASCII grid whose
    # width scales with the qubit count, so for wide circuits it explodes (a
    # 475-qubit prep serializes to ~9 MB) while adding no value — skip it there.
    # STIM (canonical) and QASM stay compact and are always kept.
    stim_body = str(circ)
    qasm_body = _to_qasm(circ)
    cirq_body = "" if props.qubit_count > LARGE_CIRCUIT_MAX_QUBITS else _to_cirq_str(circ)

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
        "notes": notes or None,
        "source": source or "",
        "tool": tool or "",
        "qubit_count": props.qubit_count,
        "depth": props.depth,
        "gate_count": props.gate_count,
        "two_qubit_gate_count": props.two_qubit_gate_count,
        "crumble_url": crumble_url,
        "quirk_url": quirk_url,
        "original_stim": original_stim,
        "bodies": bodies,
        "tags": list(tags) if tags else [],
    }


def _relabel_qubits(circ, permutation):
    """Relabel the qubit targets of a stim circuit.

    ``permutation`` covers the ``n`` code (data) qubits. Circuits may carry
    extra flag / ancilla qubits at indices ``>= n`` (e.g. fault-tolerant
    state-prep) that are not part of the code and so are absent from the
    permutation — those pass through unchanged. Non-qubit targets
    (measurement records for classically-controlled Paulis, sweep bits) are
    preserved as-is, which MQT QECC's ``relabel_qubits`` cannot do.
    """
    import stim

    mapping = {old: new for new, old in enumerate(permutation)}
    for q in range(circ.num_qubits):
        mapping.setdefault(q, q)
    out = stim.Circuit()
    for op in circ:
        if isinstance(op, stim.CircuitRepeatBlock):
            body = _relabel_qubits(op.body_copy(), permutation)
            out.append(stim.CircuitRepeatBlock(op.repeat_count, body))
            continue
        targets = [mapping[t.value] if t.is_qubit_target else t for t in op.targets_copy()]
        out.append(op.name, targets, op.gate_args_copy())
    return out


def _compact_circuit(circ):
    """Compact a stim circuit using MQT QECC."""
    try:
        from mqt.qecc.circuit_synthesis.circuit_utils import compact_stim_circuit

        return compact_stim_circuit(circ)
    except Exception as e:
        warnings.warn(f"STIM compaction failed, using original: {e}")
        return circ


def _to_qasm(circ):
    """Convert stim circuit to OpenQASM 2.0 string."""
    try:
        return circ.to_qasm(open_qasm_version=2, skip_dets_and_obs=True)
    except Exception as e:
        warnings.warn(f"QASM conversion failed: {e}")
        return ""


def _to_cirq_str(circ):
    """Convert stim circuit to cirq string representation."""
    try:
        from stimcirq import stim_circuit_to_cirq_circuit

        cirq_circ = stim_circuit_to_cirq_circuit(circ)
        return str(cirq_circ)
    except Exception as e:
        warnings.warn(f"Cirq conversion failed: {e}")
        return ""
