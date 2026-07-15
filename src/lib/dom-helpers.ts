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
 * Re-measure the collapse container around `el` after its content changed size.
 *
 * A circuit row animates open by setting an explicit `max-height` on
 * `.circuit-detail`, which pins the height measured at expand time. Anything
 * that then grows the content — switching format, showing coordinates or
 * detectors — overflows that pin and is silently clipped, with no scrollbar to
 * hint at it. So every such change has to re-measure.
 *
 * A collapsed row (`max-height: 0px`) is left alone: it is mid- or
 * post-collapse, and re-pinning it to its content height would spring it open.
 *
 * No-op when `el` is not inside a collapse container — circuit *detail* pages
 * render the body directly in the page flow, where the browser handles it.
 */
export function syncDetailHeight(el: Element): void {
  const detail = el.closest<HTMLElement>(".circuit-detail");
  if (!detail || detail.style.maxHeight === "0px") return;
  // Reading scrollHeight flushes pending layout, so this sees the new content.
  detail.style.maxHeight = detail.scrollHeight + "px";
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
  } catch (err) {
    console.warn("Failed to copy text to clipboard:", err);
    return false;
  }
}
