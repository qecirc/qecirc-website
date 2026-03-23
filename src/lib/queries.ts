import { getDb } from "./db";

export interface Code {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  n: number;
  k: number;
  d: number | null;
}

export interface Functionality {
  id: number;
  code_id: number;
  name: string;
  slug: string;
  description: string | null;
}

export interface Circuit {
  id: number;
  functionality_id: number;
  name: string;
  slug: string;
  source: string;
  format: string;
  body: string;
}

export type TaggableType = "code" | "functionality" | "circuit";

export function formatCodeParams(code: Code): string {
  return code.d != null ? `[[${code.n},${code.k},${code.d}]]` : `[[${code.n},${code.k}]]`;
}

export function getTagsFor(
  taggableType: TaggableType,
  taggableId: number,
): string[] {
  const db = getDb();
  const rows = db
    .prepare(
      `SELECT t.name FROM tags t
       JOIN taggings tg ON t.id = tg.tag_id
       WHERE tg.taggable_type = ? AND tg.taggable_id = ?
       ORDER BY t.name`,
    )
    .all(taggableType, taggableId) as { name: string }[];
  return rows.map((r) => r.name);
}

export function getAllCodes(): (Code & { tags: string[] })[] {
  const db = getDb();
  const codes = db
    .prepare("SELECT * FROM codes ORDER BY name")
    .all() as Code[];
  return codes.map((c) => ({ ...c, tags: getTagsFor("code", c.id) }));
}

export function getCodeBySlug(slug: string): Code | undefined {
  const db = getDb();
  return db
    .prepare("SELECT * FROM codes WHERE slug = ?")
    .get(slug) as Code | undefined;
}

export function getFunctionalitiesForCode(
  codeId: number,
): (Functionality & { tags: string[] })[] {
  const db = getDb();
  const rows = db
    .prepare("SELECT * FROM functionalities WHERE code_id = ? ORDER BY name")
    .all(codeId) as Functionality[];
  return rows.map((f) => ({ ...f, tags: getTagsFor("functionality", f.id) }));
}

export function getFunctionalityBySlug(
  codeId: number,
  slug: string,
): Functionality | undefined {
  const db = getDb();
  return db
    .prepare("SELECT * FROM functionalities WHERE code_id = ? AND slug = ?")
    .get(codeId, slug) as Functionality | undefined;
}

export function getCircuitsForFunctionality(
  functionalityId: number,
): (Circuit & { tags: string[] })[] {
  const db = getDb();
  const rows = db
    .prepare(
      "SELECT * FROM circuits WHERE functionality_id = ? ORDER BY name",
    )
    .all(functionalityId) as Circuit[];
  return rows.map((c) => ({ ...c, tags: getTagsFor("circuit", c.id) }));
}

type FilterOp = "=" | "!=" | ">" | ">=" | "<" | "<=";

export interface FilterCondition {
  op: FilterOp;
  value: number;
}

export interface CodeFilters {
  n?: FilterCondition[];
  k?: FilterCondition[];
  d?: FilterCondition[];
}

const VALID_OPS: FilterOp[] = ["=", "!=", ">=", ">", "<=", "<"];

/** Parse a filter string like "7", ">3,<10", "!=1" into conditions. */
export function parseFilterString(input: string): FilterCondition[] | null {
  const raw = input.trim();
  if (!raw) return null;

  const parts = raw.split(",");
  const conditions: FilterCondition[] = [];

  for (const part of parts) {
    const trimmed = part.trim();
    if (!trimmed) continue;

    const match = trimmed.match(/^(!=|>=|<=|>|<|=)?\s*(\d+)$/);
    if (!match) return null;

    const op = (match[1] || "=") as FilterOp;
    const value = parseInt(match[2], 10);
    if (!Number.isFinite(value) || value < 0) return null;

    conditions.push({ op, value });
  }

  return conditions.length > 0 ? conditions : null;
}

export function hasActiveFilters(filters: CodeFilters): boolean {
  return (filters.n?.length ?? 0) > 0
    || (filters.k?.length ?? 0) > 0
    || (filters.d?.length ?? 0) > 0;
}

export function filterCodes(filters: CodeFilters): (Code & { tags: string[] })[] {
  const db = getDb();
  const conditions: string[] = [];
  const params: number[] = [];

  function addConditions(column: string, filter?: FilterCondition[]) {
    if (!filter) return;
    for (const { op, value } of filter) {
      if (!(VALID_OPS as readonly string[]).includes(op)) continue;
      conditions.push(`c.${column} ${op} ?`);
      params.push(value);
    }
  }

  addConditions("n", filters.n);
  addConditions("k", filters.k);
  addConditions("d", filters.d);

  const where = conditions.length > 0 ? `WHERE ${conditions.join(" AND ")}` : "";
  const codes = db
    .prepare(`SELECT * FROM codes c ${where} ORDER BY c.name`)
    .all(...params) as Code[];
  return codes.map((c) => ({ ...c, tags: getTagsFor("code", c.id) }));
}

export function countAllCodes(): number {
  const db = getDb();
  const row = db.prepare("SELECT COUNT(*) as count FROM codes").get() as { count: number };
  return row.count;
}

export function searchCodes(query: string): (Code & { tags: string[] })[] {
  const db = getDb();
  const escaped = query.replace(/[%_\\]/g, "\\$&");
  const pattern = `%${escaped}%`;
  const codes = db
    .prepare(
      `SELECT DISTINCT c.* FROM codes c
       LEFT JOIN taggings tg ON tg.taggable_id = c.id AND tg.taggable_type = 'code'
       LEFT JOIN tags t ON t.id = tg.tag_id
       WHERE c.name LIKE ? ESCAPE '\\' OR t.name LIKE ? ESCAPE '\\'
       ORDER BY c.name
       LIMIT 20`,
    )
    .all(pattern, pattern) as Code[];
  return codes.map((c) => ({ ...c, tags: getTagsFor("code", c.id) }));
}

export function getCircuitBySlug(
  functionalityId: number,
  slug: string,
): Circuit | undefined {
  const db = getDb();
  return db
    .prepare(
      "SELECT * FROM circuits WHERE functionality_id = ? AND slug = ?",
    )
    .get(functionalityId, slug) as Circuit | undefined;
}
