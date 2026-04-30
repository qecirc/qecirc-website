/**
 * Shared DOM utilities for client-side scripts.
 */

/** True if focus is on a text-input-like element where keyboard shortcuts should not fire. */
export function isInputFocused(): boolean {
  const el = document.activeElement;
  if (!el) return false;
  const tag = el.tagName;
  if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return true;
  return (el as HTMLElement).isContentEditable === true;
}

/** Apply the visual "favourite" state to a heart-icon toggle button. */
export function setFavState(btn: HTMLElement, isFav: boolean): void {
  const outline = btn.querySelector<HTMLElement>(".fav-outline");
  const filled = btn.querySelector<HTMLElement>(".fav-filled");
  if (outline) outline.classList.toggle("hidden", isFav);
  if (filled) filled.classList.toggle("hidden", !isFav);
  btn.classList.toggle("text-red-400", isFav);
  btn.classList.toggle("dark:text-red-400", isFav);
  btn.classList.toggle("text-gray-300", !isFav);
  btn.classList.toggle("dark:text-gray-600", !isFav);
}

/**
 * Copy `text` to clipboard. Returns boolean indicating success.
 * Awaits the clipboard write so callers can drive UI off the actual outcome.
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  if (!navigator.clipboard) return false;
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    return false;
  }
}
