"""Tools of each project. Inactive until the project exists; never shown as passed."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from oracle import report
from oracle.repo import OracleError, tail

Runner = Callable[[list[str], Path], tuple[int, str]]

BACKEND = "Backend"
FRONTEND = "Frontend"
BACKEND_MARKER = "pyproject.toml"
FRONTEND_MARKER = "package.json"

# Coverage thresholds decided by the Tech Lead on 2026-11-12.
BACKEND_COMMANDS: tuple[tuple[str, list[str]], ...] = (
    ("ruff check", ["uv", "run", "ruff", "check", "."]),
    ("ruff format --check", ["uv", "run", "ruff", "format", "--check", "."]),
    ("mypy --strict", ["uv", "run", "mypy", "--strict", "."]),
    (
        "pytest con el 90 % de ramas en todo el backend",
        ["uv", "run", "pytest", "--cov=app", "--cov-branch", "--cov-fail-under=90"],
    ),
    (
        "100 % de ramas en domain/",
        ["uv", "run", "coverage", "report", "--include=app/domain/*", "--fail-under=100"],
    ),
)
# The frontend project must define these npm scripts; `test:ci` enforces 80 % of lines.
FRONTEND_COMMANDS: tuple[tuple[str, list[str]], ...] = (
    ("ESLint, con los límites de tamaño", ["npm", "run", "lint"]),
    ("Compilación en modo estricto", ["npm", "run", "build"]),
    ("Tests con el 80 % de líneas", ["npm", "run", "test:ci"]),
)
E2E_COMMAND = ("Playwright: principio a fin y 375 px", ["npm", "run", "e2e"])


def _run_one(block: str, name: str, command: list[str], cwd: Path, runner: Runner) -> report.Result:
    try:
        code, output = runner(command, cwd)
    except OracleError as error:
        return report.failed(block, name, [str(error)])
    if code != 0:
        return report.failed(block, name, [f"`{' '.join(command)}` terminó con código {code}", tail(output)])
    return report.passed(block, name)


def backend_checks(root: Path, runner: Runner) -> list[report.Result]:
    folder = root / "backend"
    if not (folder / BACKEND_MARKER).is_file():
        reason = f"no existe backend/{BACKEND_MARKER}"
        return [report.inactive(BACKEND, name, reason) for name, _ in BACKEND_COMMANDS]
    return [_run_one(BACKEND, name, command, folder, runner) for name, command in BACKEND_COMMANDS]


def frontend_checks(root: Path, runner: Runner, e2e: bool) -> list[report.Result]:
    folder = root / "frontend"
    e2e_name, e2e_command = E2E_COMMAND
    if not (folder / FRONTEND_MARKER).is_file():
        reason = f"no existe frontend/{FRONTEND_MARKER}"
        names = [name for name, _ in FRONTEND_COMMANDS] + [e2e_name]
        return [report.inactive(FRONTEND, name, reason) for name in names]
    results = [_run_one(FRONTEND, name, command, folder, runner) for name, command in FRONTEND_COMMANDS]
    if e2e:
        results.append(_run_one(FRONTEND, e2e_name, e2e_command, folder, runner))
    else:
        results.append(report.inactive(FRONTEND, e2e_name, "solo se ejecuta con --e2e (fase de QA)"))
    return results
