# Changelog

All notable changes to this project will be documented here. Versioning follows
the source-of-truth `package.json` version.

## Unreleased

### Added

- **Syndrome-extraction circuits are a supported kind.** The pipeline could describe an
  encoder and a state prep; a round of syndrome extraction fitted neither, and there was
  nothing to check one against.
  - **`validate_syndrome_extraction_h`** (`scripts/add_circuit/circuit_validate.py`) — a
    round must measure exactly the stabilizer group and leave the encoded state, logicals
    included, alone. It cannot be a codespace test the way the prep and encoder checks
    are: a round acts on an already-encoded state, so there is nothing to simulate it on.
    It is a **stabilizer-flow** check instead, and the ancilla-to-check correspondence is
    derived rather than assumed.
  - **`build_se_round`** (`scripts/add_circuit/syndrome_extraction.py`) — ticks of
    (data, ancilla, basis) into one canonical round, refusing a tick that reuses a qubit
    or an ancilla asked to carry both bases.
  - **`round_check_matrix`** — which operator each measurement reads, which is what
    placing detectors needs. Deliberately narrow: no map is better than a wrong one, and
    nothing in validation depends on it.
  - **A round's `stim-annotated` body is the memory experiment it belongs to** — reset the
    data, `REPEAT d` of the round, terminal readout, detectors, observable. Unlike a prep
    or an encoder, a round is not reset-free and has no tableau, so none of the derive/fit
    machinery may be pointed at it.
  - `schedule:` and `decoder:` join the `method` tag category. They pair up: a schedule
    found by search is co-designed with the decoder it was scored against, so two rounds
    for one code can differ only by `decoder:`.
  - **`scripts/add_circuit/find_sigma.py`** — the codeword-based permutation matcher,
    for codes that match a stored one on every cheap invariant but defeat
    `find_code_permutation`'s budget. Written for the asyndrome import; three importers
    need it, so it lives in the shared package rather than in one of them.

### Added

- **Bacon-Shor [[9,1,3]], [[16,1,4]] and SHYPS [[49,9,4]]**, the library's first subsystem
  codes, now that #144 gives them somewhere to live. `code.matrix` is qLDPC's _gauge_
  group, so the importer passes the stabilizer group (`get_stabilizer_ops()`) as `h` and
  the gauge group alongside it; k comes out `n - rank(h) - gauge_qubits` rather than
  `n - rank(h)`, which is the difference between [[9,1,3]] and [[9,5,3]].
  - An encoder and a |0> prep each. qLDPC's memory experiments do not support subsystem
    codes, so the two syndrome-extraction strategies report `unsupported` for them rather
    than silently producing nothing.
  - **A subsystem encoder exposes `k + gauge_qubits` free inputs**, not `k` — five for
    Bacon-Shor, one logical and four gauge. `logical_input_count` and the annotator both
    compared against `k` alone and refused every such circuit. Both now add the stored
    gauge count. Deliberately _added to the stored k_ rather than derived from `h`: the
    latter is the same number but would compare the circuit against itself and stop
    catching a stored k that disagrees with the code, which is what the check is for.
  - `add_circuit(gauge=...)` passes the group through; #144 stopped at
    `compute_code_data_h`.

- **Subsystem codes can be stored** (`data/migrations/020`). A subsystem code is described
  by two groups, not one: the **gauge** group a decoder may measure, and the **stabilizer**
  group — its centre — whose outcomes are deterministic. The difference between them is
  real qubits, `(rank(G) − rank(S)) / 2` of them, which carry no information and are not
  corrected.

  The library read k off a single check matrix as `n − rank(h)`, which counts those gauge
  qubits as logical ones: Bacon-Shor [[9,1,3]] would have been stored as **[[9,5,3]]** and
  SHYPS [[49,9,4]] as **[[49,25,4]]**, so both were excluded rather than recorded wrongly.
  Codes now carry an optional `gauge` matrix and `gauge_qubits` count, and

      k = n − rank(S) − (rank(G) − rank(S)) / 2

  which for a stabilizer code has a zero gauge term and is the formula already in use — one
  implementation, not two.
  - **`h` still means the stabilizer group**, for every code. Validators, dedup, the CSS
    split and the matrices view are untouched: a circuit is checked against the operators
    that are actually deterministic, which is what those checks want. Stabilizer codes gain
    no fields at all.
  - **Logicals are the bare ones.** `_compute_symplectic_logicals` takes the kernel of the
    gauge group rather than of `h` when there is one, so they commute with everything a
    decoder may measure, while still quotienting by the stabilizers.
  - **Identity is the gauge group's.** Two subsystem codes can share a stabilizer group and
    differ in gauge group, so `canonical_hash` is computed over the gauge group when there
    is one — it determines the stabilizer group as its centre, so it is the more
    informative of the two.
  - Tagged `subsystem`, so a reader who sees [[9,1,3]] over a rank-4 `h` is told why rather
    than left to think it a bug.

  Verified against qLDPC's own `get_code_params()` on Bacon-Shor(3), Bacon-Shor(4),
  SHYPS(3) and Steane. Importing the codes themselves is a follow-up.

### Changed

- **Submitted check matrices are stored once instead of once per circuit.** They are a
  property of the code and the labelling it was submitted in, so every circuit of one
  code wrote the same bytes — 479 files collapse to **68**. They now live in
  `data_yaml/matrices/<digest>.yaml`, content addressed, with the circuit YAML naming
  the one it uses via `original_matrices`. The original _circuit_ stays beside the
  circuit, since that genuinely differs. `db:create` resolves the reference and inlines
  both halves, so `circuit_originals`, the API and the circuit page are unchanged.
- **Large matrices are written sparsely.** Above `SPARSE_MIN_ENTRIES` a matrix is stored
  as the nonzero column indices of each row rather than dense 0/1 rows. `h` is
  (n-k) x 2n, so a dense encoding costs O(n^2) characters however sparse the code is.
  Small codes stay dense deliberately — they are the ones a person reads, and the
  threshold sits above every code the library had before the qLDPC imports, so no
  existing small file is rewritten. Readers call `matrix_format.decode` (Python) or
  `decodeMatrix` (`scripts/matrix-format.mjs`) and cannot tell which was used.

  On the current data `data_yaml/` goes **35.2 MB to 24.2 MB**, all of it from sharing:
  `circuits/originals/` drops 15.7 MB to 0.3 MB and the shared `matrices/` costs 4.3 MB
  back. The sparse encoding saves **nothing today** and is meant to — no code the library
  has reaches the threshold, and rewriting the small files a person reads would be a cost
  with no benefit. It is what makes the qLDPC codes affordable when they land: on a single
  [[1428,184]] code it is worth more than this whole repository.

  `db:create` refuses to build a circuit that still carries a per-circuit
  `originals/<stem>.original.yaml` with no `original_matrices` reference. Merging a
  branch written before this format produces no git conflict — the old file simply
  reappears — and the build would otherwise store null matrices and say nothing.
  `scripts/migrate_matrix_storage.py --write` converts such a branch.

### Fixed

- **Importing a circuit no longer costs a full re-read of the library.** Dedup compares a
  submission against every stored code, and re-parsed all of them from YAML on _every_
  call — so a bulk import paid O(library) per circuit and got slower as the library grew.
  Measured on the 74-code, 43 MB library the qLDPC imports produce: **29.3 s per
  circuit**. Parsed codes are now cached across calls, keyed on each file's
  (mtime, size) so a code written mid-import is still picked up — `add_circuit` creates
  code files as it goes, and a cache that could not see them would be worse than none.
  Every circuit after the first now pays a `stat`. Sparse storage compounds it: the same
  first parse drops to 3.6 s.
- **The submitted-order logical operators are no longer recomputed from scratch.**
  `canonical_form` only permutes columns and row-reduces, neither of which changes the
  code, so the canonical logicals permuted back _are_ the originals — worth ~25 s per
  circuit on a [[544,80]] code, and it makes the two sets agree about which logical qubit
  is which, where a second independent computation would pick some other equally valid
  basis. The permuted operators are verified against the submitted matrices before use,
  with recomputation as the fallback.
- **A non-CSS circuit for an existing code is filed under that code's slug.** On a dedup
  match the CSS path has always used the stored slug; the non-CSS path only used it when
  nothing else had set one, so `code_slug` — or a slug derived from `code_name` — won
  instead. A five-qubit-code circuit submitted with
  `code_name="Five-Qubit Perfect Code"` was written as
  `five-qubit-perfect-code--<circuit>.yaml` while the code itself lives at
  `five-qubit-code`; no code YAML was written under that name, because there was no new
  code, so the circuit referenced an entry that does not exist —
  `annotate_circuits.py` reported `code '...' not found` and `db:create` rejected it.
  `code_slug` is documented as naming a _new_ code, and on a match there is no new code
  to name.

### Added

- **Every qLDPC circuit records the one-liner that rebuilds it**, at the end of its notes:
  `Reproduce with: qldpc.circuits.get_encoding_circuit(qldpc.codes.ToricCode(4), only_zero=True)`.
  Asked for by the library's author
  ([qLDPCOrg/qLDPC#554](https://github.com/qLDPCOrg/qLDPC/issues/554)) — a reader who wants
  to rebuild one should not have to reverse-engineer the constructor from `[[n,k,d]]`.
  The snippet cannot drift from the circuit, because the constructor string **is** what the
  importer evaluates: `CodeSpec.constructor` replaced the lambda it used to hold, and
  `CodeSpec.build()` evaluates it. A snippet that stopped building the code would fail the
  import rather than mislead a reader.

- **qLDPC circuits** (58 of them), imported from
  [qLDPC](https://github.com/qLDPCOrg/qLDPC) by [data-imports/qldpc/](data-imports/qldpc/README.md):
  28 syndrome-extraction rounds in two edge-colouring schedules
  ([arXiv:2109.14609](https://arxiv.org/abs/2109.14609)), plus a tableau encoder and a
  tableau |0> preparation for each of 15 codes. Six new codes come with them — the
  Iceberg codes [[4,2,2]] and [[6,2,2]], toric d=6, two hypergraph product codes
  [[58,16,3]] and [[241,121,3]], and a toric [[16,2,4]] that is **not** the stored
  one (its X row space has 16 weight-6 codewords where the stored code has none, and
  weight enumerators are permutation invariants).
  - Upstream states both syndrome-extraction strategies are **not guaranteed
    distance-preserving or fault-tolerant**, and that its encoders are not
    fault-tolerant. That claim is reproduced in each circuit's notes rather than
    dropped: the library tags what its sources claim, and here the source claims the
    opposite.
  - Subsystem codes are excluded, not broken. `BaconShorCode` and `SHYPSCode` validate
    fine against their stabilizer group, but the library derives k as n - rank(h),
    which is only correct for stabilizer codes — Bacon-Shor [[9,1,3]] would be stored
    as [[9,5,3]]. They need a gauge-group field and a k that is not derived.

### Fixed

- **`round_check_matrix` reads rounds that hold their ancillas in the X basis**
  (`RX` ... `MX`, with Z-checks as `CZ`), not only the Z-basis form. The two are the
  same construction in different frames; before this, every X-basis round returned no
  check map and silently lost its annotated memory experiment. It now tracks the basis
  each ancilla is prepared in, pulls back that operator rather than always `Z`, and
  requires the measurement basis to match the reset basis — a round reset in X and read
  in Z has a random outcome however correct its check pattern looks.

### Added

- **Syndrome-extraction circuits — the first in the library** (56 of them), imported
  from [AlphaSyndrome](https://github.com/acasta-yhliu/asyndrome)
  ([arXiv:2601.12509](https://arxiv.org/abs/2601.12509), ASPLOS '26) by
  [data-imports/asyndrome/](data-imports/asyndrome/README.md). One stored circuit is
  one **round**: reset the ancillas, run the tick-scheduled CX ladder, measure. The
  round count is not baked in — the `stim-annotated` view repeats it `d` times into a
  memory experiment with detectors and an observable. 14 new codes come with them
  (hyperbolic surface ×6, hyperbolic color ×3, surface-with-defects ×2, and others),
  and the landing page stops saying syndrome extraction is "still to come".
  - Two of the source dataset's codes needed a distance the dataset does not give
    correctly, computed exactly by `data-imports/asyndrome/code_distance.py`
    (minimum weight of a non-trivial logical, by exhaustive enumeration — a
    distance, not a bound). The self-dual bivariate bicycle code ships `d: -1` and
    is [[42,6,6]]. The two defect surface codes declare 5 and 7 but each carry a
    **weight-2 X-logical** — the dataset's own second `logical_xs` entry, and the
    operator belonging to the qubit the defect creates. That short operator is
    what a defect _does_; what the numbers do not support is 5 and 7, which
    neither logical qubit reaches (the surviving one manages 4). Stored as
    [[24,2,2]] and [[40,2,2]], with the reason in each circuit's notes: a stored
    `[[n,k,d]]` has to describe the `h` printed beside it.
- **`validate_syndrome_extraction_h`** (`scripts/add_circuit/circuit_validate.py`),
  replacing the `NotImplementedError` stub, and a third branch in
  `npm run validate:circuits` so these circuits are checked rather than silently
  skipped. A round acts on an already-encoded state, so there is no fixed input to
  simulate it on and — carrying resets and measurements — no tableau either. It is
  checked by **stabilizer flows** instead: the group the round measures must be
  exactly the code's, and every stabilizer and logical must survive it.
  - **What it measures is derived, not assumed** (`measured_stabilizers`). Nothing
    stored records which ancilla reads which check, and deriving it is what catches
    the real failure: an X- and a Z-check sharing two data qubits whose CNOTs are
    ordered inconsistently leave their two ancillas entangled, so each outcome is
    random and the round measures nothing — with every check applied exactly once, on
    the right qubits. 10 of the source dataset's 69 schedules fail exactly this way
    and were left out; see the import README.
- **`build_se_round`** (`scripts/add_circuit/syndrome_extraction.py`) — ticks of
  `(data, ancilla, pauli)` checks to STIM. The tick assignment is the whole content of
  a scheduling result, so it is emitted verbatim and never re-packed.
- **`build_annotated_se`** — the memory-experiment view of a round: reset the data,
  `REPEAT d`, terminal readout, first-round and inter-round detectors, observable.
  `strip_readout` now recurses into `REPEAT` blocks, which is where most of those
  detectors live; the browser's line-based mirror always reached them.
- **`schedule:` and `decoder:` tags**, filed under **Method** in the circuit filter.
  They pair up: a searched schedule is co-designed with the decoder it was scored
  against, so two rounds for the same code can differ only by `decoder:`.

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
