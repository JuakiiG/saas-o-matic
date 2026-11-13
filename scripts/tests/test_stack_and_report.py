"""Tests of the tool runners (inactive without code) and of the final report."""

from __future__ import annotations

import unittest
from pathlib import Path

from oracle import checks_stack, report
from tests import support


class StackTest(unittest.TestCase):
    def test_everything_is_inactive_without_projects(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        runner = support.FakeRunner()
        results = checks_stack.backend_checks(root, runner) + checks_stack.frontend_checks(root, runner, False)
        self.assertTrue(results)
        self.assertEqual({r.status for r in results}, {report.INACTIVE})
        self.assertEqual(runner.commands, [])

    def test_backend_runs_its_tools_once_the_project_exists(self) -> None:
        root = support.make_repo(self, support.BACKEND_OK)
        support.write(root / "backend" / "pyproject.toml", "[project]\n")
        runner = support.FakeRunner()
        results = checks_stack.backend_checks(root, runner)
        self.assertEqual({r.status for r in results}, {report.OK})
        flat = [" ".join(command) for command in runner.commands]
        for expected in ("ruff check", "ruff format --check", "mypy --strict", "--cov-fail-under=90", "--fail-under=100"):
            self.assertTrue(any(expected in line for line in flat), expected)

    def test_a_failing_tool_fails_its_check_with_its_output(self) -> None:
        root = support.make_repo(self, support.BACKEND_OK)
        support.write(root / "backend" / "pyproject.toml", "[project]\n")
        results = checks_stack.backend_checks(root, support.FakeRunner(failing="mypy"))
        failed = [r for r in results if r.status == report.FAIL]
        self.assertEqual(len(failed), 1)
        self.assertIn("boom", failed[0].details[-1])

    def test_frontend_runs_its_scripts_and_e2e_only_on_request(self) -> None:
        root = support.make_repo(self, support.ALL_OK)
        support.write(root / "frontend" / "package.json", "{}\n")
        results = checks_stack.frontend_checks(root, support.FakeRunner(), False)
        by_name = {r.name: r.status for r in results}
        self.assertEqual(sorted(by_name.values()), [report.INACTIVE, report.OK, report.OK, report.OK])
        results = checks_stack.frontend_checks(root, support.FakeRunner(), True)
        self.assertEqual({r.status for r in results}, {report.OK})


class ReportTest(unittest.TestCase):
    def test_exit_code_is_zero_only_without_failures(self) -> None:
        ok = report.passed("Specs", "a")
        idle = report.inactive("Backend", "b", "no existe backend/pyproject.toml")
        bad = report.failed("Código", "c", ["backend/app/a.py: 251 líneas"])
        self.assertEqual(report.exit_code([ok, idle]), 0)
        self.assertEqual(report.exit_code([ok, idle, bad]), 1)

    def test_render_never_shows_an_inactive_check_as_passed(self) -> None:
        idle = report.inactive("Backend", "pytest", "no existe backend/pyproject.toml")
        text = report.render([report.passed("Specs", "a"), idle])
        self.assertIn("INACTIVO", text)
        self.assertIn("no existe backend/pyproject.toml", text)
        self.assertIn("1 inactiva", text)
        self.assertIn("VERDE", text)

    def test_render_shows_failures_and_their_details(self) -> None:
        bad = report.failed("Código", "tamaño", ["backend/app/a.py: 251 líneas"])
        text = report.render([bad])
        self.assertIn("FALLO", text)
        self.assertIn("backend/app/a.py: 251 líneas", text)
        self.assertIn("ROJO", text)


if __name__ == "__main__":
    unittest.main()
