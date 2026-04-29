import { TAB_ACTIVE_CLASS, TAB_INACTIVE_CLASS } from "./constants";

// `format-tab` is the query selector used to find these buttons; it MUST be
// part of the className we re-apply on toggle, hence it's repeated here.
const BASE_CLASS =
  "format-tab px-3 py-1.5 text-xs font-semibold rounded-md cursor-pointer transition-colors";
const ACTIVE_CLASS = `${BASE_CLASS} ${TAB_ACTIVE_CLASS}`;
const INACTIVE_CLASS = `${BASE_CLASS} ${TAB_INACTIVE_CLASS}`;

export function initFormatSwitchers(root: HTMLElement | Document = document): void {
  root.querySelectorAll(".format-switcher").forEach(function (switcher) {
    const tabs = switcher.querySelectorAll(".format-tab");
    const bodies = switcher.querySelectorAll(".format-body");

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        const format = (tab as HTMLElement).dataset.format;

        tabs.forEach(function (t) {
          (t as HTMLElement).className =
            (t as HTMLElement).dataset.format === format ? ACTIVE_CLASS : INACTIVE_CLASS;
        });

        bodies.forEach(function (b) {
          (b as HTMLElement).style.display =
            (b as HTMLElement).dataset.format === format ? "" : "none";
        });

        // Recalculate max-height for parent collapse container
        const detail = switcher.closest(".circuit-detail") as HTMLElement;
        if (detail && detail.style.maxHeight !== "0px") {
          requestAnimationFrame(function () {
            detail.style.maxHeight = detail.scrollHeight + "px";
          });
        }
      });
    });
  });
}
