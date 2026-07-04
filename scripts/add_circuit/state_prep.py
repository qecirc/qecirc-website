"""
State-preparation circuit tooling: derive a code from a prep circuit, validate
it (CSS or non-CSS), identify the prepared logical state, and fit a circuit to an
existing code by qubit permutation.

These are general, source-agnostic primitives for ingesting *state-preparation*
circuits — circuits that prepare a logical basis state (|0_L>, |+_L>, ...) rather
than carrying explicit check matrices. They complement :mod:`scripts.add_circuit`:
where ``add_circuit`` needs the code's matrices up front, the helpers here recover
those matrices (and the qubit labeling) from the circuit itself.

Core facts these tools are built around:

* Propagating Z through a prep circuit's tableau yields the stabilizers of the
  prepared state. For |0_L> the **pure-X** generators are exactly ``Hx`` (logical
  X flips |0_L>, so it is excluded); for |+_L> the **pure-Z** generators are
  exactly ``Hz``. A *single* basis state cannot separate the stabilizer ``Hz``
  from the logical ``Z`` (the state is stabilized by both), so the code is
  recovered by one of:

  - :func:`derive_matrices_two_circuit` — ``Hx`` from |0_L> + ``Hz`` from |+_L>;
    fully determines a CSS code with no external definition.
  - :func:`derive_matrices_self_dual` — for self-dual CSS codes ``Hz == Hx``, so a
    single |0_L> circuit suffices.
  - :func:`fit_circuit_to_anchor` / :func:`fit_circuit_to_anchor_h` — fit the
    circuit against a trusted (stored) code by a validation-driven qubit
    permutation search. Required for non-CSS or non-self-dual codes.

* Flag / ancilla qubits occupy qubit indices ``>= n``. :func:`strip_flags`
  removes them so the code can be derived from the data qubits alone, while the
  *full* circuit is what a caller stores.

* :func:`import_state_prep` ties these together: derive/anchor the matrices in the
  circuit's own labeling, verify the logical state, then hand the untouched
  circuit to ``add_circuit`` (which dedups to the canonical code, applies the
  permutation, and preserves the original circuit + matrices in ``originals/``),
  folding otherwise-unschema'd provenance into ``notes`` + ``tags``.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Union

import numpy as np
import stim

from .circuit_validate import _classify_generators, _propagate_z
from .code_identify import is_css

if TYPE_CHECKING:
    from . import AddCircuitResult


# ---------------------------------------------------------------------------
# Flag handling
# ---------------------------------------------------------------------------


def strip_flags(circuit: Union[str, stim.Circuit], n_data: int) -> stim.Circuit:
    """Return the sub-circuit acting only on data qubits ``0 .. n_data-1``.

    Gates that touch any qubit with index ``>= n_data`` (flag / ancilla qubits)
    are dropped. TICKs are dropped too. Used to recover the bare state-prep from
    a fault-tolerant circuit so the code can be derived without flag noise.
    """
    circ = circuit if isinstance(circuit, stim.Circuit) else stim.Circuit(circuit)
    out = stim.Circuit()
    for instr in circ:
        if instr.name == "TICK":
            continue
        for group in instr.target_groups():
            if all(t.value < n_data for t in group if t.is_qubit_target):
                out.append(instr.name, group, instr.gate_args_copy())
    return out


# ---------------------------------------------------------------------------
# Matrix derivation from state-prep circuits (in the circuit's own labeling)
# ---------------------------------------------------------------------------


def _clean_pure_x(zero_circuit: stim.Circuit) -> np.ndarray:
    """Hx = pure-X stabilizer generators of the |0_L> the circuit prepares."""
    tab = zero_circuit.to_tableau()
    n = len(tab)
    x_rows, z_rows = _propagate_z(tab, n, range(n))
    css, Hx, _Hz = _classify_generators(x_rows, z_rows, n)
    if not css:
        raise ValueError("Circuit does not prepare a CSS |0_L> (non-CSS stabilizers).")
    return Hx


def _clean_pure_z(plus_circuit: stim.Circuit) -> np.ndarray:
    """Hz = pure-Z stabilizer generators of the |+_L> the circuit prepares."""
    tab = plus_circuit.to_tableau()
    n = len(tab)
    x_rows, z_rows = _propagate_z(tab, n, range(n))
    css, _Hx, Hz = _classify_generators(x_rows, z_rows, n)
    if not css:
        raise ValueError("Circuit does not prepare a CSS |+_L> (non-CSS stabilizers).")
    return Hz


def derive_matrices_two_circuit(
    zero_circuit: Union[str, stim.Circuit],
    plus_circuit: Union[str, stim.Circuit],
    n: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Method A: Hx from |0_L>, Hz from |+_L>. Requires shared qubit labeling."""
    Hx = _clean_pure_x(strip_flags(zero_circuit, n))
    Hz = _clean_pure_z(strip_flags(plus_circuit, n))
    if not is_css(Hx, Hz):
        raise ValueError(
            "Hx (from |0>) and Hz (from |+>) are not CSS-compatible "
            "(Hx*Hz^T != 0). The two circuits likely use different qubit "
            "labelings; align them or use a stored anchor."
        )
    return Hx, Hz


def derive_matrices_self_dual(
    zero_circuit: Union[str, stim.Circuit],
    n: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Method B: self-dual CSS code, Hz == Hx, from a single |0_L> circuit."""
    Hx = _clean_pure_x(strip_flags(zero_circuit, n))
    Hz = Hx.copy()
    if not is_css(Hx, Hz):
        raise ValueError("Hx is not self-orthogonal; the code is not self-dual.")
    return Hx, Hz


# ---------------------------------------------------------------------------
# Validation and logical-state identification
# ---------------------------------------------------------------------------


_XZ_TO_PAULI = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}  # (x,z) -> stim pauli


def _row_support(row: np.ndarray, n: int) -> list[tuple[int, int]]:
    """A symplectic row -> ``[(data-qubit role j, stim pauli)]`` over the ``n``
    data qubits, dropping identity positions."""
    out = []
    for j in range(n):
        p = _XZ_TO_PAULI[(int(row[j]), int(row[j + n]))]
        if p:
            out.append((j, p))
    return out


def _simulate(circuit: Union[str, stim.Circuit], n: int):
    """Simulate the full circuit (flag / routing ancillas included) **once** and
    return a ``peek(support, sigma=None)`` closure.

    ``peek`` evaluates the ``+1 / 0 / -1`` expectation of a stabilizer given as a
    ``[(role, pauli)]`` support (see :func:`_row_support`), placing role ``j`` on
    circuit qubit ``sigma[j]`` (identity when ``sigma`` is ``None``). Simulating
    in full — rather than pre-stripping ancillas — is what lets these tools fit
    and validate circuits whose data qubits interact *through* routing ancillas.
    """
    circ = circuit if isinstance(circuit, stim.Circuit) else stim.Circuit(circuit)
    nq = max(circ.num_qubits, n)
    sim = stim.TableauSimulator()
    sim.do_circuit(circ)

    def peek(support: list[tuple[int, int]], sigma=None) -> int:
        ps = stim.PauliString(nq)
        for j, p in support:
            ps[j if sigma is None else sigma[j]] = p
        return sim.peek_observable_expectation(ps)

    return peek


def symplectic_validate(circuit: Union[str, stim.Circuit], H: np.ndarray, n: int) -> str:
    """Check every stabilizer row of a symplectic ``H`` (shape ``(m, 2n)``) is a
    ``+1`` eigenvalue of the state the circuit prepares. Works for non-CSS codes
    (the CSS-only counterpart is :func:`scripts.add_circuit.validate_state_prep`).

    Row layout: columns ``0..n-1`` are the X-half, ``n..2n-1`` the Z-half. The
    circuit may act on more than ``n`` qubits (flag / routing ancillas at indices
    ``>= n``): it is simulated in full and the ``n``-qubit stabilizers are peeked
    on the data qubits — so it works whether ancillas are separable verification
    qubits or routing qubits the data interacts *through* (do not pre-strip them).
    """
    peek = _simulate(circuit, n)
    for row in np.asarray(H, dtype=int):
        if peek(_row_support(row, n)) != 1:
            return f"failed: stabilizer {row.tolist()} not +1"
    return "passed"


def logical_state_of(
    circuit: Union[str, stim.Circuit],
    n: int,
    d: int,
    *,
    Hx: Optional[np.ndarray] = None,
    Hz: Optional[np.ndarray] = None,
    H: Optional[np.ndarray] = None,
) -> str:
    """Identify which logical basis state a state-prep circuit prepares.

    Stabilizers alone cannot tell |0_L> from |1_L> (both are +1 eigenstates of
    every stabilizer), so we evaluate the *logical* operator expectations on the
    prepared state. The logical operators are computed from the code matrices in
    the **circuit's own labeling** (so no permutation is needed).

    For CSS codes any ``k`` is supported: ``'zero'`` means the all-zeros state
    |0...0_L> (every Z-bar at +1), ``'plus'`` the all-plus state, and so on.
    Returns one of ``'zero' | 'one' | 'plus' | 'minus'``, or ``'unknown'`` for
    anything else (e.g. magic states, mixed logical labels, or non-CSS codes
    with k != 1).

    Caveat on sign: the logical operators are recomputed from binary (sign-free)
    matrices, so the *basis* (Z vs X) is robust but the absolute 0/1 (resp. +/-)
    label is only defined relative to the recomputed Z-bar (resp. X-bar) sign.
    Two labelings of the same code can disagree on which eigenstate is |0>. Use
    :func:`logical_basis_of` when only the basis matters (the reliable part).
    """
    from .code_identify import build_symplectic_logical
    from .compute import _compute_logicals_css, _compute_symplectic_logicals

    if Hx is not None and Hz is not None:
        Lx, Lz = _compute_logicals_css(np.asarray(Hx), np.asarray(Hz), d)
        logical = build_symplectic_logical(Lx, Lz, n=n, k=Lx.shape[0])
    elif H is not None:
        k = n - np.asarray(H).shape[0]
        if k != 1:
            return "unknown"
        # Only the expectation (a ±1/0) is read off below, so skip the cosmetic
        # minimum-weight reduction — any valid logical representative agrees.
        logical = _compute_symplectic_logicals(np.asarray(H), n, k, minimize=False)
    else:
        raise ValueError("Provide (Hx, Hz) or H.")

    k = logical.shape[0] // 2  # rows 0..k-1 are X-bars, k..2k-1 Z-bars

    peek = _simulate(circuit, n)  # simulate in full; ancillas may route the data
    x_exps = [peek(_row_support(logical[i], n)) for i in range(k)]
    z_exps = [peek(_row_support(logical[k + i], n)) for i in range(k)]
    if all(x == 0 for x in x_exps):
        if all(z == 1 for z in z_exps):
            return "zero"
        if all(z == -1 for z in z_exps):
            return "one"
    if all(z == 0 for z in z_exps):
        if all(x == 1 for x in x_exps):
            return "plus"
        if all(x == -1 for x in x_exps):
            return "minus"
    return "unknown"


_STATE_BASIS = {"zero": "z", "one": "z", "plus": "x", "minus": "x"}


def logical_basis_of(
    circuit: Union[str, stim.Circuit],
    n: int,
    d: int,
    *,
    Hx: Optional[np.ndarray] = None,
    Hz: Optional[np.ndarray] = None,
    H: Optional[np.ndarray] = None,
) -> str:
    """Sign-convention-free part of :func:`logical_state_of`: returns ``'z'``
    (a Z-basis eigenstate, |0>/|1>), ``'x'`` (an X-basis eigenstate, |+>/|->),
    or ``'unknown'``."""
    return _STATE_BASIS.get(logical_state_of(circuit, n, d, Hx=Hx, Hz=Hz, H=H), "unknown")


# ---------------------------------------------------------------------------
# Fit a circuit to an existing (anchor) code by permutation search
# ---------------------------------------------------------------------------


@dataclass
class FitResult:
    permutation: Optional[list[int]]  # perm[new] = old  (add_circuit convention)
    status: str  # 'identity' | 'found' | 'not_found'


def fit_circuit_to_anchor(
    zero_circuit: Union[str, stim.Circuit],
    Hx: np.ndarray,
    Hz: np.ndarray,
    n: int,
    max_perms: int = 200_000,
) -> FitResult:
    """Find a data-qubit permutation making the |0_L> circuit validate against
    the anchor (Hx, Hz).

    Returns ``perm`` in ``add_circuit`` convention: ``perm[new] = old`` (so the
    circuit map is ``old -> new``). Identity is tried first. The search is pruned
    by only permuting data qubits (flag qubits ``>= n`` are held fixed).

    Scaling: the fallback is brute force over ``n!`` permutations (capped at
    ``max_perms``), so it only resolves non-identity fits for small ``n`` (roughly
    ``n <= 10``). Larger codes need a structural matcher (e.g. Tanner-graph
    isomorphism); when identity fails there, prefer letting ``add_circuit``'s
    canonical-form dedup find the permutation instead.
    """
    from .code_identify import build_symplectic_h

    return fit_circuit_to_anchor_h(zero_circuit, build_symplectic_h(Hx, Hz), n, max_perms)


def _search_permutation(circuit: stim.Circuit, H: np.ndarray, n: int, max_perms: int) -> FitResult:
    """Find σ (``σ[new]=old``) so ``circuit`` prepares a +1 eigenstate of every
    stabilizer of ``H`` (a symplectic ``(m, 2n)`` matrix) after relabelling the
    ``n`` data qubits.

    The full circuit (flag / routing ancillas included) is simulated **once**;
    each candidate permutation is tested by peeking the permuted data-qubit
    stabilizers on the fixed state (rather than relabelling and re-simulating per
    permutation) — orders of magnitude faster, which makes an exhaustive small-n
    (n≲9) search practical. Simulating the full circuit is also what lets it fit
    circuits whose data qubits interact *through* routing ancillas.
    """
    peek = _simulate(circuit, n)
    supports = [_row_support(row, n) for row in H]

    def fits(sigma) -> bool:
        return all(peek(support, sigma) == 1 for support in supports)

    if fits(list(range(n))):
        return FitResult(permutation=None, status="identity")
    for tried, perm in enumerate(itertools.permutations(range(n))):
        if tried > max_perms:
            break
        if fits(perm):
            return FitResult(permutation=list(perm), status="found")
    return FitResult(permutation=None, status="not_found")


def fit_circuit_to_candidates(
    circuit: Union[str, stim.Circuit],
    H: np.ndarray,
    n: int,
    candidates: "tuple[tuple[int, ...], ...] | list[tuple[int, ...]]" = (),
) -> Optional[list[int]]:
    """Return the first permutation — identity tried first, then each of
    ``candidates`` (convention ``sigma[new] = old``) — under which ``circuit``
    prepares a ``+1`` eigenstate of every stabilizer of symplectic ``H``, or
    ``None`` if none fits.

    One simulation of the full circuit, a cheap peek per candidate (the same
    engine as :func:`_search_permutation`). Use this when an exhaustive search is
    infeasible (large ``n``) but a few candidate permutations are known, or to
    cheaply confirm the identity fit.
    """
    peek = _simulate(circuit, n)
    supports = [_row_support(row, n) for row in np.asarray(H, dtype=int)]
    for sigma in [tuple(range(n)), *candidates]:
        if all(peek(support, list(sigma)) == 1 for support in supports):
            return list(sigma)
    return None


def fit_circuit_to_anchor_h(
    zero_circuit: Union[str, stim.Circuit],
    H: np.ndarray,
    n: int,
    max_perms: int = 500_000,
) -> FitResult:
    """Symplectic (non-CSS-capable) analogue of :func:`fit_circuit_to_anchor`.

    Finds a data-qubit permutation so the circuit validates against anchor ``H``.
    Exhaustive for n ≤ 9 (9! < the default budget). The full circuit is used
    (ancillas are not stripped) so it also fits routing-ancilla circuits.
    """
    circ = zero_circuit if isinstance(zero_circuit, stim.Circuit) else stim.Circuit(zero_circuit)
    return _search_permutation(circ, np.asarray(H, dtype=int), n, max_perms)


def anchor_h_in_circuit_labeling(H: np.ndarray, n: int, fit: FitResult) -> np.ndarray:
    """Express canonical anchor ``H`` in the circuit's own qubit labeling.

    Given a ``fit`` (``perm[new] = old``) that relabels the circuit *into* the
    canonical frame, permute the columns of ``H`` the opposite way so the result
    describes the same code in the circuit's original labeling. Feeding this to
    ``add_circuit`` lets it re-derive and apply the permutation itself (keeping
    the untouched original circuit + matrices in ``originals/``).
    """
    if fit.permutation is None:
        return H.copy()
    # perm[new] = old  =>  circuit qubit `old` plays canonical role `new`.
    # Canonical column `new` must move to circuit column `old`.
    old_of_new = fit.permutation
    Hc = np.zeros_like(H)
    for new, old in enumerate(old_of_new):
        Hc[:, old] = H[:, new]  # X-half
        Hc[:, old + n] = H[:, new + n]  # Z-half
    return Hc


# ---------------------------------------------------------------------------
# High-level driver: derive/anchor -> verify -> add_circuit -> capture provenance
# ---------------------------------------------------------------------------


def import_state_prep(
    *,
    circuit: Union[str, stim.Circuit],
    n: int,
    d: int,
    code_name: str,
    circuit_name: str,
    method: str,
    plus_circuit: Union[str, stim.Circuit, None] = None,
    anchor_H: Optional[np.ndarray] = None,
    permutation: Optional[list[int]] = None,
    zoo_url: str = "",
    code_slug: str = "",
    code_tags: Optional[list[str]] = None,
    source: str = "",
    tool: str = "",
    tags: Optional[list[str]] = None,
    notes: Optional[str] = None,
    source_file: Optional[str] = None,
    logical_state: Optional[str] = None,
    connectivity: Optional[str] = None,
    gate_set: Optional[str] = None,
    device: Optional[str] = None,
    qubit_placement: Optional[str] = None,
    data_dir: str = "data_yaml",
    dry_run: bool = False,
) -> "AddCircuitResult":
    """Import one state-preparation circuit, fitting it to a single canonical code.

    ``method`` selects how the code's check matrices are obtained *in the
    circuit's own labeling* before handing off to :func:`add_circuit`:

    * ``"self_dual"`` — CSS self-dual code, ``Hz == Hx`` from a single |0_L>
      circuit.
    * ``"two_circuit"`` — ``Hx`` from |0_L> (``circuit``) and ``Hz`` from |+_L>
      (``plus_circuit``). Both must share a qubit labeling.
    * ``"anchor"`` — fit against a trusted symplectic ``anchor_H``. Required for
      non-CSS / non-self-dual codes, and for importing non-|0> states of a known
      code (the fit validates codespace membership for any logical state).

    ``permutation`` (optional) supplies the qubit permutation onto the stored
    code directly (convention ``sigma[new] = old``), bypassing ``add_circuit``'s
    dedup search — use it with ``self_dual`` / ``two_circuit`` for
    automorphism-rich codes where the search cannot confirm equivalence in time.

    The untouched ``circuit`` (flags included) is what gets stored; ``add_circuit``
    dedups it to the canonical code, applies the permutation, and preserves the
    original circuit + matrices in ``originals/``.

    Provenance / hardware metadata that has no dedicated schema field
    (``source_file``, ``logical_state``, ``connectivity``, ``gate_set``,
    ``device``, ``qubit_placement``) is recorded in the circuit ``notes`` and, for
    the categorical ones, as ``key:value`` tags — so nothing on the source side is
    silently dropped. The qubit permutation applied during canonicalization is
    appended to ``notes`` when non-trivial (it is otherwise only recoverable by
    diffing the ``originals/`` circuit against the stored body).
    """
    from . import add_circuit

    # 1. Derive the code matrices in the circuit's own labeling.
    code_kwargs: dict = {}
    if method == "self_dual":
        Hx, Hz = derive_matrices_self_dual(circuit, n)
        fit = fit_circuit_to_anchor(circuit, Hx, Hz, n)
        code_kwargs = {"Hx": Hx, "Hz": Hz}
    elif method == "two_circuit":
        if plus_circuit is None:
            raise ValueError("method='two_circuit' requires plus_circuit.")
        Hx, Hz = derive_matrices_two_circuit(circuit, plus_circuit, n)
        fit = fit_circuit_to_anchor(circuit, Hx, Hz, n)
        code_kwargs = {"Hx": Hx, "Hz": Hz}
    elif method == "anchor":
        if anchor_H is None:
            raise ValueError("method='anchor' requires anchor_H.")
        # With a supplied permutation, skip the (unscalable) search and use it.
        if permutation is not None:
            fit = FitResult(list(permutation), "found")
        else:
            fit = fit_circuit_to_anchor_h(circuit, anchor_H, n)
        code_kwargs = {"H": anchor_h_in_circuit_labeling(anchor_H, n, fit), "n": n}
    else:
        raise ValueError(f"Unknown method {method!r}. Use 'self_dual', 'two_circuit', or 'anchor'.")
    _require_fit(fit, circuit_name)

    # 1b. Determine the logical-state tag. For a CSS code the *basis* (Z vs X) is
    #     reliably derivable from the check matrices, so we use it: if it agrees
    #     with the source's label we keep that label (its 0/1 resp. +/- sign is
    #     authoritative); if it disagrees (e.g. Shor, whose X/Z convention is
    #     opposite to the library's) we use the library basis and note the source
    #     label. For a non-CSS code the logical X-bar/Z-bar ordering is not
    #     canonical, so auto-detection is unreliable and we take the source label.
    from .code_identify import split_h_to_css

    matrices = _code_kwargs_matrices(code_kwargs)
    if "Hx" in matrices:
        hx, hz = matrices["Hx"], matrices["Hz"]
    elif "H" in matrices:
        split = split_h_to_css(np.asarray(matrices["H"], dtype=int), n)
        hx, hz = split if split is not None else (None, None)
    else:
        hx = hz = None

    source_state = logical_state  # what the caller (the source) says
    original_state = None
    if hx is not None:  # CSS: basis is reliable
        lib_basis = logical_basis_of(circuit, n, d, Hx=hx, Hz=hz)
        if source_state and _STATE_BASIS.get(source_state) == lib_basis:
            logical_state = source_state  # basis agrees — keep the source's exact label
        elif lib_basis in ("z", "x"):
            logical_state = "zero" if lib_basis == "z" else "plus"
            original_state = source_state  # basis differs — record the source label
        else:
            logical_state = source_state
    else:  # non-CSS: trust the source label
        logical_state = source_state

    circuit_text = _as_text(circuit)
    common = dict(
        circuit=circuit_text,
        circuit_name=circuit_name,
        d=d,
        code_name=code_name,
        zoo_url=zoo_url,
        code_slug=code_slug,
        code_tags=code_tags,
        source=source,
        tool=tool,
        data_dir=data_dir,
        qubit_permutation=permutation,
        **code_kwargs,
    )

    # 2. Determine the permutation add_circuit will apply (canonical<-orig) for
    #    the notes. A supplied permutation is known already; otherwise a dry run
    #    computes it (skipped when supplied — it saves a full pass, which matters
    #    for large codes where the logical-operator computation is costly).
    if permutation is not None:
        applied_perm = list(permutation)
    else:
        applied_perm = add_circuit(**common, tags=tags, dry_run=True).qubit_permutation

    # 3. Assemble notes + structured tags capturing everything else.
    flag_qubits = list(range(n, stim.Circuit(circuit_text).num_qubits))
    notes = _build_notes(
        base_notes=notes,
        source_file=source_file,
        logical_state=logical_state,
        original_logical_state=original_state,
        connectivity=connectivity,
        gate_set=gate_set,
        device=device,
        flag_qubits=flag_qubits,
        qubit_placement=qubit_placement,
        permutation=applied_perm,
    )
    full_tags = _augment_tags(
        tags,
        connectivity=connectivity,
        device=device,
        logical_state=logical_state,
        has_flags=bool(flag_qubits),
    )

    # 4. Real write with the enriched metadata.
    return add_circuit(**common, tags=full_tags, notes=notes, dry_run=dry_run)


def _build_notes(
    *,
    base_notes: Optional[str],
    source_file: Optional[str],
    logical_state: Optional[str],
    original_logical_state: Optional[str] = None,
    connectivity: Optional[str],
    gate_set: Optional[str],
    device: Optional[str],
    flag_qubits: list[int],
    qubit_placement: Optional[str],
    permutation: Optional[list[int]],
) -> str:
    """Fold otherwise-unschema'd provenance into a single ``notes`` string."""
    parts: list[str] = []
    if base_notes:
        parts.append(base_notes)
    if source_file:
        parts.append(f"Source file: {source_file}")
    if logical_state:
        parts.append(f"Logical state: {logical_state}")
    # Record the source's own label when it differs from the library-convention
    # one above (e.g. the paper prepares |+> of a code the library stores with the
    # opposite X/Z convention, so it reads as a Z-basis state here).
    if original_logical_state and original_logical_state != logical_state:
        parts.append(f"Original (source) logical state: {original_logical_state}")
    if connectivity:
        parts.append(f"Connectivity: {connectivity}")
    if gate_set:
        parts.append(f"Gate set: {gate_set}")
    if device:
        parts.append(f"Device: {device}")
    if flag_qubits:
        parts.append(f"Flag/ancilla qubits: {flag_qubits}")
    if qubit_placement:
        parts.append(f"Device qubit placement (Qiskit indices): {qubit_placement}")
    if permutation is not None:
        parts.append(
            "Canonicalization qubit permutation "
            f"(stored qubit i = original qubit permutation[i]): {permutation}"
        )
    return ". ".join(parts)


def _augment_tags(
    tags: Optional[list[str]],
    *,
    connectivity: Optional[str],
    device: Optional[str],
    logical_state: Optional[str],
    has_flags: bool,
) -> list[str]:
    """Add categorical metadata as ``key:value`` tags (deduped, order-stable)."""
    out = list(tags) if tags else []
    extra = []
    if connectivity:
        extra.append(f"connectivity:{connectivity}")
    if device:
        extra.append(f"device:{device}")
    if logical_state:
        extra.append(f"logical-state:{logical_state}")
    if has_flags and "flag" not in out:
        extra.append("flag")
    for t in extra:
        if t not in out:
            out.append(t)
    return out


def _code_kwargs_matrices(code_kwargs: dict) -> dict:
    """Extract just the matrix args (Hx/Hz or H) for :func:`logical_state_of`,
    dropping ``n`` which that function already takes positionally."""
    return {k: v for k, v in code_kwargs.items() if k in ("Hx", "Hz", "H")}


def _as_text(circuit: Union[str, stim.Circuit]) -> str:
    return str(circuit) if isinstance(circuit, stim.Circuit) else circuit


def _require_fit(fit: FitResult, circuit_name: str) -> None:
    if fit.status == "not_found":
        raise ValueError(
            f"Could not fit circuit {circuit_name!r} to the code within the "
            f"permutation search budget. The circuit may prepare a different "
            f"code, or need a larger/aligned search."
        )
