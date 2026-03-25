"""
CLI: Export a reviewed YAML payload to data_yaml/ source files.

Replaces insert.py — instead of writing to SQLite, writes YAML + body files
that are consumed by create_database.mjs.

Usage:
    python -m scripts.add_circuit.export payload.yaml
    python -m scripts.add_circuit.export --dry-run payload.yaml
"""

import argparse
from pathlib import Path

import yaml


DATA_YAML = Path("data_yaml")


def main():
    parser = argparse.ArgumentParser(description="Export payload to data_yaml/ files")
    parser.add_argument("yaml_file", help="Path to reviewed payload YAML")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be written without writing")
    parser.add_argument("--data-dir", default=str(DATA_YAML), help="Path to data_yaml directory")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)

    with open(args.yaml_file) as f:
        payload = yaml.safe_load(f)

    code = payload["code"]
    code_slug = code["slug"]
    files_to_write = []

    # --- Code YAML (only if new) ---
    if code.get("status") == "new":
        code_path = data_dir / "codes" / f"{code_slug}.yaml"
        code_data = _build_code_yaml(code)
        code_yaml = _dump_yaml(code_data)
        files_to_write.append((code_path, code_yaml))

    # --- Circuits ---
    for circ in payload.get("circuits", []):
        circ_slug = circ["slug"]
        stem = f"{code_slug}--{circ_slug}"
        circuits_dir = data_dir / "circuits"

        # Circuit YAML
        circ_path = circuits_dir / f"{stem}.yaml"
        circ_data = _build_circuit_yaml(circ)
        circ_yaml = _dump_yaml(circ_data)
        files_to_write.append((circ_path, circ_yaml))

        # Body files
        for body in circ.get("bodies", []):
            if not body.get("body"):
                continue
            fmt = body["format"]
            body_path = circuits_dir / f"{stem}.{fmt}"
            files_to_write.append((body_path, body["body"]))

    # --- Write or dry-run ---
    if args.dry_run:
        print("Dry run — files that would be written:\n")
        for fpath, content in files_to_write:
            lines = content.count("\n")
            print(f"  {fpath} ({lines} lines)")
        print(f"\nTotal: {len(files_to_write)} file(s)")
    else:
        for fpath, content in files_to_write:
            fpath.parent.mkdir(parents=True, exist_ok=True)
            if fpath.exists():
                print(f"  Overwriting: {fpath}")
            else:
                print(f"  Creating: {fpath}")
            fpath.write_text(content)
        print(f"\nExported {len(files_to_write)} file(s) to {data_dir}/")
        print("Run 'npm run db:create' to rebuild the database.")


def _build_code_yaml(code):
    """Build clean code YAML dict from payload code section."""
    data = {"name": code["name"]}

    for field in ("n", "k", "d"):
        if code.get(field) is not None:
            data[field] = code[field]

    if code.get("zoo_url"):
        data["zoo_url"] = code["zoo_url"]

    if code.get("canonical_hash"):
        data["canonical_hash"] = code["canonical_hash"]

    # Matrices as compact JSON-style lists
    for field in ("hx", "hz", "logical_x", "logical_z"):
        if code.get(field) is not None:
            data[field] = code[field]

    # Tags: flatten from [{name, status}] to [name]
    tags = [t["name"] for t in code.get("tags", [])]
    if tags:
        data["tags"] = tags

    return data


def _build_circuit_yaml(circ):
    """Build clean circuit YAML dict from payload circuit section."""
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

    # Tags: flatten from [{name, status}] to [name]
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
    # Convert matrix fields to flow-style for readability
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
                # Matrix: list of lists → each row is flow-style
                result[key] = [_FlowList(row) for row in value]
        else:
            result[key] = value
    return result


if __name__ == "__main__":
    main()
