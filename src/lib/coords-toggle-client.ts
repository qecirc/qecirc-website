// Wires the "Coords" switch that shows/hides QUBIT_COORDS on a circuit body.
//
// The switch lives in the format-tab row, so it is not a descendant of the code
// block it controls. Both live inside a *scope*: a `.format-switcher`, or a
// `[data-coords-scope]` wrapper when a block is rendered without format tabs
// (e.g. the original submission on a circuit detail page).
//
// The block owns the full body in `data-raw-code`; what is on screen is derived
// from it. Copy and download read the copy button's `data-code`, so keeping that
// in sync is what makes them follow the switch rather than silently handing over
// something different from what is displayed.

import { bodyForDisplay, lineNumbered } from "./stim-format";
import { TAB_ACTIVE_CLASS, TAB_INACTIVE_CLASS } from "./constants";

const SHOW_TITLE = "Show qubit coordinates";
const HIDE_TITLE = "Hide qubit coordinates";

const ACTIVE = TAB_ACTIVE_CLASS.split(" ");
const INACTIVE = TAB_INACTIVE_CLASS.split(" ");

function paint(block: HTMLElement, btn: HTMLElement, raw: string, showCoords: boolean): void {
  const shown = bodyForDisplay(raw, showCoords);

  const codeEl = block.querySelector<HTMLElement>("pre code");
  if (codeEl) codeEl.textContent = lineNumbered(shown);

  // Copy and download both source from here (see CodeBlock.astro's download
  // handler), so this one assignment keeps all three consistent.
  const copyBtn = block.querySelector<HTMLElement>(".copy-btn");
  if (copyBtn) copyBtn.dataset.code = shown;

  btn.setAttribute("aria-checked", String(showCoords));
  btn.title = showCoords ? HIDE_TITLE : SHOW_TITLE;
  btn.classList.remove(...(showCoords ? INACTIVE : ACTIVE));
  btn.classList.add(...(showCoords ? ACTIVE : INACTIVE));
  btn.querySelector(".coords-on")?.classList.toggle("hidden", !showCoords);
  btn.querySelector(".coords-off")?.classList.toggle("hidden", showCoords);
}

/**
 * Enable the coords switch inside `scope`. Removes it when no body in the scope
 * has coordinates — most circuits have none, and only STIM ever carries them
 * (the QASM/CIRQ conversions do not), so a dead control is worse than none.
 */
export function initCoordsToggle(scope: HTMLElement): void {
  // Guard here rather than in the caller: circuit-bodies-client calls this
  // directly on a freshly cloned switcher, so a later initCoordsToggles() sweep
  // would otherwise wire a second click listener onto the same button.
  if (scope.dataset.coordsInit !== undefined) return;
  scope.dataset.coordsInit = "";

  const btn = scope.querySelector<HTMLElement>(".coords-btn");
  if (!btn) return;

  const block = scope.querySelector<HTMLElement>("[data-code-block][data-raw-code]");
  const raw = block?.dataset.rawCode;
  if (!block || !raw) {
    btn.remove();
    return;
  }

  let showCoords = false;
  paint(block, btn, raw, showCoords);

  btn.addEventListener("click", function () {
    showCoords = !showCoords;
    paint(block, btn, raw, showCoords);
  });
}

/** Initialise every not-yet-wired scope under `root`. Safe to call repeatedly:
 *  initCoordsToggle guards each scope. */
export function initCoordsToggles(root: ParentNode = document): void {
  root
    .querySelectorAll<HTMLElement>(".format-switcher, [data-coords-scope]")
    .forEach(initCoordsToggle);
}
