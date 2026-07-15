# Changelog

All notable changes to this project will be documented here. Versioning follows
the source-of-truth `package.json` version.

## Unreleased

### Added

- **Search aliases** (`data/migrations/017`). Codes and tools gain optional
  `aliases:`, and codes `related:`, hand-written with the Error Correction Zoo as
  reference. `laflamme` → the five-qubit code, `kitaev` → surface codes,
  `bb codes` → 28 circuits instead of 824. `related` names a _different, adjacent_
  code (`toric` → planar surface codes) and `/search` says so rather than
  silently equating them. See
  [docs/superpowers/plans/2026-07-15-search-aliases.md](docs/superpowers/plans/2026-07-15-search-aliases.md).
- **Code tags reach `/search`** (`data/migrations/019`). `circuit_search.tags`
  was built only from `taggable_type = 'circuit'`, so every code-level tag was
  invisible: `LDPC`, `topological`, `self-dual`, `surface-code` and `color-code`
  each matched zero circuits despite 4 codes being tagged LDPC and 10
  surface-code. They now ride in their own `code_tags` column — separate from
  `tags` so a name used at both levels cannot double-count. It failed silently
  because `search_terms` already indexed code tags, so spelling correction
  considered `topological` a real word and left the dead query alone.
- **`scripts/add_paper.py`** — fetches paper metadata from arXiv/Crossref into
  `data_yaml/papers/`, so it is never hand-written or recalled from memory.
  `npm run papers:add -- <arXiv id | DOI | link>` for one;
  `npm run papers:missing` scans every circuit `source` and fetches whatever has
  no paper yet (idempotent — the one to run after a bulk import). Refuses to
  write a record with no authors rather than emit a half-citation. Stdlib only,
  no new dependency.
  - This is the **only** part of the repo that touches the network, and it is a
    maintainer tool whose output is committed — the same shape as
    `annotate_circuits.py`. `db:create` and the site read committed YAML only and
    build identically offline.
- **Papers are searchable.** A circuit taken from a paper can now be found on
  `/search` by the paper's title, authors and arXiv id — none of which existed
  anywhere in the library before, since `circuits.source` holds only a link.
  Searching `reinforcement learning`, `Forlivesi` or `boolean satisfiability`
  now finds the circuits from those papers.
  - New `data_yaml/papers/` (7 files) and a `papers` table, with `circuits.paper_id`.
  - **Circuits do not declare their paper.** `db:create` resolves `source` against
    each paper's `url`/`arxiv_id`/`doi`, tolerating http/https, trailing slashes,
    `dx.doi.org`, `/pdf/` vs `/abs/`, and arXiv version suffixes. Adding a paper file
    enriches every circuit citing it; no circuit YAML changes. 724 of 833 circuits
    link; the remaining 109 carry `source: circuit-synth`, a tool rather than a work.
  - `circuit_search` gains a weighted `paper` column (migration 017 recreates the
    FTS5 table — it has no `ADD COLUMN`), and `search_terms` indexes paper titles and
    authors so spelling correction knows author names.
  - Paper text is `/search`-only. The header quick-search is for jumping to a known
    thing, and one paper backs up to 370 circuits.

### Changed

- **BM25 weights and the strict column set are derived from the table**
  (`src/lib/queries/search-schema.ts`), not restated by hand. Both drifted from
  `circuit_search` while this branch was being built — a 7-entry weight array for
  8 columns (silently scoring `paper` as `notes`), and a strict set missing
  `paper` (which announced "no code goes by that name" for an exact author
  match). Weights are now keyed by column name and ordered from
  `PRAGMA table_info`; a column with no weight throws and names itself instead of
  being silently scored 1.0. `scripts/smoke.sh` additionally asserts that a query
  reaching each of `aliases`, `code_tags` and `paper` still returns circuits.
- A circuit's source now renders as a citation ("Zen et al. (2024) · arXiv:2402.17761")
  instead of a bare URL, on circuit rows, detail pages and the cite toast. Detail pages
  emit the paper as a schema.org `ScholarlyArticle` with its real authors, rather than a
  URL string.
- The landing page's "Papers" stat counts the `papers` table instead of inferring papers
  from distinct `source` values that are not a tool's own links. Same number today, but
  it no longer guesses.

### Removed

- The `Circuit-Synth Encoding (Gate-Optimized)` circuit for the Gottesman
  [[8,3,3]] code (`#134`) — it did not encode the code it was filed under.
  Propagating `Z` through it landed only 1 of 8 single-qubit operators inside the
  code's stabilizer group where 5 (`n−k`) were expected, and 2 of its 5 stored
  stabilizers came out genuinely random on the `|0…0⟩` run — checked sign-free,
  so not a Pauli-frame difference. Its three sibling encoders are correct and
  remain. `#134` is retired, not reused. Surfaced by the detector work: the
  logical-input derivation is basis-independent, so it can check non-CSS codes
  that `validate:circuits` skips (see below).

### Fixed

- Qubit coordinates survive ingestion
  ([#107](https://github.com/qecirc/qecirc-website/issues/107)). `QUBIT_COORDS`
  reached the stored body intact only when a circuit had TICKs; otherwise
  compaction kept the instruction and dropped its arguments, turning
  `QUBIT_COORDS(3, 7) 0` into a meaningless bare `QUBIT_COORDS 0`. That path runs
  for TICK-less circuits — most of the library. Nothing stored was corrupted,
  because no body carried coordinates yet.

### Added

- Detectors and observables for state-preparation and encoding circuits
  ([#108](https://github.com/qecirc/qecirc-website/issues/108)), shown with a
  **Detectors toggle** next to Coords and hidden by default. Switching it on
  swaps in a new `stim-annotated` body — reset prologue, terminal readout, the
  deterministic stabilizer outcomes as `DETECTOR`s, and the logical as an
  `OBSERVABLE_INCLUDE` — and repoints the Crumble link at the matching URL. The
  canonical `stim` body stays unitary and untouched, because `to_tableau()` and
  the derive/fit pipeline depend on it. 418 of 834 circuits are annotated (357
  state prep, 61 encoders); the 62 five-qubit-code circuits are excluded,
  because non-CSS stabilizers mix X and Z on the same qubit and no single
  terminal readout basis reads them — but they still get the reset prologue,
  since being non-CSS blocks the readout, not the initialisation.
- State-prep and encoding circuits now state their `|0…0⟩` input explicitly with
  a reset prologue, in both toggle states, instead of leaving it implied.
  Encoders reset only their non-input qubits, since those are the ones actually
  fixed in `|0⟩`. Circuits that act on an already-encoded state (syndrome
  extraction, gadgets) get no prologue — a reset there would be wrong, not
  merely unhelpful.
- Encoders are annotated differently from state preps: only their ancillas are
  reset, leaving the k logical inputs free, and they get detectors but no
  observable. Hz is deterministic for any input, so the detectors hold whatever
  the reader supplies; the logical is input-dependent. The input qubits are
  unrecorded and canonicalization moves them, so they are derived from the
  circuit.
- Coordinates are now displayed with a **Coords toggle** on circuit bodies,
  hidden by default: a d=11 unrotated prep opens with 221 `QUBIT_COORDS` lines
  before its first gate. Copy and download follow the toggle, so what you take
  away is what you see. The toggle only appears on bodies that have
  coordinates. Crumble links always keep them — that is where the layout is the
  point.
- The 20 unrotated surface code circuits now carry their lattice layout, and
  their Crumble links render it. Only coordinates for qubits the circuit
  actually uses are kept: a `QUBIT_COORDS` target counts towards stim's
  `num_qubits`, so importing every declared grid site would inflate
  `qubit_count`.

- Surface code unitary Pauli-state encodings from
  [arXiv:2601.05113](https://arxiv.org/abs/2601.05113) — 40 circuits across 10
  codes (`data-imports/surface-code-encodings/`). Each code gets four circuits:
  `Ancilla-mediated` / `Direct` × `zero` / `plus`, the two variants differing in
  whether intra-plaquette gates are routed through bridge ancillas
  (nearest-neighbour) or run directly between data qubits
  (next-nearest-neighbour).
- Six new codes: `unrotated-surface-code-d-{3,5,7,9,11}` — the unrotated
  (planar) surface code family, `[[13,1,3]]` through `[[221,1,11]]`, new to the
  library — and `rotated-surface-code-d-11` (`[[121,1,11]]`), completing the
  rotated family from d=3 to d=11.
- New `partial-ft` circuit tag, for schemes that preserve the fault distance for
  only one error type. The surface code encodings preserve it for the error that
  flips the codeword (X for `|0>_L`, Z for `|+>_L`) but not the complementary
  one, which `ft` / `non-ft` cannot express. Which type is protected follows from
  the `logical-state:*` tag.
- `import_state_prep(ancilla_role=...)` distinguishes flag qubits from routing
  ancillas. Previously the `flag` tag was inferred from `num_qubits > n` alone,
  which mis-tags circuits whose ancillas only bridge gates under a restricted
  connectivity and carry no fault-tolerance role. Defaults to `"flag"`, so
  existing importers are unaffected; pass `"routing"` to opt out.
- Circuit notes render a long contiguous ancilla run as `221-440 (220 qubits)`
  instead of spelling out every index. Ancilla indices are always contiguous
  (`range(n, num_qubits)`), so the list was pure noise once a code got large.
  Runs of 8 or fewer, and any non-contiguous set, are unchanged.

- Edge caching: `s-maxage` raised from 10 minutes to 7 days (pages and API),
  paired with an automatic Cloudflare purge-everything on each deploy
  (`src/lib/cache-purge.ts`, activated by the `CLOUDFLARE_ZONE_ID` /
  `CLOUDFLARE_API_TOKEN` env vars; logged no-op without them).

- Social-share card: static `og:image` / `twitter:image` (1200×630, generated
  by `scripts/icons/generate.mjs`) on all pages; Twitter card upgraded to
  `summary_large_image`.

- Non-CSS stabilizer code support throughout the pipeline (symplectic representation).
  Submit codes via `add_circuit(H=..., n=...)` for non-CSS, or the existing
  `Hx`/`Hz` path for CSS.
- New `h` and `logical` columns on `codes`; `original_h` and `original_logical`
  on `circuit_originals` (migration `011_symplectic_storage.sql`).
- New `npm run backfill:symplectic` script for upgrading existing CSS YAMLs.
- Non-CSS code page renders stabilizers and logicals via a Pauli ↔ symplectic
  toggle; CSS pages keep the existing `Hx`/`Hz`/`Logical X`/`Logical Z` view.

### Changed

- Circuit results in the search dropdown now link to the circuit's own page
  (`/circuits/<id>`) instead of the anchored code list.
- Filtering and sorting on the codes index and code pages now run client-side
  over the rendered rows: filter changes apply instantly (no page reload) and
  every visit shares one canonical cached document. The URL contract is
  unchanged (old filter links still work, applied on load); `/api/download`
  still parses the same params server-side.
- Code pages no longer embed circuit bodies in the initial HTML; bodies load
  on first row expand via the new `/api/circuits/[qec_id]/bodies` endpoint.
  Largest page (`/codes/flag-gadgets`) drops from ~15 MB to ~3 MB HTML and
  from ~39k to ~20k DOM nodes.
- **BREAKING:** `add_circuit()` matrix arguments (`Hx`, `Hz`, `H`, `n`) are now
  keyword-only. Migration: replace `add_circuit(Hx, Hz, circuit, name, d, ...)`
  with `add_circuit(circuit=circuit, circuit_name=name, d=d, Hx=Hx, Hz=Hz, ...)`.
- The non-CSS branch of `_compute_logicals` (now `_compute_logicals_css`) was
  mathematically wrong and is replaced by the new `_compute_symplectic_logicals`.
  This affects nobody in practice (the library contained no non-CSS codes), but
  any downstream code calling the old `_compute_logicals(_, _, code_is_css=False, _)`
  must switch to `_compute_symplectic_logicals(H, n, k)`.
