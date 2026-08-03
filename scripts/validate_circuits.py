"""
Validate encoding, state-prep and syndrome-extraction circuits against stored
code check matrices.

Iterates over all circuit YAML files in data_yaml/circuits/, identifies the
circuit type (via tags), and verifies correctness against the code's symplectic
``h`` — CSS and non-CSS codes alike:

  - Encoding: validate_encoding_h (circuit maps |0...0⟩ to the code space)
            + logical_input_count (the encoder has exactly k free inputs)
  - State-prep: validate_state_prep_h (all stabilizers satisfied)
              + logical_basis (prepares the basis its logical-state tag claims;
                CSS codes only)
  - Syndrome extraction: validate_syndrome_extraction_h (the round measures
                exactly the stabilizer group and preserves the code state and
                its logicals)

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
import stim  # noqa: E402
import yaml  # noqa: E402

from scripts.add_circuit.annotate import logical_input_qubits  # noqa: E402
from scripts.add_circuit.circuit_validate import (  # noqa: E402
    _widen,
    validate_encoding_h,
    validate_state_prep_h,
    validate_syndrome_extraction_h,
)
from scripts.add_circuit.code_identify import split_h_to_css  # noqa: E402
from scripts.add_circuit.matrix_format import decode as decode_matrix  # noqa: E402
from scripts.add_circuit.state_prep import logical_basis_of  # noqa: E402

# logical-state tag -> the basis the prepared state must live in.
_TAG_BASIS = {"zero": "z", "one": "z", "plus": "x", "minus": "x"}


@dataclass
class CheckResult:
    name: str
    status: str  # "passed" | "failed" | "error" | "skipped"
    detail: str = ""


@dataclass
class CircuitResult:
    stem: str
    circuit_type: str  # "encoding" | "state-preparation" | "syndrome-extraction" | "skipped"
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
        elif "syndrome-extraction" in tags:
            circuit_type = "syndrome-extraction"
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

        # The validators check the symplectic h directly, so no CSS split is
        # needed — non-CSS codes take the same path as CSS ones.
        if code_data.get("h") is None:
            result.checks.append(CheckResult("load_code", "error", "Code YAML missing h"))
            results.append(result)
            continue

        n = code_data.get("n")
        if n is None:
            result.checks.append(CheckResult("load_code", "error", "Code YAML missing n"))
            results.append(result)
            continue

        h = decode_matrix(code_data["h"])

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
            _check_encoding(result, circuit_text, h, n)
            _check_logical_input_count(
                result,
                circuit_text,
                h,
                n,
                code_data.get("k"),
                code_data.get("gauge_qubits") or 0,
            )
        elif circuit_type == "state-preparation":
            _check_state_prep(result, circuit_text, h, n)
            _check_logical_basis(result, circuit_text, h, n, code_data.get("d"), tags)
        elif circuit_type == "syndrome-extraction":
            # Decoded here, like `h` above: a large code's `logical` is stored
            # sparsely, and handing the raw mapping to numpy is a TypeError.
            stored_logical = code_data.get("logical")
            _check_syndrome_extraction(
                result,
                circuit_text,
                h,
                n,
                None if stored_logical is None else decode_matrix(stored_logical),
            )

        results.append(result)

    return results


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


def _check_syndrome_extraction(
    result: CircuitResult,
    circuit_text: str,
    h: np.ndarray,
    n: int,
    logical: np.ndarray | None,
) -> None:
    """A syndrome-extraction round must measure exactly the stabilizer group and
    leave the encoded state — logicals included — alone.

    Unlike the prep/encoding checks this cannot be a codespace test: the round
    acts on an already-encoded state, so there is nothing to simulate it on. It
    is a *flow* check instead; see ``circuit_validate.measured_stabilizers`` for
    why the ancilla-to-stabilizer correspondence is derived rather than assumed.

    ``codes.logical`` is passed when present so ``L -> L`` is checked too. It is
    optional data, and its absence weakens the check rather than invalidating it,
    so a code without it is still checked on the stabilizers.
    """
    try:
        outcome = validate_syndrome_extraction_h(circuit_text, h, n, logical=logical)
        if outcome == "passed":
            result.checks.append(CheckResult("validate_syndrome_extraction", "passed"))
        else:
            result.checks.append(CheckResult("validate_syndrome_extraction", "failed", outcome))
    except Exception as e:
        result.checks.append(CheckResult("validate_syndrome_extraction", "error", str(e)))


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


def _check_logical_input_count(
    result: CircuitResult,
    circuit_text: str,
    h: np.ndarray,
    n: int,
    k: int | None,
    gauge_qubits: int = 0,
) -> None:
    """An encoder must expose exactly k free logical inputs, plus any gauge ones.

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
            # Terminal: `inputs` is what every line below counts, so falling
            # through raises TypeError on len(None), the blanket except turns
            # that into an "error" check, and a circuit that was merely
            # unanalysable FAILS the run — exit 1 in CI.
            result.checks.append(
                CheckResult(
                    "logical_input_count",
                    "skipped",
                    "inputs not derivable (no tableau and no resets)",
                )
            )
            return
        # A subsystem code's encoder takes the gauge qubits as inputs too, so
        # the count to expect is `k + gauge_qubits` — five for Bacon-Shor
        # [[9,1,3]]. Both numbers come from the stored code, so a `k` that
        # disagrees with the circuit is still caught.
        expected = k + gauge_qubits
        if len(inputs) != expected:
            wanted = (
                f"k={k}"
                if not gauge_qubits
                else f"{expected} — k={k} plus {gauge_qubits} gauge qubits"
            )
            result.checks.append(
                CheckResult(
                    "logical_input_count",
                    "failed",
                    f"failed: circuit implies {len(inputs)} logical inputs {inputs}, "
                    f"but the code has {wanted}",
                )
            )
        else:
            result.checks.append(CheckResult("logical_input_count", "passed"))
    except Exception as e:
        result.checks.append(CheckResult("logical_input_count", "error", str(e)))


def print_results(results: list[CircuitResult]) -> None:
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

    failed = [r for r in results if not r.is_skipped and not r.passed]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
