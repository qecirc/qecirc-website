#!/usr/bin/env python
"""MQT QECC front-search FT state-prep import.

Imports the fault-tolerant |0...0>_L preparation circuits found by MQT QECC's
front search (`mqt.qecc.circuit_synthesis.ft_search`), shipped in the qecc
repository under `scripts/ft_stateprep/front_search/`. See README.md for the
dataset layout, fit strategy and the decisions baked in.

The dataset's `index.csv` is the manifest: every row is one circuit, so a
re-run after the dataset grows imports exactly the new rows.

Usage:
  python rebuild_all.py                        # classify only (no writes)
  python rebuild_all.py --write                # import new rows into data_yaml
  python rebuild_all.py --write --overwrite    # data refresh: replace, keep qec_ids
  python rebuild_all.py --only color_17_1_5    # restrict to one dataset code
  python rebuild_all.py --dataset PATH         # dataset somewhere else
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DATASET = REPO.parent / "mqt-qecc" / "scripts/ft_stateprep/front_search"
SOURCE_FILE_PREFIX = "scripts/ft_stateprep/front_search"
sys.path.insert(0, str(REPO))

import stim  # noqa: E402

from scripts.add_circuit import import_state_prep  # noqa: E402
from scripts.add_circuit.code_identify import (  # noqa: E402
    build_symplectic_h,
    gf2_rank,
    split_h_to_css,
)
from scripts.add_circuit.find_sigma import find_sigma  # noqa: E402
from scripts.add_circuit.matrix_format import decode as decode_matrix  # noqa: E402
from scripts.add_circuit.yaml_helpers import load_yaml  # noqa: E402

# Plain-text provenance: the dataset has no stable public link yet, and the
# library requires a non-empty source. To switch to a link later, change it here
# and re-run with --write --overwrite.
SOURCE = "MQT QECC, scripts/ft_stateprep/front_search"
TOOL = "mqt-qecc"
# The search's own name as a method tag, in the library's `verification:*`
# family (`verification:opt`, `verification:heuristic`, ...). Not "block": the
# circuits mix bare checks, flags and ancilla blocks, and the [[9,1,3]] one uses
# a single bare check.
METHOD_TAG = "verification:front-search"


@dataclass(frozen=True)
class Code:
    slug: str  # stored code slug in data_yaml/codes/
    stored: bool  # True: fit onto an existing code. False: seed a new one.
    name: str = ""  # display name, new codes only
    tags: tuple[str, ...] = ()  # family tags, new codes only
    zoo_url: str = ""  # new codes only
    aliases: tuple[str, ...] = ()  # new codes only, written into the code YAML


# Dataset code (directory / JSON name) -> library code. Every stored code here
# was checked to be the same code up to a qubit permutation (find_sigma).
CODES: dict[str, Code] = {
    "surface_9_1_3": Code("rotated-surface-code-d-3", True),
    "surface_25_1_5": Code("rotated-surface-code-d-5", True),
    "surface_49_1_7": Code("rotated-surface-code-d-7", True),
    "color_17_1_5": Code("17-1-5", True),
    "color_31_1_7": Code("31-1-7", True),
    "golay_23_1_7": Code("23-1-7", True),
    "sd_20_2_6": Code("20-2-6", True),
    # Not in the library yet: the two-block group algebra (2BGA) code of Lin &
    # Pryadko, with weight-8 checks.
    "bga_24_4_5": Code(
        "24-4-5",
        False,
        name="Two-Block Group Algebra Code",
        tags=("LDPC",),
        zoo_url="https://errorcorrectionzoo.org/c/2bga",
        aliases=("[[24,4,5]]", "2BGA code"),
    ),
}


@dataclass(frozen=True)
class Row:
    code: str
    n: int
    k: int
    d: int
    t: int
    state: str
    ops: int
    cnots: int
    measurements: int
    depth: int
    qubits: int
    file: str
    extra: bool = False  # a superseded circuit, read from SUPERSEDED


# Circuits that an earlier version of the collection held and that a later
# circuit beats (at most as many operations at no greater depth, better in one),
# so the collection dropped them. Imported on request as extra entries. The
# dataset no longer has them, so a copy of each file and its index.csv row lives
# in superseded/ next to this script; their notes say they are not in the
# collection.
SUPERSEDED = HERE / "superseded"


def read_index(root: Path, extra: bool = False) -> list[Row]:
    rows = []
    with (root / "index.csv").open() as f:
        for r in csv.DictReader(f):
            ints = {k: int(v) for k, v in r.items() if k not in ("code", "state", "file")}
            rows.append(Row(code=r["code"], state=r["state"], file=r["file"], extra=extra, **ints))
    return rows


def read_superseded(current: list[Row]) -> list[Row]:
    """The vendored superseded rows. A file that is back in the dataset's
    index.csv is left to it."""
    have = {r.file for r in current}
    return [r for r in read_index(SUPERSEDED, extra=True) if r.file not in have]


def read_circuit(dataset: Path, row: Row) -> str:
    return ((SUPERSEDED if row.extra else dataset) / row.file).read_text()


def load_code(dataset: Path, name: str) -> dict[str, np.ndarray | int]:
    c = json.loads((dataset / "codes" / f"{name}.json").read_text())
    out: dict[str, np.ndarray | int] = {
        key: np.array(c[key], dtype=int) for key in ("Hx", "Hz", "Lx", "Lz")
    }
    out["n"], out["d"] = int(c["n"]), int(c["d"])
    return out


def stored_h(slug: str, data_dir: Path) -> np.ndarray:
    return decode_matrix(load_yaml((data_dir / "codes" / f"{slug}.yaml").read_text())["h"])


def prep_body(text: str, n: int) -> str:
    """Rewrite the reset layer to library convention, keep everything else.

    A stored prep body leaves the |0...0> input implied: `R` is dropped and
    `RX` becomes `H` (same rule as surface-code-encodings), for every reset that
    is the first operation on its qubit, where the rewrite is exact. A reset of
    an ancilla reused after its measurement is a real operation and is kept.

    The mid-circuit measurements and the DETECTORs stay: they ARE the
    verification. The detectors are parities of several measurements, which is
    the post-selection condition and is not recoverable from the bare
    measurements.

    Ancilla indices are compacted to `n, n+1, ...` in their original order. The
    files leave gaps (a [[17,1,5]] circuit with 25 qubits uses indices up to
    28), and stim counts a qubit up to the highest index, so the gaps would
    inflate the stored `qubit_count` past the dataset's own count. Data qubits
    keep their indices.
    """
    src = stim.Circuit(text)
    used = sorted({t.value for i in src.flattened() for t in i.targets_copy() if t.is_qubit_target})
    remap = {q: q for q in used if q < n}
    remap.update({q: n + i for i, q in enumerate(q for q in used if q >= n)})

    touched: set[int] = set()
    out = stim.Circuit()
    for inst in src.flattened():
        qubits = [t.value for t in inst.targets_copy() if t.is_qubit_target]
        if inst.name in ("R", "RX"):
            fresh = [q for q in qubits if q not in touched]
            reused = [q for q in qubits if q in touched]
            touched.update(qubits)
            if fresh and inst.name == "RX":
                out.append("H", [remap[q] for q in fresh])
            if reused:  # an ancilla reused after its measurement: a real reset
                out.append(inst.name, [remap[q] for q in reused])
            continue
        touched.update(qubits)
        targets = [
            stim.GateTarget(remap[t.value]) if t.is_qubit_target else t for t in inst.targets_copy()
        ]
        out.append(inst.name, targets, inst.gate_args_copy())
    return str(out)


def check_source(circ: stim.Circuit, code: dict, row: Row) -> str | None:
    """Consistency gate in the dataset's own labeling. Returns a reason or None.

    * counts in index.csv match the file,
    * the detectors are deterministic without noise (stim refuses to build a
      detector error model otherwise),
    * after post-selection the data qubits are a +1 eigenstate of every
      stabilizer and every Z-logical of the dataset's own matrices, i.e. they
      hold |0...0>_L. Checked on several random measurement outcomes, since a
      mid-circuit measurement result is random in a noiseless simulation.
    """
    counts = {"CX": 0, "meas": 0}
    used: set[int] = set()
    for inst in circ.flattened():
        used.update(t.value for t in inst.targets_copy() if t.is_qubit_target)
        if inst.name == "CX":
            counts["CX"] += len(inst.targets_copy()) // 2
        elif inst.name in ("M", "MX", "MR", "MRX"):
            counts["meas"] += len(inst.targets_copy())
    counts["qubits"] = len(used)
    if (counts["CX"], counts["meas"], len(used)) != (row.cnots, row.measurements, row.qubits):
        return f"index.csv counts {row.cnots}/{row.measurements}/{row.qubits} != file {counts}"
    try:
        circ.detector_error_model()
    except ValueError as e:
        return f"non-deterministic detector: {str(e).splitlines()[0][:80]}"

    n = code["n"]
    hx, hz, lz = code["Hx"], code["Hz"], code["Lz"]
    rows = [np.concatenate([r, np.zeros(n, int)]) for r in hx]
    rows += [np.concatenate([np.zeros(n, int), r]) for r in np.vstack([hz, lz])]
    for seed in range(4):
        sim = stim.TableauSimulator(seed=seed)
        sim.do_circuit(circ)
        for r in rows:
            ps = stim.PauliString(circ.num_qubits)
            for j in range(n):
                x, z = r[j], r[j + n]
                if x or z:
                    ps[j] = {(1, 0): 1, (1, 1): 2, (0, 1): 3}[(int(x), int(z))]
            if sim.peek_observable_expectation(ps) != 1:
                return f"seed {seed}: {ps} is not +1 on the prepared state"
    return None


def on_front(row: Row, rows: list[Row]) -> bool:
    """No other circuit of the same code has at most as many operations and at
    most the depth, and is strictly better in one of them. The collection is the
    front plus a few circuits kept on purpose although the front beats them."""
    return not any(
        o.code == row.code
        and o.ops <= row.ops
        and o.depth <= row.depth
        and (o.ops, o.depth) != (row.ops, row.depth)
        for o in rows
    )


def describe(row: Row, front: bool) -> tuple[str, list[str], str]:
    if row.extra:
        standing = (
            "Not in the current collection: an earlier version held it, and a later "
            "circuit with at most as many operations and no greater depth, better in "
            "one of the two, replaced it. Kept here as an alternative; a copy of the "
            "source file is in the QECirc repository, data-imports/mqt-front-search/superseded"
        )
    elif front:
        standing = (
            "On this code's depth/operation-count front: no other circuit in the "
            "collection has fewer operations without greater depth, or lower depth "
            "without more operations"
        )
    else:
        standing = (
            "Not on this code's depth/operation-count front: another circuit in the "
            "collection has fewer operations at no greater depth, or lower depth with no "
            "more operations. Kept in the collection as an alternative"
        )
    name = f"FT zero (front search, depth {row.depth}, {row.ops} ops)"
    tags = ["state-preparation", "ft", METHOD_TAG, f"distance:{row.d}"]
    notes = (
        f"Fault-tolerant preparation of the logical all-zero state, found by the front "
        f"search of MQT QECC (mqt.qecc.circuit_synthesis.ft_search). Tolerates t = {row.t} "
        f"faults: every set of at most t faults either sets a detector to 1 or leaves X "
        f"and Z errors of weight at most the number of faults each, up to stabilizers. "
        f"Post-selection protocol: a shot is accepted if every DETECTOR is 0 (detectors "
        f"are parities of the verification measurements and are kept in the stored "
        f"body). Checked with MQT QECC's exact fault-tolerance check, which enumerates "
        f"every set of up to t faults. {row.cnots} CNOTs, "
        f"{row.measurements} measurements, two-qubit depth {row.depth} (ASAP schedule). " + standing
    )
    return name, tags, notes


def gate_set_of(circ: stim.Circuit) -> str:
    skip = ("TICK", "QUBIT_COORDS", "DETECTOR", "OBSERVABLE_INCLUDE")
    return ",".join(sorted({i.name for i in circ.flattened() if i.name not in skip}))


def sigma_for(code: dict, slug: str, data_dir: Path) -> list[int] | None:
    """sigma[new] = old onto the stored code, or None if the labelings agree."""
    n = code["n"]
    hx2, hz2 = (np.asarray(m) for m in split_h_to_css(stored_h(slug, data_dir), n))

    def same(a: np.ndarray, b: np.ndarray) -> bool:
        return gf2_rank(np.vstack([a, b])) == gf2_rank(a) == gf2_rank(b)

    if same(code["Hx"], hx2) and same(code["Hz"], hz2):
        return None
    sigma = find_sigma(code["Hx"], code["Hz"], hx2, hz2)
    if sigma is None:
        raise ValueError(f"no qubit permutation onto stored code {slug}")
    return sigma


def stored_circuits(data_dir: Path) -> dict[str, Path]:
    """Source-file -> circuit YAML for every circuit this importer wrote before."""
    out = {}
    for p in sorted((data_dir / "circuits").glob("*.yaml")):
        doc = load_yaml(p.read_text())
        if doc.get("tool") != TOOL:
            continue
        for part in (doc.get("notes") or "").split(". "):
            if part.startswith(f"Source file: {SOURCE_FILE_PREFIX}/"):
                out[part.removeprefix(f"Source file: {SOURCE_FILE_PREFIX}/")] = p
    return out


def add_aliases(path: Path, aliases: tuple[str, ...]) -> None:
    """Give a newly seeded code its aliases; the pipeline has no argument for
    them. Inserted as text after `d:` so the rest of the file is untouched, and
    only when the file has none, so hand edits survive a re-run."""
    if not aliases or not path.is_file():
        return
    text = path.read_text()
    if "\naliases:" in text:
        return
    block = "aliases:\n" + "".join(f'  - "{a}"\n' for a in aliases)
    lines = text.splitlines(keepends=True)
    at = next(i for i, line in enumerate(lines) if line.startswith("d:")) + 1
    path.write_text("".join(lines[:at]) + block + "".join(lines[at:]))


def run(dataset: Path, write: bool, data_dir: Path, only: str | None, overwrite: bool) -> int:
    all_rows = read_index(dataset)
    superseded = read_superseded(all_rows)
    rows = [r for r in all_rows + superseded if not only or r.code == only]
    unknown = sorted({r.code for r in rows} - set(CODES))
    if unknown:
        raise SystemExit(f"index.csv names codes with no mapping in CODES: {unknown}")

    existing = stored_circuits(data_dir)
    report: list[str] = []
    counts = {"imported": 0, "present": 0, "skipped": 0, "failed": 0}
    codes: dict[str, dict] = {}
    sigmas: dict[str, list[int] | None] = {}

    for row in rows:
        spec = CODES[row.code]
        if row.state != "zero":
            report.append(f"SKIP {row.file}: state {row.state!r} (importer handles zero only)")
            counts["skipped"] += 1
            continue
        if row.file in existing and not overwrite:
            counts["present"] += 1
            continue
        if row.code not in codes:
            codes[row.code] = load_code(dataset, row.code)
            if spec.stored:
                sigmas[row.code] = sigma_for(codes[row.code], spec.slug, data_dir)
        code = codes[row.code]
        if (code["n"], code["d"]) != (row.n, row.d):
            report.append(f"FAIL {row.file}: index.csv n/d disagree with codes/{row.code}.json")
            counts["failed"] += 1
            continue

        raw = stim.Circuit(read_circuit(dataset, row))
        problem = check_source(raw, code, row)
        if problem:
            report.append(f"FAIL {row.file}: {problem}")
            counts["failed"] += 1
            continue

        body = prep_body(str(raw), row.n)
        own_h = build_symplectic_h(code["Hx"], code["Hz"])
        name, tags, notes = describe(row, on_front(row, all_rows))
        kwargs = dict(
            circuit=body,
            n=row.n,
            d=row.d,
            method="anchor",
            circuit_name=name,
            source=SOURCE,
            tool=TOOL,
            source_file=f"{SOURCE_FILE_PREFIX}/{row.file}",
            logical_state="zero",
            connectivity="fully-connected",
            gate_set=gate_set_of(stim.Circuit(body)),
            tags=tags,
            notes=notes,
            data_dir=str(data_dir),
            dry_run=not write,
            overwrite=overwrite,
        )
        if spec.stored:
            # Fit in the dataset's labeling against the stored code's matrices,
            # handing over sigma so no search runs (rotated d=7 defeats it).
            sh = stored_h(spec.slug, data_dir)
            sigma = sigmas[row.code]
            kwargs.update(anchor_H=sh, permutation=sigma or list(range(row.n)), code_name="")
        else:
            kwargs.update(
                anchor_H=own_h,
                # None: the fit confirms identity against the dataset's own
                # matrices, and add_circuit then seeds the code (canonicalizing
                # it and relabeling the circuit to match, recorded in notes).
                permutation=None,
                code_name=spec.name,
                code_slug=spec.slug,
                code_tags=list(spec.tags),
                zoo_url=spec.zoo_url,
            )
        try:
            import_state_prep(**kwargs)
            counts["imported"] += 1
        except Exception as e:  # noqa: BLE001
            report.append(f"FAIL {row.file}: {type(e).__name__}: {str(e).splitlines()[0][:100]}")
            counts["failed"] += 1

    if write:
        for spec in {CODES[r.code] for r in rows if not CODES[r.code].stored}:
            add_aliases(data_dir / "codes" / f"{spec.slug}.yaml", spec.aliases)

    # Circuits stored by an earlier run whose file left the index (the front
    # moved). Never deleted automatically: qec_ids are permanent, so removing
    # one is a maintainer decision.
    listed = {r.file for r in all_rows + superseded}
    for src, p in existing.items():
        if src not in listed:
            report.append(f"STALE {p.name}: {src} is no longer in index.csv")

    verb = "imported" if write else "classified"
    print(
        f"{verb}={counts['imported']} already-present={counts['present']} "
        f"skipped={counts['skipped']} failed={counts['failed']} "
        f"(of {len(rows)} rows, {len(superseded)} superseded)"
    )
    for line in report:
        print("  " + line)
    return counts["failed"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--data-dir", default=str(REPO / "data_yaml"))
    ap.add_argument("--dataset", default=str(DATASET))
    ap.add_argument("--only", default=None, help="one dataset code, e.g. color_17_1_5")
    ap.add_argument(
        "--overwrite",
        action="store_true",
        help="replace already-imported circuits in place (data refresh), keeping qec_ids",
    )
    args = ap.parse_args()
    dataset = Path(args.dataset)
    if not (dataset / "index.csv").is_file():
        raise SystemExit(f"dataset not found: {dataset} (pass --dataset)")
    failed = run(dataset, args.write, Path(args.data_dir), args.only, args.overwrite)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
