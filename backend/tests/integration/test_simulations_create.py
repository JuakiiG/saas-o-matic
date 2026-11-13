"""`POST /simulations` (SPEC-03: 4.1 and tables 5.1 and 5.2)."""

import logging
import re
from collections.abc import Iterator
from contextlib import closing
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.domain import countries, pricing
from app.domain.pricing import Quote, Tier, calculate_quote
from app.main import create_app
from app.repositories.database import Database
from tests.integration.test_generic_errors import assert_problem
from tests.integration.test_pricing_quote import (
    CUSTOMERS,
    INSERT_CUSTOMER,
    SPAIN_15_USERS,
    field_codes,
    row_counts,
)
from tests.simulation_cases import (
    INVALID_ROWS,
    MAX_ID,
    REQUEST_FIELDS,
    RESPONSE_FIELDS,
    VALID_ROWS,
    VALID_SIMULATION,
    row_id,
    simulation_with,
    with_wrong_subtotal,
)

PROBLEM_JSON = "application/problem+json"
TIMESTAMP = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ")
# The fields that a simulation shares with a quote, in the order of the quote.
CALCULATION_FIELDS = list(SPAIN_15_USERS)
AMOUNT_FIELDS = ["base_cents", "tax_rate_bp", "tax_cents", "total_cents"]
SIMULATION_COLUMNS = [
    "customer_id",
    "active_users",
    "storage_gb",
    "estimated_api_calls",
    "country",
    "base_cents",
    "tax_rate_bp",
    "tax_cents",
    "total_cents",
    "created_at",
]
TIER_COLUMNS = ["from_users", "to_users", "unit_price_cents", "users", "subtotal_cents"]
SELECT_SIMULATION = (
    "SELECT customer_id, active_users, storage_gb, estimated_api_calls, country, base_cents,"
    " tax_rate_bp, tax_cents, total_cents, created_at FROM simulations WHERE id = ?"
)
SELECT_TIERS = (
    "SELECT from_users, to_users, unit_price_cents, users, subtotal_cents"
    " FROM simulation_tiers WHERE simulation_id = ? ORDER BY position"
)
# Customers, simulations and tiers before any simulation: the three customers of the fixture.
NOTHING_STORED = [3, 0, 0]


@pytest.fixture
def database(tmp_path: Path) -> Database:
    return Database(tmp_path / "data" / "simulations.db")


@pytest.fixture
def client(
    tmp_path: Path, database: Database, monkeypatch: pytest.MonkeyPatch
) -> Iterator[TestClient]:
    """The real application, started, with three customers: 1 is ES, 2 is DE, 3 has no rate."""
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "data" / "simulations.db"))
    with TestClient(create_app()) as started:
        with closing(database.connect()) as connection:
            connection.executemany(INSERT_CUSTOMER, CUSTOMERS)
            connection.commit()
        yield started


def stored_simulation(database: Database, simulation_id: int) -> dict[str, object]:
    """What the two tables keep of a simulation, with the names of the response."""
    with closing(database.connect()) as connection:
        row = connection.execute(SELECT_SIMULATION, (simulation_id,)).fetchone()
        tiers = connection.execute(SELECT_TIERS, (simulation_id,)).fetchall()
    assert row is not None
    stored: dict[str, object] = dict(zip(SIMULATION_COLUMNS, row, strict=True))
    stored["tiers"] = [dict(zip(TIER_COLUMNS, tier, strict=True)) for tier in tiers]
    return stored


def test_simulation_of_the_example_returns_201_with_the_body_of_the_spec(
    client: TestClient,
) -> None:
    """SPEC-03/E-01, SPEC-03/E-03: the request and the response of 4.1, to the letter (CA-01)."""
    response = client.post("/simulations", json=VALID_SIMULATION)
    assert response.status_code == 201
    assert response.headers["content-type"] == "application/json"
    # There is no endpoint to read one simulation: the response points nowhere.
    assert "location" not in response.headers
    body = response.json()
    assert list(body) == RESPONSE_FIELDS
    assert TIMESTAMP.fullmatch(body["created_at"])
    expected = {**VALID_SIMULATION, **SPAIN_15_USERS, "id": 1, "created_at": body["created_at"]}
    assert body == expected


@pytest.mark.parametrize("row", VALID_ROWS, ids=ascii)
def test_valid_simulation_answers_and_stores_the_amounts_of_the_table(
    client: TestClient, database: Database, row: tuple[int, ...]
) -> None:
    """SPEC-03/E-01, SPEC-03/E-03, SPEC-03/E-04, SPEC-03/E-19: every row of 5.1 (CA-02)."""
    customer_id, users, storage, calls, *amounts = row
    request = dict(zip(REQUEST_FIELDS, (customer_id, users, storage, calls), strict=True))
    response = client.post("/simulations", json=request)
    assert response.status_code == 201
    body = response.json()
    assert [body[field] for field in AMOUNT_FIELDS] == amounts
    assert {field: body[field] for field in REQUEST_FIELDS} == request
    stored = stored_simulation(database, body["id"])
    assert stored == {field: body[field] for field in stored}
    assert len(body["tiers"]) == 3


@pytest.mark.parametrize("row", VALID_ROWS, ids=ascii)
def test_simulation_has_the_calculation_that_the_quote_answers(
    client: TestClient, row: tuple[int, ...]
) -> None:
    """SPEC-03/E-02, SPEC-02/E-08: the calculation fields are those of the quote (CA-03)."""
    customer_id, users, storage, calls, *_ = row
    request = dict(zip(REQUEST_FIELDS, (customer_id, users, storage, calls), strict=True))
    quote = client.post("/pricing/quote", json={"customer_id": customer_id, "active_users": users})
    assert quote.status_code == 200
    simulation = client.post("/simulations", json=request)
    assert simulation.status_code == 201
    body = simulation.json()
    assert {field: body[field] for field in CALCULATION_FIELDS} == quote.json()


def test_simulation_and_quote_follow_the_same_change_of_the_fee_and_of_the_rate(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """SPEC-03/E-02, SPEC-02/E-08: one calculation, so a change of it reaches both endpoints."""
    monkeypatch.setattr(pricing, "TIERS", (Tier(1, 10, 2000), *pricing.TIERS[1:]))
    monkeypatch.setitem(countries._TAX_RATES_BP, "ES", 1000)
    simulation = client.post("/simulations", json=VALID_SIMULATION)
    assert simulation.status_code == 201
    body = simulation.json()
    # The amounts of 5.4 with the fee and the rate substituted.
    assert [body[field] for field in AMOUNT_FIELDS] == [24000, 1000, 2400, 26400]
    quote = client.post("/pricing/quote", json={"customer_id": 1, "active_users": 15})
    assert {field: body[field] for field in CALCULATION_FIELDS} == quote.json()


@pytest.mark.parametrize(
    ("changes", "expected"), INVALID_ROWS, ids=[row_id(changes) for changes, _ in INVALID_ROWS]
)
def test_invalid_simulation_returns_422_and_stores_nothing(
    client: TestClient,
    database: Database,
    changes: dict[str, object],
    expected: list[tuple[str, str]],
) -> None:
    """SPEC-03/E-05, SPEC-03/E-06, SPEC-03/E-07, SPEC-03/E-09: rows of 5.2 (CA-04)."""
    response = client.post("/simulations", json=simulation_with(changes))
    assert field_codes(response) == expected
    assert row_counts(database) == NOTHING_STORED


@pytest.mark.parametrize("content", [None, b"{}"], ids=["absent-body", "empty-object"])
def test_simulation_without_fields_returns_422_with_the_four_missing(
    client: TestClient, content: bytes | None
) -> None:
    """SPEC-03/E-06, SPEC-03/E-07: one `missing` per field, in the order of the contract."""
    headers = {"content-type": "application/json"} if content else {}
    response = client.post("/simulations", content=content, headers=headers)
    assert field_codes(response) == [(field, "missing") for field in REQUEST_FIELDS]


@pytest.mark.parametrize("customer_id", [999, MAX_ID], ids=["999", "largest-id"])
def test_simulation_for_a_customer_that_does_not_exist_returns_404_and_stores_nothing(
    client: TestClient, database: Database, customer_id: int
) -> None:
    """SPEC-03/E-08: 404 `customer_not_found`, without `errors` (5.2, CA-04)."""
    response = client.post("/simulations", json=simulation_with({"customer_id": customer_id}))
    body = assert_problem(response, 404, "customer_not_found")
    assert "errors" not in body
    assert row_counts(database) == NOTHING_STORED


def test_simulation_for_a_country_without_tax_rate_returns_500_and_stores_nothing(
    client: TestClient, database: Database, caplog: pytest.LogCaptureFixture
) -> None:
    """SPEC-03/E-10: `tax_rate_not_defined`, nothing internal and no simulation (CA-05)."""
    with caplog.at_level(logging.ERROR):
        response = client.post("/simulations", json=simulation_with({"customer_id": 3}))
    assert_problem(response, 500, "tax_rate_not_defined")
    for leak in ("Traceback", "TaxRateNotDefinedError", "countries", ".py", "total_cents"):
        assert leak not in response.text
    assert row_counts(database) == NOTHING_STORED
    assert caplog.records


def test_simulation_that_fails_while_being_stored_returns_500_and_stores_nothing(
    client: TestClient,
    database: Database,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """SPEC-03/E-11, SPEC-03/E-29: the database rejects the second tier; no row is left."""

    def quote_with_a_wrong_second_tier(active_users: int, country: str) -> Quote:
        return with_wrong_subtotal(calculate_quote(active_users, country), position=2)

    monkeypatch.setattr("app.services.pricing.calculate_quote", quote_with_a_wrong_second_tier)
    with caplog.at_level(logging.ERROR):
        response = client.post("/simulations", json=VALID_SIMULATION)
    assert_problem(response, 500, "internal_error")
    for leak in ("Traceback", "IntegrityError", "CHECK", "simulation_tiers", ".py"):
        assert leak not in response.text
    assert row_counts(database) == NOTHING_STORED
    assert caplog.records


def test_valid_simulation_without_database_returns_503_and_creates_nothing(
    client: TestClient, tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """SPEC-03/E-29: the row of 5.7 of an endpoint that cannot reach the database (CA-17)."""
    path = tmp_path / "data" / "simulations.db"
    path.rename(tmp_path / "moved-away.db")
    with caplog.at_level(logging.ERROR):
        response = client.post("/simulations", json=VALID_SIMULATION)
    assert_problem(response, 503, "service_unavailable")
    for leak in ("Traceback", "sqlite", "OperationalError", ".py", tmp_path.name):
        assert leak not in response.text
    assert not path.exists()
    assert caplog.records


def test_openapi_declares_the_contract_of_the_simulation(client: TestClient) -> None:
    """SPEC-03/E-01, SPEC-03/E-07, SPEC-03/E-08: fields, types and statuses of 4.1 (CA-14)."""
    document = client.get("/openapi.json").json()
    schemas = document["components"]["schemas"]
    operation = document["paths"].get("/simulations", {}).get("post", {})
    responses = operation.get("responses", {})
    assert sorted(responses) == ["201", "404", "422", "500", "503"]
    for status in ("404", "422", "500", "503"):
        assert list(responses[status]["content"]) == [PROBLEM_JSON]
    reference = operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
    request = schemas[reference.rsplit("/", maxsplit=1)[-1]]
    types = {name: field["type"] for name, field in request["properties"].items()}
    assert types == dict.fromkeys(REQUEST_FIELDS, "integer")
    assert request["required"] == REQUEST_FIELDS
    assert request["additionalProperties"] is False
    answered = responses["201"]["content"]["application/json"]["schema"]["$ref"]
    assert list(schemas[answered.rsplit("/", maxsplit=1)[-1]]["properties"]) == RESPONSE_FIELDS
