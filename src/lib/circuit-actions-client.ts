// Keyboard shortcuts that act on the "active" circuit body on a page:
// - 1 / 2 / 3 switch format tabs (STIM / QASM / CIRQ) inside the active FormatSwitcher.
// - c / y copy the visible circuit body.
// - d download the visible circuit body.
// - D (Shift+d) clicks a page-level "download all" button (e.g. download all
//   visible circuits on a code page, or all favorites).
//
// "Active" depends on context: on a circuit detail page there is exactly one
// body; on a code page (with multiple expandable rows) it is the row whose
// `.circuit-toggle` has `aria-expanded="true"`.
//
// All bindings reuse the existing click handlers on the underlying buttons,
// so no copy/download/format logic is duplicated here.

import { isInputFocused } from "./dom-helpers";

export interface CircuitActionsConfig {
  // Container selector in which to find the active code-block. Omit to
  // disable 1/2/3 + c/y + d (e.g. on `/favorites`, where rows aren't expanded).
  activeContainerSelector?: string;
  // Page-level "download all" button selector. Omit to disable D.
  downloadAllSelector?: string;
  // Page-level "favorite this circuit" button selector — bound to `f`. Used
  // on the circuit detail page where there is no list-keynav handling f.
  favoriteSelector?: string;
}

export function initCircuitActions(config: CircuitActionsConfig): () => void {
  function findActiveContainer(): HTMLElement | null {
    if (!config.activeContainerSelector) return null;
    return document.querySelector<HTMLElement>(config.activeContainerSelector);
  }

  // Resolve the visible code-block: when wrapped in a FormatSwitcher, walk
  // through the `.format-body` whose inline display !== "none"; otherwise
  // the container itself contains a single `[data-code-block]`.
  function findActiveCodeBlock(container: HTMLElement): HTMLElement | null {
    const bodies = container.querySelectorAll<HTMLElement>(".format-body");
    if (bodies.length > 0) {
      for (const body of bodies) {
        if (body.style.display !== "none") {
          return body.querySelector<HTMLElement>("[data-code-block]");
        }
      }
      return null;
    }
    return container.querySelector<HTMLElement>("[data-code-block]");
  }

  function onKeydown(e: KeyboardEvent) {
    if (isInputFocused()) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;

    // Normalise unshifted uppercase (Caps Lock) to lowercase so capslock + d
    // doesn't falsely trigger Shift+D ("download all").
    let key = e.key;
    if (key.length === 1 && !e.shiftKey && key.toLowerCase() !== key) {
      key = key.toLowerCase();
    }

    if (key === "D" && e.shiftKey && config.downloadAllSelector) {
      const btn = document.querySelector<HTMLElement>(config.downloadAllSelector);
      if (btn && !btn.classList.contains("hidden")) {
        e.preventDefault();
        btn.click();
      }
      return;
    }

    if (key === "f" && config.favoriteSelector) {
      const btn = document.querySelector<HTMLElement>(config.favoriteSelector);
      if (btn) {
        e.preventDefault();
        btn.click();
      }
      return;
    }

    const container = findActiveContainer();
    if (!container) return;

    switch (key) {
      case "1":
      case "2":
      case "3": {
        const tabs = container.querySelectorAll<HTMLElement>(".format-tab");
        const idx = Number(e.key) - 1;
        if (tabs[idx]) {
          e.preventDefault();
          tabs[idx].click();
        }
        break;
      }
      case "c":
      case "y": {
        const block = findActiveCodeBlock(container);
        const btn = block?.querySelector<HTMLElement>(".copy-btn");
        if (btn) {
          e.preventDefault();
          btn.click();
        }
        break;
      }
      case "d": {
        const block = findActiveCodeBlock(container);
        const btn = block?.querySelector<HTMLElement>(".download-btn");
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
