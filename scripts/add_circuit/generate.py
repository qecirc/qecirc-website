"""
CLI: Generate data_yaml/ files from Hx/Hz matrices + STIM circuits.

A thin argument-parsing shell over :func:`scripts.add_circuit.add_circuit`,
which is the single write path. It used to assemble the files itself, and
drifted: it wrote a per-circuit `originals/<stem>.original.yaml` with no
`original_matrices` reference — the exact shape `create_database.mjs` throws on
— reallocated `qec_id` on every run against the documented "permanent, never
reused" rule, and with `--circuit-name` omitted wrote every input to the same
`<code>--.yaml`. Delegating removes all three by construction rather than by
keeping two writers in step.

Usage:
    python -m scripts.add_circuit.generate \
      --hx '[[1,1,0,...]]' --hz '[[1,1,0,...]]' \
      --stim circuit1.stim circuit2.stim \
      --code-name "Steane Code" \
      --circuit-name "Standard Encoding" "Syndrome Extraction" \
      --source "doi:..." "doi:..." \
      --tool "mqt-qecc" "mqt-qecc" \
      --zoo-url "https://errorcorrectionzoo.org/c/steane" \
      --d 3
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate data_yaml/ files from Hx/Hz + STIM")
    # Code-level args (shared across circuits)
    parser.add_argument("--hx", required=True, help="Hx matrix as JSON string or path to file")
    parser.add_argument("--hz", required=True, help="Hz matrix as JSON string or path to file")
    parser.add_argument("--code-name", default="", help="Code name")
    parser.add_argument("--zoo-url", default="", help="QEC Zoo URL")
    parser.add_argument("--d", type=int, required=True, help="Code distance")
    parser.add_argument("--data-dir", default="data_yaml", help="Path to data_yaml directory")
    # Circuit-level args (multiple allowed, positionally matched)
    parser.add_argument("--stim", nargs="+", required=True, help="STIM circuit file(s)")
    # Required: the circuit name is what distinguishes one circuit of a code
    # from the next, and every file is named `<code-slug>--<circuit-slug>`. With
    # it omitted, a second --stim silently overwrote the first at `<code>--`.
    parser.add_argument("--circuit-name", nargs="+", required=True, help="Circuit name(s)")
    parser.add_argument("--source", nargs="+", default=[], help="Source(s) (DOI/URL)")
    parser.add_argument("--tool", nargs="+", default=[], help="Tool slug(s)")
    parser.add_argument("--notes", nargs="+", default=[], help="Circuit notes")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace a circuit that already exists under the same slug, keeping its qec_id "
        "(the default is to refuse)",
    )
    parser.add_argument(
        "--assume-new",
        action="store_true",
        help="Add as a new code even when the dedup scan cannot confirm a match against a "
        "stored one",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print what would be written without writing"
    )

    args = parser.parse_args(argv)

    if len(args.circuit_name) < len(args.stim):
        parser.error(
            f"--circuit-name has {len(args.circuit_name)} value(s) for {len(args.stim)} "
            f"--stim file(s); every circuit needs its own name or they collide on one filename"
        )

    Hx = _load_matrix(args.hx)
    Hz = _load_matrix(args.hz)

    # Imported here rather than at module scope: `scripts.add_circuit` pulls in
    # stim and the whole ingestion stack, and `--help` should not pay for it.
    from . import UncertainDedupError, add_circuit

    results = []
    for i, stim_path in enumerate(args.stim):
        try:
            results.append(
                add_circuit(
                    circuit=Path(stim_path).read_text(encoding="utf-8"),
                    circuit_name=args.circuit_name[i],
                    d=args.d,
                    Hx=Hx,
                    Hz=Hz,
                    code_name=args.code_name,
                    zoo_url=args.zoo_url,
                    source=_get_nth(args.source, i, ""),
                    tool=_get_nth(args.tool, i, ""),
                    notes=_get_nth(args.notes, i, ""),
                    data_dir=args.data_dir,
                    dry_run=args.dry_run,
                    overwrite=args.overwrite,
                    assume_new=args.assume_new,
                )
            )
        # Both are the pipeline refusing on purpose, and both name the flag that
        # answers them. A traceback would bury that.
        except (FileExistsError, UncertainDedupError) as e:
            print(f"error: {stim_path}: {e}", file=sys.stderr)
            return 1

    for result in results:
        print(result.summary())
        print()
    return 0


def _load_matrix(arg):
    """Load matrix from JSON string or file path."""
    if Path(arg).exists():
        with open(arg, encoding="utf-8") as f:
            return np.array(json.load(f), dtype=int)
    try:
        return np.array(json.loads(arg), dtype=int)
    except json.JSONDecodeError:
        raise ValueError(
            f"'{arg}' is not a valid file path or JSON matrix. "
            f"Provide either a path to a JSON file or an inline JSON array (e.g. '[[1,0],[0,1]]')."
        )


def _get_nth(lst, i, default):
    return lst[i] if i < len(lst) else default


if __name__ == "__main__":
    sys.exit(main())
