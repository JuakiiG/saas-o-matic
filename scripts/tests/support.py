"""Shared fixtures: throwaway repositories with fake specs."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SPEC_NAMES = {
    "SPEC-01": "SPEC-01-clientes.md",
    "SPEC-02": "SPEC-02-tarificacion.md",
    "SPEC-03": "SPEC-03-simulaciones.md",
    "SPEC-04": "SPEC-04-frontend.md",
}
SPECS_DIR = Path("ai-workspace") / "01-specs"
ASSUMPTIONS = Path("ai-workspace") / "00-analisis" / "supuestos.md"
BORRADOR = dict.fromkeys(SPEC_NAMES, "borrador")
BACKEND_OK = {**BORRADOR, "SPEC-01": "aprobada", "SPEC-02": "aprobada", "SPEC-03": "aprobada"}
ALL_OK = dict.fromkeys(SPEC_NAMES, "aprobada")


def write(path: Path, text: str) -> Path:
    """Write a UTF-8 file with LF endings, creating its folders."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def spec_text(spec_id: str, state: str, assumptions: str = "A6 (`decidido`)") -> str:
    return (
        f"# {spec_id} · Test\n\n| | |\n|---|---|\n"
        f"| **Estado** | `{state}` (2026-11-12) |\n"
        f"| **Supuestos** | {assumptions} |\n\n"
        "| Id | Requisito | Cubre |\n|---|---|---|\n"
        "| E-01 | El sistema deberá hacer algo. | R-01 |\n"
        "| E-02 | El sistema deberá hacer otra cosa. | R-01 |\n"
    )


def index_text(states: dict[str, str]) -> str:
    rows = "".join(
        f"| [{spec}]({SPEC_NAMES[spec]}) | Test | R-01 | A6 | `{state}` (2026-11-12) |\n"
        for spec, state in states.items()
    )
    return "# Especificaciones\n\n| Spec | Ámbito | Requisitos | Supuestos | Estado |\n|---|---|---|---|---|\n" + rows


def assumptions_text() -> str:
    return (
        "| Id | Ambigüedad | Estado | Afecta a |\n|---|---|---|---|\n"
        "| A2 | Plan | `pendiente de confirmar` | SPEC-01 |\n"
        "| A6 | Dinero | `decidido` (2026-11-12) | SPEC-02 |\n"
    )


def make_repo(case: unittest.TestCase, states: dict[str, str]) -> Path:
    """Create a temporary project root with the four specs in the given states."""
    root = Path(case.enterContext(tempfile.TemporaryDirectory())).resolve()
    for spec, state in states.items():
        write(root / SPECS_DIR / SPEC_NAMES[spec], spec_text(spec, state))
    write(root / SPECS_DIR / "README.md", index_text(states))
    write(root / ASSUMPTIONS, assumptions_text())
    return root


def git(root: Path, *args: str) -> str:
    """Run git in the fixture repository and fail loudly if it does not work."""
    done = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, encoding="utf-8", check=False
    )
    if done.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {done.stderr}")
    return done.stdout


def git_init(root: Path) -> None:
    """Turn the fixture into a git repository isolated from the user's settings."""
    git(root, "init", "-q")
    for key, value in (
        ("user.name", "Test"),
        ("user.email", "test@example.invalid"),
        ("core.autocrlf", "false"),
        ("commit.gpgsign", "false"),
    ):
        git(root, "config", key, value)


def commit_all(root: Path, message: str) -> None:
    git(root, "add", "-A")
    git(root, "commit", "-q", "--no-verify", "-m", message)


class FakeRunner:
    """Stands in for the real process runner and records what it was asked to run.

    When asked for `coverage json -o <file>`, it writes a report with `totals`,
    which is how the oracle reads the branch coverage.
    """

    def __init__(self, failing: str = "", totals: dict[str, object] | None = None) -> None:
        self.failing = failing
        self.totals = {"covered_branches": 9, "num_branches": 10} if totals is None else totals
        self.commands: list[list[str]] = []

    def __call__(self, command: list[str], cwd: Path) -> tuple[int, str]:
        self.commands.append(command)
        if self.failing and self.failing in command:
            return 1, "boom"
        if "json" in command and "-o" in command:
            target = Path(command[command.index("-o") + 1])
            target.write_text(json.dumps({"totals": self.totals}), encoding="utf-8")
        return 0, ""
