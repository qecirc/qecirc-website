export interface Code {
  id: number;
  name: string;
  slug: string;
  n: number;
  k: number;
  d: number | null;
  zoo_url: string | null;
  h: string | null;
  logical: string | null;
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
  original_h: string | null;
  original_logical: string | null;
}

export interface Tool {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  homepage_url: string | null;
  github_url: string | null;
  paper_urls: string[] | null;
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

export type CircuitSortField = "qubit_count" | "depth" | "gate_count" | "two_qubit_gate_count";
export type SortDir = "asc" | "desc";

export interface CircuitSort {
  field: CircuitSortField;
  dir: SortDir;
}

export type CodeSortField = "n" | "k" | "d";

export interface CodeSort {
  field: CodeSortField;
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

/**
 * Narrower view of Code without the large `h` / `logical` JSON columns.
 * Use this for list and search results — anything that does not render the
 * stabilizer / logical matrices. The detail page (`getCodeBySlug`) returns
 * `CodeDetail` (same shape plus a `has_matrices` flag); the matrices
 * themselves are fetched lazily from `/api/codes/[slug]/matrices`.
 */
export type CodeListItem = Omit<Code, "h" | "logical">;

/**
 * Shape returned by `getCodeBySlug`. Same as `CodeListItem` plus a boolean
 * (better-sqlite3 returns SQLite booleans as 0 or 1) indicating whether the
 * code has stabilizer / logical matrices available for lazy loading.
 */
export type CodeDetail = CodeListItem & { has_matrices: 0 | 1 };

export type CodeWithMeta = CodeListItem & { tags: string[]; circuit_count: number };
export type ToolWithMeta = Tool & { tags: string[]; circuit_count: number };

/**
 * Narrower view of CircuitOriginal without the large `original_h` /
 * `original_logical` JSON columns. The matrices themselves are fetched
 * lazily from `/api/circuits/[qec_id]/originals`.
 */
export type CircuitOriginalLight = Pick<CircuitOriginal, "original_stim"> & {
  has_original_matrices: 0 | 1;
};
