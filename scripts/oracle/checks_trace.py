"""Traceability: every backend test cites an EARS requirement that exists.

Inactive until there are backend tests (`.claude/rules/backend.md`, "Tests").
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

from oracle import report, specgate
from oracle.repo import read_text

BLOCK = "Backend"
NAME = "Cada test del backend cita un requisito EARS que existe"
TESTS = ("backend", "tests")
_REQUIREMENT_ROW = re.compile(r"^\|\s*(E-\d+)\s*\|", re.MULTILINE)
_CITATION = re.compile(r"SPEC-\d+/E-\d+")


def _requirements(root: Path) -> set[str]:
    """Requirement ids of the backend specs, as `SPEC-02/E-03`."""
    found: set[str] = set()
    directory = specgate.specs_dir(root)
    for spec in specgate.BLOCKS["backend"]:
        for path in sorted(directory.glob(f"{spec}-*.md")):
            text = read_text(path) or ""
            found.update(f"{spec}/{row}" for row in _REQUIREMENT_ROW.findall(text))
    return found


def _test_functions(tree: ast.AST) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    functions = (node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))
    return [node for node in functions if node.name.startswith("test_")]


def _file_citations(label: str, text: str, known: set[str], problems: list[str]) -> set[str]:
    """Citations of one test file; what is wrong with it goes to `problems`."""
    try:
        tree = ast.parse(text)
    except SyntaxError as error:
        problems.append(f"{label}: no se puede analizar ({error.msg})")
        return set()
    cited: set[str] = set()
    for node in _test_functions(tree):
        citations = set(_CITATION.findall(ast.get_docstring(node) or ""))
        if not citations:
            problems.append(f"{label}:{node.lineno} {node.name}: no cita ningún requisito")
        for unknown in sorted(citations - known):
            problems.append(f"{label}:{node.lineno} {node.name}: cita {unknown}, que no existe")
        cited |= citations
    return cited


def check_traceability(root: Path, strict: bool) -> report.Result:
    """Fail on tests without a valid citation; uncovered requirements only fail when strict."""
    folder = root.joinpath(*TESTS)
    files = sorted(folder.rglob("test_*.py")) if folder.is_dir() else []
    if not files:
        return report.inactive(BLOCK, NAME, "no hay tests en backend/tests/")
    known = _requirements(root)
    problems: list[str] = []
    cited: set[str] = set()
    for path in files:
        label = path.relative_to(root).as_posix()
        cited |= _file_citations(label, read_text(path) or "", known, problems)
    uncovered = sorted(known - cited)
    notes = [f"{len(uncovered)} requisitos sin test: {', '.join(uncovered)}"] if uncovered else []
    if problems or (strict and uncovered):
        return report.failed(BLOCK, NAME, problems + notes)
    return report.passed(BLOCK, NAME, notes)
