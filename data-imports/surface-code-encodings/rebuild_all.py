#!/usr/bin/env python
"""Surface code unitary Pauli-state encodings (arXiv:2601.05113).

Imports the unitary state-preparation circuits from "Unitary fault-tolerant
encoding of Pauli states in surface codes" (Colmenarez, Zen, Olle, Marquardt &
Müller). See README.md for the dataset layout, fit strategies and decisions.

Only the *clean* *unitary* circuits are imported: the dataset's
`measurement_encoding/` circuits and its 900 `noisy_circuits/` are out of scope.

Usage:
  python rebuild_all.py                      # classify only (no writes)
  python rebuild_all.py --write              # import into the repo's data_yaml
  python rebuild_all.py --write --data-dir /tmp/dt
  python rebuild_all.py --only rotated       # substring filter on spec.key
  python rebuild_all.py --dataset PATH       # dataset clone elsewhere
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DATASET = REPO.parent / "surface_code_encodings"
sys.path.insert(0, str(REPO))

import stim  # noqa: E402

from scripts.add_circuit import (  # noqa: E402
    derive_matrices_two_circuit,
    import_state_prep,
)
from scripts.add_circuit.code_identify import build_symplectic_h  # noqa: E402
from scripts.add_circuit.matrix_format import decode as decode_matrix  # noqa: E402
from scripts.add_circuit.yaml_helpers import load_yaml  # noqa: E402

SOURCE = "https://arxiv.org/abs/2601.05113"
DISTANCES = (3, 5, 7, 9, 11)
CODE_TAGS = ["CSS", "surface-code", "topological"]

# sigma[new] = old, mapping this paper's labeling onto the stored code's.
# Only needed where a stored code already exists (rotated d<=9); new codes adopt
# the paper's labeling. d=3/d=5 came from find_code_permutation; d=7/d=9 defeat
# it (automorphism-rich) and are supplied externally. See README.
SIGMA = json.loads((HERE / "sigma_precomputed.json").read_text())


@dataclass(frozen=True)
class Code:
    slug: str
    name: str
    n: int  # data qubits (ancillas live at indices >= n)
    d: int
    rotated: bool
    stored: bool  # True: fit onto an existing code via SIGMA. False: seed it.
    zoo_url: str


def _code(rotated: bool, d: int) -> Code:
    if rotated:
        return Code(
            slug=f"rotated-surface-code-d-{d}",
            name="Rotated Surface Code",
            n=d * d,
            d=d,
            rotated=True,
            stored=d <= 9,  # d=11 is not in the library yet
            zoo_url="https://errorcorrectionzoo.org/c/rotated_surface",
        )
    return Code(
        slug=f"unrotated-surface-code-d-{d}",
        name="Unrotated Surface Code",
        n=d * d + (d - 1) * (d - 1),
        d=d,
        rotated=False,
        stored=False,  # no unrotated surface codes in the library yet
        zoo_url="https://errorcorrectionzoo.org/c/surface",
    )


CODES: dict[tuple[bool, int], Code] = {
    (rot, d): _code(rot, d) for rot in (True, False) for d in DISTANCES
}


@dataclass(frozen=True)
class Spec:
    key: str
    code: Code
    ancilla: bool  # True: ancilla-mediated (bridge qubits). False: direct.
    state: str  # "Z" -> |0>_L, "X" -> |+>_L  (the dataset's folder name)


def specs() -> list[Spec]:
    out = []
    for rot in (True, False):
        for d in DISTANCES:
            for ancilla in (True, False):
                for state in ("Z", "X"):
                    prefix = "rotated" if rot else "unrotated"
                    variant = "ancilla" if ancilla else "direct"
                    out.append(
                        Spec(
                            key=f"{prefix}-d{d}-{variant}-{state}",
                            code=CODES[(rot, d)],
                            ancilla=ancilla,
                            state=state,
                        )
                    )
    return out


def source_path(spec: Spec) -> Path:
    code_dir = "rotated_surface_code" if spec.code.rotated else "unrotated_surface_code"
    infix = "" if spec.code.rotated else "unrotated_"
    suffix = "with_ancilla" if spec.ancilla else "without_ancilla"
    return (
        DATASET
        / "clean_circuits"
        / code_dir
        / f"unitary_encoding_{suffix}"
        / spec.state
        / f"unitary_encoding_{infix}{spec.state}_L{spec.code.d}_{suffix}.stim"
    )


def prep_body(text: str) -> str:
    """The unitary preparation, in library-convention form.

    Two transformations:

    * Drop the terminal logical readout (M/MX on every data qubit, its DETECTORs
      and OBSERVABLE_INCLUDE). That is the paper's SPAM benchmark for figures 5
      and 9, not part of the encoding — same call as the flag-at-origin import.
    * Rewrite the reset layer: RX -> H, R dropped (|0...0> is implicit in a
      stored body). This also drops the qubits some files reset but never use,
      which would otherwise inflate qubit_count by up to 2x.

    QUBIT_COORDS is kept (the unrotated files carry the lattice layout; the
    rotated files ship none), but only for qubits the preparation actually
    touches. The files declare a coordinate for every grid site, including ones
    named solely in the dropped reset layer, and a QUBIT_COORDS target counts
    towards stim's num_qubits — so keeping all of them would put the inflated
    qubit_count straight back (unrotated d=3 direct: 25 rather than 13).
    """
    src = stim.Circuit(text)
    coords = src.get_final_qubit_coordinates()

    out = stim.Circuit()
    for inst in src.flattened():
        if inst.name in ("M", "MX", "DETECTOR", "OBSERVABLE_INCLUDE", "R", "QUBIT_COORDS"):
            continue
        if inst.name == "RX":
            out.append("H", [t.value for t in inst.targets_copy()])
            continue
        out.append(inst)

    used = out.num_qubits
    keep = {q: c for q, c in coords.items() if q < used and c}
    if not keep:
        return str(out)
    head = stim.Circuit()
    for q, c in sorted(keep.items()):
        head.append("QUBIT_COORDS", [q], c)
    return str(head + out)


def anchor_for(code: Code) -> np.ndarray:
    """Symplectic H for `code`, in the labeling the fit expects.

    Stored codes: the library's own `h`, so the supplied sigma maps onto it.
    New codes: derived from this paper's own |0>_L / |+>_L pair via the
    two-circuit method (Hx from |0>_L, Hz from |+>_L), which needs no external
    stabilizer definitions -- the dataset shipping both states is what makes
    that possible for these non-self-dual codes.

    Derivation always uses the *direct* circuits: `strip_flags` would drop the
    ancilla-mediated variant's bridge gates and derive the wrong code. Both
    variants share a data labeling, so one anchor serves all four circuits.
    """
    if code.stored:
        doc = load_yaml((REPO / "data_yaml" / "codes" / f"{code.slug}.yaml").read_text())
        return decode_matrix(doc["h"])
    zero = prep_body(source_path(Spec("", code, False, "Z")).read_text())
    plus = prep_body(source_path(Spec("", code, False, "X")).read_text())
    Hx, Hz = derive_matrices_two_circuit(zero, plus, code.n)
    return build_symplectic_h(Hx, Hz)


def gate_set_of(circ: stim.Circuit) -> str:
    names = sorted({i.name for i in circ if i.name not in ("TICK", "QUBIT_COORDS")})
    return ",".join(names)


def describe(spec: Spec) -> tuple[str, list[str], str]:
    """(circuit_name, tags, notes) for one spec."""
    state_word = "zero" if spec.state == "Z" else "plus"
    ket = "|0>_L" if spec.state == "Z" else "|+>_L"
    variant = "Ancilla-mediated" if spec.ancilla else "Direct"
    name = f"{variant} {state_word} prep"

    # Protected error type follows the state: the fault distance is preserved
    # only for the error that flips the codeword (X for |0>_L, Z for |+>_L).
    flipping = "X" if spec.state == "Z" else "Z"
    complementary = "Z" if spec.state == "Z" else "X"
    routing = (
        "ancillas bridge the data qubits, so gates stay nearest-neighbour"
        if spec.ancilla
        else "gates act directly between data qubits, needing next-nearest-neighbour links"
    )

    # One clause on the construction, one on the partial fault tolerance. The
    # rest -- depth, gate counts, why the terminal readout is dropped -- is
    # either already a schema field or belongs in the import README, not on
    # every circuit page.
    notes = (
        f"Unitary 'stabilizer-expanding' preparation of {ket} ({routing}). "
        f"Partially fault-tolerant: fault distance = d={spec.code.d} for "
        f"{flipping} errors, bounded for {complementary}"
    )  # no trailing '.': _build_notes joins parts with '. '

    tags = [
        "state-preparation",
        "partial-ft",
        f"distance:{spec.code.d}",
    ]
    return name, tags, notes


def run(write: bool, data_dir: Path, only: str | None) -> None:
    chosen = [s for s in specs() if not only or only in s.key]
    imported = deferred = 0
    report: list[str] = []
    anchors: dict[str, np.ndarray] = {}

    for spec in chosen:
        code = spec.code
        sigma = SIGMA.get(code.slug) if code.stored else None
        if code.stored and sigma is None:
            report.append(f"DEFER {spec.key}: no sigma for stored code {code.slug} (see README)")
            deferred += 1
            continue

        if code.slug not in anchors:
            anchors[code.slug] = anchor_for(code)

        path = source_path(spec)
        text = path.read_text()
        name, tags, notes = describe(spec)
        kwargs = dict(
            circuit=prep_body(text),
            n=code.n,
            d=code.d,
            method="anchor",
            anchor_H=anchors[code.slug],
            # None for new codes: the circuit-to-anchor fit confirms identity.
            # add_circuit still canonicalizes the new code afterwards and
            # relabels the circuit to match -- see README.
            permutation=sigma,
            code_name="" if code.stored else code.name,
            code_slug="" if code.stored else code.slug,
            code_tags=None if code.stored else CODE_TAGS,
            zoo_url="" if code.stored else code.zoo_url,
            circuit_name=name,
            source=SOURCE,
            source_file=str(path.relative_to(DATASET)),
            logical_state="zero" if spec.state == "Z" else "plus",
            connectivity="2d-grid",
            gate_set=gate_set_of(stim.Circuit(prep_body(text))),
            ancilla_role="routing",
            tags=tags,
            notes=notes,
            data_dir=str(data_dir),
            dry_run=not write,
        )
        try:
            import_state_prep(**kwargs)
            imported += 1
        except Exception as e:  # noqa: BLE001
            report.append(f"FAIL {spec.key}: {type(e).__name__}: {str(e).splitlines()[0][:90]}")
            deferred += 1

    verb = "imported" if write else "classified"
    print(f"{verb}={imported} deferred={deferred} (of {len(chosen)} selected)")
    for line in report:
        print("  " + line)


def main() -> None:
    global DATASET
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--data-dir", default=str(REPO / "data_yaml"))
    ap.add_argument("--dataset", default=str(DATASET))
    ap.add_argument("--only", default=None, help="substring filter on spec.key")
    args = ap.parse_args()
    DATASET = Path(args.dataset)
    if not DATASET.is_dir():
        raise SystemExit(f"dataset not found: {DATASET} (clone it there, or pass --dataset)")
    run(args.write, Path(args.data_dir), args.only)


if __name__ == "__main__":
    main()
