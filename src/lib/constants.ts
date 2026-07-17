import type { CircuitSortField, CodeSortField } from "../types";

export const CIRCUIT_SORT_FIELDS: readonly CircuitSortField[] = [
  "qubit_count",
  "depth",
  "gate_count",
  "two_qubit_gate_count",
  "weight",
];

export const CODE_SORT_FIELDS: readonly CodeSortField[] = ["n", "k", "d"];

export const FILTER_PART_REGEX = /^(!=|>=|<=|>|<|=)?\s*(\d+)$/;

// Codes carrying this tag are hidden by default: excluded from the /codes
// listing (until the tag is explicitly selected in the filter) and from every
// displayed code/circuit count. They stay fully searchable and their detail
// pages stay reachable — hiding governs discovery surfaces, not existence.
// Applied to the codetables.de best-known-distance sweep (mostly anonymous
// record-holder codes) so it doesn't drown the curated library.
export const HIDDEN_CODE_TAG = "codetables";

// Shared tab-toggle styling (FormatSwitcher, CodeMatrices). Compose with any
// component-specific base classes (e.g. `format-tab`, `code-matrix-toggle`,
// focus rings) at the call site.
export const TAB_ACTIVE_CLASS =
  "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 ring-1 ring-inset ring-gray-200 dark:ring-gray-700";
export const TAB_INACTIVE_CLASS =
  "text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100";

// Tag styling shared by the client-side filter (list-filter-client.ts, which
// swaps these at runtime) and the server-rendered markup (TagList.astro,
// TagFilterDropdowns.astro). Defined once here because /search renders the
// selected state on the server while /codes leaves it to the client -- the two
// must agree, and they previously only agreed by a comment asking them to.
export const TAG_SELECTED =
  "bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-700 dark:hover:bg-gray-300";
export const TAG_UNSELECTED =
  "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700";

export const DROPDOWN_ENTRY_SELECTED = TAG_SELECTED;
export const DROPDOWN_ENTRY_UNSELECTED =
  "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800";

export const SUMMARY_SELECTED = `${TAG_SELECTED} font-semibold`;
export const SUMMARY_UNSELECTED = `${TAG_UNSELECTED} font-medium`;

export const HEART_PATH =
  "M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z";
