/**
 * Grouping of circuit tags into the categories shown as dropdown fields in
 * the circuit filter. Prefix rules (`key:value` tags) keep this maintenance
 * free for new values; only genuinely new free-form tags may need a new entry.
 */

export type TagCategoryKey = "type" | "ft" | "hardware" | "method" | "other";

export const TAG_CATEGORIES: readonly { key: TagCategoryKey; label: string }[] = [
  { key: "type", label: "Type" },
  { key: "ft", label: "Fault tolerance" },
  { key: "hardware", label: "Hardware" },
  { key: "method", label: "Method" },
  { key: "other", label: "Other" },
];

const TYPE_TAGS = new Set(["encoding", "state-preparation", "syndrome-extraction"]);
const FT_TAGS = new Set(["ft", "non-ft", "flag", "deterministic"]);
const HARDWARE_TAGS = new Set(["1D-AOD"]);

export function categorizeTag(name: string): TagCategoryKey {
  if (TYPE_TAGS.has(name) || name.startsWith("logical-state:")) return "type";
  if (FT_TAGS.has(name)) return "ft";
  if (HARDWARE_TAGS.has(name) || name.startsWith("connectivity:") || name.startsWith("device:"))
    return "hardware";
  if (name.startsWith("prep:") || name.startsWith("verification:")) return "method";
  return "other";
}
