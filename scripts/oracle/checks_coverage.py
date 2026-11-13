"""Branch coverage of the backend, judged on branches alone.

`pytest --cov-branch --cov-fail-under=N` compares the combined total of
statements and branches, so well covered statements can hide untested branches:
96 of 96 statements and 2 of 4 branches is 98 % combined and 50 % of branches.
This check reads `coverage json` and compares covered branches with existing
branches. It is added to the combined threshold; it does not replace it.
"""

from __future__ import annotations

import json
import tempfile
from collections.abc import Callable
from pathlib import Path

from oracle import report
from oracle.repo import OracleError, read_text, tail

Runner = Callable[[list[str], Path], tuple[int, str]]

BLOCK = "Backend"
MIN_BRANCH_PERCENT = 90
NAME = f"{MIN_BRANCH_PERCENT} % de ramas en todo el backend (ramas cubiertas / ramas existentes)"
# `--fail-under=0`: the combined threshold of the configuration is judged by pytest, not here.
REPORT_COMMAND = ["uv", "run", "--locked", "coverage", "json", "--quiet", "--fail-under=0", "-o"]


def judge(totals: object) -> report.Result:
    """Compare covered and existing branches with integers; no rounding can help."""
    values = totals if isinstance(totals, dict) else {}
    covered, existing = values.get("covered_branches"), values.get("num_branches")
    if not isinstance(covered, int) or not isinstance(existing, int):
        return report.failed(BLOCK, NAME, ["el informe de cobertura no trae el recuento de ramas"])
    if existing == 0:
        # Nothing to measure is not a pass (CLAUDE.md, "Oráculo único").
        return report.inactive(BLOCK, NAME, "el código medido no tiene ninguna rama")
    count = f"{covered} de {existing} ramas cubiertas"
    if covered * 100 < MIN_BRANCH_PERCENT * existing:
        return report.failed(BLOCK, NAME, [f"{count}: menos del {MIN_BRANCH_PERCENT} %"])
    return report.passed(BLOCK, NAME, [count])


def _read_totals(target: Path) -> object:
    text = read_text(target)
    if text is None:
        raise OracleError("`coverage json` no ha escrito su informe")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise OracleError(f"el informe de `coverage json` no es JSON válido ({error.msg})") from error
    return data.get("totals") if isinstance(data, dict) else None


def check_branches(folder: Path, runner: Runner) -> report.Result:
    """Run `coverage json` on the data left by pytest and judge its branch totals."""
    with tempfile.TemporaryDirectory() as temporary:
        target = Path(temporary) / "coverage.json"
        command = [*REPORT_COMMAND, str(target)]
        try:
            code, output = runner(command, folder)
            if code != 0:
                return report.failed(BLOCK, NAME, [f"`{' '.join(command)}` terminó con código {code}", tail(output)])
            return judge(_read_totals(target))
        except OracleError as error:
            return report.failed(BLOCK, NAME, [str(error)])
