import type { CircuitSortField } from "../types";

export const CIRCUIT_SORT_FIELDS: readonly CircuitSortField[] = [
  "qubit_count",
  "depth",
  "gate_count",
  "two_qubit_gate_count",
];

export const FILTER_PART_REGEX = /^(!=|>=|<=|>|<|=)?\s*(\d+)$/;

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
