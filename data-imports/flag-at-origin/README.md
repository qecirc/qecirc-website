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
- **precomputed σ** (`17-1-5`): the color code is automorphism-rich, so the
  structural finder is too slow to run each time; the permutation is cached in
  [`sigma_precomputed.json`](sigma_precomputed.json) (produced once with
  `find_code_permutation`).
- **new code** (`20-2-6`, `25-1-5`, `47-1-11`, `49-1-5`, `49-1-7`, `49-1-9`,
  `71-1-11`, `81-1-9`, `95-1-7`): `assume_new=True` bypasses a _false_ uncertain
  dedup — several share `[[n,1]]` parameters and weak invariants with a stored
  code but have distinct canonical hashes.

The `+` / `F` suffixed files are alternative flag-gadget configurations of the
same code; they dedup onto the base code as separate circuit variants.

#### Deferred

- **`[[31,1,7]]`** — the same code as the stored `31-1-7`, but
  `find_code_permutation` does not converge on this automorphism-rich color code.
  Add it once a permutation is computed offline (drop it into
  `sigma_precomputed.json`).
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
