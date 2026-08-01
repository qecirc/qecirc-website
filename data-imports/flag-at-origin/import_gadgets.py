#!/usr/bin/env python
"""Flag-at-origin standalone FT gadgets (arXiv:2508.14200).

The ``*_ft_plaquette_mod_ANC.txt`` files in ``Notebook_2.zip`` are complete
fault-tolerant gadgets that prepare/measure a single weight-``n`` stabiliser,
verified to distance ``d`` (X- or Z-type), using flag ancillas. They are reusable
building blocks that do **not** correspond to any error-correcting code, so they
can't go through ``import_state_prep`` (there is nothing to validate against).

We collect them under a placeholder "Flag Gadgets" code (``n = k = 0``, no check
matrices) and write each circuit directly with the pipeline's own helpers, so the
metrics / STIM+QASM bodies / slugs match every other circuit in the library.

Usage:
  python import_gadgets.py                 # classify only (no writes)
  python import_gadgets.py --write
  python import_gadgets.py --dataset PATH  # dir holding Notebook_2.zip
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DATASET = REPO.parent / "flag_at_origin_paper"
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from convert import dict_to_stim, load_pytket_dict  # noqa: E402

from scripts.add_circuit.compute import slugify  # noqa: E402
from scripts.add_circuit.compute_circuit import compute_circuit_data  # noqa: E402
from scripts.add_circuit.ids import next_qec_id  # noqa: E402
from scripts.add_circuit.yaml_helpers import (  # noqa: E402
    build_circuit_yaml,
    build_code_yaml,
    dump_yaml,
    write_file,
)

SOURCE = "https://arxiv.org/abs/2508.14200"
TOOL = "flag-at-origin"
CODE_SLUG = "flag-gadgets"
CODE = {
    "name": "Flag Gadgets",
    "n": 0,
    "k": 0,
    "tags": [{"name": "no-code"}],  # placeholder collector — not an actual code
}

# The canonical gadget set is the plain `{d}_{w}_{X|Z}_ft_plaquette.txt` files —
# what the paper's own generate_FT_plaq_notebook() reads and its Notebook_2 table
# catalogs. The `_mod_ANC` / `_from_Cplusplus` variants are auxiliary and skipped.
# member basename -> (distance, weight, basis)
_NAME_RE = re.compile(r"^(\d+)_(\d+)_([XZ])_ft_plaquette\.txt$")
_qec_id_re = re.compile(r"^qec_id:\s*(\d+)\s*$", re.MULTILINE)


def parse_name(member: str) -> tuple[int, int, str] | None:
    m = _NAME_RE.match(member.split("/")[-1])
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), m.group(3)


def gadget_specs(zf: zipfile.ZipFile) -> list[tuple[str, int, int, str]]:
    specs = []
    for name in zf.namelist():
        if "__MACOSX" in name:
            continue
        parsed = parse_name(name)
        if parsed:
            d, w, basis = parsed
            specs.append((name, d, w, basis))
    # deterministic order: distance, weight, basis
    specs.sort(key=lambda s: (s[1], s[2], s[3]))
    return specs


def import_one(
    members: list[str], ds: list[int], w: int, basis: str, data_dir: Path, write: bool, zf
) -> str:
    """One stored circuit per distinct gadget, however many distances ship it.

    A gadget depends on the stabiliser's weight, not on the code distance it was
    verified at, so the same file comes back for every distance at or above the
    one it first appears in — the weight-4 X gadget is byte-identical at d=3, 5,
    7, 9 and 11. Storing five copies published one circuit five times with
    nothing to tell the pages apart but the number in the title. The distances
    are the information, so they become five `distance:` tags on one circuit.
    """
    member = members[0]  # lowest distance; they are byte-identical by construction
    stim_text, ndata, anc, _ = dict_to_stim(load_pytket_dict(zf.read(member).decode()))
    b = basis.lower()
    span = f"d={ds[0]}" if len(ds) == 1 else f"d={ds[0]}-{ds[-1]}"
    name = f"{basis}-type weight-{w} FT gadget ({span})"
    # The slug stays the lowest distance's, so an entry keeps its file name and
    # its permanent qec_id when a later distance turns out to ship the same
    # circuit. Deterministic either way: it is derived, not remembered.
    slug_name = f"{basis}-type weight-{w} FT gadget (d={ds[0]})"
    anc_phrase = f"{len(anc)} flag ancillas" if anc else "no flag ancillas needed"
    verified = (
        f"distance {ds[0]}"
        if len(ds) == 1
        else "distances " + ", ".join(map(str, ds[:-1])) + f" and {ds[-1]}"
    )
    notes = (
        f"Fault-tolerant gadget for a weight-{w} {basis}-type stabiliser, verified "
        f"to {verified} via the 'flag at origin' construction (arXiv:2508.14200). "
        f"A reusable building block ({ndata} data qubits + {anc_phrase}) "
        f"that is not tied to a specific code. "
        + (
            f"Source file: {member}."
            if len(members) == 1
            else "The same circuit ships at each of those distances; source files: "
            + ", ".join(members)
            + "."
        )
    )
    # Weight is a numeric metric (like qubit_count), not a tag — there are ~50
    # distinct values, so it powers a range filter instead of a tag dropdown.
    # `flag` tag only when the gadget actually uses flag ancillas; the trivial
    # low-weight cases need none but are still FT (they keep the `ft` tag).
    tags = ["gadget", "ft", *[f"distance:{d}" for d in ds], f"{b}-type"]
    if anc:
        tags.insert(1, "flag")
    circ = compute_circuit_data(
        stim_text, circuit_name=name, source=SOURCE, tool=TOOL, notes=notes, tags=tags
    )
    circ["weight"] = w
    circ["slug"] = slugify(slug_name)
    stem = f"{CODE_SLUG}--{circ['slug']}"
    if write:
        circuits_dir = data_dir / "circuits"
        # Preserve a previously-assigned qec_id on overwrite; ids are permanent.
        existing = circuits_dir / f"{stem}.yaml"
        prev = _qec_id_re.search(existing.read_text()) if existing.exists() else None
        circ["qec_id"] = int(prev.group(1)) if prev else next_qec_id(data_dir)
        write_file(circuits_dir / f"{stem}.yaml", dump_yaml(build_circuit_yaml(circ)), quiet=True)
        for body in circ.get("bodies", []):
            if body.get("body"):
                write_file(circuits_dir / f"{stem}.{body['format']}", body["body"], quiet=True)
    verb = "wrote" if write else "ok   "
    return f"{verb} {stem} (q={circ['qubit_count']}, gates={circ['gate_count']})"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dataset", default=str(DATASET))
    ap.add_argument("--data-dir", default=str(REPO / "data_yaml"))
    ap.add_argument("--limit", type=int, default=None, help="only process the first N gadgets")
    args = ap.parse_args()

    zip_path = Path(args.dataset) / "Notebook_2.zip"
    if not zip_path.exists():
        sys.exit(f"Notebook_2.zip not found at {zip_path} — clone Quantinuum/flag_at_origin_paper")
    data_dir = Path(args.data_dir)

    # Seed the placeholder code (no check matrices; n = k = 0).
    code_path = data_dir / "codes" / f"{CODE_SLUG}.yaml"
    if args.write and not code_path.exists():
        write_file(code_path, dump_yaml(build_code_yaml(CODE)), quiet=True)
        print(f"seeded code {code_path}")

    with zipfile.ZipFile(zip_path) as zf:
        specs = gadget_specs(zf)
        if args.limit:
            specs = specs[: args.limit]

        # Group by the circuit itself, not by (weight, basis): identity is what
        # the rule is about, and reading the file is the only way to know it.
        # Keyed on (basis, weight, body) so a hypothetical weight-w gadget that
        # genuinely differs between distances would still get its own entry.
        groups: dict[tuple[str, int, str], list[tuple[str, int]]] = {}
        for member, d, w, basis in specs:
            body, _, _, _ = dict_to_stim(load_pytket_dict(zf.read(member).decode()))
            groups.setdefault((basis, w, body), []).append((member, d))

        for (basis, w, _), entries in groups.items():
            entries.sort(key=lambda e: e[1])
            members = [m for m, _ in entries]
            ds = [d for _, d in entries]
            print(import_one(members, ds, w, basis, data_dir, args.write, zf), flush=True)

    merged = sum(len(v) - 1 for v in groups.values())
    print(
        f"\n{'wrote' if args.write else 'classified'} {len(groups)} flag gadgets "
        f"from {len(specs)} source files ({merged} were the same circuit at another distance)."
    )


if __name__ == "__main__":
    main()
