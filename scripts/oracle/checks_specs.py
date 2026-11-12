"""Checks about specs: no code without an approved spec, index and assumptions."""

from __future__ import annotations

import re
from pathlib import Path

from oracle import report, specgate
from oracle.repo import read_text

BLOCK = "Specs"
SPEC_IDS = tuple(spec for specs in specgate.BLOCKS.values() for spec in specs)

_INDEX_ROW = re.compile(r"^\|\s*\[(SPEC-\d+)\]\([^)]*\)\s*\|.*`(aprobada|borrador)`[^|]*\|\s*$", re.MULTILINE)
_ASSUMPTIONS_ROW = re.compile(r"^\|\s*\*\*Supuestos\*\*\s*\|(.*)\|\s*$", re.MULTILINE)
_ASSUMPTION_ID = re.compile(r"\bA\d{1,2}\b")
_ASSUMPTION_STATE = re.compile(r"^\|\s*(A\d{1,2})\s*\|[^|]*\|\s*`([^`]+)`", re.MULTILINE)


def check_gate(root: Path, files: list[str]) -> report.Result:
    """Second lock of the hook: code written by any other means is found on disk."""
    name = "Ningún fichero de código sin su bloque de specs aprobado"
    directory = specgate.specs_dir(root)
    pending = {block: specgate.pending_specs(directory, block) for block in specgate.BLOCKS}
    problems = []
    for file in files:
        parts = specgate.relative_parts(root, file)
        block = specgate.block_for(parts) if parts else None
        if block and pending[block]:
            problems.append(f"{file}: falta aprobar {', '.join(pending[block])}")
    return report.from_problems(BLOCK, name, problems)


def check_index(directory: Path) -> report.Result:
    """The state in each spec header must be the one shown in the index."""
    name = "El estado de cada spec coincide con el índice"
    index = read_text(directory / "README.md")
    if index is None:
        return report.failed(BLOCK, name, [f"no se puede leer {directory / 'README.md'}"])
    listed = dict(_INDEX_ROW.findall(index))
    problems = []
    for spec in SPEC_IDS:
        header = specgate.spec_state(directory, spec)
        if header == specgate.UNKNOWN:
            problems.append(f"{spec}: no se puede leer su estado en la cabecera")
        elif spec not in listed:
            problems.append(f"{spec}: no figura en el índice")
        elif listed[spec] != header:
            problems.append(f"{spec}: la cabecera dice `{header}` y el índice `{listed[spec]}`")
    return report.from_problems(BLOCK, name, problems)


def _cited_assumptions(directory: Path, spec: str) -> list[str]:
    matches = sorted(directory.glob(f"{spec}-*.md"))
    text = read_text(matches[0]) if matches else None
    row = _ASSUMPTIONS_ROW.search(text or "")
    return _ASSUMPTION_ID.findall(row.group(1)) if row else []


def check_assumptions(directory: Path, assumptions_file: Path) -> report.Result:
    """An approved spec cannot depend on an assumption that is not decided."""
    name = "Ninguna spec aprobada depende de un supuesto sin decidir"
    text = read_text(assumptions_file)
    if text is None:
        return report.failed(BLOCK, name, [f"no se puede leer {assumptions_file}"])
    states = dict(_ASSUMPTION_STATE.findall(text))
    problems = []
    for spec in SPEC_IDS:
        if specgate.spec_state(directory, spec) != specgate.APPROVED:
            continue
        for assumption in _cited_assumptions(directory, spec):
            state = states.get(assumption, "no figura en supuestos.md")
            if not state.startswith("decidido"):
                problems.append(f"{spec} depende de {assumption}: {state}")
    return report.from_problems(BLOCK, name, problems)
