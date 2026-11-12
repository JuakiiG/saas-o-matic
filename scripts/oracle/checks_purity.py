"""Domain purity and layer direction of the backend (SPEC-02/CA-09, SPEC-01/CA-17).

Inactive until `backend/app/` exists. Standard library `ast` only.
"""

from __future__ import annotations

import ast
import sys
from collections.abc import Iterator
from pathlib import Path

from oracle import report

BLOCK = "Backend"
APP = ("backend", "app")
DOMAIN_PACKAGE = "app.domain"
# `.claude/rules/backend.md`: api -> services -> domain, and services -> repositories.
ALLOWED_LAYERS: dict[str, tuple[str, ...]] = {
    "api": ("api", "services", "domain"),
    "services": ("services", "domain", "repositories"),
    "domain": ("domain",),
    "repositories": ("repositories",),
}
SQL_MODULE = "sqlite3"
SQL_LAYER = "repositories"
PURITY_NAME = "domain/ solo importa la biblioteca estándar y no usa float ni la división `/`"
LAYERS_NAME = "Dirección de las capas y `sqlite3` solo en repositories/"


def _python_files(folder: Path) -> list[Path]:
    return sorted(folder.rglob("*.py")) if folder.is_dir() else []


def _parse(path: Path) -> ast.AST | str:
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, SyntaxError) as error:
        return f"no se puede analizar ({error})"


def _imports(tree: ast.AST) -> Iterator[tuple[int, str]]:
    """Absolute modules imported by a file; relative imports stay inside the package."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield node.lineno, alias.name
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            yield node.lineno, node.module


def _is_pure_import(module: str) -> bool:
    if module == DOMAIN_PACKAGE or module.startswith(DOMAIN_PACKAGE + "."):
        return True
    return module.split(".")[0] in sys.stdlib_module_names


def _float_uses(tree: ast.AST) -> Iterator[tuple[int, str]]:
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == "float":
            yield node.lineno, "usa el tipo float"
        elif isinstance(node, ast.Constant) and isinstance(node.value, (float, complex)):
            yield node.lineno, f"literal con decimales ({node.value!r})"
        elif isinstance(node, (ast.BinOp, ast.AugAssign)) and isinstance(node.op, ast.Div):
            yield node.lineno, "división `/` (usa `//`)"


def _purity_problems(label: str, tree: ast.AST) -> Iterator[str]:
    for line, module in _imports(tree):
        if not _is_pure_import(module):
            yield f"{label}:{line}: importa `{module}`"
    for line, what in _float_uses(tree):
        yield f"{label}:{line}: {what}"


def check_domain_purity(root: Path) -> report.Result:
    domain = root.joinpath(*APP, "domain")
    files = _python_files(domain)
    if not files:
        return report.inactive(BLOCK, PURITY_NAME, "no existe backend/app/domain/")
    problems: list[str] = []
    for path in files:
        label = path.relative_to(root).as_posix()
        tree = _parse(path)
        if isinstance(tree, str):
            problems.append(f"{label}: {tree}")
        else:
            problems.extend(_purity_problems(label, tree))
    return report.from_problems(BLOCK, PURITY_NAME, problems)


def _layer_problems(label: str, layer: str, tree: ast.AST) -> Iterator[str]:
    for line, module in _imports(tree):
        parts = module.split(".")
        if parts[0] == SQL_MODULE and layer != SQL_LAYER:
            yield f"{label}:{line}: `{SQL_MODULE}` fuera de {SQL_LAYER}/"
        target = parts[1] if parts[0] == "app" and len(parts) > 1 else None
        if target in ALLOWED_LAYERS and target not in ALLOWED_LAYERS[layer]:
            yield f"{label}:{line}: {layer}/ importa de {target}/"


def check_layers(root: Path) -> report.Result:
    app = root.joinpath(*APP)
    files = _python_files(app)
    if not files:
        return report.inactive(BLOCK, LAYERS_NAME, "no existe backend/app/")
    problems: list[str] = []
    for path in files:
        layer = path.relative_to(app).parts[0]
        if layer not in ALLOWED_LAYERS:
            continue
        label = path.relative_to(root).as_posix()
        tree = _parse(path)
        if isinstance(tree, str):
            problems.append(f"{label}: {tree}")
        else:
            problems.extend(_layer_problems(label, layer, tree))
    return report.from_problems(BLOCK, LAYERS_NAME, problems)
