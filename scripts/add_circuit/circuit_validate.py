"""
Circuit utilities: metrics extraction and validation functions.

Uses stim.Circuit built-ins and stim.gate_data() for accurate metrics.
"""

from collections.abc import Sequence
from typing import Union

import numpy as np
import stim

from .code_identify import gf2_rank, gf2_rref
from .models import CircuitProperties, ExtractedCode

# Gate data for classification (computed once at module level)
_ALL_GATES = stim.gate_data()


def _count_gates(instr: stim.CircuitInstruction) -> int:
    """Count the number of gate applications in an instruction.

    Multi-target lines like 'CX 0 1 2 3' apply 2 gates.
    """
    return len(instr.target_groups())


def _compute_depth_layered(circ: stim.Circuit, repeat_multiplier: int = 1) -> int:
    """Compute depth by greedy layering when TICKs are absent.

    Assigns each gate to the earliest layer where none of its qubits are busy.
    """
    depth = 0
    # qubit_index -> layer that qubit is next free
    qubit_layer: dict[int, int] = {}

    for item in circ:
        if isinstance(item, stim.CircuitRepeatBlock):
            inner_depth = _compute_depth_layered(
                item.body_copy(), repeat_multiplier * item.repeat_count
            )
            depth += inner_depth
        else:
            name = item.name
            if name not in _ALL_GATES or not _ALL_GATES[name].is_unitary:
                continue
            for group in item.target_groups():
                qubits = [t.value for t in group if t.is_qubit_target]
                if not qubits:
                    continue
                earliest = max((qubit_layer.get(q, 0) for q in qubits), default=0)
                layer = earliest + 1
                for q in qubits:
                    qubit_layer[q] = layer
                if layer > depth:
                    depth = layer

    return depth * repeat_multiplier


def _has_ticks(circ: stim.Circuit) -> bool:
    """Check whether a circuit (or any nested REPEAT block) contains TICK instructions."""
    for item in circ:
        if isinstance(item, stim.CircuitRepeatBlock):
            if _has_ticks(item.body_copy()):
                return True
        elif item.name == "TICK":
            return True
    return False


def _compute_depth_and_gates(
    circ: stim.Circuit, repeat_multiplier: int = 1
) -> tuple[int, int, int]:
    """Recursively compute depth, gate count, and 2Q gate count, respecting REPEAT blocks.

    If the circuit contains TICKs (at any nesting level), depth is the TICK count.
    Otherwise, depth is computed by greedy gate layering.
    """
    depth = 0
    gate_count = 0
    two_qubit_gate_count = 0

    for item in circ:
        if isinstance(item, stim.CircuitRepeatBlock):
            inner_depth, inner_gates, inner_2q = _compute_depth_and_gates(
                item.body_copy(), repeat_multiplier * item.repeat_count
            )
            depth += inner_depth
            gate_count += inner_gates
            two_qubit_gate_count += inner_2q
        else:
            name = item.name
            if name == "TICK":
                depth += repeat_multiplier
            elif name in _ALL_GATES and _ALL_GATES[name].is_unitary:
                n_apps = _count_gates(item) * repeat_multiplier
                gate_count += n_apps
                if _ALL_GATES[name].is_two_qubit_gate:
                    two_qubit_gate_count += n_apps

    if not _has_ticks(circ):
        depth = _compute_depth_layered(circ, repeat_multiplier)

    return depth, gate_count, two_qubit_gate_count


def circuit_properties(circuit_text: str) -> CircuitProperties:
    """Extract basic structural properties, correctly accounting for REPEAT blocks."""
    if not circuit_text.strip():
        return CircuitProperties(
            qubit_count=0,
            depth=0,
            gate_count=0,
            two_qubit_gate_count=0,
        )

    circ = stim.Circuit(circuit_text)
    depth, gate_count, two_qubit_gate_count = _compute_depth_and_gates(circ)

    return CircuitProperties(
        qubit_count=circ.num_qubits,
        depth=depth,
        gate_count=gate_count,
        two_qubit_gate_count=two_qubit_gate_count,
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


# ---------------------------------------------------------------------------
# Code extraction from circuits
# ---------------------------------------------------------------------------


def _pauli_string_to_xz(ps: stim.PauliString, n: int) -> tuple[np.ndarray, np.ndarray, int]:
    """Convert a stim PauliString to binary X/Z vectors and sign.

    Returns (x_vec, z_vec, sign) where:
        x_vec[i] = 1 iff ps[i] in {X, Y}
        z_vec[i] = 1 iff ps[i] in {Z, Y}
        sign = +1 or -1
    """
    x_vec = np.zeros(n, dtype=int)
    z_vec = np.zeros(n, dtype=int)
    for i in range(n):
        p = ps[i]
        if p == 1 or p == 2:  # X or Y
            x_vec[i] = 1
        if p == 3 or p == 2:  # Z or Y
            z_vec[i] = 1
    sign = -1 if ps.sign == -1 else 1
    return x_vec, z_vec, sign


def _classify_generators(
    x_rows: np.ndarray, z_rows: np.ndarray, n: int
) -> tuple[bool, np.ndarray, np.ndarray]:
    """Classify stabilizer generators as CSS or non-CSS, return (Hx, Hz).

    For CSS: Hx = RREF of pure-X rows, Hz = RREF of pure-Z rows.
    For non-CSS: Hx = X-components, Hz = Z-components (paired rows),
    with symplectic RREF applied.
    """
    num_gens = x_rows.shape[0]
    if num_gens == 0:
        return True, np.empty((0, n), dtype=int), np.empty((0, n), dtype=int)

    # Check CSS: every generator is pure-X or pure-Z
    css = True
    for i in range(num_gens):
        has_x = np.any(x_rows[i])
        has_z = np.any(z_rows[i])
        if has_x and has_z:
            css = False
            break

    if css:
        # Separate pure-X and pure-Z rows
        hx_rows = x_rows[np.any(x_rows, axis=1)]
        hz_rows = z_rows[np.any(z_rows, axis=1)]
        Hx = gf2_rref(hx_rows) if hx_rows.size else np.empty((0, n), dtype=int)
        Hz = gf2_rref(hz_rows) if hz_rows.size else np.empty((0, n), dtype=int)
        # Strip zero rows
        if Hx.size:
            Hx = Hx[np.any(Hx, axis=1)]
        if Hz.size:
            Hz = Hz[np.any(Hz, axis=1)]
    else:
        # Non-CSS: RREF on the symplectic matrix [X | Z], then split back
        symplectic = np.hstack([x_rows, z_rows])
        rref = gf2_rref(symplectic)
        rref = rref[np.any(rref, axis=1)]
        Hx = rref[:, :n]
        Hz = rref[:, n:]

    return css, Hx, Hz


def extract_code(
    circuit: Union[stim.Circuit, str],
    circuit_type: str,
    k: int,
) -> ExtractedCode:
    """Extract Hx/Hz check matrices from a circuit via Pauli propagation.

    Args:
        circuit: STIM circuit (unitary, no measurements/noise).
        circuit_type: "encoding" or "state_prep".
        k: Number of logical qubits.

    Returns:
        ExtractedCode with check matrices.

    Raises:
        ValueError: For invalid inputs or inconsistent results.
        NotImplementedError: For non-CSS state-prep circuits.
    """
    circ = _to_stim_circuit(circuit)
    tableau = circ.to_tableau()
    n = len(tableau)

    if k < 0 or k > n:
        raise ValueError(f"k={k} must satisfy 0 <= k <= n={n}")

    if circuit_type == "encoding":
        return _extract_from_encoding(tableau, n, k)
    elif circuit_type == "state_prep":
        return _extract_from_state_prep(tableau, n, k)
    else:
        raise ValueError(f"Unknown circuit_type: {circuit_type!r}. Use 'encoding' or 'state_prep'.")


def _propagate_z(
    tableau: stim.Tableau, n: int, qubits: Sequence[int]
) -> tuple[np.ndarray, np.ndarray]:
    """Propagate Z on given qubits through tableau, return (x_rows, z_rows).

    Sign is ignored — check matrices define the same stabilizer group regardless of sign.
    """
    x_rows = []
    z_rows = []
    for j in qubits:
        z_j = stim.PauliString(n)
        z_j[j] = 3  # Z
        propagated = tableau(z_j)
        x_vec, z_vec, _sign = _pauli_string_to_xz(propagated, n)
        x_rows.append(x_vec)
        z_rows.append(z_vec)
    return np.array(x_rows, dtype=int), np.array(z_rows, dtype=int)


def _extract_from_encoding(tableau: stim.Tableau, n: int, k: int) -> ExtractedCode:
    """Extract code from encoding circuit. First k qubits are data, rest ancilla."""
    num_stabilizers = n - k

    # Propagate Z on ancilla qubits → stabilizer generators
    x_rows, z_rows = _propagate_z(tableau, n, range(k, n))

    css, Hx, Hz = _classify_generators(x_rows, z_rows, n)

    # Verify rank
    if css:
        total_rank = gf2_rank(Hx) + gf2_rank(Hz)
    else:
        total_rank = gf2_rank(np.hstack([Hx, Hz]))
    if total_rank != num_stabilizers:
        raise ValueError(
            f"Rank mismatch: expected {num_stabilizers} independent stabilizers, "
            f"got rank {total_rank}. Check that k={k} is correct."
        )

    return ExtractedCode(Hx=Hx, Hz=Hz, n=n, k=k, is_css=css)


def _extract_from_state_prep(tableau: stim.Tableau, n: int, k: int) -> ExtractedCode:
    """Extract code from state-prep circuit (CSS only).

    For |0_L⟩: X-type stabilizers are exactly the Hx generators (logical X
    does not stabilize |0_L⟩). Z-type stabilizers include both Hz generators
    and k logical Z operators.

    Note: for k >= 1, Hz cannot be uniquely separated from logical Z using
    only the circuit — multiple valid Hz choices exist. This function uses
    RREF ordering as a heuristic. For guaranteed correct extraction, prefer
    encoding circuits (where the data/ancilla split is explicit).
    """
    # Propagate Z on all qubits → n stabilizers (includes k logicals)
    x_rows, z_rows = _propagate_z(tableau, n, range(n))

    # Use _classify_generators for CSS check and initial X/Z separation
    css, Hx, _ = _classify_generators(x_rows, z_rows, n)
    if not css:
        raise NotImplementedError("Non-CSS state-prep extraction is not yet supported.")

    # Z-type rows include Hz generators + k logical Z operators
    hz_mask = np.any(z_rows, axis=1)
    all_z = gf2_rref(z_rows[hz_mask])
    all_z = all_z[np.any(all_z, axis=1)]

    rank_hx = gf2_rank(Hx)
    rank_hz = n - k - rank_hx

    if all_z.shape[0] < rank_hz:
        raise ValueError(
            f"Expected at least {rank_hz} Z-stabilizers, got {all_z.shape[0]}. "
            f"Check that k={k} is correct."
        )

    # Take first rank_hz rows of RREF as Hz (heuristic — see docstring)
    Hz = all_z[:rank_hz]

    return ExtractedCode(Hx=Hx, Hz=Hz, n=n, k=k, is_css=True)
