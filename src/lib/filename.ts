/** Build a download filename for a circuit's .stim body. */
export function buildStimFilename(meta: {
  codeSlug: string;
  circuitSlug: string;
  gateCount?: number | null;
  twoQubitGateCount?: number | null;
  depth?: number | null;
  qubitCount?: number | null;
}): string {
  const parts = [meta.codeSlug, meta.circuitSlug];
  if (meta.gateCount != null) parts.push(`G${meta.gateCount}`);
  if (meta.twoQubitGateCount != null) parts.push(`2Q${meta.twoQubitGateCount}`);
  if (meta.depth != null) parts.push(`D${meta.depth}`);
  if (meta.qubitCount != null) parts.push(`Q${meta.qubitCount}`);
  return parts.join("_") + ".stim";
}
