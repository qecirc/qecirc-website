# QECirc Codebase Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce code duplication, extract shared components, organize JS modules, split queries.ts, and fix accessibility issues — all without changing user-visible behavior.

**Architecture:** Incremental refactor in 6 independent commits. Each commit is a self-contained change that passes build+lint. Components are extracted bottom-up (shared utilities first, then components that use them). The queries.ts split uses a barrel re-export so no import paths change.

**Tech Stack:** Astro v6, TypeScript, Tailwind CSS, better-sqlite3

**Spec:** `docs/superpowers/specs/2026-04-16-codebase-refactor-design.md`

---

## File Map

### New files

| File                                      | Responsibility                                        |
| ----------------------------------------- | ----------------------------------------------------- |
| `src/lib/utils.ts`                        | Shared utility functions (safeParseMatrix)            |
| `src/components/MetricBadge.astro`        | Reusable metric badge (amber/purple/green/blue)       |
| `src/components/HeartIcon.astro`          | Heart SVG component (outline/filled)                  |
| `src/components/CollapsibleSection.astro` | Chevron toggle + max-height animated content          |
| `src/components/FormatSwitcher.astro`     | Format tab switching with CodeBlock rendering         |
| `src/lib/toggle-client.ts`                | Shared collapse/expand JS logic                       |
| `src/lib/format-switcher-client.ts`       | Shared format tab switching JS logic                  |
| `src/lib/queries/index.ts`                | Barrel re-export of all query modules                 |
| `src/lib/queries/shared.ts`               | Private query helpers (withTags, addConditions, etc.) |
| `src/lib/queries/codes.ts`                | Code-related queries                                  |
| `src/lib/queries/circuits.ts`             | Circuit-related queries                               |
| `src/lib/queries/tools.ts`                | Tool-related queries                                  |
| `src/lib/queries/search.ts`               | Search queries                                        |

### Modified files

| File                                 | Changes                                                                     |
| ------------------------------------ | --------------------------------------------------------------------------- |
| `src/components/CircuitRow.astro`    | Use MetricBadge, HeartIcon, FormatSwitcher; slim script                     |
| `src/components/CircuitFilter.astro` | Use HeartIcon                                                               |
| `src/components/Layout.astro`        | Use HeartIcon constant                                                      |
| `src/pages/circuits/[qec_id].astro`  | Use MetricBadge, HeartIcon, CollapsibleSection, FormatSwitcher; slim script |
| `src/pages/codes/[code].astro`       | Use CollapsibleSection; slim script                                         |
| `src/pages/favorites.astro`          | Use exported badge color constants                                          |
| `src/components/SearchBar.astro`     | Add aria-hidden to kbd hint                                                 |
| `CLAUDE.md`                          | Update rendering strategy and repository structure                          |

### Deleted files

| File                 | Reason                                   |
| -------------------- | ---------------------------------------- |
| `src/lib/queries.ts` | Replaced by `src/lib/queries/` directory |

---

## Task 1: Extract shared utilities and constants

**Files:**

- Create: `src/lib/utils.ts`
- Modify: `src/pages/circuits/[qec_id].astro:44-47`
- Modify: `src/pages/codes/[code].astro:32-35`
- Modify: `src/lib/constants.ts`

- [ ] **Step 1: Create `src/lib/utils.ts`**

```typescript
export function safeParseMatrix(json: string | null): number[][] | null {
  if (!json) return null;
  try {
    return JSON.parse(json);
  } catch {
    return null;
  }
}
```

- [ ] **Step 2: Add badge color map to `src/lib/constants.ts`**

Append to the existing file:

```typescript
export const METRIC_COLORS = {
  amber: {
    bg: "bg-amber-50 dark:bg-amber-900/30",
    text: "text-amber-700 dark:text-amber-300",
  },
  purple: {
    bg: "bg-purple-50 dark:bg-purple-900/30",
    text: "text-purple-700 dark:text-purple-300",
  },
  green: {
    bg: "bg-green-50 dark:bg-green-900/30",
    text: "text-green-700 dark:text-green-300",
  },
  blue: {
    bg: "bg-blue-50 dark:bg-blue-900/30",
    text: "text-blue-700 dark:text-blue-300",
  },
} as const;

export const HEART_PATH =
  "M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z";
```

- [ ] **Step 3: Update `src/pages/circuits/[qec_id].astro`**

Replace the inline `safeParseMatrix` function (lines 44-47) with an import:

```typescript
import { safeParseMatrix } from "../../lib/utils";
```

Remove lines 44-47 (the local function definition).

- [ ] **Step 4: Update `src/pages/codes/[code].astro`**

Replace the inline `safeParseMatrix` function (lines 32-35) with an import:

```typescript
import { safeParseMatrix } from "../../lib/utils";
```

Remove lines 32-35 (the local function definition).

- [ ] **Step 5: Build and lint**

Run: `npm run build && npm run lint && npm run format:check`
Expected: All pass, no errors.

- [ ] **Step 6: Commit**

```bash
git add src/lib/utils.ts src/lib/constants.ts src/pages/circuits/\[qec_id\].astro src/pages/codes/\[code\].astro
git commit -m "refactor: extract safeParseMatrix and shared constants"
```

---

## Task 2: Extract HeartIcon and MetricBadge components

**Files:**

- Create: `src/components/HeartIcon.astro`
- Create: `src/components/MetricBadge.astro`
- Modify: `src/components/CircuitRow.astro`
- Modify: `src/components/CircuitFilter.astro`
- Modify: `src/components/Layout.astro`
- Modify: `src/pages/circuits/[qec_id].astro`

- [ ] **Step 1: Create `src/components/HeartIcon.astro`**

```astro
---
import { HEART_PATH } from "../lib/constants";

interface Props {
  filled?: boolean;
  class?: string;
}

const { filled = false, class: className = "w-3.5 h-3.5" } = Astro.props;
---

<svg
  class={className}
  fill={filled ? "currentColor" : "none"}
  stroke="currentColor"
  stroke-width="2"
  viewBox="0 0 24 24"
  aria-hidden="true"
>
  <path d={HEART_PATH} />
</svg>
```

- [ ] **Step 2: Create `src/components/MetricBadge.astro`**

```astro
---
import { METRIC_COLORS } from "../lib/constants";

interface Props {
  value: number | null;
  color: keyof typeof METRIC_COLORS;
  label?: string;
  title: string;
}

const { value, color, label, title } = Astro.props;
const colors = METRIC_COLORS[color];
---

{value != null && (
  <span class={`text-xs ${colors.bg} ${colors.text} px-1.5 py-0.5 rounded`} title={title}>
    {label ? `${label} ${value}` : value}
  </span>
)}
```

- [ ] **Step 3: Update `src/components/CircuitRow.astro` to use HeartIcon and MetricBadge**

Add imports at top of frontmatter:

```typescript
import HeartIcon from "./HeartIcon.astro";
import MetricBadge from "./MetricBadge.astro";
```

Replace the heart button SVGs (lines 74-79) with:

```astro
<HeartIcon class="fav-outline w-3.5 h-3.5" />
<HeartIcon filled class="fav-filled w-3.5 h-3.5 hidden" />
```

Replace the four metric badge spans (lines 82-108) with:

```astro
<span class="text-xs text-center">
  <MetricBadge value={circuit.gate_count} color="amber" title="Gate count" />
</span>
<span class="text-xs text-center">
  <MetricBadge value={circuit.two_qubit_gate_count} color="purple" title="Two-qubit gate count" />
</span>
<span class="text-xs text-center">
  <MetricBadge value={circuit.depth} color="green" title="Circuit depth" />
</span>
<span class="text-xs text-center">
  <MetricBadge value={circuit.qubit_count} color="blue" title="Qubit count" />
</span>
```

- [ ] **Step 4: Update `src/pages/circuits/[qec_id].astro` to use HeartIcon and MetricBadge**

Add imports:

```typescript
import HeartIcon from "../../components/HeartIcon.astro";
import MetricBadge from "../../components/MetricBadge.astro";
```

Replace the heart button SVGs (lines 77-82) with:

```astro
<HeartIcon class="fav-outline w-5 h-5" />
<HeartIcon filled class="fav-filled w-5 h-5 hidden" />
```

Replace the four metric badge spans (lines 87-106) with:

```astro
<div class="flex flex-wrap gap-2 mb-4">
  <MetricBadge value={circuit.gate_count} color="amber" label="G:" title="Gate count" />
  <MetricBadge value={circuit.two_qubit_gate_count} color="purple" label="2Q:" title="Two-qubit gate count" />
  <MetricBadge value={circuit.depth} color="green" label="D:" title="Circuit depth" />
  <MetricBadge value={circuit.qubit_count} color="blue" label="Q:" title="Qubit count" />
</div>
```

- [ ] **Step 5: Update `src/components/CircuitFilter.astro` to use HeartIcon**

Add import:

```typescript
import HeartIcon from "./HeartIcon.astro";
```

Replace the inline heart SVG in the favorites toggle button (lines 93-95) with:

```astro
<HeartIcon class="w-3 h-3 inline -mt-0.5" />
```

- [ ] **Step 6: Update `src/components/Layout.astro` to use HEART_PATH constant**

Replace the `heartIconSvg` string template (line 23) with:

```typescript
import { HEART_PATH } from "../lib/constants";

const heartIconSvg = `<svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="${HEART_PATH}" /></svg>`;
```

Note: Layout.astro uses `set:html` injection, so it must stay as a string template. But the path is now from the shared constant.

- [ ] **Step 7: Build and lint**

Run: `npm run build && npm run lint && npm run format:check`
Expected: All pass. Fix any formatting issues with `npm run format`.

- [ ] **Step 8: Commit**

```bash
git add src/components/HeartIcon.astro src/components/MetricBadge.astro src/components/CircuitRow.astro src/components/CircuitFilter.astro src/components/Layout.astro src/pages/circuits/\[qec_id\].astro
git commit -m "refactor: extract HeartIcon and MetricBadge components"
```

---

## Task 3: Extract CollapsibleSection and FormatSwitcher components

**Files:**

- Create: `src/components/CollapsibleSection.astro`
- Create: `src/components/FormatSwitcher.astro`
- Create: `src/lib/toggle-client.ts`
- Create: `src/lib/format-switcher-client.ts`
- Modify: `src/components/CircuitRow.astro`
- Modify: `src/pages/circuits/[qec_id].astro`
- Modify: `src/pages/codes/[code].astro`

- [ ] **Step 1: Create `src/lib/toggle-client.ts`**

```typescript
export function initToggle(buttonId: string, detailId: string): void {
  const toggle = document.getElementById(buttonId);
  const detail = document.getElementById(detailId);
  if (!toggle || !detail) return;

  const chevron = toggle.querySelector("svg");

  toggle.addEventListener("click", function () {
    const isOpen = detail.style.maxHeight !== "0px";
    if (isOpen) {
      detail.style.maxHeight = "0px";
      chevron?.classList.remove("rotate-90");
      toggle.setAttribute("aria-expanded", "false");
    } else {
      detail.style.maxHeight = detail.scrollHeight + "px";
      chevron?.classList.add("rotate-90");
      toggle.setAttribute("aria-expanded", "true");
    }
  });
}
```

- [ ] **Step 2: Create `src/lib/format-switcher-client.ts`**

```typescript
const ACTIVE_CLASS =
  "format-tab px-3 py-1 text-xs rounded cursor-pointer transition-colors bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900";
const INACTIVE_CLASS =
  "format-tab px-3 py-1 text-xs rounded cursor-pointer transition-colors bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700";

export function initFormatSwitchers(
  root: HTMLElement | Document = document,
): void {
  root.querySelectorAll(".format-switcher").forEach(function (switcher) {
    const tabs = switcher.querySelectorAll(".format-tab");
    const bodies = switcher.querySelectorAll(".format-body");

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        const format = (tab as HTMLElement).dataset.format;

        tabs.forEach(function (t) {
          (t as HTMLElement).className =
            (t as HTMLElement).dataset.format === format
              ? ACTIVE_CLASS
              : INACTIVE_CLASS;
        });

        bodies.forEach(function (b) {
          (b as HTMLElement).style.display =
            (b as HTMLElement).dataset.format === format ? "" : "none";
        });

        // Recalculate max-height for parent collapse container
        const detail = switcher.closest(".circuit-detail") as HTMLElement;
        if (detail && detail.style.maxHeight !== "0px") {
          requestAnimationFrame(function () {
            detail.style.maxHeight = detail.scrollHeight + "px";
          });
        }
      });
    });
  });
}
```

- [ ] **Step 3: Create `src/components/CollapsibleSection.astro`**

```astro
---
interface Props {
  id: string;
  label: string;
  open?: boolean;
}

const { id, label, open = false } = Astro.props;
const buttonId = `${id}-toggle`;
const detailId = `${id}-detail`;
---

<div>
  <button
    id={buttonId}
    class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 cursor-pointer"
    aria-expanded={String(open)}
  >
    <svg
      class:list={["w-3.5 h-3.5 shrink-0 transition-transform duration-200", open && "rotate-90"]}
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <path d="M9 5l7 7-7 7" />
    </svg>
    {label}
  </button>
  <div
    id={detailId}
    class="overflow-hidden transition-[max-height] duration-300 ease-in-out"
    style={open ? undefined : "max-height: 0px;"}
  >
    <div class="mt-3">
      <slot />
    </div>
  </div>
</div>

<script define:vars={{ buttonId, detailId }}>
  import("../lib/toggle-client").then(({ initToggle }) => {
    initToggle(buttonId, detailId);
  });
</script>
```

- [ ] **Step 4: Create `src/components/FormatSwitcher.astro`**

```astro
---
import type { CircuitBody } from "../types";
import CodeBlock from "./CodeBlock.astro";

interface Props {
  bodies: CircuitBody[];
  stimFilename?: string;
  source?: string;
}

const { bodies, stimFilename, source } = Astro.props;
const hasMultipleFormats = bodies.length > 1;
---

{hasMultipleFormats ? (
  <div class="format-switcher">
    <div class="flex gap-1 mb-2">
      {bodies.map((b, i) => (
        <button
          class:list={[
            "format-tab px-3 py-1 text-xs rounded cursor-pointer transition-colors",
            i === 0
              ? "bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900"
              : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700",
          ]}
          data-format={b.format}
        >
          {b.format.toUpperCase()}
        </button>
      ))}
    </div>
    {bodies.map((b, i) => (
      <div class="format-body" data-format={b.format} style={i === 0 ? "" : "display:none"}>
        <CodeBlock
          code={b.body}
          label={`${b.format.toUpperCase()} Circuit`}
          downloadName={b.format === "stim" ? stimFilename : undefined}
          source={source}
        />
      </div>
    ))}
  </div>
) : bodies.length === 1 ? (
  <CodeBlock
    code={bodies[0].body}
    label={`${bodies[0].format.toUpperCase()} Circuit`}
    downloadName={bodies[0].format === "stim" ? stimFilename : undefined}
    source={source}
  />
) : (
  <p class="text-sm text-gray-400">No circuit body available.</p>
)}

<script>
  import { initFormatSwitchers } from "../lib/format-switcher-client";
  initFormatSwitchers();
</script>
```

- [ ] **Step 5: Update `src/pages/codes/[code].astro` to use CollapsibleSection**

Replace the matrices toggle section (lines 70-98) with:

```astro
import CollapsibleSection from "../../components/CollapsibleSection.astro";
```

```astro
{hasMatrices && (
  <div class="mb-6">
    <CollapsibleSection id="matrices" label="Check Matrices & Logical Operators">
      <div class="grid gap-x-6 gap-y-2 sm:grid-cols-2">
        {hx && <MatrixDisplay label="Hx (X-checks)" matrix={hx} />}
        {hz && <MatrixDisplay label="Hz (Z-checks)" matrix={hz} />}
        {logicalX && <MatrixDisplay label="Logical X" matrix={logicalX} />}
        {logicalZ && <MatrixDisplay label="Logical Z" matrix={logicalZ} />}
      </div>
    </CollapsibleSection>
  </div>
)}
```

Remove the matrices toggle JS from the script block (lines 165-182).

- [ ] **Step 6: Update `src/pages/circuits/[qec_id].astro` to use CollapsibleSection and FormatSwitcher**

Add imports:

```typescript
import CollapsibleSection from "../../components/CollapsibleSection.astro";
import FormatSwitcher from "../../components/FormatSwitcher.astro";
```

Replace the format switcher section (lines 165-194) with:

```astro
<h2 class="text-lg font-semibold mb-2">Circuit</h2>
<div class="mb-6">
  <FormatSwitcher bodies={bodies} stimFilename={stimFilename} source={circuit.source} />
</div>
```

Replace the originals toggle section (lines 196-231) with:

```astro
{original && (
  <div class="border-t border-gray-200 dark:border-gray-800 pt-4">
    <CollapsibleSection id="originals" label="Original submission (before canonicalization)">
      <div class="space-y-4">
        {original?.original_stim && (
          <CodeBlock code={original.original_stim} label="Original STIM Circuit" source={circuit.source} />
        )}
        {hasOriginalMatrices && (
          <div class="grid gap-x-6 gap-y-2 sm:grid-cols-2">
            {origHx && <MatrixDisplay label="Original Hx (X-checks)" matrix={origHx} />}
            {origHz && <MatrixDisplay label="Original Hz (Z-checks)" matrix={origHz} />}
            {origLx && <MatrixDisplay label="Original Logical X" matrix={origLx} />}
            {origLz && <MatrixDisplay label="Original Logical Z" matrix={origLz} />}
          </div>
        )}
      </div>
    </CollapsibleSection>
  </div>
)}
```

Remove the originals toggle JS and format switcher JS from the script block (lines 234-252, 280-299). Keep only the favorites toggle script.

- [ ] **Step 7: Update `src/components/CircuitRow.astro` to use FormatSwitcher and extracted JS**

Add import:

```typescript
import FormatSwitcher from "./FormatSwitcher.astro";
```

Replace the format switcher markup (lines 203-225) with:

```astro
<FormatSwitcher bodies={bodies} stimFilename={stimFilename} source={circuit.source} />
```

In the script block, remove `initFormatSwitchers()` function (lines 302-335) and its call (line 429). The FormatSwitcher component now handles its own initialization.

- [ ] **Step 8: Build and lint**

Run: `npm run build && npm run lint && npm run format:check`
Expected: All pass. Fix formatting with `npm run format` if needed.

- [ ] **Step 9: Commit**

```bash
git add src/components/CollapsibleSection.astro src/components/FormatSwitcher.astro src/lib/toggle-client.ts src/lib/format-switcher-client.ts src/components/CircuitRow.astro src/pages/circuits/\[qec_id\].astro src/pages/codes/\[code\].astro
git commit -m "refactor: extract CollapsibleSection and FormatSwitcher components"
```

---

## Task 4: Split queries.ts into domain modules

**Files:**

- Create: `src/lib/queries/shared.ts`
- Create: `src/lib/queries/codes.ts`
- Create: `src/lib/queries/circuits.ts`
- Create: `src/lib/queries/tools.ts`
- Create: `src/lib/queries/search.ts`
- Create: `src/lib/queries/index.ts`
- Delete: `src/lib/queries.ts`

This task requires reading the full queries.ts file and splitting it. The barrel `index.ts` re-exports everything so no import paths change.

- [ ] **Step 1: Create `src/lib/queries/shared.ts`**

Move these from `queries.ts`:

- `getTagsFor` (lines 31-45)
- `withTags` (lines 47-55)
- `withCircuitCounts` (lines 57-72)
- `parseFilterString` (lines 111-133)
- `hasActiveFilters` (lines 135-139)
- `addConditions` (lines 141-153)
- `addTagConditions` (lines 155-169)
- `getTagsWithCount` (lines 96-106)
- `buildOrderBy` (lines 87-94)

Export all public functions. Keep `withTags`, `withCircuitCounts`, `addConditions`, `addTagConditions`, `buildOrderBy` as named exports (they're used by other query modules).

```typescript
import { getDb } from "../db";
import type {
  CircuitSort,
  FilterCondition,
  FilterOp,
  TaggableType,
  TagWithCount,
} from "../../types";
import { CIRCUIT_SORT_FIELDS, FILTER_PART_REGEX } from "../constants";
// ... move function bodies here
```

- [ ] **Step 2: Create `src/lib/queries/codes.ts`**

Move these from `queries.ts`:

- `formatCodeParams` (lines 25-29)
- `getAllCodes` (lines 74-78)
- `getCodeBySlug` (lines 80-85)
- `filterCodes` (lines 171-187)
- `countAllCodes` (lines 189-195)

```typescript
import { getDb } from "../db";
import type { Code, CodeFilters, CodeWithMeta } from "../../types";
import {
  withTags,
  withCircuitCounts,
  addConditions,
  addTagConditions,
  getTagsWithCount,
} from "./shared";
// ... move function bodies here
```

- [ ] **Step 3: Create `src/lib/queries/circuits.ts`**

Move these from `queries.ts`:

- `formatCircuitId` (lines 21-23)
- `getCircuitsForCode` (lines 245-255)
- `countCircuitsForCode` (lines 257-263)
- `getCircuitTagsForCode` (lines 265-276)
- `filterCircuitsForCode` (lines 278-304)
- `getCircuitsWithBodies` (lines 306-319)
- `getBodiesForCircuits` (lines 323-354)
- `getCircuitByQecId` (lines 356-373)
- `getCircuitsByQecIds` (lines 375-396)
- `getOriginalForCircuit` (lines 398-410)
- `FORMAT_ORDER` constant (line 321)

```typescript
import { getDb } from "../db";
import type {
  Circuit,
  CircuitBody,
  CircuitFilters,
  CircuitOriginal,
  CircuitSort,
} from "../../types";
import {
  withTags,
  addConditions,
  addTagConditions,
  buildOrderBy,
  getTagsWithCount,
} from "./shared";
// ... move function bodies here
```

- [ ] **Step 4: Create `src/lib/queries/tools.ts`**

Move these from `queries.ts`:

- `enrichTools` private function (lines 414-416)
- `getAllTools` (lines 418-429)
- `getToolBySlug` — note: check if this exists. The grep showed `getToolById` at line 515.
- `getToolById` (lines 515-520)
- `filterTools` (lines 431-450)
- `getToolsForCircuits` (lines 522-547)

```typescript
import { getDb } from "../db";
import type { Tool, ToolFilters, ToolWithMeta } from "../../types";
import {
  withTags,
  withCircuitCounts,
  addConditions,
  addTagConditions,
  getTagsWithCount,
} from "./shared";
// ... move function bodies here
```

- [ ] **Step 5: Create `src/lib/queries/search.ts`**

Move these from `queries.ts`:

- `rawTokenize` (lines 197-202)
- `tokenize` (lines 204-206)
- `searchByType` (lines 208-237)
- `searchCodes` (lines 239-243)
- `searchCircuits` (lines 456-513)
- `searchTools` (lines 452-454)

```typescript
import { getDb } from "../db";
import type { Code, Circuit, Tool } from "../../types";
import { withTags } from "./shared";
// ... move function bodies here
```

- [ ] **Step 6: Create `src/lib/queries/index.ts`**

```typescript
export {
  getTagsFor,
  parseFilterString,
  hasActiveFilters,
  getTagsWithCount,
} from "./shared";
export {
  formatCodeParams,
  getAllCodes,
  getCodeBySlug,
  filterCodes,
  countAllCodes,
} from "./codes";
export {
  formatCircuitId,
  getCircuitsForCode,
  countCircuitsForCode,
  getCircuitTagsForCode,
  filterCircuitsForCode,
  getCircuitsWithBodies,
  getBodiesForCircuits,
  getCircuitByQecId,
  getCircuitsByQecIds,
  getOriginalForCircuit,
} from "./circuits";
export {
  getAllTools,
  getToolById,
  filterTools,
  getToolsForCircuits,
} from "./tools";
export { searchCodes, searchCircuits, searchTools } from "./search";
```

- [ ] **Step 7: Delete `src/lib/queries.ts`**

```bash
rm src/lib/queries.ts
```

- [ ] **Step 8: Build and lint**

Run: `npm run build && npm run lint && npm run format:check`
Expected: All pass. All existing imports (`from "../lib/queries"` or `from "../../lib/queries"`) resolve to `queries/index.ts` automatically.

- [ ] **Step 9: Commit**

```bash
git add src/lib/queries/ src/lib/queries.ts
git commit -m "refactor: split queries.ts into domain modules"
```

---

## Task 5: Accessibility pass

**Files:**

- Modify: `src/components/SearchBar.astro`
- Modify: `src/pages/favorites.astro`

- [ ] **Step 1: Add `aria-hidden` to SearchBar keyboard hint**

In `src/components/SearchBar.astro`, find the `<kbd>` element (line 12) and add `aria-hidden="true"`:

```astro
<kbd class="..." aria-hidden="true">/</kbd>
```

- [ ] **Step 2: Add `aria-label` to hidden file input in favorites page**

In `src/pages/favorites.astro`, find the hidden file input and add an aria-label:

```astro
<input id="import-file" type="file" accept=".json" class="hidden" aria-label="Import favorites file" />
```

- [ ] **Step 3: Build and lint**

Run: `npm run build && npm run lint && npm run format:check`
Expected: All pass.

- [ ] **Step 4: Commit**

```bash
git add src/components/SearchBar.astro src/pages/favorites.astro
git commit -m "fix(a11y): add missing aria attributes to search hint and import input"
```

---

## Task 6: Update documentation

**Files:**

- Modify: `CLAUDE.md`

- [ ] **Step 1: Update rendering strategy in CLAUDE.md**

Find the "Rendering strategy" section (around line 107) and update the client-side JS bullet:

Replace:

```
- Client-side JS (minimal): search bar (debounced fetch), CodeBlock copy button, filter input validation + auto-submit
```

With:

```
- Client-side JS: search bar (debounced fetch), circuit row expand/collapse, format switching, favorites (toggle/filter/export/import), CodeBlock copy/download, filter input validation + auto-submit
```

- [ ] **Step 2: Update repository structure in CLAUDE.md**

In the repository structure section, update the `lib/` entry to show the queries directory:

Replace:

```
│   ├── lib/               # DB client, STIM parser, helpers
```

With:

```
│   ├── lib/               # DB client, STIM parser, helpers
│   │   └── queries/       # Domain-specific DB query modules
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md for refactored structure and client-side JS scope"
```

---

## Final Verification

After all tasks are complete:

1. `npm run build` — no build errors
2. `npm run lint` — no lint errors
3. `npm run format:check` — all formatted
4. Manual walkthrough:
   - Browse `/` — codes listed, filters work
   - Click a code — circuits expand/collapse, format tabs switch, metrics display
   - Click heart on circuit row — toggles favorite state
   - Visit `/circuits/{id}` — detail page renders, heart works, originals collapsible works
   - Visit `/favorites` — favorited circuits show, grouped by code, download/export/import work
   - Use search bar — results appear, keyboard navigation works
   - Toggle dark mode — all elements render correctly
