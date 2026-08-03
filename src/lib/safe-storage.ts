/**
 * `localStorage` that cannot throw.
 *
 * Where storage is denied — Chrome's "block all cookies", some embedded
 * webviews, a full quota — *every* access throws a `SecurityError`, reads
 * included. Unguarded, one preference lookup aborts the rest of the module it
 * sits in: the favourites-filter read on a code page sits above the
 * "download all" wiring, so a browser that refuses storage lost the download
 * button too. A missing preference is not an error, so both calls degrade to
 * "nothing stored" rather than propagating.
 *
 * **A write is not silent, though: `setItem` reports whether it landed.** A
 * dropped preference (theme, tag view) is a shrug; a dropped *favourite* is
 * data the user thinks they saved. Any caller whose next act is to claim
 * success must check the return value — see `favorites-client.ts`, which turns
 * `false` into `StorageBlockedError` rather than reporting an import that
 * never happened.
 *
 * The two `is:inline` scripts (the theme in Layout.astro, the filter disclosure
 * in search.astro) cannot import a module and inline the same try/catch.
 */
export const safeStorage = {
  /** The stored value, or `null` if absent *or* unreadable. */
  getItem(key: string): string | null {
    try {
      return localStorage.getItem(key);
    } catch {
      return null;
    }
  },

  /** Persist a value. Returns `false` if storage refused it; never throws. */
  setItem(key: string, value: string): boolean {
    try {
      localStorage.setItem(key, value);
      return true;
    } catch {
      // Storage denied or full. The caller decides whether that is worth
      // saying out loud.
      return false;
    }
  },
};

/** Thrown by a write whose failure the user has to be told about. */
export class StorageBlockedError extends Error {
  constructor() {
    super("Browser storage is blocked, so nothing could be saved.");
    this.name = "StorageBlockedError";
  }
}
