import type {
  CircuitFilters,
  CircuitSort,
  CircuitSortField,
  CodeFilters,
  CodeSort,
  CodeSortField,
  FilterCondition,
  SortDir,
} from "../types";
import { CIRCUIT_SORT_FIELDS, CODE_SORT_FIELDS } from "./constants";
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

/**
 * Build the URL that toggles or activates a sort by `field`. Clicking again
 * with the same active field flips dir; otherwise activates with `desc`.
 */
export function circuitSortToggleUrl(
  currentUrl: URL,
  sort: CircuitSort,
  field: CircuitSortField,
  basePath: string,
): string {
  const params = new URLSearchParams(currentUrl.search);
  params.delete("focus");
  params.set("sort", field);
  if (sort.field === field) {
    params.set("sort_dir", sort.dir === "desc" ? "asc" : "desc");
  } else {
    params.set("sort_dir", "desc");
  }
  const qs = params.toString();
  return basePath + (qs ? "?" + qs : "");
}

const CODE_FILTER_FIELDS = ["n", "k", "d"] as const;

/** Parse code filters and sort params from a URL. */
export function parseCodeParams(
  url: URL,
): { filters: CodeFilters; sort: CodeSort } & ReturnType<
  typeof parseFilterParams<(typeof CODE_FILTER_FIELDS)[number]>
> {
  const result = parseFilterParams(url, CODE_FILTER_FIELDS);

  const rawSort = url.searchParams.get("sort") ?? "";
  const rawSortDir = url.searchParams.get("sort_dir") ?? "";
  const sort: CodeSort = CODE_SORT_FIELDS.includes(rawSort as CodeSortField)
    ? {
        field: rawSort as CodeSortField,
        dir: VALID_SORT_DIRS.has(rawSortDir as SortDir) ? (rawSortDir as SortDir) : "asc",
      }
    : { field: "n", dir: "asc" };

  const filters: CodeFilters = {
    ...result.parsed,
    tags: result.tags.length > 0 ? result.tags : undefined,
  };

  return { ...result, filters, sort };
}

/**
 * Build the URL that toggles or activates a code sort by `field`. Clicking again
 * with the same active field flips dir; otherwise activates with `asc` (the
 * natural default for n/k/d).
 */
export function codeSortToggleUrl(
  currentUrl: URL,
  sort: CodeSort,
  field: CodeSortField,
  basePath: string,
): string {
  const params = new URLSearchParams(currentUrl.search);
  params.delete("focus");
  params.set("sort", field);
  if (sort.field === field) {
    params.set("sort_dir", sort.dir === "asc" ? "desc" : "asc");
  } else {
    params.set("sort_dir", "asc");
  }
  const qs = params.toString();
  return basePath + (qs ? "?" + qs : "");
}
