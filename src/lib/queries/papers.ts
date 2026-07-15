import { getDb } from "../db";
import type { Paper } from "../../types";

export type PaperRow = Omit<Paper, "authors"> & { authors: string };

export function parsePaperRow(row: PaperRow): Paper {
  return { ...row, authors: JSON.parse(row.authors) as string[] };
}

/** Surname for the citation line.
 *
 * Last whitespace-separated word of the full name. This is a heuristic and it
 * would get "Ludwig van Beethoven" wrong (-> "Beethoven" is right, but "Vincent
 * van Gogh" -> "Gogh" is not), so it is confined to the citation label: every
 * search index gets the FULL name, and the link always carries the real
 * identifier. A wrong surname here mislabels a link; it cannot lose a paper.
 */
function surname(fullName: string): string {
  const parts = fullName.trim().split(/\s+/);
  return parts[parts.length - 1] ?? fullName;
}

/** Author credit in the usual convention: one name, two joined by "&", or the
 *  first followed by "et al." */
export function formatAuthors(authors: string[]): string {
  if (authors.length === 0) return "";
  if (authors.length === 1) return surname(authors[0]);
  if (authors.length === 2) return `${surname(authors[0])} & ${surname(authors[1])}`;
  return `${surname(authors[0])} et al.`;
}

/** The one-line citation shown wherever a circuit's source is displayed, e.g.
 *  "Zen et al. (2024)". Year omitted rather than faked when unknown. */
export function formatCitation(paper: Paper): string {
  const authors = formatAuthors(paper.authors);
  return paper.year == null ? authors : `${authors} (${paper.year})`;
}

/** How the paper prefers to be referred to in short form: "arXiv:2402.17761",
 *  else the DOI, else nothing. Distinct from the citation — this is the id a
 *  reader would search for, not the credit. */
export function formatPaperId(paper: Paper): string | null {
  if (paper.arxiv_id) return `arXiv:${paper.arxiv_id}`;
  if (paper.doi) return `doi:${paper.doi}`;
  return null;
}

/** Papers for a batch of circuits, keyed by circuit id. Mirrors
 *  getToolsForCircuits: one query per page, not one per row. */
export function getPapersForCircuits(circuitIds: number[]): Map<number, Paper> {
  const result = new Map<number, Paper>();
  if (circuitIds.length === 0) return result;

  const placeholders = circuitIds.map(() => "?").join(",");
  const rows = getDb()
    .prepare(
      `SELECT c.id AS circuit_id, p.* FROM circuits c
       JOIN papers p ON p.id = c.paper_id
       WHERE c.id IN (${placeholders}) AND c.paper_id IS NOT NULL`,
    )
    .all(...circuitIds) as (PaperRow & { circuit_id: number })[];

  for (const row of rows) {
    const { circuit_id, ...paper } = row;
    result.set(circuit_id, parsePaperRow(paper));
  }
  return result;
}

/** Distinct papers at least one circuit is taken from, for the landing page
 *  stat. Counts papers with circuits rather than every row in `papers`: the
 *  stat claims "circuits drawn from N papers", and a paper catalogued ahead of
 *  its circuits has contributed none yet. (`tools` counts differently and on
 *  purpose — /tools lists tools with no circuits, so countAllTools includes
 *  them.) */
export function countCircuitPapers(): number {
  const row = getDb()
    .prepare(
      `SELECT COUNT(DISTINCT p.id) AS count FROM papers p
       JOIN circuits c ON c.paper_id = p.id`,
    )
    .get() as { count: number };
  return row.count;
}
