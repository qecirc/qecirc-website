#!/usr/bin/env python
"""
Full RLFTQC import: add every circuit (excluding *_flag.stim) to the QECirc
library, anchoring each to a stored code in data_yaml and fitting it by a qubit
permutation.

All 9 codes now live in data_yaml (the 4 once seeded from MQT — shor, tetrahedral,
rotated-surface d3/d5 — were added upstream in #78), so this script only fits and
imports circuits; it does not seed codes.

Each circuit is fitted by a qubit permutation:
  identity  ->  a known supplied permutation  ->  an exhaustive search (n <= 9).
The permutation is verified by row-space equality (add_circuit's override), so it
works for automorphism-rich codes. Provenance (connectivity, device, gate set,
qubit placement, logical state, permutation) is captured in notes/tags.

Usage:
  python rebuild_all.py                 # classify only (no writes)
  python rebuild_all.py --write         # import into the repo's data_yaml
  python rebuild_all.py --write --data-dir /tmp/dt   # write elsewhere
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]  # .../qecirc-website
DATASET = REPO.parent / "RLFTQC Circuits"  # dataset sits beside the repo
sys.path.insert(0, str(REPO))

import stim  # noqa: E402

from scripts.add_circuit import (  # noqa: E402
    fit_circuit_to_anchor_h,
    fit_circuit_to_candidates,
    import_state_prep,
)
from scripts.add_circuit.matrix_format import decode as decode_matrix  # noqa: E402

SOURCE = "https://arxiv.org/abs/2402.17761"


@dataclass
class Code:
    n: int
    d: int
    slug: str  # stored code slug in data_yaml/codes/ to anchor circuits to
    known_perms: tuple[tuple[int, ...], ...] = ()  # sigma[new]=old candidates


# Every code is now present in data_yaml (the 4 that used to be seeded from MQT
# were added upstream in #78). Circuits are anchored to the stored definitions and
# fitted by qubit permutation. For n<=9 the fit is found by an exhaustive search;
# larger codes rely on `known_perms` (found once — see data-imports/rlftqc/README).
CODES: dict[str, Code] = {
    "5-1-3": Code(5, 3, "five-qubit-code"),
    "7-1-3": Code(7, 3, "steane-code"),
    "17-1-5": Code(
        17, 5, "17-1-5", known_perms=((0, 1, 4, 8, 12, 6, 7, 9, 13, 2, 3, 5, 16, 10, 11, 14, 15),)
    ),
    "19-1-5": Code(19, 5, "19-1-5"),
    "23-1-7": Code(23, 7, "23-1-7"),
    "9-1-3-shor": Code(9, 3, "shor-code"),  # identity fits main's shor-code
    "9-1-3-surface": Code(9, 3, "rotated-surface-code-d-3"),  # n<=9 search finds σ
    "15-1-3": Code(
        15, 3, "tetrahedral-code", known_perms=((7, 3, 11, 1, 9, 5, 13, 0, 8, 4, 12, 2, 10, 6, 14),)
    ),
    # [[25,1,5]] rotated surface: σ found with the structural permutation
    # finder (scripts.add_circuit.find_code_permutation, issue #80). The RL
    # circuit uses the MQT rotated_surface_d5 labeling; this maps it onto the
    # stored code.
    "25-1-5": Code(
        25,
        5,
        "rotated-surface-code-d-5",
        known_perms=(
            (
                8,
                18,
                24,
                2,
                12,
                21,
                6,
                16,
                22,
                17,
                13,
                0,
                10,
                5,
                1,
                20,
                15,
                9,
                4,
                19,
                14,
                23,
                11,
                7,
                3,
            ),
        ),
    ),
}


def family_of(path: Path) -> str | None:
    for part in path.parts:
        m = re.fullmatch(r"(\d+)-(\d+)-(\d+)(?:-(shor|surface|[a-z]+))?", part)
        if not m:
            continue
        n, d, suf = int(m.group(1)), int(m.group(3)), m.group(4)
        if suf in ("shor", "surface"):
            return f"{n}-1-{d}-{suf}"
        if n == 9:
            return "9-1-3-shor"
        return f"{n}-1-{d}"
    return None


def anchor_H(code: Code, data_dir: Path) -> np.ndarray:
    doc = yaml.safe_load((data_dir / "codes" / f"{code.slug}.yaml").read_text())
    return decode_matrix(doc["h"])


# --- metadata from the path -------------------------------------------------

_DEVICES = {"manila", "lima", "jakarta", "guadalupe", "tokyo"}


def meta_of(path: Path, n: int) -> dict:
    parts = path.relative_to(DATASET).parts
    section = parts[0]
    conn = next((p for p in parts if p in ("fully-connected", "2d-grid", "ibm")), None)
    if conn is None:
        # distance-5 and verification-circuit-synthesis have no connectivity
        # subfolder but are fully-connected per their section READMEs.
        fc = ("distance-5", "verification-circuit-synthesis")
        conn = "fully-connected" if section in fc else None
    device = None
    for p in parts:
        for dv in _DEVICES:
            if dv in p:
                device = dv
        if p == "2d-grid":
            device = "google-sycamore"
    # logical state from folder words
    joined = "/".join(parts).lower()
    state = None
    for w, s in [("zero", "zero"), ("plus", "plus"), ("minus", "minus"), ("one_logical", "one")]:
        if w in joined:
            state = s
    if state is None:
        # Per the section READMEs, unlabeled preps are |0> except the Shor code,
        # which is always prepared as |+>. Use the resolved family so device
        # variants (e.g. "9-1-3-guadalupe") are covered, not just literal folders.
        state = "plus" if family_of(path) == "9-1-3-shor" else "zero"
    ft = section != "logical-state-preparation"
    # qubit placement
    qp = path.parent / "qubit_place.txt"
    placement = qp.read_text().strip() if qp.exists() else None
    return dict(
        section=section, connectivity=conn, device=device, state=state, ft=ft, placement=placement
    )


def gate_set_of(circ: stim.Circuit) -> str:
    names = sorted({i.name for i in circ if i.name not in ("TICK", "QUBIT_COORDS")})
    return ",".join(names)


# --- fitting ----------------------------------------------------------------


# db codes that are self-dual CSS: their non-identity circuits resolve via
# add_circuit's canonical-hash dedup (method="self_dual"), no explicit sigma needed.
SELF_DUAL = {"steane-code", "17-1-5", "19-1-5", "23-1-7"}


def search_sigma(circuit_text: str, H: np.ndarray, n: int) -> list[int] | None:
    """Exhaustive (for n<=9) permutation search; None if not found in budget."""
    fit = fit_circuit_to_anchor_h(circuit_text, H, n, max_perms=400000)
    if fit.status == "identity":
        return list(range(n))
    if fit.status == "found":
        return fit.permutation
    return None


@dataclass
class Stats:
    identity: int = 0
    known: int = 0
    searched: int = 0
    failed: list[str] = field(default_factory=list)
    imported: int = 0


def short_name(fam: str, m: dict, counter: dict) -> str:
    """Short, per-code-unique circuit name: ``RL <conn> [<device>] <state> <idx>``.
    Full provenance (source path, permutation, placement) lives in the notes and
    the permanent ``#qec_id``. ``google-sycamore`` is dropped (implied by 2d-grid).
    Deterministic given the sorted iteration order, so re-runs are stable."""
    device = m["device"] if m["device"] and m["device"] != "google-sycamore" else None
    prefix = "RL " + " ".join(x for x in [m["connectivity"], device, m["state"]] if x)
    idx = counter[(fam, prefix)]
    counter[(fam, prefix)] += 1
    return f"{prefix} {idx}"


def run(write: bool, data_dir: Path, overwrite: bool = False) -> None:
    anchors = {k: anchor_H(c, data_dir) for k, c in CODES.items()}
    stims = sorted(p for p in DATASET.rglob("*.stim") if not p.name.endswith("_flag.stim"))
    per_code: dict[str, Stats] = defaultdict(Stats)
    name_counter: dict[tuple, int] = defaultdict(int)
    for p in stims:
        fam = family_of(p)
        if fam is None or fam not in CODES:
            continue
        code = CODES[fam]
        st = per_code[fam]
        txt = p.read_text()
        H = anchors[fam]
        rel = str(p.relative_to(DATASET))

        # Decide how to fit: identity/known-σ -> n<=9 search -> self-dual auto-dedup.
        method, sigma = "anchor", fit_circuit_to_candidates(txt, H, code.n, code.known_perms)
        if sigma is not None:
            if sigma == list(range(code.n)):
                st.identity += 1
            else:
                st.known += 1
        elif code.n <= 9:
            sigma = search_sigma(txt, H, code.n)
            if sigma is not None:
                st.searched += 1
        if sigma is None and code.slug in SELF_DUAL:
            method, st.searched = "self_dual", st.searched + 1  # auto-dedup by hash
        elif sigma is None:
            st.failed.append(rel)
            continue

        if not write:
            continue
        m = meta_of(p, code.n)
        circ = stim.Circuit(txt)
        try:
            # Pass the paper's folder label; import_state_prep keeps it for CSS
            # codes when the derived basis agrees, else uses the library basis and
            # notes the paper label (non-CSS codes always keep the paper label).
            kwargs = dict(
                circuit=txt,
                n=code.n,
                d=code.d,
                code_name="",
                circuit_name=short_name(fam, m, name_counter),
                method=method,
                source=SOURCE,
                tool="rlftqc",
                source_file=rel,
                logical_state=m["state"],
                connectivity=m["connectivity"],
                device=m["device"],
                gate_set=gate_set_of(circ),
                qubit_placement=m["placement"],
                tags=["state-preparation", "ft" if m["ft"] else "non-ft"],
                data_dir=str(data_dir),
                overwrite=overwrite,
            )
            if method == "anchor":
                kwargs.update(anchor_H=H, permutation=sigma)
            import_state_prep(**kwargs)
            st.imported += 1
        except Exception as e:  # noqa: BLE001
            st.failed.append(f"{rel}  ({type(e).__name__}: {str(e).splitlines()[0][:70]})")

    print(f"\n{'IMPORT' if write else 'CLASSIFY'} — {len(stims)} circuits\n" + "=" * 70)
    tot = defaultdict(int)
    for key in CODES:
        st = per_code.get(key)
        if not st:
            continue
        fit_n = st.identity + st.known + st.searched
        print(
            f"[[{CODES[key].n},1,{CODES[key].d}]] {key:16s} "
            f"identity={st.identity} known-σ={st.known} searched={st.searched} "
            f"{'imported=' + str(st.imported) if write else ''} FAIL={len(st.failed)}"
        )
        for f in st.failed:
            print(f"      FAIL {f}")
        tot["fit"] += fit_n
        tot["fail"] += len(st.failed)
        tot["imp"] += st.imported
    print("=" * 70)
    print(
        f"total fittable: {tot['fit']}   failed: {tot['fail']}"
        + (f"   imported: {tot['imp']}" if write else "")
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--data-dir", default=str(REPO / "data_yaml"))
    ap.add_argument(
        "--overwrite",
        action="store_true",
        help="replace already-imported circuits in place (data refresh), keeping qec_ids",
    )
    args = ap.parse_args()
    run(args.write, Path(args.data_dir), overwrite=args.overwrite)


if __name__ == "__main__":
    main()
