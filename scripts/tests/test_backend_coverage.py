"""Tests of how the oracle runs the backend tools: locked environment and real branch coverage."""

from __future__ import annotations

import unittest
from pathlib import Path

from oracle import checks_stack, report
from tests import support

BRANCHES = "ramas cubiertas"


def backend_project(case: unittest.TestCase) -> Path:
    root = support.make_repo(case, support.BACKEND_OK)
    support.write(root / "backend" / "pyproject.toml", "[project]\n")
    return root


def branch_check(case: unittest.TestCase, runner: support.FakeRunner) -> report.Result:
    """The one backend result that judges branches alone."""
    results = checks_stack.backend_checks(backend_project(case), runner)
    found = [result for result in results if BRANCHES in result.name]
    case.assertEqual(len(found), 1, [result.name for result in results])
    return found[0]


class LockedEnvironmentTest(unittest.TestCase):
    def test_every_backend_tool_runs_with_the_lock_enforced(self) -> None:
        runner = support.FakeRunner()
        checks_stack.backend_checks(backend_project(self), runner)
        self.assertTrue(runner.commands)
        for command in runner.commands:
            self.assertEqual(command[:3], ["uv", "run", "--locked"], command)


class BranchCoverageTest(unittest.TestCase):
    def test_covered_statements_do_not_hide_untested_branches(self) -> None:
        # Combined: (96 + 2) / (96 + 4) = 98 %, above the threshold. Branches alone: 50 %.
        totals = {"covered_lines": 96, "num_statements": 96, "covered_branches": 2, "num_branches": 4}
        result = branch_check(self, support.FakeRunner(totals=totals))
        self.assertEqual(result.status, report.FAIL)
        self.assertIn("2 de 4", " ".join(result.details))

    def test_the_case_of_the_review_fails_on_branches(self) -> None:
        # 11 of 11 statements and 2 of 4 branches: 86.67 % combined, 50 % of branches.
        totals = {"covered_lines": 11, "num_statements": 11, "covered_branches": 2, "num_branches": 4}
        self.assertEqual(branch_check(self, support.FakeRunner(totals=totals)).status, report.FAIL)

    def test_exactly_90_percent_of_branches_passes_and_shows_the_count(self) -> None:
        result = branch_check(self, support.FakeRunner(totals={"covered_branches": 9, "num_branches": 10}))
        self.assertEqual(result.status, report.OK)
        self.assertIn("9 de 10", " ".join(result.details))

    def test_just_below_90_percent_of_branches_fails(self) -> None:
        totals: dict[str, object] = {"covered_branches": 899, "num_branches": 1000}
        self.assertEqual(branch_check(self, support.FakeRunner(totals=totals)).status, report.FAIL)

    def test_code_without_branches_is_inactive_never_passed(self) -> None:
        result = branch_check(self, support.FakeRunner(totals={"covered_branches": 0, "num_branches": 0}))
        self.assertEqual(result.status, report.INACTIVE)

    def test_a_report_without_branch_data_fails(self) -> None:
        result = branch_check(self, support.FakeRunner(totals={"covered_lines": 4, "num_statements": 4}))
        self.assertEqual(result.status, report.FAIL)

    def test_a_failing_coverage_command_fails_the_check(self) -> None:
        result = branch_check(self, support.FakeRunner(failing="json"))
        self.assertEqual(result.status, report.FAIL)
        self.assertIn("boom", " ".join(result.details))

    def test_the_combined_threshold_is_kept(self) -> None:
        runner = support.FakeRunner()
        checks_stack.backend_checks(backend_project(self), runner)
        flat = [" ".join(command) for command in runner.commands]
        self.assertTrue(any("--cov-branch --cov-fail-under=90" in line for line in flat), flat)
        self.assertTrue(any("--fail-under=100" in line for line in flat), flat)

    def test_the_branch_check_is_inactive_without_the_project(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        results = checks_stack.backend_checks(root, support.FakeRunner())
        found = [result for result in results if BRANCHES in result.name]
        self.assertEqual([result.status for result in found], [report.INACTIVE])


if __name__ == "__main__":
    unittest.main()
