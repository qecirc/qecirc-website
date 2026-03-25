"""
CLI: Generate YAML payload from Hx/Hz + STIM circuits.

Usage:
    python -m scripts.add_circuit.generate \
      --hx '[[1,1,0,...]]' --hz '[[1,1,0,...]]' \
      --stim circuit1.stim circuit2.stim \
      --code-name "Steane Code" \
      --circuit-name "Standard Encoding" "Syndrome Extraction" \
      --source "doi:..." "doi:..." \
      --tool "mqt-qecc" "mqt-qecc" \
      --zoo-url "https://errorcorrectionzoo.org/c/steane" \
      --d 3 \
      -o output.yaml
"""

import argparse
import json
from pathlib import Path

import numpy as np
import yaml

from .compute import compute_code_data
from .compute_circuit import compute_circuit_data


def main():
    parser = argparse.ArgumentParser(description="Generate ingestion YAML")
    # Code-level args (shared across circuits)
    parser.add_argument("--hx", required=True, help="Hx matrix as JSON string or path to file")
    parser.add_argument("--hz", required=True, help="Hz matrix as JSON string or path to file")
    parser.add_argument("--code-name", default="", help="Code name")
    parser.add_argument("--zoo-url", default="", help="QEC Zoo URL")
    parser.add_argument("--d", type=int, default=None, help="Code distance (computed if omitted)")
    parser.add_argument("--data-dir", default="data_yaml", help="Path to data_yaml directory for dedup")
    # Circuit-level args (multiple allowed, positionally matched)
    parser.add_argument("--stim", nargs="+", required=True, help="STIM circuit file(s)")
    parser.add_argument("--circuit-name", nargs="+", default=[], help="Circuit name(s)")
    parser.add_argument("--source", nargs="+", default=[], help="Source(s) (DOI/URL)")
    parser.add_argument("--tool", nargs="+", default=[], help="Tool slug(s)")
    parser.add_argument("--description", nargs="+", default=[], help="Circuit description(s)")
    parser.add_argument("-o", "--output", default="payload.yaml", help="Output YAML path")

    args = parser.parse_args()

    # Parse matrices
    Hx = _load_matrix(args.hx)
    Hz = _load_matrix(args.hz)

    # Compute code data (with YAML dedup)
    data_dir = args.data_dir if Path(args.data_dir).exists() else None
    code_result = compute_code_data(
        Hx, Hz, d=args.d, code_name=args.code_name,
        zoo_url=args.zoo_url, data_dir=data_dir,
    )

    # Compute circuit data for each STIM file
    circuits = []
    perm = code_result["qubit_permutation"]
    code = code_result["code"]
    code_params = {
        "n": code["n"],
        "k": code["k"],
        "d": code["d"],
        "is_css": code["is_css"],
    }

    for i, stim_path in enumerate(args.stim):
        circuit_text = Path(stim_path).read_text()
        circ_data = compute_circuit_data(
            circuit_text=circuit_text,
            Hx=Hx, Hz=Hz,
            code_params=code_params,
            qubit_permutation=perm,
            circuit_name=_get_nth(args.circuit_name, i, ""),
            source=_get_nth(args.source, i, ""),
            tool=_get_nth(args.tool, i, ""),
            description=_get_nth(args.description, i, ""),
        )
        circuits.append(circ_data)

    # Assemble YAML
    payload = {
        "code": code,
        "qubit_permutation": perm,
        "circuits": circuits,
    }

    with open(args.output, "w") as f:
        yaml.dump(payload, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"Written to {args.output}")
    print(f"Code: {code['name']} [{code['status']}]")
    print(f"Circuits: {len(circuits)}")
    for c in circuits:
        func = c["detected_functionality"] or "unknown"
        print(f"  - {c['name']} ({func}) [{c['validation']}]")


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
