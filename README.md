# QECirc

A community-driven library for quantum error correction circuits.

[![Unitary Foundation](https://img.shields.io/badge/Supported%20By-UNITARY%20FOUNDATION-brightgreen.svg?style=for-the-badge)](https://unitary.foundation)

**Browse the library at [qecirc.com](https://qecirc.com)** | [About](https://qecirc.com/about)

## What QECirc is

- A place to find and share reusable quantum error correction circuits
- A fast, simple way to grab standard circuits for common tasks — encoding, state preparation, syndrome extraction, and more
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

## Quick Start

```bash
npm install
uv sync
npm run db:create
npm run dev
```

## Contributing

Circuits are submitted by opening a [GitHub Issue](https://github.com/qecirc/qecirc-website/issues/new/choose) using the provided templates.

## License

Code is licensed under [MIT](LICENSE). Data in `data_yaml/` is licensed under [CC BY-SA 4.0](LICENSE-DATA).
