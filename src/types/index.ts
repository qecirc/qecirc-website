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
  weight: number | null;
  crumble_url: string | null;
  /** Crumble link for the `stim-annotated` body. The Detectors switch points the
   *  Crumble link here; null when the circuit has no annotated body. */
  crumble_url_annotated: string | null;
  quirk_url: string | null;
  tool_id: number | null;
  /** The paper this circuit is taken from, resolved from `source` at build time
   *  (scripts/db/create_database.mjs). Null when the source names a tool rather
   *  than a paper, or cites a work data_yaml/papers/ has no record of. */
  paper_id: number | null;
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

/** A published work a circuit is taken from. Its text is what makes a circuit
 *  findable by title, author or arXiv id — `circuits.source` holds only a link. */
export interface Paper {
  id: number;
  slug: string;
  title: string;
  /** In author order — the citation renders "<first author> et al." */
  authors: string[];
  year: number | null;
  /** Bare id, no "arXiv:" prefix or version suffix. */
  arxiv_id: string | null;
  doi: string | null;
  journal_ref: string | null;
  url: string;
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

export type CircuitSortField =
  "qubit_count" | "depth" | "gate_count" | "two_qubit_gate_count" | "weight";
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
  weight?: FilterCondition[];
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
