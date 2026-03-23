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
