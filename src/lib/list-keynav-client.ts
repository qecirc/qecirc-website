// Generic keyboard navigation for listing pages. Each listing page (homepage,
// code detail, favorites) calls initListKeynav with a per-page config that
// describes which child elements to click for Enter / expand / favorite.
//
// Action shape: every binding is "find the matching child of the focused row
// and click it". This intentionally reuses the existing click handlers so
// expand/collapse, favorite, and link navigation all behave exactly as they
// do for mouse users. No logic is duplicated.

export interface ListKeynavConfig {
  // CSS selector for the focusable rows in the list.
  rowSelector: string;
  // Selector inside a row for Enter to "click" — typically a link to the
  // detail page. Optional; if omitted Enter is a no-op.
  enterSelector?: string;
  // If true, l / Right expand and h / Left collapse the focused row.
  expandable?: boolean;
  // When `expandable`: clicking the row itself toggles (e.g. CircuitRow's
  // `.circuit-toggle` handles its own click). Otherwise, expandSelector
  // names a child element to click.
  expandSelfClick?: boolean;
  expandSelector?: string;
  // Attribute on the row that reflects expansion state. Default: aria-expanded.
  expandedAttr?: string;
  // If true, f triggers a click on `favoriteSelector` inside the focused row.
  favoritable?: boolean;
  favoriteSelector?: string;
  // Optional page-level "favorites filter" button — Shift+F clicks it.
  favoriteFilterSelector?: string;
  // Attribute on the row used to match the URL fragment for initial focus
  // (so /codes/foo#42 focuses the row whose [hashAttr] === "42").
  // Default: "id".
  hashAttr?: string;
}

function isInputFocused(): boolean {
  const a = document.activeElement;
  return (
    a instanceof HTMLInputElement ||
    a instanceof HTMLTextAreaElement ||
    a instanceof HTMLSelectElement ||
    (a instanceof HTMLElement && a.isContentEditable)
  );
}

export function initListKeynav(config: ListKeynavConfig): () => void {
  const expandedAttr = config.expandedAttr ?? "aria-expanded";
  const hashAttr = config.hashAttr ?? "id";

  const getRows = () => Array.from(document.querySelectorAll<HTMLElement>(config.rowSelector));

  // Initial focus — defer to next frame so any same-tick scripts (like
  // CircuitRow's expandFromHash) can run first. Hash match wins over first-row.
  requestAnimationFrame(() => {
    const rows = getRows();
    if (rows.length === 0) return;
    const hash = location.hash.slice(1);
    const target = (hash && rows.find((r) => r.getAttribute(hashAttr) === hash)) || rows[0];
    target.focus({ preventScroll: true });
  });

  function focusedIndex(rows: HTMLElement[]): number {
    const a = document.activeElement;
    if (!(a instanceof HTMLElement)) return -1;
    return rows.findIndex((r) => r === a || r.contains(a));
  }

  function focusAt(rows: HTMLElement[], idx: number) {
    if (idx < 0 || idx >= rows.length) return;
    rows[idx].focus({ preventScroll: true });
    rows[idx].scrollIntoView({ block: "nearest" });
  }

  function clickChild(row: HTMLElement, selector: string | undefined) {
    if (!selector) return;
    row.querySelector<HTMLElement>(selector)?.click();
  }

  function toggleExpand(row: HTMLElement) {
    if (config.expandSelfClick) row.click();
    else clickChild(row, config.expandSelector);
  }

  function isExpanded(row: HTMLElement): boolean {
    return row.getAttribute(expandedAttr) === "true";
  }

  // Tracks last 'g' for the vim 'gg' (jump to first) two-key sequence.
  let lastGTime = 0;
  const GG_TIMEOUT_MS = 500;

  function onKeydown(e: KeyboardEvent) {
    if (isInputFocused()) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;

    const rows = getRows();
    if (rows.length === 0) return;
    const idx = focusedIndex(rows);

    // Caps Lock produces uppercase keys without Shift. Without this
    // normalisation, capslock + d/f/g would falsely trigger Shift+D/F/G.
    let key = e.key;
    if (key.length === 1 && !e.shiftKey && key.toLowerCase() !== key) {
      key = key.toLowerCase();
    }

    // Action keys must only fire when the row itself is focused — otherwise
    // pressing Space/Enter on a focused child button or link (favorite,
    // tag, permalink) would override its native behaviour.
    const rowDirectlyFocused = idx >= 0 && document.activeElement === rows[idx];

    // The vim 'gg' two-key sequence: any key other than 'g' must reset the
    // pending state, otherwise `g`, j, g (within 500 ms) would still teleport
    // to the first row mid-navigation.
    if (key !== "g") lastGTime = 0;

    switch (key) {
      case "j":
      case "ArrowDown":
        e.preventDefault();
        focusAt(rows, idx < 0 ? 0 : Math.min(idx + 1, rows.length - 1));
        break;
      case "k":
      case "ArrowUp":
        e.preventDefault();
        focusAt(rows, idx < 0 ? rows.length - 1 : Math.max(idx - 1, 0));
        break;
      case "Home":
        e.preventDefault();
        focusAt(rows, 0);
        break;
      case "End":
      case "G":
        e.preventDefault();
        focusAt(rows, rows.length - 1);
        break;
      case "g": {
        e.preventDefault();
        const now = Date.now();
        if (now - lastGTime < GG_TIMEOUT_MS) {
          focusAt(rows, 0);
          lastGTime = 0;
        } else {
          lastGTime = now;
        }
        break;
      }
      case "Enter":
        if (idx < 0 || !rowDirectlyFocused) return;
        e.preventDefault();
        clickChild(rows[idx], config.enterSelector);
        break;
      case "l":
      case "ArrowRight":
      case " ":
        if (!config.expandable || idx < 0 || !rowDirectlyFocused) return;
        e.preventDefault();
        toggleExpand(rows[idx]);
        break;
      case "h":
      case "ArrowLeft":
        if (!config.expandable || idx < 0 || !rowDirectlyFocused) return;
        if (isExpanded(rows[idx])) {
          e.preventDefault();
          toggleExpand(rows[idx]);
        }
        break;
      case "Escape":
        if (!config.expandable || idx < 0) return;
        if (isExpanded(rows[idx])) {
          e.preventDefault();
          toggleExpand(rows[idx]);
        }
        break;
      case "f":
        if (!config.favoritable || idx < 0 || !rowDirectlyFocused) return;
        e.preventDefault();
        clickChild(rows[idx], config.favoriteSelector);
        break;
      case "F": {
        if (!e.shiftKey || !config.favoriteFilterSelector) return;
        const btn = document.querySelector<HTMLElement>(config.favoriteFilterSelector);
        if (btn) {
          e.preventDefault();
          btn.click();
        }
        break;
      }
    }
  }

  document.addEventListener("keydown", onKeydown);
  return () => document.removeEventListener("keydown", onKeydown);
}
