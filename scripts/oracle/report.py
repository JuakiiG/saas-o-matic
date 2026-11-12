"""Result of each oracle check and the final report."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

OK = "OK"
FAIL = "FALLO"
INACTIVE = "INACTIVO"


@dataclass(frozen=True)
class Result:
    """Outcome of one check. `details` are failures, notes or the reason for being inactive."""

    block: str
    name: str
    status: str
    details: tuple[str, ...] = ()


def passed(block: str, name: str, notes: Iterable[str] = ()) -> Result:
    return Result(block, name, OK, tuple(notes))


def failed(block: str, name: str, details: Iterable[str]) -> Result:
    return Result(block, name, FAIL, tuple(details))


def inactive(block: str, name: str, reason: str) -> Result:
    return Result(block, name, INACTIVE, (reason,))


def from_problems(block: str, name: str, problems: Sequence[str]) -> Result:
    """Pass when there are no problems; otherwise fail listing them."""
    return failed(block, name, problems) if problems else passed(block, name)


def exit_code(results: Sequence[Result]) -> int:
    return 1 if any(result.status == FAIL for result in results) else 0


def _count(results: Sequence[Result], status: str) -> int:
    return sum(1 for result in results if result.status == status)


def _summary(results: Sequence[Result]) -> str:
    idle = _count(results, INACTIVE)
    failures = _count(results, FAIL)
    counts = (
        f"{_count(results, OK)} correctas, {failures} con fallo, "
        f"{idle} inactiva{'' if idle == 1 else 's'}"
    )
    if failures:
        return f"ORÁCULO EN ROJO · {counts}"
    # An inactive check proves nothing: say so next to the green verdict.
    scope = " (solo lo activo: lo inactivo no está comprobado)" if idle else ""
    return f"ORÁCULO EN VERDE{scope} · {counts}"


def render(results: Sequence[Result]) -> str:
    """Plain-text report, grouped by block in the order the checks ran."""
    lines: list[str] = []
    block = ""
    for result in results:
        if result.block != block:
            block = result.block
            lines.append(f"\n== {block} ==")
        lines.append(f"[{result.status:<8}] {result.name}")
        lines.extend(f"             - {detail}" for detail in result.details)
    lines.append("")
    lines.append(_summary(results))
    return "\n".join(lines).lstrip("\n")
