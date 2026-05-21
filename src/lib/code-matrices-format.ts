/**
 * Pure formatting helpers used by `<CodeMatrices>` to render symplectic
 * stabilizer / logical-operator matrices into the various display formats.
 *
 * Extracted from CodeMatrices.astro so the same helpers run in both the
 * Astro (server) module graph and the client-side script that lazy-loads
 * matrices on first expand of the collapsible.
 */

import { formatMatrixRows, symplecticToPauli } from "./utils";

/** Join one row per line of Pauli-formatted stabilizers / logicals. */
export function paulisJoined(matrix: number[][], n: number): string {
  return symplecticToPauli(matrix, n).join("\n");
}

/** Symplectic view: pad cells, split X/Z halves with `│`. */
export function symplecticJoined(matrix: number[][], n: number): string {
  const flat = matrix.flat();
  const colWidth = flat.length > 0 ? Math.max(...flat.map((v) => String(v).length)) : 1;
  const padCells = (cells: number[]) =>
    cells.map((v) => String(v).padStart(colWidth, " ")).join("  ");
  return matrix
    .map((row) => `[ ${padCells(row.slice(0, n))} │ ${padCells(row.slice(n, 2 * n))} ]`)
    .join("\n");
}

/**
 * CSS Hx/Hz view: two labelled matrix groups, sharing styling with the other
 * views. Sub-labels keep "[ row ]" formatting consistent and the two groups
 * are separated by a blank line.
 */
export function hxhzJoined(blocks: { label: string; matrix: number[][] }[]): string {
  return blocks
    .map(({ label, matrix }) => `${label}\n${formatMatrixRows(matrix).join("\n")}`)
    .join("\n\n");
}

/** Paste-ready `np.array(...)` literal. */
export function numpyArray(matrix: number[][]): string {
  if (matrix.length === 0) return "np.array([])";
  const rows = matrix.map((row) => `    [${row.join(", ")}],`).join("\n");
  return `np.array([\n${rows}\n])`;
}

export function numpyAssign(blocks: { name: string; matrix: number[][] }[]): string {
  return blocks.map(({ name, matrix }) => `${name} = ${numpyArray(matrix)}`).join("\n\n");
}
