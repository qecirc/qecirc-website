"""Build a syndrome-extraction round from a check schedule.

A syndrome-measurement *schedule* is the reusable description of one round: a
sequence of ticks, each a set of ``(data, ancilla, pauli)`` checks that run in
parallel. It says nothing about gates — turning it into a circuit is a fixed
recipe — but the tick assignment is the whole content of a scheduling result,
which is why this emitter never re-packs it.

The recipe, per ancilla:

* **X-check** — the ancilla is measured in the X basis: ``H`` before its first
  check and after its last, then ``CX ancilla data`` per check.
* **Z-check** — the ancilla stays in the Z basis: ``CX data ancilla`` per check.

``hadamards="per-check"`` wraps every single X-check in its own ``H`` pair
instead. The two are equivalent — between two checks on the same ancilla the
inner pair cancels — but some sources emit circuits that way, and reproducing a
published body verbatim is sometimes worth the extra gates. ``"basis"`` is the
default because it is what the rest of the library's ``gate_count`` figures are
comparable against.
"""

from collections.abc import Mapping, Sequence
from typing import Optional, Union

import stim

# One check: measure ``pauli`` on ``data``, recorded by ``ancilla``.
Check = tuple[int, int, str]

HADAMARD_STYLES = ("basis", "per-check")


def build_se_round(
    checks_by_tick: Sequence[Sequence[Check]],
    n: int,
    *,
    hadamards: str = "basis",
    coords: Optional[Mapping[int, Sequence[Union[int, float]]]] = None,
) -> stim.Circuit:
    """One syndrome-extraction round as a STIM circuit.

    ``checks_by_tick[t]`` holds the checks that run in tick ``t``; each is
    ``(data, ancilla, pauli)`` with ``pauli`` in ``"XZ"``. Data qubits are
    ``0..n-1`` and every ancilla must be ``>= n``. ``coords`` optionally supplies
    ``QUBIT_COORDS`` per qubit index.

    The circuit resets every ancilla, emits one ``TICK``-separated layer per
    tick, and measures the ancillas in **ascending index order** — that order is
    what a caller pairs with its stabilizers, and what
    :func:`~.circuit_validate.round_check_matrix` reports.

    Raises ``ValueError`` if an ancilla index collides with the data range, if a
    Pauli is not X or Z, or if a tick uses the same qubit twice — a tick is a
    parallel layer by definition, and a repeated qubit means the emitted order,
    not the schedule, would decide what the round measures.
    """
    if hadamards not in HADAMARD_STYLES:
        raise ValueError(f"hadamards must be one of {HADAMARD_STYLES}, got {hadamards!r}")

    ancillas: set[int] = set()
    first: dict[int, int] = {}
    last: dict[int, int] = {}
    for tick, checks in enumerate(checks_by_tick):
        seen: set[int] = set()
        for data, anc, pauli in checks:
            if pauli not in ("X", "Z"):
                raise ValueError(f"check pauli must be 'X' or 'Z', got {pauli!r}")
            if anc < n:
                raise ValueError(f"ancilla {anc} is inside the data range 0..{n - 1}")
            if data >= n:
                raise ValueError(f"data qubit {data} is outside the data range 0..{n - 1}")
            for q in (data, anc):
                if q in seen:
                    raise ValueError(f"tick {tick} uses qubit {q} twice; a tick must be parallel")
                seen.add(q)
            ancillas.add(anc)
            first.setdefault(anc, tick)
            last[anc] = tick

    order = sorted(ancillas)
    # An X-ancilla is one that only ever takes X-checks; a mixed ancilla would
    # need a basis change mid-round, which no schedule format expresses.
    kinds: dict[int, set[str]] = {a: set() for a in order}
    for checks in checks_by_tick:
        for _data, anc, pauli in checks:
            kinds[anc].add(pauli)
    mixed = [a for a, ps in kinds.items() if len(ps) > 1]
    if mixed:
        raise ValueError(f"ancillas {mixed} take both X and Z checks; that is not a Pauli check")
    x_ancillas = {a for a, ps in kinds.items() if ps == {"X"}}

    circ = stim.Circuit()
    for qubit, coord in sorted((coords or {}).items()):
        circ.append("QUBIT_COORDS", [int(qubit)], list(coord))
    if order:
        circ.append("R", order)
        circ.append("TICK")

    for tick, checks in enumerate(checks_by_tick):
        if hadamards == "basis":
            opening = sorted({a for _d, a, _p in checks if a in x_ancillas and first[a] == tick})
            if opening:
                circ.append("H", opening)
        for data, anc, pauli in sorted(checks, key=lambda c: c[1]):
            if pauli == "X":
                if hadamards == "per-check":
                    circ.append("H", [anc])
                circ.append("CX", [anc, data])
                if hadamards == "per-check":
                    circ.append("H", [anc])
            else:
                circ.append("CX", [data, anc])
        if hadamards == "basis":
            closing = sorted({a for _d, a, _p in checks if a in x_ancillas and last[a] == tick})
            if closing:
                circ.append("H", closing)
        circ.append("TICK")

    if order:
        circ.append("M", order)
    return circ
