import { getDb } from "../db";
import type { Tool, ToolFilters, ToolWithMeta } from "../../types";
import { withTags, withCircuitCounts, addTagConditions } from "./shared";

export type ToolRow = Omit<Tool, "paper_urls"> & { paper_urls: string | null };

export function parseToolRow(row: ToolRow): Tool {
  return { ...row, paper_urls: row.paper_urls ? (JSON.parse(row.paper_urls) as string[]) : null };
}

function enrichTools(rows: ToolRow[]): ToolWithMeta[] {
  // circuit_count describes the curated library (circuits of hidden
  // HIDDEN_CODE_TAG codes excluded, matching every other displayed count);
  // hidden_circuit_count carries the codetables remainder so surfaces can
  // state both numbers. Ordering follows the curated count so a bulk
  // reference import cannot dominate the list.
  const visible = withCircuitCounts(withTags(rows.map(parseToolRow), "tool"), "tool_id", {
    visibleCodesOnly: true,
  });
  const totals = new Map(
    withCircuitCounts(rows.map(parseToolRow), "tool_id").map((t) => [t.id, t.circuit_count]),
  );
  return visible
    .map((t) => ({ ...t, hidden_circuit_count: (totals.get(t.id) ?? 0) - t.circuit_count }))
    .toSorted((a, b) => b.circuit_count - a.circuit_count || a.name.localeCompare(b.name));
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

/** Every tool catalogued, matching what /tools lists — which includes tools
 *  that have not contributed circuits yet ("More circuit-synthesis tools"). */
export function countAllTools(): number {
  const row = getDb().prepare("SELECT COUNT(*) AS count FROM tools").get() as { count: number };
  return row.count;
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
