"""Tests of the size limits and of the silenced-rule and skipped-test checks."""

from __future__ import annotations

import unittest

from oracle import checks_code, report
from tests import support

# The markers are assembled here so that this file does not trip the checks it tests.
NOQA = "# no" + "qa"
TYPE_IGNORE = "# type: " + "ignore"
ESLINT_OFF = "eslint-" + "disable"
SKIP_MARK = "@pytest.mark." + "skip"
XFAIL_MARK = "@pytest.mark." + "xfail"


def lines(count: int) -> str:
    return "".join(f"x{i} = {i}\n" for i in range(count))


def function(body_lines: int, params: str = "") -> str:
    body = "".join(f"    v{i} = {i}\n" for i in range(body_lines))
    return f"def sample({params}):\n{body}"


class FileSizeTest(unittest.TestCase):
    def check(self, files: dict[str, str]) -> report.Result:
        root = support.make_repo(self, support.BORRADOR)
        for name, text in files.items():
            support.write(root / name, text)
        return checks_code.check_file_sizes(root, list(files))

    def test_limits(self) -> None:
        self.assertEqual(self.check({"backend/app/a.py": lines(250)}).status, report.OK)
        self.assertEqual(self.check({"backend/app/a.py": lines(251)}).status, report.FAIL)
        self.assertEqual(self.check({"scripts/oracle/a.py": lines(251)}).status, report.FAIL)
        self.assertEqual(self.check({"frontend/src/app/a.ts": lines(251)}).status, report.FAIL)

    def test_tests_and_non_code_are_not_counted(self) -> None:
        files = {
            "backend/tests/unit/test_a.py": lines(400),
            "frontend/src/app/a.spec.ts": lines(400),
            "ai-workspace/01-specs/SPEC-01.md": lines(900),
        }
        self.assertEqual(self.check(files).status, report.OK)

    def test_angular_template_limit_is_120(self) -> None:
        self.assertEqual(self.check({"frontend/src/app/a.html": "<p></p>\n" * 120}).status, report.OK)
        result = self.check({"frontend/src/app/a.html": "<p></p>\n" * 121})
        self.assertEqual(result.status, report.FAIL)
        self.assertIn("121", result.details[0])


class FunctionLimitsTest(unittest.TestCase):
    def check(self, text: str, name: str = "scripts/oracle/a.py") -> report.Result:
        root = support.make_repo(self, support.BORRADOR)
        support.write(root / name, text)
        return checks_code.check_functions(root, [name])

    def test_function_length(self) -> None:
        self.assertEqual(self.check(function(39)).status, report.OK)
        result = self.check(function(40))
        self.assertEqual(result.status, report.FAIL)
        self.assertIn("sample", result.details[0])

    def test_parameters(self) -> None:
        self.assertEqual(self.check(function(1, "a, b, c, d, e")).status, report.OK)
        self.assertEqual(self.check(function(1, "a, b, c, d, e, f")).status, report.FAIL)
        self.assertEqual(self.check(function(1, "a, b, *, c, d, e, f")).status, report.FAIL)
        method = "class K:\n    def m(self, a, b, c, d, e):\n        return a\n"
        self.assertEqual(self.check(method).status, report.OK)

    def test_tests_are_checked_too_and_syntax_errors_are_reported(self) -> None:
        self.assertEqual(self.check(function(40), "backend/tests/unit/test_a.py").status, report.FAIL)
        result = self.check("def broken(:\n")
        self.assertEqual(result.status, report.FAIL)


class SuppressionsTest(unittest.TestCase):
    def check(self, name: str, text: str) -> report.Result:
        root = support.make_repo(self, support.BORRADOR)
        support.write(root / name, text)
        return checks_code.check_suppressions(root, [name])

    def test_unjustified_markers_fail(self) -> None:
        for name, text in (
            ("backend/app/a.py", f"x = 1  {NOQA}\n"),
            ("backend/app/a.py", f"x = 1  {NOQA}: E501\n"),
            ("backend/app/a.py", f"x = f()  {TYPE_IGNORE}[arg-type]\n"),
            ("frontend/src/a.ts", f"// {ESLINT_OFF}-next-line no-console\n"),
            ("frontend/src/a.html", f"<!-- {ESLINT_OFF} -->\n"),
        ):
            with self.subTest(text=text):
                self.assertEqual(self.check(name, text).status, report.FAIL)

    def test_justified_markers_pass(self) -> None:
        for name, text in (
            ("backend/app/a.py", f"x = 1  {NOQA}: E501 -- the URL cannot be split\n"),
            ("backend/app/a.py", f"x = f()  {TYPE_IGNORE}[arg-type]  # stub of the library is wrong\n"),
            ("frontend/src/a.ts", f"// {ESLINT_OFF}-next-line no-console -- startup banner\n"),
            ("backend/app/a.py", "x = 1  # plain comment\n"),
        ):
            with self.subTest(text=text):
                self.assertEqual(self.check(name, text).status, report.OK)


class SkippedTestsTest(unittest.TestCase):
    def check(self, name: str, text: str) -> report.Result:
        root = support.make_repo(self, support.BORRADOR)
        support.write(root / name, text)
        return checks_code.check_skipped_tests(root, [name])

    def test_skipped_or_focused_tests_fail(self) -> None:
        for name, text in (
            ("backend/tests/test_a.py", f"{SKIP_MARK}\ndef test_a(): ...\n"),
            ("backend/tests/test_a.py", f"{XFAIL_MARK}\ndef test_a(): ...\n"),
            ("scripts/tests/test_a.py", "@unittest." + "skip('later')\ndef test_a(): ...\n"),
            ("frontend/src/a.spec.ts", "x" + "it('should work', () => {});\n"),
            ("frontend/src/a.spec.ts", "f" + "describe('Unit', () => {});\n"),
            ("frontend/src/a.spec.ts", "it." + "only('should work', () => {});\n"),
            ("frontend/src/a.spec.ts", "describe." + "skip('Unit', () => {});\n"),
        ):
            with self.subTest(text=text):
                self.assertEqual(self.check(name, text).status, report.FAIL)

    def test_ordinary_tests_pass(self) -> None:
        text = "it('should submit the form', () => { benefit(); submit(); });\n"
        self.assertEqual(self.check("frontend/src/a.spec.ts", text).status, report.OK)
        self.assertEqual(self.check("backend/tests/test_a.py", "def test_a(): ...\n").status, report.OK)


if __name__ == "__main__":
    unittest.main()
