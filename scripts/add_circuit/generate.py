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
import yaml

from .compute import compute_code_data
from .compute_circuit import compute_circuit_data


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
    parser.add_argument("--dry-run", action="store_true", help="Print what would be written without writing")

    args = parser.parse_args()
    data_dir = Path(args.data_dir)

    # Parse matrices
    Hx = _load_matrix(args.hx)
    Hz = _load_matrix(args.hz)

    # Compute code data (with YAML dedup)
    code_result = compute_code_data(
        Hx, Hz, d=args.d, code_name=args.code_name,
        zoo_url=args.zoo_url, data_dir=str(data_dir) if data_dir.exists() else None,
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

    # Collect files to write
    code_slug = code["slug"]
    files_to_write = []

    if code.get("status") == "new":
        files_to_write.append((
            data_dir / "codes" / f"{code_slug}.yaml",
            _dump_yaml(_build_code_yaml(code)),
        ))

    for circ in circuits:
        circ_slug = circ["slug"]
        stem = f"{code_slug}--{circ_slug}"
        circuits_dir = data_dir / "circuits"

        files_to_write.append((
            circuits_dir / f"{stem}.yaml",
            _dump_yaml(_build_circuit_yaml(circ)),
        ))

        for body in circ.get("bodies", []):
            if body.get("body"):
                files_to_write.append((circuits_dir / f"{stem}.{body['format']}", body["body"]))

    # Write or dry-run
    if args.dry_run:
        for fpath, _ in files_to_write:
            print(f"  Would write: {fpath}")
    else:
        for fpath, content in files_to_write:
            _write_file(fpath, content)

    # Summary
    print(f"Code: {code['name']} [{code['status']}]")
    print(f"Circuits: {len(circuits)}")
    for c in circuits:
        func = c["detected_functionality"] or "unknown"
        print(f"  - {c['name']} ({func}) [{c['validation']}]")
    if not args.dry_run:
        print(f"\nRun 'npm run db:create && npm run dev' to rebuild the database.")


def _write_file(fpath, content):
    """Write a file, creating parent directories as needed."""
    fpath.parent.mkdir(parents=True, exist_ok=True)
    action = "Overwriting" if fpath.exists() else "Creating"
    print(f"  {action}: {fpath}")
    fpath.write_text(content)


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


# --- YAML formatting helpers ---

def _build_code_yaml(code):
    """Build clean code YAML dict from computed code data."""
    data = {"name": code["name"]}

    for field in ("n", "k", "d"):
        if code.get(field) is not None:
            data[field] = code[field]

    if code.get("zoo_url"):
        data["zoo_url"] = code["zoo_url"]

    if code.get("canonical_hash"):
        data["canonical_hash"] = code["canonical_hash"]

    for field in ("hx", "hz", "logical_x", "logical_z"):
        if code.get(field) is not None:
            data[field] = code[field]

    tags = [t["name"] for t in code.get("tags", [])]
    if tags:
        data["tags"] = tags

    return data


def _build_circuit_yaml(circ):
    """Build clean circuit YAML dict from computed circuit data."""
    data = {"name": circ["name"]}

    if circ.get("tool"):
        data["tool"] = circ["tool"]

    if circ.get("description"):
        data["description"] = circ["description"]

    if circ.get("source"):
        data["source"] = circ["source"]

    for field in ("gate_count", "depth", "qubit_count"):
        if circ.get(field) is not None:
            data[field] = circ[field]

    if circ.get("crumble_url"):
        data["crumble_url"] = circ["crumble_url"]

    if circ.get("quirk_url"):
        data["quirk_url"] = circ["quirk_url"]

    tags = [t["name"] for t in circ.get("tags", [])]
    if tags:
        data["tags"] = tags

    return data


class _FlowList(list):
    """List that serializes as YAML flow style (inline)."""
    pass


def _flow_list_representer(dumper, data):
    return dumper.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=True)


yaml.add_representer(_FlowList, _flow_list_representer)


def _dump_yaml(data):
    """Dump dict to YAML string with matrices as flow-style lists."""
    data = _convert_matrices(data)
    return yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)


def _convert_matrices(data):
    """Convert matrix fields (lists of lists) to flow-style representation."""
    result = {}
    for key, value in data.items():
        if key in ("hx", "hz", "logical_x", "logical_z", "tags") and isinstance(value, list):
            if key == "tags":
                result[key] = _FlowList(value)
            else:
                result[key] = [_FlowList(row) for row in value]
        else:
            result[key] = value
    return result


if __name__ == "__main__":
    main()
