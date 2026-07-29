"""The codes this import covers, and why these and not others.

qLDPC's syndrome-extraction and encoding circuits work on essentially every CSS
code it can construct, so the catalogue is a choice rather than a transcription.
It is drawn along two lines:

* codes **already in the library**, so the circuits attach to existing entries
  and become directly comparable with the schedules and encoders already stored
  for them;
* a few of qLDPC's own constructions that the library has no entry for at all.

`n` and `k` are asserted against the constructed code on every run, so a wrong
row here fails loudly instead of importing a mislabelled code. `d` is asserted
against qLDPC's own exact distance wherever that is instant, which is everywhere
except the bivariate bicycle code — see `verify_d`.

**Subsystem codes are deliberately absent.** `BaconShorCode` and `SHYPSCode`
build and their circuits validate against `get_stabilizer_ops()`, but the library
derives k as n - rank(h), which is only correct for stabilizer codes: Bacon-Shor
[[9,1,3]] would be stored as [[9,5,3]] and SHYPS [[49,9,4]] as [[49,25,4]].
Storing them needs a gauge-group field and a k that is not derived — a data-model
change, not an import.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(frozen=True)
class CodeSpec:
    key: str
    family: str
    n: int
    k: int
    d: int
    build: Callable
    # Set only for codes this import expects to *create*. A code already in the
    # library takes its stored slug from the dedup match, and passing one here
    # would name its circuit files after a code entry that is never written.
    slug: Optional[str] = None
    # Whether to check `d` against qLDPC's own exact distance on every run.
    # True everywhere it is instant; False for the bivariate bicycle code, whose
    # distance search is a hard combinatorial problem that does not terminate.
    verify_d: bool = True


# name, zoo_url, code tags — reusing the vocabulary already in data_yaml/codes/.
FAMILY = {
    "steane": ("Steane Code", "https://errorcorrectionzoo.org/c/steane", ["CSS", "self-dual"]),
    "five-qubit": (
        "Five-Qubit Perfect Code",
        "https://errorcorrectionzoo.org/c/stab_5_1_3",
        ["stabilizer"],
    ),
    "hamming": (
        "Quantum Hamming Code",
        "https://errorcorrectionzoo.org/c/quantum_hamming",
        ["CSS", "hamming-code"],
    ),
    "tetrahedral": (
        "Tetrahedral Code",
        "https://errorcorrectionzoo.org/c/stab_15_1_3",
        ["CSS"],
    ),
    "iceberg": (
        "Iceberg Code",
        "https://errorcorrectionzoo.org/c/iceberg",
        ["CSS", "self-dual"],
    ),
    "rotated-surface": (
        "Rotated Surface Code",
        "https://errorcorrectionzoo.org/c/rotated_surface",
        ["CSS", "surface-code", "topological"],
    ),
    "unrotated-surface": (
        "Unrotated Surface Code",
        "https://errorcorrectionzoo.org/c/surface",
        ["CSS", "surface-code", "topological"],
    ),
    "toric": (
        "Toric Code",
        "https://errorcorrectionzoo.org/c/toric",
        ["CSS", "surface-code", "topological"],
    ),
    "hgp": (
        "Hypergraph Product Code",
        "https://errorcorrectionzoo.org/c/hypergraph_product",
        ["CSS", "LDPC"],
    ),
    "bb": (
        "Bivariate Bicycle Code",
        "",
        ["CSS", "bivariate-bicycle-code", "LDPC"],
    ),
}


def _catalogue() -> list[CodeSpec]:
    import qldpc.codes as C
    from sympy.abc import x, y

    spec = CodeSpec
    return [
        # --- already in the library: the circuits join existing entries -------
        spec("steane", "steane", 7, 1, 3, C.SteaneCode),
        spec("five-qubit", "five-qubit", 5, 1, 3, C.FiveQubitCode),
        spec("hamming-15-7-3", "hamming", 15, 7, 3, lambda: C.QuantumHammingCode(4)),
        spec("tetrahedral", "tetrahedral", 15, 1, 3, C.TetrahedralCode),
        spec("surface-d3", "rotated-surface", 9, 1, 3, lambda: C.SurfaceCode(3)),
        spec("surface-d5", "rotated-surface", 25, 1, 5, lambda: C.SurfaceCode(5)),
        spec("surface-d7", "rotated-surface", 49, 1, 7, lambda: C.SurfaceCode(7)),
        spec(
            "surface-d3-unrotated",
            "unrotated-surface",
            13,
            1,
            3,
            lambda: C.SurfaceCode(3, rotated=False),
        ),
        spec("toric-d4", "toric", 16, 2, 4, lambda: C.ToricCode(4), slug="16-2-4-toric"),
        spec(
            "bb-72-12-6",
            "bb",
            72,
            12,
            6,
            lambda: C.BBCode({x: 6, y: 6}, x**3 + y + y**2, y**3 + x + x**2),
            verify_d=False,  # d = 6 from Bravyi et al. arXiv:2308.07915, Table 3
        ),
        # --- new to the library ----------------------------------------------
        spec("iceberg-c4", "iceberg", 4, 2, 2, C.C4Code, slug="4-2-2"),
        spec("iceberg-c6", "iceberg", 6, 2, 2, C.C6Code, slug="6-2-2"),
        spec("toric-d6", "toric", 36, 2, 6, lambda: C.ToricCode(6), slug="36-2-6"),
        spec("hgp-hamming3", "hgp", 58, 16, 3, lambda: C.HGPCode(C.HammingCode(3)), slug="58-16-3"),
        spec(
            "hgp-hamming4",
            "hgp",
            241,
            121,
            3,
            lambda: C.HGPCode(C.HammingCode(4)),
            slug="241-121-3",
        ),
    ]


class _Lazy(list):
    """The catalogue, built on first use so `--help` works without qldpc."""

    def _fill(self):
        if not list.__len__(self):
            self.extend(_catalogue())
        return self

    def __iter__(self):
        return list.__iter__(self._fill())

    def __len__(self):
        return list.__len__(self._fill())


CATALOGUE = _Lazy()
