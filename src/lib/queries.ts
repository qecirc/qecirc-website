import { getDb } from "./db";
import type {
  Code,
  CodeWithMeta,
  Circuit,
  CircuitBody,
  CircuitFilters,
  CircuitSort,
  CircuitSortField,
  CodeFilters,
  FilterCondition,
  FilterOp,
  SortDir,
  TaggableType,
  TagWithCount,
  Tool,
  ToolFilters,
  ToolWithMeta,
} from "../types";

export function formatCodeParams(code: Code): string {
  return code.d != null
    ? `[[${code.n},${code.k},${code.d}]]`
    : `[[${code.n},${code.k}]]`;
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

function withTags<T extends { id: number }>(
  items: T[],
  taggableType: TaggableType,
): (T & { tags: string[] })[] {
  return items.map((item) => ({
    ...item,
    tags: getTagsFor(taggableType, item.id),
  }));
}

function withCircuitCounts<T extends { id: number }>(
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

export function getAllCodes(): CodeWithMeta[] {
  const db = getDb();
  const codes = db.prepare("SELECT * FROM codes ORDER BY name").all() as Code[];
  return withCircuitCounts(withTags(codes, "code"), "code_id");
}

export function getCodeBySlug(slug: string): Code | undefined {
  const db = getDb();
  return db.prepare("SELECT * FROM codes WHERE slug = ?").get(slug) as
    | Code
    | undefined;
}

const VALID_SORT_FIELDS: readonly string[] = [
  "qubit_count",
  "depth",
  "gate_count",
  "two_qubit_gate_count",
];

function buildOrderBy(sort?: CircuitSort): string {
  if (!sort || !VALID_SORT_FIELDS.includes(sort.field)) {
    return "ORDER BY c.name";
  }
  const dir = sort.dir === "asc" ? "ASC" : "DESC";
  // safe: field validated against VALID_SORT_FIELDS allowlist; NULLs always last
  return `ORDER BY CASE WHEN c.${sort.field} IS NULL THEN 1 ELSE 0 END, c.${sort.field} ${dir}, c.name`;
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

    const match = trimmed.match(/^(!=|>=|<=|>|<|=)?\s*(\d+)$/);
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

function addConditions(
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

function addTagConditions(
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

export function filterCodes(
  filters: CodeFilters,
): CodeWithMeta[] {
  const db = getDb();
  const conditions: string[] = [];
  const params: (number | string)[] = [];

  addConditions("n", filters.n, conditions, params);
  addConditions("k", filters.k, conditions, params);
  addConditions("d", filters.d, conditions, params);
  addTagConditions(filters.tags, "code", conditions, params);

  const where =
    conditions.length > 0 ? `WHERE ${conditions.join(" AND ")}` : "";
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

function tokenize(query: string): string[] {
  return query
    .trim()
    .split(/\s+/)
    .filter((t) => t.length > 0)
    .map((t) => `%${t.replace(/[%_\\]/g, "\\$&")}%`);
}

function searchByType<T extends { id: number }>(
  table: string,
  taggableType: TaggableType,
  query: string,
  limit: number,
): (T & { tags: string[] })[] {
  const patterns = tokenize(query);
  if (patterns.length === 0) return [];

  const db = getDb();
  const tokenClauses = patterns.map(
    () =>
      `(c.name LIKE ? ESCAPE '\\' OR EXISTS (
        SELECT 1 FROM taggings tg JOIN tags t ON t.id = tg.tag_id
        WHERE tg.taggable_id = c.id AND tg.taggable_type = ? AND t.name LIKE ? ESCAPE '\\'
      ))`,
  );
  const params: string[] = [];
  for (const p of patterns) params.push(p, taggableType, p);

  const rows = db
    .prepare(
      `SELECT c.* FROM ${table} c
       WHERE ${tokenClauses.join(" AND ")}
       ORDER BY c.name
       LIMIT ${limit}`,
    )
    .all(...params) as T[];
  return withTags(rows, taggableType);
}

export function searchCodes(query: string): (Code & { tags: string[] })[] {
  return searchByType<Code>("codes", "code", query, 20);
}

// --- Circuit queries ---

export function getCircuitsForCode(
  codeId: number,
  sort?: CircuitSort,
): (Circuit & { tags: string[] })[] {
  const db = getDb();
  const orderBy = buildOrderBy(sort);
  const rows = db
    .prepare(`SELECT * FROM circuits c WHERE c.code_id = ? ${orderBy}`)
    .all(codeId) as Circuit[];
  return withTags(rows, "circuit");
}

export function countCircuitsForCode(codeId: number): number {
  const db = getDb();
  const row = db
    .prepare("SELECT COUNT(*) as count FROM circuits WHERE code_id = ?")
    .get(codeId) as { count: number };
  return row.count;
}

export function getCircuitTagsForCode(codeId: number): TagWithCount[] {
  const db = getDb();
  return db
    .prepare(
      `SELECT t.name, COUNT(*) as count FROM tags t
       JOIN taggings tg ON t.id = tg.tag_id
       JOIN circuits c ON c.id = tg.taggable_id
       WHERE tg.taggable_type = 'circuit' AND c.code_id = ?
       GROUP BY t.name ORDER BY t.name`,
    )
    .all(codeId) as TagWithCount[];
}

export function filterCircuitsForCode(
  codeId: number,
  filters: CircuitFilters,
  sort?: CircuitSort,
): (Circuit & { tags: string[] })[] {
  const db = getDb();
  const conditions: string[] = ["c.code_id = ?"];
  const params: (number | string)[] = [codeId];

  addConditions("gate_count", filters.gate_count, conditions, params);
  addConditions(
    "two_qubit_gate_count",
    filters.two_qubit_gate_count,
    conditions,
    params,
  );
  addConditions("depth", filters.depth, conditions, params);
  addConditions("qubit_count", filters.qubit_count, conditions, params);
  addTagConditions(filters.tags, "circuit", conditions, params);

  const where = `WHERE ${conditions.join(" AND ")}`;
  const orderBy = buildOrderBy(sort);
  const circuits = db
    .prepare(`SELECT * FROM circuits c ${where} ${orderBy}`)
    .all(...params) as Circuit[];
  return withTags(circuits, "circuit");
}

const FORMAT_ORDER = ["stim", "qasm", "cirq"];

export function getBodiesForCircuits(
  circuitIds: number[],
): Map<number, CircuitBody[]> {
  const db = getDb();
  const result = new Map<number, CircuitBody[]>();
  if (circuitIds.length === 0) return result;

  const placeholders = circuitIds.map(() => "?").join(",");
  const rows = db
    .prepare(
      `SELECT circuit_id, format, body FROM circuit_bodies
       WHERE circuit_id IN (${placeholders})`,
    )
    .all(...circuitIds) as (CircuitBody & { circuit_id: number })[];

  for (const row of rows) {
    const list = result.get(row.circuit_id) ?? [];
    list.push({ format: row.format, body: row.body });
    result.set(row.circuit_id, list);
  }

  // Sort each circuit's bodies by preferred format order
  for (const [, bodies] of result) {
    bodies.sort((a, b) => {
      const ai = FORMAT_ORDER.indexOf(a.format);
      const bi = FORMAT_ORDER.indexOf(b.format);
      return (ai === -1 ? Infinity : ai) - (bi === -1 ? Infinity : bi);
    });
  }

  return result;
}

// --- Tool queries ---

function enrichTools(tools: Tool[]): ToolWithMeta[] {
  return withCircuitCounts(withTags(tools, "tool"), "tool_id");
}

export function getAllTools(): ToolWithMeta[] {
  const db = getDb();
  const tools = db
    .prepare(
      `SELECT t.* FROM tools t
       LEFT JOIN circuits c ON c.tool_id = t.id
       GROUP BY t.id
       ORDER BY COUNT(c.id) DESC, t.name`,
    )
    .all() as Tool[];
  return enrichTools(tools);
}

export function filterTools(filters: ToolFilters): ToolWithMeta[] {
  const db = getDb();
  const conditions: string[] = [];
  const params: (number | string)[] = [];

  addTagConditions(filters.tags, "tool", conditions, params);

  const where =
    conditions.length > 0 ? `WHERE ${conditions.join(" AND ")}` : "";
  const tools = db
    .prepare(
      `SELECT c.* FROM tools c
       LEFT JOIN circuits ci ON ci.tool_id = c.id
       ${where}
       GROUP BY c.id
       ORDER BY COUNT(ci.id) DESC, c.name`,
    )
    .all(...params) as Tool[];
  return enrichTools(tools);
}

export function searchTools(query: string): (Tool & { tags: string[] })[] {
  return searchByType<Tool>("tools", "tool", query, 10);
}

export function searchCircuits(
  query: string,
): (Circuit & { tags: string[]; code_slug: string; code_name: string })[] {
  const patterns = tokenize(query);
  if (patterns.length === 0) return [];

  const db = getDb();
  const tokenClauses = patterns.map(
    () =>
      `(ci.name LIKE ? ESCAPE '\\' OR co.name LIKE ? ESCAPE '\\'
        OR EXISTS (
          SELECT 1 FROM taggings tg JOIN tags t ON t.id = tg.tag_id
          WHERE tg.taggable_id = ci.id AND tg.taggable_type = 'circuit' AND t.name LIKE ? ESCAPE '\\'
        )
        OR EXISTS (
          SELECT 1 FROM tools tl WHERE tl.id = ci.tool_id AND tl.name LIKE ? ESCAPE '\\'
        ))`,
  );
  const params: string[] = [];
  for (const p of patterns) params.push(p, p, p, p);

  const rows = db
    .prepare(
      `SELECT ci.*, co.slug AS code_slug, co.name AS code_name
       FROM circuits ci
       JOIN codes co ON co.id = ci.code_id
       WHERE ${tokenClauses.join(" AND ")}
       ORDER BY ci.name
       LIMIT 10`,
    )
    .all(...params) as (Circuit & { code_slug: string; code_name: string })[];

  return rows.map((row) => ({
    ...row,
    tags: getTagsFor("circuit", row.id),
  }));
}

export function getToolById(id: number): Tool | undefined {
  const db = getDb();
  return db.prepare("SELECT * FROM tools WHERE id = ?").get(id) as
    | Tool
    | undefined;
}

export function getToolsForCircuits(circuitIds: number[]): Map<number, Tool> {
  const db = getDb();
  const result = new Map<number, Tool>();
  if (circuitIds.length === 0) return result;

  const placeholders = circuitIds.map(() => "?").join(",");
  const rows = db
    .prepare(
      `SELECT c.id as circuit_id, t.* FROM circuits c
       JOIN tools t ON t.id = c.tool_id
       WHERE c.id IN (${placeholders}) AND c.tool_id IS NOT NULL`,
    )
    .all(...circuitIds) as (Tool & { circuit_id: number })[];

  for (const row of rows) {
    result.set(row.circuit_id, {
      id: row.id,
      name: row.name,
      slug: row.slug,
      description: row.description,
      homepage_url: row.homepage_url,
      github_url: row.github_url,
    });
  }
  return result;
}
