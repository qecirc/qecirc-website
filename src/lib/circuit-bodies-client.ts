// Lazy-loads circuit bodies on code pages. Circuit rows render without any
// circuit text; on the first expand of a row (signalled by the
// `circuit-expand` CustomEvent dispatched in CircuitRow.astro) this module
// fetches /api/circuits/<qec_id>/bodies, clones #circuit-bodies-template and
// fills in tabs + line-numbered bodies. Mirrors the CodeMatrices lazy-load
// pattern: fetch-once guard, error text, retry on next expand.

import { copyToClipboard } from "./dom-helpers";
import { initFormatSwitchers } from "./format-switcher-client";
import { initBodyView } from "./body-view-client";
import {
  ANNOTATED_OF,
  bodyForDisplay,
  hasQubitCoords,
  lineNumbered,
  splitAnnotated,
} from "./stim-format";
import { TAB_ACTIVE_CLASS, TAB_INACTIVE_CLASS } from "./constants";

interface BodyEntry {
  format: string;
  body: string;
}

// Keep in sync with FormatSwitcher.astro / format-switcher-client.ts.
const TAB_BASE_CLASS =
  "format-tab px-3 py-1.5 text-xs font-semibold rounded-md cursor-pointer transition-colors";

const loaded = new WeakSet<HTMLElement>();

/** Same cite-toast behavior as CodeBlock.astro's copy/download handlers. */
function citeNotice(source: string): void {
  if (typeof window.showCiteToast !== "function") return;
  if (source && source.startsWith("http")) {
    window.showCiteToast("Please cite the source when using this circuit:", source);
  } else if (source) {
    window.showCiteToast("Please cite the source when using this circuit: " + source);
  } else {
    window.showCiteToast("Please check and cite the corresponding source when using this circuit.");
  }
}

function buildSwitcher(
  container: HTMLElement,
  template: HTMLTemplateElement,
  bodies: BodyEntry[],
): void {
  const fragment = template.content.cloneNode(true) as DocumentFragment;
  const switcher = fragment.querySelector<HTMLElement>(".format-switcher");
  const tabBar = switcher?.querySelector<HTMLElement>(".format-tabs");
  const tabProto = tabBar?.querySelector<HTMLElement>(".format-tab");
  const bodyProto = switcher?.querySelector<HTMLElement>(".format-body");
  if (!switcher || !tabBar || !tabProto || !bodyProto) return;
  tabProto.remove();
  bodyProto.remove();

  const stimFilename = container.dataset.stimFilename ?? "";
  const source = container.dataset.source ?? "";

  // The annotated body is a view of the STIM body, not a format of its own, so
  // it gets no tab; it supersedes the plain STIM body for display. Mirrors
  // FormatSwitcher.astro, which resolves this server-side.
  const { tabs, annotated } = splitAnnotated(bodies);

  // Only STIM carries coordinates or an annotated variant, so at most one body
  // per switcher owns the switches.
  let coordsSlot = tabBar.querySelector<HTMLElement>(".coords-slot");
  const switchFormat =
    tabs.find((b) => hasQubitCoords(annotated && b.format === ANNOTATED_OF ? annotated : b.body))
      ?.format ?? (annotated ? ANNOTATED_OF : undefined);
  if (switchFormat) {
    switcher.dataset.coordsFormat = switchFormat;
  } else {
    coordsSlot?.remove();
    // Must be nulled, not just detached: it is the insertBefore() reference
    // below, and a detached reference node throws NotFoundError.
    coordsSlot = null;
  }

  tabs.forEach(function (entry, i) {
    const raw = entry.body.trimEnd();
    // The annotated body supersedes the plain STIM one for display: same circuit
    // with the |0...0> input stated explicitly, plus a readout the Detectors
    // switch subtracts. Both switches derive from this one superset.
    const display = entry.format === ANNOTATED_OF && annotated ? annotated : raw;

    const tab = tabProto.cloneNode(true) as HTMLElement;
    tab.className = `${TAB_BASE_CLASS} ${i === 0 ? TAB_ACTIVE_CLASS : TAB_INACTIVE_CLASS}`;
    tab.dataset.format = entry.format;
    tab.title = `Switch to ${entry.format.toUpperCase()} (${i + 1})`;
    const tabLabel = tab.querySelector<HTMLElement>(".tab-label");
    if (tabLabel) tabLabel.textContent = entry.format.toUpperCase();
    const kbd = tab.querySelector<HTMLElement>("kbd");
    if (kbd) {
      if (i < 3) kbd.textContent = String(i + 1);
      else kbd.remove();
    }
    // The coords slot sits after the tab prototype in the template, so tabs
    // must go before it to keep the row reading [STIM][QASM][CIRQ] … [Coords].
    if (coordsSlot) tabBar.insertBefore(tab, coordsSlot);
    else tabBar.appendChild(tab);

    const bodyEl = bodyProto.cloneNode(true) as HTMLElement;
    bodyEl.dataset.format = entry.format;
    if (i !== 0) bodyEl.style.display = "none";
    const blockLabel = bodyEl.querySelector<HTMLElement>(".block-label");
    if (blockLabel) blockLabel.textContent = `${entry.format.toUpperCase()} Circuit`;

    // Seed the default view (coordinates and detectors hidden); initBodyView
    // repaints it once the whole switcher is assembled. Copy and download read
    // the copy button's data-code rather than `raw`, so they follow what is on
    // screen.
    const shown = bodyForDisplay(display, false, false);
    const codeEl = bodyEl.querySelector<HTMLElement>("pre code");
    if (codeEl) codeEl.textContent = lineNumbered(shown);
    const copyBtn = bodyEl.querySelector<HTMLElement>(".copy-btn");
    if (copyBtn) copyBtn.dataset.code = shown;

    const block = bodyEl.querySelector<HTMLElement>("[data-code-block]");
    // The switches subtract from the full body, so hand it over whenever either
    // switch is live on this format.
    if (block && entry.format === switchFormat) block.dataset.rawCode = display;

    const downloadBtn = bodyEl.querySelector<HTMLElement>(".download-btn");
    if (downloadBtn) {
      const downloadName = stimFilename ? stimFilename.replace(/\.stim$/, `.${entry.format}`) : "";
      if (downloadName) {
        downloadBtn.title = `Download ${downloadName} (d)`;
        downloadBtn.addEventListener("click", function () {
          const body = copyBtn?.dataset.code ?? shown;
          const blob = new Blob([body], { type: "text/plain" });
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = downloadName;
          a.click();
          URL.revokeObjectURL(url);
          citeNotice(source);
        });
      } else {
        downloadBtn.remove();
      }
    }

    if (copyBtn) {
      copyBtn.addEventListener("click", async function () {
        const ok = await copyToClipboard(copyBtn.dataset.code ?? shown);
        if (!ok) return;
        const label = copyBtn.querySelector<HTMLElement>(".copy-label");
        if (label) {
          const original = label.textContent;
          label.textContent = "Copied!";
          setTimeout(function () {
            label.textContent = original;
          }, 1500);
        }
        citeNotice(source);
      });
    }

    switcher.appendChild(bodyEl);
  });

  // Match FormatSwitcher.astro: no format tabs for single-format circuits. The
  // row itself stays if it still holds a body switch — the server-rendered
  // equivalent is CodeBlock.astro's lone-switch row.
  if (tabs.length < 2) {
    tabBar.querySelectorAll(".format-tab").forEach(function (t) {
      t.remove();
    });
    if (!switchFormat) tabBar.remove();
  }

  // Drops whichever switches would do nothing for this circuit.
  initBodyView(switcher);
  container.replaceChildren(fragment);
  initFormatSwitchers(container);
}

/** Re-sync the expand animation height after content changes. */
function syncDetailHeight(container: HTMLElement): void {
  const detail = container.closest<HTMLElement>(".circuit-detail");
  if (detail && detail.style.maxHeight !== "0px") {
    detail.style.maxHeight = detail.scrollHeight + "px";
  }
}

async function loadBodies(container: HTMLElement, template: HTMLTemplateElement): Promise<void> {
  if (loaded.has(container)) return;
  loaded.add(container);
  const qecId = container.dataset.qecId;
  if (!qecId) return;
  try {
    const res = await fetch(`/api/circuits/${qecId}/bodies`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = (await res.json()) as { bodies: BodyEntry[] };
    buildSwitcher(container, template, data.bodies);
  } catch (err) {
    // Log it: this catch covers both the fetch and the render, so a render bug
    // otherwise surfaces only as "Failed to load" with no way to tell why.
    console.error(`Circuit bodies failed for #${qecId}:`, err);
    loaded.delete(container); // allow a fresh expand to retry
    const status = container.querySelector<HTMLElement>(".circuit-bodies-status");
    if (status) status.textContent = "Failed to load — collapse and expand to retry.";
  }
  syncDetailHeight(container);
}

export function initCircuitBodies(): void {
  const template = document.getElementById("circuit-bodies-template") as HTMLTemplateElement | null;
  if (!template) return;

  document.addEventListener("circuit-expand", function (e) {
    const detail = e.target as HTMLElement;
    const container = detail.querySelector<HTMLElement>(".circuit-bodies");
    if (container) void loadBodies(container, template);
  });

  // A row may already be expanded before our listener registered: CircuitRow's
  // expandFromHash dispatches circuit-expand during its own module init, and
  // module execution order between component and page scripts isn't
  // guaranteed. Load bodies for any already-expanded row now.
  document
    .querySelectorAll<HTMLElement>('.circuit-toggle[aria-expanded="true"] + .circuit-detail')
    .forEach(function (detail) {
      const container = detail.querySelector<HTMLElement>(".circuit-bodies");
      if (container) void loadBodies(container, template);
    });
}
