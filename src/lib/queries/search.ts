import { getDb } from "../db";
import type { Code, Circuit, Tool } from "../../types";
import { withTags } from "./shared";

function rawTokenize(query: string): string[] {
  return query
    .trim()
    .split(/\s+/)
    .filter((t) => t.length > 0);
}

function tokenize(query: string): string[] {
  return rawTokenize(query).map((t) => `%${t.replace(/[%_\\]/g, "\\$&")}%`);
}

function searchByType<T extends { id: number }>(
  table: string,
  taggableType: "code" | "circuit" | "tool",
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
       LIMIT ?`,
    )
    .all(...params, limit) as T[];
  return withTags(rows, taggableType);
}

export function searchCodes(query: string): (Code & { tags: string[] })[] {
  return searchByType<Code>("codes", "code", query, 20);
}

export function searchCircuits(
  query: string,
): (Circuit & { tags: string[]; code_slug: string; code_name: string })[] {
  const rawTokens = rawTokenize(query);
  if (rawTokens.length === 0) return [];

  const db = getDb();
  const tokenClauses: string[] = [];
  const params: (string | number)[] = [];

  for (const raw of rawTokens) {
    const p = `%${raw.replace(/[%_\\]/g, "\\$&")}%`;
    const stripped = raw.replace(/^#/, "");
    const asInt = /^\d+$/.test(stripped) ? parseInt(stripped, 10) : null;

    if (asInt !== null) {
      tokenClauses.push(
        `(ci.qec_id = ? OR ci.name LIKE ? ESCAPE '\\' OR co.name LIKE ? ESCAPE '\\'
          OR EXISTS (
            SELECT 1 FROM taggings tg JOIN tags t ON t.id = tg.tag_id
            WHERE tg.taggable_id = ci.id AND tg.taggable_type = 'circuit' AND t.name LIKE ? ESCAPE '\\'
          )
          OR EXISTS (
            SELECT 1 FROM tools tl WHERE tl.id = ci.tool_id AND tl.name LIKE ? ESCAPE '\\'
          ))`,
      );
      params.push(asInt, p, p, p, p);
    } else {
      tokenClauses.push(
        `(ci.name LIKE ? ESCAPE '\\' OR co.name LIKE ? ESCAPE '\\'
          OR EXISTS (
            SELECT 1 FROM taggings tg JOIN tags t ON t.id = tg.tag_id
            WHERE tg.taggable_id = ci.id AND tg.taggable_type = 'circuit' AND t.name LIKE ? ESCAPE '\\'
          )
          OR EXISTS (
            SELECT 1 FROM tools tl WHERE tl.id = ci.tool_id AND tl.name LIKE ? ESCAPE '\\'
          ))`,
      );
      params.push(p, p, p, p);
    }
  }

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

  return withTags(rows, "circuit") as (Circuit & {
    tags: string[];
    code_slug: string;
    code_name: string;
  })[];
}

export function searchTools(query: string): (Tool & { tags: string[] })[] {
  return searchByType<Tool>("tools", "tool", query, 10);
}
