// Backspace (and `b` as alternate) navigates to a parent page on detail
// pages. Each page that wants this calls initBackKey with the explicit
// parent href; Backspace from a circuit detail goes to its code page,
// from a code page to the homepage. Using an explicit href rather than
// history.back() keeps the destination predictable when a user landed
// on the page via a direct URL.

function isInputFocused(): boolean {
  const a = document.activeElement;
  return (
    a instanceof HTMLInputElement ||
    a instanceof HTMLTextAreaElement ||
    a instanceof HTMLSelectElement ||
    (a instanceof HTMLElement && a.isContentEditable)
  );
}

export function initBackKey(backHref: string): () => void {
  function onKeydown(e: KeyboardEvent) {
    if (isInputFocused()) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.key !== "Backspace" && e.key !== "b") return;
    e.preventDefault();
    location.assign(backHref);
  }
  document.addEventListener("keydown", onKeydown);
  return () => document.removeEventListener("keydown", onKeydown);
}
