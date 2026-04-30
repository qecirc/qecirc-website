"""Tests for yaml_helpers.write_file atomicity and encoding."""

from pathlib import Path

from scripts.add_circuit.yaml_helpers import write_file


def test_write_file_explicit_utf8(tmp_path: Path) -> None:
    """write_file must write UTF-8 regardless of platform default encoding."""
    target = tmp_path / "ünïcödé.yaml"
    write_file(target, "name: étoilé\n", quiet=True)
    assert target.read_bytes() == b"name: \xc3\xa9toil\xc3\xa9\n"


def test_write_file_atomic_no_partial(tmp_path: Path, monkeypatch) -> None:
    """If the write fails mid-way, the destination must be untouched."""
    target = tmp_path / "out.yaml"
    target.write_text("original\n", encoding="utf-8")

    import os

    original_replace = os.replace

    def boom(src, dst):
        raise RuntimeError("simulated mid-write crash")

    monkeypatch.setattr(os, "replace", boom)

    try:
        write_file(target, "new content\n", quiet=True)
    except RuntimeError:
        pass

    monkeypatch.setattr(os, "replace", original_replace)

    # Original content preserved; no partial write
    assert target.read_text(encoding="utf-8") == "original\n"
