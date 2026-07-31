"""Find the qubit permutation that maps one CSS code onto another.

Split out of the asyndrome import, which wrote it, because three importers now
need it: a code can match a stored one on every cheap invariant and still defeat
`find_code_permutation`'s search budget. That happens exactly where you would
expect — topological codes with large automorphism groups, whose column
invariants barely separate anything.

This matcher uses the natural check structure of such a code instead: its
low-weight checks pin a qubit's local geometry down hard. The catch is that *a*
low-weight basis is not canonical — `sparsify_basis` returns weight-4 generators
for two codes, but not the same ones, so the hypergraphs are incomparable. The
set of all low-weight **codewords** is canonical, and cheap to enumerate
exactly: in RREF each row owns a pivot column no other row touches, so a
codeword of weight <= w is the sum of at most w rows. Enumerating subsets that
small is nothing, and it is exhaustive rather than a heuristic.

From there: colour refinement over that hypergraph, then backtracking with a
pairwise co-occurrence test.

Nothing here is trusted on its own. Every candidate is confirmed by row-space
equality against the stored code, and `add_circuit` repeats that check on every
import, so a wrong or stale sigma fails loudly rather than quietly mislabeling
a code's qubits.
"""

from __future__ import annotations

import itertools
from collections import defaultdict

import numpy as np

from .code_identify import gf2_rank, gf2_row_basis, gf2_rref

# Codeword weights to try, smallest first: the search widens until the words span
# the whole space (see `_checks`). Enumerating up to weight w costs C(rank, w)
# subsets, so the cap is where that stops being cheap.
WEIGHTS = (2, 3, 4, 5, 6, 7, 8, 9, 10)


def low_weight_codewords(H: np.ndarray, wmax: int) -> list[frozenset[int]]:
    """Every codeword of weight <= ``wmax`` in the row space of ``H``.

    Exhaustive, and canonical in a way no basis is. Reducing to RREF gives each
    row a private pivot column, so a sum of ``s`` rows has exactly ``s`` ones
    among the pivots — a codeword of weight <= wmax therefore uses at most
    ``wmax`` rows, and enumerating subsets that small covers all of them.

    Rows are packed into Python ints so a subset sum is one XOR and its weight
    one ``bit_count``; at weight 8 over a rank-24 space that is 735k subsets, and
    the packed form is what keeps it seconds rather than minutes.
    """
    basis = gf2_rref(np.asarray(H, dtype=int) % 2)
    basis = basis[np.any(basis, axis=1)]
    n = basis.shape[1]
    packed = [int("".join(str(int(b)) for b in row), 2) for row in basis]

    found: set[frozenset[int]] = set()
    for size in range(1, min(wmax, len(packed)) + 1):
        for subset in itertools.combinations(packed, size):
            word = 0
            for row in subset:
                word ^= row
            if 0 < word.bit_count() <= wmax:
                bits = format(word, f"0{n}b")
                found.add(frozenset(q for q in range(n) if bits[q] == "1"))
    return sorted(found, key=lambda s: (len(s), sorted(s)))


def _spanning_codewords(H: np.ndarray) -> list[frozenset[int]]:
    """Low-weight codewords of ``H``, widened until they span its whole row space.

    Spanning is the condition that makes the reduction to a graph **lossless**: if
    the codewords generate the code, a relabeling preserving them preserves the
    code, and an isomorphism of the incidence structure is a code equivalence. If
    they only span a subspace, the graph describes that subspace and nothing else
    — every complete map then fails the final row-space check, and the search
    exhausts instead of answering.

    That is not hypothetical. The 4.8.8 colour code's 36 weight-4 squares span
    rank 18 of 24; its octagons carry the rest. Stopping at "enough words" instead
    of "spanning" is what made `color-oct-9` look intractable.
    """
    target = len(gf2_row_basis(H))
    n = H.shape[1]
    for wmax in WEIGHTS:
        words = low_weight_codewords(H, wmax)
        if not words:
            continue
        matrix = np.zeros((len(words), n), dtype=int)
        for i, support in enumerate(words):
            for q in support:
                matrix[i, q] = 1
        if gf2_rank(matrix) == target:
            return words
    raise ValueError(f"low-weight codewords up to weight {WEIGHTS[-1]} do not span the code")


def _checks(Hx: np.ndarray, Hz: np.ndarray) -> list[tuple[int, frozenset[int]]]:
    """The canonical, spanning low-weight codeword hypergraph, as (type, support).

    Weight classes are distinguished by the initial colouring (which includes each
    check's size), so widening past the minimum weight adds structure rather than
    blurring it.
    """
    return [(kind, s) for kind, H in ((0, Hx), (1, Hz)) for s in _spanning_codewords(H)]


def _refine(n: int, incident, checks, colour: list) -> list:
    """Weisfeiler-Leman refinement of a qubit colouring over the check hypergraph.

    A qubit's new colour is its old one plus, for each check it sits in, that
    check's type and the multiset of its members' colours. Iterated to a fixpoint.
    Colours are canonicalised to small integers by sorted order, which is what
    makes two codes' colourings comparable — the value depends only on structure,
    never on qubit numbering.
    """
    while True:
        refined = [
            (
                colour[q],
                tuple(
                    sorted(
                        (checks[i][0], tuple(sorted(colour[p] for p in checks[i][1])))
                        for i in incident[q]
                    )
                ),
            )
            for q in range(n)
        ]
        keys = {c: i for i, c in enumerate(sorted(set(refined)))}
        new = [keys[c] for c in refined]
        if new == colour:
            return colour
        colour = new


def _incidence(n: int, checks):
    incident = defaultdict(list)
    for index, (_kind, support) in enumerate(checks):
        for q in support:
            incident[q].append(index)
    return incident


def _initial(n: int, incident, checks) -> list:
    """The degree-and-weight colouring refinement starts from."""
    seed = [tuple(sorted((checks[i][0], len(checks[i][1])) for i in incident[q])) for q in range(n)]
    keys = {c: i for i, c in enumerate(sorted(set(seed)))}
    return [keys[c] for c in seed]


def find_sigma(Hx1, Hz1, Hx2, Hz2) -> list[int] | None:
    """sigma with ``Hx1[:, sigma]`` spanning ``Hx2`` (convention sigma[new] = old).

    Individualization-refinement, the technique canonical-labelling tools are
    built on. Refinement alone stops at the code's automorphism orbits — for the
    4.8.8 colour code that is four classes of a dozen qubits, and no invariant
    will do better, because those qubits really are interchangeable. The move is
    to stop asking: pick a qubit, *declare* it its own colour, and refine again.
    The symmetry that made the class large is exactly what makes the choice free,
    and one round of it usually shatters the rest of the classes.

    Plain backtracking with a static order — refine once, then guess — is what
    this replaces. It searched the 4.8.8 code for minutes without an answer;
    re-refining after each choice settles it in well under a second.

    Nothing here is trusted: the accepted sigma is checked by exact row-space
    equality over GF(2), and `add_circuit` checks it again on every import.
    """
    n = Hx1.shape[1]
    checks1, checks2 = _checks(Hx1, Hz1), _checks(Hx2, Hz2)
    inc1, inc2 = _incidence(n, checks1), _incidence(n, checks2)
    colour1 = _refine(n, inc1, checks1, _initial(n, inc1, checks1))
    colour2 = _refine(n, inc2, checks2, _initial(n, inc2, checks2))

    def verify(sigma) -> bool:
        return np.array_equal(gf2_row_basis(Hx1[:, sigma]), gf2_row_basis(Hx2)) and np.array_equal(
            gf2_row_basis(Hz1[:, sigma]), gf2_row_basis(Hz2)
        )

    def search(c1: list, c2: list, sigma: dict) -> list[int] | None:
        # Comparable colourings are the invariant: a mismatch anywhere means this
        # branch cannot extend to an isomorphism.
        if sorted(c1) != sorted(c2):
            return None
        classes = defaultdict(list)
        for q, c in enumerate(c2):
            classes[c].append(q)

        open_class = min(
            (c for c, qs in classes.items() if len(qs) > 1),
            key=lambda c: len(classes[c]),
            default=None,
        )
        if open_class is None:
            candidate = [0] * n
            for new, c in enumerate(c2):
                candidate[new] = c1.index(c)
            return candidate if verify(candidate) else None

        new = classes[open_class][0]
        fresh = max(max(c1), max(c2)) + 1
        for old in (q for q, c in enumerate(c1) if c == open_class):
            if old in sigma.values():
                continue
            d1, d2 = list(c1), list(c2)
            d1[old] = fresh
            d2[new] = fresh
            found = search(
                _refine(n, inc1, checks1, d1),
                _refine(n, inc2, checks2, d2),
                {**sigma, new: old},
            )
            if found is not None:
                return found
        return None

    return search(colour1, colour2, {})
