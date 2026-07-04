import { getDb } from "../db";
import type {
  Code,
  CodeDetail,
  CodeFilters,
  CodeListItem,
  CodeSort,
  CodeWithMeta,
} from "../../types";
import {
  withTags,
  withCircuitCounts,
  addConditions,
  addTagConditions,
  buildCodeOrderBy,
} from "./shared";

// Columns to select for list/search views. Excludes `h` and `logical` which
// can be multi-MB JSON blobs for large codes (e.g. [[144,12,12]] BB codes).
// Pages that need the matrices use the lazy /api/codes/[slug]/matrices
// endpoint, which is the only call site that selects h/logical.
const CODE_LIST_COLUMNS = "c.id, c.name, c.slug, c.n, c.k, c.d, c.zoo_url, c.canonical_hash";

// getCodeBySlug returns the same columns as the list views plus a
// `has_matrices` flag so the detail page knows whether to render the
// (lazy-loaded) matrices section.
const CODE_DETAIL_COLUMNS = `${CODE_LIST_COLUMNS}, (c.h IS NOT NULL AND c.logical IS NOT NULL) AS has_matrices`;

export function formatCodeParams(code: Pick<Code, "n" | "k" | "d">): string {
  return code.d != null ? `[[${code.n},${code.k},${code.d}]]` : `[[${code.n},${code.k}]]`;
}

export function getAllCodes(): CodeWithMeta[] {
  const db = getDb();
  const codes = db
    .prepare(`SELECT ${CODE_LIST_COLUMNS} FROM codes c ORDER BY c.name`)
    .all() as CodeListItem[];
  return withCircuitCounts(withTags(codes, "code"), "code_id");
}

export function getCodeBySlug(slug: string): CodeDetail | undefined {
  const db = getDb();
  return db.prepare(`SELECT ${CODE_DETAIL_COLUMNS} FROM codes c WHERE c.slug = ?`).get(slug) as
    CodeDetail | undefined;
}

export function filterCodes(filters: CodeFilters, sort?: CodeSort): CodeWithMeta[] {
  const db = getDb();
  const conditions: string[] = [];
  const params: (number | string)[] = [];

  addConditions("n", filters.n, conditions, params);
  addConditions("k", filters.k, conditions, params);
  addConditions("d", filters.d, conditions, params);
  addTagConditions(filters.tags, "code", conditions, params);

  const where = conditions.length > 0 ? `WHERE ${conditions.join(" AND ")}` : "";
  const orderBy = buildCodeOrderBy(sort);
  const codes = db
    .prepare(`SELECT ${CODE_LIST_COLUMNS} FROM codes c ${where} ${orderBy}`)
    .all(...params) as CodeListItem[];
  return withCircuitCounts(withTags(codes, "code"), "code_id");
}

export function countAllCodes(): number {
  const db = getDb();
  const row = db.prepare("SELECT COUNT(*) as count FROM codes").get() as {
    count: number;
  };
  return row.count;
}
