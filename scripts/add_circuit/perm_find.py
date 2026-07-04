"""Structural qubit-permutation finder between equivalent CSS codes.

Given two CSS codes as (Hx, Hz) row spaces over GF(2), find a qubit
permutation sigma (convention: ``sigma[new] = old``) such that permuting the
columns of code 1 yields the row spaces of code 2.

Approach (independent implementation; inspired by N. Sendrier, "Finding the
Permutation Between Equivalent Linear Codes: The Support Splitting
Algorithm", and the benchmarking in github.com/MaxieHelenBichmann/bm_qecc):

1. Per-column invariants from two families:
   a. single/pair puncture ranks of Hx and Hz (always available), and
   b. per-column / per-pair incidence histograms of low-weight codewords
      (weight <= CODEWORD_WMAX), enumerated when rank <= CODEWORD_RANK_MAX.
      Family (b) is what makes highly symmetric LDPC codes (e.g. the rotated
      surface code) tractable.
2. Weisfeiler-Leman colour refinement using the pair invariants.
3. Most-constrained-first backtracking with pair-invariant consistency and
   incremental prefix-rank pruning; a full row-space equality check accepts
   the final candidate. Callers MUST still verify the returned sigma
   (add_circuit's row-space check does) — this module never bypasses
   verification.
"""

from __future__ import annotations

import itertools
from collections import Counter
from typing import Optional

import numpy as np

from .code_identify import gf2_rank, gf2_rref

CODEWORD_WMAX = 6
CODEWORD_RANK_MAX = 16
DEFAULT_BUDGET = 3_000_000


def _rowspace_key(m: np.ndarray) -> tuple[bytes, tuple[int, ...]]:
    r = gf2_rref(np.asarray(m) % 2)
    r = r[~np.all(r == 0, axis=1)]
    return r.tobytes(), r.shape


def _puncture_rank(m: np.ndarray, cols: set[int]) -> int:
    keep = [c for c in range(m.shape[1]) if c not in cols]
    return gf2_rank(m[:, keep])


def _all_words(m: np.ndarray) -> np.ndarray:
    """All codewords of the row space (requires rank <= CODEWORD_RANK_MAX)."""
    r = gf2_rref(np.asarray(m) % 2)
    r = r[~np.all(r == 0, axis=1)].astype(np.uint8)
    words = np.zeros((1, m.shape[1]), dtype=np.uint8)
    for row in r:
        words = np.vstack([words, words ^ row])
    return words


def _invariants(hx: np.ndarray, hz: np.ndarray):
    """Per-column colours and per-pair labels from both invariant families."""
    n = hx.shape[1]
    col: dict[int, tuple] = {i: () for i in range(n)}
    pair: dict[tuple[int, int], tuple] = {
        (i, j): () for i, j in itertools.combinations(range(n), 2)
    }
    for m in (hx, hz):
        for i in range(n):
            col[i] += (_puncture_rank(m, {i}),)
        for i, j in itertools.combinations(range(n), 2):
            pair[(i, j)] += (_puncture_rank(m, {i, j}),)
        if gf2_rank(m) <= CODEWORD_RANK_MAX:
            words = _all_words(m)
            wts = words.sum(axis=1)
            sel = words[(wts > 0) & (wts <= CODEWORD_WMAX)]
            swts = sel.sum(axis=1)
            for i in range(n):
                col[i] += (tuple(sorted(int(w) for w, row in zip(swts, sel) if row[i])),)
            for i, j in itertools.combinations(range(n), 2):
                pair[(i, j)] += (
                    tuple(sorted(int(w) for w, row in zip(swts, sel) if row[i] and row[j])),
                )
    colors: dict[int, object] = dict(col)
    for _ in range(n):
        new: dict[int, object] = {}
        for i in range(n):
            nb = tuple(sorted((pair[tuple(sorted((i, j)))], colors[j]) for j in range(n) if j != i))
            new[i] = hash((colors[i], nb))
        if len(set(new.values())) <= len(set(colors.values())):
            break
        colors = new
    return colors, pair


def find_code_permutation(
    hx1: np.ndarray,
    hz1: np.ndarray,
    hx2: np.ndarray,
    hz2: np.ndarray,
    budget: int = DEFAULT_BUDGET,
) -> Optional[list[int]]:
    """Find sigma (``sigma[new] = old``) mapping code 1's row spaces onto code 2's.

    Returns None when no permutation is found (inequivalent codes, or search
    budget exceeded).
    """
    hx1 = np.asarray(hx1, dtype=int) % 2
    hz1 = np.asarray(hz1, dtype=int) % 2
    hx2 = np.asarray(hx2, dtype=int) % 2
    hz2 = np.asarray(hz2, dtype=int) % 2
    n = hx1.shape[1]
    if hx2.shape[1] != n or hz1.shape[1] != n or hz2.shape[1] != n:
        return None
    if gf2_rank(hx1) != gf2_rank(hx2) or gf2_rank(hz1) != gf2_rank(hz2):
        return None

    c1, p1 = _invariants(hx1, hz1)
    c2, p2 = _invariants(hx2, hz2)
    if Counter(c1.values()) != Counter(c2.values()):
        return None

    cands = {j: frozenset(i for i in range(n) if c1[i] == c2[j]) for j in range(n)}
    target_x, target_z = _rowspace_key(hx2), _rowspace_key(hz2)
    sigma: list[Optional[int]] = [None] * n
    used: set[int] = set()
    assigned: list[int] = []
    steps = 0

    def prefix_ok() -> bool:
        old_cols = [sigma[j] for j in assigned]
        return gf2_rank(hx1[:, old_cols]) == gf2_rank(hx2[:, assigned]) and gf2_rank(
            hz1[:, old_cols]
        ) == gf2_rank(hz2[:, assigned])

    def next_col() -> int:
        best, best_avail = -1, n + 1
        for j in range(n):
            if sigma[j] is not None:
                continue
            avail = sum(1 for i in cands[j] if i not in used)
            if avail < best_avail:
                best, best_avail = j, avail
        return best

    def backtrack() -> bool:
        nonlocal steps
        if len(assigned) == n:
            p = np.array(sigma)
            return _rowspace_key(hx1[:, p]) == target_x and _rowspace_key(hz1[:, p]) == target_z
        j = next_col()
        for i in cands[j]:
            if i in used:
                continue
            if not all(
                p1[tuple(sorted((i, sigma[jj])))] == p2[tuple(sorted((j, jj)))] for jj in assigned
            ):
                continue
            steps += 1
            if steps > budget:
                raise TimeoutError
            sigma[j] = i
            used.add(i)
            assigned.append(j)
            if prefix_ok() and backtrack():
                return True
            sigma[j] = None
            used.discard(i)
            assigned.pop()
        return False

    try:
        found = backtrack()
    except TimeoutError:
        return None
    return [int(x) for x in sigma] if found else None  # type: ignore[misc]
