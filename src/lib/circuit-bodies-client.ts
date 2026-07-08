// Lazy-loads circuit bodies on code pages. Circuit rows render without any
// circuit text; on the first expand of a row (signalled by the
// `circuit-expand` CustomEvent dispatched in CircuitRow.astro) this module
// fetches /api/circuits/<qec_id>/bodies, clones #circuit-bodies-template and
// fills in tabs + line-numbered bodies. Mirrors the CodeMatrices lazy-load
// pattern: fetch-once guard, error text, retry on next expand.

import { copyToClipboard } from "./dom-helpers";
import { initFormatSwitchers } from "./format-switcher-client";
import { TAB_ACTIVE_CLASS, TAB_INACTIVE_CLASS } from "./constants";

interface BodyEntry {
  format: string;
  body: string;
}

// Keep in sync with FormatSwitcher.astro / format-switcher-client.ts.
const TAB_BASE_CLASS =
  "format-tab px-3 py-1.5 text-xs font-semibold rounded-md cursor-pointer transition-colors";

const loaded = new WeakSet<HTMLElement>();

/** Same line-number gutter format as CodeBlock.astro. */
function lineNumbered(code: string): string {
  const lines = code.trimEnd().split("\n");
  const gutterWidth = String(lines.length).length;
  return lines.map((line, i) => `${String(i + 1).padStart(gutterWidth, " ")}  ${line}`).join("\n");
}

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

  bodies.forEach(function (entry, i) {
    const raw = entry.body.trimEnd();

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
    tabBar.appendChild(tab);

    const bodyEl = bodyProto.cloneNode(true) as HTMLElement;
    bodyEl.dataset.format = entry.format;
    if (i !== 0) bodyEl.style.display = "none";
    const blockLabel = bodyEl.querySelector<HTMLElement>(".block-label");
    if (blockLabel) blockLabel.textContent = `${entry.format.toUpperCase()} Circuit`;
    const codeEl = bodyEl.querySelector<HTMLElement>("pre code");
    if (codeEl) codeEl.textContent = lineNumbered(entry.body);

    const downloadBtn = bodyEl.querySelector<HTMLElement>(".download-btn");
    if (downloadBtn) {
      const downloadName = stimFilename ? stimFilename.replace(/\.stim$/, `.${entry.format}`) : "";
      if (downloadName) {
        downloadBtn.title = `Download ${downloadName} (d)`;
        downloadBtn.addEventListener("click", function () {
          const blob = new Blob([raw], { type: "text/plain" });
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

    const copyBtn = bodyEl.querySelector<HTMLElement>(".copy-btn");
    if (copyBtn) {
      copyBtn.addEventListener("click", async function () {
        const ok = await copyToClipboard(raw);
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

  // Match FormatSwitcher.astro: no tab bar for single-format circuits.
  if (bodies.length < 2) tabBar.remove();

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
  } catch {
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
