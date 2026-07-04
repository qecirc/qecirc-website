"""Shared helpers for assigning permanent identifiers."""

import re
from pathlib import Path

_QEC_ID_RE = re.compile(r"^qec_id:\s*(\d+)\s*$", re.MULTILINE)


def next_qec_id(data_dir: Path) -> int:
    """Return the next available qec_id by scanning existing circuit YAMLs.

    Scans data_yaml/circuits/*.yaml to find max(qec_id) and returns max + 1.
    Returns 1 if no circuits exist. This avoids reusing IDs only while the
    previously assigned circuit YAML files remain present on disk; deleting
    the highest-id YAML would cause the next allocation to reuse that id.

    The ``qec_id`` is matched with a regex rather than parsing each YAML — a
    hot path during bulk imports (called once per added circuit over a growing
    set of files), where full parsing is orders of magnitude slower.
    """
    circuits_dir = Path(data_dir) / "circuits"
    max_id = 0
    if circuits_dir.exists():
        for f in circuits_dir.glob("*.yaml"):
            m = _QEC_ID_RE.search(f.read_text(encoding="utf-8"))
            if m:
                max_id = max(max_id, int(m.group(1)))
    return max_id + 1
