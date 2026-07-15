# Search aliases: alternative names for codes and tools

**Status:** implemented. Aliases are **hand-written** with the zoo as reference (not
imported — see Licensing), and loose usage is **allowed but surfaced to the user** (see
Strictness).

Measured on the built site (`/search` over HTTP, 833 circuits), before → after:

| query          | before |  after | note                                    |
| -------------- | -----: | -----: | --------------------------------------- |
| `bb codes`     |    824 | **28** | all 4 BB codes incl. gross              |
| `bb72`         |      0 |      7 | resolves to `[[72,12,6]]` alone         |
| `laflamme`     |      0 |     54 | five-qubit code                         |
| `checkerboard` |      0 |     78 | rotated surface only                    |
| `kitaev`       |      0 |     98 | all surface codes, silent (true alias)  |
| `qldpc`        |      0 |     28 | code-level tags never reached the index |
| `reed-muller`  |      0 |     52 | tetrahedral                             |
| `surface-17`   |      0 |     50 | exactly the `[[9,1,3]]` rotated surface |
| `[[7,1,3]]`    |      0 |     71 | Steane                                  |
| `toric`        |      0 |     98 | **with the `related` notice**           |
| `steane`       |     71 |     71 | unchanged                               |
| `staene`       |     71 |     71 | unchanged, still spell-corrected        |

**Known, not fixed: `msd` still returns 18 wrong results.** It corrects to `msb`, a real
dictionary term one edit away. An alias would suppress it — `correctTokens` only rewrites
tokens that match nothing — but there is nothing here to alias it _to_: the catalogue has
no magic-state circuits, and "magic state distillation" is an application of the
triorthogonal codes, not another name for them. Putting it in `aliases` would be a false
claim. Left alone deliberately; revisit if magic-state circuits are ingested.

**Found along the way: code-level tags are invisible to `/search`.** `circuit_search.tags`
holds only _circuit_ tags, so `LDPC`, `surface-code` and `color-code` — all code tags —
matched zero circuits. Aliases cover the important cases (`qldpc` now returns 28), but the
underlying gap is separate and still open.

## The problem

Codes have many names. The catalogue stores exactly one each, so every other name a
reader might type is a dead query. Measured against the current index (833 circuits,
778 dictionary terms):

| query               | hits today | what the user sees                         |
| ------------------- | ---------: | ------------------------------------------ |
| `bb codes`          |    **824** | near the whole catalogue — pure noise      |
| `toric`             |          0 | nothing                                    |
| `kitaev`            |          0 | nothing                                    |
| `laflamme`          |          0 | nothing                                    |
| `checkerboard`      |          0 | nothing                                    |
| `reed-muller`       |          0 | nothing                                    |
| `msd`               |         18 | **wrong results** — silently read as `msb` |
| `bivariate bicycle` |         21 | works                                      |
| `gross`             |          7 | works                                      |

Three distinct failure modes, and none is a typo — so the existing spelling layer
cannot reach any of them:

1. **`bb codes` is worse than empty.** `bb` matches nothing, so the AND finds zero and
   the OR fallback fires; `codes` then matches essentially every circuit. The
   forgiveness layer designed for typos actively converts a precise query into a
   firehose. `bb` is also 2 characters, so `editBudget` gives it 0 edits and the
   corrector will never touch it — this can only be fixed with data, not tuning.
2. **`toric`/`laflamme`/`checkerboard` are correctly left alone.** `correctTokens`
   only rewrites a token when it matches nothing _and_ a near neighbour exists. These
   are real words with no near neighbour, so they stay dead. Correct behaviour, wrong
   outcome.
3. **`msd` → `msb` is a false friend.** `msb` is a genuine dictionary term (18 docs),
   one edit away, so magic-state-distillation gets silently answered with something
   unrelated. An alias entry for `msd` makes it findable and, because `correctTokens`
   only fires on tokens that match _nothing_, simultaneously stops the mis-correction.

## Where the names come from

The [Error Correction Zoo](https://errorcorrectionzoo.org) — which every code already
links to via `zoo_url` — publishes `alternative_names`, `short_name`, and its own
canonical `name` per code, in machine-readable YAML
([errorcorrectionzoo/eczoo_data](https://github.com/errorcorrectionzoo/eczoo_data)).
33 of our 38 code files carry a `zoo_url`; **25 of them gain a name we do not have.**

Highlights, extracted from their YAML:

| our code                | zoo gives us                                                         |
| ----------------------- | -------------------------------------------------------------------- |
| Gross Code              | `(3,3) BB6 code`; parent is _Bivariate bicycle (BB) code_ `[BB]`     |
| Bivariate Bicycle Code  | `(6,6)/(15,3)/(9,6) BB6 code`, zoo names them `[[72,12,6]] BB6 code` |
| Five-Qubit Perfect Code | **`Laflamme code`**                                                  |
| Rotated Surface Code    | `Checkerboard code`, `Medial surface code`, `Rectified surface code` |
| Unrotated Surface Code  | zoo's canonical name is **`Kitaev surface code`**                    |
| Tesseract Code          | `[[16,6,4]] hypercube code`, `[[16,6,4]] 4D color code`              |
| Tetrahedral Code        | zoo's canonical name is **`[[15,1,3]] quantum RM code`**             |
| Quantum Golay Code      | `Qubit Golay code`                                                   |
| Carbon Code             | `C_{12} code`                                                        |

**The parent chain is not an alias source.** Walking it does yield `BB code` for gross
and `Quantum Reed-Muller` for the tetrahedral code, but it degrades fast: two hops up
from the rotated surface code sits _Quantum Tanner code_, and from Steane sits
_Lifted-product code_. Those are ancestors in a taxonomy, not other names for the
thing. Depth-1 parents are worth reading by hand as candidate **tags**; they must not
be poured into an alias field.

## Shape as built

Aliases are a property of the entity, not of the query, so they live in the data and the
index rather than a query-rewrite layer. Both engines then work from one source.

1. **`data_yaml/codes/*.yaml` gains optional `aliases:` and `related:`; tools gain
   `aliases:`.** Hand-written. `scripts/validate-yaml.mjs` rejects unknown keys, so its
   schema had to learn them.
2. **Migration `017`** adds `aliases`/`related` to `codes`, `aliases` to `tools`, and
   recreates `circuit_search` with both as indexed columns. FTS5 has no `ALTER TABLE ADD
COLUMN`, so the index is dropped and rebuilt — safe, since it holds no source data.
3. **`create_database.mjs`** folds them into `SEARCH_TEXT` and the `search_terms`
   inserts, so the spelling dictionary learns alias vocabulary (778 → 809 terms) and
   `bivarient bicycle` corrects like anything else.
4. **`resolveQuery` gained a fourth rung**, and `ResolvedQuery` a `relatedOnly` flag.
5. **`BM25_WEIGHTS` is now `[0.0, 10.0, 4.0, 4.0, 0.5, 6.0, 1.0]`** — `aliases` matches
   `code_name` (an alias _is_ a code name), and `related` sits lowest since it only ever
   decides a query nothing else answered.
6. **`searchByType`/`searchCircuits`** match `aliases` but deliberately not `related`.

### The resolution ladder

`resolveQuery` tries four expressions in order, stopping at the first with hits:

1. every term, over name/code_name/aliases/tags/notes — what was asked for
2. every term, allowing `related` — a neighbouring code, **flagged to the user**
3. any term, strict columns — `partial`
4. any term, allowing `related`

(2) precedes (3) because dropping to "any term" concedes more: `toric code` widened to
any-term matches every circuit containing "code" (824 of 833), whereas allowing
`related` returns the 98 surface codes actually meant. FTS5 column filters
(`{name code_name aliases tags notes} : (...)`) express the strict rungs; the filter
wraps the whole group, since applying it per token would change what AND/OR bind to.
`circuit_id` is UNINDEXED and cannot appear in a filter.

### On hyphens

No folding was needed. FTS5's `unicode61` splits `Reed-Muller` into `reed`+`muller`, so
both `reed muller` and `reed-muller` match; the quick-search's LIKE is substring-based
and matches either way. Storing the hyphenated form verbatim is strictly better than
folding, which would break LIKE for anyone who types the hyphen.

## Decisions taken

### 1. Licensing → hand-curate, zoo as reference

`eczoo_data` is **CC-BY-SA 4.0**; this repo is **MIT**. Bulk-importing their curated
alias lists would arguably make that data a derivative under a share-alike licence
inside an MIT repo. Instead: aliases are written by hand, using the zoo and the papers
as research. Individual code names are facts rather than creative expression, and there
are only ~33 codes. This sidesteps the licence question and the precision problem at
once — we can reject the taxonomy junk (`Quantum Tanner code` for a surface code) that
an import would drag in.

Do **not** add a script that pulls `eczoo_data` into `data_yaml/`.

### 2. Strictness → loose, but surfaced

Two fields, not one:

- **`aliases:`** — true alternative names. Match silently; these _are_ the thing.
  `Laflamme code` → five-qubit, `Checkerboard code` → rotated surface.
- **`related:`** — common loose usage. Match, but tell the user: _"No exact match for
  toric — showing surface codes."_ Mirrors the existing `corrected`/`partial` notices
  on `/search`, which already exist to say "we changed your query".

`ResolvedQuery` gains a third flag alongside `corrected`/`partial`. Note `display` and
`?literal=1` already exist for exactly this "we rewrote your query" purpose.

**On `toric` specifically:** the loose reading is better supported than assumed. The
zoo's own `toric` page states verbatim that _"toric code" is often an alternative name
for the general construction_, and its `surface` entry is canonically named **Kitaev
surface code** with toric/planar as the periodic/planar boundary cases. So `toric` is
arguably a true alias. It stays in `related:` anyway — the catalogue's codes are planar
(k=1), and saying so costs one line of UI copy and asserts nothing false.

## Curation notes

Worth knowing before writing the lists — all from the research pass:

- **Steane = the smallest 6.6.6 / triangular color code.** High-value alias, and _not_
  in the zoo's `alternative_names` field — it comes from prose plus the literature.
  Our `19-1-5`/`37-1-7` are already "6.6.6 Color Code", so this links them to Steane.
- **Bare digit forms (`713`, `513`) are UNVERIFIED.** The research pass could not find
  them in the zoo, in paper titles, or anywhere else. Do not ship them as asserted
  aliases. If digit-run matching is wanted, do it as a normalization rule (strip
  non-digits from `[[7,1,3]]`), which is a different mechanism with a different failure
  mode — and worth its own decision.
- **Notation must not be collapsed.** `[[n,k,d]]` is a stabilizer code, `[n,k,d]`
  single-bracket is _classical_, `((n,K,d))` double-parens is a **non-additive** code
  where `K` is a dimension not a qubit count, and `[[n,k,r,d]]` is a subsystem code with
  `r` gauge qubits. `((5,6,2))` is not `[[5,6,2]]`.
- **Parameters do not identify a code.** The zoo notes a _different_ BB code with the
  same `[[144,12,12]]` parameters as gross (arXiv:2407.16336). An alias keyed on
  parameters alone can be wrong.
- **Genuinely overloaded, needs disambiguation rather than aliasing:** "Floquet code"
  (→ both the dynamical-automorphism and honeycomb entries), "Floquet color code" (→ two
  distinct entries), "gross code" (above). None are in our catalogue today; the point is
  not to alias them reflexively if they arrive.
- **`msd` is the one non-code alias worth adding** — it stops the `msd` → `msb`
  mis-correction. It only pays off if magic-state circuits exist here; today they don't.

## Not in scope

Aliases for concepts with no entity behind them (`MWPM`, `union-find`, `lattice
surgery`) would resolve to nothing — the catalogue is state-prep focused. Only add an
alias for something that exists here. The tool aliases worth having are narrower than
they look: `MQT QECC` → Munich Quantum Toolkit is confirmed and useful; `Circuit-Synth`
has no public repo or paper, so only casing variants are safe; `stac` collides with
`staq` and is fuzzy-close to `Stim`, so it should stay exact-match only.
