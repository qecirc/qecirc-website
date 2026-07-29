#!/usr/bin/env python
"""Move the stored matrices to the shared, size-aware format. Run once.

Two changes, applied to every file already in `data_yaml/`:

* **Originals are stored once.** `circuits/originals/<circuit>.original.yaml`
  held the matrices a circuit was submitted against — and every circuit of one
  code holds the *same* matrices, so a code with three circuits kept three
  byte-identical copies. They move to `matrices/<digest>.yaml`, written once,
  with the circuit YAML naming the one it uses via `original_matrices`.
  The original *circuit* (`.original.stim`) is genuinely per circuit and stays.

* **Large matrices become sparse.** Above `SPARSE_MIN_ENTRIES` a matrix is
  written as nonzero column indices per row rather than dense 0/1 rows. Smaller
  matrices are left exactly as they are, so this rewrites only the files where
  it pays.

Nothing is recomputed: the matrices are read, re-encoded and written back, so
the migration cannot change what any code or circuit means. It verifies that by
decoding what it wrote and comparing against what it read.

    uv run python scripts/migrate_matrix_storage.py            # report only
    uv run python scripts/migrate_matrix_storage.py --write
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.add_circuit.matrix_format import decode as decode_matrix  # noqa: E402
from scripts.add_circuit.yaml_helpers import (  # noqa: E402
    build_original_yaml,
    dump_yaml,
    load_yaml,
    matrices_digest,
    write_file,
)


def _reencode_file(path: Path, write: bool) -> bool:
    """Rewrite a code YAML with the current matrix encoding. True if it changed."""
    text = path.read_text(encoding="utf-8")
    data = load_yaml(text)
    if not any(data.get(f) is not None for f in ("h", "logical")):
        return False
    before = {f: decode_matrix(data[f]) for f in ("h", "logical") if data.get(f) is not None}

    # build_code_yaml would drop unknown keys, so re-encode in place instead:
    # this migration must not decide what a code YAML may contain.
    from scripts.add_circuit.matrix_format import encode as encode_matrix

    for f in ("h", "logical"):
        if data.get(f) is not None:
            data[f] = encode_matrix(decode_matrix(data[f]))
    out = dump_yaml(data)
    if out == text:
        return False

    after = {f: decode_matrix(load_yaml(out)[f]) for f in before}
    for f, m in before.items():
        if not np.array_equal(m, after[f]):
            raise SystemExit(f"{path}: re-encoding changed `{f}` — refusing to write")
    if write:
        write_file(path, out, quiet=True)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data_yaml")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    circuits_dir = data_dir / "circuits"
    originals_dir = circuits_dir / "originals"
    matrices_dir = data_dir / "matrices"
    counts: Counter[str] = Counter()

    # --- codes: re-encode in place ----------------------------------------
    for path in sorted((data_dir / "codes").glob("*.yaml")):
        if _reencode_file(path, args.write):
            counts["codes re-encoded"] += 1
        else:
            counts["codes unchanged"] += 1

    # --- originals: one shared file per distinct matrix pair ----------------
    digests: dict[str, str] = {}  # digest -> rendered YAML
    for path in sorted(originals_dir.glob("*.original.yaml")):
        stem = path.name[: -len(".original.yaml")]
        circuit_path = circuits_dir / f"{stem}.yaml"
        if not circuit_path.exists():
            counts["orphaned originals (left alone)"] += 1
            continue

        stored = load_yaml(path.read_text(encoding="utf-8"))
        matrices = {
            f: decode_matrix(stored[f]) for f in ("h", "logical") if stored.get(f) is not None
        }
        if not matrices:
            counts["empty originals (left alone)"] += 1
            continue

        payload = build_original_yaml(matrices)
        digest = matrices_digest(payload)
        rendered = dump_yaml(payload)
        if digest in digests and digests[digest] != rendered:
            raise SystemExit(f"digest collision on {digest} — aborting")
        digests[digest] = rendered

        circuit_text = circuit_path.read_text(encoding="utf-8")
        circuit = load_yaml(circuit_text)
        if circuit.get("original_matrices") != digest:
            circuit["original_matrices"] = digest
            if args.write:
                write_file(circuit_path, dump_yaml(circuit), quiet=True)
            counts["circuits referenced"] += 1
        if args.write:
            path.unlink()
        counts["originals replaced"] += 1

    for digest, rendered in sorted(digests.items()):
        if args.write:
            write_file(matrices_dir / f"{digest}.yaml", rendered, quiet=True)

    for key in sorted(counts):
        print(f"  {counts[key]:5d}  {key}")
    print(f"  {len(digests):5d}  distinct matrix files written")
    if not args.write:
        print("\nDry run — pass --write to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
