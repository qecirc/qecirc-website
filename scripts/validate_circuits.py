"""
Validate encoding and state-prep circuits against stored code check matrices.

Iterates over all circuit YAML files in data_yaml/circuits/, identifies encoding
and state-preparation circuits (via tags), and verifies correctness:

  - Encoding: validate_encoding (circuit maps |0...0⟩ to the code space)
  - State-prep: validate_state_prep (all stabilizers satisfied)

Usage:
    uv run python scripts/validate_circuits.py
    uv run python scripts/validate_circuits.py --data-dir data_yaml
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
import yaml  # noqa: E402

from scripts.add_circuit.circuit_validate import (  # noqa: E402
    validate_encoding,
    validate_state_prep,
)


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


def validate_all(data_dir: str = "data_yaml") -> list[CircuitResult]:
    data_path = Path(data_dir)
    circuits_dir = data_path / "circuits"
    codes_dir = data_path / "codes"
    results: list[CircuitResult] = []

    for circ_yaml_path in sorted(circuits_dir.glob("*.yaml")):
        stem = circ_yaml_path.stem
        circ_data = yaml.safe_load(circ_yaml_path.read_text())
        tags = circ_data.get("tags", [])

        # Determine circuit type from tags
        if "encoding" in tags:
            circuit_type = "encoding"
        elif "state-preparation" in tags:
            circuit_type = "state-preparation"
        else:
            results.append(CircuitResult(stem=stem, circuit_type="skipped"))
            continue

        result = CircuitResult(stem=stem, circuit_type=circuit_type)

        # Extract code slug from filename
        code_slug = stem.split("--")[0]
        code_yaml_path = codes_dir / f"{code_slug}.yaml"

        if not code_yaml_path.exists():
            result.checks.append(
                CheckResult("load_code", "error", f"Code YAML not found: {code_yaml_path}")
            )
            results.append(result)
            continue

        code_data = yaml.safe_load(code_yaml_path.read_text())

        # CSS path is required for the existing validators.
        if code_data.get("hx") is None or code_data.get("hz") is None:
            if code_data.get("h") is not None:
                result.checks.append(
                    CheckResult(
                        "load_code",
                        "skipped",
                        "non-CSS validation not yet supported (only encoding/state-prep validators for CSS)",
                    )
                )
            else:
                result.checks.append(
                    CheckResult("load_code", "error", "Code YAML missing both hx/hz and h")
                )
            results.append(result)
            continue

        Hx = np.array(code_data["hx"], dtype=int)
        Hz = np.array(code_data["hz"], dtype=int)

        # Load STIM body
        stim_path = circ_yaml_path.with_suffix(".stim")
        if not stim_path.exists():
            result.checks.append(
                CheckResult("load_stim", "error", f"STIM file not found: {stim_path}")
            )
            results.append(result)
            continue

        circuit_text = stim_path.read_text()

        # Run checks
        if circuit_type == "encoding":
            _check_encoding(result, circuit_text, Hx, Hz)
        elif circuit_type == "state-preparation":
            _check_state_prep(result, circuit_text, Hx, Hz)

        results.append(result)

    return results


def _check_encoding(
    result: CircuitResult,
    circuit_text: str,
    Hx: np.ndarray,
    Hz: np.ndarray,
) -> None:
    try:
        outcome = validate_encoding(circuit_text, Hx, Hz)
        if outcome == "passed":
            result.checks.append(CheckResult("validate_encoding", "passed"))
        else:
            result.checks.append(CheckResult("validate_encoding", "failed", outcome))
    except Exception as e:
        result.checks.append(CheckResult("validate_encoding", "error", str(e)))


def _check_state_prep(
    result: CircuitResult,
    circuit_text: str,
    Hx: np.ndarray,
    Hz: np.ndarray,
) -> None:
    try:
        outcome = validate_state_prep(circuit_text, Hx, Hz)
        if outcome == "passed":
            result.checks.append(CheckResult("validate_state_prep", "passed"))
        else:
            result.checks.append(CheckResult("validate_state_prep", "failed", outcome))
    except Exception as e:
        result.checks.append(CheckResult("validate_state_prep", "error", str(e)))


def print_results(results: list[CircuitResult]) -> None:
    checked = [r for r in results if r.circuit_type != "skipped"]
    skipped = [r for r in results if r.circuit_type == "skipped"]
    passed = [r for r in checked if r.passed]
    failed = [r for r in checked if not r.passed]

    for r in results:
        if r.circuit_type == "skipped":
            continue
        print(f"\n  {r.stem} [{r.circuit_type}]")
        for c in r.checks:
            status_icon = {"passed": "ok", "failed": "FAIL", "error": "ERROR", "skipped": "skip"}[c.status]
            line = f"    {c.name}: {status_icon}"
            if c.detail:
                line += f" ({c.detail})"
            print(line)

    print(
        f"\nSummary: {len(checked)} checked, {len(passed)} passed, "
        f"{len(failed)} failed, {len(skipped)} skipped"
    )


def main():
    parser = argparse.ArgumentParser(description="Validate circuits against stored check matrices")
    parser.add_argument("--data-dir", default="data_yaml", help="Path to data_yaml directory")
    args = parser.parse_args()

    print(f"Validating circuits in {args.data_dir}/...")
    results = validate_all(args.data_dir)
    print_results(results)

    failed = [r for r in results if r.circuit_type != "skipped" and not r.passed]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
