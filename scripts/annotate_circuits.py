"""
Backfill `stim-annotated` bodies for state-prep and encoding circuits.

Writes `data_yaml/circuits/<stem>.stim-annotated` for every circuit that can
carry deterministic detectors, and records the matching Crumble link in the
circuit YAML as `crumble_url_annotated`.

Idempotent: re-running regenerates from source and rewrites only what changed.
Every emitted body is checked with stim's detector error model before it is
written — a circuit whose detectors are not provably deterministic is skipped
and reported, never written.

Usage:
    uv run python scripts/annotate_circuits.py
    uv run python scripts/annotate_circuits.py --dry-run
    uv run python scripts/annotate_circuits.py --only rotated-surface-code-d-3
"""

import argparse
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import numpy as np  # noqa: E402
import yaml  # noqa: E402

from scripts.add_circuit.annotate import build_annotated, validate_annotated  # noqa: E402
from scripts.add_circuit.compute_circuit import LARGE_CIRCUIT_MAX_QUBITS  # noqa: E402

ANNOTATED_FORMAT = "stim-annotated"
ANNOTATED_URL_KEY = "crumble_url_annotated"


@dataclass
class Result:
    stem: str
    status: str  # "written" | "unchanged" | "skipped" | "failed"
    detail: str = ""


def _code_slug(stem: str) -> str:
    """Code slug is everything before the first '--', matching create_database.mjs."""
    sep = stem.find("--")
    return stem[:sep] if sep > 0 else ""


def _kind_and_state(tags: list[str]) -> tuple[str, str]:
    kind = ""
    if "state-preparation" in tags:
        kind = "state-preparation"
    elif "encoding" in tags:
        kind = "encoding"
    state = next((t.split(":", 1)[1] for t in tags if t.startswith("logical-state:")), "")
    return kind, state


def annotate_all(data_dir: Path, only: str = "", dry_run: bool = False) -> list[Result]:
    codes_dir = data_dir / "codes"
    circuits_dir = data_dir / "circuits"
    originals_dir = circuits_dir / "originals"

    codes = {
        p.stem: yaml.safe_load(p.read_text(encoding="utf-8")) for p in codes_dir.glob("*.yaml")
    }
    results: list[Result] = []

    for path in sorted(circuits_dir.glob("*.yaml")):
        stem = path.stem
        if only and not stem.startswith(only):
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        tags = data.get("tags") or []
        kind, state = _kind_and_state(tags)
        if not kind:
            continue  # gadgets, syndrome extraction: nothing deterministic to annotate

        slug = _code_slug(stem)
        code = codes.get(slug)
        if code is None:
            results.append(Result(stem, "failed", f"code {slug!r} not found"))
            continue

        body_path = circuits_dir / f"{stem}.stim"
        if not body_path.exists():
            results.append(Result(stem, "failed", "no .stim body"))
            continue

        n, k = code["n"], code["k"]
        stored_h = np.array(code["h"], dtype=int)
        logical = np.array(code["logical"], dtype=int)

        original_h = None
        original_path = originals_dir / f"{stem}.original.yaml"
        if original_path.exists():
            original = yaml.safe_load(original_path.read_text(encoding="utf-8")) or {}
            if original.get("h"):
                original_h = np.array(original["h"], dtype=int)

        circ = build_annotated(
            body=body_path.read_text(encoding="utf-8"),
            stored_h=stored_h,
            logical=logical,
            n=n,
            k=k,
            kind=kind,
            logical_state=state,
            original_h=original_h,
            notes=data.get("notes") or "",
        )
        if circ is None:
            results.append(Result(stem, "skipped", f"not representable ({kind}, {state or 'n/a'})"))
            continue

        error = validate_annotated(circ)
        if error:
            results.append(Result(stem, "failed", error))
            continue

        annotated_path = circuits_dir / f"{stem}.{ANNOTATED_FORMAT}"
        text = str(circ) + "\n"
        # The Crumble link follows the same width gate as the canonical body:
        # past it the URL is megabytes and unusable.
        url = circ.to_crumble_url() if circ.num_qubits <= LARGE_CIRCUIT_MAX_QUBITS else ""

        # Compare rendered text, not the parsed value: a duplicated key parses to
        # the same value while leaving the file invalid.
        current_yaml = path.read_text(encoding="utf-8")
        desired_yaml = _with_annotated_url(current_yaml, url)
        body_changed = (
            not annotated_path.exists() or annotated_path.read_text(encoding="utf-8") != text
        )
        if not body_changed and desired_yaml == current_yaml:
            results.append(Result(stem, "unchanged"))
            continue

        if not dry_run:
            annotated_path.write_text(text, encoding="utf-8")
            if desired_yaml != current_yaml:
                path.write_text(desired_yaml, encoding="utf-8")
        results.append(
            Result(stem, "written", f"{circ.num_detectors} detectors, {circ.num_observables} obs")
        )

    return results


def _with_annotated_url(text: str, url: str) -> str:
    """Return `text` with exactly one `crumble_url_annotated`, after `crumble_url`.

    Edits the text rather than round-tripping through yaml.safe_load/dump: a full
    re-dump would reflow every circuit file (block scalars, key order, quoting)
    and bury the real change in noise.

    Pure, so the caller can diff the result against the file and stay idempotent
    even when the file is already malformed.
    """
    # Drop every existing occurrence first, then insert at most one. Doing this
    # in a single pass double-writes: the insert-after-`crumble_url` branch and
    # the replace-existing branch both fire on an already-annotated file.
    lines = [
        ln for ln in text.splitlines(keepends=True) if not ln.startswith(f"{ANNOTATED_URL_KEY}:")
    ]
    if not url:
        return "".join(lines)

    entry = f"{ANNOTATED_URL_KEY}: {url}\n"
    out, inserted = [], False
    for line in lines:
        out.append(line)
        if not inserted and line.startswith("crumble_url:"):
            out.append(entry)
            inserted = True
    if not inserted:
        out.append(entry)
    return "".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data_yaml")
    parser.add_argument("--only", default="", help="Only process stems with this prefix")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    results = annotate_all(Path(args.data_dir), only=args.only, dry_run=args.dry_run)
    counts = Counter(r.status for r in results)

    for r in results:
        if r.status == "failed":
            print(f"  FAILED   {r.stem}: {r.detail}")
    skipped = Counter(r.detail for r in results if r.status == "skipped")
    for detail, count in skipped.most_common():
        print(f"  skipped  {count:4d}  {detail}")

    print()
    for status in ("written", "unchanged", "skipped", "failed"):
        if counts[status]:
            print(f"{counts[status]:5d}  {status}")
    if args.dry_run:
        print("\n(dry run — nothing written)")
    elif counts["written"]:
        print("\nRun 'npm run db:create' to rebuild the database.")
    return 1 if counts["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
