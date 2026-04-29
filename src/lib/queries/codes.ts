import { getDb } from "../db";
import type { Code, CodeFilters, CodeWithMeta } from "../../types";
import { withTags, withCircuitCounts, addConditions, addTagConditions } from "./shared";

export function formatCodeParams(code: Code): string {
  return code.d != null ? `[[${code.n},${code.k},${code.d}]]` : `[[${code.n},${code.k}]]`;
}

export function getAllCodes(): CodeWithMeta[] {
  const db = getDb();
  const codes = db.prepare("SELECT * FROM codes ORDER BY name").all() as Code[];
  return withCircuitCounts(withTags(codes, "code"), "code_id");
}

export function getCodeBySlug(slug: string): Code | undefined {
  const db = getDb();
  return db.prepare("SELECT * FROM codes WHERE slug = ?").get(slug) as Code | undefined;
}

export function filterCodes(filters: CodeFilters): CodeWithMeta[] {
  const db = getDb();
  const conditions: string[] = [];
  const params: (number | string)[] = [];

  addConditions("n", filters.n, conditions, params);
  addConditions("k", filters.k, conditions, params);
  addConditions("d", filters.d, conditions, params);
  addTagConditions(filters.tags, "code", conditions, params);

  const where = conditions.length > 0 ? `WHERE ${conditions.join(" AND ")}` : "";
  const codes = db
    .prepare(`SELECT * FROM codes c ${where} ORDER BY c.name`)
    .all(...params) as Code[];
  return withCircuitCounts(withTags(codes, "code"), "code_id");
}

export function countAllCodes(): number {
  const db = getDb();
  const row = db.prepare("SELECT COUNT(*) as count FROM codes").get() as {
    count: number;
  };
  return row.count;
}
