"""
Circuit utilities: metrics extraction and validation functions.

Uses stim.Circuit built-ins and stim.gate_data() for accurate metrics.
"""

from collections.abc import Sequence
from typing import Optional, Union

import numpy as np
import stim

from .code_identify import gf2_rank, gf2_row_basis, gf2_rref, gf2_rref_pivots
from .models import CircuitProperties, ExtractedCode

# Gate data for classification (computed once at module level)
_ALL_GATES = stim.gate_data()

# (x, z) bit pair from a symplectic row -> stim Pauli code (0=I, 1=X, 2=Y, 3=Z)
_XZ_TO_PAULI = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}


def _is_entangling(name: str) -> bool:
    """True for genuinely-entangling two-qubit gates.

    A plain ``SWAP`` is a qubit relabeling — free AOD routing on neutral atoms —
    so it is NOT counted as a two-qubit/entangling gate. Two-qubit gates that do
    entangle (``CX``/``CZ`` and hybrids like ``ISWAP``, ``CXSWAP``, ``SWAPCX``)
    still count.
    """
    g = _ALL_GATES.get(name)
    return g is not None and g.is_unitary and g.is_two_qubit_gate and name != "SWAP"


def _counts_in_total(name: str) -> bool:
    """True for gates counted in ``gate_count``: any unitary gate except a free
    ``SWAP`` (SWAPs are free routing, excluded from every metric)."""
    g = _ALL_GATES.get(name)
    return g is not None and g.is_unitary and name != "SWAP"


def _count_gates(instr: stim.CircuitInstruction) -> int:
    """Count the number of gate applications in an instruction.

    Multi-target lines like 'CX 0 1 2 3' apply 2 gates.
    """
    return len(instr.target_groups())


def has_ticks(circ: stim.Circuit) -> bool:
    """True when the circuit (or any nested REPEAT block) contains a TICK."""
    for item in circ:
        if isinstance(item, stim.CircuitRepeatBlock):
            if has_ticks(item.body_copy()):
                return True
        elif item.name == "TICK":
            return True
    return False


def _entangling_depth_greedy(circ: stim.Circuit) -> int:
    """Two-qubit (entangling) circuit depth by greedy (ASAP) layering.

    Only entangling two-qubit gates open layers; single-qubit gates and free
    SWAPs are ignored. Used for circuits without TICK annotations, where
    parallelism must be derived from qubit usage. A ``REPEAT n`` block
    contributes ``n ×`` the entangling depth of its body.
    """
    depth = 0
    # qubit_index -> layer that qubit is next free
    qubit_layer: dict[int, int] = {}

    for item in circ:
        if isinstance(item, stim.CircuitRepeatBlock):
            depth += item.repeat_count * _entangling_depth_greedy(item.body_copy())
        elif _is_entangling(item.name):
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

    return depth


def _entangling_depth_from_ticks(circ: stim.Circuit) -> int:
    """Two-qubit (entangling) depth from the circuit's own TICK schedule.

    The TICK-separated layers are treated as authoritative (the submitter's
    schedule — e.g. the layers a hardware constraint was enforced on), so the
    depth is the number of TICK layers containing at least one entangling
    gate. No re-packing. A ``REPEAT n`` block contributes ``n ×`` the
    tick-depth of its body.
    """
    depth = 0
    layer_has_entangling = False
    for item in circ:
        if isinstance(item, stim.CircuitRepeatBlock):
            depth += item.repeat_count * _entangling_depth_from_ticks(item.body_copy())
        elif item.name == "TICK":
            depth += layer_has_entangling
            layer_has_entangling = False
        elif _is_entangling(item.name):
            layer_has_entangling = True
    return depth + layer_has_entangling


def _entangling_depth(circ: stim.Circuit) -> int:
    """Two-qubit (entangling) circuit depth.

    Circuits **with** TICKs keep their given schedule (TICK layers are
    authoritative — re-packing could break per-layer guarantees such as AOD
    non-nesting); circuits without TICKs get greedy (ASAP) layering.
    """
    if has_ticks(circ):
        return _entangling_depth_from_ticks(circ)
    return _entangling_depth_greedy(circ)


def _compute_depth_and_gates(
    circ: stim.Circuit, repeat_multiplier: int = 1
) -> tuple[int, int, int]:
    """Compute (2q-entangling depth, gate count, 2q gate count), respecting
    REPEAT blocks.

    SWAPs are excluded from all three metrics (free routing). ``depth`` is the
    two-qubit entangling depth; ``gate_count`` counts every non-SWAP unitary
    gate; ``two_qubit_gate_count`` counts entangling two-qubit gates only.
    """
    gate_count = 0
    two_qubit_gate_count = 0

    for item in circ:
        if isinstance(item, stim.CircuitRepeatBlock):
            _, inner_gates, inner_2q = _compute_depth_and_gates(
                item.body_copy(), repeat_multiplier * item.repeat_count
            )
            gate_count += inner_gates
            two_qubit_gate_count += inner_2q
        elif _counts_in_total(item.name):
            n_apps = _count_gates(item) * repeat_multiplier
            gate_count += n_apps
            if _is_entangling(item.name):
                two_qubit_gate_count += n_apps

    depth = _entangling_depth(circ)
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


def _widen(circ: stim.Circuit, n: int) -> stim.Circuit:
    """Ensure ``circ`` declares at least ``n`` qubits.

    ``num_qubits`` is the highest index stim *sees*, so a code whose last data
    qubits are never touched yields a narrower circuit than the code it encodes.
    Padding with an identity keeps those qubits addressable instead of making a
    legitimate circuit look like a width mismatch.
    """
    if circ.num_qubits >= n:
        return circ
    return circ + stim.Circuit(f"I {n - 1}")


def _row_to_pauli_string(row: np.ndarray, n: int, width: int) -> stim.PauliString:
    """A symplectic row (X-half ``0..n-1`` | Z-half ``n..2n-1``) as a Pauli string.

    ``width`` may exceed ``n``: flag / routing ancillas live at indices ``>= n``
    and carry identity in a code stabilizer.
    """
    ps = stim.PauliString(width)
    for i in range(n):
        pauli = _XZ_TO_PAULI[(int(row[i]), int(row[i + n]))]
        if pauli:
            ps[i] = pauli
    return ps


def _css_to_h(Hx: np.ndarray, Hz: np.ndarray) -> tuple[np.ndarray, int]:
    """Assemble CSS halves into a symplectic ``h``, returning ``(h, n)``.

    Lets the CSS entry points share the general symplectic implementation rather
    than keeping a parallel X/Z-specific one.
    """
    Hx = np.atleast_2d(np.asarray(Hx, dtype=int))
    Hz = np.atleast_2d(np.asarray(Hz, dtype=int))
    n = Hx.shape[1] if Hx.size else Hz.shape[1]
    zx = np.zeros_like(Hx)
    zz = np.zeros_like(Hz)
    rows = []
    if Hx.size:
        rows.append(np.hstack([Hx, zx]))
    if Hz.size:
        rows.append(np.hstack([zz, Hz]))
    if not rows:
        return np.zeros((0, 2 * n), dtype=int), n
    return np.vstack(rows), n


def _check_codespace_on_zero_input(circ: stim.Circuit, h: np.ndarray, n: int) -> str:
    """Simulate ``circ`` on ``|0...0>`` and check every stabilizer row of ``h``
    fixes the output state, up to sign.

    Reset-tolerant: uses a ``TableauSimulator`` (which supports ``R``/``RX``)
    rather than ``to_tableau``, so it works for ancilla-initialising circuits.
    Shared by :func:`validate_state_prep_h` and by :func:`validate_encoding_h`'s
    non-unitary fallback.

    **Sign.** The test is ``|<S>| == 1``, not ``<S> == +1``. ``codes.h`` is a
    sign-free binary matrix, so it names a stabilizer *group* only up to a choice
    of signs: a circuit that prepares a codeword in a different Pauli frame
    (``-YZIZY`` where the frame ``h`` was written in has ``+YZIZY``) encodes the
    same code and must pass. Since the generators commute, ``|<S>| == 1`` on each
    row means the state is a simultaneous eigenstate of all of them — i.e. it
    lies in the codespace of *some* signing of ``h``, which is exactly as much as
    a sign-free ``h`` can assert. Demanding ``+1`` would reject valid circuits.
    ``logical_state_of`` is what pins down the frame when that actually matters.

    Returns 'passed' or 'failed: <reason>'.
    """
    circ = _widen(circ, n)
    sim = stim.TableauSimulator()
    sim.do_circuit(circ)
    width = max(circ.num_qubits, n)

    for row in h:
        ps = _row_to_pauli_string(row, n, width)
        # 0 = not an eigenstate at all; ±1 = eigenstate in some Pauli frame.
        if abs(sim.peek_observable_expectation(ps)) != 1:
            return f"failed: stabilizer {ps} does not fix the prepared state"

    return "passed"


def validate_encoding_h(circuit: Union[stim.Circuit, str], h: np.ndarray, n: int) -> str:
    """Verify an encoding circuit maps |0...0> into the code space of ``h``.

    ``h`` is the symplectic stabilizer matrix (shape ``(m, 2n)``, X-half then
    Z-half) — the form stored in ``codes.h``. Works for CSS and non-CSS codes
    alike; :func:`validate_encoding` is the CSS-shaped wrapper.

    An encoding circuit U should satisfy: for every stabilizer S of the code,
    U^dag S U stabilizes |0...0> (only Z and I components, no X or Y). That test
    ignores sign by construction, matching the sign-free ``h`` — see
    :func:`_check_codespace_on_zero_input`.

    Ancilla-initialising encoders contain reset instructions (``R``/``RX`` on
    the ancilla qubits) and so have no unitary tableau. For those we fall back
    to simulating on |0...0>: the encoder then prepares |0_L>, so every code
    stabilizer must fix the output — the same ``|0...0> -> codespace`` property
    the unitary path checks, just evaluated by simulation instead of by pulling
    the stabilizers back through U.

    Returns 'passed' or 'failed: <reason>'.
    """
    h = np.atleast_2d(np.asarray(h, dtype=int)) % 2
    if h.size and h.shape[1] != 2 * n:
        raise ValueError(f"Expected h with 2n={2 * n} columns, got {h.shape[1]}")

    circ = _widen(_to_stim_circuit(circuit), n)
    try:
        tableau = circ.to_tableau()
    except ValueError:
        # Non-unitary (contains resets/measurements) — use the reset-tolerant
        # simulation check.
        return _check_codespace_on_zero_input(circ, h, n)

    width = len(tableau)
    inv = tableau.inverse()

    for row in h:
        ps = _row_to_pauli_string(row, n, width)
        propagated = inv(ps)
        for i in range(width):
            if propagated[i] in (1, 2):  # X or Y -> doesn't stabilize |0>
                return f"failed: stabilizer {ps} does not stabilize input"

    return "passed"


def validate_state_prep_h(circuit: Union[stim.Circuit, str], h: np.ndarray, n: int) -> str:
    """Verify a state-prep circuit creates a state in the code space of ``h``.

    ``h`` is the symplectic stabilizer matrix (shape ``(m, 2n)``) — see
    :func:`validate_encoding_h`. Works for CSS and non-CSS codes alike;
    :func:`validate_state_prep` is the CSS-shaped wrapper.

    Simulates the circuit on |0...0> and checks every stabilizer generator fixes
    the result (eigenvalue ±1 — see :func:`_check_codespace_on_zero_input` on why
    the sign is free). This says the output is *a* codeword; it does not say
    which one — use ``logical_state_of`` for that.

    Returns 'passed' or 'failed: <reason>'.
    """
    h = np.atleast_2d(np.asarray(h, dtype=int)) % 2
    if h.size and h.shape[1] != 2 * n:
        raise ValueError(f"Expected h with 2n={2 * n} columns, got {h.shape[1]}")
    return _check_codespace_on_zero_input(_to_stim_circuit(circuit), h, n)


def validate_encoding(circuit: Union[stim.Circuit, str], Hx: np.ndarray, Hz: np.ndarray) -> str:
    """Verify encoding circuit maps |0...0> to the code space (CSS codes).

    Thin wrapper over :func:`validate_encoding_h` for callers holding CSS halves.

    Returns 'passed' or 'failed: <reason>'.
    """
    h, n = _css_to_h(Hx, Hz)
    return validate_encoding_h(circuit, h, n)


def validate_state_prep(circuit: Union[stim.Circuit, str], Hx: np.ndarray, Hz: np.ndarray) -> str:
    """Verify state-prep circuit creates correct stabilizer state (CSS codes).

    Thin wrapper over :func:`validate_state_prep_h` for callers holding CSS
    halves.

    Returns 'passed' or 'failed: <reason>'.
    """
    h, n = _css_to_h(Hx, Hz)
    return validate_state_prep_h(circuit, h, n)


# ---------------------------------------------------------------------------
# Syndrome extraction
# ---------------------------------------------------------------------------
#
# A syndrome-extraction round is validated by *stabilizer flows*, not by
# simulation on |0...0>: it acts on an already-encoded state, so there is no
# fixed input to simulate, and it contains resets and measurements, so it has no
# tableau. Two independent things must hold, and neither implies the other:
#
#   measured   for every stabilizer S there is a flow  1 -> S xor rec[...]
#              — the ancillas are reset, so their input is trivial, and the
#              measurement record carries S's eigenvalue out of the round
#   preserved  for every stabilizer S there is a flow  S -> S
#              — the round leaves the code state where it found it
#
# The measured set is *derived* from the circuit rather than assumed from the
# measurement order: see :func:`measured_stabilizers`. That matters because
# nothing in the stored data records which ancilla measures which stabilizer,
# and because deriving it is what catches the interesting failure — an X- and a
# Z-check sharing two data qubits whose CNOTs are ordered inconsistently leave
# their two ancillas entangled, so the outcome is individually random and the
# round measures nothing, even though every check was applied exactly once.


def measured_stabilizers(circuit: Union[stim.Circuit, str], n: int) -> np.ndarray:
    """The data-qubit Paulis a round measures deterministically.

    Returns a symplectic matrix of shape ``(r, 2n)`` (X-half then Z-half) whose
    row space is the group of operators on qubits ``0..n-1`` whose eigenvalue the
    round writes into its measurement record. Qubits ``>= n`` are the ancillas.

    Derived from :meth:`stim.Circuit.flow_generators`, which returns a complete
    basis for the circuit's flows. The ones that count are those with a **trivial
    input** (the ancillas are reset, so nothing has to be supplied) and **no
    residual support on the ancillas** (an ancilla term means the outcome is
    entangled with another ancilla rather than determined — exactly the
    interleaving failure described above). Gaussian elimination over the ancilla
    columns extracts that subspace; whatever remains, restricted to the data
    qubits, is what the round actually measures.

    A flow with no measurement record is excluded: ``1 -> P`` with no ``rec``
    says the round *prepares* a P eigenstate, which is a state-prep property,
    not a measurement.
    """
    circ = _widen(_to_stim_circuit(circuit), n)
    width = circ.num_qubits
    n_anc = max(width - n, 0)
    n_meas = circ.num_measurements

    # Column layout: ancilla halves first, so RREF pivots on them and the rows
    # left without an ancilla pivot are precisely the ancilla-free subspace.
    anc_cols = 2 * n_anc
    rows: list[np.ndarray] = []
    for flow in circ.flow_generators():
        if flow.input_copy().weight:
            continue
        out = flow.output_copy()
        vec = np.zeros(anc_cols + 2 * n + n_meas, dtype=int)
        # stim trims a flow's Pauli strings to their support, so `out` may be
        # narrower than the circuit (and empty for a measurement-only flow).
        for q in range(min(width, len(out))):
            p = out[q]
            if not p:
                continue
            x, z = (p in (1, 2)), (p in (2, 3))
            if q < n:
                vec[anc_cols + q] = x
                vec[anc_cols + n + q] = z
            else:
                vec[q - n] = x
                vec[n_anc + q - n] = z
        for m in flow.measurements_copy():
            vec[anc_cols + 2 * n + (m % n_meas)] = 1
        rows.append(vec)

    if not rows:
        return np.zeros((0, 2 * n), dtype=int)

    reduced, pivots = gf2_rref_pivots(np.array(rows, dtype=int))
    n_anc_pivots = sum(1 for c in pivots if c < anc_cols)
    ancilla_free = reduced[n_anc_pivots:]
    if not ancilla_free.size:
        return np.zeros((0, 2 * n), dtype=int)

    # Keep only rows that carry a measurement record and touch a data qubit.
    data = ancilla_free[:, anc_cols : anc_cols + 2 * n]
    meas = ancilla_free[:, anc_cols + 2 * n :]
    keep = np.any(data, axis=1) & np.any(meas, axis=1)
    return data[keep]


def round_check_matrix(circuit: Union[stim.Circuit, str], n: int) -> Optional[np.ndarray]:
    """Which operator *each measurement* of a round reads, or ``None``.

    Returns a symplectic matrix with one row per measurement, in measurement
    order. Where :func:`measured_stabilizers` answers "what does this round
    measure" as a group — the question validation asks — this answers "and which
    ancilla reads which", which is what building detectors needs.

    That extra precision costs generality, so this one is deliberately narrow. An
    ancilla must be reset once, before any gate touches it, and measured once;
    nothing else non-unitary may appear. Anything outside that — ``MR``, a flag
    qubit re-used, a data qubit measured — returns ``None``, and the caller falls
    back to whatever it can do without the map. Validation never depends on this
    function, so a ``None`` here can cost an annotation but never a verdict.

    The operator is obtained by pulling ``Z_ancilla`` back through the gates that
    precede *that* measurement: whatever it becomes at the start of the round is
    what the measurement reports, given the reset fixes ``Z_ancilla = +1``.
    Residual support on *another* ancilla means the two are entangled and the
    outcome is not determined by the data at all — that also returns ``None``.

    **Per measurement, not per round**, which is what lets a round be built from
    several sequential sub-rounds — reset and read the Z-ancillas, then reset and
    read the X-ancillas, as the ZX-coloration schedules do. A later sub-round's
    operator is pulled back through the earlier ones too, so it picks up support
    on their ancillas unless that support cancels — and it cancels exactly when
    the checks commute, which for a valid schedule they do. Where they do not,
    the ancilla check above rejects the round rather than inventing a detector.
    Requiring the reset to come before any gate on that qubit is what makes the
    pull-back past it legitimate.
    """
    circ = _widen(_to_stim_circuit(circuit), n)
    width = circ.num_qubits

    # Both bases are in scope. A round may hold its ancillas in Z (`R` … `M`,
    # with the basis change on the data side) or in X (`RX` … `MX`, with
    # Z-checks applied as `CZ`) — the second is what qLDPC emits, and the two are
    # the same construction seen from different frames. What matters is only that
    # an ancilla is measured in the basis it was reset in, since that is what
    # makes its outcome a function of the data.
    unitary = stim.Circuit()
    measured: list[int] = []
    reset_basis: dict[int, int] = {}  # qubit -> stim Pauli code (1 = X, 3 = Z)
    measured_basis: dict[int, int] = {}
    prefix_len: list[int] = []  # gates preceding each measurement, in `unitary`
    touched: set[int] = set()  # qubits a gate has already acted on
    for op in circ:
        if isinstance(op, stim.CircuitRepeatBlock):
            return None
        if op.name in ("R", "RZ", "RX"):
            targets = [t.value for t in op.targets_copy()]
            if any(q in touched or q in reset_basis for q in targets):
                return None  # reset twice, or reset after a gate already moved it
            pauli = 1 if op.name == "RX" else 3
            for q in targets:
                reset_basis[q] = pauli
        elif op.name in ("M", "MZ", "MX"):
            pauli = 1 if op.name == "MX" else 3
            for t in op.targets_copy():
                measured.append(t.value)
                measured_basis[t.value] = pauli
                prefix_len.append(len(unitary))
        elif op.name == "TICK" or op.name == "QUBIT_COORDS":
            continue
        elif _ALL_GATES.get(op.name) is not None and _ALL_GATES[op.name].is_unitary:
            unitary.append(op.name, op.targets_copy(), op.gate_args_copy())
            touched.update(t.value for t in op.targets_copy())
        else:
            return None  # some other non-unitary op; out of scope

    if not measured or not set(measured) <= set(reset_basis):
        return None
    if len(set(measured)) != len(measured) or any(q < n for q in measured):
        return None
    if any(measured_basis[q] != reset_basis[q] for q in measured):
        return None  # measured in a different basis than it was prepared in

    # One tableau per distinct prefix — a two-sub-round schedule has two, not one
    # per measurement.
    inverses: dict[int, stim.Tableau] = {}
    for k in set(prefix_len):
        try:
            inverses[k] = _widen(unitary[:k], width).to_tableau().inverse()
        except ValueError:
            return None

    rows = np.zeros((len(measured), 2 * n), dtype=int)
    for row, (anc, k) in enumerate(zip(measured, prefix_len)):
        basis = reset_basis[anc]
        ps = stim.PauliString(width)
        ps[anc] = basis  # the operator the reset fixes to +1
        pulled = inverses[k](ps)
        for q in range(width):
            p = pulled[q]
            if not p:
                continue
            if q >= n:
                if q != anc or p != basis:
                    return None  # entangled with another ancilla, or basis-changed
                continue
            rows[row, q] = p in (1, 2)
            rows[row, n + q] = p in (2, 3)
    return rows


def validate_syndrome_extraction_h(
    circuit: Union[stim.Circuit, str],
    h: np.ndarray,
    n: int,
    logical: Optional[np.ndarray] = None,
) -> str:
    """Verify one syndrome-extraction round for the code with stabilizers ``h``.

    ``h`` is the symplectic stabilizer matrix (shape ``(m, 2n)``, X-half then
    Z-half) — the form stored in ``codes.h``. Data qubits are ``0..n-1``;
    everything above is an ancilla. ``logical`` is the optional ``codes.logical``
    matrix (shape ``(2k, 2n)``).

    Three checks, in the order they are reported:

    1. **measured** — the group the round measures (:func:`measured_stabilizers`)
       is exactly the stabilizer group of ``h``. Both inclusions matter: a round
       that measures too little is not extracting the full syndrome, and one that
       measures an operator outside the group is measuring something that does
       not commute with the code, which destroys the logical state.
    2. **preserved** — every stabilizer satisfies the flow ``S -> S``.
    3. **logical** — every logical operator satisfies ``L -> L`` (skipped when
       ``logical`` is not given).

    All flows are checked with ``unsigned=True``, matching the sign-free ``h``
    everywhere else in this module: a round that measures ``-S`` measures S in a
    different Pauli frame, which is a labeling difference, not an error.

    Note on (3): a round that mapped ``L -> L·S`` for some stabilizer ``S`` would
    act identically on the codespace but be reported as failing. No such circuit
    has come up; if one does, the check should be relaxed to equality modulo the
    stabilizer group rather than dropped.

    Returns 'passed' or 'failed: <reason>'.
    """
    h = np.atleast_2d(np.asarray(h, dtype=int)) % 2
    if h.size and h.shape[1] != 2 * n:
        raise ValueError(f"Expected h with 2n={2 * n} columns, got {h.shape[1]}")

    circ = _widen(_to_stim_circuit(circuit), n)
    if circ.num_measurements == 0:
        return "failed: circuit has no measurements, so it extracts no syndrome"

    measured = measured_stabilizers(circ, n)
    stab_basis, meas_basis = gf2_row_basis(h), gf2_row_basis(measured)
    if stab_basis.shape != meas_basis.shape or not np.array_equal(stab_basis, meas_basis):
        extra = gf2_rank(np.vstack([h, measured])) - gf2_rank(h) if measured.size else 0
        missing = gf2_rank(h) - (gf2_rank(measured) - extra) if measured.size else gf2_rank(h)
        return (
            f"failed: the round measures a group of rank {gf2_rank(measured)}, but the code "
            f"has {gf2_rank(h)} independent stabilizers "
            f"({missing} not measured, {extra} measured outside the stabilizer group)"
        )

    width = circ.num_qubits
    for row in h:
        ps = _row_to_pauli_string(row, n, width)
        if not circ.has_flow(stim.Flow(input=ps, output=ps), unsigned=True):
            return f"failed: stabilizer {ps} is not preserved by the round"

    if logical is not None:
        logical = np.atleast_2d(np.asarray(logical, dtype=int)) % 2
        if logical.size and logical.shape[1] != 2 * n:
            raise ValueError(f"Expected logical with 2n={2 * n} columns, got {logical.shape[1]}")
        for row in logical:
            ps = _row_to_pauli_string(row, n, width)
            if not circ.has_flow(stim.Flow(input=ps, output=ps), unsigned=True):
                return f"failed: logical operator {ps} is not preserved by the round"

    return "passed"


def validate_syndrome_extraction(
    circuit: Union[stim.Circuit, str], Hx: np.ndarray, Hz: np.ndarray
) -> str:
    """Verify a syndrome-extraction round for a CSS code.

    Thin wrapper over :func:`validate_syndrome_extraction_h` for callers holding
    CSS halves.

    Returns 'passed' or 'failed: <reason>'.
    """
    h, n = _css_to_h(Hx, Hz)
    return validate_syndrome_extraction_h(circuit, h, n)


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
