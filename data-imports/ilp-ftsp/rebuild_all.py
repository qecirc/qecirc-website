#!/usr/bin/env python
"""ILP flag-based FT state-preparation import (arXiv:2607.22498).

Imports the fault-tolerant state-preparation circuits from Criger, Hankin,
Burau & Perry, "Automated Flag-based Fault-Tolerant State Preparation using
Integer Linear Programming" (arXiv:2607.22498) into the QECirc library.

The paper ships no machine-readable circuits; the STIM bodies in ``circuits/``
were extracted from the paper sources (qpic input preserved in the tikz
figures' comments for 10 circuits; vector extraction of the three hand-edited
figure PDFs for [[24,4,5]], [[42,10,6]] and [[23,1,7]]) and validated against
the paper's stabilizer tableaux — see README.md for the full provenance and
validation story.

Check-matrix anchors come from the paper's own appendix (``anchors.py``), in
the paper's qubit labeling, which is also each circuit's labeling — so anchor
fits are the identity.  Fits onto *stored* codes use precomputed permutations
(``sigma_precomputed.json``) where the structural search is too slow to run
per-import; each cached sigma is re-verified by the pipeline's row-space check
at import time.

Usage:
  python rebuild_all.py                    # classify only (no writes)
  python rebuild_all.py --write            # import into data_yaml
  python rebuild_all.py --only 24-4-5      # restrict to specs whose key matches
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

import yaml  # noqa: E402
from anchors import ANCHORS  # noqa: E402

from scripts.add_circuit import import_state_prep  # noqa: E402

SOURCE = "https://arxiv.org/abs/2607.22498"

ZOO_SURFACE = "https://errorcorrectionzoo.org/c/rotated_surface"
ZOO_2BGA = "https://errorcorrectionzoo.org/c/2bga"
SURFACE_TAGS = ["CSS", "surface-code", "topological"]
TBGA_TAGS = ["CSS", "LDPC", "stabilizer"]

SIGMA = (
    json.loads((HERE / "sigma_precomputed.json").read_text())
    if (HERE / "sigma_precomputed.json").exists()
    else {}
)


@dataclass
class Spec:
    key: str
    fname: str  # stem in circuits/
    n: int
    k: int
    d: int
    circuit_name: str
    method: str  # "self_dual" | "anchor"
    detects: int  # fault-detection order claimed by the paper's figure caption
    anchor: str = ""  # ANCHORS key (method="anchor" with a paper/constructed anchor)
    slug: str = ""  # stored slug: anchor becomes the stored code's h + sigma
    code_name: str = ""
    code_slug: str = ""
    code_tags: list[str] = field(default_factory=lambda: ["CSS", "stabilizer"])
    zoo_url: str = ""
    logical_state: str = "zero"
    assume_new: bool = False


# Import order matters only for the two [[16,4,4]] codes (the twisted color
# code claims the plain 16-4-4 slug first; the low-weight code is provably a
# different code — X-span weight enumerators {0:1,4:4,8:54,12:4,16:1} vs
# {0:1,6:16,8:30,10:16,16:1} — so it is assume_new) and for the two
# [[24,10,4]] circuits (the |+> prep dedups onto the code its |0> twin creates).
SPECS: list[Spec] = [
    # --- existing codes ----------------------------------------------------
    Spec(
        "12-2-4",
        "12_2_4_prep",
        12,
        2,
        4,
        "FT zero (ILP flags)",
        "anchor",
        detects=2,
        slug="carbon-code",
    ),
    Spec(
        "16-2-4",
        "16_2_4_prep",
        16,
        2,
        4,
        "FT zero (ILP flags)",
        "self_dual",
        detects=2,
        slug="16-2-4",
    ),
    Spec(
        "16-6-4",
        "16_6_4_prep",
        16,
        6,
        4,
        "FT zero (ILP flags)",
        "self_dual",
        detects=2,
        slug="16-6-4",
    ),
    Spec(
        "17-1-5",
        "17_1_5_prep",
        17,
        1,
        5,
        "FT zero (ILP flags)",
        "self_dual",
        detects=2,
        slug="17-1-5",
    ),
    Spec(
        "20-2-6",
        "20_2_6_prep",
        20,
        2,
        6,
        "FT zero (ILP flags)",
        "self_dual",
        detects=3,
        slug="20-2-6",
    ),
    Spec(  # auto-dedup: the canonical-hash ladder resolves the Golay permutation
        "23-1-7",
        "23_1_7_prep",
        23,
        1,
        7,
        "FT zero (ILP flags)",
        "self_dual",
        detects=3,
        code_name="Quantum Golay Code",
    ),
    # --- new codes ---------------------------------------------------------
    Spec(
        "16-1-4",
        "16_1_4_prep",
        16,
        1,
        4,
        "FT zero (ILP flags)",
        "anchor",
        detects=2,
        anchor="16-1-4",
        code_name="Rotated Surface Code",
        code_slug="rotated-surface-code-d-4",
        code_tags=SURFACE_TAGS,
        zoo_url=ZOO_SURFACE,
    ),
    Spec(  # [[16,4,4]] color code of Prabhu & Reichardt (arXiv:2112.03785)
        "16-4-4",
        "16_4_4_8_prep",
        16,
        4,
        4,
        "FT zero (ILP flags)",
        "self_dual",
        detects=2,
        code_name="Twisted Color Code",
        code_slug="16-4-4",
        code_tags=["CSS", "self-dual", "color-code", "stabilizer"],
    ),
    Spec(  # weight-six [[16,4,4]] derived in the paper from the [[16,6,4]] RM code
        "16-4-4-low-weight",
        "16_4_4_6_prep",
        16,
        4,
        4,
        "FT zero (ILP flags)",
        "anchor",
        detects=2,
        anchor="16-4-4-low-weight",
        code_name="[[16,4,4]] Low-Weight Code",
        code_slug="16-4-4-low-weight",
        code_tags=["CSS", "self-dual", "stabilizer"],
        assume_new=True,
    ),
    Spec(
        "24-10-4",
        "24_10_4_prep",
        24,
        10,
        4,
        "FT zero (ILP flags)",
        "anchor",
        detects=2,
        anchor="24-10-4",
        code_name="Two-Block Group Algebra Code",
        code_slug="24-10-4",
        code_tags=TBGA_TAGS,
        zoo_url=ZOO_2BGA,
    ),
    Spec(
        "24-10-4-plus",
        "24_10_4_plus_prep",
        24,
        10,
        4,
        "FT plus (ILP flags)",
        "anchor",
        detects=2,
        anchor="24-10-4",
        code_name="Two-Block Group Algebra Code",
        code_slug="24-10-4",
        code_tags=TBGA_TAGS,
        zoo_url=ZOO_2BGA,
        logical_state="plus",
    ),
    Spec(
        "24-4-5",
        "24_4_5_prep",
        24,
        4,
        5,
        "FT zero (ILP flags)",
        "anchor",
        detects=3,
        anchor="24-4-5",
        code_name="Two-Block Group Algebra Code",
        code_slug="24-4-5",
        code_tags=TBGA_TAGS,
        zoo_url=ZOO_2BGA,
    ),
    Spec(
        "42-10-6",
        "42_10_6_prep",
        42,
        10,
        6,
        "FT zero (ILP flags)",
        "anchor",
        detects=3,
        anchor="42-10-6",
        code_name="Two-Block Group Algebra Code",
        code_slug="42-10-6",
        code_tags=TBGA_TAGS,
        zoo_url=ZOO_2BGA,
    ),
]


def stored_h(slug: str, data_dir: str) -> np.ndarray:
    d = yaml.safe_load((Path(data_dir) / "codes" / f"{slug}.yaml").read_text())
    h = d["h"]
    if isinstance(h, dict):  # sparse storage
        H = np.zeros((h["rows"], 2 * d["n"]), dtype=int)
        for i, cols in enumerate(h["data"]):
            H[i, cols] = 1
        return H
    return np.array(h, dtype=int)


def import_one(spec: Spec, write: bool, data_dir: str) -> str:
    body = (HERE / "circuits" / f"{spec.fname}.stim").read_text()
    ket = "+" if spec.logical_state == "plus" else "0"
    src_kind = (
        "figure PDF (vector extraction)"
        if spec.fname in ("24_4_5_prep", "42_10_6_prep", "23_1_7_prep")
        else "tikz figure (embedded qpic source)"
    )
    notes = (
        f"Fault-tolerant |{ket}>_L preparation with flag circuits constructed by "
        "integer linear programming (arXiv:2607.22498). Flag/verification "
        f"measurements are included (post-selection); the paper's figure caption "
        f"states all fault sets up to size {spec.detects} are detected or lead to "
        f"post-selection later in the QEC gadget. Circuit recovered from the "
        f"paper's {src_kind} and validated against the code's stabilizers"
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
        method=spec.method,
        source=SOURCE,
        source_file=f"data-imports/ilp-ftsp/circuits/{spec.fname}.stim",
        logical_state=spec.logical_state,
        connectivity="all-to-all",
        gate_set="CX,H,M",
        tags=tags,
        notes=notes,
        data_dir=data_dir,
        dry_run=not write,
    )
    if spec.slug:  # existing stored code
        sigma = SIGMA.get(spec.slug)
        if sigma is None:
            return f"DEFER {spec.key}: no precomputed sigma for {spec.slug}"
        kw.update(code_name="", permutation=sigma)
        if spec.method == "anchor":
            kw.update(anchor_H=stored_h(spec.slug, data_dir))
    else:  # new code
        kw.update(
            code_name=spec.code_name,
            code_slug=spec.code_slug,
            code_tags=spec.code_tags,
            zoo_url=spec.zoo_url,
            assume_new=spec.assume_new,
        )
        if spec.method == "anchor":
            kw.update(anchor_H=ANCHORS[spec.anchor])
    try:
        r = import_state_prep(**kw)
        written.extend(r.files_written or [])
        return (
            f"OK   {spec.key:18s} -> code={r.code_slug} ({r.code_status}) circuit={r.circuit_slug}"
        )
    except Exception as e:  # noqa: BLE001
        return f"FAIL {spec.key:18s} {type(e).__name__}: {str(e).splitlines()[0][:100]}"


written: list[str] = []


def renumber(base: int) -> None:
    """Shift the qec_ids of the circuit YAMLs written in this run so they start
    at ``base`` (ascending, preserving relative order).

    Used to allocate ids above the ranges already claimed by open import PRs:
    qec_ids are permanent and never reused, so parallel PRs must not both take
    max+1 (gaps are fine, collisions are not).
    """
    import re

    files = sorted(
        {f for f in written if "/circuits/" in f and f.endswith(".yaml") and "originals" not in f}
    )
    ids = []
    for f in files:
        m = re.search(r"(?m)^qec_id:\s*(\d+)\s*$", Path(f).read_text())
        ids.append((int(m.group(1)), f))
    for i, (_, f) in enumerate(sorted(ids)):
        text = Path(f).read_text()
        text = re.sub(r"(?m)^qec_id:\s*\d+\s*$", f"qec_id: {base + i}", text)
        Path(f).write_text(text)
    print(f"renumbered {len(ids)} circuits to qec_id {base}..{base + len(ids) - 1}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--data-dir", default=str(REPO / "data_yaml"))
    ap.add_argument("--only", default=None, help="substring filter on spec.key")
    ap.add_argument(
        "--qec-id-base",
        type=int,
        default=None,
        help="renumber this run's new circuits to start at this qec_id "
        "(to allocate above ranges claimed by open PRs)",
    )
    args = ap.parse_args()

    specs = [s for s in SPECS if not args.only or args.only in s.key]
    for spec in specs:
        print(import_one(spec, args.write, args.data_dir), flush=True)
    print(f"\n{'wrote' if args.write else 'classified'} {len(specs)} circuits.")
    if args.write and args.qec_id_base is not None:
        renumber(args.qec_id_base)


if __name__ == "__main__":
    main()
