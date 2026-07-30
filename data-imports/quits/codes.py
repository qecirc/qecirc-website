"""The QUITS code catalogue, transcribed from the repo's own parameter tables.

Every entry here is a code QUITS documents with published parameters — the
constructor arguments come from `doc/01A_codes_basics.ipynb`, the `[[n,k,d]]`
from the paper each table cites. Nothing is invented: where a source gives only
an upper bound on the distance, `d_is_bound` records that, and where the
distance follows from a formula rather than a table, `d_source` says which.

`n` and `k` are asserted against the constructed code on every run, so a
mis-transcribed row fails loudly instead of importing a mislabelled code.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

import numpy as np

# Classical parity-check matrices shipped with QUITS, used for the HGP codes.
PCM_DIR = "parity_check_matrices"


@dataclass(frozen=True)
class CodeSpec:
    """One code of the catalogue."""

    key: str  # stable identifier, used for SIGMA lookup and reporting
    family: str  # key into FAMILY below
    n: int
    k: int
    d: int
    build: Callable  # () -> a quits code object (needs the dataset path bound)
    d_is_bound: bool = False  # source gives d as an upper bound, not a value
    d_source: str = ""  # only when the distance is not a table lookup
    slug: Optional[str] = None  # overrides the default f"{n}-{k}-{d}"
    name: Optional[str] = None  # overrides FAMILY's name, to tell two apart


# name, zoo_url, code tags — per family, following the vocabulary already in
# data_yaml/codes/ (CSS / LDPC / self-dual / surface-code / ...).
FAMILY = {
    "bb": (
        "Bivariate Bicycle Code",
        "",
        ["CSS", "bivariate-bicycle-code", "LDPC"],
    ),
    "bpc": (
        "Balanced Product Cyclic Code",
        "https://errorcorrectionzoo.org/c/balanced_product",
        ["CSS", "LDPC"],
    ),
    "hgp": (
        "Hypergraph Product Code",
        "https://errorcorrectionzoo.org/c/hypergraph_product",
        ["CSS", "LDPC"],
    ),
    "lcs": (
        "Lift-Connected Surface Code",
        "https://errorcorrectionzoo.org/c/lcs",
        ["CSS", "surface-code", "LDPC"],
    ),
    "qlp": (
        "Quasi-Cyclic Lifted Product Code",
        "https://errorcorrectionzoo.org/c/lifted_product",
        ["CSS", "LDPC"],
    ),
}

# Per-family provenance for the code construction itself. The *schedule* has its
# own source (see SCHEDULE in rebuild_all.py) — these two are not the same paper.
FAMILY_PAPER = {
    "bb": "Bravyi et al., arXiv:2308.07915, Table 3",
    "bpc": "Tiew and Breuckmann, arXiv:2411.03302",
    "hgp": "Tillich and Zemor, arXiv:0903.0566",
    "lcs": "Old, Rispler and Muller, arXiv:2401.02911",
    "qlp": "Xu et al., arXiv:2308.08648",
}


def build_catalogue(dataset: Path) -> list[CodeSpec]:
    """The full catalogue. Imports quits lazily so `--help` works without it."""
    from quits.qldpc_code import BbCode, BpcCode, HgpCode, LcsCode, QlpCode

    specs: list[CodeSpec] = []

    # --- Bivariate bicycle, Bravyi et al. arXiv:2308.07915 Table 3 -----------
    # (n, k, d, l, m, A_x, A_y, B_x, B_y); the last two distances are the
    # paper's upper bounds, not values.
    bb = [
        (72, 12, 6, 6, 6, [3], [1, 2], [1, 2], [3], False),
        (90, 8, 10, 15, 3, [9], [1, 2], [2, 7], [0], False),
        (108, 8, 10, 9, 6, [3], [1, 2], [1, 2], [3], False),
        (144, 12, 12, 12, 6, [3], [1, 2], [1, 2], [3], False),
        (288, 12, 18, 12, 12, [3], [2, 7], [1, 2], [3], False),
        (360, 12, 24, 30, 6, [9], [1, 2], [25, 26], [3], True),
        (756, 16, 34, 21, 18, [3], [10, 17], [3, 19], [5], True),
    ]
    # [[90,8,10]] shares its parameters with the stored `90-8-10`, which is a
    # *different* code despite carrying the alias "(15,3) BB6 code": this one is
    # Table 3's (15,3) entry and its X row space has no weight-4 codewords, the
    # stored one's has 90. It is refuted in ASSUME_NEW; the suffix keeps them
    # apart on disk, and matches the slug autqec's import (#127) gives the same
    # code, so whichever lands first creates the single shared entry.
    bb_slug = {(90, 8, 10): "90-8-10-autqec"}
    bb_name = {(90, 8, 10): "Bivariate Bicycle Code (Bravyi Table 3)"}
    for n, k, d, ln, m, ax, ay, bx, by, bound in bb:
        specs.append(
            CodeSpec(
                key=f"bb-{n}-{k}-{d}",
                family="bb",
                n=n,
                k=k,
                d=d,
                d_is_bound=bound,
                slug=bb_slug.get((n, k, d)),
                name=bb_name.get((n, k, d)),
                build=lambda ln=ln, m=m, ax=ax, ay=ay, bx=bx, by=by: BbCode(ln, m, ax, ay, bx, by),
            )
        )

    # --- Balanced product cyclic, Tiew and Breuckmann arXiv:2411.03302 -------
    # lift_size = 3q and factor = 3 throughout; p2 uses the transpose convention
    # the QUITS notebook documents (lift_size minus the paper's powers).
    bpc = [
        (36, 8, 4, 6, [0, 1, 2], [0, 4, 5]),
        (54, 8, 4, 9, [0, 1, 2], [0, 7, 8]),
        (72, 8, 8, 12, [0, 1, 5], [0, 4, 11]),
        (90, 8, 10, 15, [0, 1, 5], [0, 8, 13]),
        (108, 8, 8, 18, [0, 1, 5], [0, 16, 17]),
        (126, 8, 10, 21, [0, 1, 5], [0, 14, 19]),
        (144, 8, 12, 24, [0, 1, 5], [0, 13, 23]),
        (162, 8, 12, 27, [0, 1, 5], [0, 16, 26]),
        (180, 8, 16, 30, [0, 1, 5], [0, 13, 29]),
    ]
    # Two of these share [[n,k,d]] with a stored code that is a *different*
    # code — [[90,8,10]] with a bivariate bicycle code, [[36,8,4]] with a
    # hyperbolic surface code — so the default `n-k-d` slug would collide and
    # overwrite the stored entry. Both are refuted in ASSUME_NEW; the suffix is
    # what keeps them apart on disk. rebuild_all.py refuses to import any
    # assume-new code whose slug is already taken, so a future collision fails
    # loudly rather than clobbering.
    bpc_slug_taken = {(90, 8, 10), (36, 8, 4)}
    for n, k, d, lift, p1, p2 in bpc:
        specs.append(
            CodeSpec(
                key=f"bpc-{n}-{k}-{d}",
                family="bpc",
                n=n,
                k=k,
                d=d,
                slug=f"{n}-{k}-{d}-bpc" if (n, k, d) in bpc_slug_taken else None,
                build=lambda lift=lift, p1=p1, p2=p2: BpcCode(p1, p2, lift, 3, canonical_basis="Z"),
            )
        )

    # --- Hypergraph product of the classical codes QUITS ships ---------------
    # HGP(C, C) has k = k_C^2 + k_Ct^2 and d = min(d_C, d_Ct). Each shipped
    # matrix has full row rank, so k_Ct = 0, d_Ct is infinite and the quantum
    # distance is the classical one named in the filename. The k assertion in
    # rebuild_all.py is what confirms k_Ct = 0 on every run.
    hgp = [
        (225, 9, 6, "n=12_dv=3_dc=4_dist=6.txt"),
        (625, 25, 8, "n=20_dv=3_dc=4_dist=8_arXiv2311_03307.txt"),
        (900, 36, 10, "n=24_dv=3_dc=4_dist=10_arXiv2311_03307.txt"),
    ]
    for n, k, d, fname in hgp:
        specs.append(
            CodeSpec(
                key=f"hgp-{n}-{k}-{d}",
                family="hgp",
                n=n,
                k=k,
                d=d,
                d_source="the classical code's distance; the transpose code has k = 0",
                build=lambda fname=fname: HgpCode(
                    *(np.loadtxt(dataset / PCM_DIR / fname, dtype=int),) * 2
                ),
            )
        )

    # --- Lift-connected surface, Old et al. arXiv:2401.02911 -----------------
    # The paper gives no table for these sizes but does give the closed form
    # n = [(l+1)^2 + l^2] L, k = L, d = min(L, 2l+1), with QUITS' `length` = l+1.
    # The n and k assertions check the first two against the built code.
    for lift, length in [(5, 3), (5, 4), (7, 3)]:
        ell = length - 1
        n = ((ell + 1) ** 2 + ell**2) * lift
        specs.append(
            CodeSpec(
                key=f"lcs-L{lift}-l{ell}",
                family="lcs",
                n=n,
                k=lift,
                d=min(lift, 2 * ell + 1),
                d_source="the closed form d = min(L, 2l+1) of arXiv:2401.02911",
                build=lambda lift=lift, length=length: LcsCode(lift, length),
            )
        )

    # --- Quasi-cyclic lifted product, Xu et al. arXiv:2308.08648 -------------
    # All four distances in that table are upper bounds.
    qlp = [
        (544, 80, 12, 16, [[0, 0, 0, 0, 0], [0, 2, 4, 7, 11], [0, 3, 10, 14, 15]]),
        (714, 100, 16, 21, [[0, 0, 0, 0, 0], [0, 4, 5, 7, 17], [0, 14, 18, 12, 11]]),
        (1020, 136, 20, 30, [[0, 0, 0, 0, 0], [0, 2, 14, 24, 25], [0, 16, 11, 14, 13]]),
        (1428, 184, 24, 42, [[0, 0, 0, 0, 0], [0, 6, 7, 9, 30], [0, 40, 15, 31, 35]]),
    ]
    for n, k, d, lift, b in qlp:
        specs.append(
            CodeSpec(
                key=f"qlp-{n}-{k}-{d}",
                family="qlp",
                n=n,
                k=k,
                d=d,
                d_is_bound=True,
                build=lambda lift=lift, b=b: QlpCode(np.array(b), np.array(b), lift),
            )
        )

    return specs
