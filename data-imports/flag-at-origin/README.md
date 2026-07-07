# Flag-at-origin import (arXiv:2508.14200)

Imports circuits from [Quantinuum/flag_at_origin_paper](https://github.com/Quantinuum/flag_at_origin_paper),
the code accompanying _"Flag at origin: modular fault-tolerant state preparation"_
([arXiv:2508.14200](https://arxiv.org/abs/2508.14200)).

## Dataset

Clone the paper repo next to this one so the layout is
`…/flag_at_origin_paper/` beside `…/qecirc-website/`, or pass `--dataset PATH`.
The importers read the circuits **directly from the zips** — no manual unzip:

- `Notebook_1.zip` — per-code FT `|0⟩_L` preparation circuits (one pytket
  `Circuit.to_dict()` JSON per code).
- `Notebook_2.zip` — standalone flag gadgets (`*_ft_plaquette_mod_ANC.txt`,
  same pytket-dict format).

Everything is pure Clifford + measurement (`H/CX/Measure/Barrier`), so
[`convert.py`](convert.py) turns it into STIM with no pytket dependency.

## Two importers

### `rebuild_all.py` — per-code FT |0⟩ preparations

```bash
python rebuild_all.py            # classify only
python rebuild_all.py --write
```

Each JSON is the full SPAM benchmark (prep + flag verification + terminal
logical-Z readout). We store the prep **+ flag verification** and drop the
terminal readout, matching the other FT state-prep circuits in the library.

Check matrices ("anchors") come from the authors' own stabiliser definitions,
lifted verbatim into [`stabilizers.py`](stabilizers.py) and turned into
symplectic matrices by [`anchors.py`](anchors.py). This is deliberate: a `|0⟩_L`
circuit alone only determines `⟨stabilisers, logical-Z⟩`, so for a non-self-dual
code you cannot recover `Hz` from the circuit — you need the code's own checks.

Fit strategy per code:

- **auto-dedup** (Steane, Golay, `[[9,1,3]]` → `rotated-surface-code-d-3`): the
  pipeline matches the anchor to a stored code and finds the permutation itself.
- **precomputed σ**: dedups onto a stored code the auto-search can't confirm in
  time, using a permutation cached in
  [`sigma_precomputed.json`](sigma_precomputed.json) (produced once with
  `find_code_permutation`). Two codes go this way:
  - `17-1-5` → the stored `17-1-5` 4.8.8 color code (automorphism-rich, slow).
  - `25-1-5` → the stored `rotated-surface-code-d-5`. **`[[25,1,5]]` is the d=5
    rotated surface code**, verified with `find_code_permutation` — do _not_ add
    it as a new code.
- **new code** (`20-2-6`, `47-1-11`, `49-1-5`, `49-1-7`, `49-1-9`, `71-1-11`,
  `81-1-9`, `95-1-7`): `assume_new=True` bypasses a _false_ uncertain dedup.
  Each was checked to have a `[[n,k,d]]` that **no** stored code shares (the only
  way it could be equivalent to an existing code), and canonical-hash distinctness
  alone is _not_ trusted here — it is unreliable (stale stored hashes), which is
  exactly what masked `[[25,1,5]]` as new at first.

The `+` / `F` suffixed files are alternative flag-gadget configurations of the
same code; they dedup onto the base code as separate circuit variants.

#### Deferred

- **`[[31,1,7]]`** — almost certainly the same code as the stored `31-1-7`: all
  permutation-invariant checks match (ranks, and the per-column colour-invariant
  histograms `find_code_permutation` computes). But the 4.8.8 colour code is so
  symmetric that colour refinement yields only 4 distinct qubit classes across
  31 qubits, so the backtracking search exhausts its budget without producing a
  certified σ. Add it once a permutation is computed offline (e.g. a graph-iso /
  symmetry-aware method) and dropped into `sigma_precomputed.json`.
- **`[[63,45,4]]`** — the source repo has no stabiliser definition for it, and a
  `k = 45` code cannot be recovered from a single `|0⟩_L` circuit.

### `import_gadgets.py` — standalone flag gadgets

```bash
python import_gadgets.py --write
```

The 111 `*_mod_ANC` gadgets are complete FT circuits that prepare/measure a
single weight-`n` stabiliser to distance `d` (X- or Z-type). They are reusable
building blocks that don't correspond to any code, so they can't go through the
normal `import_state_prep` path. They're collected under a placeholder
**`flag-gadgets`** code (`n = k = 0`, no check matrices — the code page renders
without a matrices section) and written directly with the pipeline's helpers, so
their metrics / STIM+QASM bodies / slugs match every other circuit.

## Re-running

Both importers are idempotent for codes (dedup) but append circuits by slug;
`--write` overwrites matching files. After importing:

```bash
npm run format && npm run validate:yaml && npm run validate:circuits && npm run db:create
```
