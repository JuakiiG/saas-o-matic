"""Size limits, silenced rules and skipped tests (CLAUDE.md, "Límites de tamaño")."""

from __future__ import annotations

import ast
import re
from collections.abc import Iterator
from pathlib import Path

from oracle import report
from oracle.repo import read_text

BLOCK = "Código"
CODE_ROOTS = ("backend", "frontend", "scripts")
CODE_SUFFIXES = (".py", ".ts", ".js", ".mjs", ".cjs")
TEST_FOLDERS = ("tests", "e2e")
TEST_SUFFIXES = (".spec.ts", ".test.ts")
MAX_FILE_LINES = 250
MAX_TEMPLATE_LINES = 120
MAX_FUNCTION_LINES = 40
MAX_PARAMETERS = 5

# Assembled from pieces so that this file does not contain the markers it looks for.
_MARKERS = ("# no" + "qa", "# type: " + "ignore", "eslint-" + "disable")
_JUSTIFICATION = re.compile(r"(--|#|//)\s*\w[\w ,.'-]{2,}")
_SKIPS_PY = re.compile(r"pytest\.mark\.(skip|xfail)|pytest\.skip\(|unittest\.skip")
_SKIPS_TS = re.compile(r"\b(xit|xdescribe|fit|fdescribe)\s*\(|\b(it|describe|test)\.(skip|only)\s*\(")


def _in_scope(file: str, suffixes: tuple[str, ...]) -> bool:
    return file.split("/")[0] in CODE_ROOTS and file.endswith(suffixes)


def _is_test(file: str) -> bool:
    parts = file.split("/")
    in_folder = any(folder in parts[:-1] for folder in TEST_FOLDERS)
    return in_folder or parts[-1].startswith("test_") or file.endswith(TEST_SUFFIXES)


def _sources(root: Path, files: list[str], suffixes: tuple[str, ...]) -> Iterator[tuple[str, str]]:
    for file in files:
        text = read_text(root / file) if _in_scope(file, suffixes) else None
        if text is not None:
            yield file, text


def check_file_sizes(root: Path, files: list[str]) -> report.Result:
    name = f"Ficheros de código de {MAX_FILE_LINES} líneas como máximo y plantillas de {MAX_TEMPLATE_LINES}"
    problems = []
    for file, text in _sources(root, files, (*CODE_SUFFIXES, ".html")):
        is_template = file.endswith(".html")
        if _is_test(file) or (is_template and not file.startswith("frontend/")):
            continue
        limit = MAX_TEMPLATE_LINES if is_template else MAX_FILE_LINES
        count = len(text.splitlines())
        if count > limit:
            problems.append(f"{file}: {count} líneas (máximo {limit})")
    return report.from_problems(BLOCK, name, problems)


def _parameter_count(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    args = node.args
    names = [arg.arg for arg in (*args.posonlyargs, *args.args, *args.kwonlyargs)]
    extras = sum(1 for extra in (args.vararg, args.kwarg) if extra is not None)
    # `self` and `cls` are not parameters the caller chooses.
    own = 1 if names[:1] in (["self"], ["cls"]) else 0
    return len(names) + extras - own


def _function_problems(file: str, tree: ast.AST) -> Iterator[str]:
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        length = (node.end_lineno or node.lineno) - node.lineno + 1
        if length > MAX_FUNCTION_LINES:
            yield f"{file}:{node.lineno} {node.name}: {length} líneas (máximo {MAX_FUNCTION_LINES})"
        count = _parameter_count(node)
        if count > MAX_PARAMETERS:
            yield f"{file}:{node.lineno} {node.name}: {count} parámetros (máximo {MAX_PARAMETERS})"


def check_functions(root: Path, files: list[str]) -> report.Result:
    name = f"Funciones de Python de {MAX_FUNCTION_LINES} líneas y {MAX_PARAMETERS} parámetros como máximo"
    problems: list[str] = []
    for file, text in _sources(root, files, (".py",)):
        try:
            tree = ast.parse(text)
        except SyntaxError as error:
            problems.append(f"{file}: no se puede analizar ({error.msg}, línea {error.lineno})")
            continue
        problems.extend(_function_problems(file, tree))
    return report.from_problems(BLOCK, name, problems)


def _unjustified(line: str) -> bool:
    for marker in _MARKERS:
        position = line.find(marker)
        if position >= 0 and not _JUSTIFICATION.search(line[position + len(marker) :]):
            return True
    return False


def check_suppressions(root: Path, files: list[str]) -> report.Result:
    name = "Ninguna regla silenciada sin un motivo en la misma línea"
    problems = []
    for file, text in _sources(root, files, (*CODE_SUFFIXES, ".html")):
        for number, line in enumerate(text.splitlines(), start=1):
            if _unjustified(line):
                problems.append(f"{file}:{number}: {line.strip()}")
    return report.from_problems(BLOCK, name, problems)


def check_skipped_tests(root: Path, files: list[str]) -> report.Result:
    name = "Ningún test saltado, marcado como fallo esperado o ejecutado en solitario"
    problems = []
    for file, text in _sources(root, files, CODE_SUFFIXES):
        pattern = _SKIPS_PY if file.endswith(".py") else _SKIPS_TS
        for number, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line):
                problems.append(f"{file}:{number}: {line.strip()}")
    return report.from_problems(BLOCK, name, problems)
