// Wires the switches that control how a circuit body is displayed: "Coords"
// (show/hide QUBIT_COORDS) and "Detectors" (swap in the annotated body, which
// carries the reset prologue, terminal readout and derived detectors).
//
// One module rather than one per switch: both derive the *same* rendered text
// from the same block, so they have to share a single view state. Two
// independent togglers would each overwrite the other's output.
//
// The switches live in the format-tab row, so they are not descendants of the
// block they control. Both live inside a *scope*: a `.format-switcher`, or a
// `[data-coords-scope]` wrapper when a block is rendered without format tabs
// (e.g. the original submission on a circuit detail page).
//
// The block owns the full bodies in `data-raw-code` / `data-annotated-code`;
// what is on screen is derived from them. Copy and download read the copy
// button's `data-code`, so keeping that in sync is what makes them follow the
// switches rather than silently handing over something different from what is
// displayed.

import { bodyForDisplay, hasQubitCoords, lineNumbered } from "./stim-format";
import { TAB_ACTIVE_CLASS, TAB_INACTIVE_CLASS } from "./constants";

const ACTIVE = TAB_ACTIVE_CLASS.split(" ");
const INACTIVE = TAB_INACTIVE_CLASS.split(" ");

const TITLES = {
  coords: { on: "Hide qubit coordinates", off: "Show qubit coordinates" },
  detectors: { on: "Hide detectors and readout", off: "Show detectors and readout" },
};

interface View {
  coords: boolean;
  detectors: boolean;
}

function setSwitch(btn: HTMLElement | null, on: boolean, kind: "coords" | "detectors"): void {
  if (!btn) return;
  btn.setAttribute("aria-checked", String(on));
  btn.title = on ? TITLES[kind].on : TITLES[kind].off;
  btn.classList.remove(...(on ? INACTIVE : ACTIVE));
  btn.classList.add(...(on ? ACTIVE : INACTIVE));
  btn.querySelector(`.${kind}-on`)?.classList.toggle("hidden", !on);
  btn.querySelector(`.${kind}-off`)?.classList.toggle("hidden", on);
}

/** The Crumble link for this switcher's circuit, or null.
 *
 *  The link lives outside the switcher (it is in the circuit's links row), so it
 *  is reached through the nearest `[data-circuit-scope]` — the wrapper each
 *  circuit row provides. Circuit *detail* pages render a single circuit with no
 *  row wrapper, so they fall back to the document, but only when that is
 *  unambiguous: several links and no scope means a wrapper is missing, and
 *  silently repointing another circuit's link is worse than doing nothing.
 */
function crumbleLink(scope: HTMLElement): HTMLAnchorElement | null {
  const row = scope.closest<HTMLElement>("[data-circuit-scope]");
  if (row) return row.querySelector<HTMLAnchorElement>("[data-crumble-link]");
  const all = document.querySelectorAll<HTMLAnchorElement>("[data-crumble-link]");
  return all.length === 1 ? all[0] : null;
}

/** Point the Crumble link at the body currently on screen. Left alone when the
 *  circuit has no annotated URL — past ~40 qubits there is no Crumble link at
 *  all. */
function paintCrumble(scope: HTMLElement, detectors: boolean): void {
  const link = crumbleLink(scope);
  if (!link) return;
  const plain = link.dataset.crumbleUrl;
  const annotated = link.dataset.crumbleUrlAnnotated;
  if (!plain || !annotated) return;
  link.href = detectors ? annotated : plain;
}

function paint(
  scope: HTMLElement,
  block: HTMLElement,
  canonical: string,
  annotated: string | undefined,
  view: View,
): void {
  const raw = view.detectors && annotated ? annotated : canonical;
  const shown = bodyForDisplay(raw, view.coords);

  const codeEl = block.querySelector<HTMLElement>("pre code");
  if (codeEl) codeEl.textContent = lineNumbered(shown);

  // Copy and download both source from here (see CodeBlock.astro's download
  // handler), so this one assignment keeps all three consistent.
  const copyBtn = block.querySelector<HTMLElement>(".copy-btn");
  if (copyBtn) copyBtn.dataset.code = shown;

  setSwitch(scope.querySelector<HTMLElement>(".coords-btn"), view.coords, "coords");
  setSwitch(scope.querySelector<HTMLElement>(".detectors-btn"), view.detectors, "detectors");
  paintCrumble(scope, view.detectors);
}

/**
 * Enable the body-view switches inside `scope`. Each switch is removed when it
 * would do nothing — most circuits have no coordinates and no annotated body,
 * and a dead control is worse than none.
 */
export function initBodyView(scope: HTMLElement): void {
  // Guard here rather than in the caller: circuit-bodies-client calls this
  // directly on a freshly cloned switcher, so a later initBodyViews() sweep
  // would otherwise wire a second click listener onto the same button.
  if (scope.dataset.bodyViewInit !== undefined) return;
  scope.dataset.bodyViewInit = "";

  const coordsBtn = scope.querySelector<HTMLElement>(".coords-btn");
  const detectorsBtn = scope.querySelector<HTMLElement>(".detectors-btn");
  if (!coordsBtn && !detectorsBtn) return;

  const block = scope.querySelector<HTMLElement>("[data-code-block][data-raw-code]");
  const canonical = block?.dataset.rawCode;
  if (!block || !canonical) {
    coordsBtn?.remove();
    detectorsBtn?.remove();
    return;
  }
  const annotated = block.dataset.annotatedCode;

  // Coordinates can live in either body, so ask both before dropping the switch.
  if (!hasQubitCoords(canonical) && !(annotated && hasQubitCoords(annotated))) {
    coordsBtn?.remove();
  }
  if (!annotated) detectorsBtn?.remove();

  const view: View = { coords: false, detectors: false };
  paint(scope, block, canonical, annotated, view);

  scope.querySelector<HTMLElement>(".coords-btn")?.addEventListener("click", function () {
    view.coords = !view.coords;
    paint(scope, block, canonical, annotated, view);
  });
  scope.querySelector<HTMLElement>(".detectors-btn")?.addEventListener("click", function () {
    view.detectors = !view.detectors;
    paint(scope, block, canonical, annotated, view);
  });
}

/** Initialise every not-yet-wired scope under `root`. Safe to call repeatedly:
 *  initBodyView guards each scope. */
export function initBodyViews(root: ParentNode = document): void {
  root.querySelectorAll<HTMLElement>(".format-switcher, [data-coords-scope]").forEach(initBodyView);
}
