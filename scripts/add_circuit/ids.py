"""Shared helpers for assigning permanent identifiers."""

from pathlib import Path

import yaml


def next_qec_id(data_dir: Path) -> int:
    """Return the next available qec_id by scanning existing circuit YAMLs.

    Scans data_yaml/circuits/*.yaml to find max(qec_id) and returns max + 1.
    Returns 1 if no circuits exist. This avoids reusing IDs only while the
    previously assigned circuit YAML files remain present on disk; deleting
    the highest-id YAML would cause the next allocation to reuse that id.
    """
    circuits_dir = Path(data_dir) / "circuits"
    max_id = 0
    if circuits_dir.exists():
        for f in circuits_dir.glob("*.yaml"):
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
            if data and isinstance(data.get("qec_id"), int):
                max_id = max(max_id, data["qec_id"])
    return max_id + 1
