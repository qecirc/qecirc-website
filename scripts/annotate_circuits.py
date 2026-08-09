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

No link is written: the Crumble URL is a pure function of the body on screen and
is derived at render time (`crumbleUrl` in src/lib/stim-format.ts), so it follows
the Detectors switch by construction instead of needing a second stored copy.

Idempotent: re-running regenerates from source and rewrites only what changed.
Every emitted body is checked with stim's detector error model before it is
written — a circuit whose detectors are not provably deterministic is skipped
and reported, never written.

Settled verdicts (unchanged/skipped/failed) are cached in
.cache/annotate-circuits.json keyed by the content of every input AND the
current output file, so re-runs only recompute circuits where something moved.
"written" is never cached: writing changes the output file, so the next run
recomputes it once and settles to a cached "unchanged". Pass --no-cache to
force a full recompute.

Usage:
    uv run python scripts/annotate_circuits.py
    uv run python scripts/annotate_circuits.py --dry-run
    uv run python scripts/annotate_circuits.py --only rotated-surface-code-d-3
    uv run python scripts/annotate_circuits.py --no-cache
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
    validate_annotated,
)
from scripts.add_circuit.matrix_format import decode as decode_matrix  # noqa: E402
from scripts.result_cache import ResultCache, source_fingerprint, text_or_missing  # noqa: E402

ANNOTATED_FORMAT = "stim-annotated"

# C-backed loader when available: ~15x faster over the whole corpus, and this
# script parses every circuit YAML even on a fully-warm cache run.
_FastLoader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def _load_yaml(text: str):
    return yaml.load(text, Loader=_FastLoader)


DEFAULT_CACHE_PATH = Path(_PROJECT_ROOT) / ".cache" / "annotate-circuits.json"

# Modules whose logic determines what gets annotated and how; hashed into
# every cache key so logic changes self-invalidate the cache.
_SOURCE_DEPS = [
    Path(__file__),
    Path(_PROJECT_ROOT) / "scripts" / "add_circuit" / "annotate.py",
    Path(_PROJECT_ROOT) / "scripts" / "add_circuit" / "compute_circuit.py",
]

# Only settled verdicts are replayable: a "written" run mutates its own inputs
# (the output file is part of the key), so caching it would be self-defeating.
_CACHEABLE_STATUSES = ("unchanged", "skipped", "failed")


def open_cache(path: Path = DEFAULT_CACHE_PATH) -> ResultCache:
    return ResultCache(path, source_fingerprint(*_SOURCE_DEPS))


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


def annotate_all(
    data_dir: Path, only: str = "", dry_run: bool = False, cache: ResultCache | None = None
) -> list[Result]:
    codes_dir = data_dir / "codes"
    circuits_dir = data_dir / "circuits"
    matrices_dir = data_dir / "matrices"

    codes = {p.stem: _load_yaml(p.read_text(encoding="utf-8")) for p in codes_dir.glob("*.yaml")}
    code_texts = {p.stem: p.read_text(encoding="utf-8") for p in codes_dir.glob("*.yaml")}
    results: list[Result] = []
    seen_stems: set[str] = set()

    def _finish(result: Result, key: str | None) -> None:
        if cache is not None and key is not None and result.status in _CACHEABLE_STATUSES:
            cache.put(result.stem, key, [result.status, result.detail])
        results.append(result)

    for path in sorted(circuits_dir.glob("*.yaml")):
        stem = path.stem
        if only and not stem.startswith(only):
            continue
        current_yaml = path.read_text(encoding="utf-8")
        data = _load_yaml(current_yaml)
        tags = data.get("tags") or []
        kind, state = _kind_and_state(tags)
        if not kind:
            continue  # flag gadgets: no code of their own, nothing to annotate against

        slug = _code_slug(stem)
        body_path = circuits_dir / f"{stem}.stim"

        # The outcome is a pure function of these inputs plus the current
        # output file (hashed in, so an out-of-date .stim-annotated misses and
        # is regenerated). Replay settled verdicts; anything else recomputes.
        key = None
        if cache is not None:
            seen_stems.add(stem)
            # The submitted matrices seed the detector sparsifier, so the key
            # tracks the shared matrices file the circuit references (the
            # reference itself is part of current_yaml).
            matrices_ref = data.get("original_matrices")
            key = cache.key(
                current_yaml,
                text_or_missing(body_path),
                code_texts.get(slug, "<no-code>"),
                text_or_missing(matrices_dir / f"{matrices_ref}.yaml")
                if matrices_ref
                else "<no-originals>",
                text_or_missing(circuits_dir / f"{stem}.{ANNOTATED_FORMAT}"),
            )
            hit = cache.get(stem, key)
            if hit is not None:
                results.append(Result(stem, hit[0], hit[1]))
                continue

        code = codes.get(slug)
        if code is None:
            _finish(Result(stem, "failed", f"code {slug!r} not found"), key)
            continue

        if not body_path.exists():
            _finish(Result(stem, "failed", "no .stim body"), key)
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
                original = _load_yaml(original_path.read_text(encoding="utf-8")) or {}
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
            _finish(Result(stem, "skipped", skip_reason), key)
            continue

        error = validate_annotated(circ)
        if error:
            _finish(Result(stem, "failed", error), key)
            continue

        annotated_path = circuits_dir / f"{stem}.{ANNOTATED_FORMAT}"
        text = str(circ) + "\n"
        if annotated_path.exists() and annotated_path.read_text(encoding="utf-8") == text:
            _finish(Result(stem, "unchanged"), key)
            continue

        if not dry_run:
            annotated_path.write_text(text, encoding="utf-8")
        results.append(
            Result(stem, "written", f"{circ.num_detectors} detectors, {circ.num_observables} obs")
        )

    if cache is not None:
        # A partial run (--only) sees a subset of stems; pruning to it would
        # evict every other circuit's entry.
        cache.save(prune_to=seen_stems if not only else None)
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data_yaml")
    parser.add_argument("--only", default="", help="Only process stems with this prefix")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Recompute every circuit instead of replaying settled verdicts",
    )
    args = parser.parse_args()

    cache = None if args.no_cache else open_cache()
    results = annotate_all(Path(args.data_dir), only=args.only, dry_run=args.dry_run, cache=cache)
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
    if cache is not None and cache.hits:
        print(f"       ({cache.hits} verdicts replayed from cache)")
    if args.dry_run:
        print("\n(dry run — nothing written)")
    elif counts["written"]:
        print("\nRun 'npm run db:create' to rebuild the database.")
    return 1 if counts["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
