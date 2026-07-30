"""eval_det/ import: deterministic FT state prep (arXiv:2501.05527).

One library entry per published .qasm prep file (18), each stored as the
worst-case execution body built from the protocol data in results.csv (see
det_protocol.py). Seeds three new codes whose Hx=Hz matrices are hard-coded
in eval_det/eval.py (copied verbatim below): [[11,1,3]], [[16,2,4]], and the
[[16,6,4]] tesseract ("hypercube") code.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from det_protocol import (
    build_worst_case_body,
    load_protocols,
    pick_variant,
    qasm_prep_to_stim,
    render_notes,
)

HERE = Path(__file__).resolve().parent
import sys  # noqa: E402

import rebuild_all  # noqa: E402  (shares DATASET/EVAL_DET/anchor_h/sigma_for)

sys.path.insert(0, str(rebuild_all.REPO))
from scripts.add_circuit import import_state_prep  # noqa: E402
from scripts.add_circuit.code_identify import build_symplectic_h  # noqa: E402
from scripts.add_circuit.state_prep import symplectic_validate  # noqa: E402

# CSV variant -> library tag suffix ("global" gets no tag at all).
VARIANT_TAG = {"optimal": "opt", "heuristic": "heuristic"}

# Hx = Hz matrices copied verbatim from eval_det/eval.py (MIT).
MATRIX_11_1_3 = np.array(
    [
        [1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1],
    ]
)
MATRIX_16_2_4 = np.array(
    [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
        [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0],
    ]
)
MATRIX_HYPERCUBE = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
    ]
)

NEW_CODES: dict[str, dict] = {
    "11_1_3": dict(slug="11-1-3", name="[[11,1,3]]", n=11, d=3, hx=MATRIX_11_1_3),
    "16_2_4": dict(slug="16-2-4", name="[[16,2,4]]", n=16, d=4, hx=MATRIX_16_2_4),
    "hypercube": dict(
        slug="16-6-4",
        name="Tesseract Code",
        n=16,
        d=4,
        hx=MATRIX_HYPERCUBE,
        zoo_url="https://errorcorrectionzoo.org/c/stab_16_6_4",
    ),
}

# Existing codes reuse the eval fit strategies; mqt_dir gives the matrices used
# both for the pre-import validation gate and (perm_find) the sigma search.
DET_CODES: dict[str, dict] = {
    "steane": dict(slug="steane-code", n=7, d=3, fit="identity", mqt_dir="steane"),
    "shor": dict(slug="shor-code", n=9, d=3, fit="identity", mqt_dir="shor"),
    "surface_3": dict(
        slug="rotated-surface-code-d-3", n=9, d=3, fit="search", mqt_dir="rotated_surface_d3"
    ),
    "tetrahedral": dict(slug="tetrahedral-code", n=15, d=3, fit="perm_find", mqt_dir="tetrahedral"),
    "carbon": dict(slug="carbon-code", n=12, d=4, fit="perm_find", mqt_dir="carbon"),
    "hamming": dict(slug="15-7-3", n=15, d=3, fit="perm_find", mqt_dir="hamming_15"),
    "11_1_3": dict(new=True, n=11, d=3),
    "16_2_4": dict(new=True, n=16, d=4),
    "hypercube": dict(new=True, n=16, d=4),
}


def det_procedure(fname: str) -> str:
    return "heuristic" if "heuristic" in fname else "opt"  # eval.py's parsing rule


def _mqt_h(code_dir: str, cfg: dict) -> np.ndarray:
    """Symplectic H in MQT's own labeling — the validation gate anchor."""
    if cfg.get("new"):
        hx = NEW_CODES[code_dir]["hx"]
        return build_symplectic_h(hx, hx)
    base = rebuild_all.DATASET / "src/mqt/qecc/codes" / cfg["mqt_dir"]
    hx = np.load(base / "hx.npy").astype(int)
    hz = np.load(base / "hz.npy").astype(int)
    return build_symplectic_h(hx, hz)


def run_det(write: bool, data_dir: Path, overwrite: bool = False) -> tuple[int, int]:
    protos = load_protocols(rebuild_all.EVAL_DET / "results.csv")
    imported = deferred = 0
    report: list[str] = []
    circuits_root = rebuild_all.EVAL_DET / "circuits"
    for code_dir in sorted(p.name for p in circuits_root.iterdir() if p.is_dir()):
        cfg = DET_CODES[code_dir]
        n, d = cfg["n"], cfg["d"]
        for qasm_path in sorted((rebuild_all.EVAL_DET / "circuits" / code_dir).glob("*.qasm")):
            rel = f"{code_dir}/{qasm_path.name}"
            state_zero = qasm_path.name.startswith("zero")
            proc = det_procedure(qasm_path.name)
            key = (code_dir, state_zero, proc)
            if key not in protos:
                report.append(f"DEFER {rel}: no CSV row")
                deferred += 1
                continue
            proto = pick_variant(protos[key])
            prep = qasm_prep_to_stim(qasm_path.read_text())
            body, _stats = build_worst_case_body(prep, proto, n, state_zero)
            # Consistency gate: the body must stabilize the code in MQT's own
            # labeling (catches any error in the reconstruction).
            gate = symplectic_validate(str(body), _mqt_h(code_dir, cfg), n)
            if gate != "passed":
                report.append(f"DEFER {rel}: consistency gate ({gate})")
                deferred += 1
                continue
            state = "zero" if state_zero else "plus"
            kwargs = dict(
                circuit=str(body),
                n=n,
                d=d,
                code_name="",
                circuit_name=f"Det FT {state} ({proc})",
                source=rebuild_all.SOURCE_DET,
                tool="mqt-qecc",
                source_file=f"scripts/ft_stateprep/eval_det/circuits/{rel}",
                logical_state=state,
                connectivity="fully-connected",
                gate_set=rebuild_all.gate_set_of(body),
                # Variant tag conventions: "global" is dropped (jointly-optimized
                # two-layer solution, the library default) and "optimal" is
                # spelled "opt" to match the eval/rlftqc imports.
                tags=[
                    "state-preparation",
                    "ft",
                    "deterministic",
                    f"prep:{proc}",
                ]
                + (
                    []
                    if proto.variant == "global"
                    else [f"verification:{VARIANT_TAG[proto.variant]}"]
                ),
                notes=render_notes(proto, state_zero, rel),
                data_dir=str(data_dir),
                overwrite=overwrite,
            )
            if cfg.get("new"):
                # No permutation kwarg: the anchor is already in the circuit's
                # labeling (identity fit found immediately), and a supplied
                # permutation would demand a stored-code match that does not
                # exist yet — add_circuit seeds the code instead.
                nc = NEW_CODES[code_dir]
                kwargs.update(
                    method="anchor",
                    anchor_H=build_symplectic_h(nc["hx"], nc["hx"]),
                    code_name=nc["name"],
                    code_slug=nc["slug"],
                    zoo_url=nc.get("zoo_url", ""),
                )
            elif cfg["fit"] == "identity":
                h = rebuild_all.anchor_h(cfg["slug"], data_dir)
                kwargs.update(method="anchor", anchor_H=h, permutation=list(range(n)))
            elif cfg["fit"] == "perm_find":
                h = rebuild_all.anchor_h(cfg["slug"], data_dir)
                sigma = rebuild_all.sigma_for(cfg["mqt_dir"], cfg["slug"], n, data_dir)
                if sigma is None:
                    report.append(f"DEFER {rel}: permutation not found")
                    deferred += 1
                    continue
                kwargs.update(method="anchor", anchor_H=h, permutation=sigma)
            else:  # search (n <= 9)
                kwargs.update(method="anchor", anchor_H=rebuild_all.anchor_h(cfg["slug"], data_dir))
            if not write:
                imported += 1
                continue
            try:
                import_state_prep(**kwargs)
                imported += 1
            except Exception as e:  # noqa: BLE001
                report.append(f"FAIL {rel}: {type(e).__name__}: {str(e).splitlines()[0][:80]}")
                deferred += 1
    print(f"eval_det/: {'imported' if write else 'classified'}={imported} deferred={deferred}")
    for line in report:
        print("  " + line)
    return imported, deferred
