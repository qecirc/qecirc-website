#!/usr/bin/env python
"""qLDPC circuit import (github.com/qLDPCOrg/qLDPC).

Imports three kinds of circuit from the qLDPC library:

* **syndrome extraction** — one round, from `get_memory_experiment_parts`, in
  each of the two edge-colouring strategies the library ships;
* **encoding** — `get_encoding_circuit`, synthesised from the code's tableau;
* **|0> preparation** — the same with `only_zero=True`.

qLDPC is a generator, not a dataset: it ships no circuits, so this importer
constructs each code and calls it. Every circuit is gated on the matching
validator before anything is written.

qLDPC needs `stim>=1.16` and this project pins `stim>=1.15,<2`, so no separate
environment is needed — run it from the repository root:

  uv run --with 'qldpc==0.3.2' python data-imports/qldpc/rebuild_all.py
  uv run --with 'qldpc==0.3.2' python data-imports/qldpc/rebuild_all.py --write

  --only surface   restrict to catalogue keys containing this string
  --kinds se       restrict to circuit kinds (comma-separated: se, encoding, prep)
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import stim
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from codes import CATALOGUE, FAMILY  # noqa: E402

from scripts.add_circuit import (  # noqa: E402
    UncertainDedupError,
    add_circuit,
    validate_encoding_h,
    validate_state_prep_h,
    validate_syndrome_extraction_h,
)
from scripts.add_circuit.code_identify import (  # noqa: E402
    canonical_hash,
    split_h_to_css,
)

TOOL = "qldpc"

# Qubit permutations (sigma[new] = old) onto stored codes whose symmetry defeats
# the dedup search's budget. Computed by find_sigma.py and re-verified by
# add_circuit on every run, so a stale entry fails loudly.
SIGMA = (
    json.loads((HERE / "sigma_precomputed.json").read_text())
    if (HERE / "sigma_precomputed.json").exists()
    else {}
)

# Both syndrome-measurement strategies implement Algorithm 1 of
# arXiv:2109.14609, so that paper — not the library — is the circuit's source.
# The encoders synthesise from the code's tableau and reproduce no published
# construction, so they name the tool instead, as `circuit-synth` circuits do.
EDGE_COLORING_PAPER = "https://arxiv.org/abs/2109.14609"
TOOL_SOURCE = "qldpc"

# Both strategies run the X-checks and Z-checks in separate passes; that is
# verified per circuit by `interleaves_xz`, never assumed from the name.
SE_STRATEGIES = {
    "edge-coloring": (
        "Edge-coloring schedule",
        "The Tanner graph's edges are greedily coloured and one colour runs per tick.",
    ),
    "edge-coloring-xz": (
        "Edge-coloring schedule (X/Z split)",
        "The X- and Z-check subgraphs are coloured separately, then run one colour per tick.",
    ),
}

# Upstream states this plainly for both strategies, in the class docstrings, and
# it is the honest distinction from the schedules imported from other sources —
# so it goes on the circuit page rather than being quietly dropped.
SE_CAVEAT = (
    "The library states this strategy is not guaranteed to be distance-preserving "
    "or fault-tolerant."
)

ENCODING_CAVEAT = (
    "Synthesised from the code's tableau, so it carries no flag qubits and no "
    "distance guarantee; the library states its encoders are not fault-tolerant."
)


def snippet(spec, call: str) -> str:
    """The qLDPC one-liner that rebuilds this circuit.

    Asked for by qLDPC's author (qLDPCOrg/qLDPC#554): a reader should be able to
    reproduce a circuit without reverse-engineering the constructor from
    [[n,k,d]]. `spec.constructor` is the expression this import actually
    evaluates, so the recorded line cannot drift from the circuit it describes.
    """
    return f"Reproduce with: {call.format(code=spec.constructor)}"


# Codes whose cheap invariants align with a stored code that is NOT the same
# code. `assume_new` is only safe with a proof, so the proof lives next to it.
ASSUME_NEW = {
    "toric-d4": (
        "Candidate 16-2-4 has the same n, k, d and row-space ranks, but a "
        "different code: the exhaustive weight enumerator of this code's X row "
        "space has 8 words of weight 4 and 16 of weight 6, where the stored "
        "code has 12 of weight 4 and none of weight 6. Weight enumerators are "
        "permutation invariants, and the Z spaces differ the same way, so no "
        "relabeling reconciles them."
    ),
}


def interleaves_xz(round_circuit: stim.Circuit, n: int) -> bool:
    """True when some tick carries both an X- and a Z-check.

    The check type is read off each two-qubit gate — an ancilla is the control of
    an X-check and the target of a Z-check — so the resulting tag is a
    measurement of the emitted circuit rather than a restatement of its name.
    """
    ticks: list[set[str]] = [set()]
    for ins in round_circuit:
        if ins.name == "TICK":
            ticks.append(set())
        elif ins.name in ("CX", "CY", "CZ"):
            for group in ins.target_groups():
                ticks[-1].add("X" if group[0].value >= n else "Z")
    return any(len(t) > 1 for t in ticks)


def se_round(qec_cycle: stim.Circuit) -> stim.Circuit:
    """The repeated round of a qLDPC memory experiment.

    qLDPC already emits data qubits `0..n-1` and ancillas above them, and its
    round is `RX` ancillas -> tick-separated CX/CZ layers -> `MX` ancillas, so
    only the detectors and observable have to come off: they belong to the
    memory experiment, and the `stim-annotated` view rebuilds them.
    """
    body = next(
        (item.body_copy() for item in qec_cycle if isinstance(item, stim.CircuitRepeatBlock)),
        None,
    )
    if body is None:
        raise ValueError("no REPEAT block in the QEC cycle")
    out = stim.Circuit()
    for ins in body:
        if ins.name not in ("DETECTOR", "OBSERVABLE_INCLUDE", "SHIFT_COORDS"):
            out.append(ins)
    return out


def owns_slug(slug: str, code) -> bool:
    """True when `slug` is free, or already holds *this* code.

    `canonical_hash` of the submitted (Hx, Hz) is what `add_circuit` records on
    the code entry, so comparing it identifies an entry this import wrote on an
    earlier run — which must not be mistaken for a collision with someone
    else's code, or the importer would stop being re-runnable.
    """
    path = REPO / "data_yaml" / "codes" / f"{slug}.yaml"
    if not path.exists():
        return True
    stored = yaml.safe_load(path.read_text())
    n = stored["n"]
    split = split_h_to_css(np.asarray(code.matrix, dtype=int) % 2, n)
    if split is None:  # non-CSS: assume_new is not used for any such code here
        return False
    return stored.get("canonical_hash") == canonical_hash(np.array(split[0]), np.array(split[1]))


@dataclass
class Outcome:
    code: str
    kind: str
    status: str  # "imported" | "invalid" | "unsupported" | "error"
    detail: str = ""


def report(outcome: Outcome) -> Outcome:
    """Print as we go. A full run takes minutes and constructs some large codes,
    so a silent wait makes a slow code indistinguishable from a hung one."""
    print(
        f"  {outcome.status:11s} {outcome.code:24s} {outcome.kind:20s} {outcome.detail}",
        flush=True,
    )
    return outcome


def run(write: bool, only: str, kinds: set[str]) -> list[Outcome]:
    from qldpc.circuits import (
        EdgeColoring,
        EdgeColoringXZ,
        get_encoding_circuit,
        get_memory_experiment_parts,
    )
    from qldpc.objects import Pauli

    strategies = {"edge-coloring": EdgeColoring(), "edge-coloring-xz": EdgeColoringXZ()}
    out: list[Outcome] = []

    for spec in CATALOGUE:
        if only and only not in spec.key:
            continue
        try:
            code = spec.build()
        except Exception as e:  # noqa: BLE001 — report and keep going
            detail = f"build: {type(e).__name__}: {e}"
            out.append(report(Outcome(spec.key, "*", "error", detail)))
            continue

        # n and k are free; the distance is not. qLDPC computes an exact distance
        # for every code here except the bivariate bicycle one, where the search
        # is a hard combinatorial problem and does not terminate in any useful
        # time — so that one's distance is taken from its source table instead
        # (see codes.py) and checked here only when `verify_d` says it is cheap.
        n, k = len(code), int(code.dimension)
        built = (n, k) if not spec.verify_d else (n, k, code.get_distance())
        expected = (spec.n, spec.k) if not spec.verify_d else (spec.n, spec.k, spec.d)
        if built != expected:
            out.append(
                report(
                    Outcome(
                        spec.key,
                        "*",
                        "error",
                        f"catalogue says {expected}, built {built}",
                    )
                )
            )
            continue

        # For a subsystem code `code.matrix` is the *gauge* group, and the
        # operators a circuit is checked against are the stabilizers — the
        # centre of it. Everything downstream (validators, dedup, the CSS split)
        # works on the stabilizer group, and the gauge group rides alongside so
        # k can be computed as n - rank(h) - gauge qubits instead of n - rank(h).
        subsystem = bool(getattr(code, "is_subsystem_code", False))
        gauge = np.asarray(code.matrix, dtype=int) % 2 if subsystem else None
        h = (
            np.asarray(code.get_stabilizer_ops(), dtype=int) % 2
            if subsystem
            else np.asarray(code.matrix, dtype=int) % 2
        )
        logical = np.asarray(code.get_logical_ops(), dtype=int) % 2
        name, zoo, code_tags = FAMILY[spec.family]
        sigma = SIGMA.get(spec.key, {}).get("sigma")

        # `matrix_x` / `matrix_z` are the code's own check matrices; `code.matrix`
        # is the symplectic view of the same thing. See the note at add_circuit.
        # A subsystem code always takes the symplectic path, and carries its
        # gauge group with it.
        if subsystem:
            css_or_h = {"H": h, "n": n, "gauge": gauge}
        elif not hasattr(code, "matrix_x"):
            css_or_h = {"H": h, "n": n}
        else:
            css_or_h = {
                "Hx": np.asarray(code.matrix_x, dtype=int) % 2,
                "Hz": np.asarray(code.matrix_z, dtype=int) % 2,
            }

        # `code_slug` names a *new* code. On a dedup match `add_circuit` files
        # under the stored slug and ignores this, on both the CSS and the
        # non-CSS path, so a spec that matches an existing entry leaves it
        # empty.
        slug = spec.slug or ""

        # `assume_new` skips the dedup check, so nothing downstream would notice
        # that the slug belongs to an unrelated stored code — and `overwrite=True`
        # would replace it. Refuse in that case. An entry this import wrote on an
        # earlier run is not that case, so the guard compares canonical hashes
        # rather than merely testing for the file: re-running must stay idempotent.
        if spec.key in ASSUME_NEW and not owns_slug(slug, code):
            out.append(
                report(
                    Outcome(
                        spec.key,
                        "*",
                        "error",
                        f"slug {slug} is taken by a different code; give this "
                        f"spec an explicit distinct slug in codes.py",
                    )
                )
            )
            continue

        def emit(kind: str, circuit, circuit_name, source, tags, notes) -> None:
            if not write:
                out.append(report(Outcome(spec.key, kind, "imported", "dry run")))
                return
            try:
                result = add_circuit(
                    circuit=circuit,
                    circuit_name=circuit_name,
                    d=spec.d,
                    # Prefer the CSS pair over the symplectic `h`. Both name the
                    # same code and give the same canonical form and hash, but
                    # `H=` routes through `split_h_to_css`, which row-reduces to
                    # detect CSS structure — and that RREF basis, not the
                    # submitted one, is then stored as the circuit's *original*
                    # matrices. For an LDPC code that replaces low-weight checks
                    # with dense rows, losing the structure the code is defined
                    # by. Non-CSS codes have no pair, so they keep the `H=` path.
                    **css_or_h,
                    source=source,
                    code_name=name,
                    code_slug=slug,
                    code_tags=code_tags,
                    zoo_url=zoo,
                    tool=TOOL,
                    tags=tags,
                    notes=notes,
                    qubit_permutation=sigma,
                    assume_new=spec.key in ASSUME_NEW,
                    overwrite=True,
                )
            except UncertainDedupError as e:
                detail = f"uncertain dedup: {e.candidates}"
                out.append(report(Outcome(spec.key, kind, "error", detail)))
                return
            except Exception as e:  # noqa: BLE001
                out.append(report(Outcome(spec.key, kind, "error", f"{type(e).__name__}: {e}")))
                return
            out.append(
                Outcome(spec.key, kind, "imported", f"{result.code_slug} [{result.code_status}]")
            )

        # --- syndrome extraction -------------------------------------------
        if "se" in kinds:
            rounds: dict[str, object] = {}
            for key, strategy in strategies.items():
                try:
                    parts = get_memory_experiment_parts(
                        code, Pauli.Z, num_rounds=2, syndrome_measurement_strategy=strategy
                    )
                    circuit = se_round(parts.qec_cycle)
                except ValueError as e:
                    # Memory experiments are CSS- and stabilizer-only upstream.
                    out.append(report(Outcome(spec.key, f"se:{key}", "unsupported", str(e))))
                    continue
                except Exception as e:  # noqa: BLE001
                    out.append(report(Outcome(spec.key, f"se:{key}", "error", repr(e)[:120])))
                    continue

                verdict = validate_syndrome_extraction_h(circuit, h, n, logical=logical)
                if verdict != "passed":
                    out.append(
                        Outcome(spec.key, f"se:{key}", "invalid", verdict.removeprefix("failed: "))
                    )
                    continue
                rounds[key] = circuit

            # Two strategies, sometimes one circuit. Colouring the X- and Z-check
            # subgraphs separately gives the joint colouring back, byte for byte,
            # whenever the Tanner graph is small enough that the joint one already
            # separates them — five codes here. Both are still stored: they are
            # different algorithms that happen to agree, and on 9 of the 14 codes
            # that carry both they do not (the toric [[16,2,4]] is depth 4 against
            # 9). Dropping one would file that agreement as if the library had only
            # ever had one strategy. Each says instead which other strategy landed
            # on the same round, so a reader is not left comparing two identical
            # pages and wondering what they missed.
            for key, circuit in rounds.items():
                body = str(circuit)
                twins = [
                    SE_STRATEGIES[other][0]
                    for other, c in rounds.items()
                    if other != key and str(c) == body
                ]
                circuit_name, blurb = SE_STRATEGIES[key]
                if twins:
                    blurb += (
                        " On this code the "
                        + " and ".join(f"{t!r}" for t in twins)
                        + " strategy produces the identical round — the two colourings "
                        "coincide when the Tanner graph is small enough, which is a "
                        "property of this code rather than of either strategy."
                    )

                interleaved = interleaves_xz(circuit, n)
                emit(
                    f"se:{key}",
                    circuit,
                    circuit_name,
                    EDGE_COLORING_PAPER,
                    [
                        "syndrome-extraction",
                        "schedule:interleaved" if interleaved else "schedule:xz-separated",
                    ],
                    " ".join(
                        [
                            "One syndrome-extraction round.",
                            blurb,
                            f"Data qubits 0-{n - 1}, then the ancillas, measured in "
                            "index order; every ancilla is prepared and read in the X basis.",
                            SE_CAVEAT,
                            snippet(
                                spec,
                                "qldpc.circuits.get_memory_experiment_parts({code}, "
                                "qldpc.objects.Pauli.Z, num_rounds=2, "
                                "syndrome_measurement_strategy=qldpc.circuits."
                                f"{type(strategies[key]).__name__}()).qec_cycle"
                                " — the body stored here is that cycle's REPEAT block with"
                                " the detectors and observable removed, since they belong to"
                                " the memory experiment rather than to the round.",
                            ),
                        ]
                    ),
                )

        # --- encoding and |0> preparation ------------------------------------
        for kind, only_zero, circuit_name, tags in (
            ("encoding", False, "Tableau encoding", ["encoding", "non-ft"]),
            (
                "prep",
                True,
                "Tableau |0> preparation",
                ["state-preparation", "non-ft", "logical-state:zero"],
            ),
        ):
            if kind not in kinds:
                continue
            try:
                circuit = get_encoding_circuit(code, only_zero=only_zero)
            except Exception as e:  # noqa: BLE001
                out.append(report(Outcome(spec.key, kind, "error", repr(e)[:120])))
                continue

            check = validate_state_prep_h if only_zero else validate_encoding_h
            verdict = check(circuit, h, n)
            if verdict != "passed":
                reason = verdict.removeprefix("failed: ")
                out.append(report(Outcome(spec.key, kind, "invalid", reason)))
                continue

            emit(
                kind,
                circuit,
                circuit_name,
                TOOL_SOURCE,
                tags,
                " ".join(
                    [
                        "Prepares the logical |0> state."
                        if only_zero
                        else f"Encodes {k} logical qubits; the first {k} qubits are the input.",
                        ENCODING_CAVEAT,
                        snippet(
                            spec,
                            "qldpc.circuits.get_encoding_circuit({code}"
                            + (", only_zero=True)" if only_zero else ")"),
                        ),
                    ]
                ),
            )

    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write into data_yaml/")
    parser.add_argument("--only", default="", help="restrict to catalogue keys containing this")
    parser.add_argument(
        "--kinds",
        default="se,encoding,prep",
        help="comma-separated circuit kinds to import",
    )
    args = parser.parse_args()

    results = run(args.write, args.only, set(args.kinds.split(",")))
    for r in results:
        print(f"  {r.status:11s} {r.code:24s} {r.kind:20s} {r.detail}")

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
