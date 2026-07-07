"""pytket ``Circuit.to_dict()`` (JSON or Python-repr) -> STIM, dependency-free.

The flag-at-origin circuits (the per-code prep JSONs and the ``_mod_ANC`` flag
gadgets) use only H / CX / Measure / Barrier and never measure a qubit twice, so
the mapping is exact: H->H, CX->CX, Measure->M, Barrier->drop. Data qubits
(register ``"q"``) map to STIM indices ``0..n-1``; flag ancillas follow.
"""

import ast
import json


def load_pytket_dict(text: str) -> dict:
    """Parse a pytket circuit dict from text (JSON, or Python-repr with single
    quotes as the gadget files use)."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return ast.literal_eval(text)


def dict_to_stim(d: dict):
    """Convert a pytket circuit dict to STIM.

    Returns ``(stim_text, n_data, ancilla_indices, meta)``.
    """
    data = sorted((q for q in d["qubits"] if q[0] == "q"), key=lambda q: q[1][0])
    anc = sorted((q for q in d["qubits"] if q[0] != "q"), key=lambda q: (q[0], q[1][0]))
    idx = {}
    for i, q in enumerate(data):
        idx[(q[0], tuple(q[1]))] = i
    for j, q in enumerate(anc):
        idx[(q[0], tuple(q[1]))] = len(data) + j

    def gi(arg):
        return idx[(arg[0], tuple(arg[1]))]

    lines, meas_order = [], []
    for c in d["commands"]:
        t = c["op"]["type"]
        a = c["args"]
        if t == "Barrier":
            continue
        elif t == "H":
            lines.append(("H", [gi(a[0])]))
        elif t == "CX":
            lines.append(("CX", [gi(a[0]), gi(a[1])]))
        elif t == "Measure":
            q = gi(a[0])
            lines.append(("M", [q]))
            meas_order.append(q)
        else:
            raise ValueError(f"unexpected op {t!r}")

    out = []
    for g, qs in lines:
        if out and out[-1][0] == g and g in ("H", "M"):
            out[-1][1].extend(qs)
        else:
            out.append([g, list(qs)])
    text = "\n".join(f"{g} " + " ".join(map(str, qs)) for g, qs in out) + "\n"
    return (
        text,
        len(data),
        [len(data) + j for j in range(len(anc))],
        {
            "n_qubits": len(d["qubits"]),
            "meas_order": meas_order,
        },
    )


def pytket_to_stim(path):
    """Convenience: convert a pytket circuit dict file on disk to STIM."""
    return dict_to_stim(load_pytket_dict(open(path).read()))


if __name__ == "__main__":
    import sys

    t, n, anc, _ = pytket_to_stim(sys.argv[1])
    print(t)
    print(f"# n_data={n} ancillas={anc}")
