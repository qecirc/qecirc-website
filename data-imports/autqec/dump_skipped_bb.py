#!/usr/bin/env python
"""Dump check matrices of the skipped BB codes for external equivalence checks.

For each bivariate bicycle code whose autqec circuits could not be attached to
the stored library code (see README.md "Deliberately skipped"), this writes
both sides' matrices to ``skipped_bb_codes/``:

  <slug>.autqec.hx.txt / .hz.txt   autqec's CSS construction
                                   (examples/bivariate_bicycle_codes/code_data)
  <slug>.stored.hx.txt / .hz.txt   the library code's CSS split of codes/<slug>.yaml

All files are dense 0/1 matrices, one row per stabilizer generator, entries
space-separated. Both codes are CSS, so Hx/Hz fully describe them. The open
question per code: does a qubit permutation sigma (optionally composed with an
X<->Z swap) map one row space onto the other?

Usage:
  uv run python data-imports/autqec/dump_skipped_bb.py [--dataset PATH]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from rebuild_all import _default_dataset  # noqa: E402

from scripts.add_circuit.code_identify import split_h_to_css  # noqa: E402

SKIPPED = [
    ("n90k8d10", "90-8-10"),
    ("n108k8d10", "108-8-10"),
    ("n144k12d12", "144-12-12"),
]


def write_mat(path: Path, mat: np.ndarray) -> None:
    rows = [" ".join(str(int(v)) for v in row) for row in np.asarray(mat, dtype=int)]
    path.write_text("\n".join(rows) + "\n")
    print(f"  wrote {path.relative_to(REPO)}  {mat.shape[0]}x{mat.shape[1]}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default=str(_default_dataset()))
    args = ap.parse_args()

    bb_data = Path(args.dataset) / "examples" / "bivariate_bicycle_codes" / "code_data"
    out_dir = HERE / "skipped_bb_codes"
    out_dir.mkdir(exist_ok=True)

    for stem, slug in SKIPPED:
        print(f"== {slug} ==")
        hx = np.array(np.load(bb_data / f"HX_{stem}.npy"), dtype=int) % 2
        hz = np.array(np.load(bb_data / f"HZ_{stem}.npy"), dtype=int) % 2
        write_mat(out_dir / f"{slug}.autqec.hx.txt", hx)
        write_mat(out_dir / f"{slug}.autqec.hz.txt", hz)

        code = yaml.safe_load((REPO / "data_yaml" / "codes" / f"{slug}.yaml").read_text())
        h = np.array(code["h"], dtype=int)
        css = split_h_to_css(h, code["n"])
        if css is None:
            raise SystemExit(f"stored {slug} unexpectedly not CSS-decomposable")
        write_mat(out_dir / f"{slug}.stored.hx.txt", css[0])
        write_mat(out_dir / f"{slug}.stored.hz.txt", css[1])


if __name__ == "__main__":
    main()
