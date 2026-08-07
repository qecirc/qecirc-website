"""The `npm run generate` CLI must write what `add_circuit` writes.

It used to assemble the files itself and drifted from the one write path: a
per-circuit `originals/<stem>.original.yaml` with no `original_matrices`
reference (`create_database.mjs` throws on exactly that shape), a `qec_id`
reallocated on every run, and one filename for every `--stim` when
`--circuit-name` was omitted. These pin the delegation.
"""

import json

import pytest
import yaml

from scripts.add_circuit.generate import main

# Steane code, self-dual.
_HX = [[1, 0, 1, 0, 1, 0, 1], [0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1]]
_ENCODER = "H 0\nH 1\nH 2\nCX 0 3 0 4 0 6 1 3 1 5 1 6 2 4 2 5 2 6\n"


def _run(tmp_path, *extra, names=("Standard Encoding",), stims=1):
    stim_path = tmp_path / "enc.stim"
    stim_path.write_text(_ENCODER)
    argv = [
        "--hx",
        json.dumps(_HX),
        "--hz",
        json.dumps(_HX),
        "--d",
        "3",
        "--code-name",
        "Steane Code",
        "--data-dir",
        str(tmp_path / "data_yaml"),
        "--stim",
        *([str(stim_path)] * stims),
        "--circuit-name",
        *names,
        *extra,
    ]
    return main(argv)


def _circuit_yaml(tmp_path, stem="steane-code--standard-encoding"):
    return yaml.safe_load((tmp_path / "data_yaml/circuits" / f"{stem}.yaml").read_text())


def test_matrices_are_written_by_reference_not_beside_the_circuit(tmp_path):
    """The shape `db:create` rejects: an `originals/<stem>.original.yaml` with
    no `original_matrices` key on the circuit."""
    assert _run(tmp_path) == 0
    originals = tmp_path / "data_yaml/circuits/originals"
    assert not list(originals.glob("*.original.yaml"))
    digest = _circuit_yaml(tmp_path)["original_matrices"]
    assert (tmp_path / "data_yaml/matrices" / f"{digest}.yaml").exists()


def test_qec_id_survives_a_rerun(tmp_path):
    """`qec_id` is permanent and never reused; the CLI used to allocate a fresh
    one on every run."""
    assert _run(tmp_path) == 0
    first = _circuit_yaml(tmp_path)["qec_id"]
    assert _run(tmp_path, "--overwrite") == 0
    assert _circuit_yaml(tmp_path)["qec_id"] == first


def test_an_existing_circuit_is_refused_without_overwrite(tmp_path, capsys):
    assert _run(tmp_path) == 0
    assert _run(tmp_path) == 1
    assert "already exists" in capsys.readouterr().err


def test_unnamed_circuits_cannot_collide_on_one_filename(tmp_path):
    with pytest.raises(SystemExit):
        _run(tmp_path, stims=2, names=("Only One Name",))


def test_dry_run_writes_nothing(tmp_path):
    assert _run(tmp_path, "--dry-run") == 0
    assert not (tmp_path / "data_yaml/circuits").exists()
