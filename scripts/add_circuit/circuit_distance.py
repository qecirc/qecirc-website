"""Circuit-level distance of a syndrome-extraction round.

The stored `d` of a code is a property of the *code*: the fewest data-qubit
errors that take one codeword to another. The circuit that measures its checks
can be worse, and usually is — a single fault on an ancilla can propagate
through the CX ladder onto several data qubits at once, so it costs one fault to
do what would otherwise take several errors. The number that says how bad is the
**circuit-level distance**: the fewest faults *anywhere in the circuit* — gate,
idle, reset or measurement — that flip a logical observable while firing no
detector.

It is a property of the schedule, not of the code, which is the whole point:
two rounds measuring the same checks in a different order can differ by a step,
and only this tells them apart. QUITS' `examples/circuit_distance_search.py`
computes the same quantity the same way; the search itself is stim's.

**It depends on the noise model**, so :data:`UNIFORM_P` is part of the answer.
The model here is the standard uniform circuit-level one — depolarizing after
every gate, depolarizing on every idle qubit each tick, and a flip on every
reset and measurement — chosen to match what QUITS' `ErrorModel` applies when
all four of its rates are set equal. A model that leaves out idle noise reports
a larger distance, because it simply has fewer places to fault.

The number does not depend on the *rate*: the search counts error mechanisms in
the detector error model, and every location carries one at any p in (0, 1).
"""

from __future__ import annotations

from typing import Optional

import stim

# The rate every fault location gets. Any value in (0, 1) gives the same
# distance; this one is the usual quoted figure and keeps the DEM readable.
UNIFORM_P = 1e-3

_RESET_FLIP = {"R": "X_ERROR", "RZ": "X_ERROR", "RX": "Z_ERROR", "RY": "Z_ERROR"}
_MEASURE = {"M", "MZ", "MX", "MY"}
_PASS_THROUGH = {"DETECTOR", "OBSERVABLE_INCLUDE", "QUBIT_COORDS", "SHIFT_COORDS"}


def with_uniform_noise(circuit: stim.Circuit, p: float = UNIFORM_P) -> stim.Circuit:
    """The same circuit with a fault location at every gate, idle, reset and readout.

    Idle noise is applied per ``TICK``, to every qubit the tick did not touch —
    that is what makes a long round cost more than a short one, and leaving it
    out is the usual reason a hand-rolled model reports too high a distance.
    """
    all_qubits = set(range(circuit.num_qubits))
    return _noisy(circuit, p, all_qubits)


def _noisy(circuit: stim.Circuit, p: float, all_qubits: set[int]) -> stim.Circuit:
    out = stim.Circuit()
    busy: set[int] = set()  # touched since the last TICK

    for op in circuit:
        if isinstance(op, stim.CircuitRepeatBlock):
            out.append(
                stim.CircuitRepeatBlock(op.repeat_count, _noisy(op.body_copy(), p, all_qubits))
            )
            continue

        name = op.name
        targets = op.targets_copy()
        qubits = [t.value for t in targets if t.is_qubit_target]

        if name == "TICK":
            idle = sorted(all_qubits - busy)
            if idle:
                out.append("DEPOLARIZE1", idle, p)
            out.append("TICK")
            busy = set()
            continue

        if name in _PASS_THROUGH:
            out.append(name, targets, op.gate_args_copy())
            continue

        if name in _MEASURE:
            # stim takes the flip probability as the gate argument, which is
            # exactly a measurement fault: the record is wrong, the state is not.
            out.append(name, targets, p)
            busy.update(qubits)
            continue

        if name in _RESET_FLIP:
            out.append(name, targets, op.gate_args_copy())
            out.append(_RESET_FLIP[name], qubits, p)
            busy.update(qubits)
            continue

        gate = stim.gate_data(name)
        if not gate.is_unitary:
            raise ValueError(f"no noise model for {name!r}")
        out.append(name, targets, op.gate_args_copy())
        # A two-qubit gate's fault is correlated across the pair, so it is one
        # DEPOLARIZE2 over both and not two independent DEPOLARIZE1s — the
        # difference is exactly the hook errors this number exists to catch.
        out.append("DEPOLARIZE2" if gate.is_two_qubit_gate else "DEPOLARIZE1", qubits, p)
        busy.update(qubits)

    idle = sorted(all_qubits - busy)
    if idle:
        out.append("DEPOLARIZE1", idle, p)
    return out


def round_circuit_distance(
    body: str,
    stored_h,
    logical,
    n: int,
    d: int,
    *,
    rounds: Optional[int] = None,
    p: float = UNIFORM_P,
) -> Optional[int]:
    """Circuit-level distance of one syndrome-extraction round, or ``None``.

    **Both bases, and the smaller wins.** A CSS code's Z and X memories are
    different experiments and fail at different weights: the rotated surface code
    d=5 under the library's depth-optimal schedule survives 5 faults in Z memory
    and only 3 in X. Reporting the Z number alone would have called that schedule
    distance-preserving. Worse, the Z number is not even bounded by ``d`` — the
    [[45,1,5]] code's Z memory takes 6, because 5 is its *Z* distance and the
    observable there is flipped by X errors.

    ``None`` when there is nothing to measure: a non-CSS code has no check in
    either pure basis, so neither experiment exists.
    """
    from .annotate import build_annotated_se, validate_annotated

    found: list[int] = []
    for basis in ("Z", "X"):
        experiment = build_annotated_se(body, stored_h, logical, n, rounds or d, basis=basis)
        if experiment is None or validate_annotated(experiment) is not None:
            continue
        got = circuit_distance(with_uniform_noise(experiment, p), max_degree=d)
        if got is not None:
            found.append(got)
    return min(found) if found else None


def circuit_distance(circuit: stim.Circuit, *, max_degree: int) -> Optional[int]:
    """Fewest faults that flip an observable with no detector fired, or ``None``.

    ``circuit`` must already carry noise, detectors and at least one observable —
    :func:`with_uniform_noise` over a memory experiment.

    ``max_degree`` bounds how far the search may wander: it caps the size of the
    detection-event sets it will hold and the degree of the edges it will follow.
    It does **not** cap the answer — the returned count can exceed it — it only
    keeps the search from exploring the whole detector error model of a large
    code. The code's own distance is the natural setting, since a fault set
    heavier than that is not the one being looked for.

    ``None`` means stim refused: the model was not searchable within the bound.
    """
    try:
        errors = circuit.search_for_undetectable_logical_errors(
            dont_explore_detection_event_sets_with_size_above=max_degree,
            dont_explore_edges_with_degree_above=max_degree,
            dont_explore_edges_increasing_symptom_degree=False,
        )
    except ValueError:
        return None
    return len(errors) or None
