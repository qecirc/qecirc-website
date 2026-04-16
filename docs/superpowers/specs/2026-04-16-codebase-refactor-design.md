# QECirc Codebase Refactor — Design Spec

**Date:** 2026-04-16
**Scope:** Component extraction, JS module organization, queries split, accessibility fixes, documentation update
**Strategy:** Incremental — each section is an independent commit, tested between steps

---

## 1. Component Extraction

### 1a. MetricBadge.astro

**New file:** `src/components/MetricBadge.astro`

Props:

- `value: number | null` — metric value (renders nothing if null)
- `color: "amber" | "purple" | "green" | "blue"` — badge color theme
- `label?: string` — optional visible prefix (e.g. `"G:"` on detail page, omitted on rows)
- `title: string` — tooltip text (e.g. "Gate count")

Replaces repeated badge markup in:

- `src/components/CircuitRow.astro` (lines 82-108)
- `src/pages/circuits/[qec_id].astro` (lines 87-106)

Note: The favorites page builds badges in client JS — this cannot use the Astro component directly but should reference the same color constants.

### 1b. CollapsibleSection.astro

**New file:** `src/components/CollapsibleSection.astro`

Props:

- `id: string` — unique identifier for the toggle/detail pair
- `label: string` — button text
- `open?: boolean` — initial state (default: false)

Renders: chevron button + `<slot>` wrapped in max-height transition div. Includes a small inline script for the toggle behavior.

Replaces toggle pattern in:

- `src/pages/codes/[code].astro` (matrices toggle, lines 70-98 + 165-182)
- `src/pages/circuits/[qec_id].astro` (originals toggle, lines 196-231 + 234-251)

### 1c. FormatSwitcher.astro

**New file:** `src/components/FormatSwitcher.astro`

Props:

- `bodies: CircuitBody[]` — array of format/body pairs
- `stimFilename?: string` — download filename for stim format
- `source?: string` — citation source passed to CodeBlock

Renders: tab buttons + CodeBlock instances with format switching. Includes inline script for tab logic.

Replaces format switcher in:

- `src/components/CircuitRow.astro` (lines 203-335)
- `src/pages/circuits/[qec_id].astro` (lines 165-187 + 254-274)

### 1d. HeartIcon.astro

**New file:** `src/components/HeartIcon.astro`

Props:

- `filled?: boolean` — outline vs filled (default: false)
- `class?: string` — size/color classes

Replaces 7+ duplicated heart SVG definitions across Layout, CircuitRow, CircuitFilter, circuit detail page, and favorites page.

### 1e. Utility Dedup

**New file:** `src/lib/utils.ts`

Extract `safeParseMatrix(json: string | null): number[][] | null` — currently duplicated identically in:

- `src/pages/circuits/[qec_id].astro` (line 44)
- `src/pages/codes/[code].astro` (line 32)

---

## 2. JS Module Extraction

### 2a. toggle-client.ts

**New file:** `src/lib/toggle-client.ts`

```typescript
export function initToggle(buttonId: string, detailId: string): void;
```

Handles: chevron rotation, max-height animation, aria-expanded. Used by matrices, originals, and any CollapsibleSection that needs programmatic init.

### 2b. format-switcher-client.ts

**New file:** `src/lib/format-switcher-client.ts`

```typescript
export function initFormatSwitchers(root?: HTMLElement): void;
```

Handles: tab active state, body show/hide, max-height recalculation. Consolidates duplicate logic from CircuitRow and circuit detail page scripts.

### 2c. Inline Script Reduction

**CircuitRow.astro:** Current ~145 lines shrinks to ~40 lines calling:

- `initFormatSwitchers()` from format-switcher-client.ts
- `initFavorites()` (already uses imported favorites-client.ts)
- Permalink/ID copy handlers (stay inline — small and page-specific)

**[qec_id].astro:** Current ~65 lines shrinks to ~20 lines calling:

- `initToggle("originals-toggle", "originals-detail")`
- `initFormatSwitchers()`
- Favorites init (stays inline — page-specific)

**[code].astro:** Current ~50 lines shrinks to ~15 lines calling:

- `initToggle("matrices-toggle", "matrices-detail")`
- Download handler (stays inline — page-specific)

---

## 3. Split queries.ts

Split `src/lib/queries.ts` (547 lines) into domain modules:

| Module                        | Functions                                                                                                                                                                                                                                                   | ~Lines |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| `src/lib/queries/shared.ts`   | `withTags`, `withCircuitCounts`, `addConditions`, `addTagConditions`, `getTagsFor`                                                                                                                                                                          | ~80    |
| `src/lib/queries/codes.ts`    | `getAllCodes`, `getCodeBySlug`, `filterCodes`, `getCodeTagsForFilter`, `countCodes`, `formatCodeParams`                                                                                                                                                     | ~120   |
| `src/lib/queries/circuits.ts` | `getCircuitsForCode`, `filterCircuitsForCode`, `getCircuitsWithBodies`, `getBodiesForCircuits`, `getCircuitByQecId`, `getCircuitsByQecIds`, `getOriginalForCircuit`, `countCircuitsForCode`, `getCircuitTagsForCode`, `formatCircuitId`, `hasActiveFilters` | ~200   |
| `src/lib/queries/tools.ts`    | `getAllTools`, `getToolBySlug`, `filterTools`, `getToolsForCircuits`                                                                                                                                                                                        | ~70    |
| `src/lib/queries/search.ts`   | `searchByType`, `searchCodes`, `searchCircuits`, `searchTools`                                                                                                                                                                                              | ~80    |
| `src/lib/queries/index.ts`    | Re-exports from all modules                                                                                                                                                                                                                                 | ~10    |

**Key constraint:** The `index.ts` barrel export ensures all existing imports (`from "../lib/queries"`) continue to work unchanged. No import paths need updating.

---

## 4. Accessibility Pass

### 4a. Color Contrast

- Audit all `text-gray-400` on white/light backgrounds — bump to `text-gray-500` where contrast ratio falls below WCAG AA (4.5:1)
- Same for dark mode `text-gray-500` on `bg-gray-950`

### 4b. Keyboard Navigation

- Add `tabindex="0"` and `keydown` handler (Enter/Space) to format tab buttons
- Ensure arrow key navigation between tabs follows WAI-ARIA tabs pattern

### 4c. ARIA Attributes

- Add `aria-expanded` to matrices toggle button in `[code].astro` (currently missing)
- Add `aria-label="Import favorites file"` to hidden file input in `favorites.astro`
- Verify all decorative SVGs have `aria-hidden="true"`

### 4d. Screen Reader

- Add `aria-hidden="true"` to SearchBar keyboard hint (`/` badge)

---

## 5. Documentation Update

### CLAUDE.md

- Update rendering strategy section (line 107-109) to accurately describe client-side JS scope:
  - Remove "minimal" qualifier
  - List actual interactive features: search bar, circuit row expand/collapse, format switching, favorites, filter validation, copy-to-clipboard
- Update repository structure section to reflect new `src/lib/queries/` directory

---

## Verification

After each incremental step:

1. `npm run build` — no build errors
2. `npm run lint` — no lint errors
3. `npm run format:check` — formatting clean
4. Manual spot-check that the affected UI still works as before

After all steps: 5. Full manual walkthrough: browse codes, expand circuits, switch formats, favorite/unfavorite, visit favorites page, export/import, download, search
