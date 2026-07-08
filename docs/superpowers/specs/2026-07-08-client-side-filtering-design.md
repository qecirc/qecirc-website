# Client-side filtering and sorting on listing pages — design

**Date:** 2026-07-08
**Status:** Approved (approach A of the caching/architecture discussion)

## Rationale

Filtering and sorting on the codes index (`/`) and code detail pages
(`/codes/[slug]`) currently work by navigating to a new URL and re-rendering
server-side. Costs: every filter change is a full page reload (an 800 ms
debounce plus network round-trip, with a `?focus=` hack to restore lost
input focus), and every unique filter/sort combination is its own edge-cache
entry that is almost never hit again.

Row counts are small (32 codes; ≤354, later ~1000 circuits per code), so the
client can filter/sort the already-rendered rows instantly. Pages become
canonical (one cache entry each), and the filter UX loses the reload cycle.

This is "Half A" of a two-stage plan. "Half B" (rows shipped as JSON with
windowed DOM rendering) is only needed if codes approach ~1000 circuits; the
data-attribute layer below is the seam where it would slot in.

## Scope

- In scope: `/` (n/k/d + tags + sort) and `/codes/[slug]` (five metrics +
  tags + sort, favorites-filter interplay).
- Out of scope: `/tools` (tag filtering stays server-side — ~10 tools,
  negligible cache/UX impact), `/api/download` (keeps its server-side param
  parsing and exact URL contract), search, favorites page.

## Design

### Data layer (the Half-B seam)

Each row root element carries its filter/sort data:

- `CircuitRow` outer `div[id]`: `data-metrics` (JSON:
  `{gate_count, two_qubit_gate_count, depth, qubit_count, weight}`),
  `data-tags` (JSON array), `data-name`.
- `CodeCard` root: `data-metrics` (JSON: `{n, k, d}`), `data-tags`,
  `data-name`.

Row containers get `data-list-container` for sort reordering.

### Client module: `src/lib/list-filter-client.ts`

One shared, config-driven module (pattern: `initListKeynav`). Replaces
`filter-client.ts` (deleted). Config per page: form selector, row selector,
container selector, filter fields, default-order snapshot, count-label
selector(s), empty-state selector, base path.

State: `{ conditions per field, tags[], sort | null }`, initialised from
`location.search` on load (deep links keep working), reapplied on
`popstate`.

Behavior:

- **Numeric filters** — same grammar as today via the shared
  `FILTER_PART_REGEX` (`>10`, `>=`, `<=`, `!=`, `=`, bare number,
  comma-AND). Invalid input: red ring + "Invalid filter" + status swap,
  exactly as `filter-client.ts` does now. Input applies after a short
  (~200 ms) debounce — no navigation.
- **SQL parity rules** — a row with a NULL metric fails every numeric
  condition on that field (matches SQL three-valued logic); sorting places
  NULLs last regardless of direction with `name` as tiebreak (matches
  `buildOrderBy`); name comparison uses plain UTF-16 `<` (approximates
  SQLite BINARY collation).
- **Defaults** — circuits default sort is `two_qubit_gate_count asc`
  (matches `parseCircuitParams`); codes default is `n, k, d, name`
  (matches `buildCodeOrderBy`). SSR renders rows in default order; the
  initial DOM order is snapshotted at init and restored when sort returns
  to default.
- **Tags** — AND semantics (row must carry all selected tags), matching
  `addTagConditions`.
- **Apply** — toggle `display` on row roots, reorder rows in the container
  for sort, update "Showing X of Y" labels (including the count inside the
  code page's download-all button), toggle the client-managed empty-state
  block, update sort arrows/highlight and tag selected-states (dropdown
  entries, summary "(n)" counts, selected chips re-rendered client-side,
  cloud and row tag links).

### Interception (progressive-enhancement style)

All existing controls stay real links/inputs; the module intercepts:

- `input[data-filter]` — debounce + apply + `replaceState`.
- Sort links (filter-bar labels and the code page's column headers) — get
  `data-sort-field`; click → toggle asc/desc per current state (same
  semantics as `circuitSortToggleUrl`), apply + `pushState`.
- Tag links (dropdown popovers, tag cloud, selected chips, per-row tags on
  circuits, per-card tags on codes) — get `data-tag`; click → toggle,
  apply + `pushState`.
- Clear-filters link — `data-clear-filters`; click → reset, `pushState`.

`pushState` for discrete clicks means the back button steps through filter
states (parity with today's navigation); typed input uses `replaceState`.
Server-side, links are generated against the clean base path (no inherited
query params) so they remain meaningful as standalone hrefs
(middle-click/new-tab opens the canonical page and the client applies the
param on load).

### URL contract (unchanged)

Same param names (`n`, `k`, `d`, `gate_count`, …, `tag` repeated, `sort`,
`sort_dir`). Old bookmarked URLs apply client-side on load. The `?focus=`
param and its machinery are deleted (no reloads → focus never lost).
`/api/download` continues to read the same params from
`window.location.search` — download-all honors active filters exactly as
before.

### Server simplification

- `index.astro` / `codes/[code].astro` stop parsing filter/sort params:
  always render the full list in default order. Filter components lose
  their `raw*`, `errors`, `hasFilters`, `focus` props (inputs render empty;
  the client fills them from the URL).
- `filterCodes` / `filterCircuitsForCode` remain for `/api/download` only.
- JSON-LD: the code page's `ItemList` is now always the canonical full
  list, with `itemListElement` capped at 200 entries (`numberOfItems`
  keeps the true total).
- An empty-state block ("No circuits/codes match…", with a clear link) is
  server-rendered hidden on both pages; the client toggles it.

### Known behavior changes (accepted)

- Opening a shared filter URL shows the full list for a few ms before
  filters apply.
- No-JS visitors see the full unfiltered list; filter inputs are inert
  (previously a no-JS form GET submit could filter; auto-submit, expand,
  favorites already required JS).
- A `#qec_id` permalink whose row is excluded by simultaneous filter params
  now expands a hidden row (previously the row was absent entirely) —
  harmless; hash-focus in keynav skips hidden rows.
- Filter semantics live client-side; `/api/download` keeps the server
  parser. Both share `FILTER_PART_REGEX`; a sync comment links them.

## Testing & verification

- `scripts/smoke.sh` additions: a code page with filter params returns 200
  and renders the same row count as the canonical page (server ignores
  params); codes index with params returns 200.
- Programmatic browser matrix (preview): every filter grammar form incl.
  comma-AND and invalid input; sort from both locations with arrow/
  highlight updates; tag toggling from all five link surfaces; count labels;
  empty state; URL sync incl. back/forward; deep-link application;
  favorites-filter + numeric filter intersection; keynav skipping hidden
  rows; lazy bodies on filtered rows; download-all URL params; weight
  filter only on weighted codes; localStorage tag-view persistence.
- `lint`, `format:check`, `build`, `pytest`, `smoke.sh`.

## Rollout

- Branch `feat/client-side-filtering` off `main`; PR; patch bump
  0.4.9 → 0.4.10 (URL contract and YAML/DB unchanged).
