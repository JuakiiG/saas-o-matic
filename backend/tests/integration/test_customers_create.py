"""`POST /customers` (SPEC-01: 4.1 and tables 5.7 and 5.8)."""

import logging
import re
from collections.abc import Iterator
from contextlib import closing
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from httpx2 import Response

from app.domain.customers import search_form
from app.main import create_app
from app.repositories.database import Database
from tests.customer_cases import (
    EXTRA_INVALID_ROWS,
    FIELDS,
    INVALID_ROWS,
    VALID_ROWS,
    customer_with,
)
from tests.integration.test_generic_errors import assert_problem

# The example of 4.1: what is sent and what is answered, except `id` and `created_at`.
EXAMPLE_REQUEST: dict[str, object] = {
    "company_name": "  Ejemplo Uno SL ",
    "tax_id": "b-1234567 4",
}
EXAMPLE_RESPONSE = {
    "company_name": "Ejemplo Uno SL",
    "tax_id": "B12345674",
    "contact_email": "compras@ejemplo-uno.example",
    "country": "ES",
    "plan": "professional",
}
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
STORED_COLUMNS = (
    "SELECT id, company_name, company_name_search, tax_id, contact_email, country, plan,"
    " created_at FROM customers ORDER BY id"
)


@pytest.fixture
def database(tmp_path: Path) -> Database:
    return Database(tmp_path / "data" / "customers.db")


@pytest.fixture
def client(
    tmp_path: Path, database: Database, monkeypatch: pytest.MonkeyPatch
) -> Iterator[TestClient]:
    """The real application, started, with an empty database."""
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "data" / "customers.db"))
    with TestClient(create_app()) as started:
        yield started


def create(client: TestClient, changes: dict[str, object]) -> Response:
    return client.post("/customers", json=customer_with(changes))


def field_codes(response: Response) -> list[tuple[str, str]]:
    errors = assert_problem(response, 422, "validation_error")["errors"]
    assert isinstance(errors, list)
    return [(error["field"], error["code"]) for error in errors]


def stored_customers(database: Database) -> list[tuple[object, ...]]:
    with closing(database.connect()) as connection:
        rows: list[tuple[object, ...]] = connection.execute(STORED_COLUMNS).fetchall()
        return rows


def test_valid_customer_is_created_with_201_its_location_and_the_stored_fields(
    client: TestClient,
) -> None:
    """SPEC-01/E-01, SPEC-01/E-02, SPEC-01/E-08: the example of 4.1 (CA-06)."""
    response = create(client, EXAMPLE_REQUEST)
    assert response.status_code == 201
    assert response.headers["content-type"] == "application/json"
    assert response.headers.get("location") == "/customers/1"
    body = response.json()
    assert list(body) == ["id", *FIELDS, "created_at"]
    assert body == {"id": 1, **EXAMPLE_RESPONSE, "created_at": body["created_at"]}
    assert TIMESTAMP.fullmatch(body["created_at"])


def test_created_customer_is_stored_with_the_search_form_of_its_name(
    client: TestClient, database: Database
) -> None:
    """SPEC-01/E-33, SPEC-01/E-08: the stored row, with its search column (CA-18)."""
    response = create(client, {"company_name": " Ñandú Pruebas SL ", "tax_id": "b-1234567 4"})
    assert response.status_code == 201
    body = response.json()
    assert stored_customers(database) == [
        (
            1,
            "Ñandú Pruebas SL",
            search_form("Ñandú Pruebas SL"),
            "B12345674",
            "compras@ejemplo-uno.example",
            "ES",
            "professional",
            body["created_at"],
        )
    ]
    assert search_form("Ñandú Pruebas SL") == "nandu pruebas sl"


@pytest.mark.parametrize(("changes", "stored"), VALID_ROWS, ids=ascii)
def test_valid_field_is_accepted_and_answered_trimmed_or_normalized(
    client: TestClient, changes: dict[str, object], stored: dict[str, str]
) -> None:
    """SPEC-01/E-02, SPEC-01/E-03, SPEC-01/E-04, SPEC-01/E-34: the valid rows of 5.7 (CA-07)."""
    response = create(client, changes)
    assert response.status_code == 201
    assert {field: response.json()[field] for field in stored} == stored


@pytest.mark.parametrize(("changes", "expected"), INVALID_ROWS + EXTRA_INVALID_ROWS, ids=ascii)
def test_invalid_customer_returns_422_with_one_code_per_field_and_stores_nothing(
    client: TestClient,
    database: Database,
    changes: dict[str, object],
    expected: list[tuple[str, str]],
) -> None:
    """SPEC-01/E-03, SPEC-01/E-04, SPEC-01/E-05, SPEC-01/E-06, SPEC-01/E-07: rows of 5.7 (CA-07).

    Also SPEC-01/E-15, SPEC-01/E-16, SPEC-01/E-18, SPEC-01/E-34 and SPEC-01/E-35: the two
    codes of the identifier are different ones (CA-08) and `errors` follows the contract.
    """
    assert field_codes(create(client, changes)) == expected
    assert stored_customers(database) == []


@pytest.mark.parametrize("content", [None, b"{}"], ids=["absent-body", "empty-object"])
def test_customer_without_fields_returns_422_with_the_five_missing(
    client: TestClient, content: bytes | None
) -> None:
    """SPEC-01/E-07: an absent body is an empty object: five `missing`, in contract order."""
    headers = {"content-type": "application/json"} if content else {}
    response = client.post("/customers", content=content, headers=headers)
    assert field_codes(response) == [(field, "missing") for field in FIELDS]


def test_wrong_check_character_never_tells_the_right_one(client: TestClient) -> None:
    """SPEC-01/E-17: two identifiers with different right letters, the same body (CA-09)."""
    first = create(client, {"tax_id": "12345678A"})
    second = create(client, {"tax_id": "00000000A"})
    assert field_codes(first) == [("tax_id", "invalid_tax_id_check_character")]
    assert first.content == second.content
    assert "12345678" not in first.text


def test_duplicate_of_country_and_normalized_identifier_returns_409(
    client: TestClient, database: Database
) -> None:
    """SPEC-01/E-19: `customer_already_exists`, compared in normalized form (5.8, CA-10)."""
    assert create(client, {}).status_code == 201
    stored = stored_customers(database)
    for tax_id in ("B12345674", "b-1234567 4"):
        body = assert_problem(create(client, {"tax_id": tax_id}), 409, "customer_already_exists")
        assert body["title"] == "Conflict"
        # Nothing about the customer that already exists (D-06).
        assert sorted(body) == ["code", "detail", "status", "title", "type"]
    assert stored_customers(database) == stored


def test_same_identifier_in_another_country_and_same_name_are_not_duplicates(
    client: TestClient, database: Database
) -> None:
    """SPEC-01/E-20: unique by country and identifier, not by name (5.8, CA-10)."""
    assert create(client, {}).status_code == 201
    assert create(client, {"country": "PT"}).status_code == 201
    assert create(client, {"tax_id": "A12345674"}).status_code == 201
    assert [row[0] for row in stored_customers(database)] == [1, 2, 3]


def test_validation_wins_over_a_duplicate(client: TestClient, database: Database) -> None:
    """SPEC-01/E-21: a duplicate with an invalid email answers 422 (5.8, CA-10)."""
    assert create(client, {}).status_code == 201
    response = create(client, {"contact_email": "sin-arroba.example"})
    assert field_codes(response) == [("contact_email", "invalid_email")]
    assert len(stored_customers(database)) == 1


def test_valid_customer_without_database_returns_503_and_creates_nothing(
    client: TestClient, tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """SPEC-03/E-29: an endpoint that cannot write to the database answers 503."""
    path = tmp_path / "data" / "customers.db"
    path.rename(tmp_path / "moved-away.db")
    with caplog.at_level(logging.ERROR):
        response = create(client, {})
    assert_problem(response, 503, "service_unavailable")
    assert not path.exists()
    assert caplog.records
