"""YAML formatting helpers for code and circuit data."""

from pathlib import Path

import yaml


def build_code_yaml(code):
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


def build_circuit_yaml(circ):
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


def dump_yaml(data):
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


def write_file(fpath, content, quiet=False):
    """Write a file, creating parent directories as needed."""
    fpath = Path(fpath)
    fpath.parent.mkdir(parents=True, exist_ok=True)
    if not quiet:
        action = "Overwriting" if fpath.exists() else "Creating"
        print(f"  {action}: {fpath}")
    fpath.write_text(content)
