/**
 * Behavior for a tag filter block rendered by TagFilterDropdowns.astro:
 * one category dropdown open at a time, close on outside click / Escape, and
 * a persisted toggle between the grouped view and the flat all-tags cloud.
 *
 * The root element configures each instance via data attributes:
 *   data-storage-key   localStorage key for the persisted view choice
 *   data-default-view  "grouped" | "all" — used when nothing is persisted
 */
export function initTagDropdowns(root: HTMLElement): void {
  const dropdowns = Array.from(root.querySelectorAll<HTMLDetailsElement>("[data-tag-dropdown]"));

  dropdowns.forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (!d.open) return;
      dropdowns.forEach(function (other) {
        if (other !== d) other.open = false;
      });
      // Right-align the popover when it would overflow the viewport edge.
      const pop = d.querySelector<HTMLElement>("[data-tag-popover]");
      if (!pop) return;
      pop.classList.remove("right-0");
      pop.classList.add("left-0");
      if (pop.getBoundingClientRect().right > document.documentElement.clientWidth - 8) {
        pop.classList.remove("left-0");
        pop.classList.add("right-0");
      }
    });
  });

  document.addEventListener("click", function (e) {
    const target = e.target as Node;
    dropdowns.forEach(function (d) {
      if (d.open && !d.contains(target)) d.open = false;
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    dropdowns.forEach(function (d) {
      d.open = false;
    });
  });

  const grouped = root.querySelector<HTMLElement>("[data-tag-grouped]");
  const cloud = root.querySelector<HTMLElement>("[data-tag-cloud]");
  const toggles = Array.from(root.querySelectorAll<HTMLButtonElement>("[data-tag-view-toggle]"));
  if (!grouped || !cloud || toggles.length === 0) return;

  const storageKey = root.dataset.storageKey ?? "qecirc:tag-view";
  const defaultView = root.dataset.defaultView === "all" ? "all" : "grouped";

  function applyView(view: string): void {
    grouped!.classList.toggle("hidden", view === "all");
    cloud!.classList.toggle("hidden", view !== "all");
  }

  const stored = localStorage.getItem(storageKey);
  applyView(stored === "all" || stored === "grouped" ? stored : defaultView);

  toggles.forEach(function (btn) {
    btn.addEventListener("click", function () {
      const view = grouped!.classList.contains("hidden") ? "grouped" : "all";
      localStorage.setItem(storageKey, view);
      applyView(view);
    });
  });
}
