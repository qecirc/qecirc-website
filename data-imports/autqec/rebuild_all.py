#!/usr/bin/env python
"""autqec logical Clifford gates from code automorphisms (arXiv:2409.18175).

Sayginel/Koutsioumpas/Webster/Rajput/Browne find logical Clifford gates of
stabilizer codes from the automorphism groups of associated binary linear
codes. The expensive step (MAGMA/Bliss automorphism search) is already done —
the ``autqec`` repository commits its results — so this importer only replays
cheap, deterministic circuit synthesis. Two sections:

**examples** — the paper's worked examples ([[4,2,2]], [[5,1,3]], Steane,
[[17,1,7]], BB [[72,12,6]]). Pickles hold automorphism-group *generators*
(``examples/auts_data/*.pkl``); circuits are synthesized here:

  aut generator -> physical circuit (1q Cliffords + SWAPs, or H/S/sqrt(X)+SWAP
  for the duality families) -> Pauli corrections fixing stabilizer signs ->
  STIM, relabeled to the stored code's canonical qubit order.

**codetables** — the paper's n <= 28 sweep over codetables.de best-known
[[n,k]] codes. Pickles hold finished *circuits* with Pauli corrections
(``codetables/logical_gates/gates_n{n}k{k}.pkl`` and the ZX variant); parity
checks ship as ``codetables/parity_checks/*.npy``; best-known distances come
from ``codetables_distances.json`` (see fetch_codetables_distances.py). Only
d >= 3 codes are imported. Except for the handful of identified codes below,
these are anonymous record-holders: their code entries are tagged
``codetables``, which hides them from the /codes listing and all displayed
counts (see HIDDEN_CODE_TAG in src/lib/constants.ts) while leaving them fully
searchable. Identified codes — verified permutation-equivalent to a stored
code, or unique up to equivalence — are imported as normal visible codes:

  [[7,1,3]]  -> steane-code (verified: hash dedup fits it)
  [[8,3,3]]  -> gottesman-8-3-3-code (verified)
  [[17,1,7]] -> 17-1-7 (same dataset as the examples section)
  [[6,1,3]]  -> new normal code: THE six-qubit code (unique up to equivalence)
  [[5,1,3]]  -> hidden ct-5-1-3: local-Clifford-equivalent to five-qubit-code
                (the code is unique) but NOT permutation-equivalent, so its
                circuits cannot be relabeled onto the stored entry
  [[11,1,5]] -> hidden ct-11-1-5: plausibly the Gottesman/quantum dodecacode,
                but no machine-readable reference tableau was available to
                verify — future identification welcome

For every circuit the logical action is recomputed *in the stored code's
logical basis* and written as ``logical_action`` — the machine-checked claim
``npm run validate:circuits`` verifies via ``validate_logical_gate_h``.
Generators with identity logical action are skipped; identical bodies (within
a code, or already on disk from a previous section) are deduplicated.

Requires a checkout of https://github.com/hsayginel/autqec next to the
website repository (or pass --dataset). Uses only committed pickles + numpy;
no MAGMA, Bliss, or igraph needed.

Usage:
  python rebuild_all.py                 # classify only (no writes)
  python rebuild_all.py --write
  python rebuild_all.py --section codetables
  python rebuild_all.py --dataset PATH  # autqec checkout (default: sibling)
"""

from __future__ import annotations

import argparse
import json
import pickle
import re
import sys
from pathlib import Path

import numpy as np
import stim

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def _default_dataset() -> Path:
    """Find the autqec checkout: sibling of the repo, walking up for worktrees."""
    for base in (REPO.parent, *REPO.parents):
        cand = base / "autqec"
        if (cand / "examples" / "auts_data").is_dir():
            return cand
    return REPO.parent / "autqec"


sys.path.insert(0, str(REPO))

from scripts.add_circuit.circuit_validate import (  # noqa: E402
    induced_logical_action,
    transversality_class,
    validate_logical_gate_h,
)
from scripts.add_circuit.code_identify import split_h_to_css  # noqa: E402
from scripts.add_circuit.compute import compute_code_data_h  # noqa: E402
from scripts.add_circuit.compute_circuit import compute_circuit_data  # noqa: E402
from scripts.add_circuit.ids import next_qec_id  # noqa: E402
from scripts.add_circuit.perm_find import find_code_permutation  # noqa: E402
from scripts.add_circuit.yaml_helpers import (  # noqa: E402
    build_circuit_yaml,
    build_code_yaml,
    build_original_yaml,
    dump_yaml,
    load_yaml,
    write_file,
)

SOURCE = "https://arxiv.org/abs/2409.18175"
TOOL = "autqec"
HIDDEN_CODE_TAG = "codetables"  # keep in sync with src/lib/constants.ts

# Qubit permutations onto stored codes that the structural finder cannot
# recover within budget (automorphism-rich BB codes). Found offline via the
# weight-6-codeword incidence-graph isomorphism (see README) and verified by
# row-space equality both there and again on every load below. Convention
# matches compute_circuit_data's qubit_permutation: sigma[new] = old.
SIGMA_PRECOMPUTED = HERE / "sigma_precomputed.json"

# autqec gate tuple name -> stim gate. Verified exactly (binary action AND
# signs) against autqec's clifford_circ_stab_update on every 1-/2-qubit Pauli.
GATE_MAP = {
    "H": "H",
    "S": "S",
    "Xsqrt": "SQRT_X",
    "GammaXYZ": "C_XYZ",  # X->Y->Z->X
    "GammaXZY": "C_ZYX",  # X->Z->Y->X
    "SWAP": "SWAP",
    "CNOT": "CX",
    "CZ": "CZ",
    "C(X,X)": "XCX",
    "X": "X",
    "Y": "Y",
    "Z": "Z",
}

PRETTY = {
    "H": "H",
    "S": "S",
    "SQRT_X": "√X",
    "C_XYZ": "Γ(XYZ)",
    "C_ZYX": "Γ(XZY)",
    "CX": "CNOT",
    "CZ": "CZ",
    "XCX": "C(X,X)",
    "SWAP": "SWAP",
    "X": "X",
    "Y": "Y",
    "Z": "Z",
}

_qec_id_re = re.compile(r"^qec_id:\s*(\d+)\s*$", re.MULTILINE)
_gates_pkl_re = re.compile(r"gates_n(\d+)k(\d+)\.pkl")


def autqec_to_stim(gates: list, n: int) -> stim.Circuit:
    """autqec gate-tuple list (1-indexed) -> stim.Circuit on n qubits."""
    out = stim.Circuit()
    for gate, q in gates:
        name = GATE_MAP[gate]
        if isinstance(q, tuple):
            out.append(name, [int(q[0]) - 1, int(q[1]) - 1])
        else:
            out.append(name, [int(q) - 1])
    if out.num_qubits < n:
        out.append("I", [n - 1])
    return out


# Tagging policy on top of the structural transversality_class fact: transversal
# circuits are unconditionally FT (errors cannot spread), SWAP-transversal ones
# are FT only architecture-dependently so they get no `ft` tag (the circuit
# notes explain), and general Clifford circuits make no FT claim.
STRUCTURE_POLICY = {
    "transversal": ("Transversal", ["transversal", "ft"]),
    "swap-transversal": ("SWAP-transversal", ["swap-transversal"]),
    "general": ("Short-depth", []),
}


def load_auts(path: Path) -> list:
    with open(path, "rb") as f:
        return pickle.load(f)["auts"]


def _gf2_rref(mat: np.ndarray) -> np.ndarray:
    """Reduced row echelon form over F2 with zero rows dropped — a canonical
    representative of the row space, so equality of RREFs is equality of
    spaces."""
    m = (np.array(mat, dtype=np.uint8) % 2).copy()
    r = 0
    for c in range(m.shape[1]):
        piv = next((i for i in range(r, m.shape[0]) if m[i, c]), None)
        if piv is None:
            continue
        m[[r, piv]] = m[[piv, r]]
        for i in range(m.shape[0]):
            if i != r and m[i, c]:
                m[i] ^= m[r]
        r += 1
        if r == m.shape[0]:
            break
    return m[:r]


def sigma_verifies(H: np.ndarray, stored_h: np.ndarray, n: int, sigma: list[int]) -> bool:
    """Does relabeling H's qubits by sigma (sigma[new] = old, both symplectic
    halves moving together) give exactly the stored code's row space?"""
    perm = np.array(sigma, dtype=int)
    H_p = np.zeros_like(H)
    H_p[:, np.arange(n)] = H[:, perm]
    H_p[:, np.arange(n) + n] = H[:, perm + n]
    a, b = _gf2_rref(H_p), _gf2_rref(stored_h)
    return a.shape == b.shape and np.array_equal(a, b)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dataset", default=str(_default_dataset()))
    ap.add_argument("--data-dir", default=str(REPO / "data_yaml"))
    ap.add_argument("--codes", nargs="*", help="only process these pickle stems (e.g. n5k1d3)")
    ap.add_argument(
        "--section",
        choices=("examples", "codetables", "all"),
        default="all",
        help="which dataset section to import",
    )
    args = ap.parse_args()

    dataset = Path(args.dataset)
    auts_dir = dataset / "examples" / "auts_data"
    if not auts_dir.is_dir():
        sys.exit(f"autqec checkout not found at {dataset} — clone hsayginel/autqec there")
    data_dir = Path(args.data_dir)

    sys.path.insert(0, str(dataset))
    from autqec.automorphisms import (  # noqa: E402
        circ_from_aut,
        circ_from_symp_mat,
        logical_circ_and_pauli_correct,
    )
    from autqec.utils.linalg import inv_mod2, rref_mod2  # noqa: E402
    from autqec.utils.qec import compute_standard_form, stabs_to_H_symp  # noqa: E402
    from autqec.XY_dualities import circ_from_XY_duality  # noqa: E402
    from autqec.ZX_dualities import circ_from_ZX_duality  # noqa: E402
    from autqec.ZY_dualities import circ_from_ZY_duality  # noqa: E402

    def independent_generating_set(H: np.ndarray) -> np.ndarray:
        """Row-reduce a (possibly redundant) stabilizer matrix to a full-rank
        generating set expressed in the original qubit basis — the same step the
        paper's bivariate-bicycle notebooks apply, since ``circ_from_aut`` and
        ``compute_standard_form`` require independent rows."""
        rref, _, _, transform_cols = rref_mod2(H)
        rref = rref[~np.all(rref == 0, axis=1)]
        if rref.shape[0] == H.shape[0]:
            return H
        return (rref @ inv_mod2(transform_cols)) % 2

    def action_from_u(u: np.ndarray, k: int) -> tuple[str, str, list[str]]:
        """Decompose a binary symplectic logical action into gates.

        Returns (stim_text, pretty_name, logical_op_tags). Uses autqec's own
        ``circ_from_symp_mat`` decomposition (H-CNOT-S-CZ layers), so the claim
        is produced by the same algebra as the physical circuits.
        """
        gates = circ_from_symp_mat(u).run()
        circ = autqec_to_stim(gates, k)
        # drop the widening I, if any, from the claim text
        text = "\n".join(line for line in str(circ).splitlines() if not line.startswith("I "))
        parts = []
        ops = []
        for gate, q in gates:
            name = GATE_MAP[gate]
            if k == 1:
                parts.append(PRETTY[name])
            elif isinstance(q, tuple):
                parts.append(f"{PRETTY[name]}({q[0]},{q[1]})")
            else:
                parts.append(f"{PRETTY[name]}({q})")
            ops.append(name)
        pretty = "·".join(parts)
        tags = [f"logical-op:{name}" for name in dict.fromkeys(ops)]
        return text, pretty, tags

    steane_hamming = np.array(
        [[1, 0, 0, 1, 0, 1, 1], [0, 1, 0, 1, 1, 0, 1], [0, 0, 1, 0, 1, 1, 1]], dtype=int
    )
    zeros7 = np.zeros_like(steane_hamming)

    # ------------------------------------------------------------------
    # Section: examples — paper-labeled codes, exactly as the autqec example
    # notebooks define them. Pickles hold automorphism generators.
    # ------------------------------------------------------------------
    EXAMPLE_CODES = [
        {
            "stem": "n4k2d2",
            "name": "[[4,2,2]]",
            "slug": "4-2-2",
            "n": 4,
            "d": 2,
            "zoo_url": "https://errorcorrectionzoo.org/c/stab_4_2_2",
            "H": stabs_to_H_symp(["XXXX", "ZZZZ"]),
        },
        {
            "stem": "n5k1d3",
            "name": "Five-Qubit Perfect Code",
            "slug": "five-qubit-code",  # the stored slug — dedup must land here
            "n": 5,
            "d": 3,
            "zoo_url": "",
            "H": stabs_to_H_symp(["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]),
        },
        {
            "stem": "n7k1d3",
            "name": "Steane Code",
            "slug": "steane-code",  # the stored slug — dedup must land here
            "n": 7,
            "d": 3,
            "zoo_url": "",
            "H": np.vstack(
                [np.hstack([steane_hamming, zeros7]), np.hstack([zeros7, steane_hamming])]
            ).astype(int),
        },
        {
            "stem": "n17k1d7",
            "name": "[[17,1,7]]",
            "slug": "17-1-7",
            "n": 17,
            "d": 7,
            "zoo_url": "",
            "H": np.array(
                np.load(dataset / "codetables" / "parity_checks" / "H_symp_n17k1.npy"), dtype=int
            ),
        },
    ]

    # Bivariate bicycle codes (paper Sec. on BB codes; full ⟨H,S⟩+SWAP groups
    # in full_aut_groups/). [[72,12,6]] fits the stored code directly (shared
    # labeling, hash dedup); [[108,8,10]] and [[144,12,12]] fit via the
    # offline-precomputed sigmas in sigma_precomputed.json (weight-6-codeword
    # incidence-graph isomorphism; re-verified on every run).
    #
    # autqec's [[90,8,10]] is a genuinely DIFFERENT code than the stored
    # 90-8-10: its X-space has 45 weight-6 codewords and none of weight 4, vs
    # the stored code's 90 weight-4 + 600 weight-6 — weight enumerators are
    # permutation invariants, so no relabeling can reconcile them. It is
    # imported as a second, distinct code entry with its own slug and a
    # disambiguating name.
    bb_dir = dataset / "examples" / "bivariate_bicycle_codes"
    for stem, slug, name, d in [
        ("n72k12d6", "72-12-6", "Bivariate Bicycle Code", 6),
        ("n90k8d10", "90-8-10-autqec", "Bivariate Bicycle Code (autqec)", 10),
        ("n108k8d10", "108-8-10", "Bivariate Bicycle Code", 10),
        ("n144k12d12", "144-12-12", "Gross Code", 12),
    ]:
        hx = np.array(np.load(bb_dir / "code_data" / f"HX_{stem}.npy"), dtype=int)
        hz = np.array(np.load(bb_dir / "code_data" / f"HZ_{stem}.npy"), dtype=int)
        zx, zz = np.zeros_like(hx), np.zeros_like(hz)
        spec = {
            "stem": stem,
            "name": name,
            "slug": slug,
            "n": hx.shape[1],
            "d": d,
            "zoo_url": "",
            "H": np.vstack([np.hstack([hx, zx]), np.hstack([zz, hz])]),
            "auts_dir": bb_dir / "full_aut_groups",
            "families": ("automorphism",),
        }
        if slug == "90-8-10-autqec":
            spec["notes_suffix"] = (
                " Note: this code shares its [[90,8,10]] parameters with, but is "
                "provably inequivalent to, the library's other bivariate bicycle "
                "code 90-8-10 — their X-space weight enumerators differ (45 "
                "weight-6 codewords here vs 90 weight-4 + 600 weight-6 there), "
                "which no qubit relabeling can reconcile."
            )
        EXAMPLE_CODES.append(spec)

    FAMILIES = [
        ("automorphism", "auts_{stem}.pkl", circ_from_aut),
        ("ZX-duality", "ZX_dualities_{stem}.pkl", circ_from_ZX_duality),
        ("XY-duality", "XY_dualities_{stem}.pkl", circ_from_XY_duality),
        ("YZ-duality", "YZ_dualities_{stem}.pkl", circ_from_ZY_duality),
    ]

    def example_circuits(spec, H):
        """Synthesize circuits from the committed automorphism generators."""
        all_families = tuple(f for f, _, _ in FAMILIES)
        for family, pattern, ctor in FAMILIES:
            if family not in spec.get("families", all_families):
                continue
            pkl = spec.get("auts_dir", auts_dir) / pattern.format(stem=spec["stem"])
            if not pkl.exists():
                print(f"  ({family}: no pickle, skipped)")
                continue
            for gen_idx, aut in enumerate(load_auts(pkl)):
                aut = [tuple(int(x) for x in cyc) for cyc in aut]
                phys_circ, _symp = ctor(H, aut).circ()
                _log_act, full_circ = logical_circ_and_pauli_correct(H, phys_circ).run()
                yield family, gen_idx, full_circ

    # ------------------------------------------------------------------
    # Section: codetables — best-known [[n,k]] codes, d >= 3. Pickles hold
    # finished circuits (Pauli corrections included).
    # ------------------------------------------------------------------
    ct_dir = dataset / "codetables"

    # (n, k) pairs whose code has an identity in the curated library. Every
    # other codetables code is an anonymous record-holder: slug ct-n-k-d,
    # tagged HIDDEN_CODE_TAG. Rationale for each entry is in the module
    # docstring; verification was permutation-equivalence via the site's own
    # dedup machinery (canonical hash + structural fit).
    CT_IDENTIFIED: dict[tuple[int, int], dict] = {
        (7, 1): {"name": "Steane Code", "slug": "steane-code", "hidden": False},
        (8, 3): {
            "name": "Gottesman [[8,3,3]] Code",
            "slug": "gottesman-8-3-3-code",
            "hidden": False,
        },
        (17, 1): {"name": "[[17,1,7]]", "slug": "17-1-7", "hidden": False},
        (6, 1): {
            "name": "Six-Qubit Code",
            "slug": "6-1-3",
            "hidden": False,
            "zoo_url": "https://errorcorrectionzoo.org/c/stab_6_1_3",
        },
    }

    def codetables_specs():
        distances = json.loads((HERE / "codetables_distances.json").read_text())
        gate_dirs = [
            ("automorphism", ct_dir / "logical_gates"),
            ("ZX-duality", ct_dir / "ZX_dualities" / "logical_gates"),
        ]
        pairs = sorted(tuple(map(int, key.split(","))) for key in distances)
        for n, k in pairs:
            d = distances[f"{n},{k}"]["d_lower"]
            if d < 3:
                continue
            pickles = [
                (family, gdir / f"gates_n{n}k{k}.pkl")
                for family, gdir in gate_dirs
                if (gdir / f"gates_n{n}k{k}.pkl").exists()
            ]
            if not pickles:
                continue
            ident = CT_IDENTIFIED.get((n, k), {})
            hidden = ident.get("hidden", True)
            spec = {
                "stem": f"ct_n{n}k{k}",
                "name": ident.get("name", f"[[{n},{k},{d}]] (codetables)"),
                "slug": ident.get("slug", f"ct-{n}-{k}-{d}"),
                "n": n,
                "d": d,
                "zoo_url": ident.get("zoo_url", ""),
                "H": np.array(
                    np.load(ct_dir / "parity_checks" / f"H_symp_n{n}k{k}.npy"), dtype=int
                ),
                "gate_pickles": pickles,
                "code_tags": [HIDDEN_CODE_TAG] if hidden else [],
                "notes_suffix": (
                    " The code is the best-known-distance [[%d,%d]] stabilizer code "
                    "from Grassl's codetables.de tables (snapshotted in the autqec "
                    "repository)." % (n, k)
                ),
            }
            yield spec

    def codetables_circuits(spec, H):
        """Yield the finished circuits committed in the codetables pickles."""
        del H  # circuits are precomputed; H only feeds the shared pipeline
        for family, pkl in spec["gate_pickles"]:
            with open(pkl, "rb") as f:
                data = pickle.load(f)
            for gen_idx, (phys, log_act) in enumerate(zip(data["physical"], data["logical"])):
                if not log_act:
                    # identity logical action is basis-independent — skip early
                    yield family, gen_idx, None
                    continue
                yield family, gen_idx, [(g, q) for g, q in phys]

    # ------------------------------------------------------------------
    # Shared per-code pipeline
    # ------------------------------------------------------------------
    stats = {"written": 0, "trivial": 0, "deduped": 0}

    def process_code(spec, circuits_iter) -> None:
        H, n, d = independent_generating_set(spec["H"]), spec["n"], spec["d"]
        code_result = compute_code_data_h(
            H,
            n,
            d,
            code_name=spec["name"],
            zoo_url=spec["zoo_url"],
            data_dir=str(data_dir),
            code_slug=spec["slug"],
        )
        code = code_result["code"]
        slug = code["slug"]
        perm = code_result["qubit_permutation"]
        print(f"\n== {spec['name']} -> {slug} ({code['status']}, perm={perm}) ==")

        code_path = data_dir / "codes" / f"{slug}.yaml"
        pre_existing = code_path.exists()
        if code["status"] == "new" and not pre_existing:
            for tag in spec.get("code_tags", []):
                code.setdefault("tags", []).append({"name": tag})
            if args.write:
                write_file(code_path, dump_yaml(build_code_yaml(code)), quiet=True)
                print(f"  seeded code {code_path.name}")
            else:
                print(f"  would seed code {code_path.name}")

        # Logical action is claimed against the STORED basis, so load it.
        if code_path.exists():
            stored = load_yaml(code_path.read_text())
            # A "new" code whose file already existed before this run means the
            # hash dedup missed a genuinely stored code — fit onto it. A file
            # we just seeded is our own canonical form; `perm` from
            # compute_code_data_h already maps onto it.
            if code["status"] == "new" and pre_existing:
                # The hash dedup missed (permutation-heavy codes like BB are
                # exactly where the canonical hash is not a true invariant).
                # Try the offline-precomputed sigma first, then the finder.
                h_stored_arr = np.array(stored["h"], dtype=int)
                sigma = None
                precomputed = (
                    json.loads(SIGMA_PRECOMPUTED.read_text())
                    if SIGMA_PRECOMPUTED.exists()
                    else {}
                )
                if slug in precomputed:
                    cand = precomputed[slug]
                    if not sigma_verifies(H, h_stored_arr, n, cand):
                        sys.exit(f"{slug}: precomputed sigma failed row-space verification")
                    sigma = cand
                    print("  (hash dedup missed; precomputed sigma verified)")
                else:
                    css_mine = split_h_to_css(H, n)
                    css_stored = split_h_to_css(h_stored_arr, n)
                    if css_mine is not None and css_stored is not None:
                        sigma = find_code_permutation(*css_mine, *css_stored)
                    if sigma is not None:
                        print(f"  (hash dedup missed; structural fit found perm={sigma})")
                if sigma is None:
                    sys.exit(
                        f"{slug}: stored code exists but no qubit permutation onto it "
                        "was found — different code, or search budget exceeded"
                    )
                perm = sigma
        elif code["status"] == "existing":
            sys.exit(f"dedup matched an existing code but {code_path} is missing — wrong slug?")
        else:
            stored = code  # dry run for a new code: canonical form not yet on disk
        h_stored = np.array(stored["h"], dtype=int)
        logical_stored = np.array(stored["logical"], dtype=int)
        k = logical_stored.shape[0] // 2

        # Paper-frame matrices for the originals/ record.
        _G, LX, LZ, _D = compute_standard_form(H)
        original_matrices = {"h": H.tolist(), "logical": np.vstack([LX, LZ]).tolist()}

        # Dedup against bodies already on disk for this code: the codetables
        # section revisits codes the examples section (or a previous run)
        # already populated — e.g. steane-code and 17-1-7.
        seen_bodies: set[str] = set()
        for existing_stim in (data_dir / "circuits").glob(f"{slug}--*.stim"):
            seen_bodies.add(existing_stim.read_text().strip())
        slug_counts: dict[str, int] = {}

        for family, gen_idx, full_circ in circuits_iter:
            if full_circ is None:
                stats["trivial"] += 1
                continue
            paper_stim = autqec_to_stim(full_circ, n)

            # Relabel to the stored code's canonical qubit order and get
            # the induced logical action in the stored basis.
            circ_data = compute_circuit_data(
                str(paper_stim), qubit_permutation=perm, circuit_name="tmp"
            )
            body = next(b["body"] for b in circ_data["bodies"] if b["format"] == "stim")
            u = induced_logical_action(body, h_stored, logical_stored, n)
            if isinstance(u, str):
                raise AssertionError(f"{slug} {family} gen {gen_idx}: {u}")
            if np.array_equal(u, np.eye(2 * k, dtype=int)):
                stats["trivial"] += 1
                continue
            if body.strip() in seen_bodies:
                stats["deduped"] += 1
                continue
            seen_bodies.add(body.strip())

            action_text, pretty, op_tags = action_from_u(u, k)
            check = validate_logical_gate_h(body, h_stored, logical_stored, n, action_text)
            if check != "passed":
                raise AssertionError(f"{slug} {family} gen {gen_idx}: {check}")

            struct, struct_tags = STRUCTURE_POLICY[transversality_class(paper_stim)]
            # Large-k codes induce logical actions dozens of gates long —
            # name those by provenance and leave the full action to the
            # notes and the logical_action field.
            if len(pretty) <= 48:
                name = f"{struct} logical {pretty}"
            else:
                name = f"{struct} logical Clifford ({family} gen {gen_idx})"
            notes = (
                f"Logical {pretty} (gates in application order) from generator "
                f"{gen_idx} of the code's {family} group, computed by autqec "
                f"(arXiv:2409.18175). Physical circuit is "
                f"{struct.lower()} — single-qubit Cliffords"
                + (" + SWAPs" if struct == "SWAP-transversal" else "")
                + (" + entangling gates" if struct == "Short-depth" else "")
                + ", with Pauli corrections that fix the stabilizer signs. "
                "The logical_action field states the claim in the stored "
                "code's logical basis; validate:circuits checks it."
            )
            if struct == "SWAP-transversal":
                notes += (
                    " SWAP-transversal circuits are fault-tolerant on "
                    "architectures where SWAPs are error-benign (shuttling "
                    "ion traps, atom arrays), hence no unconditional ft tag."
                )
            notes += spec.get("notes_suffix", "")
            tags = ["logical-gate", *struct_tags, *op_tags]

            def build(circuit_name: str) -> dict:
                built = compute_circuit_data(
                    str(paper_stim),
                    qubit_permutation=perm,
                    circuit_name=circuit_name,
                    source=SOURCE,
                    tool=TOOL,
                    notes=notes,
                    tags=tags,
                )
                built["logical_action"] = action_text
                return built

            final = build(name)
            base_slug = final["slug"]
            slug_counts[base_slug] = slug_counts.get(base_slug, 0) + 1
            if slug_counts[base_slug] > 1:
                name = f"{name} ({slug_counts[base_slug]})"
                final = build(name)

            stem = f"{slug}--{final['slug']}"
            if args.write:
                circuits_dir = data_dir / "circuits"
                existing = circuits_dir / f"{stem}.yaml"
                prev = _qec_id_re.search(existing.read_text()) if existing.exists() else None
                final["qec_id"] = int(prev.group(1)) if prev else next_qec_id(data_dir)
                write_file(
                    circuits_dir / f"{stem}.yaml", dump_yaml(build_circuit_yaml(final)), quiet=True
                )
                for b in final.get("bodies", []):
                    if b.get("body"):
                        write_file(circuits_dir / f"{stem}.{b['format']}", b["body"], quiet=True)
                originals = circuits_dir / "originals"
                write_file(originals / f"{stem}.original.stim", str(paper_stim), quiet=True)
                write_file(
                    originals / f"{stem}.original.yaml",
                    dump_yaml(build_original_yaml(original_matrices)),
                    quiet=True,
                )
            stats["written"] += 1
            verb = "wrote" if args.write else "ok   "
            print(f"  {verb} {stem} [{family} gen {gen_idx}] logical={pretty} ({struct})")

    # ------------------------------------------------------------------
    # Run the requested sections
    # ------------------------------------------------------------------
    if args.section in ("examples", "all"):
        for spec in EXAMPLE_CODES:
            if args.codes and spec["stem"] not in args.codes:
                continue
            H_reduced = independent_generating_set(spec["H"])
            process_code(spec, example_circuits(spec, H_reduced))

    if args.section in ("codetables", "all"):
        for spec in codetables_specs():
            if args.codes and spec["stem"] not in args.codes:
                continue
            H_reduced = independent_generating_set(spec["H"])
            process_code(spec, codetables_circuits(spec, H_reduced))

    print(
        f"\n{'wrote' if args.write else 'classified'} {stats['written']} circuits "
        f"({stats['trivial']} trivial-action generators skipped, "
        f"{stats['deduped']} duplicates)."
    )


if __name__ == "__main__":
    main()
