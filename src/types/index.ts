export interface Code {
  id: number;
  name: string;
  slug: string;
  n: number;
  k: number;
  d: number | null;
  zoo_url: string | null;
  hx: string | null;
  hz: string | null;
  logical_x: string | null;
  logical_z: string | null;
  canonical_hash: string | null;
}

export interface Circuit {
  id: number;
  qec_id: number;
  code_id: number;
  name: string;
  slug: string;
  notes: string | null;
  source: string;
  gate_count: number | null;
  two_qubit_gate_count: number | null;
  depth: number | null;
  qubit_count: number | null;
  crumble_url: string | null;
  quirk_url: string | null;
  tool_id: number | null;
}

export interface CircuitBody {
  format: string;
  body: string;
}

export interface CircuitOriginal {
  original_stim: string;
  original_hx: string;
  original_hz: string;
  original_logical_x: string;
  original_logical_z: string;
}

export interface Tool {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  homepage_url: string | null;
  github_url: string | null;
}

export interface ToolFilters {
  tags?: string[];
}

export type TaggableType = "code" | "circuit" | "tool";

export type FilterOp = "=" | "!=" | ">" | ">=" | "<" | "<=";

export interface FilterCondition {
  op: FilterOp;
  value: number;
}

export interface CodeFilters {
  n?: FilterCondition[];
  k?: FilterCondition[];
  d?: FilterCondition[];
  tags?: string[];
}

export type CircuitSortField =
  | "qubit_count"
  | "depth"
  | "gate_count"
  | "two_qubit_gate_count";
export type SortDir = "asc" | "desc";

export interface CircuitSort {
  field: CircuitSortField;
  dir: SortDir;
}

export interface CircuitFilters {
  gate_count?: FilterCondition[];
  two_qubit_gate_count?: FilterCondition[];
  depth?: FilterCondition[];
  qubit_count?: FilterCondition[];
  tags?: string[];
}

export interface TagWithCount {
  name: string;
  count: number;
}

export type CodeWithMeta = Code & { tags: string[]; circuit_count: number };
export type ToolWithMeta = Tool & { tags: string[]; circuit_count: number };
