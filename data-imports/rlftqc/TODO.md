# RLFTQC import — status & remaining work

Goal: add every RLFTQC circuit (excludes `*_flag.stim`) to the QECirc library.

## Works end-to-end (verified on a scratch copy of `data_yaml`)

`python rebuild_all.py --write --data-dir <scratch>` → **238 / 239 imported, 0
failures, ~80s**. Validator: all imported circuits pass (non-CSS circuits skipped
by the CSS validator — expected). No duplicate codes: the circuits anchor to the
codes already in `data_yaml`.

## Resolved decisions

- **Curation** → import all (no subsetting).
- **Logical-state label** → CSS: library basis (Z→`zero`, X→`plus`), keeping the
  source's exact label when its basis agrees, else library basis + a note with the
  source label (Shor's X/Z convention). Non-CSS (5-qubit): source label directly.
- **Slug style** → short + numeric index, e.g. `rl-2d-grid-zero-3`; provenance in
  notes + the permanent `#qec_id`.
- **Location** → in the repo at `data-imports/rlftqc/`; dataset stays beside the repo.

## Merge with `main` (done)

- Merged `origin/main` (was 11 commits ahead) into `feat/state-prep-ingestion` —
  **no conflicts**.
- **#78 independently added the same 4 codes** we were seeding. The importer was
  adapted to _anchor to main's codes_ instead of seeding duplicates:
  `shor-code`, `tetrahedral-code`, `rotated-surface-code-d-3/-d-5`. Shor +
  tetrahedral fit under identity; `9-1-3-surface` via the n≤9 search.

## Remaining

1. **Apply to the real `data_yaml`** and build: `python rebuild_all.py --write`
   then `npm run format && npm run validate:yaml && npm run validate:circuits &&
npm run db:create && npm run dev` → inspect the site.
2. **Commit** the `data-imports/rlftqc/` dir (the `scripts/add_circuit/` tooling +
   merge are already committed on `feat/state-prep-ingestion`). Bump version
   (patch) per CLAUDE.md.
3. **Deferred: the one `[[25,1,5]]` circuit.** n=25 is too large to brute-search
   and `find_qubit_permutation` can't confirm the σ into main's
   `rotated-surface-code-d-5` labeling. Needs a structural permutation-finder
   (Tanner-graph isomorphism) — the same future improvement that would remove the
   hand-supplied `17-1-5` σ. Then flip it on and re-import.

## Handy facts

- `rebuild_all.py` (no `--write`) prints the per-code fit classification.
- Supplied σ live in `CODES[...].known_perms` (convention `σ[new]=old`).
- Self-dual codes (steane, 17/19/23) resolve non-identity fits via
  `method="self_dual"` (canonical-hash dedup) — no explicit σ.
