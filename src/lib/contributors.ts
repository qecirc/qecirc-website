/**
 * The project's human contributors — the single source of truth for the site.
 *
 * MAINTAINED BY HAND, deliberately. This is not the GitHub contributor list: it
 * excludes bots (Claude, Renovate) and the `qecirc` service account, and it
 * INCLUDES people who helped without ever committing and so have no GitHub link.
 * Generating it from the API would silently drop those names.
 *
 * Rendered by src/pages/about.astro and counted on the landing page. Mirror any
 * change in README.md, which keeps its own copy for people reading the repo.
 */
export interface Contributor {
  name: string;
  /** GitHub username; omitted for contributors without an account. */
  github?: string;
}

export const CONTRIBUTORS: readonly Contributor[] = [
  { name: "Ludwig Schmid", github: "lsschmid" },
  { name: "Tom Peham", github: "pehamTom" },
  { name: "Remmy Zen", github: "remmyzen" },
  { name: "Maxie Helen Bichmann", github: "MaxieHelenBichmann" },
  { name: "Diego Forlivesi", github: "DiegoForlivesi" },
  { name: "David Amaro", github: "davamaro" },
  { name: "Luis Colmenarez" },
];
