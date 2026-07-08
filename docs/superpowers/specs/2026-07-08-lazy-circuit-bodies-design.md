# Lazy-load circuit bodies on code pages — design

**Date:** 2026-07-08
**Status:** Approved

## Problem

Code pages (`/codes/[code]`) render every circuit's body in every format
(STIM, QASM, Cirq) into the initial HTML, inside collapsed rows that most
visitors never expand. Each body ships **twice**: once in the `<pre>` (with a
line-number gutter) and once HTML-escaped in the copy button's `data-code`
attribute. On top of that, each row carries ~13 kB of repeated static chrome
(format tabs, copy/download buttons, SVG icons, kbd hints) × 3 CodeBlocks.

Measured on `/codes/flag-gadgets` (354 circuits, 1000 bodies):

| Metric | Value |
| --- | --- |
| HTML size | 15.2 MB (640 kB compressed in production) |
| DOM nodes | 39,248 (~25× Lighthouse's "excessive DOM" threshold) |
| `domInteractive` | ~334 ms on fast desktop; est. 1.5–3 s on mid-range mobile |

## Goal

Ship code pages without inline circuit bodies or per-row CodeBlock chrome.
Target: ~1–2 MB HTML and ~9k DOM nodes on `flag-gadgets`, with no visible
UX change beyond a brief "Loading circuit…" state on first expand.

## Non-goals

- Circuit detail pages (`/circuits/[qec_id]`) keep fully server-rendered
  bodies — they are small (~93 kB) and carry the `SoftwareSourceCode`
  JSON-LD for SEO. `CodeBlock.astro` is unchanged, including its `data-code`
  attribute (harmless at ≤4 blocks per page).
- No pagination/virtualization of circuit rows (re-evaluate if needed after
  this lands).
- No changes to `/api/download` (download-all zip is built server-side).

## Design

### 1. New API endpoint: `GET /api/circuits/[qec_id]/bodies`

- File: `src/pages/api/circuits/[qec_id]/bodies.ts`, `prerender = false`.
- Validates `qec_id` (positive integer), looks up the circuit, returns:

  ```json
  { "bodies": [{ "format": "stim", "body": "..." }, ...] }
  ```

- Bodies sorted in the existing preferred order (stim, qasm, cirq) by
  reusing `getBodiesForCircuits` / `FORMAT_ORDER` from
  `src/lib/queries/circuits.ts` (export a small
  `getBodiesForCircuitByQecId(qecId)` helper there).
- 404 when the circuit doesn't exist or has no bodies.
- `Cache-Control: public, max-age=3600` — same as the sibling
  `originals.ts` and `matrices.ts` endpoints. Safe because `qec_id` is
  permanent and never reused; body edits between deploys tolerate ≤1 h of
  browser-cache staleness.

### 2. `CircuitRow.astro` — stop rendering bodies

- Remove the `bodies` prop and the `<FormatSwitcher>` usage.
- The detail panel keeps the server-rendered metadata block (ID, source,
  tool, Crumble/Quirk links, notes) and gains a placeholder:

  ```html
  <div class="circuit-bodies" data-qec-id={...} data-stim-filename={...} data-source={...}>
    <p class="circuit-bodies-status text-sm text-gray-400">Loading circuit…</p>
  </div>
  ```

- `stimFilename` (already computed server-side per row) and `source` move
  onto the placeholder as data attributes so the client can build download
  names and cite notices without re-deriving them.
- `codes/[code].astro` stops calling `getCircuitsWithBodies` and calls the
  filter/sort query directly (no `bodiesMap`).

### 3. Shared `<template>` for the switcher/CodeBlock skeleton

- New component `CircuitBodiesTemplate.astro`, rendered **once** per code
  page (from `codes/[code].astro`), containing a `<template
  id="circuit-bodies-template">` with the FormatSwitcher + CodeBlock
  markup skeleton: tab bar (with kbd hints), and one format-body block
  (header with label, download button, copy button; empty `<pre><code>`).
  The client clones the format-body block per format and the tab button
  per format.
- Markup is copied from `FormatSwitcher.astro` / `CodeBlock.astro`; both
  files get a "keep in sync with CircuitBodiesTemplate.astro" comment (and
  vice versa). This is the accepted trade-off of approach A.

### 4. New client module: `src/lib/circuit-bodies-client.ts`

Modeled on the `CodeMatrices` lazy-load script:

- `initCircuitBodies({ containerSelector, templateId })` called from the
  code page script.
- Hooks the row-expand path via a custom event: `CircuitRow`'s existing
  toggle handler dispatches `circuit-expand` on the `.circuit-detail`
  element whenever it expands a row (same pattern as
  `CollapsibleSection`'s `collapsible-open`). All expand entry points —
  click, keyboard nav (which synthesizes a click), and `expandFromHash` —
  flow through that handler, so one event covers them all.
  `circuit-bodies-client` listens for it and calls
  `loadBodies(placeholder)`.
- `loadBodies`:
  - WeakSet guard so each row fetches once; on fetch failure the guard is
    released and the status text becomes
    "Failed to load — collapse and expand to retry."
  - Fetches `/api/circuits/${qecId}/bodies`, clones the template, fills:
    - tab buttons per format (labels + `1`/`2`/`3` kbd hints, first active),
      hidden entirely when only one format exists (matching current
      `hasMultipleFormats` behavior);
    - per-format `<pre><code>` with line-numbered text (same
      gutter-padding logic as `CodeBlock.astro`: line numbers padded to
      the width of the last line number, two-space separator);
    - download names derived from `data-stim-filename` with the format
      extension swapped (same rule as `FormatSwitcher.downloadNameFor`).
  - Copy/download handlers read the **raw body from a JS map** (no
    `data-code` attribute) and fire the existing cite-toast, mirroring
    `CodeBlock`'s script behavior.
  - Calls `initFormatSwitchers(clonedRoot)` (it already accepts a root)
    to wire tab switching.
  - Re-syncs the collapse animation: `detail.style.maxHeight =
    detail.scrollHeight + "px"` after insertion (and the existing
    format-switcher client already re-syncs on tab clicks).

### 5. Keyboard shortcuts and existing behaviors

- `circuit-actions-client` (keys `1/2/3`, `c`, `y`, `d`) targets elements
  by class inside the expanded `.circuit-detail`; the cloned template uses
  the same class names (`format-tab`, `copy-btn`, `download-btn`), so the
  shortcuts work once bodies are loaded. Before the fetch resolves, the
  keys are no-ops for that row (querySelector finds nothing) — acceptable
  for a <100 ms window.
- Hash permalinks (`/codes/foo#42`): `expandFromHash` clicks the toggle,
  which triggers the same expand path and therefore the fetch.
- Favorites filter, sorting, tag filtering, download-all: untouched.

## Files touched

| File | Change |
| --- | --- |
| `src/pages/api/circuits/[qec_id]/bodies.ts` | new endpoint |
| `src/lib/queries/circuits.ts` | add `getBodiesForCircuitByQecId`; remove `getCircuitsWithBodies` (its only caller was `codes/[code].astro`) |
| `src/components/CircuitRow.astro` | remove FormatSwitcher/bodies, add placeholder |
| `src/components/CircuitBodiesTemplate.astro` | new template component |
| `src/lib/circuit-bodies-client.ts` | new client module |
| `src/pages/codes/[code].astro` | drop bodiesMap, render template, init client module |
| `src/components/FormatSwitcher.astro`, `CodeBlock.astro` | sync comments only |
| `scripts/smoke.sh` | add bodies-endpoint check |
| `package.json`, `pyproject.toml`, `uv.lock` | version bump 0.4.6 → 0.4.7 |

## Testing & verification

1. `npm run lint`, `npm run format:check`, `npm run build`.
2. `scripts/smoke.sh` against the dev server, including the new endpoint
   check (fetch a real `qec_id` from `/api/circuits?ids=…`, assert JSON
   shape).
3. Browser verification on `/codes/flag-gadgets` and a small code page:
   expand a row (bodies appear, tabs switch, copy + download work, cite
   toast fires), keyboard shortcuts `1/2/3/c/d`, hash permalink
   auto-expand, favorites filter, single-format circuits (no tab bar).
4. Re-measure: HTML size and DOM nodes on `/codes/flag-gadgets` before vs
   after (expect ~15 MB → ~1–2 MB, ~39k → ~9k nodes).

## Rollout

- Branch + PR per repo convention (no direct commits to `main`).
- Commit: `feat(browse): lazy-load circuit bodies on code pages`.
- Patch version bump (non-breaking, no schema change).
- Follow-up (separate, config-only): Cloudflare Cache Rule to activate the
  existing `s-maxage` headers — instructions to be provided at that point.
