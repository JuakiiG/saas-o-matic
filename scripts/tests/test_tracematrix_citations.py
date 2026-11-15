"""Tests of the citation grammar and of how the tests of each kind of file are found."""

from __future__ import annotations

import unittest

from tracematrix import citations

PYTHON = '''
def helper():
    """SPEC-01/E-09: a helper is not a test."""


def test_one():
    """SPEC-01/E-01, SPEC-01/E-02: two requirements (CA-06)."""


class TestGroup:
    def test_two(self):
        """SPEC-03/E-24 a E-26: a range."""

    def test_three(self):
        pass
'''

# Formatted as Prettier leaves it: a block ends where a declaration starts at its indent or less.
TYPESCRIPT = """
// SPEC-04/E-99: a comment is not a citation of a test.
describe('Alta · SPEC-04/E-05 a E-07, E-40 (CA-05)', () => {
  it('should send the form', () => {
    // SPEC-04/E-50: neither is a comment in the body.
    expect(1).toBe(1);
  });

  it.each([
    ['a', { b: 1 }],
    ['c', { d: 2 }],
  ])('should show %s next to its field (SPEC-04/E-09)', (name, value) => {
    expect(name).toBe(value);
  });

  it.each(['x', 'y'])(
    'should reject %s without calling the API (SPEC-04/E-45, E-46)',
    (text) => {
      expect(text).toBe('');
    },
  );

  describe('nested · SPEC-01/E-26', () => {
    it('should keep both blocks', () => {});
  });
});

describe('No citation', () => {
  it('should cite on its own (SPEC-04/E-57)', () => {});
});
"""

PLAYWRIGHT = """
test.use({ viewport: { width: 375, height: 667 } });

test.describe('Width of 375 px', () => {
  test.beforeAll(async () => {});

  for (const size of SIZES) {
    test(`should not scroll sideways at ${size.width} px (SPEC-04/CA-13, E-30)`, async ({
      page,
    }) => {
      await page.goto('/');
    });
  }
});
"""


def spec04(*ids: str) -> frozenset[citations.Citation]:
    return frozenset(("SPEC-04", item) for item in ids)


class ParseCitationsTest(unittest.TestCase):
    def test_single_citation(self) -> None:
        self.assertEqual(citations.parse_citations("SPEC-02/E-03: rounding"), {("SPEC-02", "E-03")})

    def test_list_takes_the_spec_of_its_prefix(self) -> None:
        found = citations.parse_citations("Journeys · SPEC-04/E-31, E-52 y E-53 (CA-09)")
        self.assertEqual(found, spec04("E-31", "E-52", "E-53"))

    def test_range_is_expanded(self) -> None:
        found = citations.parse_citations("Alta · SPEC-04/E-08 a E-11, E-40")
        self.assertEqual(found, spec04("E-08", "E-09", "E-10", "E-11", "E-40"))

    def test_criteria_are_cited_like_requirements(self) -> None:
        found = citations.parse_citations("(SPEC-04/CA-13, E-30)")
        self.assertEqual(found, spec04("CA-13", "E-30"))

    def test_ids_without_a_spec_are_not_citations(self) -> None:
        self.assertEqual(citations.parse_citations("the row of 5.5 (E-29, CA-08)"), set())

    def test_a_list_ends_at_anything_else(self) -> None:
        found = citations.parse_citations("SPEC-04/E-29, 5.5; see E-30. SPEC-01/E-26")
        self.assertEqual(found, {("SPEC-04", "E-29"), ("SPEC-01", "E-26")})


class PythonTestsTest(unittest.TestCase):
    def test_every_test_function_with_its_docstring(self) -> None:
        found = citations.python_tests("backend/tests/test_a.py", PYTHON)
        self.assertEqual({test.file for test in found}, {"backend/tests/test_a.py"})
        self.assertEqual([test.line for test in found], [6, 11, 14])
        self.assertEqual(found[0].own, {("SPEC-01", "E-01"), ("SPEC-01", "E-02")})
        self.assertEqual(found[1].own, {("SPEC-03", "E-24"), ("SPEC-03", "E-25"), ("SPEC-03", "E-26")})
        self.assertEqual(found[2].own, frozenset())
        self.assertEqual({test.inherited for test in found}, {frozenset()})

    def test_a_file_that_cannot_be_parsed_is_an_error(self) -> None:
        with self.assertRaises(SyntaxError):
            citations.python_tests("backend/tests/test_a.py", "def test_(:\n")


class TypescriptTestsTest(unittest.TestCase):
    def test_tests_inherit_the_citations_of_their_blocks(self) -> None:
        found = citations.typescript_tests("a.spec.ts", TYPESCRIPT)
        block = spec04("E-05", "E-06", "E-07", "E-40")
        self.assertEqual([test.line for test in found], [4, 9, 16, 24, 29])
        self.assertEqual([test.inherited for test in found[:3]], [block] * 3)
        self.assertEqual(found[3].inherited, block | {("SPEC-01", "E-26")})
        self.assertEqual(found[4].inherited, frozenset())

    def test_own_citations_come_from_the_title_only(self) -> None:
        found = citations.typescript_tests("a.spec.ts", TYPESCRIPT)
        own = [test.own for test in found]
        self.assertEqual(own[0], frozenset())
        self.assertEqual(own[1], spec04("E-09"))
        self.assertEqual(own[2], spec04("E-45", "E-46"))
        self.assertEqual(own[4], spec04("E-57"))

    def test_playwright_tests_and_not_their_hooks(self) -> None:
        found = citations.typescript_tests("e2e/a.spec.ts", PLAYWRIGHT)
        self.assertEqual([test.line for test in found], [8])
        self.assertEqual(found[0].own, spec04("CA-13", "E-30"))
        self.assertEqual(found[0].cited, spec04("CA-13", "E-30"))


if __name__ == "__main__":
    unittest.main()
