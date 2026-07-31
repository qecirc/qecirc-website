"""Subsystem codes: the gauge group, and the k it implies.

A stabilizer code is described by one group. A **subsystem code** is described by
two: the *gauge* group `G` a decoder may measure, and the *stabilizer* group
`S` — the centre of `G` — whose outcomes are actually deterministic. The
difference between them is real qubits: `(rank(G) - rank(S)) / 2` **gauge
qubits**, which carry no information and are not corrected.

That is the whole reason this file exists. The library stores one check matrix
per code and read `k` off it as `n - rank(h)`, which is right only when the two
groups coincide. Storing Bacon-Shor [[9,1,3]] that way gives [[9,5,3]] — the four
gauge qubits counted as logical ones — so the codes were excluded rather than
recorded wrongly. With the gauge group in hand:

    k = n - rank(S) - (rank(G) - rank(S)) / 2

and for a stabilizer code `G == S`, the gauge term is zero and the formula is the
one the library already used. There is no separate code path.

**What is stored where.** `h` keeps meaning the stabilizer group, for every code,
so validators, dedup, the CSS split and the matrices view are untouched — a
circuit is checked against the operators that are deterministic, which is what
those checks want. The gauge group goes in its own field, present only when it
differs from `h`.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from .code_identify import gf2_rank


def symplectic_product(a: np.ndarray, b: np.ndarray, n: int) -> np.ndarray:
    """`a_i` against `b_j`: 0 where they commute, 1 where they anticommute."""
    a = np.asarray(a, dtype=int) % 2
    b = np.asarray(b, dtype=int) % 2
    return (a[:, :n] @ b[:, n:].T + a[:, n:] @ b[:, :n].T) % 2


def gauge_qubits(gauge: np.ndarray, stabilizers: np.ndarray, n: int) -> int:
    """How many gauge qubits `G` carries over `S`.

    Raises when the difference is odd, which no valid pair can produce: gauge
    qubits come in anticommuting pairs, so `rank(G) - rank(S)` is always even.
    An odd value means the two matrices do not describe the same code, and
    guessing a `k` from them would be worse than refusing.
    """
    gap = gf2_rank(gauge) - gf2_rank(stabilizers)
    if gap < 0:
        raise ValueError("the stabilizer group cannot outrank the gauge group")
    if gap % 2:
        raise ValueError(
            f"rank(gauge) - rank(stabilizers) = {gap} is odd; gauge qubits come in "
            "anticommuting pairs, so these two matrices are not one code"
        )
    del n  # signature kept uniform with the rest of this module
    return gap // 2


def logical_qubits(gauge: np.ndarray, stabilizers: np.ndarray, n: int) -> int:
    """`k` for a code given both groups. Reduces to `n - rank(h)` when equal."""
    return n - gf2_rank(stabilizers) - gauge_qubits(gauge, stabilizers, n)


def check_stabilizers_are_central(gauge: np.ndarray, stabilizers: np.ndarray, n: int) -> None:
    """Refuse a pair where `S` is not inside the centre of `G`.

    The centre is what makes `S`'s outcomes deterministic; a "stabilizer" that
    anticommutes with a gauge operator is not one, and every number derived here
    would be meaningless. Cheap to check and worth checking, because the two
    matrices arrive from a caller that could have paired them up wrongly.
    """
    stabilizers = np.atleast_2d(np.asarray(stabilizers, dtype=int) % 2)
    if not stabilizers.size:
        return
    if symplectic_product(stabilizers, np.asarray(gauge, dtype=int) % 2, n).any():
        raise ValueError(
            "a stabilizer anticommutes with a gauge operator, so the stabilizer "
            "group is not central in the gauge group"
        )


def describe(
    gauge: Optional[np.ndarray], stabilizers: np.ndarray, n: int
) -> tuple[int, int, Optional[np.ndarray]]:
    """`(k, gauge_qubit_count, gauge_to_store)` for a code.

    `gauge` may be None, or equal to the stabilizer group; either way this is a
    stabilizer code, the count is zero and nothing extra is stored.
    """
    stabilizers = np.asarray(stabilizers, dtype=int) % 2
    if gauge is None:
        return n - gf2_rank(stabilizers), 0, None

    gauge = np.asarray(gauge, dtype=int) % 2
    if gauge.shape[1] != stabilizers.shape[1]:
        raise ValueError(
            f"gauge group is {gauge.shape[1]} columns and the stabilizer group "
            f"{stabilizers.shape[1]}; both must be 2n = {2 * n}"
        )
    check_stabilizers_are_central(gauge, stabilizers, n)
    count = gauge_qubits(gauge, stabilizers, n)
    if count == 0:
        return n - gf2_rank(stabilizers), 0, None
    return n - gf2_rank(stabilizers) - count, count, gauge
