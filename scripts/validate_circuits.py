"""
Validate encoding and state-prep circuits against stored code check matrices.

Iterates over all circuit YAML files in data_yaml/circuits/, identifies encoding
and state-preparation circuits (via tags), and verifies correctness against the
code's symplectic ``h`` — CSS and non-CSS codes alike:

  - Encoding: validate_encoding_h (circuit maps |0...0⟩ to the code space)
            + logical_input_count (the encoder has exactly k free inputs)
  - State-prep: validate_state_prep_h (all stabilizers satisfied)
              + logical_basis (prepares the basis its logical-state tag claims;
                CSS codes only)
  - Logical gate: validate_logical_gate_h (unitary circuit preserves the
                  stabilizer group and induces the logical Clifford claimed
                  by its logical_action field)

Results are cached in .cache/validate-circuits.json keyed by the content of
every input (circuit YAML, STIM body, code YAML) plus a fingerprint of the
validator sources, so re-runs only recompute circuits whose inputs changed.
Pass --no-cache to force a full recompute.

Usage:
    uv run python scripts/validate_circuits.py
    uv run python scripts/validate_circuits.py --data-dir data_yaml
    uv run python scripts/validate_circuits.py --no-cache
"""

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Ensure project root is on sys.path so `scripts.add_circuit` is importable
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import numpy as np  # noqa: E402
import stim  # noqa: E402
import yaml  # noqa: E402

from scripts.add_circuit.annotate import logical_input_qubits  # noqa: E402
from scripts.add_circuit.circuit_validate import (  # noqa: E402
    _widen,
    validate_encoding_h,
    validate_logical_gate_h,
    validate_state_prep_h,
)
from scripts.add_circuit.code_identify import split_h_to_css  # noqa: E402
from scripts.add_circuit.state_prep import logical_basis_of  # noqa: E402
from scripts.result_cache import ResultCache, source_fingerprint, text_or_missing  # noqa: E402

# logical-state tag -> the basis the prepared state must live in.
_TAG_BASIS = {"zero": "z", "one": "z", "plus": "x", "minus": "x"}

# C-backed loader when available: ~15x faster over the whole corpus, and this
# script parses every circuit YAML even on a fully-warm cache run.
_FastLoader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def _load_yaml(text: str):
    return yaml.load(text, Loader=_FastLoader)


DEFAULT_CACHE_PATH = Path(_PROJECT_ROOT) / ".cache" / "validate-circuits.json"

# Every module whose logic determines a validation verdict. Their combined
# hash is mixed into each cache key, so editing any of them invalidates the
# whole cache automatically — no version constant to bump.
_SOURCE_DEPS = [
    Path(__file__),
    Path(_PROJECT_ROOT) / "scripts" / "add_circuit" / "annotate.py",
    Path(_PROJECT_ROOT) / "scripts" / "add_circuit" / "circuit_validate.py",
    Path(_PROJECT_ROOT) / "scripts" / "add_circuit" / "code_identify.py",
    Path(_PROJECT_ROOT) / "scripts" / "add_circuit" / "state_prep.py",
]


def open_cache(path: Path = DEFAULT_CACHE_PATH) -> ResultCache:
    return ResultCache(path, source_fingerprint(*_SOURCE_DEPS))


@dataclass
class CheckResult:
    name: str
    status: str  # "passed" | "failed" | "error" | "skipped"
    detail: str = ""


@dataclass
class CircuitResult:
    stem: str
    circuit_type: str  # "encoding" | "state-preparation" | "skipped"
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        # Circuit passes if all checks are "passed" and there are checks (not all-skipped)
        if not self.checks:
            return False
        return all(c.status in ("passed", "skipped") for c in self.checks) and any(
            c.status == "passed" for c in self.checks
        )

    @property
    def is_skipped(self) -> bool:
        # Skipped = no runnable validation for this circuit: it lacks a
        # functionality tag, or every check was skipped. These must not count as
        # failures. Note the validators themselves no longer skip on non-CSS
        # codes — they check the symplectic h directly.
        return self.circuit_type == "skipped" or (
            bool(self.checks) and all(c.status == "skipped" for c in self.checks)
        )


def _to_cacheable(result: CircuitResult) -> dict:
    return {
        "circuit_type": result.circuit_type,
        "checks": [[c.name, c.status, c.detail] for c in result.checks],
    }


def _from_cacheable(stem: str, data: dict) -> CircuitResult:
    return CircuitResult(
        stem=stem,
        circuit_type=data["circuit_type"],
        checks=[CheckResult(*c) for c in data["checks"]],
    )


def validate_all(
    data_dir: str = "data_yaml", cache: ResultCache | None = None
) -> list[CircuitResult]:
    data_path = Path(data_dir)
    circuits_dir = data_path / "circuits"
    codes_dir = data_path / "codes"
    results: list[CircuitResult] = []
    seen_stems: set[str] = set()
    code_texts: dict[str, str] = {}  # slug -> YAML text; ~30 codes serve ~900 circuits

    for circ_yaml_path in sorted(circuits_dir.glob("*.yaml")):
        stem = circ_yaml_path.stem
        circ_text = circ_yaml_path.read_text()
        circ_data = _load_yaml(circ_text)
        tags = circ_data.get("tags", [])

        # Determine circuit type from tags
        if "encoding" in tags:
            circuit_type = "encoding"
        elif "state-preparation" in tags:
            circuit_type = "state-preparation"
        elif "logical-gate" in tags:
            circuit_type = "logical-gate"
        else:
            results.append(CircuitResult(stem=stem, circuit_type="skipped"))
            continue

        # Extract code slug from filename
        code_slug = stem.split("--")[0]
        code_yaml_path = codes_dir / f"{code_slug}.yaml"
        stim_path = circ_yaml_path.with_suffix(".stim")

        # The verdict is a pure function of these three texts (plus validator
        # sources, hashed into the cache fingerprint), so an unchanged key
        # means the stored result is exact — replay it.
        if cache is not None:
            seen_stems.add(stem)
            if code_slug not in code_texts:
                code_texts[code_slug] = text_or_missing(code_yaml_path)
            key = cache.key(circ_text, text_or_missing(stim_path), code_texts[code_slug])
            hit = cache.get(stem, key)
            if hit is not None:
                results.append(_from_cacheable(stem, hit))
                continue

        result = _validate_one(stem, circuit_type, circ_data, tags, code_yaml_path, stim_path)
        if cache is not None:
            cache.put(stem, key, _to_cacheable(result))
        results.append(result)

    if cache is not None:
        cache.save(prune_to=seen_stems)
    return results


def _validate_one(
    stem: str,
    circuit_type: str,
    circ_data: dict,
    tags: list[str],
    code_yaml_path: Path,
    stim_path: Path,
) -> CircuitResult:
    result = CircuitResult(stem=stem, circuit_type=circuit_type)

    if not code_yaml_path.exists():
        result.checks.append(
            CheckResult("load_code", "error", f"Code YAML not found: {code_yaml_path}")
        )
        return result

    code_data = _load_yaml(code_yaml_path.read_text())

    # The validators check the symplectic h directly, so no CSS split is
    # needed — non-CSS codes take the same path as CSS ones.
    if code_data.get("h") is None:
        result.checks.append(CheckResult("load_code", "error", "Code YAML missing h"))
        return result

    n = code_data.get("n")
    if n is None:
        result.checks.append(CheckResult("load_code", "error", "Code YAML missing n"))
        return result

    h = np.array(code_data["h"], dtype=int)

    if not stim_path.exists():
        result.checks.append(CheckResult("load_stim", "error", f"STIM file not found: {stim_path}"))
        return result

    circuit_text = stim_path.read_text()

    # Run checks
    if circuit_type == "encoding":
        _check_encoding(result, circuit_text, h, n)
        _check_logical_input_count(result, circuit_text, h, n, code_data.get("k"))
    elif circuit_type == "state-preparation":
        _check_state_prep(result, circuit_text, h, n)
        _check_logical_basis(result, circuit_text, h, n, code_data.get("d"), tags)
    elif circuit_type == "logical-gate":
        _check_logical_gate(
            result,
            circuit_text,
            h,
            n,
            code_data.get("logical"),
            circ_data.get("logical_action"),
        )

    return result


def _check_encoding(result: CircuitResult, circuit_text: str, h: np.ndarray, n: int) -> None:
    try:
        outcome = validate_encoding_h(circuit_text, h, n)
        if outcome == "passed":
            result.checks.append(CheckResult("validate_encoding", "passed"))
        else:
            result.checks.append(CheckResult("validate_encoding", "failed", outcome))
    except Exception as e:
        result.checks.append(CheckResult("validate_encoding", "error", str(e)))


def _check_state_prep(result: CircuitResult, circuit_text: str, h: np.ndarray, n: int) -> None:
    try:
        outcome = validate_state_prep_h(circuit_text, h, n)
        if outcome == "passed":
            result.checks.append(CheckResult("validate_state_prep", "passed"))
        else:
            result.checks.append(CheckResult("validate_state_prep", "failed", outcome))
    except Exception as e:
        result.checks.append(CheckResult("validate_state_prep", "error", str(e)))


def _check_logical_basis(
    result: CircuitResult,
    circuit_text: str,
    h: np.ndarray,
    n: int,
    d: int | None,
    tags: list[str],
) -> None:
    """A state-prep must prepare a logical state in the basis its tag claims.

    Complementary to the codespace check, which is basis-blind: every codeword is
    a +1 eigenstate of every stabilizer, so ``validate_state_prep`` cannot tell
    |0>_L from |+>_L. Only the logical operators distinguish them.

    Basis, not the full 0/1 label: ``codes.logical`` is sign-free, so which
    eigenstate is called |0> is not determined by stored data (see
    :func:`logical_state_of`'s caveat). The basis is.

    CSS only, on principle rather than as a gap: for a non-CSS code both logical
    operators are mixed-type Paulis, so which is X-bar and which is Z-bar is a
    labeling convention and the basis inherits that arbitrariness. There is no
    convention-independent answer to check against.
    """
    tag = next((t.split(":", 1)[1] for t in tags if t.startswith("logical-state:")), "")
    if not tag:
        result.checks.append(CheckResult("logical_basis", "skipped", "no logical-state: tag"))
        return
    expected = _TAG_BASIS.get(tag)
    if expected is None:
        result.checks.append(
            CheckResult("logical_basis", "skipped", f"logical-state:{tag} names no basis")
        )
        return
    css = split_h_to_css(h, n)
    if css is None:
        result.checks.append(
            CheckResult(
                "logical_basis",
                "skipped",
                "non-CSS: X-bar/Z-bar labeling is a convention, so the basis is not well-defined",
            )
        )
        return
    if d is None:
        result.checks.append(CheckResult("logical_basis", "error", "Code YAML missing d"))
        return
    try:
        got = logical_basis_of(circuit_text, n, d, Hx=css[0], Hz=css[1])
        if got == expected:
            result.checks.append(CheckResult("logical_basis", "passed"))
        elif got == "unknown":
            result.checks.append(
                CheckResult(
                    "logical_basis",
                    "failed",
                    f"failed: tagged logical-state:{tag} (basis {expected!r}), but the circuit "
                    "prepares no uniform single-basis logical state",
                )
            )
        else:
            result.checks.append(
                CheckResult(
                    "logical_basis",
                    "failed",
                    f"failed: tagged logical-state:{tag} (basis {expected!r}), "
                    f"but the circuit prepares a {got!r}-basis state",
                )
            )
    except Exception as e:
        result.checks.append(CheckResult("logical_basis", "error", str(e)))


def _check_logical_gate(
    result: CircuitResult,
    circuit_text: str,
    h: np.ndarray,
    n: int,
    logical: "list | None",
    logical_action: "str | None",
) -> None:
    """A logical-gate circuit must preserve the stabilizer group and induce the
    logical Clifford its ``logical_action`` field claims.

    Both properties are checked at the binary symplectic level (mod stabilizers,
    signs free) — a logical gate is only defined up to logical Paulis, and the
    stored matrices carry no sign frame. See :func:`validate_logical_gate_h`.
    """
    if logical is None:
        result.checks.append(
            CheckResult("validate_logical_gate", "error", "Code YAML missing logical")
        )
        return
    if not logical_action:
        result.checks.append(
            CheckResult(
                "validate_logical_gate",
                "error",
                "logical-gate circuit has no logical_action field to check against",
            )
        )
        return
    try:
        outcome = validate_logical_gate_h(
            circuit_text, h, np.array(logical, dtype=int), n, logical_action
        )
        if outcome == "passed":
            result.checks.append(CheckResult("validate_logical_gate", "passed"))
        else:
            result.checks.append(CheckResult("validate_logical_gate", "failed", outcome))
    except Exception as e:
        result.checks.append(CheckResult("validate_logical_gate", "error", str(e)))


def _check_logical_input_count(
    result: CircuitResult,
    circuit_text: str,
    h: np.ndarray,
    n: int,
    k: int | None,
) -> None:
    """An encoder must expose exactly k free logical inputs.

    Basis-independent, and complementary to the codespace check: it looks at the
    encoder's *inputs* rather than its output on |0...0>, so it catches circuits
    that land in a valid codespace but of the wrong code. That is exactly how the
    Gottesman [[8,3,3]] gate-optimized encoder (#134) was caught — it implied 7
    logical inputs where k=3.
    """
    if k is None:
        result.checks.append(CheckResult("logical_input_count", "error", "Code YAML missing k"))
        return
    try:
        # Widen to n first, as the codespace check does: an encoder that never
        # touches its last data qubits is narrower than the code, and
        # logical_input_qubits reports a width mismatch as "not derivable" —
        # i.e. it would silently skip rather than check.
        circ = _widen(stim.Circuit(circuit_text), n)
        inputs = logical_input_qubits(circ, h, n)
        if inputs is None:
            result.checks.append(
                CheckResult(
                    "logical_input_count",
                    "skipped",
                    "inputs not derivable (no tableau and no resets)",
                )
            )
        elif len(inputs) != k:
            result.checks.append(
                CheckResult(
                    "logical_input_count",
                    "failed",
                    f"failed: circuit implies {len(inputs)} logical inputs {inputs}, "
                    f"but the code has k={k}",
                )
            )
        else:
            result.checks.append(CheckResult("logical_input_count", "passed"))
    except Exception as e:
        result.checks.append(CheckResult("logical_input_count", "error", str(e)))


def print_results(results: list[CircuitResult], cache: ResultCache | None = None) -> None:
    checked = [r for r in results if not r.is_skipped]
    skipped = [r for r in results if r.is_skipped]
    passed = [r for r in checked if r.passed]
    failed = [r for r in checked if not r.passed]

    for r in results:
        if r.circuit_type == "skipped":
            continue
        print(f"\n  {r.stem} [{r.circuit_type}]")
        status_icons = {"passed": "ok", "failed": "FAIL", "error": "ERROR", "skipped": "skip"}
        for c in r.checks:
            status_icon = status_icons[c.status]
            line = f"    {c.name}: {status_icon}"
            if c.detail:
                line += f" ({c.detail})"
            print(line)

    cached = f" ({cache.hits} from cache)" if cache is not None and cache.hits else ""
    print(
        f"\nSummary: {len(checked)} checked{cached}, {len(passed)} passed, "
        f"{len(failed)} failed, {len(skipped)} skipped"
    )


def main():
    parser = argparse.ArgumentParser(description="Validate circuits against stored check matrices")
    parser.add_argument("--data-dir", default="data_yaml", help="Path to data_yaml directory")
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Recompute every circuit instead of replaying cached results",
    )
    args = parser.parse_args()

    cache = None if args.no_cache else open_cache()
    print(f"Validating circuits in {args.data_dir}/...")
    results = validate_all(args.data_dir, cache=cache)
    print_results(results, cache=cache)

    failed = [r for r in results if not r.is_skipped and not r.passed]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
