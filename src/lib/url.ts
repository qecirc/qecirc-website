import type {
  CircuitFilters,
  CircuitSort,
  CircuitSortField,
  FilterCondition,
  SortDir,
} from "../types";
import { CIRCUIT_SORT_FIELDS } from "./constants";
import { parseFilterString } from "./queries";

// NOTE: listing pages filter/sort client-side (src/lib/list-filter-client.ts,
// which mirrors these semantics — KEEP IN SYNC). The parsers below remain for
// /api/download, which still reads the same URL params server-side.

/**
 * Parse numeric filter params and tags from a URL.
 * Returns raw strings, parsed conditions, per-field error flags and tags.
 */
export function parseFilterParams<F extends string>(
  url: URL,
  fields: readonly F[],
): {
  raw: Record<F, string>;
  parsed: Partial<Record<F, FilterCondition[]>>;
  errors: Record<F, boolean>;
  tags: string[];
} {
  const raw = {} as Record<F, string>;
  const parsed = {} as Partial<Record<F, FilterCondition[]>>;
  const errors = {} as Record<F, boolean>;

  for (const field of fields) {
    const value = url.searchParams.get(field) ?? "";
    raw[field] = value;
    const result = value.trim() ? parseFilterString(value) : undefined;
    parsed[field] = result ?? undefined;
    errors[field] = value.trim() !== "" && result === null;
  }

  const tags = url.searchParams.getAll("tag");

  return { raw, parsed, errors, tags };
}

const CIRCUIT_FILTER_FIELDS = [
  "gate_count",
  "two_qubit_gate_count",
  "depth",
  "qubit_count",
  "weight",
] as const;
const VALID_SORT_DIRS = new Set<SortDir>(["asc", "desc"]);

/** Parse circuit filters and sort params from a URL (used by /api/download). */
export function parseCircuitParams(
  url: URL,
): { filters: CircuitFilters; sort: CircuitSort } & ReturnType<
  typeof parseFilterParams<(typeof CIRCUIT_FILTER_FIELDS)[number]>
> {
  const result = parseFilterParams(url, CIRCUIT_FILTER_FIELDS);

  const rawSort = url.searchParams.get("sort") ?? "";
  const rawSortDir = url.searchParams.get("sort_dir") ?? "";
  const sort: CircuitSort = CIRCUIT_SORT_FIELDS.includes(rawSort as CircuitSortField)
    ? {
        field: rawSort as CircuitSortField,
        dir: VALID_SORT_DIRS.has(rawSortDir as SortDir) ? (rawSortDir as SortDir) : "asc",
      }
    : { field: "two_qubit_gate_count", dir: "asc" };

  const filters: CircuitFilters = {
    ...result.parsed,
    tags: result.tags.length > 0 ? result.tags : undefined,
  };

  return { ...result, filters, sort };
}

/**
 * Build a URL that toggles a tag in/out of the current selection.
 * Used by TagList on server-filtered pages (currently /tools).
 */
export function tagToggleUrl(
  currentSearch: string,
  selectedTags: string[],
  tagName: string,
  basePath: string,
): string {
  const params = new URLSearchParams(currentSearch);
  params.delete("tag");
  const newTags = selectedTags.includes(tagName)
    ? selectedTags.filter((t) => t !== tagName)
    : [...selectedTags, tagName];
  for (const t of newTags) params.append("tag", t);
  const qs = params.toString();
  return basePath + (qs ? "?" + qs : "");
}
