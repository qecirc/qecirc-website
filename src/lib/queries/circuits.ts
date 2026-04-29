import { getDb } from "../db";
import type {
  Circuit,
  CircuitBody,
  CircuitFilters,
  CircuitOriginal,
  CircuitSort,
  TagWithCount,
} from "../../types";
import {
  withTags,
  buildOrderBy,
  hasActiveFilters,
  addConditions,
  addTagConditions,
} from "./shared";

export function formatCircuitId(qecId: number): string {
  return `#${qecId}`;
}

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

export function countAllCircuits(): number {
  const db = getDb();
  const row = db.prepare("SELECT COUNT(*) as count FROM circuits").get() as {
    count: number;
  };
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
  addConditions("two_qubit_gate_count", filters.two_qubit_gate_count, conditions, params);
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

export function getCircuitsWithBodies(
  codeId: number,
  filters: CircuitFilters,
  sort?: CircuitSort,
): {
  circuits: (Circuit & { tags: string[] })[];
  bodiesMap: Map<number, CircuitBody[]>;
} {
  const circuits = hasActiveFilters(filters)
    ? filterCircuitsForCode(codeId, filters, sort)
    : getCircuitsForCode(codeId, sort);
  const bodiesMap = getBodiesForCircuits(circuits.map((c) => c.id));
  return { circuits, bodiesMap };
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
  for (const [, bodies] of result) {
    bodies.sort((a, b) => {
      const ai = FORMAT_ORDER.indexOf(a.format);
      const bi = FORMAT_ORDER.indexOf(b.format);
      return (ai === -1 ? Infinity : ai) - (bi === -1 ? Infinity : bi);
    });
  }

  return result;
}

export function getCircuitByQecId(
  qecId: number,
): (Circuit & { tags: string[]; code_slug: string; code_name: string; code_n: number }) | null {
  const db = getDb();
  const row = db
    .prepare(
      `SELECT c.*, co.slug AS code_slug, co.name AS code_name, co.n AS code_n
       FROM circuits c
       JOIN codes co ON co.id = c.code_id
       WHERE c.qec_id = ?`,
    )
    .get(qecId) as (Circuit & { code_slug: string; code_name: string; code_n: number }) | undefined;
  if (!row) return null;
  const [enriched] = withTags([row], "circuit");
  return {
    ...enriched,
    code_slug: row.code_slug,
    code_name: row.code_name,
    code_n: row.code_n,
  };
}

export function getCircuitsByQecIds(
  qecIds: number[],
): (Circuit & { tags: string[]; code_slug: string; code_name: string })[] {
  if (qecIds.length === 0) return [];
  const capped = qecIds.slice(0, 200);
  const db = getDb();
  const placeholders = capped.map(() => "?").join(",");
  const rows = db
    .prepare(
      `SELECT c.*, co.slug AS code_slug, co.name AS code_name
       FROM circuits c
       JOIN codes co ON co.id = c.code_id
       WHERE c.qec_id IN (${placeholders})
       ORDER BY co.name, c.name`,
    )
    .all(...capped) as (Circuit & { code_slug: string; code_name: string })[];
  return withTags(rows, "circuit") as (Circuit & {
    tags: string[];
    code_slug: string;
    code_name: string;
  })[];
}

export function getOriginalForCircuit(circuitId: number): CircuitOriginal | null {
  const db = getDb();
  return (
    (db
      .prepare(
        `SELECT original_stim, original_hx, original_hz, original_logical_x, original_logical_z, original_h, original_logical
       FROM circuit_originals WHERE circuit_id = ?`,
      )
      .get(circuitId) as CircuitOriginal | undefined) ?? null
  );
}
