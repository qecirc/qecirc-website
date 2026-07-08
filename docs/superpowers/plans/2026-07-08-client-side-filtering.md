# Client-Side Filtering Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> Note: this plan is executed inline in the authoring session by the author with full context; per-step code is specified at the level of exact interfaces, semantics, and parity rules rather than full listings, with the verification matrix in full detail (the priority named by the maintainer).

**Goal:** Filtering/sorting on `/` and `/codes/[slug]` runs client-side over server-rendered rows; pages become canonical (one cache entry each); the reload-per-filter-change UX and the `?focus=` hack disappear.

**Architecture:** Rows carry `data-metrics`/`data-tags`/`data-name`; a shared config-driven module `list-filter-client.ts` intercepts filter inputs, sort links, and tag links, applies via `display` toggling + DOM reorder, and syncs the URL (pushState for clicks, replaceState for typing, popstate reapplies). Server always renders the full canonical list. `/api/download` keeps server-side parsing.

**Spec:** `docs/superpowers/specs/2026-07-08-client-side-filtering-design.md` (parity rules: NULL fails conditions; NULLs sort last; circuits default sort `two_qubit_gate_count asc`; codes default `n,k,d,name`; tag AND semantics; UTF-16 name tiebreak).

**Tech Stack:** Astro v7, TypeScript. No new dependencies. Branch `feat/client-side-filtering`.

---

### Task 1: Data attributes + shared client module

**Files:**

- Create: `src/lib/list-filter-client.ts`
- Modify: `src/components/CircuitRow.astro` (outer `div[id]`: `data-metrics`, `data-tags`, `data-name`; tag links get `data-tag`)
- Modify: `src/components/CodeCard.astro` (root: same three attrs)
- Modify: `src/components/TagList.astro` (links get `data-tag`)
- Modify: `src/components/TagFilterDropdowns.astro` (popover links + chips get `data-tag`; chips container gets `data-tag-chips`)
- Modify: `src/components/CircuitFilter.astro` / `CodeFilter.astro` (sort labels get `data-sort-field`; clear link gets `data-clear-filters`; arrows become always-rendered `data-sort-arrow` spans)
- Modify: `src/pages/codes/[code].astro` (column headers get `data-sort-field`; list container gets `data-list-container`; hidden empty-state block)
- Modify: `src/pages/index.astro` (grid gets `data-list-container`; hidden empty-state block)

- [ ] **Step 1:** `list-filter-client.ts` — `initListFilter(config)` with config `{ form, fields, rowSelector, containerSelector, basePath, countTargets, emptyStateSelector, defaultSortField?, defaultSortDir? }`. State from `location.search` at init; row data parsed once into a WeakMap. Filter grammar via shared `FILTER_PART_REGEX`; validation UI identical to old `filter-client.ts` (red ring, status swap). Apply = hide/show + reorder + counts + empty state + control styling (sort arrows ▲/▼ + active classes; tag link selected classes; chips re-render; dropdown summary counts). URL sync + popstate. Semantics per spec parity rules.
- [ ] **Step 2:** Add the data attributes and markers listed above; keep all hrefs working as standalone links (generated from clean base path).
- [ ] **Step 3:** `npm run lint` — clean.
- [ ] **Step 4:** Commit `feat(browse): add list-filter client module + row data attributes`.

### Task 2: Server simplification + wiring

**Files:**

- Modify: `src/pages/index.astro`, `src/pages/codes/[code].astro` (stop parsing filter/sort params; always full list, default order; init the module; JSON-LD ItemList always rendered, capped at 200)
- Modify: `src/components/CodeFilter.astro`, `CircuitFilter.astro` (drop `raw*`/`errors`/`hasFilters`/`focus` props; empty inputs)
- Modify: `src/lib/url.ts` (drop `focus` handling and now-unused sort-URL helpers as applicable; `parseCircuitParams` stays for `/api/download` with a sync comment)
- Delete: `src/lib/filter-client.ts`
- Modify: `scripts/smoke.sh`

- [ ] **Step 1:** Page + component changes; grep confirms no remaining consumers of removed props/helpers.
- [ ] **Step 2:** smoke additions: `/codes/$slug?gate_count=%3E999999` → 200 with same `circuit-bodies-status` count as canonical; `/?n=%3E9999` → 200.
- [ ] **Step 3:** `npm run lint && npm run format && ./scripts/smoke.sh` — green.
- [ ] **Step 4:** Commit `feat(browse): client-side filtering/sorting on listing pages`.

### Task 3: Verification matrix (browser, programmatic via preview)

Codes index (`/`):

- [ ] Type `>10` in n → visible cards = cards with n>10 (computed from data attrs); URL has `n=%3E10`; Clear link appears; count label updates.
- [ ] Comma-AND `>10,<30`; `!=7`; bare `7`; `>=`/`<=` forms — each matches data-attr computation.
- [ ] Invalid input (`>>3`) → red ring + "Invalid filter"; rows unchanged; URL unchanged.
- [ ] Sort by k desc via label link → first card has max k; arrow ▼; URL `sort=k&sort_dir=desc`; click again flips.
- [ ] Tag toggle from cloud → only tagged cards; selected styling; toggle off restores.
- [ ] Deep link `/?n=>10&sort=d&sort_dir=desc` (fresh load) → filters and sort applied.
- [ ] history.back() after several changes → prior state reapplied each step.

Code page (`/codes/steane-code` + `/codes/flag-gadgets`):

- [ ] Each metric filter incl. comma-AND; rows with NULL metric excluded when that field filtered.
- [ ] Default view: 2Q label marked active-asc (parity with today).
- [ ] Sort via filter-bar label AND via column header (G/2Q/D/Q) — same result, both indicators update; NULL metrics sort last in asc and desc.
- [ ] Tag dropdown: select → chip appears, summary shows "(1)", rows filtered (AND with second tag); chip click removes; per-row tag link toggles; grouped/"all tags" view switch persists (localStorage).
- [ ] "X of Y circuits" inside download button updates; Shift+D/download-all fetch URL contains active filter params.
- [ ] Empty state on impossible filter (`gate_count=>999999`) with working clear link.
- [ ] Favorites filter (Shift+F) intersects with numeric filter.
- [ ] Keynav j/k skips hidden rows; expand (l) on a filtered-in row lazy-loads bodies.
- [ ] Hash permalink + filters: `#<id>` row visible when filters admit it.
- [ ] Weight filter present on flag-gadgets, absent on steane-code.
- [ ] JSON-LD: ItemList present with numberOfItems = total, itemListElement.length ≤ 200.

- [ ] `npm run build`, `uv run pytest -q`, `./scripts/smoke.sh` — green.
- [ ] Fix-forward any failures; re-run affected checks.

### Task 4: Housekeeping + PR

- [ ] CHANGELOG entry (Unreleased → Changed); CLAUDE.md client-side JS list + rendering-strategy note.
- [ ] Version 0.4.9 → 0.4.10 (`package.json`, `pyproject.toml`, `UV_NO_CONFIG=1 uv lock`, `npm install`); lockfile private-registry grep.
- [ ] `lint`/`format:check` final; commit `chore(release): bump version to 0.4.10`; push; PR to `main` with measured before/after cache-entry story + full verification list.
