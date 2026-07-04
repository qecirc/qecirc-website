# MQT FT State-Prep Import Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Import 51 non-deterministic FT state-prep circuits (`eval/`, arXiv:2408.11894) and 18 deterministic worst-case FT state-prep circuits (`eval_det/`, arXiv:2501.05527) from the MQT QECC repo into `data_yaml/`, seeding 3 new codes and adding a reusable structural permutation finder.

**Architecture:** A new reusable `scripts/add_circuit/perm_find.py` finds qubit permutations between equivalent CSS codes (Sendrier-style support splitting + low-weight-codeword invariants + pruned backtracking — prototype already validated on all 3 hard codes). A dataset-specific driver `data-imports/mqt-ftsp/rebuild_all.py` (mirroring `data-imports/rlftqc/rebuild_all.py`) imports both parts through the existing `scripts.add_circuit.import_state_prep` pipeline. eval_det bodies are built as worst-case execution traces from `results.csv` protocol data.

**Tech Stack:** Python (numpy, stim — already deps), existing `scripts/add_circuit` pipeline, pytest for the reusable component.

**Spec:** `docs/superpowers/specs/2026-07-04-mqt-ftsp-import-design.md`

**Dataset:** clone of `https://github.com/munich-quantum-toolkit/qecc` sitting at `../qecc` relative to the repo root (already cloned at `/tmp/mqt-qecc` for development; the driver expects `REPO.parent / "qecc"` — copy or re-clone before the final run: `git clone --depth 1 https://github.com/munich-quantum-toolkit/qecc ../qecc`).

**Pre-validated facts (do not re-derive):**

- Fit results per eval/ dir: steane+shor identity; hamming/cc_4_8_8/cc_6_6_6/cc_4_8_8_d7 self-dual hash dedup; rotated_surface_d3 n≤9 search; tetrahedral/carbon/rotated_surface_d5 need σ.
- Found + circuit-validated σs (`sigma[new] = old`, MQT labeling → stored labeling):
  - tetrahedral → tetrahedral-code: `(0, 1, 8, 2, 9, 10, 3, 4, 12, 14, 7, 13, 6, 5, 11)`
  - carbon → carbon-code: `(0, 3, 1, 4, 2, 5, 6, 9, 7, 10, 8, 11)`
  - rotated_surface_d5 → rotated-surface-code-d-5: `(8, 18, 24, 2, 12, 21, 6, 16, 22, 17, 13, 0, 10, 5, 1, 20, 15, 9, 4, 19, 14, 23, 11, 7, 3)`
- Defective files (defer, do not import): `eval/circuits/rotated_surface_d3/zero_non_ft_heuristic.stim` (invalid: odd CX target count) and `eval/circuits/hamming/plus_ft_heuristic_opt.stim` (violates a Z-stabilizer).
- eval_det: 18 qasm files, all bare h+cx; CSV row exists for every file; variant preference global → optimal → heuristic; only `carbon zero_heuristic` lacks a global row.

---

### Task 1: Structural permutation finder (`perm_find.py`) — TDD

**Files:**

- Create: `scripts/add_circuit/perm_find.py`
- Modify: `scripts/add_circuit/__init__.py` (re-export)
- Test: `scripts/tests/test_perm_find.py`

- [ ] **Step 1: Write the failing tests**

```python
# scripts/tests/test_perm_find.py
"""Tests for the structural permutation finder."""

import numpy as np
import pytest

from scripts.add_circuit.perm_find import find_code_permutation

STEANE_H = np.array([
    [0, 0, 0, 1, 1, 1, 1],
    [0, 1, 1, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1],
])

# MQT carbon code (from mqt-qecc src/mqt/qecc/codes/carbon/{hx,hz}.npy)
CARBON_HX = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
])
CARBON_HZ = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
])
# NOTE: verify these fixture literals against the .npy files before first
# test run: np.load('/tmp/mqt-qecc/src/mqt/qecc/codes/carbon/hx.npy').
# If they differ, replace the literals with the actual arrays.


def _rowspace_rref(m: np.ndarray) -> np.ndarray:
    from scripts.add_circuit.code_identify import gf2_rref
    r = gf2_rref(np.asarray(m) % 2)
    return r[~np.all(r == 0, axis=1)]


def _assert_maps(hx1, hz1, hx2, hz2, sigma):
    p = np.array(sigma)
    assert np.array_equal(_rowspace_rref(hx1[:, p]), _rowspace_rref(hx2))
    assert np.array_equal(_rowspace_rref(hz1[:, p]), _rowspace_rref(hz2))


def test_identity_on_steane():
    sigma = find_code_permutation(STEANE_H, STEANE_H, STEANE_H, STEANE_H)
    assert sigma is not None
    _assert_maps(STEANE_H, STEANE_H, STEANE_H, STEANE_H, sigma)


def test_relabeled_steane_roundtrip():
    rng = np.random.default_rng(42)
    perm = rng.permutation(7)
    hx1 = STEANE_H[:, perm]
    sigma = find_code_permutation(hx1, hx1, STEANE_H, STEANE_H)
    assert sigma is not None
    _assert_maps(hx1, hx1, STEANE_H, STEANE_H, sigma)


def test_relabeled_carbon_roundtrip():
    rng = np.random.default_rng(7)
    perm = rng.permutation(12)
    hx1, hz1 = CARBON_HX[:, perm], CARBON_HZ[:, perm]
    sigma = find_code_permutation(hx1, hz1, CARBON_HX, CARBON_HZ)
    assert sigma is not None
    _assert_maps(hx1, hz1, CARBON_HX, CARBON_HZ, sigma)


def test_inequivalent_returns_none():
    # Steane vs a code with an extra independent row: not equivalent.
    other = np.vstack([STEANE_H, np.array([[1, 1, 0, 0, 0, 0, 0]])])
    sigma = find_code_permutation(STEANE_H, STEANE_H, other, other)
    assert sigma is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `UV_NO_CONFIG=1 uv run pytest scripts/tests/test_perm_find.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.add_circuit.perm_find'`

- [ ] **Step 3: Implement `perm_find.py`**

The prototype was validated in-session (tetrahedral 7s, carbon 7s, surface-d5 0.1s with codeword invariants). Implementation combines BOTH invariant families:

```python
# scripts/add_circuit/perm_find.py
"""Structural qubit-permutation finder between equivalent CSS codes.

Given two CSS codes as (Hx, Hz) row spaces over GF(2), find a qubit
permutation sigma (convention: sigma[new] = old) such that permuting the
columns of code 1 yields the row spaces of code 2.

Approach (independent implementation; inspired by N. Sendrier, "Finding the
Permutation Between Equivalent Linear Codes: The Support Splitting
Algorithm", and benchmarking in github.com/MaxieHelenBichmann/bm_qecc):

1. Per-column invariants from two families:
   a. single/pair puncture ranks of Hx and Hz (always available), and
   b. per-column / per-pair incidence histograms of low-weight codewords
      (weight <= CODEWORD_WMAX), enumerated when rank <= CODEWORD_RANK_MAX.
      Family (b) is what makes highly symmetric LDPC codes (e.g. rotated
      surface) tractable.
2. Weisfeiler-Leman colour refinement using the pair invariants.
3. Most-constrained-first backtracking with pair-invariant consistency and
   incremental prefix-rank pruning; a full row-space equality check accepts
   the final candidate. The caller MUST still verify the returned sigma
   (add_circuit's row-space check does this) — this module never bypasses
   verification.
"""

from __future__ import annotations

import itertools
from collections import Counter
from typing import Optional

import numpy as np

from .code_identify import gf2_rank, gf2_rref

CODEWORD_WMAX = 6
CODEWORD_RANK_MAX = 16
DEFAULT_BUDGET = 3_000_000


def _rowspace_key(m: np.ndarray) -> tuple[bytes, tuple[int, int]]:
    r = gf2_rref(np.asarray(m) % 2)
    r = r[~np.all(r == 0, axis=1)]
    return r.tobytes(), r.shape


def _puncture_rank(m: np.ndarray, cols: set[int]) -> int:
    keep = [c for c in range(m.shape[1]) if c not in cols]
    return gf2_rank(m[:, keep])


def _all_words(m: np.ndarray) -> np.ndarray:
    """All codewords of the row space (requires rank <= CODEWORD_RANK_MAX)."""
    r = gf2_rref(np.asarray(m) % 2)
    r = r[~np.all(r == 0, axis=1)].astype(np.uint8)
    k, n = r.shape
    words = np.zeros((1, n), dtype=np.uint8)
    for b in range(k):
        words = np.vstack([words, words ^ r[b]])
    return words


def _invariants(hx: np.ndarray, hz: np.ndarray):
    """Per-column colours and per-pair labels from both invariant families."""
    n = hx.shape[1]
    col: dict[int, tuple] = {i: () for i in range(n)}
    pair: dict[tuple[int, int], tuple] = {
        (i, j): () for i, j in itertools.combinations(range(n), 2)
    }
    for m in (hx, hz):
        # family (a): puncture ranks
        for i in range(n):
            col[i] += (_puncture_rank(m, {i}),)
        for i, j in itertools.combinations(range(n), 2):
            pair[(i, j)] += (_puncture_rank(m, {i, j}),)
        # family (b): low-weight codeword incidence
        if gf2_rank(m) <= CODEWORD_RANK_MAX:
            words = _all_words(m)
            wts = words.sum(axis=1)
            sel = words[(wts > 0) & (wts <= CODEWORD_WMAX)]
            swts = sel.sum(axis=1)
            for i in range(n):
                col[i] += (tuple(sorted(int(w) for w, row in zip(swts, sel) if row[i])),)
            for i, j in itertools.combinations(range(n), 2):
                pair[(i, j)] += (
                    tuple(sorted(int(w) for w, row in zip(swts, sel) if row[i] and row[j])),
                )
    # WL refinement
    colors = dict(col)
    for _ in range(n):
        new = {}
        for i in range(n):
            nb = tuple(
                sorted(
                    (pair[tuple(sorted((i, j)))], colors[j]) for j in range(n) if j != i
                )
            )
            new[i] = hash((colors[i], nb))
        if len(set(new.values())) <= len(set(colors.values())):
            break
        colors = new
    return colors, pair


def find_code_permutation(
    hx1: np.ndarray,
    hz1: np.ndarray,
    hx2: np.ndarray,
    hz2: np.ndarray,
    budget: int = DEFAULT_BUDGET,
) -> Optional[list[int]]:
    """Find sigma (sigma[new] = old) with rowspace(H1[:, sigma]) == rowspace(H2).

    Returns None if no permutation is found (inequivalent codes, or search
    budget exceeded).
    """
    hx1 = np.asarray(hx1, dtype=int) % 2
    hz1 = np.asarray(hz1, dtype=int) % 2
    hx2 = np.asarray(hx2, dtype=int) % 2
    hz2 = np.asarray(hz2, dtype=int) % 2
    n = hx1.shape[1]
    if hx2.shape[1] != n or hz1.shape[1] != n or hz2.shape[1] != n:
        return None
    if gf2_rank(hx1) != gf2_rank(hx2) or gf2_rank(hz1) != gf2_rank(hz2):
        return None

    c1, p1 = _invariants(hx1, hz1)
    c2, p2 = _invariants(hx2, hz2)
    if Counter(c1.values()) != Counter(c2.values()):
        return None

    cands = {j: frozenset(i for i in range(n) if c1[i] == c2[j]) for j in range(n)}
    target_x, target_z = _rowspace_key(hx2), _rowspace_key(hz2)
    sigma: list[Optional[int]] = [None] * n
    used: set[int] = set()
    assigned: list[int] = []
    steps = 0

    def prefix_ok() -> bool:
        old_cols = [sigma[j] for j in assigned]
        return gf2_rank(hx1[:, old_cols]) == gf2_rank(hx2[:, assigned]) and gf2_rank(
            hz1[:, old_cols]
        ) == gf2_rank(hz2[:, assigned])

    def next_col() -> int:
        best, best_avail = -1, n + 1
        for j in range(n):
            if sigma[j] is not None:
                continue
            avail = sum(1 for i in cands[j] if i not in used)
            if avail < best_avail:
                best, best_avail = j, avail
        return best

    def backtrack() -> bool:
        nonlocal steps
        if len(assigned) == n:
            p = np.array(sigma)
            return (
                _rowspace_key(hx1[:, p]) == target_x
                and _rowspace_key(hz1[:, p]) == target_z
            )
        j = next_col()
        for i in cands[j]:
            if i in used:
                continue
            if not all(
                p1[tuple(sorted((i, sigma[jj])))] == p2[tuple(sorted((j, jj)))]
                for jj in assigned
            ):
                continue
            steps += 1
            if steps > budget:
                raise TimeoutError
            sigma[j] = i
            used.add(i)
            assigned.append(j)
            if prefix_ok() and backtrack():
                return True
            sigma[j] = None
            used.discard(i)
            assigned.pop()
        return False

    try:
        found = backtrack()
    except TimeoutError:
        return None
    return [int(x) for x in sigma] if found else None  # type: ignore[arg-type]
```

Add to `scripts/add_circuit/__init__.py` (alongside the existing re-exports):

```python
from .perm_find import find_code_permutation
```

and append `"find_code_permutation"` to `__all__` if the module defines one.

- [ ] **Step 4: Verify fixture literals, run tests**

First verify the carbon fixture matches reality:
Run: `UV_NO_CONFIG=1 uv run python -c "import numpy as np; print(np.load('/tmp/mqt-qecc/src/mqt/qecc/codes/carbon/hx.npy').astype(int).tolist()); print(np.load('/tmp/mqt-qecc/src/mqt/qecc/codes/carbon/hz.npy').astype(int).tolist())"`
If output differs from the test literals, update the literals to match.

Run: `UV_NO_CONFIG=1 uv run pytest scripts/tests/test_perm_find.py -v`
Expected: 4 PASS

- [ ] **Step 5: Lint and full Python test suite**

Run: `UV_NO_CONFIG=1 uv run ruff check scripts/ && UV_NO_CONFIG=1 uv run ruff format scripts/ && UV_NO_CONFIG=1 uv run pytest -q`
Expected: ruff clean, all tests pass (160 existing + 4 new).

- [ ] **Step 6: Commit**

```bash
git add scripts/add_circuit/perm_find.py scripts/add_circuit/__init__.py scripts/tests/test_perm_find.py
git commit -m "feat(add-circuit): structural permutation finder for equivalent CSS codes"
```

---

### Task 2: Driver — Part 1 (eval/) import

**Files:**

- Create: `data-imports/mqt-ftsp/rebuild_all.py`

- [ ] **Step 1: Write the driver with Part 1 support**

Follow `data-imports/rlftqc/rebuild_all.py` structurally (read it first). Key content:

```python
#!/usr/bin/env python
"""MQT FT state-prep import: eval/ (arXiv:2408.11894) + eval_det/ (arXiv:2501.05527).

Usage:
  python rebuild_all.py                 # classify only (no writes)
  python rebuild_all.py --write         # import into the repo's data_yaml
  python rebuild_all.py --write --data-dir /tmp/dt
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
DATASET = REPO.parent / "qecc"  # clone of munich-quantum-toolkit/qecc
EVAL = DATASET / "scripts/ft_stateprep/eval/circuits"
EVAL_DET = DATASET / "scripts/ft_stateprep/eval_det"
sys.path.insert(0, str(REPO))

import stim  # noqa: E402

from scripts.add_circuit import (  # noqa: E402
    find_code_permutation,
    import_state_prep,
)
from scripts.add_circuit.code_identify import split_h_to_css  # noqa: E402

SOURCE_EVAL = "https://arxiv.org/abs/2408.11894"
SOURCE_DET = "https://arxiv.org/abs/2501.05527"

# Files that are defective in the source repo (verified 2026-07-04; see README).
DEFECTIVE = {
    "rotated_surface_d3/zero_non_ft_heuristic.stim",  # truncated mid-verification
    "hamming/plus_ft_heuristic_opt.stim",  # prepared state violates a Z-stabilizer
}


@dataclass
class EvalCode:
    slug: str          # stored code slug in data_yaml/codes/
    n: int
    d: int
    fit: str           # "identity" | "search" | "self_dual" | "perm_find"
    mqt_dir: str = ""  # matrices dir under DATASET/src/mqt/qecc/codes/ (perm_find only)


EVAL_CODES: dict[str, EvalCode] = {
    "steane": EvalCode("steane-code", 7, 3, "identity"),
    "shor": EvalCode("shor-code", 9, 3, "identity"),
    "rotated_surface_d3": EvalCode("rotated-surface-code-d-3", 9, 3, "search"),
    "rotated_surface_d5": EvalCode(
        "rotated-surface-code-d-5", 25, 5, "perm_find", "rotated_surface_d5"
    ),
    "hamming": EvalCode("15-7-3", 15, 3, "self_dual"),
    "tetrahedral": EvalCode("tetrahedral-code", 15, 3, "perm_find", "tetrahedral"),
    "carbon": EvalCode("carbon-code", 12, 4, "perm_find", "carbon"),
    "cc_4_8_8": EvalCode("17-1-5", 17, 5, "self_dual"),
    "cc_6_6_6": EvalCode("19-1-5", 19, 5, "self_dual"),
    "cc_4_8_8_d7": EvalCode("31-1-7", 31, 7, "self_dual"),
}


def anchor_h(slug: str, data_dir: Path) -> np.ndarray:
    doc = yaml.safe_load((data_dir / "codes" / f"{slug}.yaml").read_text())
    return np.asarray(doc["h"], dtype=int)


def sigma_for(code: EvalCode, data_dir: Path) -> list[int] | None:
    """Compute sigma once per code via the structural finder."""
    hx1 = np.load(DATASET / "src/mqt/qecc/codes" / code.mqt_dir / "hx.npy").astype(int)
    hz1 = np.load(DATASET / "src/mqt/qecc/codes" / code.mqt_dir / "hz.npy").astype(int)
    hx2, hz2 = split_h_to_css(anchor_h(code.slug, data_dir), code.n)
    return find_code_permutation(hx1, hz1, np.asarray(hx2), np.asarray(hz2))


def eval_name(fname: str) -> tuple[str, list[str], str]:
    """Parse eval filename -> (display name, tags, notes fragment).

    zero_ft_opt_opt         -> "FT zero (opt/opt)",  [ft, prep:opt, verification:opt]
    plus_non_ft_heuristic   -> "Non-FT plus (heuristic)", [non-ft, prep:heuristic]
    zero_ft_naive           -> "FT zero (naive)",    [ft, verification:naive]
    zero_ft_heuristic_mixed -> "FT zero (heuristic/mixed)"
    """
    stem = fname.removesuffix(".stim")
    state = "zero" if stem.startswith("zero") else "plus"
    rest = stem.removeprefix(f"{state}_")
    if rest.startswith("non_ft_"):
        prep = rest.removeprefix("non_ft_")
        return (
            f"Non-FT {state} ({prep})",
            ["state-preparation", "non-ft", f"prep:{prep}"],
            f"non-FT prep, synthesis method: {prep}",
        )
    rest = rest.removeprefix("ft_")
    parts = rest.split("_")
    if len(parts) == 1:  # e.g. zero_ft_naive
        verify = parts[0]
        return (
            f"FT {state} ({verify})",
            ["state-preparation", "ft", f"verification:{verify}"],
            f"FT prep with {verify} verification",
        )
    prep, verify = parts[0], parts[1]
    return (
        f"FT {state} ({prep}/{verify})",
        ["state-preparation", "ft", f"prep:{prep}", f"verification:{verify}"],
        f"FT prep (prep synthesis: {prep}, verification synthesis: {verify})",
    )


def run_eval(write: bool, data_dir: Path) -> None:
    sigmas: dict[str, list[int] | None] = {}
    report: list[str] = []
    imported = deferred = 0
    for dirname, code in EVAL_CODES.items():
        h = anchor_h(code.slug, data_dir)
        if code.fit == "perm_find":
            sigmas[dirname] = sigma_for(code, data_dir)
            if sigmas[dirname] is None:
                report.append(f"DEFER all {dirname}: permutation not found")
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
                gate_set=",".join(sorted({i.name for i in stim.Circuit(txt)})),
                tags=tags,
                notes=method_note,
                data_dir=str(data_dir),
            )
            if code.fit == "identity":
                kwargs.update(method="anchor", anchor_H=h, permutation=list(range(code.n)))
            elif code.fit == "perm_find":
                kwargs.update(method="anchor", anchor_H=h, permutation=sigmas[dirname])
            elif code.fit == "search":
                kwargs.update(method="anchor", anchor_H=h)  # n<=9: add_circuit searches
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
```

**Note on `method`/`permutation` kwargs:** check `import_state_prep`'s actual
behaviour before finalizing (read `scripts/add_circuit/state_prep.py:400-470`):

- `method="anchor"` + `permutation` uses the supplied σ (row-space verified).
- `method="anchor"` **without** permutation runs `fit_circuit_to_anchor`
  (exhaustive search, works for n≤9 — used for `rotated_surface_d3`). If the
  search path requires different arguments, mirror what
  `data-imports/rlftqc/rebuild_all.py` does for its `9-1-3-surface` case.
- `method="self_dual"` derives matrices from the circuit and dedups by
  canonical hash. **For `plus` circuits of self-dual codes**, verify on one
  hamming plus file that `derive_matrices_self_dual` works; if it fails for
  plus states, fall back to `method="anchor"` with a σ obtained by running
  `find_code_permutation` on that code (matrices from
  `DATASET/src/mqt/qecc/codes/hamming_15/` etc. — same mechanism as
  `perm_find` codes).

Also add the `main()` / argparse block (copy the shape from rlftqc's driver, adding an `--only eval|det` flag for incremental testing).

- [ ] **Step 2: Classify-only run**

```bash
git clone --depth 1 https://github.com/munich-quantum-toolkit/qecc ../qecc  # if not present
UV_NO_CONFIG=1 uv run python data-imports/mqt-ftsp/rebuild_all.py --only eval
```

Expected output: `eval/: classified=51 deferred=2`, the 2 DEFER lines naming the defective files, no FAIL lines, and σs found for tetrahedral/carbon/rotated_surface_d5.

- [ ] **Step 3: Write to a scratch copy and validate**

```bash
cp -r data_yaml /tmp/dt-eval
UV_NO_CONFIG=1 uv run python data-imports/mqt-ftsp/rebuild_all.py --only eval --write --data-dir /tmp/dt-eval
```

Expected: `imported=51 deferred=2`. Spot-check one imported YAML (e.g. a steane `FT zero (opt/opt)`) for name, tags (`ft`, `prep:opt`, `verification:opt`, `logical-state:zero`), `tool: mqt-qecc`, `source`, and an `originals/` entry.

- [ ] **Step 4: Commit the driver**

```bash
git add data-imports/mqt-ftsp/rebuild_all.py
git commit -m "feat(import): MQT ft-stateprep eval driver (51 circuits, 2 defective deferred)"
```

---

### Task 3: eval_det protocol parser + worst-case body builder

**Files:**

- Create: `data-imports/mqt-ftsp/det_protocol.py`

- [ ] **Step 1: Write the module**

```python
"""Parse eval_det/results.csv protocol data and build worst-case Stim bodies.

Layer semantics (state_prep_det.py): for |0>_L layer 0 measures Z-stabilizers
(detects X errors), layer 1 X-stabilizers; for |+>_L swapped. Each layer:
round-1 verification stabs (always measured, hook flags where marked), then —
per round-1 outcome — round-2 stabs and a Pauli correction chosen by the
round-2 outcome. The stored body linearizes the WORST branch (max round-2
CNOTs, tie-break max correction weight, hook branches included).

Verification measurement sub-circuit ordering is ported verbatim from
simulation_det.py::_create_stab_measurement_circuit:
  - one measurement ancilla per stab, flag ancillas AFTER all measurement
    ancillas of the block;
  - stab support iterated in ascending qubit order;
  - X-stabs: H on ancilla before and after the CX chain; CX anc->data.
    Z-stabs: CX data->anc;
  - flagged stabs: flag opens before the 2nd data CX and closes before the
    LAST data CX (Z: H flag; CX flag->anc ... CX flag->anc; H flag,
    X: CX anc->flag ... CX anc->flag);
  - all ancillas of a block measured together at block end (MR in stim).
Ancilla indices restart at n for every block (MR frees them), so
qubit_count = n + max block width.
"""

from __future__ import annotations

import ast
import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import stim


# ---------- CSV parsing ----------

def _parse_np(cell: str):
    """Parse a numpy-repr CSV cell like "[array([0, 1, ...]), ...]" or
    "{1: ([array(...)], {0: array(...), 1: array(...)}), ...}"."""
    cleaned = re.sub(r"array\(", "np.array(", cell)
    cleaned = re.sub(r",\s*dtype=int8", "", cleaned)
    return eval(cleaned, {"np": np})  # noqa: S307 - trusted repo data


@dataclass
class Layer:
    stabs: list[np.ndarray]                     # round-1 verification stabs
    flagged: list[bool]                          # hook flag per stab
    corrections: dict[int, tuple[list[np.ndarray], dict[int, np.ndarray]]]
    hook_corrections: list[dict]                 # per-stab hook branch tables


@dataclass
class DetProtocol:
    variant: str                                 # heuristic | optimal | global
    layers: tuple[Layer, Layer]


def load_protocols(csv_path: Path) -> dict[tuple[str, bool, str], dict[str, DetProtocol]]:
    """-> {(code, zero_state, procedure): {variant: DetProtocol}}"""
    out: dict = {}
    for row in csv.DictReader(csv_path.open()):
        key = (row["code"], row["zero_state"] == "True", row["procedure"])
        layers = []
        for idx in (0, 1):
            stabs = _parse_np(row[f"verification_stabs_{idx}"])
            corrections = _parse_np(row[f"recovery_stabs_{idx}"])
            flags_raw = _parse_np(row[f"flags_{idx}"])
            # flags cell is either [False, False] (no hooks) or a list of
            # per-stab dicts (hook branch tables); normalize:
            if isinstance(flags_raw, list) and flags_raw and isinstance(flags_raw[0], dict):
                hook_corrections = flags_raw
            else:
                hook_corrections = [{}] * len(stabs)
            flagged = [bool(h) for h in hook_corrections]
            layers.append(Layer(stabs, flagged, corrections or {}, hook_corrections))
        out.setdefault(key, {})[row["verification"]] = DetProtocol(
            row["verification"], (layers[0], layers[1])
        )
    return out


VARIANT_PREFERENCE = ("global", "optimal", "heuristic")


def pick_variant(variants: dict[str, DetProtocol]) -> DetProtocol:
    for v in VARIANT_PREFERENCE:
        if v in variants:
            return variants[v]
    raise KeyError(f"no known variant among {sorted(variants)}")


# ---------- qasm -> stim prep ----------

def qasm_prep_to_stim(qasm: str) -> stim.Circuit:
    """Convert the bare h/cx OPENQASM 2.0 encoders to stim (verified: the 18
    eval_det files contain only qreg/h/cx lines)."""
    ops = []
    for line in qasm.splitlines():
        line = line.strip().rstrip(";")
        if m := re.fullmatch(r"h q\[(\d+)\]", line):
            ops.append(f"H {m.group(1)}")
        elif m := re.fullmatch(r"cx q\[(\d+)\],\s*q\[(\d+)\]", line):
            ops.append(f"CX {m.group(1)} {m.group(2)}")
        elif line.startswith(("OPENQASM", "include", "qreg")) or not line:
            continue
        else:
            raise ValueError(f"unexpected qasm line: {line!r}")
    return stim.Circuit("\n".join(ops))


# ---------- worst-case body ----------

def _support(vec: np.ndarray) -> list[int]:
    return [int(i) for i in np.flatnonzero(np.asarray(vec) % 2)]


def _measure_block(stabs, flagged, z_stabs: bool, n: int) -> tuple[stim.Circuit, int]:
    """Port of _create_stab_measurement_circuit; returns (circuit, block_width)."""
    c = stim.Circuit()
    num_stabs = len(stabs)
    anc = n                                   # measurement ancillas: n .. n+num_stabs-1
    flag = n + num_stabs                      # flag ancillas after
    measured: list[int] = []
    for s_idx, (stab, has_flag) in enumerate(zip(stabs, flagged)):
        a = n + s_idx
        sup = _support(stab)
        if not z_stabs:
            c.append("H", [a])
        for q_idx, q in enumerate(sup):
            if has_flag and q_idx == 1:
                if z_stabs:
                    c.append("H", [flag])
                    c.append("CX", [flag, a])
                else:
                    c.append("CX", [a, flag])
            if has_flag and q_idx == len(sup) - 1:
                if z_stabs:
                    c.append("CX", [flag, a])
                    c.append("H", [flag])
                else:
                    c.append("CX", [a, flag])
            c.append("CX", [q, a] if z_stabs else [a, q])
        if not z_stabs:
            c.append("H", [a])
        measured.append(a)
        if has_flag:
            measured.append(flag)
            flag += 1
    c.append("MR", sorted(measured))
    return c, (flag - n)


def worst_branch(layer: Layer):
    """Pick the most expensive branch across det + hook corrections.

    Returns (round2_stabs, correction_vec) or None if the layer is trivial.
    Cost = (sum of round-2 stab support sizes i.e. CNOTs, correction weight).
    """
    best = None
    tables = [layer.corrections] + [h for h in layer.hook_corrections if h]
    for table in tables:
        for _outcome, (stabs2, recs) in table.items():
            cnots = sum(len(_support(s)) for s in stabs2)
            for _o2, corr in recs.items():
                cost = (cnots, len(_support(corr)))
                if best is None or cost > best[0]:
                    best = (cost, stabs2, corr)
    if best is None:
        return None
    return best[1], best[2]


def build_worst_case_body(
    prep: stim.Circuit, proto: DetProtocol, n: int, zero_state: bool
) -> tuple[stim.Circuit, dict]:
    """prep -> layer0 verification -> worst branch (round2 + Pauli) -> layer1 ...

    Returns (circuit, stats) where stats counts verification/correction CNOTs
    and max ancilla block width for the consistency gate.
    """
    body = stim.Circuit()
    body += prep
    stats = {"cnots": 0, "max_width": 0}
    for layer_idx, layer in enumerate(proto.layers):
        z_stabs = zero_state if layer_idx == 0 else not zero_state
        if layer.stabs:
            blk, width = _measure_block(layer.stabs, layer.flagged, z_stabs, n)
            body += blk
            stats["max_width"] = max(stats["max_width"], width)
            stats["cnots"] += sum(len(_support(s)) for s in layer.stabs)
        wb = worst_branch(layer)
        if wb is not None:
            stabs2, corr = wb
            blk, width = _measure_block(stabs2, [False] * len(stabs2), z_stabs, n)
            body += blk
            stats["max_width"] = max(stats["max_width"], width)
            stats["cnots"] += sum(len(_support(s)) for s in stabs2)
            sup = _support(corr)
            if sup:
                # correction Paulis: X corrections fix X-detected... the
                # correction acts in the SAME basis as the errors the layer
                # detects: layer measuring Z-stabs detects X errors -> X corr.
                body.append("X" if z_stabs else "Z", sup)
    return body, stats


# ---------- notes rendering ----------

def render_notes(proto: DetProtocol, zero_state: bool, source_file: str) -> str:
    lines = [
        "Deterministic FT state preparation (arXiv:2501.05527). The stored body",
        "and metrics show the WORST-CASE branch of an adaptive protocol (fair-",
        "comparison convention): prep, then per layer the always-measured",
        "round-1 verification and the most expensive outcome branch (round-2",
        "measurements + Pauli correction). The actual protocol branches on",
        "measurement outcomes as tabulated below.",
        f"Verification variant: {proto.variant}. Source file: {source_file}.",
    ]
    for idx, layer in enumerate(proto.layers):
        z = zero_state if idx == 0 else not zero_state
        basis = "Z" if z else "X"
        lines.append(f"— Layer {idx} ({basis}-stabilizer verification) —")
        if not layer.stabs:
            lines.append("  (trivial: no verification measurements)")
            continue
        for i, s in enumerate(layer.stabs):
            flag = " [hook flag]" if layer.flagged[i] else ""
            lines.append(f"  round-1 stab {i}: {basis}{_support(s)}{flag}")
        for outcome, (stabs2, recs) in sorted(layer.corrections.items()):
            lines.append(f"  outcome {outcome:b}:")
            for s in stabs2:
                lines.append(f"    measure {basis}{_support(s)}")
            for o2, corr in sorted(recs.items()):
                p = "X" if z else "Z"
                lines.append(f"    -> outcome {o2:b}: apply {p}{_support(corr)}")
        for i, hooks in enumerate(layer.hook_corrections):
            for outcome, (stabs2, recs) in sorted(hooks.items()) if hooks else []:
                lines.append(f"  hook flag of stab {i}, outcome {outcome:b}:")
                for s in stabs2:
                    lines.append(f"    measure {basis}{_support(s)}")
                for o2, corr in sorted(recs.items()):
                    p = "X" if z else "Z"
                    lines.append(f"    -> outcome {o2:b}: apply {p}{_support(corr)}")
    return "\n".join(lines)
```

**Correction-basis check:** before trusting `"X" if z_stabs else "Z"`, verify
against `simulation_det.py::return_correction` (read it: it builds the
correction circuit given `zero_state`) — if it applies the opposite Pauli,
flip the condition here AND in `render_notes`.

- [ ] **Step 2: Smoke-test the parser standalone**

```bash
UV_NO_CONFIG=1 uv run python - <<'PYEOF'
import sys; sys.path.insert(0, '.')
sys.path.insert(0, 'data-imports/mqt-ftsp')
from pathlib import Path
from det_protocol import load_protocols, pick_variant, qasm_prep_to_stim, build_worst_case_body, render_notes
protos = load_protocols(Path('../qecc/scripts/ft_stateprep/eval_det/results.csv'))
print(len(protos), "protocol groups (expect 18)")
key = ('steane', True, 'opt')
p = pick_variant(protos[key])
print("steane variant:", p.variant)
prep = qasm_prep_to_stim(Path('../qecc/scripts/ft_stateprep/eval_det/circuits/steane/zero_opt.qasm').read_text())
body, stats = build_worst_case_body(prep, p, 7, True)
print(body)
print(stats)
print(render_notes(p, True, 'circuits/steane/zero_opt.qasm')[:400])
PYEOF
```

Expected: 18 groups; a valid stim circuit with H/CX/MR and a Pauli correction; readable notes. Manually sanity-check the steane output: round-1 verification stabs should match `verification_stabs_*` in the steane/opt CSV row.

- [ ] **Step 3: Commit**

```bash
git add data-imports/mqt-ftsp/det_protocol.py
git commit -m "feat(import): eval_det protocol parser and worst-case body builder"
```

---

### Task 4: Driver — Part 2 (eval_det/) import + new codes

**Files:**

- Modify: `data-imports/mqt-ftsp/rebuild_all.py`

- [ ] **Step 1: Extract the three new-code matrices**

The Hx=Hz matrices for `11_1_3`, `16_2_4`, `hypercube` are hard-coded in
`../qecc/scripts/ft_stateprep/eval_det/eval.py`. Read that file and copy the
literals into the driver as numpy arrays:

```python
# In rebuild_all.py — matrices copied verbatim from eval_det/eval.py (MIT).
NEW_CODES = {
    "11_1_3": dict(slug="11-1-3", name="[[11,1,3]]", n=11, d=3, hx=np.array([...])),
    "16_2_4": dict(slug="16-2-4", name="[[16,2,4]]", n=16, d=4, hx=np.array([...])),
    "hypercube": dict(
        slug="16-6-4", name="Tesseract Code", n=16, d=4, hx=np.array([...]),
        zoo_url="https://errorcorrectionzoo.org/c/stab_16_6_4",
    ),
}
# All three are self-dual: Hz = Hx.
```

(Use the exact arrays from eval.py — do not retype by hand; copy-paste.)

- [ ] **Step 2: Add `run_det()` to the driver**

```python
DET_CODES: dict[str, dict] = {
    # existing codes: reuse EVAL_CODES fit strategies
    "steane": dict(slug="steane-code", n=7, d=3, fit="identity"),
    "shor": dict(slug="shor-code", n=9, d=3, fit="identity"),
    "surface_3": dict(slug="rotated-surface-code-d-3", n=9, d=3, fit="search"),
    "tetrahedral": dict(slug="tetrahedral-code", n=15, d=3, fit="perm_find", mqt_dir="tetrahedral"),
    "carbon": dict(slug="carbon-code", n=12, d=4, fit="perm_find", mqt_dir="carbon"),
    "hamming": dict(slug="15-7-3", n=15, d=3, fit="self_dual"),
    # new codes: seeded on first import, identity by construction
    "11_1_3": dict(new=True, n=11, d=3),
    "16_2_4": dict(new=True, n=16, d=4),
    "hypercube": dict(new=True, n=16, d=4),
}


def det_procedure(fname: str) -> str:
    return "heuristic" if "heuristic" in fname else "opt"  # eval.py's rule


def run_det(write: bool, data_dir: Path) -> None:
    from det_protocol import (
        build_worst_case_body, load_protocols, pick_variant,
        qasm_prep_to_stim, render_notes,
    )
    protos = load_protocols(EVAL_DET / "results.csv")
    imported = deferred = 0
    report: list[str] = []
    for code_dir in sorted(p.name for p in (EVAL_DET / "circuits").iterdir() if p.is_dir()):
        cfg = DET_CODES[code_dir]
        for qasm_path in sorted((EVAL_DET / "circuits" / code_dir).glob("*.qasm")):
            rel = f"{code_dir}/{qasm_path.name}"
            state_zero = qasm_path.name.startswith("zero")
            proc = det_procedure(qasm_path.name)
            key = (code_dir, state_zero, proc)
            if key not in protos:
                report.append(f"DEFER {rel}: no CSV row")
                deferred += 1
                continue
            proto = pick_variant(protos[key])
            n = cfg["n"]
            prep = qasm_prep_to_stim(qasm_path.read_text())
            body, stats = build_worst_case_body(prep, proto, n, state_zero)
            # consistency gate: verification CNOTs from the protocol tables
            expected_cnots = sum(
                len(np.flatnonzero(s)) for layer in proto.layers for s in layer.stabs
            )
            got_verif_cnots = stats["cnots"]  # includes worst-branch round-2
            if got_verif_cnots < expected_cnots:
                report.append(f"DEFER {rel}: consistency gate (cnots {got_verif_cnots} < {expected_cnots})")
                deferred += 1
                continue
            state = "zero" if state_zero else "plus"
            name = f"Det FT {state} ({proc})"
            kwargs = dict(
                circuit=str(body),
                n=n,
                d=cfg["d"],
                code_name=cfg.get("name", ""),
                circuit_name=name,
                source=SOURCE_DET,
                tool="mqt-qecc",
                source_file=f"scripts/ft_stateprep/eval_det/circuits/{rel}",
                logical_state=state,
                connectivity="fully-connected",
                tags=["state-preparation", "ft", "deterministic",
                      f"prep:{proc}", f"verification:{proto.variant}"],
                notes=render_notes(proto, state_zero, rel),
                data_dir=str(data_dir),
            )
            if cfg.get("new"):
                nc = NEW_CODES[code_dir]
                kwargs.update(
                    method="self_dual",
                    code_name=nc["name"],
                    code_slug=nc["slug"],
                    zoo_url=nc.get("zoo_url", ""),
                )
            elif cfg["fit"] == "identity":
                h = anchor_h(cfg["slug"], data_dir)
                kwargs.update(method="anchor", anchor_H=h, permutation=list(range(n)))
            elif cfg["fit"] == "perm_find":
                h = anchor_h(cfg["slug"], data_dir)
                hx1 = np.load(DATASET / "src/mqt/qecc/codes" / cfg["mqt_dir"] / "hx.npy").astype(int)
                hz1 = np.load(DATASET / "src/mqt/qecc/codes" / cfg["mqt_dir"] / "hz.npy").astype(int)
                hx2, hz2 = split_h_to_css(h, n)
                sigma = find_code_permutation(hx1, hz1, np.asarray(hx2), np.asarray(hz2))
                if sigma is None:
                    report.append(f"DEFER {rel}: permutation not found")
                    deferred += 1
                    continue
                kwargs.update(method="anchor", anchor_H=h, permutation=sigma)
            elif cfg["fit"] == "search":
                kwargs.update(method="anchor", anchor_H=anchor_h(cfg["slug"], data_dir))
            else:
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
    print(f"eval_det/: {'imported' if write else 'classified'}={imported} deferred={deferred}")
    for line in report:
        print("  " + line)
```

**Two things to verify while wiring this up** (adjust if reality differs):

1. Whether `import_state_prep` accepts `code_slug`/`zoo_url` for new-code
   seeding with `method="self_dual"` — read its signature (lines 400–430 of
   `state_prep.py`); it does take `zoo_url` and `code_slug`. If seeding also
   needs `code_tags`, pass `code_tags=["CSS"]`.
2. The body contains measurements + Pauli corrections after them; confirm
   `validate:circuits` / `symplectic_validate` accepts it (the worst-case
   Pauli correction applied WITHOUT a preceding error makes the final state
   differ from the codespace by that Pauli!). **This is expected to fail
   validation** — the worst-case branch applies a correction for an error
   that didn't happen in the noiseless simulation. Resolution (pick during
   implementation, document in README):
   - Preferred: append the correction as `stim` classically-controlled ops
     (`CX rec[-k] q` etc.) conditioned on the round-2 ancilla measurement —
     in the noiseless run the measurements are trivial, so the state stays in
     the codespace AND the gates still count toward metrics.
   - If classically-controlled Paulis don't count in the metric computation
     (`compute_circuit.py`), fall back to plain Paulis + skip-validation flag
     if `import_state_prep` offers one; otherwise ask the maintainer.

- [ ] **Step 3: Classify + scratch write**

```bash
UV_NO_CONFIG=1 uv run python data-imports/mqt-ftsp/rebuild_all.py --only det
# Expected: eval_det/: classified=18 deferred=0
cp -r data_yaml /tmp/dt-det
UV_NO_CONFIG=1 uv run python data-imports/mqt-ftsp/rebuild_all.py --only det --write --data-dir /tmp/dt-det
# Expected: imported=18 deferred=0; three new code YAMLs (11-1-3, 16-2-4, 16-6-4)
```

Spot-check `/tmp/dt-det/codes/16-6-4.yaml` (name "Tesseract Code", zoo_url set)
and one circuit YAML's notes (protocol tables render readably).

- [ ] **Step 4: Commit**

```bash
git add data-imports/mqt-ftsp/rebuild_all.py
git commit -m "feat(import): eval_det deterministic worst-case import + 3 new codes"
```

---

### Task 5: README for the importer

**Files:**

- Create: `data-imports/mqt-ftsp/README.md`

- [ ] **Step 1: Write the README**

Follow `data-imports/rlftqc/README.md`'s structure. Must document:

- What the two parts are (papers, directories), expected `../qecc` layout, run commands.
- The worst-case-body convention for eval_det (and that notes carry the full adaptive protocol).
- Fit strategy per code (the table from the spec) incl. the three found σs.
- The 2 deferred defective files with their exact defects — flagged for an upstream mqt-qecc issue.
- Variant preference (global → optimal → heuristic) and the eval.py filename-parsing rule.
- The new codes seeded (11-1-3, 16-2-4, 16-6-4 Tesseract).
- Follow-up note: `find_code_permutation` can now unblock rlftqc's deferred [[25,1,5]] circuit.

- [ ] **Step 2: Commit**

```bash
git add data-imports/mqt-ftsp/README.md
git commit -m "docs(import): mqt-ftsp importer README"
```

---

### Task 6: Real import run + full validation

**Files:**

- Modifies (generated): `data_yaml/circuits/*`, `data_yaml/codes/*`, `data_yaml/circuits/originals/*`

- [ ] **Step 1: Fresh classify of both parts**

```bash
UV_NO_CONFIG=1 uv run python data-imports/mqt-ftsp/rebuild_all.py
```

Expected: eval classified=51 deferred=2, det classified=18 deferred=0.

- [ ] **Step 2: Real write**

```bash
UV_NO_CONFIG=1 uv run python data-imports/mqt-ftsp/rebuild_all.py --write
```

Expected: 69 circuits imported into `data_yaml/`, 3 new codes.

- [ ] **Step 3: Full validation suite**

```bash
npm run format
npm run validate:yaml
npm run validate:circuits
npm run db:create
npm run lint && npm run format:check
UV_NO_CONFIG=1 uv run pytest -q
```

Expected: all pass. `validate:circuits` validates encoding/state-prep circuits
against the code's check matrices — the eval `ft` circuits (with MR
verification) and the det worst-case bodies must pass; if the det bodies fail
per Task 4 note 2, resolve there before this step.

- [ ] **Step 4: Dev-server spot-check**

```bash
npx astro dev stop 2>/dev/null; npm run dev &
```

Check on `http://localhost:4321`:

- `/codes/steane-code` shows the new `FT zero (opt/opt)` etc. rows with tool → `/tools#mqt-qecc`.
- A `Det FT zero (opt)` circuit detail page renders the protocol notes readably.
- `/codes/16-6-4` exists (Tesseract Code) with its `Det FT zero (heuristic)` circuit.
- `/tools` shows MQT QECC's circuit count grew (37 → 106).

- [ ] **Step 5: Commit the data**

```bash
git add data_yaml/
git commit -m "feat(circuits): import MQT FT state-prep circuits (arXiv:2408.11894, arXiv:2501.05527)

51 non-deterministic FT/non-FT state-prep circuits (eval/) and 18
deterministic worst-case FT state-prep circuits (eval_det/), plus 3 new
codes: [[11,1,3]], [[16,2,4]], [[16,6,4]] Tesseract. Two defective
source files deferred (see data-imports/mqt-ftsp/README.md)."
```

---

### Task 7: PR

- [ ] **Step 1: Push and open PR**

```bash
git push -u origin feat/mqt-ftsp-import
gh pr create --title "feat(circuits): MQT QECC FT state-prep import (69 circuits, 3 new codes, perm finder)" --body "..."
```

PR body should summarize: the two papers, 51+18 circuits, worst-case-body convention, the new `find_code_permutation` component, the 2 deferred defective upstream files, and the validation results. End with the standard Claude Code attribution footer.

---

## Final state checklist (maps to spec)

- Structural permutation finder + tests — Task 1
- eval/ import, 51 circuits, 2 defective deferred, verified fit strategies — Task 2
- eval_det protocol parser, worst-case bodies, notes, consistency gate — Tasks 3–4
- 3 new codes seeded — Task 4
- README with deferrals + σs + follow-up — Task 5
- Full run + validations + dev-server check — Task 6
- No version bump (data-only) — per spec
