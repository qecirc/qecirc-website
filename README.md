# QECirc

A community-driven library for quantum error correction circuits.

[![Unitary Foundation](https://img.shields.io/badge/Supported%20By-UNITARY%20FOUNDATION-brightgreen.svg?style=for-the-badge)](https://unitary.foundation)

**Browse the library at [qecirc.com](https://qecirc.com)** | [About](https://qecirc.com/about)

## What QECirc is

- A place to find and share reusable quantum error correction circuits
- A fast, simple way to grab standard circuits for common tasks — encoding, state preparation, logical gates, syndrome extraction, and more
- A hub for the QEC circuit community, highlighting well-crafted circuits and the tools used to create them
- Simple to use and open to everyone

## What QECirc is not

- A replacement for the [QEC Zoo](https://errorcorrectionzoo.org/) — detailed code properties belong there
- An archive for highly specific circuit constructions — those are better stored on platforms like Zenodo, with a link from the Zoo

## Alpha Status

QECirc is currently in alpha. The site is under active development, which means functionality, URLs, permalinks, and circuit data may change without notice. If you encounter any issues or incorrect data, please [open an issue](https://github.com/qecirc/qecirc-website/issues) on GitHub.

## Development

QECirc was created and is maintained by Ludwig Schmid and Tom Peham.

The project is funded by the [Unitary Foundation](https://unitary.foundation) and supported by the [Chair for Design Automation](https://www.cda.cit.tum.de/) at the Technical University of Munich.

## Contributors

<!-- Maintained by hand — the repository's human contributors, excluding bots
     (Claude, Renovate) and the `qecirc` service account, PLUS people who helped
     without committing and so have no GitHub link (listed unlinked). Do not
     regenerate this from the GitHub contributor list: that would silently drop
     the unlinked names. Mirror any change here in src/lib/contributors.ts, which
     the About page renders and the landing page counts. -->

[Ludwig Schmid](https://github.com/lsschmid), [Tom Peham](https://github.com/pehamTom), [Remmy Zen](https://github.com/remmyzen), [Maxie Helen Bichmann](https://github.com/MaxieHelenBichmann), [Diego Forlivesi](https://github.com/DiegoForlivesi), [David Amaro](https://github.com/davamaro), [Luis Colmenarez](https://github.com/luis2colmena), [Hasan Sayginel](https://github.com/hsayginel), [Michael A. Perlin](https://github.com/perlinm), [Mingyu Kang](https://github.com/mkangquantum), [Yuhao Liu](https://github.com/acasta-yhliu)

## Quick Start

```bash
npm install
uv sync
npm run db:create
npm run dev
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for all the ways to help.

Most circuits are submitted by opening a [GitHub Issue](https://github.com/qecirc/qecirc-website/issues/new/choose) using the provided templates — a maintainer then ingests them.

To add circuits yourself, or import a whole dataset, see the ingestion guides:

- [docs/adding-circuits.md](docs/adding-circuits.md) — manual workflow: the helper functions, the `add_circuit` / `import_state_prep` APIs, fitting to existing codes, bulk imports, and an FAQ.
- [docs/adding-circuits-agent.md](docs/adding-circuits-agent.md) — the `/add-circuit` agent-assisted workflow.

## License

Code is licensed under [MIT](LICENSE). Data in `data_yaml/` is licensed under [CC BY-SA 4.0](LICENSE-DATA).
