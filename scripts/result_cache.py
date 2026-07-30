"""Content-addressed result cache for full-scan maintenance scripts.

``validate_circuits.py`` and ``annotate_circuits.py`` recompute a pure function
of file contents for every circuit in the library, so their cost grows with the
library rather than with the change being made. This cache makes re-runs
proportional to the diff: each circuit's result is stored under a key derived
from every input that determines it, and a re-run replays stored results for
circuits whose key is unchanged.

Correct by construction, not by invalidation policy:

- The key hashes the *contents* of all inputs (circuit YAML, STIM body, code
  YAML, ...), so any edit — however irrelevant it looks — recomputes that
  circuit. Over-invalidation costs one circuit's check; under-invalidation is
  impossible as long as callers hash everything the result depends on.
- The key also mixes in a fingerprint of the script's own source modules
  (:func:`source_fingerprint`), so changing validator/annotator logic
  invalidates everything automatically. There is no version constant to forget
  to bump.
- A stale or corrupt cache file therefore can never produce a wrong result —
  at worst it produces a full recompute. This is also what makes the cache
  safe to restore across CI runs via ``actions/cache``.

The cache lives in ``.cache/`` (gitignored). Entries are pruned to the stems
seen in the latest run, so renames and deletions do not accumulate.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path

MISSING = "<missing>"  # sentinel for "input file does not exist" (≠ empty file)


def source_fingerprint(*files: Path) -> str:
    """Hash of the given source files' bytes — mix into every cache key so
    logic changes self-invalidate."""
    h = hashlib.sha256()
    for f in files:
        h.update(f.name.encode())
        h.update(f.read_bytes())
    return h.hexdigest()


def text_or_missing(path: Path) -> str:
    """File content for key-building, distinguishing absent from empty."""
    return path.read_text(encoding="utf-8") if path.exists() else MISSING


class ResultCache:
    """Maps a stem to (content key, JSON-serializable result)."""

    def __init__(self, path: Path, fingerprint: str):
        self.path = path
        self.fingerprint = fingerprint
        self.hits = 0
        self.misses = 0
        self._entries: dict[str, dict] = {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                self._entries = data
        except (OSError, ValueError):
            pass  # absent or corrupt cache = cold cache

    def key(self, *parts: str) -> str:
        h = hashlib.sha256(self.fingerprint.encode())
        for p in parts:
            h.update(b"\x00")
            h.update(p.encode())
        return h.hexdigest()

    def get(self, stem: str, key: str):
        """The stored result for `stem`, or None if absent or inputs changed."""
        entry = self._entries.get(stem)
        if entry and entry.get("key") == key:
            self.hits += 1
            return entry["result"]
        self.misses += 1
        return None

    def put(self, stem: str, key: str, result) -> None:
        self._entries[stem] = {"key": key, "result": result}

    def save(self, prune_to: set[str] | None = None) -> None:
        """Atomically persist, dropping stems not in `prune_to` (if given)."""
        if prune_to is not None:
            self._entries = {s: e for s, e in self._entries.items() if s in prune_to}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self._entries, f)
            os.replace(tmp, self.path)
        except BaseException:
            os.unlink(tmp)
            raise
