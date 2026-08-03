import { safeStorage, StorageBlockedError } from "./safe-storage";

// Reads degrade quietly (no favourites is a valid answer); writes do not. A
// write that vanishes here is the user's own list, and a caller that assumes
// it landed will report a success that did not happen — so every write throws
// StorageBlockedError instead of returning as if it had worked.

const STORAGE_KEY = "qecirc-favorites";

/**
 * Say it here, not at each call site: the hearts in `CircuitRow.astro` have no
 * error path of their own, and a silent no-op there is exactly the lie this is
 * meant to prevent. Precedent for a lib module reaching for the toast is
 * `src/lib/cite-client.ts`.
 */
function toastStorageBlocked(): void {
  if (typeof window !== "undefined" && typeof window.showCiteToast === "function") {
    window.showCiteToast("Couldn't update favorites — this browser is blocking site storage.");
  }
}

export function getFavorites(): number[] {
  try {
    const raw = safeStorage.getItem(STORAGE_KEY);
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

/**
 * Toggle a circuit's favorite status. Returns `true` if now favorited.
 *
 * Toasts and throws `StorageBlockedError` if the new list could not be stored —
 * the caller must not fill in a heart for something that was never saved.
 */
export function toggleFavorite(qecId: number): boolean {
  const favs = getFavorites();
  const idx = favs.indexOf(qecId);
  if (idx === -1) {
    favs.push(qecId);
  } else {
    favs.splice(idx, 1);
  }
  if (!safeStorage.setItem(STORAGE_KEY, JSON.stringify(favs))) {
    toastStorageBlocked();
    throw new StorageBlockedError();
  }
  return idx === -1;
}

/** Export favorites as a JSON string. */
export function exportFavorites(): string {
  return JSON.stringify({ favorites: getFavorites() });
}

const MAX_IMPORT_SIZE = 100_000; // 100 KB max file size
const MAX_FAVORITES = 5_000; // cap total favorites

/**
 * Import favorites from a JSON string. Merges with existing. Returns count of
 * newly added IDs.
 *
 * The count is computed from an in-memory Set, so it describes an import that
 * has not been persisted yet: throws `StorageBlockedError` when the write is
 * refused, rather than reporting "Imported 3" for a list that is still empty.
 */
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
  if (!safeStorage.setItem(STORAGE_KEY, JSON.stringify([...existing])))
    throw new StorageBlockedError();
  return existing.size - before;
}
