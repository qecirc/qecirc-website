"""Build symplectic anchor matrices (h, logical) from the flag-at-origin repo's
pure-Python stabilizer definitions (lifted into faot_stabilizers.py)."""

import numpy as np
from stabilizers import get_stabilisers_and_logicals


def _rows(entries, n):
    rows = []
    for e in entries:
        r = np.zeros(2 * n, dtype=int)
        for q, p in e["paulis"].items():
            if p in ("X", "Y"):
                r[q] = 1
            if p in ("Z", "Y"):
                r[n + q] = 1
        rows.append(r)
    return np.array(rows, dtype=int)


def gf2_rank(M):
    M = M.copy() % 2
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if M[i, c]:
                piv = i
                break
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        for i in range(rows):
            if i != r and M[i, c]:
                M[i] ^= M[r]
        r += 1
    return r


def anchor_for(n, k, d):
    stabs, logs = get_stabilisers_and_logicals((n, k, d))
    H = _rows(stabs, n)
    L = _rows(logs, n)
    return H, L


if __name__ == "__main__":
    codes = [
        (7, 1, 3),
        (9, 1, 3),
        (17, 1, 5),
        (20, 2, 6),
        (23, 1, 7),
        (25, 1, 5),
        (31, 1, 7),
        (47, 1, 11),
        (49, 1, 5),
        (49, 1, 7),
        (49, 1, 9),
        (71, 1, 11),
        (81, 1, 9),
        (95, 1, 7),
    ]
    for n, k, d in codes:
        H, L = anchor_for(n, k, d)
        Hx, Hz = H[:, :n], H[:, n:]
        css_cross = (Hx @ Hz.T) % 2
        rank = gf2_rank(H)
        css = not css_cross.any()
        print(
            f"[[{n},{k},{d}]] H={H.shape} rank={rank} (n-k={n - k}) "
            f"CSS={css} L={L.shape}(2k={2 * k})"
        )
