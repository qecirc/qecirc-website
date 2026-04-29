import type { CircuitSortField } from "../types";

export const CIRCUIT_SORT_FIELDS: readonly CircuitSortField[] = [
  "qubit_count",
  "depth",
  "gate_count",
  "two_qubit_gate_count",
];

export const FILTER_PART_REGEX = /^(!=|>=|<=|>|<|=)?\s*(\d+)$/;

// Shared tab-toggle styling (FormatSwitcher, CodeMatrices). Compose with any
// component-specific base classes (e.g. `format-tab`, `code-matrix-toggle`,
// focus rings) at the call site.
export const TAB_ACTIVE_CLASS =
  "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 ring-1 ring-inset ring-gray-200 dark:ring-gray-700";
export const TAB_INACTIVE_CLASS =
  "text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100";

export const HEART_PATH =
  "M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z";
