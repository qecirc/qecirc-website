#!/usr/bin/env python
"""Compute the qubit permutations this import needs, into sigma_precomputed.json.

Four of the dataset's codes match a stored code on every invariant but defeat
`find_code_permutation`'s search budget: it derives its column invariants from
puncture ranks and (when the rank is small enough) low-weight codeword
histograms, and for the d=7 and d=9 rotated surface codes the rank is past that
cutoff, leaving only the weak invariant and a very symmetric code.

The matcher itself lives in `scripts.add_circuit.find_sigma`, which reads a
topological code's low-weight codewords as a canonical hypergraph and settles it
by individualization-refinement. This script only drives it: which dataset code
should land on which stored slug, and where the answers are kept.

Nothing is trusted on its own. The matcher confirms every candidate by row-space
equality against the stored code, and `add_circuit` repeats that check on every
import, so a wrong or stale sigma fails loudly.

Run from the repository root:

    uv run python data-imports/asyndrome/find_sigma.py [--dataset PATH]
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
DATASET = REPO.parent / "asyndrome"
sys.path.insert(0, str(REPO))

from scripts.add_circuit.code_identify import split_h_to_css  # noqa: E402
from scripts.add_circuit.find_sigma import find_sigma  # noqa: E402

# dataset code -> stored code slug it should be filed under.
TARGETS = {
    "surface-5x5": "rotated-surface-code-d-5",
    "surface-7x7": "rotated-surface-code-d-7",
    "surface-9x9": "rotated-surface-code-d-9",
    "color-oct-9": "49-1-9",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute the import's qubit permutations")
    parser.add_argument("--dataset", default=str(DATASET), help="clone of acasta-yhliu/asyndrome")
    parser.add_argument("--only", default="", help="restrict to one target code")
    args = parser.parse_args()
    dataset = Path(args.dataset)

    # Merge rather than overwrite: these take minutes to find and seconds to
    # verify, so a partial run must never discard an earlier one's work.
    path = HERE / "sigma_precomputed.json"
    out = json.loads(path.read_text()) if path.exists() else {}
    targets = {k: v for k, v in TARGETS.items() if not args.only or k == args.only}
    for key, slug in targets.items():
        doc = json.loads((dataset / "qecc" / f"{key}.json").read_text())
        n = doc["n"]
        stabilizers = doc["x_stabilizers"] + doc["z_stabilizers"]
        Hx1 = np.array([[1 if c == "X" else 0 for c in s] for s in stabilizers if "X" in s])
        Hz1 = np.array([[1 if c == "Z" else 0 for c in s] for s in stabilizers if "Z" in s])

        stored = yaml.safe_load((REPO / "data_yaml/codes" / f"{slug}.yaml").read_text())
        Hx2, Hz2 = split_h_to_css(np.array(stored["h"], dtype=int), n)

        sigma = find_sigma(Hx1, Hz1, Hx2, Hz2)
        print(f"  {key:14s} -> {slug:26s} {'found' if sigma else 'NOT FOUND'}", flush=True)
        if sigma:
            # Written as we go: the colour code can search for minutes, and an
            # interrupted run must not cost the ones already settled.
            out[key] = {"slug": slug, "sigma": sigma}
            path.write_text(json.dumps(out, indent=2) + "\n")

    path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\n{len(out)}/{len(TARGETS)} permutations in sigma_precomputed.json")
    return 0 if len(out) == len(TARGETS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
