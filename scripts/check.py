# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""The oracle: one command that says whether the repository is in a correct state.

Run from the repository root with `uv run scripts/check.py`. It exits with 0
only if no check fails. Checks whose code does not exist yet are reported as
INACTIVO and switch themselves on when that code appears.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from oracle import (  # imported after the path is set just above
    checks_code,
    checks_hygiene,
    checks_purity,
    checks_specs,
    checks_stack,
    checks_trace,
    report,
    specgate,
)
from oracle.repo import OracleError, listed_files, run, tail

ASSUMPTIONS = ("ai-workspace", "00-analisis", "supuestos.md")
SELF_TESTS = [sys.executable, "-m", "unittest", "discover", "-s", "scripts/tests", "-t", "scripts"]


def _guarded(block: str, check: Callable[[], report.Result]) -> report.Result:
    """Run a check; if it cannot be carried out, that is a failure, never a pass."""
    try:
        return check()
    except OracleError as error:
        return report.failed(block, f"No se pudo ejecutar {check.__name__}", [str(error)])


def _self_tests() -> report.Result:
    name = "Tests del oráculo y del hook (unittest)"
    code, output = run(SELF_TESTS, ROOT)
    if code != 0:
        return report.failed("Scripts", name, [tail(output, 25)])
    summary = [line for line in output.splitlines() if line.startswith("Ran ")]
    return report.passed("Scripts", name, summary)


def _repository_checks() -> list[Callable[[], report.Result]]:
    files = listed_files(ROOT)
    specs = specgate.specs_dir(ROOT)
    return [
        lambda: checks_specs.check_gate(ROOT, files),
        lambda: checks_specs.check_index(specs),
        lambda: checks_specs.check_assumptions(specs, ROOT.joinpath(*ASSUMPTIONS)),
        lambda: checks_code.check_file_sizes(ROOT, files),
        lambda: checks_code.check_functions(ROOT, files),
        lambda: checks_code.check_suppressions(ROOT, files),
        lambda: checks_code.check_skipped_tests(ROOT, files),
        lambda: checks_hygiene.check_trailers(ROOT),
        lambda: checks_hygiene.check_line_endings(ROOT),
        lambda: checks_hygiene.check_private(ROOT),
        _self_tests,
    ]


def collect(e2e: bool, strict_trace: bool) -> list[report.Result]:
    """Run every check, in the order of the report."""
    try:
        checks = _repository_checks()
    except OracleError as error:
        return [report.failed("Repositorio", "Listar los ficheros del repositorio", [str(error)])]
    results = [_guarded("Repositorio", check) for check in checks]
    results += checks_stack.backend_checks(ROOT, run)
    results.append(checks_purity.check_domain_purity(ROOT))
    results.append(checks_purity.check_layers(ROOT))
    results.append(checks_trace.check_traceability(ROOT, strict_trace))
    results += checks_stack.frontend_checks(ROOT, run, e2e)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Oráculo de SaaS-O-Matic")
    parser.add_argument("--e2e", action="store_true", help="ejecuta también las pruebas de Playwright")
    parser.add_argument(
        "--strict-trace", action="store_true", help="falla si queda algún requisito del backend sin test"
    )
    options = parser.parse_args()
    results = collect(options.e2e, options.strict_trace)
    sys.stdout.buffer.write((report.render(results) + "\n").encode("utf-8"))
    return report.exit_code(results)


if __name__ == "__main__":
    sys.exit(main())
