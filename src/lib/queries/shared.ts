import { getDb } from "../db";
import type {
  CircuitFilters,
  CircuitSort,
  CodeFilters,
  FilterCondition,
  FilterOp,
  TaggableType,
  TagWithCount,
  ToolFilters,
} from "../../types";
import { CIRCUIT_SORT_FIELDS, FILTER_PART_REGEX } from "../constants";

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

export function withTags<T extends { id: number }>(
  items: T[],
  taggableType: TaggableType,
): (T & { tags: string[] })[] {
  if (items.length === 0) return [];
  const db = getDb();
  const placeholders = items.map(() => "?").join(",");
  const rows = db
    .prepare(
      `SELECT tg.taggable_id, t.name FROM tags t
       JOIN taggings tg ON t.id = tg.tag_id
       WHERE tg.taggable_type = ? AND tg.taggable_id IN (${placeholders})
       ORDER BY t.name`,
    )
    .all(taggableType, ...items.map((i) => i.id)) as {
    taggable_id: number;
    name: string;
  }[];

  const tagMap = new Map<number, string[]>();
  for (const row of rows) {
    const list = tagMap.get(row.taggable_id) ?? [];
    list.push(row.name);
    tagMap.set(row.taggable_id, list);
  }

  return items.map((item) => ({
    ...item,
    tags: tagMap.get(item.id) ?? [],
  }));
}

export function withCircuitCounts<T extends { id: number }>(
  items: T[],
  fkColumn: "code_id" | "tool_id",
): (T & { circuit_count: number })[] {
  if (items.length === 0) return [];
  const db = getDb();
  const placeholders = items.map(() => "?").join(",");
  const rows = db
    .prepare(
      `SELECT ${fkColumn} AS fk, COUNT(*) AS count FROM circuits
       WHERE ${fkColumn} IN (${placeholders}) GROUP BY ${fkColumn}`,
    )
    .all(items.map((i) => i.id)) as { fk: number; count: number }[];
  const counts = new Map(rows.map((r) => [r.fk, r.count]));
  return items.map((i) => ({ ...i, circuit_count: counts.get(i.id) ?? 0 }));
}

export function getTagsWithCount(taggableType: TaggableType): TagWithCount[] {
  const db = getDb();
  return db
    .prepare(
      `SELECT t.name, COUNT(*) as count FROM tags t
       JOIN taggings tg ON t.id = tg.tag_id
       WHERE tg.taggable_type = ?
       GROUP BY t.name ORDER BY t.name`,
    )
    .all(taggableType) as TagWithCount[];
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

    const match = trimmed.match(FILTER_PART_REGEX);
    if (!match) return null;

    const op = (match[1] || "=") as FilterOp;
    const value = parseInt(match[2], 10);
    if (!Number.isFinite(value) || value < 0) return null;

    conditions.push({ op, value });
  }

  return conditions.length > 0 ? conditions : null;
}

export function hasActiveFilters(
  filters: CodeFilters | CircuitFilters | ToolFilters,
): boolean {
  return Object.values(filters).some((v) => Array.isArray(v) && v.length > 0);
}

export function buildOrderBy(sort?: CircuitSort): string {
  if (!sort || !CIRCUIT_SORT_FIELDS.includes(sort.field)) {
    return "ORDER BY c.name";
  }
  const dir = sort.dir === "asc" ? "ASC" : "DESC";
  // safe: field validated against VALID_SORT_FIELDS allowlist; NULLs always last
  return `ORDER BY CASE WHEN c.${sort.field} IS NULL THEN 1 ELSE 0 END, c.${sort.field} ${dir}, c.name`;
}

export function addConditions(
  column: string,
  filter: FilterCondition[] | undefined,
  conditions: string[],
  params: (number | string)[],
) {
  if (!filter) return;
  for (const { op, value } of filter) {
    if (!(VALID_OPS as readonly string[]).includes(op)) continue;
    conditions.push(`c.${column} ${op} ?`);
    params.push(value);
  }
}

export function addTagConditions(
  tags: string[] | undefined,
  taggableType: TaggableType,
  conditions: string[],
  params: (number | string)[],
) {
  if (!tags) return;
  for (const tag of tags) {
    conditions.push(
      `EXISTS (SELECT 1 FROM taggings tg JOIN tags t ON t.id = tg.tag_id
       WHERE tg.taggable_id = c.id AND tg.taggable_type = ? AND t.name = ?)`,
    );
    params.push(taggableType, tag);
  }
}
