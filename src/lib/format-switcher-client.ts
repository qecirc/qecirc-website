const ACTIVE_CLASS =
  "format-tab px-3 py-1.5 text-xs font-semibold rounded-md cursor-pointer transition-colors bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 ring-1 ring-inset ring-gray-200 dark:ring-gray-700";
const INACTIVE_CLASS =
  "format-tab px-3 py-1.5 text-xs font-semibold rounded-md cursor-pointer transition-colors text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100";

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
