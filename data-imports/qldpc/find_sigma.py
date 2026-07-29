#!/usr/bin/env python
"""Compute the qubit permutations this import needs, into sigma_precomputed.json.

Three of qLDPC's codes are the same code as a stored entry under a different
qubit order, but `find_code_permutation`'s budget runs out on them: they are
topological codes with large automorphism groups, which is precisely the case
its column invariants cannot separate.

The matcher itself is not rewritten here. `data-imports/asyndrome/find_sigma.py`
solved exactly this problem for exactly this kind of code — low-weight codewords
as a canonical hypergraph, then individualization-refinement — so this reuses its
`find_sigma` rather than keeping a second copy of 250 lines that would drift.

Nothing is trusted on its own: each candidate is confirmed here by row-space
equality against the stored code, and `add_circuit` repeats that check on every
import, so a wrong or stale sigma fails loudly instead of quietly publishing a
circuit for the wrong qubit layout.

Run from the repository root:

    uv run --with 'qldpc==0.3.2' python data-imports/qldpc/find_sigma.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "data-imports" / "asyndrome"))

from codes import CATALOGUE  # noqa: E402
from find_sigma import find_sigma  # noqa: E402  (the asyndrome import's matcher)

from scripts.add_circuit.code_identify import gf2_rref, split_h_to_css  # noqa: E402

# catalogue key -> stored code slug it should attach to.
TARGETS = {
    "surface-d7": "rotated-surface-code-d-7",
    "surface-d3-unrotated": "unrotated-surface-code-d-3",
    "toric-d4": "16-2-4",
}


def row_space(matrix: np.ndarray) -> np.ndarray:
    reduced = gf2_rref(np.asarray(matrix, dtype=int) % 2)
    return np.array([row for row in reduced if row.any()])


def verify(hx1, hz1, hx2, hz2, sigma) -> bool:
    """sigma is right only if it maps both row spaces onto the stored ones."""
    return np.array_equal(row_space(hx1[:, sigma]), row_space(hx2)) and np.array_equal(
        row_space(hz1[:, sigma]), row_space(hz2)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", default="", help="restrict to one catalogue key")
    args = parser.parse_args()

    specs = {spec.key: spec for spec in CATALOGUE}
    path = HERE / "sigma_precomputed.json"
    # Merge rather than overwrite: an interrupted run must not discard the
    # permutations an earlier one already settled.
    out = json.loads(path.read_text()) if path.exists() else {}

    targets = {k: v for k, v in TARGETS.items() if not args.only or k == args.only}
    for key, slug in targets.items():
        code = specs[key].build()
        n = len(code)
        hx1, hz1 = split_h_to_css(np.asarray(code.matrix, dtype=int) % 2, n)
        stored = yaml.safe_load((REPO / "data_yaml/codes" / f"{slug}.yaml").read_text())
        hx2, hz2 = split_h_to_css(np.array(stored["h"], dtype=int), n)

        sigma = find_sigma(np.array(hx1), np.array(hz1), np.array(hx2), np.array(hz2))
        ok = sigma is not None and verify(
            np.array(hx1), np.array(hz1), np.array(hx2), np.array(hz2), sigma
        )
        print(f"  {key:22s} -> {slug:28s} {'verified' if ok else 'NOT FOUND'}", flush=True)
        if ok:
            out[key] = {"slug": slug, "sigma": sigma}
            path.write_text(json.dumps(out, indent=2) + "\n")

    path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\n{len(out)}/{len(TARGETS)} permutations in sigma_precomputed.json")
    return 0 if len(out) == len(TARGETS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
