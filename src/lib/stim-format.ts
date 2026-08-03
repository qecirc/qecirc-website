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
 *  part of the circuit — most bodies carry flag/verification measurements — and
 *  must survive. The annotator appends exactly one readout instruction, last, so
 *  once the annotations are dropped it is the final line; anything earlier
 *  belongs to the body.
 *
 *  **An unannotated body is returned untouched**, and that guard is load-bearing
 *  rather than an optimisation. `hasDetectors` is what decides whether the
 *  Detectors switch exists, so without it a body with no annotations had its
 *  final measurement removed with no control anywhere on the page to bring it
 *  back: 294 canonical bodies end in a readout, and `/circuits/662` rendered
 *  `H 0 / CX …` while its Crumble link opened the same circuit *with* `M 10`.
 *  Copy and Download hand over what is displayed, so the user could take away a
 *  circuit missing its final measurement. Tying the subtraction to the presence
 *  of annotations means the readout is only ever hidden when there is a switch
 *  that restores it.
 *
 *  Mirrors `strip_readout` in scripts/add_circuit/annotate.py, which the
 *  annotator's own tests use as the reference for the same rule. Keep the two in
 *  step — with one known difference: the Python one recurses into `REPEAT`
 *  blocks and pops a round's own final measurement, which for a syndrome round
 *  is part of the circuit, not an epilogue.
 */
export function stripReadout(code: string): string {
  const trimmed = code.trimEnd();
  if (!hasDetectors(trimmed)) return trimmed;
  const lines = trimmed.split("\n").filter((line) => !ANNOTATION_LINE.test(line));
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

/** Instruction names Crumble abbreviates in a URL. stim's own
 *  `Circuit.to_crumble_url()` writes these short forms, and the two must agree
 *  or a link stops matching the one the pipeline used to store. */
const CRUMBLE_ABBREVIATIONS: Record<string, string> = {
  QUBIT_COORDS: "Q",
  DETECTOR: "DT",
  OBSERVABLE_INCLUDE: "OI",
};

const INSTRUCTION_NAME = /^[A-Z_][A-Z_0-9]*/;
const PAREN_ARGS = /\(([^)]*)\)/g;

export const CRUMBLE_BASE = "https://algassert.com/crumble#circuit=";

/** A Crumble link for a STIM body — the transform stim's `to_crumble_url()`
 *  applies, reproduced exactly.
 *
 *  This used to be stored per circuit (`crumble_url`, plus a second
 *  `crumble_url_annotated` for the Detectors view), which cost half a megabyte
 *  of YAML to say something the body already says, went stale whenever the body
 *  was regenerated, and was dropped above ~40 qubits because the stored string
 *  got too big. Deriving it removes all three problems: the link now exists at
 *  any width, and it is by construction the circuit that is on screen.
 *
 *  The encoding, verified against all 1123 URLs the library used to store:
 *  lines are joined with `;`, blank lines and indentation dropped, the three
 *  instruction names above abbreviated, `, ` inside a parenthesised argument
 *  list collapsed to `,`, the space after `)` dropped, every remaining space
 *  written `_`, and a single trailing `_` appended.
 */
export function crumbleUrl(body: string): string {
  const parts: string[] = [];
  for (const rawLine of body.split("\n")) {
    let line = rawLine.trim();
    if (!line) continue;
    const name = line.match(INSTRUCTION_NAME)?.[0];
    if (name && name in CRUMBLE_ABBREVIATIONS) {
      line = CRUMBLE_ABBREVIATIONS[name] + line.slice(name.length);
    }
    line = line.replace(PAREN_ARGS, (_m, args: string) => `(${args.replaceAll(", ", ",")})`);
    parts.push(line.replaceAll(") ", ")").replaceAll(" ", "_"));
  }
  return `${CRUMBLE_BASE}${parts.join(";")}_`;
}

/** The Crumble link for an annotated body, following the Detectors switch.
 *
 *  Coordinates are always kept — in Crumble the layout is the point, so the
 *  Coords switch is deliberately not an argument here.
 */
export function crumbleAnnotatedUrl(annotated: string, showDetectors: boolean): string {
  return crumbleUrl(showDetectors ? annotated : stripReadout(annotated));
}

/** The Crumble link a circuit opens with: its default view, detectors hidden.
 *
 *  `annotated` is the circuit's `stim-annotated` body, or undefined when it has
 *  none. Either way `stripReadout` only subtracts from a body that carries
 *  annotations, so a circuit that was never annotated is linked whole — 294
 *  canonical bodies end in a measurement that is part of the circuit.
 */
export function crumbleHref(stim: string, annotated: string | undefined): string {
  return annotated === undefined ? crumbleUrl(stim) : crumbleAnnotatedUrl(annotated, false);
}

/** The longest URL this will emit, in characters.
 *
 *  Not a qubit count. The old `crumble_url` column was blanked past 40 qubits,
 *  which denied a working link to every 144-qubit circuit in the library while
 *  saying nothing about the one number that matters — how long the string
 *  actually comes out. Measuring the string keeps those links (a 144-qubit
 *  syndrome round derives to ~8 KB) and refuses only the ones no browser will
 *  open: a 2688-qubit schedule derives to 232 KB plain and 782 KB with
 *  detectors, which is both an unusable link and, server-rendered into an
 *  `href`, exactly the page bloat this change removes elsewhere.
 *
 *  65,536 is the narrowest ceiling among current browsers — Chrome accepts
 *  ~2 MB and Safari ~80 KB, Firefox is the binding constraint at ~64 KB — so a
 *  link that is offered opens everywhere. It costs 22 of 972 circuits their
 *  link, all of them 720 qubits or wider; the gate it replaces cost 275.
 */
export const CRUMBLE_MAX_URL_LENGTH = 65_536;

export interface CrumbleLinks {
  /** Detectors hidden — what the page shows, and what the anchor opens with. */
  plain: string;
  /** Detectors shown. Always the longer of the two. */
  detectors: string;
}

/** Both Crumble views for a circuit, or null when either is too long to open.
 *
 *  Gated on the pair rather than on each separately: the Detectors switch has to
 *  be able to repoint the link, and an anchor that works until you press a
 *  button is worse than one that was never offered. Two circuits (#1215, #1216,
 *  720 qubits) are refused on the detectors view alone.
 */
export function crumbleLinks(stim: string, annotated: string | undefined): CrumbleLinks | null {
  const plain = crumbleHref(stim, annotated);
  const detectors = annotated === undefined ? plain : crumbleAnnotatedUrl(annotated, true);
  if (plain.length > CRUMBLE_MAX_URL_LENGTH) return null;
  if (detectors.length > CRUMBLE_MAX_URL_LENGTH) return null;
  return { plain, detectors };
}
