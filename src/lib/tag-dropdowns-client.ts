const VIEW_LS_KEY = "qecirc:tag-view"; // "grouped" (default) | "all"

/**
 * Behavior for the category tag dropdowns in the circuit filter:
 * one dropdown open at a time, close on outside click / Escape, and a
 * persisted toggle between the grouped view and the flat all-tags cloud.
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

  function applyView(view: string): void {
    grouped!.classList.toggle("hidden", view === "all");
    cloud!.classList.toggle("hidden", view !== "all");
  }

  if (localStorage.getItem(VIEW_LS_KEY) === "all") applyView("all");

  toggles.forEach(function (btn) {
    btn.addEventListener("click", function () {
      const view = grouped!.classList.contains("hidden") ? "grouped" : "all";
      localStorage.setItem(VIEW_LS_KEY, view);
      applyView(view);
    });
  });
}
