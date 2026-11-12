"""Tests of the checks that stay inactive until the backend exists: purity, layers, traceability."""

from __future__ import annotations

import unittest

from oracle import checks_purity, checks_trace, report
from tests import support

DOMAIN = "backend/app/domain/pricing.py"


class PurityTest(unittest.TestCase):
    def check(self, text: str) -> report.Result:
        root = support.make_repo(self, support.BACKEND_OK)
        support.write(root / DOMAIN, text)
        return checks_purity.check_domain_purity(root)

    def test_inactive_until_the_domain_exists(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        self.assertEqual(checks_purity.check_domain_purity(root).status, report.INACTIVE)
        self.assertEqual(checks_purity.check_layers(root).status, report.INACTIVE)

    def test_pure_integer_code_passes(self) -> None:
        text = (
            "from dataclasses import dataclass\n"
            "from app.domain.tiers import TIERS\n"
            "from . import countries\n\n"
            "def tax(base: int, rate_bp: int) -> int:\n"
            "    return (base * rate_bp + 5000) // 10000\n"
        )
        self.assertEqual(self.check(text).status, report.OK)

    def test_impure_code_fails(self) -> None:
        for text in (
            "import fastapi\n",
            "from pydantic import BaseModel\n",
            "from app.services import quotes\n",
            "RATE = 0.21\n",
            "def half(n: int) -> int:\n    return n / 2\n",
            "def total(n: int) -> None:\n    n /= 2\n",
            "def as_number(text: str) -> float:\n    return float(text)\n",
        ):
            with self.subTest(text=text):
                self.assertEqual(self.check(text).status, report.FAIL)


class LayersTest(unittest.TestCase):
    def check(self, name: str, text: str) -> report.Result:
        root = support.make_repo(self, support.BACKEND_OK)
        support.write(root / DOMAIN, "X = 1\n")
        support.write(root / name, text)
        return checks_purity.check_layers(root)

    def test_allowed_directions_pass(self) -> None:
        for name, text in (
            ("backend/app/api/customers.py", "from app.services import customers\nfrom app.domain import tax_id\n"),
            ("backend/app/services/quotes.py", "from app.domain import pricing\nfrom app.repositories import customers\n"),
            ("backend/app/repositories/customers.py", "import sqlite3\n"),
            ("backend/app/repositories/customers.py", "import sqlite3\nfrom app.domain import customer\n"),
        ):
            with self.subTest(name=name, text=text):
                self.assertEqual(self.check(name, text).status, report.OK)

    def test_forbidden_directions_fail(self) -> None:
        for name, text in (
            ("backend/app/api/customers.py", "from app.repositories import customers\n"),
            ("backend/app/services/quotes.py", "from app.api import schemas\n"),
            ("backend/app/services/quotes.py", "import sqlite3\n"),
            ("backend/app/api/customers.py", "import sqlite3\n"),
            ("backend/app/repositories/customers.py", "from app.services import quotes\n"),
            ("backend/app/repositories/customers.py", "from app.api import schemas\n"),
            (DOMAIN, "from app.repositories import customers\n"),
            (DOMAIN, "from app.services import quotes\n"),
            (DOMAIN, "from app.api import schemas\n"),
            (DOMAIN, "import sqlite3\n"),
        ):
            with self.subTest(name=name, text=text):
                self.assertEqual(self.check(name, text).status, report.FAIL)


class TraceabilityTest(unittest.TestCase):
    def check(self, text: str | None, strict: bool = False) -> report.Result:
        root = support.make_repo(self, support.BACKEND_OK)
        if text is not None:
            support.write(root / "backend/tests/unit/test_pricing.py", text)
        return checks_trace.check_traceability(root, strict)

    def test_inactive_until_there_are_backend_tests(self) -> None:
        self.assertEqual(self.check(None).status, report.INACTIVE)

    def test_every_test_must_cite_an_existing_requirement(self) -> None:
        cited = 'def test_a():\n    """SPEC-02/E-01: base price."""\n'
        self.assertEqual(self.check(cited).status, report.OK)
        self.assertEqual(self.check("def test_a():\n    assert True\n").status, report.FAIL)
        unknown = 'def test_a():\n    """SPEC-02/E-99."""\n'
        result = self.check(unknown)
        self.assertEqual(result.status, report.FAIL)
        self.assertIn("SPEC-02/E-99", result.details[0])

    def test_uncovered_requirements_are_listed_and_only_fail_when_strict(self) -> None:
        cited = 'def test_a():\n    """SPEC-02/E-01."""\n'
        lenient = self.check(cited)
        self.assertEqual(lenient.status, report.OK)
        self.assertTrue(any("SPEC-02/E-02" in note for note in lenient.details))
        self.assertEqual(self.check(cited, strict=True).status, report.FAIL)


if __name__ == "__main__":
    unittest.main()
