"""
Circuit-level computation: compact stim, validation, links, format conversions, tags.
"""

from typing import Optional

import numpy as np
import stim

from .circuit_validate import circuit_properties, classify_functionality
from .compute import slugify
from .models import CodeParams, TagEntry
from .tag_suggest import suggest_circuit_tags, suggest_classification_tags


def compute_circuit_data(
    circuit_text: str,
    Hx: np.ndarray,
    Hz: np.ndarray,
    code_params: dict,  # {n, k, d, is_css}
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

    # 3. Validation
    functionality = classify_functionality(str(circ))
    validation = _validate_circuit(circ, Hx, Hz, functionality)

    # 4. Metrics
    props = circuit_properties(str(circ))

    # 5. Links
    crumble_url = circ.to_crumble_url()
    quirk_url = circ.to_quirk_url()

    # 6. Format conversions
    stim_body = str(circ)
    qasm_body = _to_qasm(circ)
    cirq_body = _to_cirq_str(circ)

    # 7. Tags
    cp = CodeParams(
        n=code_params["n"],
        k=code_params["k"],
        is_css=code_params.get("is_css", False),
        d=code_params.get("d"),
    )
    tags: list[TagEntry] = []
    if functionality:
        tags.extend(suggest_classification_tags(functionality, stim_body))
    tags.extend(suggest_circuit_tags(props, cp))

    # 8. Slug
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
        "detected_functionality": functionality,
        "validation": validation,
        "crumble_url": crumble_url,
        "quirk_url": quirk_url,
        "original_stim": original_stim,
        "tags": [{"name": t.name, "status": t.status} for t in tags],
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


def _validate_circuit(circ, Hx, Hz, functionality):
    """Validate circuit against code matrices. Returns 'passed', 'skipped', or 'failed: reason'."""
    try:
        if functionality == "encoding":
            return _validate_encoding(circ, Hx, Hz)
        elif functionality == "state-preparation":
            return _validate_state_prep(circ, Hx, Hz)
        return "skipped"
    except Exception as e:
        return f"failed: {e}"


def _validate_encoding(circ, Hx, Hz):
    """Verify encoding circuit by checking stabilizer propagation through the tableau.

    An encoding circuit maps |0...0> to the code space. For every stabilizer S
    of the code, U^dag S U must stabilize |0...0>, meaning it can only contain
    Z and I (no X or Y components).
    """
    tableau = circ.to_tableau()
    n = Hx.shape[1]
    num_qubits = len(tableau)
    inv = tableau.inverse()

    for label, H, pauli_val in [("Z", Hz, 3), ("X", Hx, 1)]:
        for row in H:
            ps = stim.PauliString(num_qubits)
            for i, v in enumerate(row):
                if v:
                    ps[i] = pauli_val
            propagated = inv(ps)
            for i in range(num_qubits):
                if propagated[i] in (1, 2):  # X or Y -> doesn't stabilize |0>
                    return f"failed: {label}-stabilizer does not stabilize input"

    return "passed"


def _validate_state_prep(circ, Hx, Hz):
    """Verify state-prep circuit creates correct stabilizers via simulation."""
    sim = stim.TableauSimulator()
    sim.do_circuit(circ)
    n = Hx.shape[1]

    for row in Hz:
        ps = stim.PauliString(n)
        for i, v in enumerate(row):
            if v:
                ps[i] = 3  # Z
        if sim.peek_observable_expectation(ps) != 1:
            return "failed: Z-stabilizer not satisfied"

    for row in Hx:
        ps = stim.PauliString(n)
        for i, v in enumerate(row):
            if v:
                ps[i] = 1  # X
        if sim.peek_observable_expectation(ps) != 1:
            return "failed: X-stabilizer not satisfied"

    return "passed"


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
