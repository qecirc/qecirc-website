import { getDb } from "./db";

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
  code_id: number;
  name: string;
  slug: string;
  description: string | null;
  source: string;
  gate_count: number | null;
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

type FilterOp = "=" | "!=" | ">" | ">=" | "<" | "<=";

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

export interface CircuitFilters {
  gate_count?: FilterCondition[];
  depth?: FilterCondition[];
  qubit_count?: FilterCondition[];
  tags?: string[];
}

export interface TagWithCount {
  name: string;
  count: number;
}

export function getCodeTagsWithCount(): TagWithCount[] {
  const db = getDb();
  return db
    .prepare(
      `SELECT t.name, COUNT(*) as count FROM tags t
       JOIN taggings tg ON t.id = tg.tag_id
       WHERE tg.taggable_type = 'code'
       GROUP BY t.name ORDER BY t.name`,
    )
    .all() as TagWithCount[];
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
    || (filters.d?.length ?? 0) > 0
    || (filters.tags?.length ?? 0) > 0;
}

export function hasActiveCircuitFilters(filters: CircuitFilters): boolean {
  return (filters.gate_count?.length ?? 0) > 0
    || (filters.depth?.length ?? 0) > 0
    || (filters.qubit_count?.length ?? 0) > 0
    || (filters.tags?.length ?? 0) > 0;
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

export function filterCodes(filters: CodeFilters): (Code & { tags: string[] })[] {
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

// --- Circuit queries ---

export function getCircuitsForCode(
  codeId: number,
): (Circuit & { tags: string[] })[] {
  const db = getDb();
  const rows = db
    .prepare("SELECT * FROM circuits WHERE code_id = ? ORDER BY name")
    .all(codeId) as Circuit[];
  return rows.map((c) => ({ ...c, tags: getTagsFor("circuit", c.id) }));
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
): (Circuit & { tags: string[] })[] {
  const db = getDb();
  const conditions: string[] = ["c.code_id = ?"];
  const params: (number | string)[] = [codeId];

  addConditions("gate_count", filters.gate_count, conditions, params);
  addConditions("depth", filters.depth, conditions, params);
  addConditions("qubit_count", filters.qubit_count, conditions, params);
  addTagConditions(filters.tags, "circuit", conditions, params);

  const where = `WHERE ${conditions.join(" AND ")}`;
  const circuits = db
    .prepare(`SELECT * FROM circuits c ${where} ORDER BY c.name`)
    .all(...params) as Circuit[];
  return circuits.map((c) => ({ ...c, tags: getTagsFor("circuit", c.id) }));
}

const FORMAT_ORDER = ["stim", "qasm", "cirq"];

export function getBodiesForCircuits(circuitIds: number[]): Map<number, CircuitBody[]> {
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
  for (const [id, bodies] of result) {
    bodies.sort((a, b) => {
      const ai = FORMAT_ORDER.indexOf(a.format);
      const bi = FORMAT_ORDER.indexOf(b.format);
      return (ai === -1 ? Infinity : ai) - (bi === -1 ? Infinity : bi);
    });
  }

  return result;
}

// --- Tool queries ---

type ToolWithMeta = Tool & { tags: string[]; circuit_count: number };

function enrichTools(tools: Tool[]): ToolWithMeta[] {
  const db = getDb();
  return tools.map((t) => {
    const tags = getTagsFor("tool", t.id);
    const row = db
      .prepare("SELECT COUNT(*) as count FROM circuits WHERE tool_id = ?")
      .get(t.id) as { count: number };
    return { ...t, tags, circuit_count: row.count };
  });
}

export function getAllTools(): ToolWithMeta[] {
  const db = getDb();
  const tools = db.prepare("SELECT * FROM tools ORDER BY name").all() as Tool[];
  return enrichTools(tools);
}

export function getToolTagsWithCount(): TagWithCount[] {
  const db = getDb();
  return db
    .prepare(
      `SELECT t.name, COUNT(*) as count FROM tags t
       JOIN taggings tg ON t.id = tg.tag_id
       WHERE tg.taggable_type = 'tool'
       GROUP BY t.name ORDER BY t.name`,
    )
    .all() as TagWithCount[];
}

export function filterTools(filters: ToolFilters): ToolWithMeta[] {
  const db = getDb();
  const conditions: string[] = [];
  const params: (number | string)[] = [];

  if (filters.tags) {
    for (const tag of filters.tags) {
      conditions.push(
        `EXISTS (SELECT 1 FROM taggings tg JOIN tags t ON t.id = tg.tag_id
         WHERE tg.taggable_id = c.id AND tg.taggable_type = ? AND t.name = ?)`,
      );
      params.push("tool", tag);
    }
  }

  const where = conditions.length > 0 ? `WHERE ${conditions.join(" AND ")}` : "";
  const tools = db
    .prepare(`SELECT * FROM tools c ${where} ORDER BY c.name`)
    .all(...params) as Tool[];
  return enrichTools(tools);
}

export function hasActiveToolFilters(filters: ToolFilters): boolean {
  return (filters.tags?.length ?? 0) > 0;
}

export function searchTools(query: string): (Tool & { tags: string[] })[] {
  const db = getDb();
  const escaped = query.replace(/[%_\\]/g, "\\$&");
  const pattern = `%${escaped}%`;
  const tools = db
    .prepare(
      `SELECT DISTINCT c.* FROM tools c
       LEFT JOIN taggings tg ON tg.taggable_id = c.id AND tg.taggable_type = 'tool'
       LEFT JOIN tags t ON t.id = tg.tag_id
       WHERE c.name LIKE ? ESCAPE '\\' OR t.name LIKE ? ESCAPE '\\'
       ORDER BY c.name
       LIMIT 10`,
    )
    .all(pattern, pattern) as Tool[];
  return tools.map((t) => ({ ...t, tags: getTagsFor("tool", t.id) }));
}

export function getToolById(id: number): Tool | undefined {
  const db = getDb();
  return db.prepare("SELECT * FROM tools WHERE id = ?").get(id) as Tool | undefined;
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
