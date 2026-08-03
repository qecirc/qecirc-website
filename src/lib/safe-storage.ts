/**
 * `localStorage` that cannot throw.
 *
 * Where storage is denied — Chrome's "block all cookies", some embedded
 * webviews, a full quota — *every* access throws a `SecurityError`, reads
 * included. Unguarded, one preference lookup aborts the rest of the module it
 * sits in: the favourites-filter read on a code page sits above the
 * "download all" wiring, so a browser that refuses storage lost the download
 * button too. A missing preference is not an error, so both calls degrade to
 * "nothing stored" / "not persisted" rather than propagating.
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

  /** Persist a value, silently doing nothing if storage refuses it. */
  setItem(key: string, value: string): void {
    try {
      localStorage.setItem(key, value);
    } catch {
      // Storage denied or full — the preference just does not survive the page.
    }
  },
};
