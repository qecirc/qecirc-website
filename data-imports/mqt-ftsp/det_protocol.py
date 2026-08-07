"""Parse eval_det/results.csv protocol data and build worst-case Stim bodies.

Layer semantics (mqt-qecc state_prep_det.py / simulation_det.py): for |0>_L
layer 0 measures Z-stabilizers (detects X errors), layer 1 X-stabilizers; for
|+>_L swapped. Each layer: round-1 verification stabs (always measured, hook
flags where marked), then — per round-1 outcome — round-2 stabs and a Pauli
correction chosen by the round-2 outcome. Deterministic (det) branches measure
round-2 stabs in the layer's own basis and correct with X (Z-stab layer) or Z
(X-stab layer); hook-flag branches use the OPPOSITE basis for both.

The stored body linearizes the WORST branch per layer (max round-2 CNOTs,
tie-break max correction weight, hook branches included) — but only its
measurements: the outcome-dependent Pauli correction is NOT part of the stored
circuit (in practice it is absorbed into the Pauli frame; the full correction
tables live in the notes). Bodies therefore contain only H/CX/MR, so the QASM
view can be generated.

Verification measurement sub-circuit ordering is ported verbatim from
simulation_det.py::_create_stab_measurement_circuit:
  - one measurement ancilla per stab; flag ancillas AFTER all measurement
    ancillas of the block;
  - stab support iterated in ascending qubit order;
  - Z-stabs: CX data->anc. X-stabs: H anc, CX anc->data, H anc;
  - flagged stabs: flag opens before the 2nd data CX and closes before the
    last data CX (Z: H flag; CX flag->anc ... CX flag->anc; H flag;
    X: CX anc->flag ... CX anc->flag);
  - all ancillas of a block measured together at block end (MR, ascending).
Ancilla indices restart at n for every block (MR frees them), so
qubit_count = n + max block width.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import stim

# ---------- CSV parsing ----------


def _parse_np(cell: str):
    """Parse a numpy-repr CSV cell like "[array([0, 1, ...]), ...]" or
    "{1: ([array(...)], {0: array(...), 1: array(...)}), ...}"."""
    cleaned = re.sub(r"array\(", "np.array(", cell)
    cleaned = re.sub(r",\s*dtype=int8", "", cleaned)
    return eval(cleaned, {"np": np, "False": False, "True": True})  # noqa: S307


@dataclass
class Layer:
    stabs: list[np.ndarray]  # round-1 verification stabs
    flagged: list[bool]  # hook flag per stab
    corrections: dict  # {outcome: ([round-2 stabs], {outcome2: correction})}
    hook_corrections: list[dict]  # per-stab hook branch tables


@dataclass
class DetProtocol:
    variant: str  # heuristic | optimal | global
    layers: tuple[Layer, Layer]


def load_protocols(csv_path: Path) -> dict[tuple[str, bool, str], dict[str, DetProtocol]]:
    """-> {(code, zero_state, procedure): {variant: DetProtocol}}"""
    out: dict = {}
    for row in csv.DictReader(csv_path.open()):
        key = (row["code"], row["zero_state"] == "True", row["procedure"])
        layers = []
        for idx in (0, 1):
            stabs = _parse_np(row[f"verification_stabs_{idx}"])
            corrections = _parse_np(row[f"recovery_stabs_{idx}"]) or {}
            flags_raw = _parse_np(row[f"flags_{idx}"])
            hook_corrections = [h if isinstance(h, dict) else {} for h in flags_raw]
            if len(hook_corrections) < len(stabs):
                hook_corrections += [{}] * (len(stabs) - len(hook_corrections))
            flagged = [bool(h) for h in hook_corrections]
            layers.append(Layer(list(stabs), flagged, corrections, hook_corrections))
        out.setdefault(key, {})[row["verification"]] = DetProtocol(
            row["verification"], (layers[0], layers[1])
        )
    return out


VARIANT_PREFERENCE = ("global", "optimal", "heuristic")


def pick_variant(variants: dict[str, DetProtocol]) -> DetProtocol:
    for v in VARIANT_PREFERENCE:
        if v in variants:
            return variants[v]
    raise KeyError(f"no known variant among {sorted(variants)}")


# ---------- qasm -> stim prep ----------


def qasm_prep_to_stim(qasm: str) -> stim.Circuit:
    """Convert the bare h/cx OPENQASM 2.0 encoders to stim."""
    ops = []
    for line in qasm.splitlines():
        line = line.strip().rstrip(";")
        if m := re.fullmatch(r"h q\[(\d+)\]", line):
            ops.append(f"H {m.group(1)}")
        elif m := re.fullmatch(r"cx q\[(\d+)\],\s*q\[(\d+)\]", line):
            ops.append(f"CX {m.group(1)} {m.group(2)}")
        elif line.startswith(("OPENQASM", "include", "qreg")) or not line:
            continue
        else:
            raise ValueError(f"unexpected qasm line: {line!r}")
    return stim.Circuit("\n".join(ops))


# ---------- worst-case body ----------


def _support(vec) -> list[int]:
    return [int(i) for i in np.flatnonzero(np.asarray(vec) % 2)]


def _measure_block(stabs, flagged, z_stabs: bool, n: int) -> tuple[stim.Circuit, int]:
    """Port of _create_stab_measurement_circuit; returns (circuit, block width)."""
    c = stim.Circuit()
    num_stabs = len(stabs)
    flag = n + num_stabs  # flag ancillas placed after measurement ancillas
    measured: list[int] = []
    for s_idx, (stab, has_flag) in enumerate(zip(stabs, flagged)):
        a = n + s_idx
        sup = _support(stab)
        if not z_stabs:
            c.append("H", [a])
        for q_idx, q in enumerate(sup):
            if has_flag and q_idx == 1:
                if z_stabs:
                    c.append("H", [flag])
                    c.append("CX", [flag, a])
                else:
                    c.append("CX", [a, flag])
            if has_flag and q_idx == len(sup) - 1:
                if z_stabs:
                    c.append("CX", [flag, a])
                    c.append("H", [flag])
                else:
                    c.append("CX", [a, flag])
            c.append("CX", [q, a] if z_stabs else [a, q])
        if not z_stabs:
            c.append("H", [a])
        measured.append(a)
        if has_flag:
            measured.append(flag)
            flag += 1
    if measured:
        c.append("MR", sorted(measured))
    return c, (flag - n)


def worst_branch(layer: Layer):
    """Most expensive branch across det + hook correction tables.

    Returns (round2_stabs, correction_vec, outcome1, outcome2, flip_basis,
    hook_ordinal) or None. Cost = (round-2 CNOT count, correction weight).
    Hook branches measure and correct in the opposite basis (flip_basis=True);
    hook_ordinal is the branch's position among the layer's flagged stabs
    (None for det branches).
    """
    best = None
    tables = [(layer.corrections, False, None)]
    ordinal = 0
    for h in layer.hook_corrections:
        if h:
            tables.append((h, True, ordinal))
            ordinal += 1
    for table, flip, hook in tables:
        for o1, (stabs2, recs) in table.items():
            cnots = sum(len(_support(s)) for s in stabs2)
            for o2, corr in recs.items():
                cost = (cnots, len(_support(corr)))
                if best is None or cost > best[0]:
                    best = (cost, list(stabs2), corr, int(o1), int(o2), flip, hook)
    if best is None:
        return None
    return best[1], best[2], best[3], best[4], best[5], best[6]


def build_worst_case_body(
    prep: stim.Circuit, proto: DetProtocol, n: int, zero_state: bool
) -> tuple[stim.Circuit, dict]:
    """prep -> per layer: round-1 verification -> worst branch (round-2 + corr).

    Returns (circuit, stats): stats has 'cnots' (verification + round-2 CX
    count, data-ancilla only) and 'max_width' (max ancillas alive in a block).
    """
    body = stim.Circuit()
    body += prep
    stats = {"cnots": 0, "max_width": 0}
    for layer_idx, layer in enumerate(proto.layers):
        z_stabs = zero_state if layer_idx == 0 else not zero_state
        if layer.stabs:
            blk, width = _measure_block(layer.stabs, layer.flagged, z_stabs, n)
            body += blk
            stats["max_width"] = max(stats["max_width"], width)
            stats["cnots"] += sum(len(_support(s)) for s in layer.stabs)
        wb = worst_branch(layer)
        if wb is None:
            continue
        stabs2, _corr, _o1, _o2, flip, _hook = wb
        branch_z = (not z_stabs) if flip else z_stabs
        if stabs2:
            # Only the branch's measurements enter the body; its Pauli
            # correction is a Pauli-frame update, documented in the notes.
            blk, width = _measure_block(stabs2, [False] * len(stabs2), branch_z, n)
            body += blk
            stats["max_width"] = max(stats["max_width"], width)
            stats["cnots"] += sum(len(_support(s)) for s in stabs2)
    return body, stats


# ---------- notes rendering ----------


def _fmt_stab(vec, z_basis: bool) -> str:
    return ("Z" if z_basis else "X") + "[" + ",".join(str(q) for q in _support(vec)) + "]"


def _fmt_recs(recs: dict, z_basis: bool) -> str:
    """One-line round-2 outcome table: '0 -> none, 1 -> X[6], ...'."""
    parts = []
    for o2, corr in sorted(recs.items()):
        sup = _support(corr)
        pauli = ("X" if z_basis else "Z") + "[" + ",".join(str(q) for q in sup) + "]"
        parts.append(f"{o2:b} -> {pauli if sup else 'none'}")
    return ", ".join(parts)


def render_notes(proto: DetProtocol, zero_state: bool, source_file: str) -> str:  # noqa: ARG001
    lines = [
        f"Deterministic FT state preparation (arXiv:2501.05527); verification variant: "
        f"{proto.variant}. Body and metrics show the worst-case branch of the adaptive "
        "protocol: prep, round-1 verification (always measured), then the most expensive "
        "branch's round-2 measurements. The outcome-dependent Pauli correction is not "
        "part of the circuit (Pauli-frame update); apply it per the branch tables below "
        "(outcome bits MSB-first in measurement order):",
    ]
    for idx, layer in enumerate(proto.layers):
        z = zero_state if idx == 0 else not zero_state
        basis = "Z" if z else "X"
        if not layer.stabs:
            lines.append(f"Layer {idx} ({basis}): trivial, no verification")
            continue
        stabs = ", ".join(
            _fmt_stab(s, z) + ("*" if layer.flagged[i] else "") for i, s in enumerate(layer.stabs)
        )
        hooked = " (* = hook flag)" if any(layer.flagged) else ""
        lines.append(f"Layer {idx} ({basis}): round-1 measure {stabs}{hooked}")
        for outcome, (stabs2, recs) in sorted(layer.corrections.items()):
            measured = ", ".join(_fmt_stab(s, z) for s in stabs2 if _support(s))
            step = f"measure {measured}; " if measured else ""
            lines.append(f"  outcome {outcome:b}: {step}{_fmt_recs(recs, z)}")
        for i, hooks in enumerate(layer.hook_corrections):
            for outcome, (stabs2, recs) in sorted(hooks.items()) if hooks else []:
                measured = ", ".join(_fmt_stab(s, not z) for s in stabs2 if _support(s))
                step = f"measure {measured}; " if measured else ""
                lines.append(
                    f"  hook of stab {i} (outcome {outcome:b}): {step}{_fmt_recs(recs, not z)}"
                )
    return "\n".join(lines)
