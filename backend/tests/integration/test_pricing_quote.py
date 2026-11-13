"""`POST /pricing/quote` (SPEC-02, section 4 and tables 5.4 and 5.5)."""

import logging
from collections.abc import Iterator
from contextlib import closing
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from httpx2 import Response

from app.main import create_app
from app.repositories.database import Database
from tests.integration.test_generic_errors import assert_problem

PROBLEM_JSON = "application/problem+json"
MAX_ID = 9223372036854775807
INSERT_CUSTOMER = (
    "INSERT INTO customers (id, company_name, company_name_search, tax_id, contact_email,"
    " country, plan, created_at) VALUES (:id, 'Acme', 'acme', :tax_id, 'a@acme.example',"
    " :country, 'starter', '2026-11-13T10:00:00Z')"
)
# Customer 3 has a country without tax rate: only a direct insertion can store it.
CUSTOMERS = [
    {"id": 1, "tax_id": "B12345674", "country": "ES"},
    {"id": 2, "tax_id": "DE123456789", "country": "DE"},
    {"id": 3, "tax_id": "000", "country": "US"},
]
COUNT_QUERIES = [
    "SELECT count(*) FROM customers",
    "SELECT count(*) FROM simulations",
    "SELECT count(*) FROM simulation_tiers",
]
# The response of section 4 of the spec, to the letter.
SPAIN_15_USERS = {
    "currency": "EUR",
    "active_users": 15,
    "tiers": [
        {
            "from_users": 1,
            "to_users": 10,
            "unit_price_cents": 1000,
            "users": 10,
            "subtotal_cents": 10000,
        },
        {
            "from_users": 11,
            "to_users": 50,
            "unit_price_cents": 800,
            "users": 5,
            "subtotal_cents": 4000,
        },
        {
            "from_users": 51,
            "to_users": None,
            "unit_price_cents": 500,
            "users": 0,
            "subtotal_cents": 0,
        },
    ],
    "base_cents": 14000,
    "country": "ES",
    "tax_rate_bp": 2100,
    "tax_cents": 2940,
    "total_cents": 16940,
}
ABSENT = object()
NOT_AN_INTEGER = [15.5, 15.0, "15", True, None]


@pytest.fixture
def database(tmp_path: Path) -> Database:
    return Database(tmp_path / "data" / "quote.db")


@pytest.fixture
def client(
    tmp_path: Path, database: Database, monkeypatch: pytest.MonkeyPatch
) -> Iterator[TestClient]:
    """The real application, started, with three customers inserted directly."""
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "data" / "quote.db"))
    with TestClient(create_app()) as started:
        with closing(database.connect()) as connection:
            connection.executemany(INSERT_CUSTOMER, CUSTOMERS)
            connection.commit()
        yield started


def quote(client: TestClient, customer_id: object = 1, active_users: object = 15) -> Response:
    """Post a quote; `ABSENT` leaves the field out of the body."""
    fields = {"customer_id": customer_id, "active_users": active_users}
    body = {name: value for name, value in fields.items() if value is not ABSENT}
    return client.post("/pricing/quote", json=body)


def field_codes(response: Response) -> list[tuple[str, str]]:
    errors = assert_problem(response, 422, "validation_error")["errors"]
    assert isinstance(errors, list)
    return [(error["field"], error["code"]) for error in errors]


def row_counts(database: Database) -> list[int]:
    with closing(database.connect()) as connection:
        return [connection.execute(query).fetchone()[0] for query in COUNT_QUERIES]


def test_quote_for_a_spanish_customer_with_15_users_is_the_example_of_the_spec(
    client: TestClient,
) -> None:
    """SPEC-02/E-11, SPEC-02/E-06, SPEC-02/E-07: exactly the response of section 4 (CA-05)."""
    response = quote(client)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == SPAIN_15_USERS


def test_quote_takes_the_tax_rate_from_the_country_of_the_stored_customer(
    client: TestClient,
) -> None:
    """SPEC-02/E-07: a German customer pays the German rate; the request carries no rate."""
    response = quote(client, customer_id=2)
    assert response.status_code == 200
    body = response.json()
    assert (body["country"], body["tax_rate_bp"]) == ("DE", 1900)
    assert (body["base_cents"], body["tax_cents"], body["total_cents"]) == (14000, 2660, 16660)


@pytest.mark.parametrize(
    ("active_users", "total"), [(0, 0), (100_000, 60520570)], ids=["minimum", "maximum"]
)
def test_quote_accepts_the_limits_of_active_users(
    client: TestClient, active_users: int, total: int
) -> None:
    """SPEC-02/E-02, SPEC-02/E-11: 0 and 100000 users are valid, with the totals of 5.1."""
    response = quote(client, active_users=active_users)
    assert response.status_code == 200
    assert response.json()["total_cents"] == total
    assert len(response.json()["tiers"]) == 3


def test_quotes_do_not_create_or_modify_any_stored_data(
    client: TestClient, database: Database
) -> None:
    """SPEC-02/E-12: after several quotes, valid or not, every table has the same rows (CA-06)."""
    before = row_counts(database)
    requests = [(1, 15), (2, 51), (1, 100_000), (999, 15), (1, -1)]
    statuses = [quote(client, *request).status_code for request in requests]
    # The quotes were really calculated: an endpoint that answers nothing writes nothing.
    assert statuses == [200, 200, 200, 404, 422]
    assert before == [3, 0, 0]
    assert row_counts(database) == before


@pytest.mark.parametrize(
    ("active_users", "code"),
    [(-1, "out_of_range"), (100_001, "out_of_range")]
    + [(value, "not_an_integer") for value in NOT_AN_INTEGER]
    + [(ABSENT, "missing")],
    ids=["-1", "100001", "15.5", "15.0", "'15'", "true", "null", "absent"],
)
def test_quote_with_invalid_active_users_returns_422(
    client: TestClient, active_users: object, code: str
) -> None:
    """SPEC-02/E-09, SPEC-02/E-14: every row of 5.4 about the value of `active_users` (CA-07)."""
    assert field_codes(quote(client, active_users=active_users)) == [("active_users", code)]


def test_quote_with_an_additional_field_returns_422_unknown_field(client: TestClient) -> None:
    """SPEC-02/E-07, SPEC-02/E-14: the request cannot bring the rate; last row of 5.4 (CA-07)."""
    body = {"customer_id": 1, "active_users": 15, "tax_rate_bp": 0}
    response = client.post("/pricing/quote", json=body)
    assert field_codes(response) == [("tax_rate_bp", "unknown_field")]


@pytest.mark.parametrize("customer_id", [999, MAX_ID], ids=["999", "largest-id"])
def test_quote_for_a_customer_that_does_not_exist_returns_404(
    client: TestClient, customer_id: int
) -> None:
    """SPEC-02/E-13: 404 `customer_not_found`, without `errors` (5.5, CA-07)."""
    body = assert_problem(quote(client, customer_id=customer_id), 404, "customer_not_found")
    assert "errors" not in body


@pytest.mark.parametrize(
    ("customer_id", "code"),
    [(0, "out_of_range"), (-1, "out_of_range"), (MAX_ID + 1, "out_of_range")]
    + [(value, "not_an_integer") for value in (1.0, "1", True, None)]
    + [(ABSENT, "missing")],
    ids=["0", "-1", "2^63", "1.0", "'1'", "true", "null", "absent"],
)
def test_quote_with_invalid_customer_id_returns_422(
    client: TestClient, customer_id: object, code: str
) -> None:
    """SPEC-02/E-15, SPEC-02/E-14: every invalid row of 5.5 (CA-07)."""
    assert field_codes(quote(client, customer_id=customer_id)) == [("customer_id", code)]


def test_validation_wins_over_a_customer_that_does_not_exist(client: TestClient) -> None:
    """SPEC-02/E-14: customer 999 and -1 users answer 422, not 404 (last row of 5.5)."""
    assert field_codes(quote(client, 999, -1)) == [("active_users", "out_of_range")]


def test_invalid_request_is_rejected_without_reading_the_database(
    client: TestClient, database: Database, tmp_path: Path
) -> None:
    """SPEC-02/E-15: with the database file moved away, an invalid id still answers 422."""
    (tmp_path / "data" / "quote.db").rename(tmp_path / "moved-away.db")
    assert field_codes(quote(client, customer_id=0)) == [("customer_id", "out_of_range")]


def test_valid_quote_without_database_returns_503_and_creates_nothing(
    client: TestClient, tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """SPEC-03/E-29: an endpoint that cannot read the database answers 503, like `/health`."""
    path = tmp_path / "data" / "quote.db"
    path.rename(tmp_path / "moved-away.db")
    with caplog.at_level(logging.ERROR):
        response = quote(client)
    assert_problem(response, 503, "service_unavailable")
    for leak in ("Traceback", "sqlite", "OperationalError", ".py", tmp_path.name):
        assert leak not in response.text
    assert not path.exists()
    assert caplog.records


@pytest.mark.parametrize("content", [None, b"{}"], ids=["absent-body", "empty-object"])
def test_quote_without_fields_returns_422_with_both_missing(
    client: TestClient, content: bytes | None
) -> None:
    """SPEC-02/E-14: no 422 leaves in the format of the framework, not even without a body."""
    headers = {"content-type": "application/json"} if content else {}
    response = client.post("/pricing/quote", content=content, headers=headers)
    assert field_codes(response) == [("customer_id", "missing"), ("active_users", "missing")]


def test_quote_for_a_country_without_tax_rate_returns_500_tax_rate_not_defined(
    client: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    """SPEC-02/E-10: an internal failure, never a rate of 0 %, and nothing internal (CA-11)."""
    with caplog.at_level(logging.ERROR):
        response = quote(client, customer_id=3)
    assert_problem(response, 500, "tax_rate_not_defined")
    for leak in ("Traceback", "TaxRateNotDefinedError", "countries", ".py", "total_cents"):
        assert leak not in response.text
    assert caplog.records


def test_openapi_declares_the_contract_of_the_quote(client: TestClient) -> None:
    """SPEC-02/E-11, SPEC-02/E-13, SPEC-02/E-14: fields, types and statuses of section 4 (CA-10)."""
    document = client.get("/openapi.json").json()
    schemas = document["components"]["schemas"]
    operation = document["paths"].get("/pricing/quote", {}).get("post", {})
    responses = operation.get("responses", {})
    assert sorted(responses) == ["200", "404", "422", "500", "503"]
    for status in ("404", "422", "500", "503"):
        assert list(responses[status]["content"]) == [PROBLEM_JSON]
    reference = operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
    request = schemas[reference.rsplit("/", maxsplit=1)[-1]]
    assert {name: field["type"] for name, field in request["properties"].items()} == {
        "customer_id": "integer",
        "active_users": "integer",
    }
    assert request["required"] == ["customer_id", "active_users"]
    assert request["additionalProperties"] is False
    answered = responses["200"]["content"]["application/json"]["schema"]["$ref"]
    assert list(schemas[answered.rsplit("/", maxsplit=1)[-1]]["properties"]) == list(SPAIN_15_USERS)
    assert "HTTPValidationError" not in schemas
