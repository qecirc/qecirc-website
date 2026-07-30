#!/usr/bin/env python
"""MQT FT state-prep import: eval/ (arXiv:2408.11894) + eval_det/ (arXiv:2501.05527).

Imports the published fault-tolerant state-preparation circuits from the
munich-quantum-toolkit/qecc repository into the QECirc library. See README.md
for the dataset layout, fit strategies, and known deferred files.

Usage:
  python rebuild_all.py                  # classify only (no writes)
  python rebuild_all.py --write          # import into the repo's data_yaml
  python rebuild_all.py --write --data-dir /tmp/dt
  python rebuild_all.py --only eval      # restrict to one part (eval|det)
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DATASET = REPO.parent / "mqt-qecc"  # clone of munich-quantum-toolkit/qecc
EVAL = DATASET / "scripts/ft_stateprep/eval/circuits"
EVAL_DET = DATASET / "scripts/ft_stateprep/eval_det"
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

import stim  # noqa: E402

from scripts.add_circuit import (  # noqa: E402
    find_code_permutation,
    import_state_prep,
)
from scripts.add_circuit.code_identify import split_h_to_css  # noqa: E402
from scripts.add_circuit.matrix_format import decode as decode_matrix  # noqa: E402

SOURCE_EVAL = "https://arxiv.org/abs/2408.11894"
SOURCE_DET = "https://arxiv.org/abs/2501.05527"

# Files that are defective in the source repo (verified 2026-07-04; see README).
DEFECTIVE = {
    "rotated_surface_d3/zero_non_ft_heuristic.stim",  # truncated mid-verification
    "hamming/plus_ft_heuristic_opt.stim",  # prepared state violates a Z-stabilizer
}


@dataclass
class EvalCode:
    slug: str  # stored code slug in data_yaml/codes/
    n: int
    d: int
    fit: str  # "identity" | "search" | "self_dual" | "perm_find"
    mqt_dir: str = ""  # matrices dir under DATASET/src/mqt/qecc/codes/ (perm_find)


EVAL_CODES: dict[str, EvalCode] = {
    "steane": EvalCode("steane-code", 7, 3, "identity"),
    "shor": EvalCode("shor-code", 9, 3, "identity"),
    "rotated_surface_d3": EvalCode("rotated-surface-code-d-3", 9, 3, "search"),
    "rotated_surface_d5": EvalCode(
        "rotated-surface-code-d-5", 25, 5, "perm_find", "rotated_surface_d5"
    ),
    # hamming has plus-state circuits; self-dual derivation only works from a
    # |0> circuit, so fit via the structural finder against MQT's matrices.
    "hamming": EvalCode("15-7-3", 15, 3, "perm_find", "hamming_15"),
    "tetrahedral": EvalCode("tetrahedral-code", 15, 3, "perm_find", "tetrahedral"),
    "carbon": EvalCode("carbon-code", 12, 4, "perm_find", "carbon"),
    "cc_4_8_8": EvalCode("17-1-5", 17, 5, "self_dual"),
    "cc_6_6_6": EvalCode("19-1-5", 19, 5, "self_dual"),
    "cc_4_8_8_d7": EvalCode("31-1-7", 31, 7, "self_dual"),
}


def anchor_h(slug: str, data_dir: Path) -> np.ndarray:
    doc = yaml.safe_load((data_dir / "codes" / f"{slug}.yaml").read_text())
    return decode_matrix(doc["h"])


def sigma_for(mqt_dir: str, slug: str, n: int, data_dir: Path) -> list[int] | None:
    """Compute sigma (sigma[new]=old) once per code via the structural finder."""
    hx1 = np.load(DATASET / "src/mqt/qecc/codes" / mqt_dir / "hx.npy").astype(int)
    hz1 = np.load(DATASET / "src/mqt/qecc/codes" / mqt_dir / "hz.npy").astype(int)
    hx2, hz2 = split_h_to_css(anchor_h(slug, data_dir), n)
    return find_code_permutation(hx1, hz1, np.asarray(hx2), np.asarray(hz2))


def eval_name(fname: str) -> tuple[str, list[str], str]:
    """Parse an eval filename into (display name, tags, notes fragment)."""
    stem = fname.removesuffix(".stim")
    state = "zero" if stem.startswith("zero") else "plus"
    rest = stem.removeprefix(f"{state}_")
    if rest.startswith("non_ft_"):
        prep = rest.removeprefix("non_ft_")
        return (
            f"Non-FT {state} ({prep})",
            ["state-preparation", "non-ft", f"prep:{prep}"],
            f"Non-FT state preparation, synthesis method: {prep}",
        )
    rest = rest.removeprefix("ft_")
    parts = rest.split("_")
    if len(parts) == 1:  # e.g. zero_ft_naive
        verify = parts[0]
        return (
            f"FT {state} ({verify})",
            ["state-preparation", "ft", f"verification:{verify}"],
            f"FT state preparation with {verify} verification (post-selection)",
        )
    prep, verify = parts[0], parts[1]
    return (
        f"FT {state} ({prep}/{verify})",
        ["state-preparation", "ft", f"prep:{prep}", f"verification:{verify}"],
        f"FT state preparation (prep synthesis: {prep}, verification synthesis: "
        f"{verify}); verification measurements included, post-selection protocol",
    )


def gate_set_of(circ: stim.Circuit) -> str:
    names = sorted({i.name for i in circ if i.name not in ("TICK", "QUBIT_COORDS")})
    return ",".join(names)


def run_eval(write: bool, data_dir: Path, overwrite: bool = False) -> tuple[int, int]:
    report: list[str] = []
    imported = deferred = 0
    for dirname, code in EVAL_CODES.items():
        h = anchor_h(code.slug, data_dir)
        sigma: list[int] | None = None
        if code.fit == "perm_find":
            sigma = sigma_for(code.mqt_dir, code.slug, code.n, data_dir)
            if sigma is None:
                n_files = len(list((EVAL / dirname).glob("*.stim")))
                report.append(f"DEFER all {dirname} ({n_files}): permutation not found")
                deferred += n_files
                continue
        for path in sorted((EVAL / dirname).glob("*.stim")):
            rel = f"{dirname}/{path.name}"
            if rel in DEFECTIVE:
                report.append(f"DEFER {rel}: defective in source (see README)")
                deferred += 1
                continue
            txt = path.read_text()
            name, tags, method_note = eval_name(path.name)
            state = "zero" if path.name.startswith("zero") else "plus"
            kwargs = dict(
                circuit=txt,
                n=code.n,
                d=code.d,
                code_name="",
                circuit_name=name,
                source=SOURCE_EVAL,
                tool="mqt-qecc",
                source_file=f"scripts/ft_stateprep/eval/circuits/{rel}",
                logical_state=state,
                connectivity="fully-connected",
                gate_set=gate_set_of(stim.Circuit(txt)),
                tags=tags,
                notes=method_note,
                data_dir=str(data_dir),
                overwrite=overwrite,
            )
            if code.fit == "identity":
                kwargs.update(method="anchor", anchor_H=h, permutation=list(range(code.n)))
            elif code.fit == "perm_find":
                kwargs.update(method="anchor", anchor_H=h, permutation=sigma)
            elif code.fit == "search":
                kwargs.update(method="anchor", anchor_H=h)  # n<=9: fit searches
            else:  # self_dual
                kwargs.update(method="self_dual")
            if not write:
                imported += 1
                continue
            try:
                import_state_prep(**kwargs)
                imported += 1
            except Exception as e:  # noqa: BLE001
                report.append(f"FAIL {rel}: {type(e).__name__}: {str(e).splitlines()[0][:80]}")
                deferred += 1
    print(f"eval/: {'imported' if write else 'classified'}={imported} deferred={deferred}")
    for line in report:
        print("  " + line)
    return imported, deferred


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--data-dir", default=str(REPO / "data_yaml"))
    ap.add_argument("--only", choices=["eval", "det"], default=None)
    ap.add_argument(
        "--overwrite",
        action="store_true",
        help="replace already-imported circuits in place (data refresh), keeping qec_ids",
    )
    args = ap.parse_args()
    if not DATASET.exists():
        sys.exit(f"dataset not found at {DATASET} — clone munich-quantum-toolkit/qecc there")
    data_dir = Path(args.data_dir)
    if args.only in (None, "eval"):
        run_eval(args.write, data_dir, overwrite=args.overwrite)
    if args.only in (None, "det"):
        from run_det import run_det  # noqa: PLC0415  (module added in Task 4)

        run_det(args.write, data_dir, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
