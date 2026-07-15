// Formatting helpers for displayed circuit bodies. Pure string work, imported
// from both Astro frontmatter (CodeBlock.astro renders server-side) and the
// browser (circuit-bodies-client.ts clones a template on code pages), so the
// two paths cannot drift.

/** A QUBIT_COORDS line, e.g. `QUBIT_COORDS(3, 7) 0`. */
const COORDS_LINE = /^\s*QUBIT_COORDS\b/;

/** Line-number gutter, right-aligned to the widest line number. */
export function lineNumbered(code: string): string {
  const lines = code.trimEnd().split("\n");
  const gutterWidth = String(lines.length).length;
  return lines.map((line, i) => `${String(i + 1).padStart(gutterWidth, " ")}  ${line}`).join("\n");
}

export function hasQubitCoords(code: string): boolean {
  return code.split("\n").some((line) => COORDS_LINE.test(line));
}

/** Drop QUBIT_COORDS declarations. The result is still valid STIM: coordinates
 *  are qubit metadata and carry no operational meaning. */
export function stripQubitCoords(code: string): string {
  return code
    .split("\n")
    .filter((line) => !COORDS_LINE.test(line))
    .join("\n")
    .trimEnd();
}

/** The body as displayed. Coordinates are hidden unless asked for: a d=11
 *  unrotated prep opens with 221 QUBIT_COORDS lines before its first gate,
 *  which buries the circuit. The Crumble link always keeps them — that is where
 *  the layout is the point. */
export function bodyForDisplay(code: string, showCoords: boolean): string {
  const raw = code.trimEnd();
  return showCoords ? raw : stripQubitCoords(raw);
}
