#!/usr/bin/env python
"""Exact CSS code distance, for the one dataset code that ships without one.

`qecc/self-dual-bbcode.json` gives `d: -1`, and a code YAML needs a real
distance — so its schedule was left out of the import. This computes the
distance rather than guessing it.

The definition, and the whole method: a Z-type logical operator is a vector in
ker(Hx) that is not in the row space of Hz, and `d_Z` is the smallest weight of
one. Every such vector is (some combination of Hz rows) XOR (some *non-zero*
combination of the Z-logicals), so enumerating both sides covers all of them
exactly once — no sampling, no bound, no decoder. `d = min(d_X, d_Z)`.

That is 2^rank(Hz) x (2^k - 1) vectors. It is only affordable because the numbers
here are small: the self-dual bivariate bicycle code is [[42,6,d]] with rank 18
per side, so 63 x 262144 = 16.5M candidates, each one XOR and one popcount on a
packed 64-bit word. Doubling the combination table and letting numpy count bits
makes it a couple of seconds. Nothing about it scales — a [[144,12,12]] code
would need 2^66 — which is exactly why it lives here and not in the pipeline.

Run from the repository root:

    uv run python data-imports/asyndrome/code_distance.py [--dataset PATH] [--code KEY]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DATASET = REPO.parent / "asyndrome"
sys.path.insert(0, str(REPO))

from scripts.add_circuit.code_identify import gf2_row_basis  # noqa: E402

# Refuse rather than run for hours. The work is 2^rank x (2^k - 1) vectors, so
# the budget is on rank + k, not on either alone: a [[60,18,4]] hyperbolic code
# has a modest rank 21 and still needs 2^39 candidates.
MAX_LOG2_WORK = 26


def _pack(rows: np.ndarray) -> list[int]:
    """Each binary row as one Python int (n <= 63 assumed, checked by caller)."""
    return [int("".join(str(int(b)) for b in row), 2) for row in rows]


def _all_combinations(packed: list[int]) -> np.ndarray:
    """Every XOR-combination of ``packed``, by repeated doubling."""
    out = np.zeros(1, dtype=np.uint64)
    for row in packed:
        out = np.concatenate([out, out ^ np.uint64(row)])
    return out


def css_distance_half(stabilizers: np.ndarray, logicals: np.ndarray) -> int:
    """Minimum weight of a non-trivial logical in one CSS sector.

    ``stabilizers`` and ``logicals`` are binary matrices over the same n columns:
    the checks of one type and the logical operators of the *other* type's
    partner (Hz with Lz for the Z sector).
    """
    basis = gf2_row_basis(stabilizers)
    logical_basis = gf2_row_basis(logicals)
    work = len(basis) + len(logical_basis)
    if work > MAX_LOG2_WORK:
        raise ValueError(
            f"2^{work} candidates (rank {len(basis)}, k {len(logical_basis)}) "
            f"exceeds the 2^{MAX_LOG2_WORK} budget"
        )

    cosets = _all_combinations(_pack(basis))
    best = None
    for rep in _all_combinations(_pack(logical_basis))[1:]:  # skip the trivial class
        weight = int(np.bitwise_count(cosets ^ rep).min())
        if best is None or weight < best:
            best = weight
    if best is None:
        raise ValueError("no logical operators: k = 0")
    return best


def css_distance(Hx: np.ndarray, Hz: np.ndarray, Lx: np.ndarray, Lz: np.ndarray) -> tuple[int, int]:
    """``(d_X, d_Z)``; the code distance is the smaller."""
    return (
        css_distance_half(Hx, Lx),
        css_distance_half(Hz, Lz),
    )


def _load(path: Path):
    """Dataset JSON to (Hx, Hz, Lx, Lz), reading the Pauli from the string.

    `self-dual-bbcode.json` has its two stabilizer fields swapped, so the key is
    not to be trusted — see the import README.
    """
    doc = json.loads(path.read_text())
    n = doc["n"]

    def rows(strings, pauli):
        picked = [s for s in strings if pauli in s]
        if not picked:
            return np.zeros((0, n), dtype=int)
        return np.array([[1 if c == pauli else 0 for c in s] for s in picked], dtype=int)

    stabilizers = doc["x_stabilizers"] + doc["z_stabilizers"]
    return (
        rows(stabilizers, "X"),
        rows(stabilizers, "Z"),
        rows(doc["logical_xs"], "X"),
        rows(doc["logical_zs"], "Z"),
        doc,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Exact CSS distance of a dataset code")
    parser.add_argument("--dataset", default=str(DATASET))
    parser.add_argument("--code", default="self-dual-bbcode")
    args = parser.parse_args()

    Hx, Hz, Lx, Lz, doc = _load(Path(args.dataset) / "qecc" / f"{args.code}.json")
    dx, dz = css_distance(Hx, Hz, Lx, Lz)
    print(f"{args.code}: [[{doc['n']},{doc['k']}]] declared d = {doc['d']}")
    print(f"  d_X = {dx}   d_Z = {dz}   ->  d = {min(dx, dz)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
