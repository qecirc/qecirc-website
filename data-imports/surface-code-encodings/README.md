# Surface code unitary encodings import (arXiv:2601.05113)

Imports the unitary Pauli-state preparation circuits from _"Unitary fault-tolerant
encoding of Pauli states in surface codes"_ — Colmenarez, Zen, Olle, Marquardt &
Müller, [arXiv:2601.05113](https://arxiv.org/abs/2601.05113) (8 Jan 2026).

The paper's scheme prepares `|0⟩_L` and `|+⟩_L` in rotated and unrotated surface
codes with **"stabilizer-expanding" circuits**: unitary, `O(d)` depth, and
distance-preserving — unlike prior unitary methods with constant fault distance.
It reports up to an order of magnitude lower logical error rates than
measurement-based encoding, which is the point for platforms where measurement is
expensive relative to gates.

## Dataset

Clone the artifact repo next to this one so the layout is
`…/surface_code_encodings/` beside `…/qecirc-website/`, or pass `--dataset PATH`.

```
surface_code_encodings/
├── clean_circuits/{rotated,unrotated}_surface_code/
│   ├── measurement_encoding/{X,Z}/            ← out of scope
│   ├── unitary_encoding_with_ancilla/{X,Z}/   ← imported
│   └── unitary_encoding_without_ancilla/{X,Z}/← imported
└── noisy_circuits/…                           ← out of scope (900 files)
```

`X` is `|+⟩_L` and `Z` is `|0⟩_L` — the folder names are the **basis, not the
gate**. Confirmed against the dataset's own `plot_main.py` loader, whose
docstring reads `state: 'X' for plus and 'Z' for zero state`.

**Scope: 40 of the 960 files.** 2 code types × 2 ancilla variants × 2 states ×
5 distances (`d = 3,5,7,9,11`). The 20 `measurement_encoding/` circuits are
excluded (this import is about the unitary scheme), as are the 900 noisy
circuits — those are 15 error rates per clean circuit for the paper's figures,
not distinct constructions.

## Run

```bash
python rebuild_all.py                   # classify only
python rebuild_all.py --write
python rebuild_all.py --only rotated-d7 # substring filter on spec.key
```

Then the standard chain:

```bash
npm run format && npm run validate:yaml && npm run validate:circuits && npm run db:create
```

## The two variants

Both are unitary and both are stabilizer-expanding, so neither word discriminates;
what differs is **how the intra-plaquette CNOTs are routed**, which is what the
names carry:

| Variant            | Circuit name              | Routing                                           | Connectivity needed                          |
| ------------------ | ------------------------- | ------------------------------------------------- | -------------------------------------------- |
| `with_ancilla/`    | `Ancilla-mediated … prep` | ancillas act as bridge qubits between data qubits | nearest-neighbour, planar 2D                 |
| `without_ancilla/` | `Direct … prep`           | two-qubit gates run directly between data qubits  | next-nearest-neighbour (plaquette diagonals) |

The paper frames the ancilla variant as _"fully compatible with planar 2D qubit
connectivity"_, eliminating next-nearest-neighbour requirements; the direct
variant targets platforms with reconfigurable connectivity (neutral atoms,
trapped ions).

Rotated-vs-unrotated and distance are already in the **code slug**, so circuit
names carry only state × routing — four names per code. The state is spelled
`zero` / `plus` rather than `|0⟩` because `slugify` strips non-alphanumerics
(`|0⟩ prep` → `0-prep`, and `|+⟩ prep` → `prep`, losing the state entirely).

## Codes

`n = d²` (rotated) and `n = d² + (d−1)²` (unrotated, the planar code with
boundaries). All ten derive as `[[n,1,d]]`, CSS, **not self-dual**.

| Code                                    | n                    | Status  | Fit                        |
| --------------------------------------- | -------------------- | ------- | -------------------------- |
| `rotated-surface-code-d-{3,5}`          | 9, 25                | stored  | precomputed σ              |
| `rotated-surface-code-d-{7,9}`          | 49, 81               | stored  | precomputed σ (external)   |
| `rotated-surface-code-d-11`             | 121                  | **new** | seeded, then canonicalized |
| `unrotated-surface-code-d-{3,5,7,9,11}` | 13, 41, 85, 145, 221 | **new** | seeded, then canonicalized |

Six new codes. The unrotated family is new to the library entirely; rotated
`d=11` extends the existing `d=3..9`. New codes reuse the stored naming
convention — display `name` repeats across sizes ("Rotated Surface Code") and
the slug carries the distance — and are tagged `[CSS, surface-code, topological]`
to match. Zoo: `/c/rotated_surface` for rotated, `/c/surface` (Kitaev surface
code, the parent entry that covers the unrotated version) for unrotated. There is
no Zoo entry for the planar variant specifically.

### Check matrices come from the circuits

No hand-written stabilizer definitions are needed, unlike
[`flag-at-origin`](../flag-at-origin/README.md), which had to lift the authors'
own stabilisers into `stabilizers.py`. The reason: a `|0⟩_L` circuit alone only
determines `⟨stabilisers, logical-Z⟩`, so `Hz` is unrecoverable for a
non-self-dual code — but **this dataset ships `|0⟩_L` and `|+⟩_L` in a shared
labeling**, so `derive_matrices_two_circuit` recovers `Hx` from the zero circuit
and `Hz` from the plus circuit. That the derivation succeeds is itself the proof
the two share a labeling (it raises when `Hx·Hzᵀ ≠ 0`).

Derivation always uses the **direct** circuits. `strip_flags` would drop the
ancilla-mediated variant's bridge gates and silently derive the wrong code. All
four circuits of a code share a data labeling — verified by
`symplectic_validate` passing for all 40 against the anchor derived from the
direct pair — so one anchor and one σ serve all four.

### Fit strategy

Convention `σ[new] = old`, verified by row-space equality at import regardless of
provenance, so a wrong σ fails loudly rather than corrupting the library.

- **New codes** — no σ. The anchor is derived in the paper's own labeling, so the
  circuit-to-anchor fit confirms identity on its first try. That is _not_ the end
  of it: `add_circuit` then canonicalizes the new code to the form its
  `canonical_hash` is taken over and relabels the circuit to match, so the stored
  code is in canonical form, not the paper's. The relabeling is recorded per
  circuit under "Canonicalization qubit permutation" in the notes, and the
  paper's own labeling survives in `circuits/originals/`.
- **`d=3`, `d=5`** — σ from `find_code_permutation` (0.1 s for `d=5`), cached in
  [`sigma_precomputed.json`](sigma_precomputed.json).
- **`d=7`, `d=9`** — `find_code_permutation` **cannot crack these**: surface codes
  are automorphism-rich, and a `d=7` search was abandoned after several minutes.
  The canonical-hash dedup reports `uncertain` for both — which is the useful
  signal that they **are** the stored codes, so `assume_new=True` would be
  actively wrong here (flag-at-origin's README records the mirror-image trap,
  where `[[25,1,5]]` was masked as new when it was really the d=5 rotated surface
  code). σ supplied externally, same route as that import's `31-1-7` — and, like
  that one, **returned in the opposite orientation** (`σ[old] = new`) and stored
  inverted via `np.argsort`. Both were verified against `Hx` _and_ `Hz` before
  being cached.

Only `Hx` is needed to pin σ, even though these codes are not self-dual: at `d=3`
a brute force over all 9! permutations finds 32 preserving `Hx` and the same 32
preserving `Hx` and `Hz` together, so `Hz` adds no constraint. The externally
found `d=7` / `d=9` σ — searched on `Hx` alone — satisfy `Hz` too, which is the
same result at scale.

Circuits whose code has no σ are **deferred, not guessed** — `rebuild_all.py`
reports them and continues.

## Decisions baked in

- **Terminal readout dropped.** Every one of the 40 files ends with `M`/`MX` on
  all data qubits plus `DETECTOR`s and `OBSERVABLE_INCLUDE` — the SPAM benchmark
  behind figures 5 and 9, not part of the encoding. The stored body is the prep
  alone, matching flag-at-origin and mqt-ftsp for the same circuit shape.

  Note what this does **not** mean: `circuits/originals/` holds the circuit
  _pre-canonicalization_ — as handed to `add_circuit`, before qubit relabeling —
  and what is handed over is already `prep_body()`-transformed. So the originals
  are the stripped prep in the paper's labeling, **not** the published file
  byte-for-byte. The dropped readout, the detectors, and the observable survive
  only in the upstream dataset; the exact file is identified by `Source file:` in
  each circuit's notes. Same for the other importers that pre-process a body.

- **Reset layer rewritten** to library convention: `RX` → `H`, `R` dropped
  (`|0…0⟩` is implicit in a stored body). This is also what makes the tableau
  well-defined for derivation, and it **fixes inflated qubit counts for free** —
  the rotated `Z` files reset `2d²−1` qubits and the unrotated files reset
  `(2d−1)²`, most never used. `d=5` direct stores `qubit_count: 25`, not 49.
- **`QUBIT_COORDS` kept** ([#107](https://github.com/qecirc/qecirc-website/issues/107)).
  The unrotated files carry the lattice layout; the rotated ones ship none, so
  20 of the 40 circuits have coordinates and 20 do not. That asymmetry is the
  upstream data's, not a decision. Coordinates flow into the Crumble link, which
  is what makes the layout visible there rather than an abstract gate list.

  Only coordinates for qubits the preparation **actually touches** are kept. The
  files declare one per grid site, including sites named solely in the dropped
  reset layer, and a `QUBIT_COORDS` target counts towards stim's `num_qubits` —
  so keeping all of them would put the inflated `qubit_count` straight back
  (unrotated d=3 direct: 25 rather than 13).

- **`partial-ft`, a new tag.** The library had only `ft` (509) and `non-ft` (251).
  Neither fits: the paper preserves fault distance _"only for the type of error
  that flips the corresponding codeword, for example, X errors when preparing the
  logical state |0⟩\_L"_, while for _"the complementary type of error … the
  effective fault distance is bounded"_. **Which** error type is protected follows
  from the state, so `logical-state:zero|plus` already carries it and no
  companion `x-type`/`z-type` tag is added.
- **`connectivity:2d-grid` on both variants.** Maintainer's call. Note this tag
  elsewhere in the library (23 rlftqc circuits) means _gates restricted to grid
  edges_, i.e. nearest-neighbour — which is true of the ancilla variant but not
  of the direct one, whose plaquette diagonals are not grid edges. The two
  variants are therefore distinguishable by **name only**, not by filter.
- **`ancilla_role="routing"`.** These circuits' ancillas are bridge qubits, not
  flag qubits. The pipeline previously inferred `flag` from `num_qubits > n`
  alone, which would have added all 20 ancilla-mediated circuits to a `flag`
  filter that 483 circuits rely on to mean a fault-tolerance claim. Fixed
  generally in `scripts/add_circuit/state_prep.py` (`ancilla_role`, default
  `"flag"` — existing importers unaffected); the notes label the qubits
  "Routing ancilla qubits" accordingly.
- **No tool.** The paper is standalone; no `tool:` field, so no `tool:*` tag.

## Fidelity check

The paper gives two-qubit gate counts for the rotated code as `(5t+3)(d−1)` with
ancilla and `(3t+1)(d−1)` without, where `t = ⌊(d−1)/2⌋`, and depth `5(d−1)` /
`3(d−1)`. **All 20 rotated circuits match on both counts**, as computed
independently by the pipeline from the stored bodies:

| d   | direct CX / depth | ancilla CX / depth |
| --- | ----------------- | ------------------ |
| 3   | 8 / 6             | 16 / 10            |
| 5   | 28 / 12           | 52 / 20            |
| 7   | 60 / 18           | 108 / 30           |
| 9   | 104 / 24          | 184 / 40           |
| 11  | 160 / 30          | 280 / 50           |

The paper gives no formula for the unrotated code; these fit
`(5d−2)(d−1)` with ancilla and `(3d−2)(d−1)` without, verified against all 20
files (26/92/198/344/530 and 14/52/114/200/310) — roughly double the rotated
counts, consistent with roughly double the qubits.
