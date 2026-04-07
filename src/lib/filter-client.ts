import { FILTER_PART_REGEX } from "./constants";

/**
 * Shared client-side logic for CodeFilter and CircuitFilter components.
 * Config is read from data-* attributes on the form element.
 *
 * Expected form attributes:
 *   data-filter-fields  — comma-separated field names (e.g. "n,k,d")
 *   data-filter-focus   — field to auto-focus on load (from server)
 *   data-base-path      — navigation base path (e.g. "/" or "/codes/steane-code")
 *   data-preserve-sort  — if present, preserves sort/sort_dir params
 */
export function initFilterForm(form: HTMLFormElement): void {
  const fields = (form.dataset.filterFields ?? "").split(",");
  const focus = form.dataset.filterFocus ?? "";
  const basePath = form.dataset.basePath ?? "/";
  const preserveSort = form.dataset.preserveSort !== undefined;

  const statusDiv = form.querySelector<HTMLElement>("[data-filter-status]");
  const errorSpan = form.querySelector<HTMLElement>("[data-filter-error]");
  const inputs = form.querySelectorAll<HTMLInputElement>("input[data-filter]");
  let debounceTimer: ReturnType<typeof setTimeout>;
  let lastEditedField = "";

  // Restore focus after page reload, then strip focus param from visible URL
  if (focus && fields.includes(focus)) {
    const target = form.querySelector<HTMLInputElement>(
      `input[name="${focus}"]`,
    );
    if (target) {
      target.focus();
      const val = target.value;
      target.setSelectionRange(val.length, val.length);
    }
    const url = new URL(window.location.href);
    url.searchParams.delete("focus");
    history.replaceState(null, "", url.toString());
  }

  function isValidFilter(value: string): boolean {
    const trimmed = value.trim();
    if (trimmed === "") return true;
    const parts = trimmed.split(",");
    for (let i = 0; i < parts.length; i++) {
      const part = parts[i].trim();
      if (part === "") continue;
      if (!FILTER_PART_REGEX.test(part)) return false;
    }
    return true;
  }

  function validateAndUpdate(): boolean {
    let hasError = false;
    inputs.forEach(function (input) {
      const invalid = !isValidFilter(input.value);
      if (invalid) hasError = true;
      if (invalid) {
        input.classList.add("ring-1", "ring-red-300");
      } else {
        input.classList.remove("ring-1", "ring-red-300");
      }
    });
    if (errorSpan && statusDiv) {
      if (hasError) {
        errorSpan.classList.remove("hidden");
        Array.from(statusDiv.children).forEach(function (el) {
          if (el !== errorSpan) el.classList.add("hidden");
        });
      } else {
        errorSpan.classList.add("hidden");
        Array.from(statusDiv.children).forEach(function (el) {
          if (el !== errorSpan) el.classList.remove("hidden");
        });
      }
    }
    return !hasError;
  }

  function submitFilters(): void {
    if (!validateAndUpdate()) return;
    const params = new URLSearchParams();
    const data = new FormData(form);
    data.forEach(function (value, key) {
      if (typeof value === "string" && value.trim() !== "") {
        params.set(key, value.trim());
      }
    });
    // Preserve tag params from current URL
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.getAll("tag").forEach(function (t) {
      params.append("tag", t);
    });
    // Optionally preserve sort params
    if (preserveSort) {
      const sortField = urlParams.get("sort");
      const sortDir = urlParams.get("sort_dir");
      if (sortField) params.set("sort", sortField);
      if (sortDir) params.set("sort_dir", sortDir);
    }
    if (lastEditedField && fields.includes(lastEditedField)) {
      params.set("focus", lastEditedField);
    }
    const target = basePath + (params.size > 0 ? "?" + params.toString() : "");
    // Skip reload if URL would be the same (minus focus param)
    const currentParams = new URLSearchParams(window.location.search);
    currentParams.delete("focus");
    const newCheck = new URLSearchParams(params);
    newCheck.delete("focus");
    if (newCheck.toString() === currentParams.toString()) return;
    window.location.href = target;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    clearTimeout(debounceTimer);
    submitFilters();
  });

  form.addEventListener("input", function (e) {
    clearTimeout(debounceTimer);
    const target = e.target as HTMLInputElement;
    if (target?.name && fields.includes(target.name)) {
      lastEditedField = target.name;
    }
    validateAndUpdate();
    debounceTimer = setTimeout(submitFilters, 800);
  });
}
