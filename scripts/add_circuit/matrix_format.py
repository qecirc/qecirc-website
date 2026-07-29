"""How a binary matrix is written into YAML, and read back.

Every matrix the library stores — a code's ``h`` and ``logical``, and the
original matrices a circuit was submitted against — is binary and, for the codes
that dominate the repo's size, mostly zero. Writing them as dense rows of 0s and
1s costs O(n²) characters regardless: the stored ``h`` is (n−k) × 2n, so the
quasi-cyclic lifted product code [[1428,184,≤24]] is 3.5M entries and 13.5 MB.

So above a size threshold the matrix is written as its **nonzero column indices**
per row instead:

.. code-block:: yaml

    h:
      rows: 1244
      cols: 2856
      nonzero:
        - [3, 17, 402]
        - [1, 88]

Below the threshold nothing changes — a matrix stays a plain list of rows. That
is deliberate: small codes are readable as dense rows, they are the ones a person
actually reads, and leaving them alone means introducing this format does not
rewrite every file in the repository.

The two encodings are distinguished by type, not by a flag: a list is dense, a
mapping is sparse. :func:`decode` accepts either, so a reader never has to know
which was used.
"""

from __future__ import annotations

from typing import Any, Union

import numpy as np

# Above this many entries (rows × cols) a matrix is written sparsely. Chosen so
# that every code in the library before the qLDPC imports stays dense — the
# largest was the unrotated surface code [[221,1,11]] at ~97k entries — and the
# codes that cost real disk space do not.
SPARSE_MIN_ENTRIES = 100_000


def encode(matrix: Any, *, threshold: int = SPARSE_MIN_ENTRIES) -> Union[list, dict]:
    """A matrix as it should be written to YAML.

    Returns a list of rows when the matrix is small, and the sparse mapping
    above ``threshold``. Values are reduced mod 2 — every matrix here is over
    GF(2), and storing anything else would be a bug in the caller.
    """
    m = np.asarray(matrix, dtype=int) % 2
    if m.ndim != 2:
        raise ValueError(f"expected a 2-D matrix, got shape {m.shape}")
    rows, cols = m.shape
    if rows * cols < threshold:
        return m.tolist()
    return {
        "rows": int(rows),
        "cols": int(cols),
        "nonzero": [[int(c) for c in np.flatnonzero(row)] for row in m],
    }


def decode(value: Any) -> np.ndarray:
    """A stored matrix as a dense ``numpy`` array, whichever encoding was used."""
    if isinstance(value, dict):
        rows, cols = int(value["rows"]), int(value["cols"])
        nonzero = value["nonzero"]
        if len(nonzero) != rows:
            raise ValueError(f"sparse matrix declares {rows} rows but lists {len(nonzero)}")
        m = np.zeros((rows, cols), dtype=int)
        for i, indices in enumerate(nonzero):
            for c in indices:
                if not 0 <= c < cols:
                    raise ValueError(f"column index {c} out of range for {rows}x{cols}")
                m[i, int(c)] = 1
        return m
    return np.asarray(value, dtype=int) % 2


def is_sparse(value: Any) -> bool:
    """True when a stored value uses the sparse encoding."""
    return isinstance(value, dict)
