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
- `Notebook_2.zip` — standalone flag gadgets (`{d}_{w}_{X|Z}_ft_plaquette.txt`,
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
  [`sigma_precomputed.json`](sigma_precomputed.json). Every cached σ is verified
  by the pipeline's row-space check at import, regardless of how it was found.
  Three codes go this way:
  - `17-1-5` → the stored `17-1-5` 4.8.8 color code (automorphism-rich, slow);
    from `find_code_permutation`.
  - `25-1-5` → the stored `rotated-surface-code-d-5`. **`[[25,1,5]]` is the d=5
    rotated surface code**, verified with `find_code_permutation` — do _not_ add
    it as a new code.
  - `31-1-7` → the stored `31-1-7` 4.8.8 color code. Our `find_code_permutation`
    can't crack this one (colour refinement collapses all 31 qubits into 4
    classes, so the search exhausts its budget). The permutation was found with
    an external tool — [`bm_qecc`](https://github.com/MaxieHelenBichmann/bm_qecc)
    by Maxie Helen Bichmann — and stored inverted into our `σ[new]=old`
    convention.
- **new code** (`rotated-surface-code-d-7`, `rotated-surface-code-d-9`, `49-1-9`,
  `71-1-11`, `47-1-11`, `20-2-6`, `49-1-5`, `95-1-7`): `assume_new=True` bypasses
  a _false_ uncertain dedup. Each was checked to have a `[[n,k,d]]` that **no**
  stored code shares (the only way it could be equivalent to an existing code);
  canonical-hash distinctness alone is _not_ trusted here — it is unreliable
  (stale stored hashes), which is exactly what masked `[[25,1,5]]` as new at first.

The `+` / `F` suffixed files are alternative flag-gadget configurations of the
same code; they dedup onto the base code as separate circuit variants.

### Identifying the new codes

Five of the new codes are known codes — named/tagged/linked accordingly, from
the paper repo's own inline comments (`#7x7 surface` etc.) plus the natural
stabiliser-weight structure and QEC Zoo:

| Code          | Identity                       | slug                       |
| ------------- | ------------------------------ | -------------------------- |
| `[[49,1,7]]`  | Rotated Surface Code (7×7)     | `rotated-surface-code-d-7` |
| `[[81,1,9]]`  | Rotated Surface Code (9×9)     | `rotated-surface-code-d-9` |
| `[[49,1,9]]`  | 4.8.8 Color Code (9×9)         | `49-1-9`                   |
| `[[71,1,11]]` | 4.8.8 Color Code (11×11)       | `71-1-11`                  |
| `[[47,1,11]]` | Quantum Quadratic-Residue Code | `47-1-11`                  |

The remaining three — `[[20,2,6]]` (self-dual, 4.8.8-like weights but `k=2`),
`[[49,1,5]]` and `[[95,1,7]]` (not self-dual, mixed weights) — have no name in
the source repo or QEC Zoo, so they keep parameter names + `CSS`/`stabilizer`
(and `self-dual` where applicable).

`[[63,45,4]]` is **out of scope** — the source repo has no stabiliser definition
for it and a `k = 45` code can't be recovered from a single `|0⟩_L` circuit, so
it is intentionally not imported.

### `import_gadgets.py` — standalone flag gadgets

```bash
python import_gadgets.py --write
```

Imports the **354 plain `{d}_{w}_{X|Z}_ft_plaquette.txt`** gadgets — one per
`(distance, weight, basis)`, the canonical set the paper's own
`generate_FT_plaq_notebook()` reads and its Notebook_2 table catalogs (weights
2–51, distances 3/5/7/9/11). The `_mod_ANC` and `_from_Cplusplus` variants are
auxiliary — `_mod_ANC` only covers 111 configs and merely adds a redundant flag
to the trivial weight-2/3 cases; `_from_Cplusplus` is a different C++ text format
and coverage-redundant — so both are skipped.

Each gadget is a complete FT circuit that prepares/measures a single weight-`w`
stabiliser to distance `d`. They don't correspond to any code, so they can't go
through `import_state_prep`; they're collected under a placeholder
**`flag-gadgets`** code (`n = k = 0`, no check matrices — so the code page has no
matrices section; tagged `no-code`) and written directly with the pipeline's
helpers, so metrics / STIM+QASM bodies / slugs match every other circuit.

Tags: `gadget`, `ft`, `distance:d`, `x-type`/`z-type`, plus `flag` **only** when
the gadget actually uses flag ancillas (the trivial low-weight cases need none
but stay `ft`). The stabiliser **weight** is stored as a numeric `weight` field
(not a tag — ~50 distinct values), which drives a range filter shown only on this
listing (see `codeHasWeightedCircuits`); it's `null` for every code circuit.

## Re-running

Both importers are idempotent for codes (dedup) but append circuits by slug;
`--write` overwrites matching files. After importing:

```bash
npm run format && npm run validate:yaml && npm run validate:circuits && npm run db:create
```
