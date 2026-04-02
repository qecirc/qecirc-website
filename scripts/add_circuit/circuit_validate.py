"""
Circuit utilities: metrics extraction and validation functions.

Uses stim.Circuit built-ins and stim.gate_data() for accurate metrics.
"""

from pathlib import Path
from typing import Union

import numpy as np
import stim

from .models import CircuitProperties

# Gate data for classification (computed once at module level)
_ALL_GATES = stim.gate_data()


def load_circuit(path: str | Path) -> str:
    return Path(path).read_text()


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
        )

    circ = stim.Circuit(circuit_text)
    depth, gate_count = _compute_depth_and_gates(circ)

    return CircuitProperties(
        qubit_count=circ.num_qubits,
        depth=depth,
        gate_count=gate_count,
    )


# ---------------------------------------------------------------------------
# Public validation functions
# ---------------------------------------------------------------------------


def _to_stim_circuit(circuit: Union[stim.Circuit, str]) -> stim.Circuit:
    """Convert string to stim.Circuit if needed."""
    if isinstance(circuit, stim.Circuit):
        return circuit
    return stim.Circuit(circuit)


def validate_encoding(circuit: Union[stim.Circuit, str], Hx: np.ndarray, Hz: np.ndarray) -> str:
    """Verify encoding circuit maps |0...0> to the code space.

    An encoding circuit U should satisfy: for every stabilizer S of the code,
    U^dag S U stabilizes |0...0> (only Z and I components, no X or Y).

    Returns 'passed' or 'failed: <reason>'.
    """
    circ = _to_stim_circuit(circuit)
    tableau = circ.to_tableau()
    num_qubits = len(tableau)
    inv = tableau.inverse()

    for label, H, pauli_val in [("Z", Hz, 3), ("X", Hx, 1)]:
        for row in H:
            ps = stim.PauliString(num_qubits)
            for i, v in enumerate(row):
                if v:
                    # stim Pauli encoding: 0=I, 1=X, 2=Y, 3=Z
                    ps[i] = pauli_val
            propagated = inv(ps)
            for i in range(num_qubits):
                if propagated[i] in (1, 2):  # X or Y -> doesn't stabilize |0>
                    return f"failed: {label}-stabilizer does not stabilize input"

    return "passed"


def validate_state_prep(circuit: Union[stim.Circuit, str], Hx: np.ndarray, Hz: np.ndarray) -> str:
    """Verify state-prep circuit creates correct stabilizer state.

    Simulates the circuit on |0...0> and checks that all stabilizer
    generators have expectation value +1.

    Returns 'passed' or 'failed: <reason>'.
    """
    circ = _to_stim_circuit(circuit)
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


def validate_syndrome_extraction(
    circuit: Union[stim.Circuit, str], Hx: np.ndarray, Hz: np.ndarray
) -> str:
    """Verify syndrome extraction circuit.

    Not yet implemented.
    """
    raise NotImplementedError("Syndrome extraction validation not yet implemented")
