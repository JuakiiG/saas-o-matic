"""Tests of the spec gate shared by the hook and the oracle."""

from __future__ import annotations

import unittest

from oracle import specgate
from tests import support

SPECS = support.SPECS_DIR


class SpecStateTest(unittest.TestCase):
    def test_reads_the_state_from_the_header(self) -> None:
        root = support.make_repo(self, support.BACKEND_OK)
        self.assertEqual(specgate.spec_state(root / SPECS, "SPEC-01"), "aprobada")
        self.assertEqual(specgate.spec_state(root / SPECS, "SPEC-04"), "borrador")

    def test_missing_or_unreadable_spec_is_unknown(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        (root / SPECS / support.SPEC_NAMES["SPEC-02"]).unlink()
        support.write(root / SPECS / support.SPEC_NAMES["SPEC-03"], "# sin cabecera\n")
        self.assertEqual(specgate.spec_state(root / SPECS, "SPEC-02"), "desconocido")
        self.assertEqual(specgate.spec_state(root / SPECS, "SPEC-03"), "desconocido")

    def test_state_without_date_or_outside_the_header_does_not_count(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        text = "# SPEC-01\n\n| **Estado** | `aprobada` |\n\nEl estado será `aprobada` (2026-11-12).\n"
        support.write(root / SPECS / support.SPEC_NAMES["SPEC-01"], text)
        self.assertEqual(specgate.spec_state(root / SPECS, "SPEC-01"), "desconocido")


class DecideTest(unittest.TestCase):
    def assert_actions(self, states: dict[str, str], cases: list[tuple[str, str]]) -> None:
        root = support.make_repo(self, states)
        for target, expected in cases:
            with self.subTest(target=target):
                self.assertEqual(specgate.decide(root, target, "").action, expected)

    def test_everything_in_draft_blocks_backend_and_frontend(self) -> None:
        self.assert_actions(
            support.BORRADOR,
            [
                ("backend/app/domain/pricing.py", "deny"),
                ("backend/tests/unit/test_pricing.py", "deny"),
                ("backend/pyproject.toml", "deny"),
                ("frontend/src/app/app.ts", "deny"),
                ("frontend/src/app/app.spec.ts", "deny"),
                ("frontend/e2e/alta.spec.ts", "deny"),
                ("frontend/package.json", "deny"),
                ("backend\\app\\main.py", "deny"),
                ("ai-workspace/../backend/app/main.py", "deny"),
                ("BACKEND/app/main.py", "deny"),
                ("./frontend/src/main.ts", "deny"),
            ],
        )

    def test_everything_in_draft_allows_what_is_not_application_code(self) -> None:
        self.assert_actions(
            support.BORRADOR,
            [
                ("backend/README.md", "allow"),
                ("backend/.gitkeep", "allow"),
                ("frontend/README.md", "allow"),
                ("ai-workspace/03-proceso/sesion-03.md", "allow"),
                ("scripts/check.py", "allow"),
                ("scripts/tests/test_specgate.py", "allow"),
                ("README.md", "allow"),
                ("backend-notes.md", "allow"),
            ],
        )

    def test_absolute_paths_inside_and_outside_the_project(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        inside = str(root / "backend" / "app" / "main.py")
        outside = str(root.parent / "otro-proyecto" / "backend" / "main.py")
        self.assertEqual(specgate.decide(root, inside, "").action, "deny")
        self.assertEqual(specgate.decide(root, outside, "").action, "allow")

    def test_backend_block_needs_its_three_specs(self) -> None:
        partial = {**support.BACKEND_OK, "SPEC-03": "borrador"}
        root = support.make_repo(self, partial)
        decision = specgate.decide(root, "backend/app/main.py", "")
        self.assertEqual(decision.action, "deny")
        self.assertIn("SPEC-03", decision.reason)
        self.assertNotIn("SPEC-01", decision.reason)

    def test_backend_approved_opens_backend_only(self) -> None:
        self.assert_actions(
            support.BACKEND_OK,
            [
                ("backend/app/main.py", "allow"),
                ("backend/tests/unit/test_x.py", "allow"),
                ("frontend/src/app/app.ts", "deny"),
            ],
        )

    def test_everything_approved_opens_frontend(self) -> None:
        self.assert_actions(support.ALL_OK, [("frontend/src/app/app.ts", "allow")])

    def test_missing_spec_fails_closed(self) -> None:
        root = support.make_repo(self, support.ALL_OK)
        (root / SPECS / support.SPEC_NAMES["SPEC-04"]).unlink()
        self.assertEqual(specgate.decide(root, "frontend/src/main.ts", "").action, "deny")

    def test_gate_files_ask_for_human_confirmation(self) -> None:
        self.assert_actions(
            support.ALL_OK,
            [
                (".claude/settings.json", "ask"),
                (".claude/settings.local.json", "ask"),
                ("scripts/hooks/pre_tool_use.py", "ask"),
                ("scripts/oracle/specgate.py", "ask"),
                ("scripts/oracle/report.py", "allow"),
            ],
        )

    def test_writing_the_approved_state_in_a_spec_asks(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        spec = "ai-workspace/01-specs/SPEC-01-clientes.md"
        self.assertEqual(specgate.decide(root, spec, "| **Estado** | `aprobada` (2026-11-13) |").action, "ask")
        self.assertEqual(specgate.decide(root, spec, "Aprobada").action, "ask")
        self.assertEqual(specgate.decide(root, spec, "Un requisito nuevo.").action, "allow")
        other = "ai-workspace/03-proceso/sesion-03.md"
        self.assertEqual(specgate.decide(root, other, "la spec está aprobada").action, "allow")


if __name__ == "__main__":
    unittest.main()
