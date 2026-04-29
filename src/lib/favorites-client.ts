const STORAGE_KEY = "qecirc-favorites";

export function getFavorites(): number[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter((v): v is number => typeof v === "number" && Number.isInteger(v));
  } catch {
    return [];
  }
}

export function isFavorite(qecId: number): boolean {
  return getFavorites().includes(qecId);
}

/** Toggle a circuit's favorite status. Returns `true` if now favorited. */
export function toggleFavorite(qecId: number): boolean {
  const favs = getFavorites();
  const idx = favs.indexOf(qecId);
  if (idx === -1) {
    favs.push(qecId);
  } else {
    favs.splice(idx, 1);
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(favs));
  return idx === -1;
}

/** Export favorites as a JSON string. */
export function exportFavorites(): string {
  return JSON.stringify({ favorites: getFavorites() });
}

const MAX_IMPORT_SIZE = 100_000; // 100 KB max file size
const MAX_FAVORITES = 5_000; // cap total favorites

/** Import favorites from a JSON string. Merges with existing. Returns count of newly added IDs. */
export function importFavorites(json: string): number {
  if (json.length > MAX_IMPORT_SIZE) throw new Error("File too large");
  const parsed = JSON.parse(json);
  if (typeof parsed !== "object" || parsed === null || !Array.isArray(parsed.favorites))
    throw new Error("Invalid format");
  if (Object.keys(parsed).length !== 1) throw new Error("Unexpected fields in file");
  const valid = parsed.favorites.filter(
    (v: unknown): v is number => typeof v === "number" && Number.isInteger(v) && v > 0,
  );
  const existing = new Set(getFavorites());
  const before = existing.size;
  for (const id of valid) {
    if (existing.size >= MAX_FAVORITES) break;
    existing.add(id);
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify([...existing]));
  return existing.size - before;
}
