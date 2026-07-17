"""Tests for the content-addressed result cache and its validate/annotate wiring."""

from pathlib import Path

import yaml

from scripts.result_cache import MISSING, ResultCache, source_fingerprint, text_or_missing
from scripts.tests.test_validate_circuits import _FIVE_QUBIT_ENCODER, FIVE_QUBIT_CODE
from scripts.validate_circuits import validate_all


def _layout(tmp_path):
    for sub in ("tools", "codes", "circuits"):
        (tmp_path / sub).mkdir()
    (tmp_path / "codes" / "test-code.yaml").write_text(yaml.dump(FIVE_QUBIT_CODE))
    circ_yaml = {"qec_id": 9999, "name": "Stub", "source": "test", "tags": ["encoding"]}
    (tmp_path / "circuits" / "test-code--stub.yaml").write_text(yaml.dump(circ_yaml))
    (tmp_path / "circuits" / "test-code--stub.stim").write_text(_FIVE_QUBIT_ENCODER)


def _cache(tmp_path) -> ResultCache:
    return ResultCache(tmp_path / "cache.json", fingerprint="test-fp")


# --- ResultCache unit behavior ---


def test_roundtrip_and_persistence(tmp_path):
    cache = _cache(tmp_path)
    key = cache.key("a", "b")
    cache.put("stem", key, {"x": 1})
    cache.save()

    reloaded = _cache(tmp_path)
    assert reloaded.get("stem", key) == {"x": 1}


def test_fingerprint_change_invalidates(tmp_path):
    cache = _cache(tmp_path)
    cache.put("stem", cache.key("a"), "result")
    cache.save()

    bumped = ResultCache(tmp_path / "cache.json", fingerprint="other-fp")
    assert bumped.get("stem", bumped.key("a")) is None


def test_key_sensitive_to_every_part(tmp_path):
    cache = _cache(tmp_path)
    assert cache.key("a", "b") != cache.key("a", "c")
    assert cache.key("a", "b") != cache.key("ab", "")  # parts are delimited


def test_corrupt_cache_file_is_cold_not_fatal(tmp_path):
    (tmp_path / "cache.json").write_text("{not json")
    cache = _cache(tmp_path)
    assert cache.get("stem", cache.key("a")) is None


def test_prune_drops_unseen_stems(tmp_path):
    cache = _cache(tmp_path)
    cache.put("kept", cache.key("a"), 1)
    cache.put("dropped", cache.key("a"), 2)
    cache.save(prune_to={"kept"})

    reloaded = _cache(tmp_path)
    assert reloaded.get("kept", reloaded.key("a")) == 1
    assert reloaded.get("dropped", reloaded.key("a")) is None


def test_text_or_missing_distinguishes_absent_from_empty(tmp_path):
    empty = tmp_path / "empty.txt"
    empty.write_text("")
    assert text_or_missing(empty) == ""
    assert text_or_missing(tmp_path / "absent.txt") == MISSING
    assert text_or_missing(empty) != text_or_missing(tmp_path / "absent.txt")


def test_source_fingerprint_tracks_content(tmp_path):
    f = tmp_path / "mod.py"
    f.write_text("a = 1")
    before = source_fingerprint(f)
    f.write_text("a = 2")
    assert source_fingerprint(f) != before


# --- validate_circuits integration ---


def test_second_run_replays_identical_results(tmp_path):
    _layout(tmp_path)
    cache = _cache(tmp_path)

    cold = validate_all(data_dir=str(tmp_path), cache=cache)
    assert cache.hits == 0 and cache.misses == 1

    warm = validate_all(data_dir=str(tmp_path), cache=cache)
    assert cache.hits == 1
    assert [
        (r.stem, r.circuit_type, [(c.name, c.status, c.detail) for c in r.checks]) for r in cold
    ] == [(r.stem, r.circuit_type, [(c.name, c.status, c.detail) for c in r.checks]) for r in warm]


def test_editing_stim_invalidates_that_circuit(tmp_path):
    _layout(tmp_path)
    cache = _cache(tmp_path)
    validate_all(data_dir=str(tmp_path), cache=cache)

    (tmp_path / "circuits" / "test-code--stub.stim").write_text("I 0 1 2 3 4")
    results = validate_all(data_dir=str(tmp_path), cache=cache)
    assert cache.hits == 0 and cache.misses == 2  # the edited circuit missed both runs
    assert not results[0].passed  # and was genuinely revalidated


def test_editing_code_yaml_invalidates_its_circuits(tmp_path):
    _layout(tmp_path)
    cache = _cache(tmp_path)
    validate_all(data_dir=str(tmp_path), cache=cache)
    misses_before = cache.misses

    code = dict(FIVE_QUBIT_CODE, k=2)  # wrong k -> logical_input_count must fail now
    (tmp_path / "codes" / "test-code.yaml").write_text(yaml.dump(code))
    results = validate_all(data_dir=str(tmp_path), cache=cache)
    assert cache.misses == misses_before + 1
    checks = {c.name: c for c in results[0].checks}
    assert checks["logical_input_count"].status == "failed"


def test_deleted_circuit_is_pruned_on_save(tmp_path):
    _layout(tmp_path)
    cache_path = tmp_path / "cache.json"
    cache = ResultCache(cache_path, fingerprint="test-fp")
    validate_all(data_dir=str(tmp_path), cache=cache)

    for suffix in (".yaml", ".stim"):
        (tmp_path / "circuits" / f"test-code--stub{suffix}").unlink()
    validate_all(data_dir=str(tmp_path), cache=cache)

    reloaded = Path(cache_path).read_text()
    assert "test-code--stub" not in reloaded
