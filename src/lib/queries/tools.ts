import { getDb } from "../db";
import type { Tool, ToolFilters, ToolWithMeta } from "../../types";
import { withTags, withCircuitCounts, addTagConditions } from "./shared";

type ToolRow = Omit<Tool, "paper_urls"> & { paper_urls: string | null };

function parseToolRow(row: ToolRow): Tool {
  return { ...row, paper_urls: row.paper_urls ? (JSON.parse(row.paper_urls) as string[]) : null };
}

function enrichTools(rows: ToolRow[]): ToolWithMeta[] {
  return withCircuitCounts(withTags(rows.map(parseToolRow), "tool"), "tool_id");
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
    .all() as ToolRow[];
  return enrichTools(tools);
}

export function getToolById(id: number): Tool | undefined {
  const db = getDb();
  const row = db.prepare("SELECT * FROM tools WHERE id = ?").get(id) as ToolRow | undefined;
  return row ? parseToolRow(row) : undefined;
}

export function filterTools(filters: ToolFilters): ToolWithMeta[] {
  const db = getDb();
  const conditions: string[] = [];
  const params: (number | string)[] = [];

  addTagConditions(filters.tags, "tool", conditions, params);

  const where = conditions.length > 0 ? `WHERE ${conditions.join(" AND ")}` : "";
  const tools = db
    .prepare(
      `SELECT c.* FROM tools c
       LEFT JOIN circuits ci ON ci.tool_id = c.id
       ${where}
       GROUP BY c.id
       ORDER BY COUNT(ci.id) DESC, c.name`,
    )
    .all(...params) as ToolRow[];
  return enrichTools(tools);
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
    .all(...circuitIds) as (ToolRow & { circuit_id: number })[];

  for (const row of rows) {
    result.set(row.circuit_id, {
      id: row.id,
      name: row.name,
      slug: row.slug,
      description: row.description,
      homepage_url: row.homepage_url,
      github_url: row.github_url,
      paper_urls: row.paper_urls ? (JSON.parse(row.paper_urls) as string[]) : null,
    });
  }
  return result;
}
