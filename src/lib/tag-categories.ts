/**
 * Grouping of circuit tags into the categories shown as dropdown fields in
 * the circuit filter. Prefix rules (`key:value` tags) keep this maintenance
 * free for new values; only genuinely new free-form tags may need a new entry.
 */

export type TagCategoryKey = "type" | "ft" | "hardware" | "method" | "tools" | "other";

export const TAG_CATEGORIES: readonly { key: TagCategoryKey; label: string }[] = [
  { key: "type", label: "Type" },
  { key: "ft", label: "Fault tolerance" },
  { key: "hardware", label: "Hardware" },
  { key: "method", label: "Method" },
  { key: "tools", label: "Tools" },
  { key: "other", label: "Other" },
];

const TYPE_TAGS = new Set(["encoding", "state-preparation", "syndrome-extraction"]);
const FT_TAGS = new Set(["ft", "non-ft", "flag", "deterministic"]);
const HARDWARE_TAGS = new Set(["1D-AOD"]);

export function categorizeTag(name: string): TagCategoryKey {
  if (TYPE_TAGS.has(name) || name.startsWith("logical-state:")) return "type";
  // `distance:N` is a fault-tolerance property (a circuit/gadget FT to distance N).
  // `circuit-distance:N` is the measured one — a different number, the same
  // question — so it belongs beside it rather than in "Other".
  if (FT_TAGS.has(name) || name.startsWith("distance:") || name.startsWith("circuit-distance:"))
    return "ft";
  if (HARDWARE_TAGS.has(name) || name.startsWith("connectivity:") || name.startsWith("device:"))
    return "hardware";
  // `schedule:` and `decoder:` describe how a syndrome-extraction round was
  // produced. They pair up: a schedule found by search is co-designed with the
  // decoder it was scored against, so two rounds for one code can differ only
  // by `decoder:`.
  if (
    name.startsWith("prep:") ||
    name.startsWith("verification:") ||
    name.startsWith("schedule:") ||
    name.startsWith("decoder:")
  )
    return "method";
  // `tool:<slug>` tags are derived from each circuit's tool at DB-build time.
  if (name.startsWith("tool:")) return "tools";
  return "other";
}

// --- code tags ---------------------------------------------------------------

export type CodeTagCategoryKey = "family" | "properties";

export const CODE_TAG_CATEGORIES: readonly { key: CodeTagCategoryKey; label: string }[] = [
  { key: "family", label: "Code family" },
  { key: "properties", label: "Properties" },
];

// Family tags conventionally end in "-code"; the set covers the exceptions.
const FAMILY_TAGS = new Set(["LDPC", "topological", "bosonic"]);

export function categorizeCodeTag(name: string): CodeTagCategoryKey {
  if (name.endsWith("-code") || FAMILY_TAGS.has(name)) return "family";
  return "properties";
}
