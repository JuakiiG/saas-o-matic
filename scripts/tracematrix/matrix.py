"""The matrix: requirements and criteria of each spec against the tests that cite them."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path

from oracle import specgate
from tracematrix.citations import ID_LIST, Citation, FoundTest, expand_ids, python_tests, typescript_tests

_REQUIREMENT_ROW = re.compile(r"^\|\s*(E-\d+)\s*\|", re.MULTILINE)
# The last cell of a criterion row names its requirements; the text before may hold a `|`.
_CRITERION_ROW = re.compile(r"^\|\s*(CA-\d+)\s*\|.*\|([^|]*)\|\s*$", re.MULTILINE)
_SPEC_FILE = re.compile(r"^(SPEC-\d+)-.*\.md$")
# Group, folder, file pattern and reader, in the order of the columns of the matrix.
GROUPS: tuple[tuple[str, str, str, Callable[[str, str], list[FoundTest]]], ...] = (
    ("Backend", "backend/tests", "test_*.py", python_tests),
    ("Frontend", "frontend/src", "*.spec.ts", typescript_tests),
    ("Playwright", "frontend/e2e", "*.spec.ts", typescript_tests),
)
NONE = "—"


@dataclass
class Spec:
    """Requirements of a spec, and which of them each acceptance criterion names."""

    spec_id: str
    requirements: list[str] = field(default_factory=list)
    criteria: dict[str, list[str]] = field(default_factory=dict)


def _number(item: str) -> int:
    return int(item.split("-")[1])


def read_spec(spec_id: str, text: str) -> Spec:
    """Requirement rows and criterion rows of the text of a spec."""
    requirements = sorted(set(_REQUIREMENT_ROW.findall(text)), key=_number)
    criteria = {
        criterion: [item for listing in ID_LIST.findall(cell) for item in expand_ids(listing)]
        for criterion, cell in _CRITERION_ROW.findall(text)
    }
    return Spec(spec_id, requirements, criteria)


def read_specs(root: Path) -> list[Spec]:
    """Every spec of the repository, in the order of their ids."""
    specs = []
    for path in sorted(specgate.specs_dir(root).glob("SPEC-*.md"), key=lambda path: path.name):
        match = _SPEC_FILE.match(path.name)
        if match:
            specs.append(read_spec(match.group(1), path.read_text(encoding="utf-8")))
    return specs


def collect_tests(root: Path) -> dict[str, list[FoundTest]]:
    """Tests of the repository, by group, in the order of the columns."""
    found: dict[str, list[FoundTest]] = {}
    for group, folder, pattern, reader in GROUPS:
        labels = sorted(path.relative_to(root).as_posix() for path in (root / folder).rglob(pattern))
        found[group] = [test for label in labels for test in reader(label, (root / label).read_text("utf-8"))]
    return found


def _citing(tests: Iterable[FoundTest], citation: Citation) -> list[FoundTest]:
    return [test for test in tests if citation in test.cited]


def _files(tests: Iterable[FoundTest], counted: bool) -> str:
    """Files of some tests, in order; with how many of the tests are in each, if asked."""
    counts = Counter(test.file for test in tests)
    names = [f"`{file}` ({counts[file]})" if counted else f"`{file}`" for file in sorted(counts)]
    return ", ".join(names) or NONE


def _totals(tests: dict[str, list[FoundTest]]) -> str:
    rows = ["### Tests contados", "", "| Grupo | Tests declarados | Ficheros | Con alguna cita | Sin ninguna cita |"]
    rows.append("|---|---|---|---|---|")
    for group, found in tests.items():
        citing = sum(1 for test in found if test.cited)
        files = len({test.file for test in found})
        rows.append(f"| {group} | {len(found)} | {files} | {citing} | {len(found) - citing} |")
    return "\n".join(rows)


def _spec_table(spec: Spec, tests: dict[str, list[FoundTest]]) -> str:
    groups = " | ".join(tests)
    rows = [f"### {spec.spec_id}", "", f"| Requisito | {groups} | Total | En su título | Ficheros |"]
    rows.append("|---|" + "---|" * (len(tests) + 3))
    for item in spec.requirements:
        citing = [_citing(found, (spec.spec_id, item)) for found in tests.values()]
        every = [test for found in citing for test in found]
        direct = sum(1 for test in every if (spec.spec_id, item) in test.own)
        counts = " | ".join(str(len(found)) for found in citing)
        rows.append(f"| {item} | {counts} | {len(every)} | {direct} | {_files(every, counted=True)} |")
    return "\n".join(rows)


def _criteria_of(spec: Spec, item: str, every: list[FoundTest]) -> str:
    """Criteria that name a requirement, each with how many tests cite it and where."""
    parts = []
    for criterion, named in spec.criteria.items():
        if item in named:
            citing = _citing(every, (spec.spec_id, criterion))
            where = f" ({_files(citing, counted=False)})" if citing else ""
            parts.append(f"{criterion}: {len(citing)}{where}")
    return "; ".join(parts) or "sin cubrir"


def _uncited(specs: list[Spec], every: list[FoundTest]) -> str:
    rows = ["### Requisitos sin ningún test que los cite", ""]
    missing = [(spec, item) for spec in specs for item in spec.requirements if not _citing(every, (spec.spec_id, item))]
    if not missing:
        return "\n".join([*rows, "Ninguno."])
    rows += ["| Requisito | Criterios que lo nombran: tests que citan cada criterio |", "|---|---|"]
    rows += [f"| {spec.spec_id}/{item} | {_criteria_of(spec, item, every)} |" for spec, item in missing]
    return "\n".join(rows)


def _unknown(specs: list[Spec], every: list[FoundTest]) -> str:
    """Citations of a requirement or of a criterion that no spec has."""
    known = {(spec.spec_id, item) for spec in specs for item in [*spec.requirements, *spec.criteria]}
    strangers = sorted({citation for test in every for citation in test.cited} - known)
    rows = ["### Citas de algo que no está en las specs", ""]
    for citation in strangers:
        rows.append(f"- `{citation[0]}/{citation[1]}`: {_files(_citing(every, citation), counted=False)}")
    return "\n".join(rows if strangers else [*rows, "Ninguna."])


def _silent(every: list[FoundTest]) -> str:
    """Tests that cite nothing, neither in their title nor through a block, by file."""
    counts = Counter(test.file for test in every if not test.cited)
    rows = ["### Tests sin ninguna cita", ""]
    rows += [f"- `{file}` ({counts[file]})" for file in sorted(counts)]
    return "\n".join(rows if counts else [*rows, "Ninguno."])


def render(specs: list[Spec], tests: dict[str, list[FoundTest]]) -> str:
    """The tables of the document, as Markdown."""
    every = [test for found in tests.values() for test in found]
    sections = [_totals(tests), *(_spec_table(spec, tests) for spec in specs)]
    sections += [_uncited(specs, every), _unknown(specs, every), _silent(every)]
    return "\n\n".join(sections) + "\n"
