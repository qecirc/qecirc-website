# Contributing to QECirc

Thanks for helping grow the library! There are a few ways to contribute, from
"here's a circuit" to a full pull request. Pick the one that fits.

## Contribute a circuit

**The easiest way — no setup needed.** Open a
[Circuit Submission issue](https://github.com/qecirc/qecirc-website/issues/new/choose)
and paste your STIM circuit, its distance, and a source. Check matrices are
optional for encoding circuits (we can derive them). A maintainer takes it from
there.

Have circuits but no time to file them one by one? Email
[contribute@qecirc.com](mailto:contribute@qecirc.com) and we're happy to do the
ingestion for you.

## Report bad data, bugs, or ideas

Use the matching [issue template](https://github.com/qecirc/qecirc-website/issues/new/choose):

- **Data Correction** — something wrong in an existing circuit or code.
- **Bug Report** — the site misbehaves.
- **Feature Request** — an idea for the library.

## Add circuits yourself

Want to run the ingestion pipeline directly, or import a whole dataset? The
scripts and their helpers are documented in:

- **[docs/adding-circuits.md](docs/adding-circuits.md)** — the manual workflow:
  helper functions, the `add_circuit` / `import_state_prep` APIs, fitting to
  existing codes, bulk/dataset imports, and an FAQ.
- **[docs/adding-circuits-agent.md](docs/adding-circuits-agent.md)** — the
  `/add-circuit` agent-assisted workflow.

## Code contributions

### Setup

```bash
npm install      # Node dependencies
uv sync          # Python dependencies
npm run db:create
npm run dev      # http://localhost:4321
```

`data_yaml/` is the source of truth; the SQLite database is built from it. After
editing any YAML, run `npm run db:create` and **restart the dev server** (it
caches the DB connection).

### Before you open a PR

```bash
npm run format          # Prettier (CI fails on unformatted files)
npm run lint            # ESLint
npm run validate:yaml   # only if you touched data_yaml/
npm run validate:circuits
```

### Conventions

- **Pull requests only** — no direct commits to `main`.
- **[Conventional Commits](https://www.conventionalcommits.org/)** —
  `feat(browse): …`, `fix(parser): …`, `docs: …`, etc.
- **Bump the version** in the same PR that ships the change — see the
  [versioning table in CLAUDE.md](CLAUDE.md#versioning).
- Prefer built-ins and the standard library; justify any new dependency in the
  PR description.

## Licensing

By contributing you agree that your contributions are licensed under the
project's dual license: code under [MIT](LICENSE) and data (`data_yaml/`) under
[CC BY-SA 4.0](LICENSE-DATA).
