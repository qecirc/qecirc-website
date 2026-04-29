"""
Backfill ``h`` and ``logical`` (symplectic) fields into existing YAML files.

Existing data in this repo is all CSS, so this script only knows how to
upgrade YAML files that already have ``hx``, ``hz``, ``logical_x``,
``logical_z``: it builds the symplectic forms via ``build_symplectic_h`` and
``build_symplectic_logical`` and writes them back to the YAML in place.

Idempotent: skips files that already have ``h`` or ``logical``.

Usage:
    uv run python scripts/regenerate_h_logical.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import yaml

# Allow running as a script: ensure repo root is importable.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.add_circuit.code_identify import (  # noqa: E402
    build_symplectic_h,
    build_symplectic_logical,
)
from scripts.add_circuit.yaml_helpers import dump_yaml  # noqa: E402


def _upgrade(data: dict, *, n: int | None = None, k: int | None = None) -> bool:
    """Add h/logical to ``data`` in place. Returns True iff modified."""
    if "h" in data and "logical" in data:
        return False
    if data.get("hx") is None or data.get("hz") is None:
        return False  # not a CSS-shaped record we can upgrade

    Hx = np.array(data["hx"], dtype=int)
    Hz = np.array(data["hz"], dtype=int)
    n_eff = n if n is not None else int(Hx.shape[1])

    if "h" not in data:
        h = build_symplectic_h(Hx, Hz)
        data["h"] = h.tolist()

    if "logical" not in data:
        if data.get("logical_x") is None or data.get("logical_z") is None:
            return True  # h added but logical not derivable
        Lx = np.array(data["logical_x"], dtype=int)
        Lz = np.array(data["logical_z"], dtype=int)
        k_eff = k if k is not None else int(Lx.shape[0])
        logical = build_symplectic_logical(Lx, Lz, n=n_eff, k=k_eff)
        data["logical"] = logical.tolist()
    return True


def _ordered_yaml(data: dict, key_order: list[str]) -> dict:
    """Reorder a dict so listed keys come first (in order), preserving the rest."""
    ordered = {}
    for key in key_order:
        if key in data:
            ordered[key] = data[key]
    for key, value in data.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def upgrade_code_yaml(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        return False
    if not _upgrade(data, n=data.get("n"), k=data.get("k")):
        return False
    ordered = _ordered_yaml(
        data,
        [
            "name",
            "n",
            "k",
            "d",
            "zoo_url",
            "canonical_hash",
            "hx",
            "hz",
            "logical_x",
            "logical_z",
            "h",
            "logical",
            "tags",
        ],
    )
    path.write_text(dump_yaml(ordered), encoding="utf-8")
    return True


def upgrade_original_yaml(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        return False
    if not _upgrade(data):
        return False
    ordered = _ordered_yaml(
        data,
        ["hx", "hz", "logical_x", "logical_z", "h", "logical"],
    )
    path.write_text(dump_yaml(ordered), encoding="utf-8")
    return True


def main() -> int:
    data_root = ROOT / "data_yaml"
    codes_dir = data_root / "codes"
    originals_dir = data_root / "circuits" / "originals"

    upgraded = 0
    skipped = 0

    for path in sorted(codes_dir.glob("*.yaml")):
        if upgrade_code_yaml(path):
            print(f"  upgraded code: {path.relative_to(ROOT)}")
            upgraded += 1
        else:
            skipped += 1

    for path in sorted(originals_dir.glob("*.original.yaml")):
        if upgrade_original_yaml(path):
            print(f"  upgraded original: {path.relative_to(ROOT)}")
            upgraded += 1
        else:
            skipped += 1

    print(f"\n{upgraded} file(s) upgraded, {skipped} unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
