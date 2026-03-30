"""
CLI: Generate data_yaml/ files from Hx/Hz matrices + STIM circuits.

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
from pathlib import Path

import numpy as np

from .compute import compute_code_data
from .compute_circuit import compute_circuit_data
from .yaml_helpers import build_circuit_yaml, build_code_yaml, dump_yaml, write_file


def main():
    parser = argparse.ArgumentParser(description="Generate data_yaml/ files from Hx/Hz + STIM")
    # Code-level args (shared across circuits)
    parser.add_argument("--hx", required=True, help="Hx matrix as JSON string or path to file")
    parser.add_argument("--hz", required=True, help="Hz matrix as JSON string or path to file")
    parser.add_argument("--code-name", default="", help="Code name")
    parser.add_argument("--zoo-url", default="", help="QEC Zoo URL")
    parser.add_argument("--d", type=int, default=None, help="Code distance (computed if omitted)")
    parser.add_argument("--data-dir", default="data_yaml", help="Path to data_yaml directory")
    # Circuit-level args (multiple allowed, positionally matched)
    parser.add_argument("--stim", nargs="+", required=True, help="STIM circuit file(s)")
    parser.add_argument("--circuit-name", nargs="+", default=[], help="Circuit name(s)")
    parser.add_argument("--source", nargs="+", default=[], help="Source(s) (DOI/URL)")
    parser.add_argument("--tool", nargs="+", default=[], help="Tool slug(s)")
    parser.add_argument("--description", nargs="+", default=[], help="Circuit description(s)")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print what would be written without writing"
    )

    args = parser.parse_args()
    data_dir = Path(args.data_dir)

    # Parse matrices
    Hx = _load_matrix(args.hx)
    Hz = _load_matrix(args.hz)

    # Compute code data once (shared across all circuits)
    code_result = compute_code_data(
        Hx,
        Hz,
        d=args.d,
        code_name=args.code_name,
        zoo_url=args.zoo_url,
        data_dir=str(data_dir) if data_dir.exists() else None,
    )

    code = code_result["code"]
    perm = code_result["qubit_permutation"]
    code_slug = code["slug"]
    code_params = {
        "n": code["n"],
        "k": code["k"],
        "d": code["d"],
        "is_css": code["is_css"],
    }

    # Collect all files to write
    files_to_write = []

    if code.get("status") == "new":
        files_to_write.append(
            (
                data_dir / "codes" / f"{code_slug}.yaml",
                dump_yaml(build_code_yaml(code)),
            )
        )

    # Compute circuit data for each STIM file
    circuits = []
    for i, stim_path in enumerate(args.stim):
        circuit_text = Path(stim_path).read_text()
        circ_data = compute_circuit_data(
            circuit_text=circuit_text,
            Hx=Hx,
            Hz=Hz,
            code_params=code_params,
            qubit_permutation=perm,
            circuit_name=_get_nth(args.circuit_name, i, ""),
            source=_get_nth(args.source, i, ""),
            tool=_get_nth(args.tool, i, ""),
            description=_get_nth(args.description, i, ""),
        )
        circuits.append(circ_data)

        stem = f"{code_slug}--{circ_data['slug']}"
        circuits_dir = data_dir / "circuits"

        files_to_write.append(
            (
                circuits_dir / f"{stem}.yaml",
                dump_yaml(build_circuit_yaml(circ_data)),
            )
        )

        for body in circ_data.get("bodies", []):
            if body.get("body"):
                files_to_write.append((circuits_dir / f"{stem}.{body['format']}", body["body"]))

    # Write or dry-run
    if args.dry_run:
        for fpath, _ in files_to_write:
            print(f"  Would write: {fpath}")
    else:
        for fpath, content in files_to_write:
            write_file(fpath, content)

    # Summary
    print(f"Code: {code['name']} [{code['status']}]")
    print(f"Circuits: {len(circuits)}")
    for c in circuits:
        func = c["detected_functionality"] or "unknown"
        print(f"  - {c['name']} ({func}) [{c['validation']}]")
    if not args.dry_run:
        print("\nRun 'npm run db:create && npm run dev' to rebuild the database.")


def _load_matrix(arg):
    """Load matrix from JSON string or file path."""
    if Path(arg).exists():
        with open(arg) as f:
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
    main()
