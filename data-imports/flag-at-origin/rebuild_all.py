#!/usr/bin/env python
"""Flag-at-origin FT state-preparation import (arXiv:2508.14200).

Imports the fault-tolerant logical |0>_L preparation circuits from
Quantinuum/flag_at_origin_paper into the QECirc library. The circuits ship as
pytket ``Circuit.to_dict()`` JSON inside ``Notebook_1.zip``; each is a full SPAM
benchmark (prep + flag verification + terminal logical-Z readout). We keep the
prep + flag verification and drop the terminal readout, matching how the other
FT state-prep circuits are stored.

Code check matrices ("anchors") come from the authors' own stabiliser
definitions, lifted verbatim into ``stabilizers.py`` — deriving them from a
|0>_L circuit alone is impossible for non-self-dual codes (you only recover
<stabilisers, logical-Z>). See README.md for the dataset layout and decisions.

Usage:
  python rebuild_all.py                    # classify only (no writes)
  python rebuild_all.py --write            # import into data_yaml
  python rebuild_all.py --dataset PATH     # path holding Notebook_1.zip
  python rebuild_all.py --only 49-1-9      # restrict to codes whose spec.key matches
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DATASET = REPO.parent / "flag_at_origin_paper"  # clone of the paper repo
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

import stim  # noqa: E402
from anchors import anchor_for  # noqa: E402
from convert import dict_to_stim, load_pytket_dict  # noqa: E402

from scripts.add_circuit import import_state_prep  # noqa: E402
from scripts.add_circuit.matrix_format import decode as decode_matrix  # noqa: E402

SOURCE = "https://arxiv.org/abs/2508.14200"
TOOL = "flag-at-origin"

# QEC Zoo links + family tags for the identified new codes (see README).
ZOO_SURFACE = "https://errorcorrectionzoo.org/c/rotated_surface"
ZOO_COLOR = "https://errorcorrectionzoo.org/c/488_color"
ZOO_QR = "https://errorcorrectionzoo.org/c/galois_quad_residue"
ZOO_TRIORTHOGONAL = "https://errorcorrectionzoo.org/c/triorthogonal"
SURFACE_TAGS = ["CSS", "surface-code", "topological"]
COLOR_TAGS = ["CSS", "self-dual", "color-code", "topological"]

# Precomputed qubit permutations (sigma[new] = old) mapping the flag-at-origin
# labelling onto the stored color codes, for the two automorphism-rich codes
# where the pipeline's structural finder is too slow to run each import.
# Produced once with find_code_permutation() (see README). Empty until computed.
SIGMA = (
    json.loads((HERE / "sigma_precomputed.json").read_text())
    if (HERE / "sigma_precomputed.json").exists()
    else {}
)


@dataclass
class Spec:
    key: str  # short id for --only / reporting
    fname: str  # member name inside Notebook_1.zip (without the "Notebook_1/" prefix)
    n: int
    k: int
    d: int
    circuit_name: str
    mode: str  # "std" (auto-dedup or new code) | "perm" (existing, precomputed sigma)
    code_name: str = ""  # proposed name if the code is new (ignored on dedup)
    code_tags: list[str] = field(default_factory=lambda: ["CSS", "stabilizer"])
    code_slug: str = ""  # explicit slug for a new code (default: derived from name)
    zoo_url: str = ""  # QEC Zoo link for a new code
    logical_state: str = "zero"  # "zero" (|0>_L / |0..0>_L) or "plus" (|+>_L)
    slug: str = ""  # stored slug for mode="perm"
    # Base-new codes whose [[n,k]] params collide with a stored code (a false
    # "uncertain" dedup — the canonical hashes differ). Variants stay False so
    # they dedup by exact hash onto the base code created earlier in the run.
    assume_new: bool = False


# One entry per circuit file. [[63,45,4]] is intentionally out of scope: no
# stabiliser definition exists in the source repo, and it can't be recovered
# from a |0>_L circuit (k=45).
SPECS: list[Spec] = [
    # --- existing codes (auto-dedup; the proposed code_name is ignored on match) ---
    Spec(
        "7-1-3",
        "SteaneCode.json",
        7,
        1,
        3,
        "FT zero (flag at origin)",
        "std",
        code_name="Steane Code",
    ),
    Spec(
        "9-1-3",
        "Code_[[9,1,3]].json",
        9,
        1,
        3,
        "FT zero (flag at origin)",
        "std",
        code_name="[[9,1,3]] Code",
    ),
    Spec(
        "23-1-7",
        "GolayCode.json",
        23,
        1,
        7,
        "FT zero (flag at origin)",
        "std",
        code_name="Quantum Golay Code",
    ),
    # --- existing color codes needing a precomputed permutation ---
    Spec(
        "17-1-5",
        "SeventeenColorCode.json",
        17,
        1,
        5,
        "FT zero (flag at origin)",
        "perm",
        slug="17-1-5",
    ),
    Spec(
        "31-1-7",
        "Code_[[31,1,7]].json",
        31,
        1,
        7,
        "FT zero (flag at origin)",
        "perm",
        slug="31-1-7",
    ),
    # --- new codes (base codes: assume_new to bypass false-collision dedup) ---
    # Identities from the paper repo's own comments + stabiliser-weight structure
    # + QEC Zoo; the three [[20,2,6]] / [[49,1,5]] / [[95,1,7]] have no known name.
    Spec(
        "20-2-6",
        "TwentyDist6Code.json",
        20,
        2,
        6,
        "FT zero (flag at origin)",
        "std",
        code_name="[[20,2,6]] Code",
        code_slug="20-2-6",
        code_tags=["CSS", "self-dual", "stabilizer"],
        assume_new=True,
    ),
    # [[25,1,5]] is the d=5 rotated surface code (verified with find_code_permutation),
    # so both variants dedup onto the stored rotated-surface-code-d-5 via a precomputed
    # permutation — NOT a new code.
    Spec(
        "25-1-5",
        "Code_[[25,1,5]].json",
        25,
        1,
        5,
        "FT zero (flag at origin)",
        "perm",
        slug="rotated-surface-code-d-5",
    ),
    Spec(
        "25-1-5-F",
        "Code_[[25,1,5]]F.json",
        25,
        1,
        5,
        "FT zero (flag at origin, variant F)",
        "perm",
        slug="rotated-surface-code-d-5",
    ),
    # [[49,1,5]] and [[95,1,7]] are triorthogonal codes and the paper prepares
    # |+>_L for them (Table I), not |0>_L.
    Spec(
        "49-1-5-plus",
        "Code_[[49,1,5]]+.json",
        49,
        1,
        5,
        "FT plus (flag at origin, variant +)",
        "std",
        code_name="Triorthogonal Code",
        code_slug="49-1-5",
        code_tags=["CSS", "triorthogonal", "stabilizer"],
        zoo_url=ZOO_TRIORTHOGONAL,
        logical_state="plus",
        assume_new=True,
    ),
    Spec(
        "49-1-5-F",
        "Code_[[49,1,5]]F.json",
        49,
        1,
        5,
        "FT plus (flag at origin, variant F)",
        "std",
        code_name="Triorthogonal Code",
        code_slug="49-1-5",
        code_tags=["CSS", "triorthogonal", "stabilizer"],
        zoo_url=ZOO_TRIORTHOGONAL,
        logical_state="plus",
    ),
    Spec(  # 7x7 rotated surface code (paper comment "#7x7 surface")
        "49-1-7",
        "Code_[[49,1,7]].json",
        49,
        1,
        7,
        "FT zero (flag at origin)",
        "std",
        code_name="Rotated Surface Code",
        code_slug="rotated-surface-code-d-7",
        code_tags=SURFACE_TAGS,
        zoo_url=ZOO_SURFACE,
        assume_new=True,
    ),
    Spec(  # 9x9 4.8.8 colour code (paper comment "#9x9 color")
        "49-1-9",
        "Code_[[49,1,9]].json",
        49,
        1,
        9,
        "FT zero (flag at origin)",
        "std",
        code_name="4.8.8 Color Code",
        code_slug="49-1-9",
        code_tags=COLOR_TAGS,
        zoo_url=ZOO_COLOR,
        assume_new=True,
    ),
    Spec(  # 9x9 rotated surface code (paper comment "#9x9 surface")
        "81-1-9",
        "Code_[[81,1,9]].json",
        81,
        1,
        9,
        "FT zero (flag at origin)",
        "std",
        code_name="Rotated Surface Code",
        code_slug="rotated-surface-code-d-9",
        code_tags=SURFACE_TAGS,
        zoo_url=ZOO_SURFACE,
        assume_new=True,
    ),
    Spec(  # 11x11 4.8.8 colour code (paper comment "#11x11 color")
        "71-1-11",
        "Code_[[71,1,11]].json",
        71,
        1,
        11,
        "FT zero (flag at origin)",
        "std",
        code_name="4.8.8 Color Code",
        code_slug="71-1-11",
        code_tags=COLOR_TAGS,
        zoo_url=ZOO_COLOR,
        assume_new=True,
    ),
    Spec(  # quantum quadratic-residue code (self-dual, uniform weight-12)
        "47-1-11",
        "Code_[[47,1,11]].json",
        47,
        1,
        11,
        "FT zero (flag at origin)",
        "std",
        code_name="Quantum Quadratic-Residue Code",
        code_slug="47-1-11",
        code_tags=["CSS", "self-dual"],
        zoo_url=ZOO_QR,
        assume_new=True,
    ),
    Spec(
        "95-1-7",
        "Code_[[95,1,7]]+.json",
        95,
        1,
        7,
        "FT plus (flag at origin)",
        "std",
        code_name="Triorthogonal Code",
        code_slug="95-1-7",
        code_tags=["CSS", "triorthogonal", "stabilizer"],
        zoo_url=ZOO_TRIORTHOGONAL,
        logical_state="plus",
        assume_new=True,
    ),
]


def read_circuit(zf: zipfile.ZipFile, fname: str) -> dict:
    return load_pytket_dict(zf.read(f"Notebook_1/{fname}").decode())


def prep_body(circuit_dict: dict, n: int) -> tuple[str, dict]:
    """STIM prep body: full circuit minus the terminal logical-Z readout of the
    data qubits (0..n-1). Flag/ancilla measurements are kept."""
    text, ndata, anc, meta = dict_to_stim(circuit_dict)
    if ndata != n:
        raise ValueError(f"data-qubit count {ndata} != expected n={n}")
    c = stim.Circuit(text)
    out = stim.Circuit()
    for instr in c:
        if instr.name == "M":
            keep = [t.value for t in instr.targets_copy() if t.value >= n]
            if keep:
                out.append("M", keep)
        else:
            out.append(
                instr.name,
                [t.value for t in instr.targets_copy()],
                instr.gate_args_copy(),
            )
    return str(out) + "\n", meta


def import_one(spec: Spec, zf: zipfile.ZipFile, write: bool, data_dir: str) -> str:
    d = read_circuit(zf, spec.fname)
    body, _ = prep_body(d, spec.n)
    # Conceptual note only; the pipeline appends source_file / logical_state /
    # connectivity / gate_set / flag qubits / permutation from the kwargs below.
    ket = "+" if spec.logical_state == "plus" else "0"
    notes = (
        f"Fault-tolerant |{ket}>_L preparation via the 'flag at origin' construction "
        "(arXiv:2508.14200). Flag-verification measurements are included "
        "(post-selection); the terminal data-qubit readout of the SPAM benchmark "
        "is not part of the prep."
    )
    tags = [
        "state-preparation",
        "ft",
        "flag",
        f"logical-state:{spec.logical_state}",
        f"distance:{spec.d}",
    ]
    kw = dict(
        circuit=body,
        n=spec.n,
        d=spec.d,
        circuit_name=spec.circuit_name,
        method="anchor",
        source=SOURCE,
        tool=TOOL,
        source_file=f"Notebook_1/{spec.fname}",
        logical_state=spec.logical_state,
        connectivity="all-to-all",
        gate_set="CX,H,M",
        tags=tags,
        notes=notes,
        data_dir=data_dir,
        dry_run=not write,
    )
    if spec.mode == "perm":
        import yaml  # noqa: PLC0415

        sH = decode_matrix(
            yaml.safe_load((Path(data_dir) / "codes" / f"{spec.slug}.yaml").read_text())["h"]
        )
        sigma = SIGMA.get(spec.slug)
        if sigma is None:
            return f"DEFER {spec.key}: no precomputed sigma for {spec.slug}"
        kw.update(code_name="", anchor_H=sH, permutation=sigma)
    else:
        H, _ = anchor_for(spec.n, spec.k, spec.d)
        # Always pass a code_name: the pipeline needs it to seed a new code, and
        # ignores it when the submission dedups onto an existing stored code.
        kw.update(
            anchor_H=H,
            code_name=spec.code_name,
            code_slug=spec.code_slug,
            code_tags=spec.code_tags,
            zoo_url=spec.zoo_url,
            assume_new=spec.assume_new,
        )
    try:
        r = import_state_prep(**kw)
        return (
            f"OK   {spec.key:12s} -> code={r.code_slug} ({r.code_status}) circuit={r.circuit_slug}"
        )
    except Exception as e:  # noqa: BLE001
        return f"FAIL {spec.key:12s} {type(e).__name__}: {str(e).splitlines()[0][:90]}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dataset", default=str(DATASET))
    ap.add_argument("--data-dir", default=str(REPO / "data_yaml"))
    ap.add_argument("--only", default=None, help="substring filter on spec.key")
    args = ap.parse_args()

    zip_path = Path(args.dataset) / "Notebook_1.zip"
    if not zip_path.exists():
        sys.exit(f"Notebook_1.zip not found at {zip_path} — clone Quantinuum/flag_at_origin_paper")

    specs = [s for s in SPECS if not args.only or args.only in s.key]
    with zipfile.ZipFile(zip_path) as zf:
        for spec in specs:
            print(import_one(spec, zf, args.write, args.data_dir), flush=True)
    print(f"\n{'wrote' if args.write else 'classified'} {len(specs)} circuits.")


if __name__ == "__main__":
    main()
