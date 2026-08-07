"""
Circuit-level computation: compact stim, links, format conversions.
"""

import warnings
from typing import Optional

import stim

from .circuit_validate import circuit_properties, has_ticks
from .compute import slugify

# Above this qubit count a Quirk URL is useless and enormous: Quirk's own UI
# tops out around 16 qubits, and the URL scales with width (a 144-qubit
# syndrome round serializes to ~240 KB, which is most of the page it sits on).
# Past the threshold we omit it. The Crumble link has no such gate — it is
# derived from the body at render time (`crumbleUrl` in src/lib/stim-format.ts)
# and so costs nothing to keep at any width.
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

    # 4. Links. Only Quirk is stored, and only below the width gate — see
    # LARGE_CIRCUIT_MAX_QUBITS. The Crumble link is derived from the body the
    # page is showing, so there is nothing to compute or store here.
    quirk_url = circ.to_quirk_url() if props.qubit_count <= LARGE_CIRCUIT_MAX_QUBITS else ""

    # 5. Format conversions. STIM is canonical; QASM is the one alternate view.
    stim_body = str(circ)
    qasm_body = _to_qasm(circ)

    # 6. Slug
    slug = slugify(circuit_name) if circuit_name else ""

    # Build bodies list, omitting empty conversions
    bodies = [{"format": "stim", "body": stim_body}]
    if qasm_body:
        bodies.append({"format": "qasm", "body": qasm_body})

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
    """Compact a stim circuit using MQT QECC, preserving qubit coordinates.

    ``compact_stim_circuit`` keeps the ``QUBIT_COORDS`` instructions but drops
    their arguments, turning ``QUBIT_COORDS(3, 7) 0`` into a meaningless bare
    ``QUBIT_COORDS 0``. It only re-packs gate timing and never renumbers qubits
    (the whole pipeline depends on indices matching the code's columns), so the
    coordinates are captured beforehand and re-attached by index afterwards.
    """
    coords = circ.get_final_qubit_coordinates()
    try:
        from mqt.qecc.circuit_synthesis.circuit_utils import compact_stim_circuit

        compacted = compact_stim_circuit(circ)
    except Exception as e:
        warnings.warn(f"STIM compaction failed, using original: {e}")
        return circ
    return _restore_coords(compacted, coords)


def _restore_coords(circ, coords):
    """Re-emit ``QUBIT_COORDS`` for ``coords`` at the front of ``circ``.

    ``coords`` maps qubit index -> coordinate list, as returned by
    ``get_final_qubit_coordinates()`` before compaction. Any coordinate-less
    ``QUBIT_COORDS`` left behind by compaction is dropped in favour of these.
    """
    import stim

    coords = {q: c for q, c in coords.items() if c}
    if not coords:
        return circ

    out = stim.Circuit()
    for q, c in sorted(coords.items()):
        out.append("QUBIT_COORDS", [q], c)
    for op in circ:
        if isinstance(op, stim.CircuitRepeatBlock):
            out.append(op)
            continue
        if op.name == "QUBIT_COORDS":
            continue
        out.append(op.name, op.targets_copy(), op.gate_args_copy())
    return out


def _to_qasm(circ):
    """Convert stim circuit to OpenQASM 2.0 string."""
    try:
        return circ.to_qasm(open_qasm_version=2, skip_dets_and_obs=True)
    except Exception as e:
        warnings.warn(f"QASM conversion failed: {e}")
        return ""
