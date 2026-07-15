// Formatting helpers for displayed circuit bodies. Pure string work, imported
// from both Astro frontmatter (CodeBlock.astro renders server-side) and the
// browser (circuit-bodies-client.ts clones a template on code pages), so the
// two paths cannot drift.

/** A QUBIT_COORDS line, e.g. `QUBIT_COORDS(3, 7) 0`. */
const COORDS_LINE = /^\s*QUBIT_COORDS\b/;

/** The detector/observable-annotated STIM body. Stored as its own
 *  `circuit_bodies` format, but it is a *view* of the STIM body rather than a
 *  format of its own, so it never gets a format tab. It supersedes the plain
 *  STIM body for display, and the switches subtract from it. */
export const ANNOTATED_FORMAT = "stim-annotated";

/** The format whose tab the Detectors switch belongs to. */
export const ANNOTATED_OF = "stim";

export interface FormatBody {
  format: string;
  body: string;
}

/** Split the annotated body out of a bodies list.
 *
 *  Shared by the server (FormatSwitcher) and the browser (circuit-bodies-client)
 *  so the two cannot disagree about which formats get a tab.
 */
export function splitAnnotated<T extends FormatBody>(
  bodies: T[],
): { tabs: T[]; annotated: string | undefined } {
  const annotated = bodies.find((b) => b.format === ANNOTATED_FORMAT)?.body?.trimEnd();
  return { tabs: bodies.filter((b) => b.format !== ANNOTATED_FORMAT), annotated };
}

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

/** A DETECTOR or OBSERVABLE_INCLUDE annotation. */
const ANNOTATION_LINE = /^\s*(DETECTOR|OBSERVABLE_INCLUDE)\b/;
/** A terminal readout: `M`/`MX` followed by targets. Deliberately does NOT match
 *  `MR`, `MY`, `MZ` or `MPP` — those appear mid-body as flag measurements. */
const READOUT_LINE = /^\s*(M|MX)\s/;
/** A bare TICK. */
const TICK_LINE = /^\s*TICK\s*$/;

export function hasDetectors(code: string): boolean {
  return code.split("\n").some((line) => ANNOTATION_LINE.test(line));
}

/** Drop the readout epilogue, keeping the reset prologue and the body.
 *
 *  Only the *added* epilogue goes. Pre-existing mid-circuit measurements are
 *  part of the circuit — 399 of 834 bodies carry flag/verification measurements
 *  — and must survive. The generator appends exactly one readout instruction,
 *  last, so once the annotations are dropped it is the final line; anything
 *  earlier belongs to the body.
 *
 *  Mirrors `strip_readout` in scripts/add_circuit/annotate.py, which does the
 *  same server-side to build the un-annotated Crumble link. Keep the two in step.
 */
export function stripReadout(code: string): string {
  const lines = code
    .trimEnd()
    .split("\n")
    .filter((line) => !ANNOTATION_LINE.test(line));
  if (lines.length && READOUT_LINE.test(lines[lines.length - 1])) lines.pop();
  while (lines.length && TICK_LINE.test(lines[lines.length - 1])) lines.pop();
  return lines.join("\n").trimEnd();
}

/** The body as displayed, derived from the fullest form the circuit has.
 *
 *  Both switches subtract from that one superset rather than swapping between
 *  bodies, so they compose. Coordinates are hidden unless asked for: a d=11
 *  unrotated prep opens with 221 QUBIT_COORDS lines before its first gate, which
 *  buries the circuit. Detectors are hidden unless asked for too — but the reset
 *  prologue stays in both, because stating the |0...0> input explicitly is not
 *  part of what the Detectors switch is about. The Crumble link always keeps
 *  coordinates: that is where the layout is the point.
 */
export function bodyForDisplay(code: string, showCoords: boolean, showDetectors: boolean): string {
  let out = code.trimEnd();
  if (!showDetectors) out = stripReadout(out);
  if (!showCoords) out = stripQubitCoords(out);
  return out.trimEnd();
}
