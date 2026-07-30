#!/usr/bin/env python
"""QUITS syndrome-extraction schedule import (arXiv:2504.02673).

Imports the syndrome-extraction *schedules* of mkangquantum/quits, the artifact
of "QUITS: A modular Qldpc code circUIT Simulator" (Quantum 9, 1931 (2025)).

Unlike the asyndrome dataset, QUITS ships no circuits: it is a generator, so this
importer calls it. `code.build_circuit(...)` returns a whole memory experiment;
one library circuit is the single syndrome-extraction round inside its `REPEAT`
block, normalised to the library's convention by `se_round` below.

Every import is gated on `validate_syndrome_extraction_h` — the round must
measure exactly the code's stabilizer group and preserve every stabilizer and
logical, checked against the *stored* code after any relabeling.

QUITS needs `stim>=1.13` and the project pins `stim>=1.15,<2`, so no separate
environment is needed — run it straight from the repository root:

  uv run --with 'quits==1.1.0' python data-imports/quits/rebuild_all.py
  uv run --with 'quits==1.1.0' python data-imports/quits/rebuild_all.py --write

  --dataset PATH   clone of mkangquantum/quits (only the shipped classical
                   parity-check matrices are read from it; the codes themselves
                   are constructed by the installed package)
  --only bpc       restrict to catalogue keys containing this string
"""

from __future__ import annotations

import argparse
import json
import os
import sys

# QUITS' edge colourings iterate over sets whose order depends on Python's
# per-process string hash seed, so the same code and strategy produce a
# *different* (equally valid) schedule on every run — verified: three runs, three
# circuits. Its own `seed=1` covers the random module and not this. Since hash
# randomisation is fixed before the interpreter starts, the only way to pin it
# from inside the script is to re-exec once with it set, which is what this does.
# Without it the committed circuits cannot be regenerated from the recorded
# command, which is the whole point of keeping the importer.
if os.environ.get("PYTHONHASHSEED") != "0":
    os.environ["PYTHONHASHSEED"] = "0"
    os.execv(sys.executable, [sys.executable, *sys.argv])
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import stim
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DATASET = REPO.parent / "quits"  # clone of the artifact repo
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from codes import FAMILY, FAMILY_PAPER, build_catalogue  # noqa: E402

from scripts.add_circuit import (  # noqa: E402
    UncertainDedupError,
    add_circuit,
    validate_syndrome_extraction_h,
)
from scripts.add_circuit.code_identify import canonical_hash  # noqa: E402

TOOL = "quits"

# The schedule is what is being published, so `source` is the paper that
# *defines the schedule*, not the paper that defines the code. Only `cardinal`
# and its N/S-merged variant are QUITS' own contribution.
QUITS_PAPER = "https://arxiv.org/abs/2504.02673"

# strategy -> (circuit name, source, tags, note)
# Source terminology lives in the name; the tag records the structural property
# a reader can filter on — whether X- and Z-checks share ticks or run in
# separate passes. Verified per circuit by `interleaves_xz` below, never assumed.
SCHEDULE = {
    "cardinal": (
        "Cardinal schedule",
        QUITS_PAPER,
        "Tanner edges split into cardinal directions, each direction edge-coloured.",
    ),
    "cardinalNSmerge": (
        "Cardinal schedule (N/S merged)",
        QUITS_PAPER,
        "As the cardinal schedule, with the north and south edges coloured together.",
    ),
    "zxcoloration": (
        "ZX-coloration schedule",
        "https://arxiv.org/abs/2308.08648",
        "Z-checks and X-checks in two separate edge-coloured passes.",
    ),
    "custom": (
        "Bivariate bicycle schedule",
        "https://arxiv.org/abs/2308.07915",
        "The seven-layer schedule built from the code's own six shift permutations.",
    ),
}

# Codes whose cheap invariants align with a stored code that is NOT the same
# code. Each one is refuted here rather than waved through: `assume_new` is only
# safe with a proof, and the proof is recorded next to the flag.
#
# Both are balanced-product cyclic codes colliding with an unrelated stored code
# that happens to share n and k.
ASSUME_NEW = {
    "bpc-36-8-4": (
        "Candidate 36-8-4 is a hyperbolic surface code. Its X- and Z-row-space "
        "ranks are 11 and 17; this code's are 14 and 14. Rank is a permutation "
        "invariant and an X<->Z swap gives 17/11, so no relabeling reconciles "
        "them. The exhaustive weight enumerators differ too (X-space: 18 words "
        "of weight 6 here, 12 there)."
    ),
    "bpc-108-8-8": (
        "Candidate 108-8-10 is a bivariate bicycle code of distance 10; this "
        "code has distance 8, and permutation-equivalent codes have equal "
        "distance. Independently, ISD sweeps find weight-8 codewords in this "
        "code's X row space and none in the stored code's."
    ),
    "bb-90-8-10": (
        'Candidate 90-8-10 carries the alias "(15,3) BB6 code" but is not this '
        "code: enumerating every weight-4 vector against each X row space gives "
        "0 codewords here and 90 there. The weight enumerator is a permutation "
        "invariant, so no relabeling reconciles them. This is Bravyi et al. "
        "Table 3's (15,3) entry, built from its own polynomials, and is the same "
        "code autqec imports as 90-8-10-autqec — hence the shared slug."
    ),
}

# Catalogue keys deliberately left out, with the reason recorded for the README.
EXCLUDED: dict[str, str] = {}

# Extra `seed` values to import beyond the default 1, per (catalogue key,
# strategy). The seed drives the edge orientation and colouring behind the two
# cardinal strategies — zxcoloration ignores it — so a different seed is a
# different schedule for the same checks, at identical depth and gate count.
#
# What it is *not* is free variety worth importing wholesale. A sweep of 12
# seeds over the five cardinal-family codes whose circuit distance is
# measurable (see scripts/measure_circuit_distance.py) found the default seed
# already at the best distance available everywhere except one, and the two
# lift-connected-surface codes produce only two distinct schedules however the
# seed is set. So this list holds the improvements and nothing else: a second
# circuit that measures the same as the first tells a reader nothing and costs
# them a row.
EXTRA_SEEDS: dict[tuple[str, str], tuple[int, ...]] = {
    # Circuit distance 4 — the code's own — against seed 1's 3, at the same
    # depth (8) and two-qubit count (216). Seed 7 is an equally good, different
    # schedule; one of the two is enough to make the point.
    ("bpc-36-8-4", "cardinal"): (2,),
}

# Qubit permutations (sigma[new] = old) onto stored codes whose automorphism
# group defeats the dedup search's budget. Not computed here: QUITS labels these
# codes exactly as autqec does (identical row spaces, verified), so these are the
# permutations that import derived. add_circuit re-verifies each one by row-space
# equality on every run, so a stale entry fails loudly rather than silently.
SIGMA = (
    json.loads((HERE / "sigma_precomputed.json").read_text())
    if (HERE / "sigma_precomputed.json").exists()
    else {}
)


# ---------------------------------------------------------------------------
# Turning a QUITS memory experiment into one canonical round
# ---------------------------------------------------------------------------


def se_round(circuit: stim.Circuit, data_qubits, check_qubits) -> stim.Circuit:
    """The single syndrome-extraction round inside a QUITS memory experiment.

    Two normalisations, both of them identities on a steady-state round:

    * **Qubit indices.** The library wants data `0..n-1` and ancillas `>= n`.
      Most QUITS strategies already do that, but `BbCode`'s `custom` schedule
      renumbers to X-checks, then data, then Z-checks
      (`BbCode._ensure_custom_qubit_indexing`), so the round is relabelled from
      the code object's own `data_qubits` / `check_qubits`.
    * **Reset placement.** `custom` ends its round on `MR`. The library's round
      begins with `R` and ends with `M`; rotating the reset from the end of one
      round to the start of the next is the same circuit repeated.

    Detectors and the observable are dropped: they belong to the memory
    experiment, and `annotate.build_annotated_se` rebuilds them from the code.
    """
    body = next(
        (item.body_copy() for item in circuit if isinstance(item, stim.CircuitRepeatBlock)),
        None,
    )
    if body is None:
        raise ValueError("no REPEAT block — not a memory experiment")

    n = len(data_qubits)
    relabel = {int(q): i for i, q in enumerate(data_qubits)}
    relabel.update({int(q): n + i for i, q in enumerate(check_qubits)})

    out = stim.Circuit()
    reset_at_end: list[list[stim.GateTarget]] = []
    for ins in body:
        if ins.name in ("DETECTOR", "OBSERVABLE_INCLUDE", "SHIFT_COORDS"):
            continue
        targets = [
            stim.GateTarget(relabel[t.value]) if t.is_qubit_target else t
            for t in ins.targets_copy()
        ]
        if ins.name == "MR":
            reset_at_end.append(targets)
            out.append("M", targets, ins.gate_args_copy())
        else:
            out.append(ins.name, targets, ins.gate_args_copy())

    if reset_at_end:
        head = stim.Circuit()
        for targets in reset_at_end:
            head.append("R", targets)
        head.append("TICK")
        out = head + out
    return out


def interleaves_xz(round_circuit: stim.Circuit, n: int) -> bool:
    """True when some tick carries both an X- and a Z-check.

    An ancilla is the *control* of an X-check and the *target* of a Z-check, so
    the check type is read off each two-qubit gate rather than assumed from the
    strategy name — which is what makes the resulting tag a measurement.
    """
    ticks: list[set[str]] = [set()]
    for ins in round_circuit:
        if ins.name == "TICK":
            ticks.append(set())
        elif ins.name in ("CX", "CZ"):
            for group in ins.target_groups():
                ticks[-1].add("X" if group[0].value >= n else "Z")
    return any(len(t) > 1 for t in ticks)


def symplectic(hx: np.ndarray, hz: np.ndarray) -> tuple[np.ndarray, int]:
    """CSS (Hx, Hz) as the symplectic `h` of shape (m, 2n)."""
    hx = np.asarray(hx, dtype=int) % 2
    hz = np.asarray(hz, dtype=int) % 2
    n = hx.shape[1]
    top = np.hstack([hx, np.zeros_like(hx)])
    bottom = np.hstack([np.zeros_like(hz), hz])
    return np.vstack([top, bottom]), n


def symplectic_logicals(lx: np.ndarray, lz: np.ndarray, n: int) -> np.ndarray:
    """CSS logicals as the symplectic `logical` of shape (2k, 2n)."""
    lx = np.asarray(lx, dtype=int) % 2
    lz = np.asarray(lz, dtype=int) % 2
    out = np.zeros((lx.shape[0] + lz.shape[0], 2 * n), dtype=int)
    out[: lx.shape[0], :n] = lx
    out[lx.shape[0] :, n:] = lz
    return out


def notes_for(spec, strategy: str, interleaved: bool) -> str:
    """Only what the circuit page does not already say.

    The name gives the schedule, `depth` is the tick count, `source` is the paper
    and the tags carry the structural class — so what is left is the scope (one
    round, not a memory experiment), the qubit layout, and any caveat on the
    stored parameters.
    """
    lines = [
        "One syndrome-extraction round.",
        SCHEDULE[strategy][2],
        f"Data qubits 0-{spec.n - 1}, then the ancillas (Z-checks first), measured in index order.",
        "X- and Z-checks share ticks."
        if interleaved
        else "X- and Z-checks run in separate passes.",
        f"Code construction: {FAMILY_PAPER[spec.family]}.",
    ]
    if spec.d_is_bound:
        lines.append(f"Stored d={spec.d} is the source's upper bound, not a proven distance.")
    elif spec.d_source:
        lines.append(f"Distance {spec.d} from {spec.d_source}.")
    return " ".join(lines)


def owns_slug(slug: str, code) -> bool:
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
    return stored.get("canonical_hash") == canonical_hash(
        np.asarray(code.hx, dtype=int) % 2, np.asarray(code.hz, dtype=int) % 2
    )


@dataclass
class Outcome:
    code: str
    strategy: str
    status: str  # "imported" | "invalid" | "excluded" | "error"
    detail: str = ""


def run(dataset: Path, write: bool, only: str, max_n: int = 0) -> list[Outcome]:
    out: list[Outcome] = []
    for spec in build_catalogue(dataset):
        if only and only not in spec.key:
            continue
        if max_n and spec.n > max_n:
            out.append(Outcome(spec.key, "*", "skipped", f"n={spec.n} exceeds --max-n {max_n}"))
            continue
        if spec.key in EXCLUDED:
            out.append(Outcome(spec.key, "*", "excluded", EXCLUDED[spec.key]))
            continue

        try:
            code = spec.build()
        except Exception as e:  # noqa: BLE001 — report and keep going
            out.append(Outcome(spec.key, "*", "error", f"build: {type(e).__name__}: {e}"))
            continue

        # The catalogue is transcribed by hand; refuse to import a code whose
        # shape does not match the row it claims to be.
        n_built, k_built = code.hx.shape[1], code.lx.shape[0]
        if (n_built, k_built) != (spec.n, spec.k):
            out.append(
                Outcome(
                    spec.key,
                    "*",
                    "error",
                    f"catalogue says [[{spec.n},{spec.k}]], built [[{n_built},{k_built}]]",
                )
            )
            continue

        h, n = symplectic(code.hx, code.hz)
        logical = symplectic_logicals(code.lx, code.lz, n)
        name, zoo, code_tags = FAMILY[spec.family]
        name = spec.name or name
        sigma = SIGMA.get(spec.key, {}).get("sigma")
        slug = spec.slug or f"{spec.n}-{spec.k}-{spec.d}"

        # `assume_new` tells add_circuit to skip the dedup check, so nothing
        # downstream will notice that the slug belongs to an unrelated stored
        # code — and `overwrite=True` would replace it. Refuse instead: a code
        # we have *proved* is not the stored one must not be filed under its
        # slug. An entry this import wrote on an earlier run is not that case,
        # so the guard compares canonical hashes rather than merely testing for
        # the file — re-running must stay idempotent.
        if spec.key in ASSUME_NEW and not owns_slug(slug, code):
            out.append(
                Outcome(
                    spec.key,
                    "*",
                    "error",
                    f"slug {slug} is taken by a different code; give this "
                    f"spec an explicit distinct slug in codes.py",
                )
            )
            continue

        for strategy in sorted(code.supported_strategies):
            base_name, source, _ = SCHEDULE[strategy]
            for seed in (1, *EXTRA_SEEDS.get((spec.key, strategy), ())):
                kind = strategy if seed == 1 else f"{strategy}:seed{seed}"
                # Seed 1 keeps the plain name: it is what QUITS builds by
                # default, so naming it after a seed would imply a choice
                # nobody made.
                circuit_name = base_name if seed == 1 else f"{base_name} (seed {seed})"
                try:
                    experiment = code.build_circuit(
                        strategy=strategy, num_rounds=2, basis="Z", seed=seed
                    )
                    circuit = se_round(experiment, code.data_qubits, code.check_qubits)
                except Exception as e:  # noqa: BLE001
                    out.append(Outcome(spec.key, kind, "error", f"{type(e).__name__}: {e}"))
                    continue

                verdict = validate_syndrome_extraction_h(circuit, h, n, logical=logical)
                if verdict != "passed":
                    out.append(Outcome(spec.key, kind, "invalid", verdict.removeprefix("failed: ")))
                    continue

                interleaved = interleaves_xz(circuit, n)
                tags = [
                    "syndrome-extraction",
                    "schedule:interleaved" if interleaved else "schedule:xz-separated",
                ]

                if not write:
                    out.append(
                        Outcome(spec.key, kind, "imported", f"{circuit.num_ticks} ticks, dry run")
                    )
                    continue

                try:
                    result = add_circuit(
                        circuit=circuit,
                        circuit_name=circuit_name,
                        d=spec.d,
                        # Pass the CSS pair, not the symplectic `h`. Both name the
                        # same code and produce the same canonical form and hash,
                        # but `H=` routes through `split_h_to_css`, which row-reduces
                        # to detect CSS structure and hands back an RREF basis — and
                        # that basis, not the submitted one, is what gets stored as
                        # the circuit's *original* matrices. For an LDPC code that
                        # turns weight-6 checks into weight-44 rows and throws away
                        # the low-weight structure the code is defined by.
                        Hx=code.hx,
                        Hz=code.hz,
                        source=source,
                        code_name=name,
                        code_slug=slug,
                        code_tags=code_tags,
                        zoo_url=zoo,
                        tool=TOOL,
                        tags=tags,
                        notes=notes_for(spec, strategy, interleaved),
                        qubit_permutation=sigma,
                        assume_new=spec.key in ASSUME_NEW,
                        overwrite=True,
                    )
                except UncertainDedupError as e:
                    out.append(Outcome(spec.key, kind, "error", f"uncertain dedup: {e.candidates}"))
                    continue
                except Exception as e:  # noqa: BLE001
                    out.append(Outcome(spec.key, kind, "error", f"{type(e).__name__}: {e}"))
                    continue
                out.append(
                    Outcome(
                        spec.key,
                        kind,
                        "imported",
                        f"{result.code_slug} [{result.code_status}]",
                    )
                )
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default=str(DATASET), help="clone of mkangquantum/quits")
    parser.add_argument("--write", action="store_true", help="write into data_yaml/")
    parser.add_argument("--only", default="", help="restrict to catalogue keys containing this")
    parser.add_argument(
        "--max-n",
        type=int,
        default=0,
        help="skip codes with more than this many physical qubits. The stored "
        "check matrix is (n-k) x 2n, and one copy is kept per circuit under "
        "circuits/originals/, so the footprint grows as n^2: the four QLP codes "
        "and the two large HGP codes are 90%% of the catalogue's disk cost.",
    )
    args = parser.parse_args()

    results = run(Path(args.dataset), args.write, args.only, args.max_n)
    for r in results:
        print(f"  {r.status:9s} {r.code:20s} {r.strategy:16s} {r.detail}")

    counts: dict[str, int] = {}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1
    print("\n" + ", ".join(f"{v} {k}" for k, v in sorted(counts.items())))
    if not args.write:
        print("Dry run — pass --write to import.")
    else:
        print(
            "\nNext: uv run python scripts/annotate_circuits.py && npm run format && "
            "npm run validate:yaml && npm run validate:circuits && npm run db:create"
        )
    return 1 if counts.get("error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
