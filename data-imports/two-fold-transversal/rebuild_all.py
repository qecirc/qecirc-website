#!/usr/bin/env python
"""Depth-one two-local logical Clifford gates (arXiv:2608.05688).

Albert, "Beyond transversality: structure of Clifford circuits for CSS codes",
surveys 136 CSS codes whose depth-one two-local ("two-fold transversal")
Clifford circuits realize large logical Clifford groups — for 78 codes the
full Sp(2k,2). The companion repository ships the survey as two certified JSON
datasets; this importer converts every recorded gate string to STIM and files
it as a ``logical-gate`` circuit.

Datasets (checkout of https://github.com/valbert4/two-fold-transversal next to
the website repo, or --dataset):

  data/full_codes_depth1.json — 78 codes, full logical Clifford group
  data/ldpc_codes_depth1.json — 58 QLDPC codes, exact recorded group order

Gate-string grammar (the dataset's ``data/README.md``) -> STIM:

  S<q> -> S q          V<q>    -> SQRT_X q      H<q> -> H q
  CZ<i,j> -> CZ i j    cz<i,j> -> XCX i j       CX<i,j> -> CX i j
  (a,b,..) -> trailing SWAP network (cycle a->b->.., applied last)
  ^        -> layout separator (ZX-duality strings), no gate

The datasets are binary-symplectic and therefore sign-free: each STIM circuit
is one Pauli frame of the gate, exactly the equivalence class the sign-free
``validate_logical_gate_h`` checks (a logical gate is only defined up to
logical Paulis anyway). The conversion was verified against the paper's own
reference parser (``data/certify/core.py``) on all 12,586 gate strings —
exact symplectic equality, code preservation, and a depth-one two-local audit
of the emitted STIM.

Per circuit, the induced logical action is recomputed *in the stored code's
logical basis* and written as ``logical_action``. At 12,586 circuits the
importer computes it with one batched GF(2) solve per circuit (numerically
identical to the pipeline's ``induced_logical_action`` — asserted on the
first circuit of every code) and leaves the authoritative per-circuit
re-verification to ``npm run validate:circuits``, which re-checks every
stored circuit with the pipeline's own ``validate_logical_gate_h``.

Selection (the generating-set policy): identity actions are dropped, one
circuit is kept per distinct logical action (which provably preserves the
generated logical group), and full-group codes are further cut to the
certificate's verified generating prefix (``C_generators_used`` — its exact
Schreier-Sims run proved that prefix generates Sp(2k,2); median 6 per code).
Order-free-certified and QLDPC codes keep every distinct action.
``--all-circuits`` disables the prefix cut. Runs reconcile: two-fold circuits
and seeded codes a re-run no longer keeps are pruned (other tools' files are
never touched). Circuit conversion fans out over --workers processes; all
writes stay in the main process.

Codes: all 136 are imported as visible entries with family tags and (where a
page was verified to exist) an Error Correction Zoo link. Codes already in
the library are deduplicated by canonical hash, then by a structural
permutation fit against every stored code with the same [[n,k,d]]; the gross
code additionally tries the offline sigma shared with the autqec import.

Usage:
  python rebuild_all.py                  # classify only (no writes)
  python rebuild_all.py --write
  python rebuild_all.py --codes "[[10,2,3]]eczoo:dd1f5a7f"
  python rebuild_all.py --file full     # or ldpc / both
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import stim

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def _default_dataset() -> Path:
    """Find the two-fold-transversal checkout: sibling of the repo, walking up
    for worktrees."""
    for base in (REPO.parent, *REPO.parents):
        cand = base / "two-fold-transversal"
        if (cand / "data" / "full_codes_depth1.json").is_file():
            return cand
    return REPO.parent / "two-fold-transversal"


sys.path.insert(0, str(REPO))

from scripts.add_circuit.circuit_validate import (  # noqa: E402
    induced_logical_action,
    transversality_class,
)
from scripts.add_circuit.code_identify import split_h_to_css  # noqa: E402
from scripts.add_circuit.compute import compute_code_data_h, slugify  # noqa: E402
from scripts.add_circuit.compute_circuit import compute_circuit_data  # noqa: E402
from scripts.add_circuit.ids import next_qec_id  # noqa: E402
from scripts.add_circuit.matrix_format import decode as decode_matrix  # noqa: E402
from scripts.add_circuit.perm_find import find_code_permutation  # noqa: E402
from scripts.add_circuit.yaml_helpers import (  # noqa: E402
    build_circuit_yaml,
    build_code_yaml,
    build_original_yaml,
    dump_yaml,
    load_yaml,
    matrices_digest,
    write_file,
)

SOURCE = "https://arxiv.org/abs/2608.05688"
TOOL = "two-fold-transversal"

# Offline qubit permutations shared with the autqec import (sigma[new] = old).
# The gross code's labeling is common to autqec/qLDPC/QUITS; whether this
# dataset shares it is decided by sigma_verifies at runtime, never assumed.
AUTQEC_SIGMAS = REPO / "data-imports" / "autqec" / "sigma_precomputed.json"

TOK = re.compile(
    r"S(\d+)|V(\d+)|CZ<(\d+),(\d+)>|cz<(\d+),(\d+)>|CX<(\d+),(\d+)>|H(\d+)|(\^)|\(([\d,]+)\)"
)

# ---------------------------------------------------------------------------
# Families: label shorthand -> (display name, code tags, verified zoo URL).
# Names and descriptions follow the paper's Table III (paper/app_codes.tex);
# zoo URLs were fetch-verified on 2026-08-07 — absent means no page confirmed,
# not that none exists. `CSS`/`self-dual` are auto-detected by the pipeline
# and never hand-added. `LDPC` is added for ldpc_codes_depth1.json entries.
# ---------------------------------------------------------------------------
FAMILY = {
    "se": ("Self-Dual Even Code", [], ""),
    "ml": ("Self-Dual Doubly-Even Code", [], ""),
    "qecdb": ("qecdb.org Code", [], ""),
    "2bga": (
        "Two-Block Group-Algebra Code",
        ["two-block-group-algebra"],
        "https://errorcorrectionzoo.org/c/2bga",
    ),
    "coset2bga": ("Coset Two-Block Group-Algebra Code", ["two-block-group-algebra"], ""),
    "toricdir": (
        "Bivariate Bicycle Code",
        ["bivariate-bicycle-code"],
        "https://errorcorrectionzoo.org/c/qcga",
    ),
    "kasai": ("Affine Block-Circulant Code", [], ""),
    "cc": ("Clustered-Cyclic Code", [], ""),
    "copycup": (
        "Abelian Balanced-Product Code",
        ["balanced-product"],
        "https://errorcorrectionzoo.org/c/balanced_product",
    ),
    "mm": ("Multivariate Multicycle Code", [], ""),
    "dd422": ("[[4,2,2]]-Concatenated Symplectic Double", ["concatenated"], ""),
}

# eczoo entries are individual named codes, keyed by their uuid octet. The two
# [[10,2,3]] entries are told apart by their check weights (the rotated toric
# code has the weight-4, degree-4 checks).
ECZOO = {
    "dd1f5a7f": ("Rotated Toric Code", "https://errorcorrectionzoo.org/c/toric"),
    "1cdbcad5": ("Binarized Galois-Qudit Code", "https://errorcorrectionzoo.org/c/stab_10_2_3"),
    "880eb7d7": (
        "Constant-Excitation Phantom Code",
        "https://errorcorrectionzoo.org/c/constant_excitation",
    ),
    "9a9707b2": ("Carbon Code", "https://errorcorrectionzoo.org/c/carbon"),
}

# cons: constructions, keyed by construction tag (with trailing digits for the
# parameterized families).
CONS = {
    "blk45k12": ("qecdb.org Block Code", [], ""),
    "blk45k18": ("qecdb.org Block Code", [], ""),
    "qrm6": ("Middle Reed-Muller Code QRM(6)", ["reed-muller"], ""),
    "johnson16": ("Cut-Complement Code", [], ""),
    "concat112": ("Concatenation-Lift Code", ["concatenated", "reed-muller"], ""),
    "gross144": (
        "Gross Code",
        ["bivariate-bicycle-code"],
        "https://errorcorrectionzoo.org/c/gross",
    ),
}
CONS_PREFIX = [
    ("grid", "Bipartite Grid Code", [], ""),
    ("quadric", "Quadric Tower Code", [], ""),
    (
        "sdbb",
        "Self-Dual Bivariate Bicycle Code",
        ["bivariate-bicycle-code"],
        "https://errorcorrectionzoo.org/c/qcga",
    ),
]

STRUCTURE_POLICY = {
    "transversal": ("Transversal", ["transversal", "ft"]),
    "swap-transversal": ("SWAP-transversal", ["swap-transversal"]),
    "general": ("Depth-one two-local", []),
}

_qec_id_re = re.compile(r"^qec_id:\s*(\d+)\s*$", re.MULTILINE)
_label_re = re.compile(r"^\[\[(\d+),(\d+),(\d+)\]\](\w+):([\w.-]+)$")

PRETTY = {
    "S": "S",
    "SQRT_X": "√X",
    "CX": "CNOT",
    "CZ": "CZ",
    "XCX": "C(X,X)",
    "H": "H",
    "SWAP": "SWAP",
    "X": "X",
    "Y": "Y",
    "Z": "Z",
    "C_XYZ": "Γ(XYZ)",
    "C_ZYX": "Γ(XZY)",
}


# ---------------------------------------------------------------------------
# Dataset parsing
# ---------------------------------------------------------------------------
def pauli_vec(s: str, n: int) -> np.ndarray:
    """Pauli string ("Z0Z2Z3") -> symplectic row vector (x | z)."""
    v = np.zeros(2 * n, dtype=int)
    consumed = 0
    for m in re.finditer(r"([XYZ])(\d+)", s):
        consumed += len(m.group(0))
        p, q = m.group(1), int(m.group(2))
        if p in "XY":
            v[q] ^= 1
        if p in "ZY":
            v[n + q] ^= 1
    if consumed != len(s.replace(" ", "")):
        raise ValueError(f"unparsed Pauli string: {s!r}")
    return v


def perm_from_cycles(cycles: list[list[int]], n: int) -> list[int]:
    """p[i] = where qubit i's operator ends up; cycle (a,b,c) = a->b->c->a."""
    p = list(range(n))
    for cyc in cycles:
        for idx in range(len(cyc)):
            p[cyc[idx]] = cyc[(idx + 1) % len(cyc)]
    return p


def perm_to_swaps(p: list[int]) -> list[tuple[int, int]]:
    """Decompose permutation p (i -> p[i]) into SWAPs, applied in list order."""
    swaps: list[tuple[int, int]] = []
    seen = [False] * len(p)
    for start in range(len(p)):
        if seen[start] or p[start] == start:
            seen[start] = True
            continue
        cyc = [start]
        seen[start] = True
        q = p[start]
        while q != start:
            cyc.append(q)
            seen[q] = True
            q = p[q]
        for i in range(len(cyc) - 2, -1, -1):
            swaps.append((cyc[i], cyc[i + 1]))
    return swaps


def gate_string_to_stim(s: str, n: int) -> stim.Circuit:
    """One dataset gate string -> STIM circuit on n qubits (permutation last)."""
    circ = stim.Circuit()
    cycles: list[list[int]] = []
    consumed = 0
    for m in TOK.finditer(s or ""):
        consumed += len(m.group(0))
        if m.group(1) is not None:
            circ.append("S", [int(m.group(1))])
        elif m.group(2) is not None:
            circ.append("SQRT_X", [int(m.group(2))])
        elif m.group(3) is not None:
            circ.append("CZ", [int(m.group(3)), int(m.group(4))])
        elif m.group(5) is not None:
            circ.append("XCX", [int(m.group(5)), int(m.group(6))])
        elif m.group(7) is not None:
            circ.append("CX", [int(m.group(7)), int(m.group(8))])
        elif m.group(9) is not None:
            circ.append("H", [int(m.group(9))])
        elif m.group(10) is not None:  # '^' — layout only
            continue
        elif m.group(11) is not None:
            cycles.append([int(x) for x in m.group(11).split(",")])
    if consumed != len((s or "").replace(" ", "")):
        raise ValueError(f"unparsed gate string: {s!r}")
    for a, b in perm_to_swaps(perm_from_cycles(cycles, n)):
        circ.append("SWAP", [a, b])
    if circ.num_qubits < n:
        circ.append("I", [n - 1])
    return circ


# ---------------------------------------------------------------------------
# Fast logical action (batched GF(2) solve)
# ---------------------------------------------------------------------------
def stim_symplectic(body: str, n: int) -> np.ndarray:
    """2n x 2n binary symplectic action of a unitary STIM body, row-vector
    (x | z) convention."""
    circ = stim.Circuit(body)
    if circ.num_qubits < n:
        circ.append("I", [n - 1])
    tab = circ.to_tableau()
    M = np.zeros((2 * n, 2 * n), dtype=np.uint8)
    for q in range(n):
        for row, out in ((q, tab.x_output(q)), (n + q, tab.z_output(q))):
            xs, zs = out.to_numpy()
            M[row, :n] = xs
            M[row, n:] = zs
    return M


def batched_logical_action(M: np.ndarray, h: np.ndarray, logical: np.ndarray, n: int):
    """Induced logical action of physical symplectic M, in the basis of
    ``logical``'s rows — same convention as the pipeline's
    ``induced_logical_action``, computed as ONE batched GF(2) solve instead of
    per-row Gaussian elimination. Returns the 2k x 2k matrix, or an error str.

    Solves x·A = w for A = [logical; h] and every image row w = L_i·M at once.
    [logical; h] has full row rank (logicals independent mod stabilizers), so
    the solution is unique and the first 2k coefficients are the action."""
    two_k = logical.shape[0]
    W = (logical.astype(np.uint8) @ M) % 2
    A = np.vstack([logical, h]).astype(np.uint8) % 2
    aug = np.hstack([A.T.copy(), W.T.copy()])  # 2n x (rows(A) + 2k)
    cols = A.shape[0]
    r = 0
    piv: dict[int, int] = {}
    for c in range(cols):
        hit = np.nonzero(aug[r:, c])[0]
        if hit.size == 0:
            continue
        pr = r + hit[0]
        if pr != r:
            aug[[r, pr]] = aug[[pr, r]]
        mask = aug[:, c].astype(bool)
        mask[r] = False
        aug[mask] ^= aug[r]
        piv[c] = r
        r += 1
    lhs_zero = ~aug[:, :cols].any(axis=1)
    if aug[lhs_zero][:, cols:].any():
        return "failed: image of a logical is outside the normalizer span"
    if len(piv) != cols:
        return "failed: [logical; h] not full rank"
    x = np.zeros((cols, two_k), dtype=np.uint8)
    for c, pr in piv.items():
        x[c] = aug[pr, cols:]
    return x[:two_k].T % 2


def action_from_u(u: np.ndarray, k: int) -> tuple[str, str, list[str]]:
    """Binary symplectic logical action -> (stim_text, pretty, logical-op tags).

    Signs chosen +: the stored frames are sign-free, so the action is only
    defined up to logical Paulis. Decomposition via stim's tableau elimination.
    """

    def to_pauli(row: np.ndarray) -> stim.PauliString:
        ps = stim.PauliString(k)
        for j in range(k):
            ps[j] = {(0, 0): 0, (1, 0): 1, (1, 1): 2, (0, 1): 3}[(int(row[j]), int(row[k + j]))]
        return ps

    tab = stim.Tableau.from_conjugated_generators(
        xs=[to_pauli(u[j]) for j in range(k)],
        zs=[to_pauli(u[k + j]) for j in range(k)],
    )
    circ = tab.to_circuit("elimination")
    lines, parts, ops = [], [], []
    for instr in circ:
        if instr.name == "I":
            continue
        for group in instr.target_groups():
            qs = [t.value for t in group]
            lines.append(f"{instr.name} " + " ".join(str(q) for q in qs))
            label = PRETTY.get(instr.name, instr.name)
            if k == 1:
                parts.append(label)
            else:
                parts.append(f"{label}({','.join(str(q) for q in qs)})")
            ops.append(instr.name)
    text = "\n".join(lines)
    pretty = "·".join(parts) if parts else "identity"
    tags = [f"logical-op:{name}" for name in dict.fromkeys(ops)]
    return text, pretty, tags


def classify_u(u: np.ndarray, k: int) -> tuple[str, str, int]:
    """Classify a logical action by the paper's own layer taxonomy.

    The 2k x 2k symplectic u in blocks [[A, B], [C, D]] (X-bar images on top):
    returns (tag-slug, display label, support = number of logical qubits acted
    on non-trivially). This is what makes hundreds of same-code circuits
    distinguishable — the gate list of stim's elimination decomposition is an
    artifact of the decomposition, not of the action.
    """
    A, B = u[:k, :k], u[:k, k:]
    C, D = u[k:, :k], u[k:, k:]
    eye = np.eye(k, dtype=u.dtype)
    ident_rows = np.concatenate(
        [
            (u[:k] == np.hstack([eye, 0 * eye])).all(axis=1),
            (u[k:] == np.hstack([0 * eye, eye])).all(axis=1),
        ]
    )
    support = int(sum(1 for j in range(k) if not (ident_rows[j] and ident_rows[k + j])))
    if not C.any() and not B.any():
        if ((A.sum(axis=0) == 1).all() and (A.sum(axis=1) == 1).all()) and np.array_equal(D, A):
            return "permutation", "qubit permutation", support
        return "cnot", "CNOT circuit", support
    if np.array_equal(A, eye) and np.array_equal(D, eye) and not C.any():
        return "z-diagonal", "Z-diagonal (S/CZ) gate", support
    if np.array_equal(A, eye) and np.array_equal(D, eye) and not B.any():
        return "x-diagonal", "X-diagonal (√X/XX) gate", support
    if not A.any() and not D.any():
        return "h-type", "Hadamard-type gate", support
    return "general", "Clifford", support


# ---------------------------------------------------------------------------
# Worker: convert + classify one chunk of gate strings for one code
# ---------------------------------------------------------------------------
def process_chunk(task: dict) -> list[dict]:
    """Runs in a worker process. Returns one record per gate string:
    {"index", "skip": "identity"} or the full circuit dict (sans qec_id)."""
    n, k = task["n"], task["k"]
    h = np.array(task["h"], dtype=int)
    logical = np.array(task["logical"], dtype=int)
    perm = task["perm"]
    out = []
    for i, gate_string in task["gens"]:
        paper_stim = gate_string_to_stim(gate_string, n)
        final = compute_circuit_data(
            str(paper_stim),
            qubit_permutation=perm,
            circuit_name="placeholder",
            source=SOURCE,
            tool=TOOL,
        )
        body = next(b["body"] for b in final["bodies"] if b["format"] == "stim")
        u = batched_logical_action(stim_symplectic(body, n), h, logical, n)
        if isinstance(u, str):
            raise AssertionError(f"{task['label']} gen {i}: {u}")
        if task["selfcheck"]:
            ref = induced_logical_action(body, h, logical, n)
            assert not isinstance(ref, str) and np.array_equal(u, ref % 2), (
                f"{task['label']} gen {i}: batched action disagrees with pipeline"
            )
            task["selfcheck"] = False
        if np.array_equal(u, np.eye(2 * k, dtype=np.uint8)):
            out.append({"index": i, "skip": "identity"})
            continue

        action_text, pretty, op_tags = action_from_u(u, k)
        cls_tag, cls_label, support = classify_u(u, k)
        struct, struct_tags = STRUCTURE_POLICY[transversality_class(paper_stim)]
        if len(pretty) <= 48:
            # Short enough to name by the exact action; the op tags of its
            # decomposition are faithful at this size.
            circ_name = f"{struct} logical {pretty}"
            class_tags = [f"logical-class:{cls_tag}", *op_tags]
        else:
            # Long decompositions are artifacts of the elimination routine, so
            # the name states the action's structural class and support, and
            # the misleading per-op tags are dropped in favour of the class.
            circ_name = f"{struct} logical {cls_label} on {support}/{k} qubits (gen {i})"
            class_tags = [f"logical-class:{cls_tag}"]
        action_summary = (
            f"Logical {pretty} (gates in application order)"
            if len(pretty) <= 160
            else f"Logical {cls_label} acting on {support} of the {k} logical qubits"
        )
        notes = (
            f"{action_summary}, from generator {i} "
            f"of dataset entry {task['label']} ({task['file']}) of arXiv:2608.05688. "
            "The physical circuit is depth-one two-local (two-fold transversal): "
            "one layer in which each qubit is touched by at most one two-qubit "
            "gate; a trailing SWAP network, where present, is the string's "
            "compensating qubit permutation. The dataset is binary-symplectic "
            f"(sign-free), so the circuit is one Pauli frame of the gate — "
            f"{task['claim_note']}. The logical_action field states the claim in "
            "the stored code's logical basis; validate:circuits checks it."
        )
        final["name"] = circ_name
        final["slug"] = slugify(circ_name)
        final["notes"] = notes
        final["tags"] = ["logical-gate", "two-fold-transversal", *struct_tags, *class_tags]
        final["logical_action"] = action_text
        out.append({"index": i, "final": final, "body": body, "original_stim": str(paper_stim)})
    return out


# ---------------------------------------------------------------------------
# Code naming / fitting helpers
# ---------------------------------------------------------------------------
def family_of(label: str) -> tuple[str, str, list[str], str, str]:
    """label -> (source, display name, family tags, zoo_url, uuid octet/tag)."""
    m = _label_re.match(label)
    if not m:
        raise ValueError(f"unparsed label: {label!r}")
    n, k, d, src, ident = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4), m.group(5)
    params = f"[[{n},{k},{d}]]"
    if src == "eczoo":
        name, zoo = ECZOO[ident]
        return src, name, [], zoo, ident
    if src == "cons":
        if ident in CONS:
            name, tags, zoo = CONS[ident]
        else:
            for prefix, pname, ptags, pzoo in CONS_PREFIX:
                if ident.startswith(prefix):
                    name, tags, zoo = pname, ptags, pzoo
                    break
            else:
                raise ValueError(f"unknown construction: {ident!r}")
        return src, f"{name} {params}", tags, zoo, ident
    name, tags, zoo = FAMILY[src]
    return src, f"{name} {params}", tags, zoo, ident


def _gf2_rref(mat: np.ndarray) -> np.ndarray:
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
    """Relabeling H by sigma (sigma[new] = old) gives the stored row space?"""
    perm = np.array(sigma, dtype=int)
    H_p = np.zeros_like(H)
    H_p[:, np.arange(n)] = H[:, perm]
    H_p[:, np.arange(n) + n] = H[:, perm + n]
    a, b = _gf2_rref(H_p), _gf2_rref(stored_h)
    return a.shape == b.shape and np.array_equal(a, b)


# The structural finder is a search: it costs ~10s per FAILED attempt at
# n=22 and does not terminate in reasonable time on automorphism-rich codes
# at n=64 (one such pair hung a full run). Every known true fit onto a
# pre-existing code is tiny (carbon n=12, the 16-2-4/16-6-4/20-2-6 refusals)
# or covered by an offline sigma (gross, n=144), so the finder only runs
# below this bound; larger hash-missed codes are imported as new with a
# printed note, the qLDPC-refutation precedent for offline verification.
FIT_SEARCH_MAX_N = 20


class StoredIndex:
    """(n,k,d) -> [(slug, h)] over the codes that existed BEFORE this run.

    Codes seeded by this run are deliberately NOT candidates: the dataset's
    uuid registry already asserts its entries are pairwise distinct codes,
    and the se/ml/dd422 sweeps share parameters constantly — fitting each
    new entry against its same-parameter predecessors is what made a full
    run spend 34 minutes on doomed permutation searches."""

    def __init__(self, data_dir: Path):
        self.by_params: dict[tuple[int, int, int], list[tuple[str, np.ndarray]]] = {}
        for code_file in sorted((data_dir / "codes").glob("*.yaml")):
            stored = load_yaml(code_file.read_text())
            if "h" not in stored:  # placeholder codes (flag-gadgets) have no matrices
                continue
            key = (stored.get("n"), stored.get("k"), stored.get("d"))
            h = np.array(decode_matrix(stored["h"]), dtype=int)
            self.by_params.setdefault(key, []).append((code_file.stem, h))

    def fit(self, H: np.ndarray, n: int, k: int, d: int):
        """Structural fallback when the canonical-hash dedup misses. Returns
        (slug, sigma) or None."""
        precomputed = json.loads(AUTQEC_SIGMAS.read_text()) if AUTQEC_SIGMAS.exists() else {}
        for slug, h_stored in self.by_params.get((n, k, d), []):
            if slug in precomputed and sigma_verifies(H, h_stored, n, precomputed[slug]):
                return slug, precomputed[slug]
            if n > FIT_SEARCH_MAX_N:
                print(
                    f"   note: same-params stored code {slug} not fitted "
                    f"(finder skipped at n={n} > {FIT_SEARCH_MAX_N}); importing as "
                    "a distinct code — verify offline if identity is suspected"
                )
                continue
            css_mine = split_h_to_css(H, n)
            css_stored = split_h_to_css(h_stored, n)
            if css_mine is not None and css_stored is not None:
                sigma = find_code_permutation(*css_mine, *css_stored)
                if sigma is not None and sigma_verifies(H, h_stored, n, sigma):
                    return slug, sigma
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dataset", default=str(_default_dataset()))
    ap.add_argument("--data-dir", default=str(REPO / "data_yaml"))
    ap.add_argument("--codes", nargs="*", help="only these dataset labels")
    ap.add_argument("--file", choices=("full", "ldpc", "both"), default="both")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument(
        "--all-circuits",
        action="store_true",
        help="import every distinct-action circuit instead of the generating-set policy",
    )
    args = ap.parse_args()

    dataset = Path(args.dataset)
    if not (dataset / "data" / "full_codes_depth1.json").is_file():
        sys.exit(f"dataset not found at {dataset} — clone valbert4/two-fold-transversal there")
    data_dir = Path(args.data_dir)

    # The certificate's verified generating prefix per full-group code: after
    # dropping identity images and duplicate logical actions, its Schreier-Sims
    # run (gaporder.py) proved the first C_generators_used distinct actions
    # already generate Sp(2k,2). None = the code was certified by an order-free
    # method, so no prefix exists and every distinct action is kept.
    cert_path = dataset / "data" / "certify" / "certificate_depth1_Sp.json"
    prefix_of: dict[str, int | None] = {
        e["label"]: e.get("C_generators_used") for e in json.loads(cert_path.read_text())["codes"]
    }

    # Slug assignment must not depend on leftovers of earlier runs: only codes
    # tracked in git (the real pre-import library) block the plain n-k-d slug.
    try:
        import subprocess

        tracked_code_slugs = {
            Path(p).stem
            for p in subprocess.run(
                ["git", "ls-files", "data_yaml/codes/"],
                capture_output=True,
                text=True,
                check=True,
                cwd=REPO,
            ).stdout.splitlines()
        }
    except Exception:
        tracked_code_slugs = {p.stem for p in (data_dir / "codes").glob("*.yaml")}

    files = []
    if args.file in ("full", "both"):
        files.append(("full", dataset / "data" / "full_codes_depth1.json"))
    if args.file in ("ldpc", "both"):
        files.append(("ldpc", dataset / "data" / "ldpc_codes_depth1.json"))

    stats = {"written": 0, "trivial": 0, "deduped": 0, "codes_new": 0, "codes_existing": 0}
    used_names: dict[str, str] = {}
    used_slugs: dict[str, str] = {}
    qec_counter = next_qec_id(data_dir)  # incremented locally; scans once
    index = StoredIndex(data_dir)
    pool = ProcessPoolExecutor(max_workers=args.workers)
    t_start = time.time()

    for which, path in files:
        claim_note = (
            "the paper's certificate verifies the full recorded generator set "
            "realizes the full logical Clifford group Sp(2k,2)"
            if which == "full"
            else "the paper's certificate verifies the exact order of the logical "
            "group the full recorded generator set realizes"
        )
        for entry in json.loads(path.read_text()):
            label = entry["label"]
            if args.codes and label not in args.codes:
                continue
            t0 = time.time()
            n, k, d = entry["n"], entry["k"], entry["d"]
            src, name, fam_tags, zoo, ident = family_of(label)
            if which == "ldpc" and "LDPC" not in fam_tags:
                fam_tags = [*fam_tags, "LDPC"]

            S = np.array([pauli_vec(s, n) for s in entry["isotropic_generators"]], dtype=int)
            L = np.array([pauli_vec(s, n) for s in entry["logical_ops"]], dtype=int)
            assert S.shape == (n - k, 2 * n), f"{label}: stabilizer count"
            assert L.shape == (2 * k, 2 * n), f"{label}: logical count"

            if name in used_names and used_names[name] != label:
                name = f"{name} ({ident})"
            used_names.setdefault(name, label)

            base = f"{n}-{k}-{d}"
            slug_pref = base
            if base in tracked_code_slugs or (
                slug_pref in used_slugs and used_slugs[slug_pref] != label
            ):
                slug_pref = f"{base}-{src}"
            if slug_pref in used_slugs and used_slugs[slug_pref] != label:
                slug_pref = f"{base}-{src}-{ident}"

            code_result = compute_code_data_h(
                S, n, d, code_name=name, zoo_url=zoo, data_dir=str(data_dir), code_slug=slug_pref
            )
            code = code_result["code"]
            slug = code["slug"]
            perm = code_result["qubit_permutation"]

            if code["status"] == "new":
                fitted = index.fit(S, n, k, d)
                if fitted is not None:
                    slug, perm = fitted
                    code["status"] = "existing"
                    print(f"== {label} -> {slug} (existing, structural fit)")
                else:
                    used_slugs[slug] = label
                    stats["codes_new"] += 1
                    for tag in fam_tags:
                        if tag not in [t["name"] for t in code.get("tags", [])]:
                            code.setdefault("tags", []).append({"name": tag})
                    if args.write:
                        write_file(
                            data_dir / "codes" / f"{slug}.yaml",
                            dump_yaml(build_code_yaml(code)),
                            quiet=True,
                        )
                    print(f"== {label} -> {slug} (new)")
            else:
                print(f"== {label} -> {slug} ({code['status']})")
            if code["status"] == "existing":
                stats["codes_existing"] += 1
            # Later same-params entries must not claim this slug, whether it
            # was seeded now or matched an existing file.
            used_slugs.setdefault(slug, label)

            code_path = data_dir / "codes" / f"{slug}.yaml"
            if not code_path.exists():
                if args.write:
                    sys.exit(f"{label}: code file {code_path} missing after seed")
                # Dry run for a new code: its canonical form is not on disk
                # yet, but compute_code_data_h returned it — and `perm`
                # already maps the dataset frame onto it.
                stored = code
            else:
                stored = load_yaml(code_path.read_text())
            h_stored = np.array(decode_matrix(stored["h"]), dtype=int)
            logical_stored = np.array(decode_matrix(stored["logical"]), dtype=int)

            original_yaml = build_original_yaml({"h": S.tolist(), "logical": L.tolist()})
            digest = matrices_digest(original_yaml) if original_yaml else None
            if args.write and original_yaml:
                write_file(
                    data_dir / "matrices" / f"{digest}.yaml", dump_yaml(original_yaml), quiet=True
                )

            # Fan the gate strings out over the worker pool.
            gens = list(enumerate(entry["depth1_clif_generators"]))
            chunk_size = max(1, min(48, (len(gens) + args.workers - 1) // args.workers))
            base_task = {
                "n": n,
                "k": k,
                "h": h_stored.tolist(),
                "logical": logical_stored.tolist(),
                "perm": perm,
                "label": label,
                "file": path.name,
                "claim_note": claim_note,
            }
            futures = []
            for start in range(0, len(gens), chunk_size):
                task = dict(
                    base_task, gens=gens[start : start + chunk_size], selfcheck=(start == 0)
                )
                futures.append(pool.submit(process_chunk, task))

            records = [rec for f in futures for rec in f.result()]
            records.sort(key=lambda rec: rec["index"])

            # Selection: drop identities, dedupe by induced logical action
            # (equal action text = equal action; dropping duplicates cannot
            # change the generated logical group), then — unless
            # --all-circuits — cut full-group codes at the certificate's
            # verified generating prefix. Order-free and QLDPC codes keep
            # every distinct action, the strongest reduction that provably
            # preserves their recorded group.
            prefix = None if args.all_circuits else prefix_of.get(label)
            kept, seen_actions = [], set()
            for rec in records:
                if rec.get("skip") == "identity":
                    stats["trivial"] += 1
                    continue
                action = rec["final"]["logical_action"]
                if action in seen_actions:
                    stats["deduped"] += 1
                    continue
                seen_actions.add(action)
                kept.append(rec)
            if prefix is not None and len(kept) > prefix:
                stats["beyond_prefix"] = stats.get("beyond_prefix", 0) + len(kept) - prefix
                kept = kept[:prefix]
            if prefix is not None:
                selection_note = (
                    f" This circuit is part of the certificate's verified generating "
                    f"prefix: the paper's exact Schreier-Sims certificate confirms the "
                    f"logical actions of these {len(kept)} circuits generate the full "
                    "logical Clifford group Sp(2k,2)."
                )
            else:
                selection_note = (
                    " One circuit per distinct logical action is kept from the recorded "
                    "generator set; dropping duplicate actions preserves the generated "
                    "logical group."
                )

            slug_counts: dict[str, int] = {}
            code_written = 0
            kept_stems: set[str] = set()
            for rec in kept:
                final = rec["final"]
                final["notes"] += selection_note
                base_slug = final["slug"]
                slug_counts[base_slug] = slug_counts.get(base_slug, 0) + 1
                if slug_counts[base_slug] > 1:
                    final["name"] = f"{final['name']} ({slug_counts[base_slug]})"
                    final["slug"] = f"{base_slug}-{slug_counts[base_slug]}"
                stem = f"{slug}--{final['slug']}"
                kept_stems.add(stem)
                if args.write:
                    circuits_dir = data_dir / "circuits"
                    existing = circuits_dir / f"{stem}.yaml"
                    prev = _qec_id_re.search(existing.read_text()) if existing.exists() else None
                    if prev:
                        final["qec_id"] = int(prev.group(1))
                    else:
                        final["qec_id"] = qec_counter
                        qec_counter += 1
                    circuit_yaml = build_circuit_yaml(final)
                    if digest:
                        circuit_yaml["original_matrices"] = digest
                    write_file(circuits_dir / f"{stem}.yaml", dump_yaml(circuit_yaml), quiet=True)
                    for b in final.get("bodies", []):
                        if b.get("body"):
                            write_file(
                                circuits_dir / f"{stem}.{b['format']}", b["body"], quiet=True
                            )
                    write_file(
                        circuits_dir / "originals" / f"{stem}.original.stim",
                        rec["original_stim"],
                        quiet=True,
                    )
                stats["written"] += 1
                code_written += 1

            # Reconcile: any two-fold circuit of this code that this run did
            # not keep is a leftover of an earlier run or policy — remove it.
            # Circuits from other tools sharing the code are never touched.
            if args.write:
                circuits_dir = data_dir / "circuits"
                for stale_yaml in sorted(circuits_dir.glob(f"{slug}--*.yaml")):
                    stem = stale_yaml.stem
                    if stem in kept_stems:
                        continue
                    if f"tool: {TOOL}" not in stale_yaml.read_text():
                        continue
                    for path_ in (
                        stale_yaml,
                        circuits_dir / f"{stem}.stim",
                        circuits_dir / f"{stem}.qasm",
                        circuits_dir / f"{stem}.stim-annotated",
                        circuits_dir / "originals" / f"{stem}.original.stim",
                    ):
                        path_.unlink(missing_ok=True)
                    stats["pruned"] = stats.get("pruned", 0) + 1
            print(
                f"   {'wrote' if args.write else 'ok'} {code_written} circuits"
                f" in {time.time() - t0:.1f}s"
            )

    # Global reconcile (full runs only — a --codes/--file subset run sees only
    # part of the dataset and must not judge the rest): remove code entries an
    # earlier run seeded under a slug no current entry claims, with their
    # circuits, and matrices files nothing references anymore. Only files not
    # tracked in git are candidates — the pre-import library is never touched.
    if args.write and not args.codes and args.file == "both":
        import subprocess

        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard", "data_yaml/"],
            capture_output=True,
            text=True,
            cwd=REPO,
        ).stdout.splitlines()
        for rel in untracked:
            p = REPO / rel
            if p.parent == data_dir / "codes" and p.suffix == ".yaml":
                if p.stem in used_slugs:
                    continue
                for circ_yaml in sorted((data_dir / "circuits").glob(f"{p.stem}--*.yaml")):
                    stem = circ_yaml.stem
                    for path_ in (
                        circ_yaml,
                        data_dir / "circuits" / f"{stem}.stim",
                        data_dir / "circuits" / f"{stem}.qasm",
                        data_dir / "circuits" / f"{stem}.stim-annotated",
                        data_dir / "circuits" / "originals" / f"{stem}.original.stim",
                    ):
                        path_.unlink(missing_ok=True)
                    stats["pruned"] = stats.get("pruned", 0) + 1
                p.unlink()
                stats["codes_pruned"] = stats.get("codes_pruned", 0) + 1
        referenced = set()
        for circ_yaml in (data_dir / "circuits").glob("*.yaml"):
            m = re.search(r"^original_matrices: (\S+)$", circ_yaml.read_text(), re.M)
            if m:
                referenced.add(m.group(1))
        for rel in untracked:
            p = REPO / rel
            if p.parent == data_dir / "matrices" and p.stem not in referenced:
                p.unlink()
                stats["matrices_pruned"] = stats.get("matrices_pruned", 0) + 1

    pool.shutdown()
    print(f"\n{stats}  ({time.time() - t_start:.0f}s total)")


if __name__ == "__main__":
    main()
