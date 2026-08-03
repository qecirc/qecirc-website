"""
Backfill `stim-annotated` bodies.

Writes `data_yaml/circuits/<stem>.stim-annotated`, and what it writes depends on
what the circuit is:

- **State-prep and encoding** — a reset prologue stating the `|0...0>` input,
  then the body, then — where a terminal readout basis exists — the readout and
  its detectors. Non-CSS codes get the prologue alone (see
  `annotate.build_annotated`).
- **Syndrome extraction** — the memory experiment the round belongs to: reset
  the data, `REPEAT d` of the round, terminal readout, detectors, observable
  (see `annotate.build_annotated_se`). A round is not reset-free and has no
  tableau, so none of the derive/fit machinery is pointed at it.

Also rewrites both Crumble links in the circuit YAML. `crumble_url` follows what
the STIM tab shows by default, which now carries the prologue, so leaving it
pointing at the reset-free stored body would make link and text disagree.
`crumble_url_annotated` is written only when there is a second view to link to.

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
import stim  # noqa: E402
import yaml  # noqa: E402

from scripts.add_circuit.annotate import (  # noqa: E402
    build_annotated,
    build_annotated_se,
    logical_input_qubits,
    strip_readout,
    validate_annotated,
)
from scripts.add_circuit.compute_circuit import LARGE_CIRCUIT_MAX_QUBITS  # noqa: E402
from scripts.add_circuit.matrix_format import decode as decode_matrix  # noqa: E402

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
    elif "syndrome-extraction" in tags:
        kind = "syndrome-extraction"
    state = next((t.split(":", 1)[1] for t in tags if t.startswith("logical-state:")), "")
    return kind, state


def annotate_all(data_dir: Path, only: str = "", dry_run: bool = False) -> list[Result]:
    codes_dir = data_dir / "codes"
    circuits_dir = data_dir / "circuits"
    matrices_dir = data_dir / "matrices"

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
            continue  # flag gadgets: no code of their own, nothing to annotate against

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
        gauge_qubits = code.get("gauge_qubits") or 0
        stored_h = decode_matrix(code["h"])
        logical = decode_matrix(code["logical"])

        # The submitted matrices are shared by every circuit of one code, so the
        # circuit names the file rather than carrying its own copy.
        original_h = None
        if data.get("original_matrices"):
            original_path = matrices_dir / f"{data['original_matrices']}.yaml"
            if original_path.exists():
                original = yaml.safe_load(original_path.read_text(encoding="utf-8")) or {}
                if original.get("h"):
                    original_h = decode_matrix(original["h"])

        if kind == "syndrome-extraction":
            # A round is annotated as the memory experiment it belongs to, and
            # the round count that makes one distance-preserving is d.
            circ = build_annotated_se(
                body=body_path.read_text(encoding="utf-8"),
                stored_h=stored_h,
                logical=logical,
                n=n,
                rounds=code.get("d") or 1,
            )
            skip_reason = "no per-measurement check map (see round_check_matrix)"
        else:
            circ = build_annotated(
                body=body_path.read_text(encoding="utf-8"),
                stored_h=stored_h,
                logical=logical,
                n=n,
                k=k,
                kind=kind,
                logical_state=state,
                gauge_qubits=gauge_qubits,
                original_h=original_h,
                notes=data.get("notes") or "",
            )
            skip_reason = _why_skipped(body_path, stored_h, n, k, kind, gauge_qubits)
        if circ is None:
            results.append(Result(stem, "skipped", skip_reason))
            continue

        error = validate_annotated(circ)
        if error:
            results.append(Result(stem, "failed", error))
            continue

        annotated_path = circuits_dir / f"{stem}.{ANNOTATED_FORMAT}"
        text = str(circ) + "\n"
        # Both Crumble links follow the same width gate as the canonical body:
        # past it the URL is megabytes and unusable.
        wide = circ.num_qubits > LARGE_CIRCUIT_MAX_QUBITS
        # `crumble_url` is the link for what the STIM tab shows by default, which
        # for these circuits is the reset prologue + body — not the stored
        # canonical body, which leaves the |0...0> input implied. Overwriting it
        # is what keeps the link and the displayed text in step.
        plain_url = "" if wide else strip_readout(circ).to_crumble_url()
        # The second link only exists if there is a second view. A prologue-only
        # body (non-CSS: no basis reads its stabilizers) has no Detectors switch,
        # so an annotated URL there would just duplicate `crumble_url`.
        url = "" if wide or circ.num_detectors == 0 else circ.to_crumble_url()

        # Compare rendered text, not the parsed value: a duplicated key parses to
        # the same value while leaving the file invalid.
        current_yaml = path.read_text(encoding="utf-8")
        desired_yaml = _with_urls(current_yaml, plain_url, url)
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


def _why_skipped(
    body_path: Path, stored_h: np.ndarray, n: int, k: int, kind: str, gauge_qubits: int = 0
) -> str:
    """Explain a ``build_annotated`` refusal.

    Every prep and encoder should get at least a reset prologue, so a refusal is
    worth a reason rather than a shrug. For an encoder it means the k logical
    inputs could not be derived — and since the derivation just asks which
    qubits' Z propagates outside the stabilizer group, an answer other than k
    says the circuit and the code it is filed under disagree.
    """
    if kind != "encoding":
        return "no reset targets"
    circ = stim.Circuit(body_path.read_text(encoding="utf-8"))
    inputs = logical_input_qubits(circ, stored_h, n)
    if inputs is None:
        return "encoder inputs underivable (no tableau and no resets)"
    expected = k + gauge_qubits
    detail = "" if not gauge_qubits else f" (k={k} plus {gauge_qubits} gauge qubits)"
    return (
        f"encoder derived {len(inputs)} logical inputs, expected {expected}{detail} — "
        f"circuit and stored h disagree"
    )


def _with_urls(text: str, plain: str, annotated: str) -> str:
    """Return `text` with the two Crumble links set: `crumble_url` to `plain`,
    followed by exactly one `crumble_url_annotated`.

    Edits the text rather than round-tripping through yaml.safe_load/dump: a full
    re-dump would reflow every circuit file (block scalars, key order, quoting)
    and bury the real change in noise.

    Pure, so the caller can diff the result against the file and stay idempotent
    even when the file is already malformed.
    """
    # Drop every existing occurrence of the annotated key first, then insert at
    # most one. Doing this in a single pass double-writes: the
    # insert-after-`crumble_url` branch and the replace-existing branch both fire
    # on an already-annotated file. `crumble_url:` does not match the longer key.
    lines = [
        ln for ln in text.splitlines(keepends=True) if not ln.startswith(f"{ANNOTATED_URL_KEY}:")
    ]
    if not annotated:
        return "".join(lines)

    entry = f"{ANNOTATED_URL_KEY}: {annotated}\n"
    out, inserted = [], False
    for line in lines:
        if plain and line.startswith("crumble_url:"):
            out.append(f"crumble_url: {plain}\n")
        else:
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
