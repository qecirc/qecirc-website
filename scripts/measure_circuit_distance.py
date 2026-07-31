#!/usr/bin/env python
"""Measure the circuit-level distance of stored syndrome-extraction rounds.

Writes it back as a `circuit-distance:<N>` tag, so the listing pages can filter
on it next to `distance:<N>` — the code's distance, which is a different number
and usually a larger one.

The search is stim's and its cost grows fast with n and d, so every circuit gets
a wall-clock budget and anything that overruns is simply left untagged. An
absent tag means "not measured", never "no faults found": see
`scripts/add_circuit/circuit_distance.py` for what the number is and which noise
model produces it.

    uv run python scripts/measure_circuit_distance.py                  # report
    uv run python scripts/measure_circuit_distance.py --write
    uv run python scripts/measure_circuit_distance.py --only 36-8-4 --timeout 300
"""

from __future__ import annotations

import argparse
import multiprocessing as mp
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.add_circuit.circuit_distance import round_circuit_distance  # noqa: E402
from scripts.add_circuit.matrix_format import decode as decode_matrix  # noqa: E402
from scripts.add_circuit.yaml_helpers import dump_yaml, load_yaml, write_file  # noqa: E402

TAG = "circuit-distance"
SE_TAG = "syndrome-extraction"


def _worker(body, h, logical, n, d, queue):
    try:
        queue.put(round_circuit_distance(body, h, logical, n, d))
    except Exception as exc:  # noqa: BLE001 - reported, not raised, per circuit
        queue.put(f"error: {type(exc).__name__}: {exc}")


def measure_with_budget(body, h, logical, n, d, timeout):
    """The distance, or None if it did not finish inside `timeout` seconds.

    In its own process because stim's search is a single C++ call that cannot be
    interrupted — the only way to stop it is to kill what is running it.
    """
    queue: mp.Queue = mp.Queue()
    proc = mp.Process(target=_worker, args=(body, h, logical, n, d, queue))
    started = time.time()
    proc.start()
    proc.join(timeout)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        return None, time.time() - started, "timeout"
    if queue.empty():
        return None, time.time() - started, "died"
    got = queue.get()
    if isinstance(got, str):
        return None, time.time() - started, got
    return got, time.time() - started, "measured" if got is not None else "no result"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data_yaml")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--only", default="", help="restrict to circuits whose stem contains this")
    parser.add_argument("--timeout", type=int, default=120, help="seconds per circuit")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    codes = {
        p.stem: load_yaml(p.read_text(encoding="utf-8"))
        for p in (data_dir / "codes").glob("*.yaml")
    }

    jobs = []
    for path in sorted((data_dir / "circuits").glob("*.yaml")):
        if args.only and args.only not in path.stem:
            continue
        doc = load_yaml(path.read_text(encoding="utf-8"))
        if SE_TAG not in (doc.get("tags") or []):
            continue
        code = codes.get(path.stem.split("--")[0])
        body = path.with_suffix(".stim")
        if code is None or not body.exists() or code.get("h") is None:
            continue
        jobs.append((code["n"], path, doc, code, body))

    jobs.sort(key=lambda j: j[0])
    counts = {"measured": 0, "timeout": 0, "unchanged": 0, "written": 0}
    print(f"{len(jobs)} syndrome-extraction circuits, {args.timeout}s budget each\n")
    print(f"{'n':>5} {'d':>3} {'cd':>4} {'secs':>7}  circuit")

    for n, path, doc, code, body in jobs:
        d = code["d"]
        got, secs, status = measure_with_budget(
            body.read_text(encoding="utf-8"),
            decode_matrix(code["h"]),
            decode_matrix(code["logical"]) if code.get("logical") is not None else None,
            n,
            d,
            args.timeout,
        )
        print(
            f"{n:>5} {d:>3} {str(got):>4} {secs:>7.1f}  {path.stem}"
            + ("" if status in ("measured", "no result") else f"  [{status}]"),
            flush=True,
        )
        if got is None:
            counts["timeout"] += 1
            continue
        counts["measured"] += 1

        tags = [t for t in (doc.get("tags") or []) if not t.startswith(f"{TAG}:")]
        tags.append(f"{TAG}:{got}")
        if tags == doc.get("tags"):
            counts["unchanged"] += 1
            continue
        doc["tags"] = tags
        counts["written"] += 1
        if args.write:
            write_file(path, dump_yaml(doc), quiet=True)

    print()
    for key in ("measured", "timeout", "written", "unchanged"):
        print(f"  {counts[key]:5d}  {key}")
    if not args.write:
        print("\nDry run — pass --write to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
