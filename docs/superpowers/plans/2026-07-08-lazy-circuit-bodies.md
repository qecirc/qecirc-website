# Lazy-Load Circuit Bodies Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Code pages (`/codes/[code]`) stop embedding circuit bodies in HTML; bodies are fetched on first row expand via a new JSON endpoint (15 MB → ~1–2 MB on the largest page).

**Architecture:** New `/api/circuits/[qec_id]/bodies` endpoint (mirrors the existing `originals.ts`). `CircuitRow` renders a placeholder instead of `FormatSwitcher` and dispatches a `circuit-expand` CustomEvent on expand (same pattern as `toggle-client.ts`'s `collapsible-open`). A new client module clones a shared `<template>` and fills in tabs + line-numbered bodies, mirroring the `CodeMatrices` lazy-load pattern.

**Tech Stack:** Astro v7, TypeScript, better-sqlite3, Tailwind. No new dependencies.

**Spec:** `docs/superpowers/specs/2026-07-08-lazy-circuit-bodies-design.md`

**Testing note:** This repo has no JS unit-test framework (Python `pytest` covers only ingestion scripts), and the minimal-dependencies rule rules out adding one for this change. Tests here are: `scripts/smoke.sh` (integration, curl-based — extended first, red/green style, in Task 1) plus a scripted browser-verification checklist (Task 4). Work on branch `feat/lazy-circuit-bodies` (already exists; spec is committed there). The dev server must be running for smoke checks: `npm run dev` (port 4321).

---

### Task 1: Bodies API endpoint

**Files:**
- Modify: `scripts/smoke.sh` (add endpoint check)
- Modify: `src/lib/queries/circuits.ts` (add query helper)
- Modify: `src/lib/queries/index.ts` (export it)
- Create: `src/pages/api/circuits/[qec_id]/bodies.ts`

- [ ] **Step 1: Add the failing smoke check**

In `scripts/smoke.sh`, inside the `else` branch that already checks `/circuits/$qec_id`, add one line after `check "/api/circuits?ids=$qec_id" "qec_id"`:

```bash
  check "/api/circuits/$qec_id/bodies" '"format":"stim"'
```

- [ ] **Step 2: Run smoke to verify it fails**

Run: `./scripts/smoke.sh`
Expected: `FAIL /api/circuits/<id>/bodies: HTTP error` (404 — route doesn't exist yet). All other checks OK.

- [ ] **Step 3: Add the query helper**

In `src/lib/queries/circuits.ts`, add after `getBodiesForCircuits` (keep `getBodiesForCircuits` itself — `/api/download` and the circuit detail page still use it):

```ts
/** Bodies for a single circuit looked up by its public qec_id, in preferred
 * format order. Returns [] when the circuit doesn't exist. */
export function getBodiesForCircuitByQecId(qecId: number): CircuitBody[] {
  const db = getDb();
  const row = db.prepare("SELECT id FROM circuits WHERE qec_id = ?").get(qecId) as
    | { id: number }
    | undefined;
  if (!row) return [];
  return getBodiesForCircuits([row.id]).get(row.id) ?? [];
}
```

In `src/lib/queries/index.ts`, add `getBodiesForCircuitByQecId,` to the `./circuits` export list (keep alphabetical-ish placement next to `getBodiesForCircuits`).

- [ ] **Step 4: Create the endpoint**

Create `src/pages/api/circuits/[qec_id]/bodies.ts`:

```ts
export const prerender = false;

import type { APIRoute } from "astro";
import { getBodiesForCircuitByQecId } from "../../../../lib/queries";

export const GET: APIRoute = ({ params }) => {
  const qecId = Number(params.qec_id);
  if (!Number.isInteger(qecId) || qecId < 1) {
    return new Response("Invalid qec_id", { status: 400 });
  }

  const bodies = getBodiesForCircuitByQecId(qecId);
  if (bodies.length === 0) {
    return new Response("Not found", { status: 404 });
  }

  return new Response(JSON.stringify({ bodies }), {
    headers: {
      "Content-Type": "application/json",
      // qec_ids are permanent and never reused; body edits between deploys
      // tolerate <=1h of browser-cache staleness (matches originals.ts).
      "Cache-Control": "public, max-age=3600",
    },
  });
};
```

- [ ] **Step 5: Run smoke to verify it passes**

Run: `./scripts/smoke.sh`
Expected: all checks `OK`, including `OK   /api/circuits/<id>/bodies`.

Also verify edge cases:
- `curl -s -o /dev/null -w "%{http_code}" http://localhost:4321/api/circuits/999999/bodies` → `404`
- `curl -s -o /dev/null -w "%{http_code}" http://localhost:4321/api/circuits/abc/bodies` → `400`

- [ ] **Step 6: Commit**

```bash
git add scripts/smoke.sh src/lib/queries/circuits.ts src/lib/queries/index.ts "src/pages/api/circuits/[qec_id]/bodies.ts"
git commit -m "feat(api): add /api/circuits/[qec_id]/bodies endpoint

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: Template component + client module (inert until Task 3 wires them up)

**Files:**
- Create: `src/components/CircuitBodiesTemplate.astro`
- Create: `src/lib/circuit-bodies-client.ts`

- [ ] **Step 1: Create the template component**

Create `src/components/CircuitBodiesTemplate.astro`. The markup skeleton is a copy of `FormatSwitcher.astro` (tab bar) + `CodeBlock.astro` (code block) with the dynamic parts left empty — the client clones the `.format-tab` and `.format-body` prototypes once per format:

```astro
---
// Markup skeleton cloned client-side by circuit-bodies-client.ts when a
// circuit row is first expanded on a code page. Rendered once per code page.
// KEEP THE TAB / CODE-BLOCK MARKUP IN SYNC with FormatSwitcher.astro and
// CodeBlock.astro (server-rendered on circuit detail pages).
import { TAB_INACTIVE_CLASS } from "../lib/constants";

const TAB_BASE_CLASS =
  "format-tab px-3 py-1.5 text-xs font-semibold rounded-md cursor-pointer transition-colors";
---

<template id="circuit-bodies-template">
  <div class="format-switcher">
    <div class="format-tabs flex gap-0.5 mb-2">
      <button class={`${TAB_BASE_CLASS} ${TAB_INACTIVE_CLASS}`} data-format="">
        <span class="tab-label"></span>
        <kbd
          class="ml-1.5 inline-block min-w-[1rem] text-center px-1 rounded border border-gray-300 dark:border-gray-700 bg-white/60 dark:bg-gray-900/60 text-[10px] text-gray-400 dark:text-gray-500 font-mono"
        ></kbd>
      </button>
    </div>
    <div class="format-body" data-format="">
      <div
        class="rounded border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900 overflow-hidden"
        data-code-block
      >
        <div
          class="border-b border-gray-200 dark:border-gray-800 px-4 py-2 text-xs text-gray-500 dark:text-gray-400 flex items-center justify-between"
        >
          <span class="block-label"></span>
          <div class="flex items-center gap-3.5">
            <button
              class="download-btn flex items-center gap-1 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 cursor-pointer"
              aria-label="Download file"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3" />
              </svg>
              <span>Download</span>
              <kbd class="ml-0.5 inline-block min-w-[1rem] text-center px-1 rounded border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-[10px] text-gray-400 dark:text-gray-500 font-mono">
                d
              </kbd>
            </button>
            <button
              class="copy-btn flex items-center gap-1 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 cursor-pointer"
              aria-label="Copy to clipboard"
              title="Copy to clipboard (c)"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <span class="copy-label">Copy</span>
              <kbd class="ml-0.5 inline-block min-w-[1rem] text-center px-1 rounded border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-[10px] text-gray-400 dark:text-gray-500 font-mono">
                c
              </kbd>
            </button>
          </div>
        </div>
        <pre class="overflow-x-auto p-4 text-sm leading-relaxed"><code></code></pre>
      </div>
    </div>
  </div>
</template>
```

- [ ] **Step 2: Create the client module**

Create `src/lib/circuit-bodies-client.ts`:

```ts
// Lazy-loads circuit bodies on code pages. Circuit rows render without any
// circuit text; on the first expand of a row (signalled by the
// `circuit-expand` CustomEvent dispatched in CircuitRow.astro) this module
// fetches /api/circuits/<qec_id>/bodies, clones #circuit-bodies-template and
// fills in tabs + line-numbered bodies. Mirrors the CodeMatrices lazy-load
// pattern: fetch-once guard, error text, retry on next expand.

import { copyToClipboard } from "./dom-helpers";
import { initFormatSwitchers } from "./format-switcher-client";
import { TAB_ACTIVE_CLASS, TAB_INACTIVE_CLASS } from "./constants";

interface BodyEntry {
  format: string;
  body: string;
}

// Keep in sync with FormatSwitcher.astro / format-switcher-client.ts.
const TAB_BASE_CLASS =
  "format-tab px-3 py-1.5 text-xs font-semibold rounded-md cursor-pointer transition-colors";

const loaded = new WeakSet<HTMLElement>();

/** Same line-number gutter format as CodeBlock.astro. */
function lineNumbered(code: string): string {
  const lines = code.trimEnd().split("\n");
  const gutterWidth = String(lines.length).length;
  return lines
    .map((line, i) => `${String(i + 1).padStart(gutterWidth, " ")}  ${line}`)
    .join("\n");
}

/** Same cite-toast behavior as CodeBlock.astro's copy/download handlers. */
function citeNotice(source: string): void {
  if (typeof window.showCiteToast !== "function") return;
  if (source && source.startsWith("http")) {
    window.showCiteToast("Please cite the source when using this circuit:", source);
  } else if (source) {
    window.showCiteToast("Please cite the source when using this circuit: " + source);
  } else {
    window.showCiteToast(
      "Please check and cite the corresponding source when using this circuit.",
    );
  }
}

function buildSwitcher(
  container: HTMLElement,
  template: HTMLTemplateElement,
  bodies: BodyEntry[],
): void {
  const fragment = template.content.cloneNode(true) as DocumentFragment;
  const switcher = fragment.querySelector<HTMLElement>(".format-switcher");
  const tabBar = switcher?.querySelector<HTMLElement>(".format-tabs");
  const tabProto = tabBar?.querySelector<HTMLElement>(".format-tab");
  const bodyProto = switcher?.querySelector<HTMLElement>(".format-body");
  if (!switcher || !tabBar || !tabProto || !bodyProto) return;
  tabProto.remove();
  bodyProto.remove();

  const stimFilename = container.dataset.stimFilename ?? "";
  const source = container.dataset.source ?? "";

  bodies.forEach(function (entry, i) {
    const raw = entry.body.trimEnd();

    const tab = tabProto.cloneNode(true) as HTMLElement;
    tab.className = `${TAB_BASE_CLASS} ${i === 0 ? TAB_ACTIVE_CLASS : TAB_INACTIVE_CLASS}`;
    tab.dataset.format = entry.format;
    tab.title = `Switch to ${entry.format.toUpperCase()} (${i + 1})`;
    const tabLabel = tab.querySelector<HTMLElement>(".tab-label");
    if (tabLabel) tabLabel.textContent = entry.format.toUpperCase();
    const kbd = tab.querySelector<HTMLElement>("kbd");
    if (kbd) {
      if (i < 3) kbd.textContent = String(i + 1);
      else kbd.remove();
    }
    tabBar.appendChild(tab);

    const bodyEl = bodyProto.cloneNode(true) as HTMLElement;
    bodyEl.dataset.format = entry.format;
    if (i !== 0) bodyEl.style.display = "none";
    const blockLabel = bodyEl.querySelector<HTMLElement>(".block-label");
    if (blockLabel) blockLabel.textContent = `${entry.format.toUpperCase()} Circuit`;
    const codeEl = bodyEl.querySelector<HTMLElement>("pre code");
    if (codeEl) codeEl.textContent = lineNumbered(entry.body);

    const downloadBtn = bodyEl.querySelector<HTMLElement>(".download-btn");
    if (downloadBtn) {
      const downloadName = stimFilename
        ? stimFilename.replace(/\.stim$/, `.${entry.format}`)
        : "";
      if (downloadName) {
        downloadBtn.title = `Download ${downloadName} (d)`;
        downloadBtn.addEventListener("click", function () {
          const blob = new Blob([raw], { type: "text/plain" });
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = downloadName;
          a.click();
          URL.revokeObjectURL(url);
          citeNotice(source);
        });
      } else {
        downloadBtn.remove();
      }
    }

    const copyBtn = bodyEl.querySelector<HTMLElement>(".copy-btn");
    if (copyBtn) {
      copyBtn.addEventListener("click", async function () {
        const ok = await copyToClipboard(raw);
        if (!ok) return;
        const label = copyBtn.querySelector<HTMLElement>(".copy-label");
        if (label) {
          const original = label.textContent;
          label.textContent = "Copied!";
          setTimeout(function () {
            label.textContent = original;
          }, 1500);
        }
        citeNotice(source);
      });
    }

    switcher.appendChild(bodyEl);
  });

  // Match FormatSwitcher.astro: no tab bar for single-format circuits.
  if (bodies.length < 2) tabBar.remove();

  container.replaceChildren(fragment);
  initFormatSwitchers(container);
}

/** Re-sync the expand animation height after content changes. */
function syncDetailHeight(container: HTMLElement): void {
  const detail = container.closest<HTMLElement>(".circuit-detail");
  if (detail && detail.style.maxHeight !== "0px") {
    detail.style.maxHeight = detail.scrollHeight + "px";
  }
}

async function loadBodies(
  container: HTMLElement,
  template: HTMLTemplateElement,
): Promise<void> {
  if (loaded.has(container)) return;
  loaded.add(container);
  const qecId = container.dataset.qecId;
  if (!qecId) return;
  try {
    const res = await fetch(`/api/circuits/${qecId}/bodies`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = (await res.json()) as { bodies: BodyEntry[] };
    buildSwitcher(container, template, data.bodies);
  } catch {
    loaded.delete(container); // allow a fresh expand to retry
    const status = container.querySelector<HTMLElement>(".circuit-bodies-status");
    if (status) status.textContent = "Failed to load — collapse and expand to retry.";
  }
  syncDetailHeight(container);
}

export function initCircuitBodies(): void {
  const template = document.getElementById(
    "circuit-bodies-template",
  ) as HTMLTemplateElement | null;
  if (!template) return;

  document.addEventListener("circuit-expand", function (e) {
    const detail = e.target as HTMLElement;
    const container = detail.querySelector<HTMLElement>(".circuit-bodies");
    if (container) void loadBodies(container, template);
  });
}
```

- [ ] **Step 3: Lint and typecheck**

Run: `npm run lint`
Expected: no errors. (The new module is imported by nothing yet — that's fine; Task 3 wires it.)

- [ ] **Step 4: Commit**

```bash
git add src/components/CircuitBodiesTemplate.astro src/lib/circuit-bodies-client.ts
git commit -m "feat(browse): add circuit-bodies template and lazy-load client module

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Wire up — CircuitRow placeholder, event dispatch, code page

**Files:**
- Modify: `src/components/CircuitRow.astro`
- Modify: `src/pages/codes/[code].astro`
- Modify: `src/lib/queries/circuits.ts` (remove `getCircuitsWithBodies`)
- Modify: `src/lib/queries/index.ts` (drop its export)
- Modify: `src/components/FormatSwitcher.astro`, `src/components/CodeBlock.astro` (sync comments only)

- [ ] **Step 1: CircuitRow — drop bodies, render placeholder, dispatch event**

In `src/components/CircuitRow.astro`:

1. Imports/Props: remove `CircuitBody` from the type import and remove the `FormatSwitcher` import; delete `bodies: CircuitBody[];` from `Props`; remove `bodies` from the destructuring.

```ts
import type { Circuit, Tool } from "../types";
```
```ts
interface Props {
  circuit: Circuit & { tags: string[] };
  tool?: Tool;
  codeSlug: string;
  currentUrl: URL;
}

const { circuit, tool, codeSlug, currentUrl } = Astro.props;
```

2. Replace the `<FormatSwitcher ... />` line at the bottom of the detail panel with the placeholder (filled by circuit-bodies-client.ts on first expand):

```astro
<div
  class="circuit-bodies"
  data-qec-id={anchorId}
  data-stim-filename={stimFilename}
  data-source={circuit.source}
>
  <p class="circuit-bodies-status text-sm text-gray-400">Loading circuit&hellip;</p>
</div>
```

3. In the `<script>`, in the expand branch of the toggle click handler, add the event dispatch directly after `history.replaceState(null, "", "#" + qecId);`:

```ts
          // Signal circuit-bodies-client (code pages) to lazy-load bodies.
          detail.dispatchEvent(new CustomEvent("circuit-expand", { bubbles: true }));
```

- [ ] **Step 2: Code page — drop bodiesMap, render template, init client**

In `src/pages/codes/[code].astro`:

1. Imports: replace `getCircuitsWithBodies` with `getCircuitsForCode` and `filterCircuitsForCode` in the queries import; add the template component import:

```ts
import CircuitBodiesTemplate from "../../components/CircuitBodiesTemplate.astro";
```

2. Replace the fetch line:

```ts
const { circuits, bodiesMap } = getCircuitsWithBodies(code.id, filters, sort);
```

with:

```ts
const circuits = hasFilters
  ? filterCircuitsForCode(code.id, filters, sort)
  : getCircuitsForCode(code.id, sort);
```

3. Update the row render (remove the `bodies` prop):

```astro
<CircuitRow circuit={circuit} tool={toolsMap.get(circuit.id)} codeSlug={codeSlug!} currentUrl={Astro.url} />
```

4. Render the template once, directly before `</Layout>`:

```astro
  <CircuitBodiesTemplate />
</Layout>
```

5. In the page `<script>`, add:

```ts
import { initCircuitBodies } from "../../lib/circuit-bodies-client";
```

and call `initCircuitBodies();` after `initBackKey("/");`.

- [ ] **Step 3: Remove getCircuitsWithBodies**

Verify it has no other callers: `grep -rn "getCircuitsWithBodies" src/` → only `queries/circuits.ts` and `queries/index.ts` remain. Delete the whole `getCircuitsWithBodies` function from `src/lib/queries/circuits.ts` and remove `getCircuitsWithBodies,` from `src/lib/queries/index.ts`.

- [ ] **Step 4: Sync comments in the server-rendered twins**

Top of `src/components/FormatSwitcher.astro` frontmatter, after the imports:

```ts
// KEEP THE TAB MARKUP IN SYNC with CircuitBodiesTemplate.astro, which is
// cloned client-side on code pages (this component renders only on circuit
// detail pages).
```

Top of `src/components/CodeBlock.astro` frontmatter, after the Props interface:

```ts
// KEEP THE CODE-BLOCK MARKUP IN SYNC with CircuitBodiesTemplate.astro, which
// is cloned client-side on code pages (this component renders only on
// circuit detail pages and the favorites page's export block, if any).
```

- [ ] **Step 5: Lint, format, smoke**

Run: `npm run lint && npm run format && ./scripts/smoke.sh`
Expected: lint clean, prettier may rewrite the new files (fine), smoke all `OK`.

Quick behavioral spot-check (dev server auto-reloads):

```bash
curl -s http://localhost:4321/codes/steane-code | grep -c "circuit-bodies-status"   # expect: number of circuits (213)
curl -s http://localhost:4321/codes/steane-code | grep -c "format-switcher"          # expect: 1 (the template only)
curl -s -o /dev/null -w "%{size_download}\n" http://localhost:4321/codes/flag-gadgets # expect: ~1-2 MB, was 15.2 MB
```

- [ ] **Step 6: Commit**

```bash
git add src/components/CircuitRow.astro "src/pages/codes/[code].astro" src/lib/queries/circuits.ts src/lib/queries/index.ts src/components/FormatSwitcher.astro src/components/CodeBlock.astro
git commit -m "feat(browse): lazy-load circuit bodies on code pages

Code pages no longer embed circuit bodies (all formats) in the initial
HTML; bodies are fetched from /api/circuits/[qec_id]/bodies on first row
expand. /codes/flag-gadgets drops from 15.2 MB to ~1 MB HTML.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Browser verification + production build

**Files:** none (verification only; fix-forward if a check fails)

- [ ] **Step 1: Production build**

Run: `npm run build`
Expected: build succeeds (this also rebuilds the DB first per the build script).

- [ ] **Step 2: Browser checklist on the dev server**

Use the preview browser (or a manual browser) on `http://localhost:4321`:

1. `/codes/steane-code`: click a circuit row → "Loading circuit…" flashes, then STIM body with line numbers appears; tab bar shows STIM/QASM/CIRQ where the circuit has those formats.
2. Format tabs: click QASM → body switches; press `1`/`2`/`3` → tabs switch (keyboard path).
3. Press `c` → "Copied!" label + cite toast appears; paste buffer holds the raw body (no line numbers).
4. Press `d` → file downloads with the `<code>_<circuit>_G..._2Q..._D..._Q....<format>` name; cite toast appears.
5. Collapse and re-expand the same row → instant (no second fetch; check the network panel or server log shows one `/bodies` request).
6. Hash permalink: open `/codes/steane-code#<some qec_id>` directly → row auto-expands and its body loads.
7. Single-format circuit: find one via `sqlite3 data/qecirc.db "SELECT c.qec_id, co.slug FROM circuits c JOIN codes co ON co.id=c.code_id JOIN circuit_bodies cb ON cb.circuit_id=c.id GROUP BY c.id HAVING COUNT(cb.id)=1 LIMIT 1;"` → expand it → code block renders with NO tab bar.
8. Failure path: expand a row with dev-tools offline mode (or temporarily rename the endpoint) → placeholder shows "Failed to load — collapse and expand to retry."; going back online, collapse + expand → loads.
9. `/circuits/<qec_id>` (detail page): unchanged — bodies server-rendered, copy/download work.
10. Favorites filter (Shift+F), download-all (Shift+D), sorting and tag filters on the code page: still work.

- [ ] **Step 3: Re-measure and record**

```bash
curl -s -o /dev/null -w "flag-gadgets: %{size_download} bytes\n" http://localhost:4321/codes/flag-gadgets
```

In the browser console on `/codes/flag-gadgets`:

```js
({ nodes: document.getElementsByTagName("*").length,
   interactive: Math.round(performance.getEntriesByType("navigation")[0].domInteractive) })
```

Expected: ~1–2 MB (was 15.2 MB), roughly 9k nodes (was 39,248). Record actual numbers for the PR description.

---

### Task 5: Housekeeping — changelog, version bump, docs

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `package.json`, `pyproject.toml`, `uv.lock`, `package-lock.json`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Changelog entry**

In `CHANGELOG.md` under `## Unreleased` → `### Changed`, add:

```markdown
- Code pages no longer embed circuit bodies in the initial HTML; bodies load
  on first row expand via the new `/api/circuits/[qec_id]/bodies` endpoint.
  Largest page (`/codes/flag-gadgets`) drops from ~15 MB to ~1 MB HTML.
```

- [ ] **Step 2: Version bump (patch: 0.4.6 → 0.4.7)**

- `package.json`: `"version": "0.4.7"`
- `pyproject.toml`: `version = "0.4.7"`
- Run: `UV_NO_CONFIG=1 uv lock` (never without `UV_NO_CONFIG=1` — keeps private-registry refs out)
- Run: `npm install` (syncs `package-lock.json`)

- [ ] **Step 3: Update CLAUDE.md client-side JS inventory**

In the "Rendering strategy" bullet listing client-side JS, extend with the new behavior, e.g. append `, lazy-loaded circuit bodies on code pages (fetch on first expand)` to the existing list.

- [ ] **Step 4: Final checks + commit**

Run: `npm run lint && npm run format:check && ./scripts/smoke.sh`
Expected: all clean/OK.

```bash
git add CHANGELOG.md package.json pyproject.toml uv.lock package-lock.json CLAUDE.md
git commit -m "chore(release): bump version to 0.4.7

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: PR

- [ ] **Step 1: Push and open PR**

```bash
git push -u origin feat/lazy-circuit-bodies
gh pr create --title "feat(browse): lazy-load circuit bodies on code pages" --body "$(cat <<'EOF'
## Summary
- Code pages no longer embed every circuit body (STIM/QASM/Cirq, each twice) in the initial HTML
- New `/api/circuits/[qec_id]/bodies` endpoint (mirrors `originals.ts`); bodies fetch on first row expand, following the CodeMatrices lazy-load pattern
- `/codes/flag-gadgets`: 15.2 MB → <measured> MB HTML, 39,248 → <measured> DOM nodes

## Not changed
- Circuit detail pages keep fully server-rendered bodies (SEO / SoftwareSourceCode JSON-LD)
- Download-all, favorites, sorting, filtering, keyboard shortcuts, hash permalinks

## Test plan
- `scripts/smoke.sh` extended with the new endpoint check
- Manual browser checklist: expand/format-switch/copy/download/cite-toast, keyboard `1/2/3/c/d`, hash auto-expand, single-format circuits, failure + retry path
- Design doc: `docs/superpowers/specs/2026-07-08-lazy-circuit-bodies-design.md`

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Fill in the `<measured>` numbers from Task 4 Step 3 before submitting.
