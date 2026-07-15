"""Derive detectors and observables for state-prep and encoding circuits.

The stored ``stim`` body is a pure unitary (no terminal readout, no annotations)
because ``to_tableau()`` and the derive/fit machinery depend on it. This module
builds a *separate* ``stim-annotated`` body: reset prologue, the body verbatim,
a terminal readout, and the deterministic stabilizer outcomes as ``DETECTOR``s.

Two shapes, because the circuits mean different things:

* **state prep** — every qubit is reset, the prepared basis fixes which half of
  the stabilizers is deterministic (Hz for ``|0>_L``, Hx for ``|+>_L``), and the
  logical is deterministic too, so it becomes an ``OBSERVABLE_INCLUDE``.
* **encoding** — only the ancillas are reset; the k logical inputs are left free.
  Hz is deterministic for *any* input (the encoder maps into the codespace and
  every codeword is stabilized by all of Hz), so the detectors hold regardless of
  what the reader puts on the inputs. The logical is input-dependent, so there is
  no observable.

Non-CSS codes are refused: their stabilizers mix X and Z on the same qubit
(the five-qubit code's ``YZIZY``), so no single terminal basis reads them.
"""

import re
from typing import Optional

import numpy as np
import stim

from .code_identify import canonical_form, canonical_form_h, gf2_rank, split_h_to_css

# Matches the permutation line that `state_prep` writes into the notes, e.g.
#   "... (stored qubit i = original qubit permutation[i]): [4, 3, 2, 1, 0]"
_PERM_RE = re.compile(r"permutation\[i\]\)?:\s*\[([0-9,\s]+)\]")

# Random restarts for the sparsifier. Greedy row reduction is seed-sensitive, so
# a handful of shuffled retries buys a materially better basis (unrotated d=9:
# max weight 18 -> 4) for a few hundred milliseconds on the largest codes.
_SPARSIFY_RESTARTS = 12
_SPARSIFY_ROUNDS = 60


def _rowspace_eq(a: np.ndarray, b: np.ndarray) -> bool:
    """True when two GF(2) matrices span the same row space."""
    ra, rb = gf2_rank(a), gf2_rank(b)
    return ra == rb == gf2_rank(np.vstack([a, b]))


def _apply_perm(h: np.ndarray, n: int, perm: list[int]) -> np.ndarray:
    """Relabel the qubit columns of a symplectic matrix.

    ``perm`` maps canonical column index -> original column index, matching both
    :func:`canonical_form` and the convention recorded in the notes ("stored
    qubit i = original qubit permutation[i]").
    """
    idx = np.array(perm, dtype=int)
    return np.hstack([h[:, :n][:, idx], h[:, n:][:, idx]])


def _recompute_perm(original_h: np.ndarray, n: int) -> list[int]:
    """Replay the canonicalization to recover the permutation add_circuit used.

    ``canonical_form`` is deterministic and returns the permutation it applied,
    so for codes created *from* this circuit it can be replayed from the original
    matrix alone. It is not a true permutation invariant for automorphism-rich
    codes, which is why the caller verifies the result and falls back.
    """
    css = split_h_to_css(original_h, n)
    if css is not None:
        return canonical_form(css[0], css[1])[2]
    return canonical_form_h(original_h, n)[1]


def map_original_h(
    original_h: np.ndarray,
    stored_h: np.ndarray,
    n: int,
    notes: str = "",
) -> Optional[tuple[np.ndarray, str]]:
    """Bring a submitted ``original_h`` into the stored (canonical) qubit labeling.

    ``codes.h`` is kept in RREF for dedup, which destroys the natural check
    structure (a weight-6 bivariate-bicycle check becomes weight-48). The
    submitter's basis is usually the natural one, and a permutation preserves row
    weight, so mapping the original across recovers it exactly.

    Three paths, tried in order — together they cover every circuit in the
    library. They are complementary: ``canonical_form`` replays exactly for codes
    created from this circuit, but is not a true invariant for automorphism-rich
    codes (the surface codes) — and those are precisely the ones fitted by search,
    whose permutation was recorded in the notes.

    Returns ``(mapped_h, how)``, or ``None`` when no path yields the right row
    space. Every candidate is checked by row-space equality before being
    returned, so a future change to ``canonical_form`` degrades to ``None``
    rather than to silently wrong detectors.
    """
    if original_h.shape[1] != 2 * n:
        return None

    if _rowspace_eq(stored_h, original_h):
        return original_h, "direct"

    match = _PERM_RE.search(notes or "")
    if match:
        perm = [int(x) for x in match.group(1).split(",")]
        if len(perm) == n and sorted(perm) == list(range(n)):
            candidate = _apply_perm(original_h, n, perm)
            if _rowspace_eq(stored_h, candidate):
                return candidate, "notes"

    try:
        candidate = _apply_perm(original_h, n, _recompute_perm(original_h, n))
    except Exception:
        return None
    if _rowspace_eq(stored_h, candidate):
        return candidate, "recomputed"
    return None


def sparsify_basis(h: np.ndarray, rng: Optional[np.random.Generator] = None) -> np.ndarray:
    """Reduce row weights while preserving the row space.

    Greedy: repeatedly replace a row by its sum with another when that lowers its
    weight. Row operations only, so the row space — and therefore detector
    validity — is preserved by construction.

    Seeded from the submitter's basis this reaches the natural check weight for
    every surface code in the library; seeded from RREF it stalls (unrotated d=9
    stops at 18 instead of 4). Callers should pass the mapped original.
    """
    if h.shape[0] == 0:
        return h
    rng = rng or np.random.default_rng(0)

    def run(shuffle: bool) -> np.ndarray:
        m = h.copy() % 2
        order = list(range(m.shape[0]))
        improved, rounds = True, 0
        while improved and rounds < _SPARSIFY_ROUNDS:
            improved, rounds = False, rounds + 1
            if shuffle:
                rng.shuffle(order)
            for i in order:
                for j in order:
                    if i == j:
                        continue
                    combined = (m[i] + m[j]) % 2
                    if 0 < combined.sum() < m[i].sum():
                        m[i] = combined
                        improved = True
        return m

    best = run(False)
    best_weight = int(best.sum())
    for _ in range(_SPARSIFY_RESTARTS):
        candidate = run(True)
        weight = int(candidate.sum())
        if weight < best_weight:
            best, best_weight = candidate, weight
    return best


def _half(h: np.ndarray, n: int, basis: str) -> np.ndarray:
    """Pure-X or pure-Z rows of a symplectic matrix, as length-n vectors."""
    rows = []
    for row in h:
        x_any, z_any = row[:n].any(), row[n:].any()
        if basis == "Z" and z_any and not x_any:
            rows.append(row[n:])
        elif basis == "X" and x_any and not z_any:
            rows.append(row[:n])
    return np.array(rows, dtype=int) if rows else np.zeros((0, n), dtype=int)


def logical_input_qubits(circ: stim.Circuit, stored_h: np.ndarray, n: int) -> Optional[list[int]]:
    """The qubits carrying an encoder's k logical inputs.

    Canonicalization permutes the data qubits, so the submitted "first k qubits
    are the inputs" convention does not survive into the stored body (one d=3
    surface-code encoder's input sits at qubit 3). Nothing records where it went,
    so it is derived:

    * unitary encoders — propagate ``Z_q`` through the tableau; the qubits whose
      image falls outside the stabilizer group carry a logical, not an ancilla.
    * ancilla-initialising encoders have no tableau (they contain resets), but
      they reset exactly their ancillas, so the never-reset qubits are the inputs.

    Returns ``None`` if neither route applies.
    """
    try:
        tableau = circ.to_tableau()
    except ValueError:
        reset = set()
        for op in circ:
            if isinstance(op, stim.CircuitRepeatBlock):
                continue
            if op.name in ("R", "RX", "RY", "RZ"):
                reset.update(t.value for t in op.targets_copy())
        if not reset:
            return None
        return [q for q in range(circ.num_qubits) if q not in reset]

    width = len(tableau)
    rank = gf2_rank(stored_h)
    inputs = []
    for q in range(width):
        pauli = stim.PauliString(width)
        pauli[q] = 3  # Z
        image = tableau(pauli)
        x = np.array([1 if image[i] in (1, 2) else 0 for i in range(width)], dtype=int)
        z = np.array([1 if image[i] in (3, 2) else 0 for i in range(width)], dtype=int)
        vec = np.concatenate([x, z])
        if len(vec) != stored_h.shape[1]:
            return None
        if gf2_rank(np.vstack([stored_h, vec])) != rank:
            inputs.append(q)
    return inputs


def build_annotated(
    body: str,
    stored_h: np.ndarray,
    logical: np.ndarray,
    n: int,
    k: int,
    kind: str,
    logical_state: str = "",
    original_h: Optional[np.ndarray] = None,
    notes: str = "",
) -> Optional[stim.Circuit]:
    """Build the ``stim-annotated`` body, or ``None`` when not applicable.

    ``kind`` is ``"state-preparation"`` or ``"encoding"``; ``logical_state`` is
    ``"zero"`` or ``"plus"`` (ignored for encoders, which have no prepared state).

    Returns ``None`` — never raises — for the cases this cannot represent:
    non-CSS codes, unsupported logical states, or a code whose deterministic half
    is empty. Callers treat ``None`` as "no annotated body for this circuit".
    The result is *not* validated here; run :func:`validate_annotated` on it.
    """
    if split_h_to_css(stored_h, n) is None:
        return None  # mixed X/Z stabilizers: no single terminal basis reads them

    if kind == "state-preparation":
        if logical_state == "zero":
            basis = "Z"
        elif logical_state == "plus":
            basis = "X"
        else:
            return None
    elif kind == "encoding":
        basis = "Z"  # Hz is deterministic for any logical input; Hx is not
    else:
        return None

    source = stim.Circuit(body)

    # Prefer the submitter's basis (mapped into this labeling) over RREF; fall
    # back to the stored matrix when no original maps.
    basis_h = stored_h
    if original_h is not None:
        mapped = map_original_h(original_h, stored_h, n, notes)
        if mapped is not None:
            basis_h = mapped[0]
    detectors = sparsify_basis(_half(basis_h, n, basis))
    if detectors.shape[0] == 0:
        return None

    if kind == "encoding":
        inputs = logical_input_qubits(source, stored_h, n)
        if inputs is None or len(inputs) != k:
            return None
        reset = [q for q in range(source.num_qubits) if q not in set(inputs)]
    else:
        inputs = []
        reset = list(range(source.num_qubits))

    out = stim.Circuit()
    for qubit, coord in sorted(source.get_final_qubit_coordinates().items()):
        if coord:
            out.append("QUBIT_COORDS", [qubit], coord)
    if reset:
        out.append("R", reset)
        out.append("TICK")
    for op in source:
        if isinstance(op, stim.CircuitRepeatBlock):
            out.append(op)
            continue
        if op.name == "QUBIT_COORDS":
            continue
        out.append(op.name, op.targets_copy(), op.gate_args_copy())
    # Bodies that carry their own TICK schedule already end on one; don't double it.
    if len(out) and out[-1].name != "TICK":
        out.append("TICK")
    out.append("M" if basis == "Z" else "MX", list(range(n)))

    for row in detectors:
        support = [i for i in range(n) if row[i]]
        out.append("DETECTOR", [stim.target_rec(i - n) for i in support])

    # Encoders carry an arbitrary logical, so no observable is deterministic.
    if kind == "state-preparation":
        observables = _half(logical, n, basis)
        for index in range(min(k, observables.shape[0])):
            support = [i for i in range(n) if observables[index][i]]
            out.append("OBSERVABLE_INCLUDE", [stim.target_rec(i - n) for i in support], index)

    return out


def strip_readout(circ: stim.Circuit) -> stim.Circuit:
    """Drop the readout epilogue, keeping the reset prologue and the body.

    The inverse of what the Detectors switch shows: reset prologue + circuit,
    with no terminal measurement and no annotations. Resets stay — the whole
    point of the prologue is to state the ``|0...0>`` input explicitly instead of
    leaving it implied.

    Only the *added* epilogue goes. Pre-existing mid-circuit measurements are
    part of the circuit (399 of 834 bodies carry flag/verification measurements)
    and must survive. :func:`build_annotated` appends exactly one readout
    instruction, last, so after the annotations are dropped it is the final
    instruction — anything earlier belongs to the body.

    Mirrors ``stripReadout`` in src/lib/stim-format.ts, which does the same for
    the browser. Keep the two in step.
    """
    ops = [op for op in circ if op.name not in ("DETECTOR", "OBSERVABLE_INCLUDE")]
    if ops and ops[-1].name in ("M", "MX"):
        ops.pop()
    while ops and ops[-1].name == "TICK":
        ops.pop()

    out = stim.Circuit()
    for op in ops:
        if isinstance(op, stim.CircuitRepeatBlock):
            out.append(op)
            continue
        out.append(op.name, op.targets_copy(), op.gate_args_copy())
    return out


def validate_annotated(circ: stim.Circuit) -> Optional[str]:
    """Check every detector is deterministic. Returns an error string, or None.

    Building a detector error model forces stim to prove each detector's parity
    is fixed in a noiseless run, so this rejects a wrong-basis detector set or a
    single flipped bit in a check row. It is an exact analysis, not sampling.
    """
    try:
        circ.detector_error_model(decompose_errors=False)
    except Exception as e:
        return str(e).splitlines()[0]
    return None
