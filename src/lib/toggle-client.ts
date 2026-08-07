export function initToggle(buttonId: string, detailId: string): void {
  const toggle = document.getElementById(buttonId);
  const detail = document.getElementById(detailId);
  if (!toggle || !detail) return;

  const chevron = toggle.querySelector("svg");

  toggle.addEventListener("click", function () {
    const isOpen = detail.style.maxHeight !== "0px";
    if (isOpen) {
      detail.style.maxHeight = "0px";
      // `max-height: 0` + `overflow: hidden` clips the panel but leaves its
      // controls tabbable; inert has to track max-height, not just the class.
      detail.inert = true;
      chevron?.classList.remove("rotate-90");
      toggle.setAttribute("aria-expanded", "false");
    } else {
      detail.inert = false;
      detail.style.maxHeight = detail.scrollHeight + "px";
      chevron?.classList.add("rotate-90");
      toggle.setAttribute("aria-expanded", "true");
      // Notify in-section listeners (e.g. lazy-loaders) that the section
      // opened. Per-instance dedup is the listener's responsibility.
      detail.dispatchEvent(new CustomEvent("collapsible-open"));
    }
  });
}
