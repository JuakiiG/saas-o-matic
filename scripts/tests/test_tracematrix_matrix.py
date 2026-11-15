"""Tests of the matrix: what is read from a spec, which tests are collected and what is written."""

from __future__ import annotations

import unittest

from tests import support
from tracematrix import matrix
from tracematrix.citations import FoundTest

SPEC = """
## 3. Requisitos (EARS)

| Id | Requisito | Cubre |
|---|---|---|
| E-01 | Cuando se abre el panel, el sistema deberá mostrar el listado. | R-10 |
| E-12 | El sistema deberá mostrar el detalle. | R-11 |
| E-02 | El sistema deberá buscar. | R-10 |

## 6. Criterios de aceptación

| Id | Criterio | Requisitos |
|---|---|---|
| CA-01 | Un test reproduce cada fila de 5.1 (E-99 no es de esta columna). | E-01 a E-02, E-12 |
| CA-02 | Una prueba lee los colores. | — (2.8) |
| CA-03 | Otra, con `a | b` en el texto. | E-12 |
"""


def found(file: str, own: set[tuple[str, str]], inherited: set[tuple[str, str]] | None = None) -> FoundTest:
    return FoundTest(file, 1, frozenset(own), frozenset(inherited or set()))


class ReadSpecTest(unittest.TestCase):
    def test_requirements_in_numeric_order(self) -> None:
        self.assertEqual(matrix.read_spec("SPEC-04", SPEC).requirements, ["E-01", "E-02", "E-12"])

    def test_criteria_with_the_requirements_of_their_last_column(self) -> None:
        criteria = matrix.read_spec("SPEC-04", SPEC).criteria
        self.assertEqual(criteria, {"CA-01": ["E-01", "E-02", "E-12"], "CA-02": [], "CA-03": ["E-12"]})


class CollectTestsTest(unittest.TestCase):
    def test_each_group_takes_its_own_files(self) -> None:
        root = support.make_repo(self, support.ALL_OK)
        python = 'def test_a():\n    """SPEC-01/E-01: a."""\n'
        typescript = "it('should work (SPEC-04/E-01)', () => {});\n"
        support.write(root / "backend/tests/unit/test_a.py", python)
        support.write(root / "backend/tests/cases.py", python)
        support.write(root / "frontend/src/app/a.spec.ts", typescript)
        support.write(root / "frontend/src/app/a.ts", typescript)
        support.write(root / "frontend/e2e/sub/b.spec.ts", typescript)
        support.write(root / "frontend/e2e/support/c.ts", typescript)
        support.write(root / "frontend/node_modules/x/d.spec.ts", typescript)
        files = {group: [test.file for test in tests] for group, tests in matrix.collect_tests(root).items()}
        expected = {
            "Backend": ["backend/tests/unit/test_a.py"],
            "Frontend": ["frontend/src/app/a.spec.ts"],
            "Playwright": ["frontend/e2e/sub/b.spec.ts"],
        }
        self.assertEqual(files, expected)


class RenderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.specs = [matrix.read_spec("SPEC-04", SPEC)]
        self.tests = {
            "Backend": [found("backend/tests/test_a.py", {("SPEC-04", "E-01")})],
            "Frontend": [
                found("frontend/src/a.spec.ts", set(), {("SPEC-04", "E-01")}),
                found("frontend/src/a.spec.ts", {("SPEC-04", "E-01")}, {("SPEC-04", "E-02")}),
                found("frontend/src/b.spec.ts", {("SPEC-01", "E-01")}),
            ],
            "Playwright": [found("frontend/e2e/c.spec.ts", {("SPEC-04", "CA-01"), ("SPEC-04", "CA-03")})],
        }

    def test_one_row_per_requirement_with_counts_and_files(self) -> None:
        text = matrix.render(self.specs, self.tests)
        self.assertIn("### SPEC-04\n", text)
        self.assertIn("| E-01 | 1 | 2 | 0 | 3 | 2 | `backend/tests/test_a.py` (1), `frontend/src/a.spec.ts` (2) |", text)
        self.assertIn("| E-02 | 0 | 1 | 0 | 1 | 0 | `frontend/src/a.spec.ts` (1) |", text)
        self.assertIn("| E-12 | 0 | 0 | 0 | 0 | 0 | — |", text)

    def test_uncited_requirements_with_the_criteria_that_name_them(self) -> None:
        text = matrix.render(self.specs, self.tests)
        row = "| SPEC-04/E-12 | CA-01: 1 (`frontend/e2e/c.spec.ts`); CA-03: 1 (`frontend/e2e/c.spec.ts`) |"
        self.assertIn(row, text)
        self.assertNotIn("| SPEC-04/E-01 |", text)

    def test_a_criterion_that_no_test_cites_is_said(self) -> None:
        self.tests["Playwright"] = []
        text = matrix.render(self.specs, self.tests)
        self.assertIn("| SPEC-04/E-12 | CA-01: 0; CA-03: 0 |", text)

    def test_an_uncited_requirement_without_criterion_is_uncovered(self) -> None:
        self.specs[0].criteria = {}
        text = matrix.render(self.specs, self.tests)
        self.assertIn("| SPEC-04/E-12 | sin cubrir |", text)

    def test_citations_of_what_does_not_exist_are_listed(self) -> None:
        self.tests["Frontend"].append(found("frontend/src/b.spec.ts", {("SPEC-04", "E-77")}))
        text = matrix.render(self.specs, self.tests)
        self.assertIn("- `SPEC-01/E-01`: `frontend/src/b.spec.ts`", text)
        self.assertIn("- `SPEC-04/E-77`: `frontend/src/b.spec.ts`", text)

    def test_tests_that_cite_nothing_are_listed_by_file(self) -> None:
        heading = "### Tests sin ninguna cita\n\n"
        self.assertIn(heading + "Ninguno.", matrix.render(self.specs, self.tests))
        self.tests["Frontend"] += [found("frontend/src/b.spec.ts", set()), found("frontend/src/b.spec.ts", set())]
        self.tests["Playwright"].append(found("frontend/e2e/c.spec.ts", set()))
        text = matrix.render(self.specs, self.tests)
        self.assertIn(heading + "- `frontend/e2e/c.spec.ts` (1)\n- `frontend/src/b.spec.ts` (2)\n", text)

    def test_totals_of_each_group(self) -> None:
        text = matrix.render(self.specs, self.tests)
        self.assertIn("| Backend | 1 | 1 | 1 | 0 |", text)
        self.assertIn("| Frontend | 3 | 2 | 3 | 0 |", text)
        self.tests["Frontend"].append(found("frontend/src/b.spec.ts", set()))
        self.assertIn("| Frontend | 4 | 2 | 3 | 1 |", matrix.render(self.specs, self.tests))
        self.assertIn("| Playwright | 1 | 1 | 1 | 0 |", text)


if __name__ == "__main__":
    unittest.main()
