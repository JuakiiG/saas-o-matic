"""Tests of the oracle checks about specs: gate on disk, index and assumptions."""

from __future__ import annotations

import unittest

from oracle import checks_specs, report
from tests import support

SPECS = support.SPECS_DIR


class GateOnDiskTest(unittest.TestCase):
    def test_code_without_approved_spec_fails_and_names_the_file(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        files = ["backend/.gitkeep", "backend/README.md", "backend/app/probe.py", "CLAUDE.md"]
        result = checks_specs.check_gate(root, files)
        self.assertEqual(result.status, report.FAIL)
        self.assertEqual(len(result.details), 1)
        self.assertIn("backend/app/probe.py", result.details[0])

    def test_no_code_or_approved_block_passes(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        self.assertEqual(checks_specs.check_gate(root, ["backend/.gitkeep"]).status, report.OK)
        root = support.make_repo(self, support.BACKEND_OK)
        self.assertEqual(checks_specs.check_gate(root, ["backend/app/main.py"]).status, report.OK)
        self.assertEqual(checks_specs.check_gate(root, ["frontend/src/main.ts"]).status, report.FAIL)


class IndexTest(unittest.TestCase):
    def test_matching_states_pass(self) -> None:
        root = support.make_repo(self, support.BACKEND_OK)
        self.assertEqual(checks_specs.check_index(root / SPECS).status, report.OK)

    def test_header_and_index_disagreeing_fails(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        support.write(root / SPECS / support.SPEC_NAMES["SPEC-02"], support.spec_text("SPEC-02", "aprobada"))
        result = checks_specs.check_index(root / SPECS)
        self.assertEqual(result.status, report.FAIL)
        self.assertIn("SPEC-02", result.details[0])

    def test_spec_missing_from_the_index_fails(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        partial = {k: v for k, v in support.BORRADOR.items() if k != "SPEC-04"}
        support.write(root / SPECS / "README.md", support.index_text(partial))
        self.assertEqual(checks_specs.check_index(root / SPECS).status, report.FAIL)


class AssumptionsTest(unittest.TestCase):
    def test_draft_spec_may_depend_on_an_open_assumption(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        text = support.spec_text("SPEC-01", "borrador", "A6 (`decidido`) · A2 (`pendiente de confirmar`)")
        support.write(root / SPECS / support.SPEC_NAMES["SPEC-01"], text)
        result = checks_specs.check_assumptions(root / SPECS, root / support.ASSUMPTIONS)
        self.assertEqual(result.status, report.OK)

    def test_approved_spec_with_an_open_assumption_fails(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        text = support.spec_text("SPEC-01", "aprobada", "A6 (`decidido`) · A2 (`pendiente de confirmar`)")
        support.write(root / SPECS / support.SPEC_NAMES["SPEC-01"], text)
        result = checks_specs.check_assumptions(root / SPECS, root / support.ASSUMPTIONS)
        self.assertEqual(result.status, report.FAIL)
        self.assertIn("A2", result.details[0])

    def test_approved_spec_citing_an_unknown_assumption_fails(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        text = support.spec_text("SPEC-01", "aprobada", "A6 y A99")
        support.write(root / SPECS / support.SPEC_NAMES["SPEC-01"], text)
        result = checks_specs.check_assumptions(root / SPECS, root / support.ASSUMPTIONS)
        self.assertEqual(result.status, report.FAIL)


if __name__ == "__main__":
    unittest.main()
