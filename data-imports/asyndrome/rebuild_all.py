#!/usr/bin/env python
"""AlphaSyndrome syndrome-measurement schedule import (arXiv:2601.12509).

Imports the syndrome-measurement *schedules* from acasta-yhliu/asyndrome, the
artifact of "AlphaSyndrome: Tackling the Syndrome Measurement Circuit Scheduling
Problem for QEC Codes" (ASPLOS '26). A schedule is a list of ticks, each a set of
``(data, ancilla, pauli)`` checks that run in parallel; the paper's contribution
is the tick assignment, so the emitter never re-packs it.

One schedule becomes one library circuit: a single syndrome-extraction round.
``scripts/add_circuit/syndrome_extraction.build_se_round`` does the emitting and
``validate_syndrome_extraction_h`` gates every import — 10 of the dataset's 69
schedules do not survive that check. See README.md for which, and why.

Usage:
  python rebuild_all.py                    # classify only (no writes)
  python rebuild_all.py --write            # import into data_yaml
  python rebuild_all.py --dataset PATH     # clone of acasta-yhliu/asyndrome
  python rebuild_all.py --only surface     # restrict to codes whose name matches
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DATASET = REPO.parent / "asyndrome"  # clone of the artifact repo
sys.path.insert(0, str(REPO))

from scripts.add_circuit import (  # noqa: E402
    UncertainDedupError,
    add_circuit,
    build_se_round,
    validate_syndrome_extraction_h,
)
from scripts.add_circuit.code_identify import canonical_hash, split_h_to_css  # noqa: E402

SOURCE = "https://arxiv.org/abs/2601.12509"
TOOL = "asyndrome"

# Per-family metadata for codes this import has to create. Keyed by the
# dataset's own `family` field.
FAMILY = {
    "Rotated Surface Code": (
        "Rotated Surface Code",
        "https://errorcorrectionzoo.org/c/rotated_surface",
        ["CSS", "surface-code", "topological"],
    ),
    "Hexagon Color Code": (
        "6.6.6 Color Code",
        "https://errorcorrectionzoo.org/c/triangular_color",
        ["CSS", "self-dual", "color-code", "topological"],
    ),
    "SquareOctagon Color Code": (
        "4.8.8 Color Code",
        "https://errorcorrectionzoo.org/c/488_color",
        ["CSS", "self-dual", "color-code", "topological"],
    ),
    "Defect Surface Code": (
        "Surface Code with Defects",
        "",
        ["CSS", "surface-code", "topological"],
    ),
    "Hyperbolic Surface Code": (
        "Hyperbolic Surface Code",
        "https://errorcorrectionzoo.org/c/hyperbolic_surface",
        ["CSS", "surface-code", "topological", "LDPC"],
    ),
    "Hyperbolic Color Code": (
        "Hyperbolic Color Code",
        "https://errorcorrectionzoo.org/c/hyperbolic_color",
        ["CSS", "self-dual", "color-code", "topological", "LDPC"],
    ),
    "Bivariate Bicycle Code": (
        "Bivariate Bicycle Code",
        "",
        ["CSS", "bivariate-bicycle-code", "LDPC"],
    ),
    "Self-Dual Bivariate Bicycle Code": (
        "Self-Dual Bivariate Bicycle Code",
        "",
        ["CSS", "self-dual", "bivariate-bicycle-code", "LDPC"],
    ),
}

# How each scheduling method is presented. `decoder` is empty for the methods
# that do not consult one.
DECODER = {
    "bp_osd": ("BP-OSD", "bp-osd"),
    "bp_lsd": ("BP-LSD", "bp-lsd"),
    "pymatching": ("MWPM", "mwpm"),
    "hypergraph_union_find": ("Union-Find", "union-find"),
}

# Codes excluded outright, with the reason recorded for the README.
EXCLUDED_CODES: dict[str, str] = {}

# Codes whose cheap invariants align with a stored code that is NOT the same
# code. `assume_new` is only safe with a proof, so the proof sits next to the
# flag rather than in a commit message.
ASSUME_NEW = {
    "hypersurface-36-8-4-4": (
        "Candidate 36-8-4-bpc is a balanced-product cyclic code (QUITS, "
        "arXiv:2504.02673) that happens to share n and k. Its X- and Z-row-space "
        "ranks are both 14; this code's are 11 and 17. Rank is a permutation "
        "invariant and an X<->Z swap gives 17/11, so no relabeling reconciles "
        "them. The exhaustive weight enumerators differ too — the X row space "
        "has 12 words of weight 6 here and 18 there, and this code has 18 of "
        "weight 4 in Z where the stored one has none."
    ),
}

# Distances computed exactly by code_distance.py and committed here rather than
# recomputed on every import. The enumeration is exhaustive, so these are the
# distances, not bounds. Two reasons a code appears here:
#
#   self-dual-bbcode  the dataset ships `d: -1` — no distance at all.
#   defect-5/-7       the dataset's declared d is the nominal lattice distance,
#                     not the distance of the matrices it ships. Both have a
#                     weight-2 X-logical — and it is the file's own second
#                     `logical_xs` entry, supports {1,8} and {2,11}. Storing 5
#                     and 7 would make the library's [[n,k,d]] contradict the
#                     `h` printed beside it.
DISTANCE = {
    "self-dual-bbcode": 6,
    "defect-5": 2,
    "defect-7": 2,
}

# Two dataset codes that are one stored code: at d=3 both colour-code lattices
# are the Steane code, so all six schedules land on `steane-code`. They are not
# six copies of three circuits — the two lattices give different check bases and
# so different tick structures, and depth alone separates them. Without the
# lattice in the name the three names collide and the second import overwrites
# the first, publishing three schedules where the dataset has six.
LATTICE = {
    "color-hex-3": "the 6.6.6 lattice",
    "color-oct-3": "the 4.8.8 lattice",
}

# A one-line flag where the stored distance will not match the one a reader
# finds in the paper. The reasoning belongs in this README, not on 56 circuit
# pages.
DISTANCE_NOTE = {
    "defect-5": "Stored d=2, not the source's 5: one of its own logical X operators has weight 2.",
    "defect-7": "Stored d=2, not the source's 7: one of its own logical X operators has weight 2.",
    "self-dual-bbcode": "Stored d=6, computed exactly; the source gives none.",
}

# Qubit permutations (sigma[new] = old) onto stored codes whose automorphism
# group defeats the dedup search's budget. Computed once by find_sigma.py and
# verified on every import by add_circuit's row-space check; see README.
SIGMA = (
    json.loads((HERE / "sigma_precomputed.json").read_text())
    if (HERE / "sigma_precomputed.json").exists()
    else {}
)


@dataclass
class Code:
    """One entry of the dataset's `qecc/` directory."""

    key: str
    n: int
    k: int
    d: int
    family: str
    h: np.ndarray  # symplectic, (m, 2n)
    logical: np.ndarray  # symplectic, (2k, 2n)
    dropped: list[int] = field(default_factory=list)


def load_code(path: Path) -> Code:
    """Read a `qecc/<name>.json` into symplectic matrices.

    Two things this must not take at face value:

    * **The Pauli type comes from the string, not the field name.**
      `self-dual-bbcode.json` has the two fields swapped — `x_stabilizers` holds
      Z-strings — and the dataset's own code reads the character, so everything
      downstream of it is self-consistent. Reading the key would silently build
      the wrong matrices.
    * **A qubit in no stabilizer is not part of the code.** The two defect codes
      each carry one (index 12 and 20): the stabilizer group gives k = 3 where
      the file declares k = 2, and neither logical touches the qubit. It is
      dropped and the remaining qubits are renumbered, which is a relabeling of
      the schedule and nothing more.
    """
    doc = json.loads(path.read_text())
    stabilizers = doc["x_stabilizers"] + doc["z_stabilizers"]
    n = doc["n"]

    live = sorted({q for s in stabilizers for q in range(n) if s[q] != "I"})
    dropped = [q for q in range(n) if q not in set(live)]

    def rows(strings: list[str]) -> np.ndarray:
        if not strings:
            return np.zeros((0, 2 * len(live)), dtype=int)
        return np.array(
            [
                [1 if s[q] in ("X", "Y") else 0 for q in live]
                + [1 if s[q] in ("Z", "Y") else 0 for q in live]
                for s in strings
            ],
            dtype=int,
        )

    return Code(
        key=path.stem,
        n=len(live),
        k=doc["k"],
        d=doc["d"],
        family=doc["family"],
        h=rows(stabilizers),
        logical=np.vstack([rows(doc["logical_xs"]), rows(doc["logical_zs"])]),
        dropped=dropped,
    )


def load_schedule(path: Path, code: Code, original_n: int) -> list[list[tuple[int, int, str]]]:
    """Read a schedule, renumbering around any dropped qubit.

    The ancilla block starts at `original_n` in the dataset and at `code.n` here,
    so both halves shift when a qubit is dropped.
    """
    shift = {q: q - sum(1 for d in code.dropped if d < q) for q in range(original_n)}
    ticks = []
    for tick in json.loads(path.read_text()):
        ticks.append(
            [
                (
                    shift[chk["data"]],
                    code.n + (chk["ancilla"] - original_n),
                    chk["pauli"],
                )
                for chk in tick
            ]
        )
    return ticks


def presentation(method: str, key: str) -> tuple[str, list[str]]:
    """Circuit name and tags for a scheduling method."""
    lattice = f" on {LATTICE[key]}" if key in LATTICE else ""
    if method.startswith("alpha-"):
        label, slug = DECODER[method.split("-", 1)[1]]
        return (
            f"AlphaSyndrome schedule ({label}){lattice}",
            ["syndrome-extraction", "schedule:alpha", f"decoder:{slug}"],
        )
    if method == "baseline":
        return (
            f"Depth-optimal schedule{lattice}",
            ["syndrome-extraction", "schedule:depth-optimal"],
        )
    return (
        f"{method.capitalize()} schedule{lattice}",
        ["syndrome-extraction", f"schedule:{method}"],
    )


def notes_for(code: Code) -> str:
    """Only what the page does not already say.

    The name gives the method and decoder, the tags repeat them, `depth` is the
    tick count and `source` is the paper — so none of that belongs here. What is
    left is the scope (one round, not a memory experiment), the qubit layout a
    reader needs to use it, and where we depart from the source.
    """
    lines = [
        "One syndrome-extraction round.",
        f"Data qubits 0-{code.n - 1}, then the ancillas (X-checks first), measured in index order.",
        "Hadamards once per X-ancilla, not per check (equivalent).",
    ]
    if code.key in LATTICE:
        lines.append(
            f"Scheduled on {LATTICE[code.key]}; at d=3 that colour code is the Steane code, "
            "which is why it is filed here."
        )
    if code.dropped:
        which = ", ".join(str(q) for q in code.dropped)
        lines.append(f"Source qubit {which} is in no stabilizer and is dropped.")
    if code.key in DISTANCE_NOTE:
        lines.append(DISTANCE_NOTE[code.key])
    return " ".join(lines)


def owns_slug(slug: str, code: Code) -> bool:
    """True when `slug` is free, or already holds *this* code.

    `canonical_hash` of the submitted (Hx, Hz) is what `add_circuit` records on
    the code entry, so comparing it identifies an entry this import wrote on an
    earlier run — which must not be mistaken for a collision with someone else's
    code, or the importer would stop being re-runnable.
    """
    path = REPO / "data_yaml" / "codes" / f"{slug}.yaml"
    if not path.exists():
        return True
    stored = yaml.safe_load(path.read_text())
    Hx, Hz = split_h_to_css(code.h, code.n)
    return stored.get("canonical_hash") == canonical_hash(Hx, Hz)


@dataclass
class Outcome:
    code: str
    method: str
    status: str  # "imported" | "invalid" | "excluded" | "error"
    detail: str = ""


def run(dataset: Path, write: bool, only: str) -> list[Outcome]:
    qecc = dataset / "qecc"
    if not qecc.is_dir():
        raise SystemExit(f"no qecc/ directory under {dataset} — pass --dataset")

    out: list[Outcome] = []
    for code_path in sorted(qecc.glob("*.json")):
        key = code_path.stem
        folder = qecc / key
        if not folder.is_dir():
            continue  # a code with no schedules
        if only and only not in key:
            continue
        if key in EXCLUDED_CODES:
            out.append(Outcome(key, "*", "excluded", EXCLUDED_CODES[key]))
            continue

        original_n = json.loads(code_path.read_text())["n"]
        code = load_code(code_path)
        if key in DISTANCE:
            code.d = DISTANCE[key]
        name, zoo, tags = FAMILY[code.family]
        sigma = SIGMA.get(key, {}).get("sigma")
        slug = f"{code.n}-{code.k}-{code.d}"

        # `assume_new` tells add_circuit to skip the dedup check, so nothing
        # downstream would notice that the slug belongs to an unrelated stored
        # code — and `overwrite=True` would replace it. Refuse instead: a code
        # we have *proved* is not the stored one must not be filed under its
        # slug. An entry an earlier run of this import wrote is not that case,
        # so the guard compares canonical hashes rather than merely testing for
        # the file — re-running has to stay idempotent.
        if key in ASSUME_NEW and not owns_slug(slug, code):
            out.append(Outcome(key, "*", "error", f"slug {slug} is taken by another code"))
            continue

        for schedule_path in sorted(folder.glob("*.json")):
            method = schedule_path.stem
            ticks = load_schedule(schedule_path, code, original_n)
            circuit = build_se_round(ticks, code.n)

            verdict = validate_syndrome_extraction_h(circuit, code.h, code.n, logical=code.logical)
            if verdict != "passed":
                out.append(Outcome(key, method, "invalid", verdict.removeprefix("failed: ")))
                continue

            circuit_name, circuit_tags = presentation(method, key)
            if not write:
                out.append(Outcome(key, method, "imported", f"{len(ticks)} ticks, dry run"))
                continue

            try:
                result = add_circuit(
                    circuit=circuit,
                    circuit_name=circuit_name,
                    d=code.d,
                    H=code.h,
                    n=code.n,
                    source=SOURCE,
                    code_name=name,
                    code_slug=slug,
                    code_tags=tags,
                    zoo_url=zoo,
                    tool=TOOL,
                    tags=circuit_tags,
                    notes=notes_for(code),
                    qubit_permutation=sigma,
                    assume_new=key in ASSUME_NEW,
                    overwrite=True,
                )
            except UncertainDedupError as e:
                out.append(Outcome(key, method, "error", f"uncertain dedup: {e.candidates}"))
                continue
            except Exception as e:  # noqa: BLE001 — report and keep going
                out.append(Outcome(key, method, "error", f"{type(e).__name__}: {e}"))
                continue
            out.append(
                Outcome(
                    key,
                    method,
                    "imported",
                    f"{result.code_slug} [{result.code_status}] #{len(result.files_written)} files",
                )
            )
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default=str(DATASET), help="clone of acasta-yhliu/asyndrome")
    parser.add_argument("--write", action="store_true", help="write into data_yaml/")
    parser.add_argument("--only", default="", help="restrict to codes whose key contains this")
    args = parser.parse_args()

    results = run(Path(args.dataset), args.write, args.only)
    for r in results:
        print(f"  {r.status:9s} {r.code:24s} {r.method:28s} {r.detail}")

    counts: dict[str, int] = {}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1
    print("\n" + ", ".join(f"{v} {k}" for k, v in sorted(counts.items())))
    if not args.write:
        print("Dry run — pass --write to import.")
    else:
        print(
            "\nNext: uv run python scripts/annotate_circuits.py && "
            # Re-import carries over only `qec_id`, so every measured
            # `circuit-distance:` tag on these circuits is gone. The script
            # strips and re-measures, so this restores them.
            "uv run python scripts/measure_circuit_distance.py --write && "
            "npm run format && "
            "npm run validate:yaml && npm run validate:circuits && npm run db:create"
        )
    return 1 if counts.get("error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
