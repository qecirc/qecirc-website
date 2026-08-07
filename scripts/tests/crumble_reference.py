"""Emit stim's own Crumble URL for every committed circuit body.

The reference side of `crumble-url.test.mjs`. `crumbleUrl` in
src/lib/stim-format.ts is a hand-written reimplementation of
`stim.Circuit.to_crumble_url()` — the link used to be computed here, in Python,
and stored; it is now derived in the browser, so nothing would notice if a stim
upgrade changed the encoding or an edit to the abbreviation table broke it. This
prints what stim says, one body per line, so the JS test can diff against it.

Output: `<filename>\t<canonical>\t<url>`, tab-separated, one line per body file.
`canonical` is 1 when the file is already what `str(stim.Circuit(text))` emits —
the exactness claim only holds for canonical text, so the JS side asserts it
rather than assuming it. A URL contains no tab and no newline, so the format
needs no escaping.

Usage (from the repo root, and normally via `npm test`):
    uv run python scripts/tests/crumble_reference.py [--data-dir data_yaml]
"""

import argparse
import sys
from pathlib import Path

import stim

# Every committed body format that is STIM text. `.qasm` is not stim's to parse.
BODY_SUFFIXES = (".stim", ".stim-annotated")


def emit(data_dir: Path, out) -> int:
    circuits_dir = data_dir / "circuits"
    paths = sorted(p for p in circuits_dir.iterdir() if p.suffix in BODY_SUFFIXES)
    for path in paths:
        text = path.read_text(encoding="utf-8")
        circ = stim.Circuit(text)
        canonical = 1 if str(circ) == text.rstrip("\n") else 0
        out.write(f"{path.name}\t{canonical}\t{circ.to_crumble_url()}\n")
    return len(paths)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data_yaml")
    args = parser.parse_args()
    count = emit(Path(args.data_dir), sys.stdout)
    print(f"{count} bodies", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
