#!/usr/bin/env python
"""Fetch best-known distances for the codetables codes from codetables.de.

The autqec dataset's ``codetables/`` sweep commits parity checks and gate
circuits for the best-known [[n,k]] stabilizer codes (Grassl's tables) but no
distance values. This script looks up, for every (n,k) pair that has at least
one nontrivial precomputed gate circuit, the current best-known minimum
distance (lower bound = best construction, upper bound) from

    https://codetables.de/QECC/QECC.php?q=4&n=<n>&k=<k>

and caches the result as ``codetables_distances.json`` next to this script.
Existing cache entries are not re-fetched, so interrupting and re-running is
cheap. Requests are spaced politely.

Caveat: codetables.de is updated over time, so today's lower bound may exceed
the distance of the code snapshotted in the autqec repo. The cached JSON keeps
both bounds; an importer should verify the snapshot matches (e.g. via the
stabilizer matrix on the same page) or state d as "best known at fetch time".

Usage:
  uv run python data-imports/autqec/fetch_codetables_distances.py [--dataset PATH]
"""

from __future__ import annotations

import argparse
import json
import pickle
import re
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from rebuild_all import _default_dataset  # noqa: E402

CACHE = HERE / "codetables_distances.json"
URL = "https://codetables.de/QECC/QECC.php?q=4&n={n}&k={k}"
_BOUND = re.compile(r"(lower|upper) bound:</TD><TD>(\d+)</TD>", re.IGNORECASE)
_GATES = re.compile(r"gates_n(\d+)k(\d+)\.pkl")


def pairs_with_gates(dataset: Path) -> list[tuple[int, int]]:
    """(n,k) pairs having >=1 nontrivial precomputed gate circuit, any family."""
    ct = dataset / "codetables"
    pairs = set()
    for gate_dir in (ct / "logical_gates", ct / "ZX_dualities" / "logical_gates"):
        for p in gate_dir.glob("gates_n*.pkl"):
            n, k = map(int, _GATES.match(p.name).groups())
            if k == 0 or k == n:
                continue
            with open(p, "rb") as f:
                d = pickle.load(f)
            if any(d["logical"]):
                pairs.add((n, k))
    return sorted(pairs)


def fetch_bounds(n: int, k: int) -> dict:
    with urllib.request.urlopen(URL.format(n=n, k=k), timeout=30) as resp:
        html = resp.read().decode(errors="replace").replace("\n", " ")
    bounds = {m.group(1).lower(): int(m.group(2)) for m in _BOUND.finditer(html)}
    if "lower" not in bounds or "upper" not in bounds:
        raise ValueError(f"could not parse bounds for [[{n},{k}]]")
    return {"d_lower": bounds["lower"], "d_upper": bounds["upper"]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default=str(_default_dataset()))
    ap.add_argument("--delay", type=float, default=0.7, help="seconds between requests")
    args = ap.parse_args()

    cache: dict[str, dict] = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    pairs = pairs_with_gates(Path(args.dataset))
    todo = [(n, k) for (n, k) in pairs if f"{n},{k}" not in cache]
    print(f"{len(pairs)} (n,k) pairs with gates; {len(todo)} to fetch, {len(cache)} cached")

    for i, (n, k) in enumerate(todo):
        try:
            cache[f"{n},{k}"] = fetch_bounds(n, k)
            print(f"  [{i + 1}/{len(todo)}] [[{n},{k}]] -> d={cache[f'{n},{k}']}", flush=True)
        except Exception as e:  # keep going; rerun picks up the gaps
            print(f"  [{i + 1}/{len(todo)}] [[{n},{k}]] FAILED: {e}", flush=True)
        CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n")
        time.sleep(args.delay)

    done = sum(1 for (n, k) in pairs if f"{n},{k}" in cache)
    print(f"cache now covers {done}/{len(pairs)} pairs -> {CACHE.name}")


if __name__ == "__main__":
    main()
