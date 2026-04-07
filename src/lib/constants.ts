import type { CircuitSortField } from "../types";

export const CIRCUIT_SORT_FIELDS: readonly CircuitSortField[] = [
  "qubit_count",
  "depth",
  "gate_count",
  "two_qubit_gate_count",
];

export const FILTER_PART_REGEX = /^(!=|>=|<=|>|<|=)?\s*(\d+)$/;
