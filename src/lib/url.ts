import type {
  CircuitFilters,
  CircuitSort,
  CircuitSortField,
  FilterCondition,
  SortDir,
} from "../types";
import { CIRCUIT_SORT_FIELDS } from "./constants";
import { parseFilterString } from "./queries";

/**
 * Parse numeric filter params and tags from a URL.
 * Returns raw strings (for repopulating inputs), parsed conditions,
 * per-field error flags, selected tags, and the validated focus field.
 */
export function parseFilterParams<F extends string>(
  url: URL,
  fields: readonly F[],
): {
  raw: Record<F, string>;
  parsed: Partial<Record<F, FilterCondition[]>>;
  errors: Record<F, boolean>;
  tags: string[];
  focus: string;
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

  const validFocus = new Set<string>([...fields, ""]);
  const rawFocus = url.searchParams.get("focus") ?? "";
  const focus = validFocus.has(rawFocus) ? rawFocus : "";

  return { raw, parsed, errors, tags, focus };
}

const CIRCUIT_FILTER_FIELDS = [
  "gate_count",
  "two_qubit_gate_count",
  "depth",
  "qubit_count",
] as const;
const VALID_SORT_DIRS = new Set<SortDir>(["asc", "desc"]);

/** Parse circuit filters and sort params from a URL. */
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
        dir: VALID_SORT_DIRS.has(rawSortDir as SortDir) ? (rawSortDir as SortDir) : "desc",
      }
    : { field: "gate_count", dir: "desc" };

  const filters: CircuitFilters = {
    ...result.parsed,
    tags: result.tags.length > 0 ? result.tags : undefined,
  };

  return { ...result, filters, sort };
}

/**
 * Build a URL that toggles a tag in/out of the current selection.
 * Clears the `focus` param so the page doesn't re-focus a filter input.
 */
export function tagToggleUrl(
  currentSearch: string,
  selectedTags: string[],
  tagName: string,
  basePath: string,
): string {
  const params = new URLSearchParams(currentSearch);
  params.delete("tag");
  params.delete("focus");
  const newTags = selectedTags.includes(tagName)
    ? selectedTags.filter((t) => t !== tagName)
    : [...selectedTags, tagName];
  for (const t of newTags) params.append("tag", t);
  const qs = params.toString();
  return basePath + (qs ? "?" + qs : "");
}
