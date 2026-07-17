import { getDb } from "../db";
import { HIDDEN_CODE_TAG } from "../constants";
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
  // A placeholder collector (e.g. the flag-gadget bucket) carries n = 0 and has
  // no meaningful [[n,k,d]] parameters — render nothing rather than "[[0,0]]".
  if (code.n === 0) return "";
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

// Codes tagged HIDDEN_CODE_TAG (and their circuits) are left out of every
// displayed count and of the homepage discovery surfaces — they are a
// reference shelf, not part of the curated library the numbers advertise.
// `codesAlias` is the codes table's alias in the calling query; the caller
// must bind HIDDEN_CODE_TAG for the `?`.
export function visibleCodePredicate(codesAlias = "c"): string {
  return `NOT EXISTS (
    SELECT 1 FROM taggings tg JOIN tags t ON t.id = tg.tag_id
    WHERE tg.taggable_id = ${codesAlias}.id AND tg.taggable_type = 'code' AND t.name = ?
  )`;
}

export function countAllCodes(): number {
  const db = getDb();
  const row = db
    .prepare(`SELECT COUNT(*) as count FROM codes c WHERE ${visibleCodePredicate()}`)
    .get(HIDDEN_CODE_TAG) as { count: number };
  return row.count;
}
