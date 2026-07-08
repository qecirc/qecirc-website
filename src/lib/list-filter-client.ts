// Client-side filtering and sorting for listing pages (codes index, code
// detail). Rows are server-rendered in canonical default order and carry
// their data in attributes (data-metrics, data-tags, data-name); this module
// intercepts filter inputs, sort links ([data-sort-field]) and tag links
// ([data-tag]), applies filters by toggling the Tailwind `hidden` class,
// reorders rows for sort, and keeps the URL in sync (pushState for clicks,
// replaceState while typing; popstate reapplies). The server ignores these
// params for rendering — /api/download still parses them (src/lib/url.ts).
//
// Semantics mirror the SQL layer (KEEP IN SYNC with src/lib/queries/shared.ts):
// - parseFilterString grammar (FILTER_PART_REGEX, comma = AND);
// - a NULL metric fails every condition on that field;
// - sorting places NULLs last regardless of direction, name as tiebreak
//   (plain UTF-16 comparison, approximating SQLite BINARY collation);
// - tag filters AND together (row must carry all selected tags).

import { FILTER_PART_REGEX } from "./constants";
import type { FilterCondition, FilterOp, SortDir } from "../types";

export interface ListFilterConfig {
  // Form containing the numeric inputs ([data-filter]) and status area.
  formSelector: string;
  // All URL filter fields, in canonical param order. May include fields
  // without a rendered input (e.g. `weight` on codes without weighted
  // circuits) — those still filter when present in the URL, matching the
  // previous server behavior.
  fields: string[];
  // Row root elements (carry data-metrics/data-tags/data-name).
  rowSelector: string;
  // Parent of the rows; rows are reordered inside it for sorting.
  containerSelector: string;
  basePath: string;
  // Element whose textContent shows the count; formatCount renders it.
  countSelector?: string;
  formatCount?: (visible: number, total: number, active: boolean) => string;
  // Block shown when filters hide every row.
  emptyStateSelector?: string;
  // The sort the server rendered the rows in (never null).
  defaultSort: { field: string; dir: SortDir };
}

interface RowData {
  metrics: Record<string, number | null>;
  tags: Set<string>;
  name: string;
}

interface ListState {
  raw: Record<string, string>;
  conditions: Record<string, FilterCondition[] | null>;
  tags: string[];
  sort: { field: string; dir: SortDir };
}

// ---------------------------------------------------------------------------
// Styling constants. KEEP IN SYNC with the server-rendered class lists in
// TagList.astro / TagFilterDropdowns.astro / CircuitRow.astro /
// CircuitFilter.astro / CodeFilter.astro.
// ---------------------------------------------------------------------------

const TAG_SELECTED =
  "bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-700 dark:hover:bg-gray-300";
const TAG_UNSELECTED =
  "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700";

const DROPDOWN_ENTRY_SELECTED =
  "bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-700 dark:hover:bg-gray-300";
const DROPDOWN_ENTRY_UNSELECTED =
  "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800";

const SUMMARY_SELECTED =
  "bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-700 dark:hover:bg-gray-300 font-semibold";
const SUMMARY_UNSELECTED =
  "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 font-medium";

const SORT_LABEL_ACTIVE = "text-amber-600 dark:text-amber-400 font-semibold cursor-pointer";
const SORT_LABEL_INACTIVE =
  "text-gray-600 dark:text-gray-400 font-medium hover:text-gray-900 dark:hover:text-gray-100 cursor-pointer";

// Column-header links ([data-sort-header]) only toggle the highlight classes.
const SORT_HEADER_ACTIVE = "text-amber-600 dark:text-amber-400";

const CHIP_X_ICON =
  '<svg class="w-3 h-3 opacity-70" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 18L18 6M6 6l12 12" /></svg>';

const VALID_DIRS = new Set<SortDir>(["asc", "desc"]);

/** Same grammar as queries/shared.ts parseFilterString (KEEP IN SYNC). */
function parseFilterString(input: string): FilterCondition[] | null {
  const rawInput = input.trim();
  if (!rawInput) return null;
  const parts = rawInput.split(",");
  const conditions: FilterCondition[] = [];
  for (const part of parts) {
    const trimmed = part.trim();
    if (!trimmed) continue;
    const match = trimmed.match(FILTER_PART_REGEX);
    if (!match) return null;
    const op = (match[1] || "=") as FilterOp;
    const value = parseInt(match[2], 10);
    if (!Number.isFinite(value) || value < 0) return null;
    conditions.push({ op, value });
  }
  return conditions.length > 0 ? conditions : null;
}

/** Same validity rule as the input UI used before (empty is valid). */
function isValidFilter(value: string): boolean {
  const trimmed = value.trim();
  if (trimmed === "") return true;
  const parts = trimmed.split(",").map((p) => p.trim());
  if (parts.every((p) => p === "")) return false;
  return parts.every((p) => p === "" || FILTER_PART_REGEX.test(p));
}

function condHolds(value: number, cond: FilterCondition): boolean {
  switch (cond.op) {
    case "=":
      return value === cond.value;
    case "!=":
      return value !== cond.value;
    case ">":
      return value > cond.value;
    case ">=":
      return value >= cond.value;
    case "<":
      return value < cond.value;
    case "<=":
      return value <= cond.value;
  }
}

function swapClasses(el: Element, from: string, to: string): void {
  el.classList.remove(...from.split(" "));
  el.classList.add(...to.split(" "));
}

export function initListFilter(config: ListFilterConfig): void {
  const form = document.querySelector<HTMLFormElement>(config.formSelector);
  const container = document.querySelector<HTMLElement>(config.containerSelector);
  const rows = Array.from(document.querySelectorAll<HTMLElement>(config.rowSelector));
  if (!container || rows.length === 0) return;

  // Snapshot = server-rendered default order; restored when sort is default.
  const snapshot = rows.slice();

  const rowData = new Map<HTMLElement, RowData>();
  for (const row of rows) {
    let metrics: Record<string, number | null> = {};
    let tags: string[] = [];
    try {
      metrics = JSON.parse(row.dataset.metrics ?? "{}");
      tags = JSON.parse(row.dataset.tags ?? "[]");
    } catch {
      /* malformed data attribute — row simply never matches metric filters */
    }
    rowData.set(row, { metrics, tags: new Set(tags), name: row.dataset.name ?? "" });
  }

  const inputs = form
    ? Array.from(form.querySelectorAll<HTMLInputElement>("input[data-filter]"))
    : [];
  const inputByField = new Map(inputs.map((i) => [i.name, i]));
  const errorSpan = form?.querySelector<HTMLElement>("[data-filter-error]") ?? null;
  const clearLink = document.querySelector<HTMLElement>("[data-clear-filters]");
  const countEl = config.countSelector
    ? document.querySelector<HTMLElement>(config.countSelector)
    : null;
  const emptyEl = config.emptyStateSelector
    ? document.querySelector<HTMLElement>(config.emptyStateSelector)
    : null;
  const chipsEl = document.querySelector<HTMLElement>("[data-tag-chips]");

  let state = stateFromLocation();
  let appliedSortKey = `${config.defaultSort.field}:${config.defaultSort.dir}`;

  function stateFromLocation(): ListState {
    const params = new URLSearchParams(location.search);
    const raw: Record<string, string> = {};
    const conditions: Record<string, FilterCondition[] | null> = {};
    for (const field of config.fields) {
      const value = params.get(field) ?? "";
      raw[field] = value;
      conditions[field] = value.trim() ? parseFilterString(value) : null;
    }
    const tags = params.getAll("tag");
    const rawSort = params.get("sort") ?? "";
    const rawDir = params.get("sort_dir") ?? "";
    const sort = config.fields.includes(rawSort)
      ? { field: rawSort, dir: VALID_DIRS.has(rawDir as SortDir) ? (rawDir as SortDir) : "asc" }
      : { ...config.defaultSort };
    return { raw, conditions, tags, sort };
  }

  function urlFromState(): string {
    const params = new URLSearchParams();
    for (const field of config.fields) {
      const value = state.raw[field]?.trim();
      if (value) params.set(field, value);
    }
    for (const tag of state.tags) params.append("tag", tag);
    if (
      state.sort.field !== config.defaultSort.field ||
      state.sort.dir !== config.defaultSort.dir
    ) {
      params.set("sort", state.sort.field);
      params.set("sort_dir", state.sort.dir);
    }
    const qs = params.toString();
    return config.basePath + (qs ? "?" + qs : "");
  }

  function syncUrl(mode: "push" | "replace"): void {
    const target = urlFromState();
    const current = location.pathname + location.search;
    if (target === current) return;
    if (mode === "push") history.pushState(null, "", target);
    else history.replaceState(null, "", target);
  }

  function hasActiveFilters(): boolean {
    return (
      state.tags.length > 0 || config.fields.some((f) => (state.conditions[f]?.length ?? 0) > 0)
    );
  }

  function rowMatches(data: RowData): boolean {
    for (const field of config.fields) {
      const conds = state.conditions[field];
      if (!conds || conds.length === 0) continue;
      const value = data.metrics[field];
      if (value == null) return false; // SQL parity: NULL fails every condition
      for (const cond of conds) if (!condHolds(value, cond)) return false;
    }
    for (const tag of state.tags) if (!data.tags.has(tag)) return false;
    return true;
  }

  function comparator(field: string, dir: SortDir) {
    const sign = dir === "desc" ? -1 : 1;
    return (a: HTMLElement, b: HTMLElement): number => {
      const da = rowData.get(a)!;
      const db = rowData.get(b)!;
      const va = da.metrics[field];
      const vb = db.metrics[field];
      if (va == null && vb == null) return da.name < db.name ? -1 : da.name > db.name ? 1 : 0;
      if (va == null) return 1; // NULLs last regardless of direction
      if (vb == null) return -1;
      if (va !== vb) return (va - vb) * sign;
      return da.name < db.name ? -1 : da.name > db.name ? 1 : 0;
    };
  }

  function apply(): void {
    let visible = 0;
    for (const row of rows) {
      const ok = rowMatches(rowData.get(row)!);
      row.classList.toggle("hidden", !ok);
      if (ok) visible++;
    }

    const sortKey = `${state.sort.field}:${state.sort.dir}`;
    if (sortKey !== appliedSortKey) {
      const ordered =
        state.sort.field === config.defaultSort.field && state.sort.dir === config.defaultSort.dir
          ? snapshot
          : snapshot.slice().sort(comparator(state.sort.field, state.sort.dir));
      container!.append(...ordered);
      appliedSortKey = sortKey;
    }

    const active = hasActiveFilters();
    if (countEl && config.formatCount) {
      countEl.textContent = config.formatCount(visible, rows.length, active);
    }
    if (emptyEl) emptyEl.classList.toggle("hidden", visible > 0);
    if (clearLink) clearLink.classList.toggle("hidden", !active);
  }

  // -------------------------------------------------------------------------
  // Control styling
  // -------------------------------------------------------------------------

  function updateSortIndicators(): void {
    for (const link of document.querySelectorAll<HTMLElement>("[data-sort-field]")) {
      const field = link.dataset.sortField!;
      const isActive = state.sort.field === field;
      const arrow = link.querySelector<HTMLElement>("[data-sort-arrow]");
      if (arrow) arrow.textContent = isActive ? (state.sort.dir === "desc" ? "▼" : "▲") : "";
      if (link.hasAttribute("data-sort-header")) {
        for (const cls of SORT_HEADER_ACTIVE.split(" ")) link.classList.toggle(cls, isActive);
      } else {
        swapClasses(
          link,
          isActive ? SORT_LABEL_INACTIVE : SORT_LABEL_ACTIVE,
          isActive ? SORT_LABEL_ACTIVE : SORT_LABEL_INACTIVE,
        );
      }
    }
  }

  function renderChips(): void {
    if (!chipsEl) return;
    chipsEl.replaceChildren();
    for (const tag of state.tags) {
      const a = document.createElement("a");
      a.href = `${config.basePath}?tag=${encodeURIComponent(tag)}`;
      a.dataset.tag = tag;
      a.title = `Remove tag filter "${tag}"`;
      a.className = `inline-flex items-center gap-1 rounded px-2 py-0.5 text-xs transition-colors ${TAG_SELECTED}`;
      a.textContent = tag;
      a.insertAdjacentHTML("beforeend", CHIP_X_ICON);
      chipsEl.append(a);
    }
  }

  function updateTagStyling(): void {
    const selected = new Set(state.tags);
    for (const link of document.querySelectorAll<HTMLElement>("[data-tag]")) {
      if (chipsEl && chipsEl.contains(link)) continue; // chips are re-rendered
      const isSelected = selected.has(link.dataset.tag ?? "");
      const inDropdown = link.closest("[data-tag-popover]") !== null;
      const sel = inDropdown ? DROPDOWN_ENTRY_SELECTED : TAG_SELECTED;
      const unsel = inDropdown ? DROPDOWN_ENTRY_UNSELECTED : TAG_UNSELECTED;
      swapClasses(link, isSelected ? unsel : sel, isSelected ? sel : unsel);
    }
    // Dropdown summaries: selected-count badge + emphasis.
    for (const dropdown of document.querySelectorAll<HTMLElement>("[data-tag-dropdown]")) {
      const tagsInGroup = Array.from(
        dropdown.querySelectorAll<HTMLElement>("[data-tag-popover] [data-tag]"),
      ).map((l) => l.dataset.tag ?? "");
      const n = tagsInGroup.filter((t) => selected.has(t)).length;
      const summary = dropdown.querySelector<HTMLElement>("summary");
      const countSpan = summary?.querySelector<HTMLElement>("[data-summary-count]");
      if (countSpan) countSpan.textContent = n > 0 ? `(${n})` : "";
      if (summary) {
        swapClasses(
          summary,
          n > 0 ? SUMMARY_UNSELECTED : SUMMARY_SELECTED,
          n > 0 ? SUMMARY_SELECTED : SUMMARY_UNSELECTED,
        );
      }
    }
    renderChips();
  }

  // -------------------------------------------------------------------------
  // Input validation UI (same behavior as the previous filter-client.ts)
  // -------------------------------------------------------------------------

  function validateInputs(): boolean {
    let hasError = false;
    for (const input of inputs) {
      const invalid = !isValidFilter(input.value);
      if (invalid) hasError = true;
      input.classList.toggle("ring-1", invalid);
      input.classList.toggle("ring-red-300", invalid);
    }
    if (errorSpan) errorSpan.classList.toggle("hidden", !hasError);
    // The clear link shares the status area: an error message displaces it.
    if (clearLink) clearLink.classList.toggle("hidden", hasError || !hasActiveFilters());
    return !hasError;
  }

  function syncInputsFromState(): void {
    for (const field of config.fields) {
      const input = inputByField.get(field);
      if (input) input.value = state.raw[field] ?? "";
    }
    validateInputs();
  }

  function readInputsIntoState(): void {
    for (const input of inputs) {
      state.raw[input.name] = input.value;
      const trimmed = input.value.trim();
      state.conditions[input.name] = trimmed ? parseFilterString(trimmed) : null;
    }
  }

  // -------------------------------------------------------------------------
  // Events
  // -------------------------------------------------------------------------

  let debounceTimer: ReturnType<typeof setTimeout>;

  if (form) {
    form.addEventListener("input", () => {
      clearTimeout(debounceTimer);
      const valid = validateInputs();
      debounceTimer = setTimeout(() => {
        if (!valid) return;
        readInputsIntoState();
        apply();
        syncUrl("replace");
      }, 200);
    });
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      clearTimeout(debounceTimer);
      if (!validateInputs()) return;
      readInputsIntoState();
      apply();
      syncUrl("replace");
    });
  }

  document.addEventListener("click", (e) => {
    if (e.defaultPrevented) return;
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const target = e.target as HTMLElement;

    const tagLink = target.closest<HTMLElement>("[data-tag]");
    if (tagLink && tagLink.dataset.tag) {
      e.preventDefault();
      const tag = tagLink.dataset.tag;
      state.tags = state.tags.includes(tag)
        ? state.tags.filter((t) => t !== tag)
        : [...state.tags, tag];
      apply();
      updateTagStyling();
      syncUrl("push");
      return;
    }

    const sortLink = target.closest<HTMLElement>("[data-sort-field]");
    if (sortLink && sortLink.dataset.sortField) {
      e.preventDefault();
      const field = sortLink.dataset.sortField;
      state.sort =
        state.sort.field === field
          ? { field, dir: state.sort.dir === "asc" ? "desc" : "asc" }
          : { field, dir: "asc" };
      apply();
      updateSortIndicators();
      syncUrl("push");
      return;
    }

    const clear = target.closest<HTMLElement>("[data-clear-filters]");
    if (clear) {
      e.preventDefault();
      for (const field of config.fields) {
        state.raw[field] = "";
        state.conditions[field] = null;
      }
      state.tags = [];
      state.sort = { ...config.defaultSort };
      syncInputsFromState();
      apply();
      updateSortIndicators();
      updateTagStyling();
      syncUrl("push");
    }
  });

  window.addEventListener("popstate", () => {
    state = stateFromLocation();
    syncInputsFromState();
    apply();
    updateSortIndicators();
    updateTagStyling();
  });

  // -------------------------------------------------------------------------
  // Init: apply any deep-linked URL state (no-op styling when default).
  // -------------------------------------------------------------------------

  syncInputsFromState();
  apply();
  updateSortIndicators();
  updateTagStyling();
}
