"""The rows of SPEC-03 that name real endpoints: CORS (5.6), generic errors (5.7) and
immutability (4.3).

`test_generic_errors.py` and `test_cors.py` prove the same machinery with probe routes,
written before the business endpoints existed. Here each row runs against the endpoint
that it names.
"""

import json
import logging
from collections.abc import Iterator
from contextlib import closing
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.repositories.customers import CustomerRepository
from app.repositories.database import Database
from tests.integration.test_cors import (
    ALLOW_ORIGIN,
    OTHER,
    PREFLIGHT,
    REJECTED_PREFLIGHT_HEADERS,
)
from tests.integration.test_generic_errors import assert_problem
from tests.integration.test_pricing_quote import CUSTOMERS, INSERT_CUSTOMER, field_codes
from tests.simulation_cases import VALID_SIMULATION

JSON = {"content-type": "application/json"}
TEXT = {"content-type": "text/plain"}
FRONTEND = "http://localhost:4200"
CUT_SIMULATION = b'{"customer_id":'
VALID_QUOTE = json.dumps({"customer_id": 1, "active_users": 15}).encode()
INTERNAL_DETAIL = "detail that must stay inside the server"
# A simulation stored directly, so that there is something that could change.
INSERT_SIMULATION = (
    "INSERT INTO simulations (id, customer_id, active_users, storage_gb, estimated_api_calls,"
    " country, base_cents, tax_rate_bp, tax_cents, total_cents, created_at)"
    " VALUES (1, 1, 1, 0, 0, 'ES', 1000, 2100, 210, 1210, '2026-11-13T15:00:00Z')"
)
INSERT_TIER = "INSERT INTO simulation_tiers VALUES (1, 1, 1, 10, 1000, 1, 1000)"
EVERY_ROW = [
    "SELECT * FROM customers ORDER BY id",
    "SELECT * FROM simulations ORDER BY id",
    "SELECT * FROM simulation_tiers ORDER BY simulation_id, position",
]
# Table 5.7: method, path, headers, body, and the status and code that it answers.
GENERIC_ROWS = [
    ("POST", "/customers", JSON, b'{"company_name":', 400, "malformed_request"),
    ("POST", "/simulations", JSON, b"[1, 2]", 400, "malformed_request"),
    ("POST", "/simulations", JSON, b"null", 400, "malformed_request"),
    ("POST", "/simulations", JSON, b"15", 400, "malformed_request"),
    ("POST", "/pricing/quote", TEXT, VALID_QUOTE, 415, "unsupported_media_type"),
    ("POST", "/simulations?debug=1", TEXT, CUT_SIMULATION, 415, "unsupported_media_type"),
    ("POST", "/simulations?debug=1", JSON, CUT_SIMULATION, 400, "malformed_request"),
    ("GET", "/clientes", {}, None, 404, "not_found"),
    ("GET", "/customers/1/extra", {}, None, 404, "not_found"),
    ("GET", "/simulations", {}, None, 405, "method_not_allowed"),
    ("POST", "/customers/1", {}, None, 405, "method_not_allowed"),
    ("DELETE", "/meta", {}, None, 405, "method_not_allowed"),
    ("OPTIONS", "/customers", {}, None, 405, "method_not_allowed"),
    ("OPTIONS", "/customers", {"origin": FRONTEND}, None, 405, "method_not_allowed"),
]
TWO_ORIGINS = "http://a.example,http://b.example"
# The four rows of `GET /meta` of 5.6: `CORS_ORIGINS` (None is undefined), the origin of the
# request and the origin that the response admits (None is no header).
META_ROWS = [
    (None, FRONTEND, FRONTEND),
    (None, OTHER, None),
    (TWO_ORIGINS, FRONTEND, None),
    (TWO_ORIGINS, "http://b.example", "http://b.example"),
]
# 4.3: what would modify or delete, on the three routes, and the reading that does not exist.
FORBIDDEN_OPERATIONS = [
    (method, path)
    for path in ("/customers", "/customers/1", "/simulations")
    for method in ("PUT", "PATCH", "DELETE")
] + [("GET", "/simulations")]


@pytest.fixture
def database(tmp_path: Path) -> Database:
    return Database(tmp_path / "data" / "real.db")


@pytest.fixture
def client(
    tmp_path: Path, database: Database, monkeypatch: pytest.MonkeyPatch
) -> Iterator[TestClient]:
    """The real application, started, with three customers and one simulation."""
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "data" / "real.db"))
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    with TestClient(create_app()) as started:
        with closing(database.connect()) as connection:
            connection.executemany(INSERT_CUSTOMER, CUSTOMERS)
            connection.execute(INSERT_SIMULATION)
            connection.execute(INSERT_TIER)
            connection.commit()
        yield started


def stored_rows(database: Database) -> list[list[tuple[object, ...]]]:
    """Every row of the three tables, to see that nothing changed."""
    with closing(database.connect()) as connection:
        return [connection.execute(query).fetchall() for query in EVERY_ROW]


@pytest.mark.parametrize(
    "row",
    GENERIC_ROWS,
    ids=[f"{row[0]} {row[1]} {row[4]} {index}" for index, row in enumerate(GENERIC_ROWS)],
)
def test_generic_error_of_a_real_endpoint_has_the_status_and_the_code_of_the_table(
    client: TestClient, row: tuple[str, str, dict[str, str], bytes | None, int, str]
) -> None:
    """SPEC-03/E-29, SPEC-03/E-33: every row of 5.7 that answers an error (CA-17)."""
    method, path, headers, content, status, code = row
    response = client.request(method, path, headers=headers, content=content)
    assert_problem(response, status, code)


def test_json_content_type_with_parameters_is_accepted_by_the_quote(client: TestClient) -> None:
    """SPEC-03/E-29: `application/json; charset=utf-8` and a valid body answer 200 (5.7)."""
    headers = {"content-type": "application/json; charset=utf-8"}
    response = client.post("/pricing/quote", content=VALID_QUOTE, headers=headers)
    assert response.status_code == 200
    assert response.json()["total_cents"] == 16940


def test_valid_simulation_with_an_undocumented_parameter_returns_422_and_stores_nothing(
    client: TestClient, database: Database
) -> None:
    """SPEC-03/E-29, SPEC-03/E-06: `unknown_field` in the field `debug` (5.7, CA-17)."""
    before = stored_rows(database)
    response = client.post("/simulations?debug=1", json=VALID_SIMULATION)
    assert field_codes(response) == [("debug", "unknown_field")]
    assert stored_rows(database) == before


def test_unexpected_failure_of_a_repository_returns_500_that_the_frontend_can_read(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """SPEC-03/E-29, SPEC-03/E-24: `internal_error`, nothing internal, CORS header (5.6, 5.7)."""

    def fail(self: CustomerRepository, customer_id: int) -> str | None:
        raise RuntimeError(INTERNAL_DETAIL)

    monkeypatch.setattr(CustomerRepository, "country_of", fail)
    with caplog.at_level(logging.ERROR):
        response = client.post("/simulations", json=VALID_SIMULATION, headers={"Origin": FRONTEND})
    assert_problem(response, 500, "internal_error")
    for leak in (INTERNAL_DETAIL, "Traceback", "RuntimeError", ".py"):
        assert leak not in response.text
    assert response.headers.get("access-control-allow-origin") == FRONTEND
    assert caplog.records


@pytest.mark.parametrize(("configured", "origin", "allowed"), META_ROWS)
def test_meta_answers_with_the_origin_only_to_an_admitted_one(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    configured: str | None,
    origin: str,
    allowed: str | None,
) -> None:
    """SPEC-03/E-24, SPEC-03/E-25, SPEC-03/E-26: the four rows of `GET /meta` of 5.6 (CA-15)."""
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "data" / "cors.db"))
    if configured is None:
        monkeypatch.delenv("CORS_ORIGINS", raising=False)
    else:
        monkeypatch.setenv("CORS_ORIGINS", configured)
    with TestClient(create_app()) as started:
        response = started.get("/meta", headers={"Origin": origin})
    assert response.status_code == 200
    assert [country["code"] for country in response.json()["countries"]][:2] == ["ES", "PT"]
    # The requesting origin or no header at all: never `*`.
    assert response.headers.get(ALLOW_ORIGIN) == allowed


def test_preflight_of_the_customers_from_the_frontend_returns_200_with_cors_headers(
    client: TestClient, database: Database
) -> None:
    """SPEC-03/E-30: the admitted preflight of `OPTIONS /customers` of 5.6, not a 405 (CA-15)."""
    before = stored_rows(database)
    response = client.options("/customers", headers={"Origin": FRONTEND, **PREFLIGHT})
    assert response.status_code == 200
    assert response.headers.get(ALLOW_ORIGIN) == FRONTEND
    assert "POST" in response.headers["access-control-allow-methods"]
    assert "content-type" in response.headers["access-control-allow-headers"].lower()
    assert stored_rows(database) == before


@pytest.mark.parametrize(
    ("changes", "expected"),
    [
        ({"Origin": OTHER}, REJECTED_PREFLIGHT_HEADERS),
        (
            {"Access-Control-Request-Method": "DELETE"},
            {**REJECTED_PREFLIGHT_HEADERS, ALLOW_ORIGIN: FRONTEND},
        ),
    ],
    ids=["unlisted-origin", "unlisted-method"],
)
def test_rejected_preflight_of_the_customers_gets_the_standard_rejection(
    client: TestClient, changes: dict[str, str], expected: dict[str, str]
) -> None:
    """SPEC-03/E-31: the two rejected preflights of 5.6, status and every header (CA-15)."""
    headers = {"Origin": FRONTEND, **PREFLIGHT, **changes}
    response = client.options("/customers", headers=headers)
    assert response.status_code == 400
    assert dict(response.headers) == expected
    assert response.headers["content-type"] != "application/problem+json"


@pytest.mark.parametrize(("method", "path"), FORBIDDEN_OPERATIONS)
def test_no_operation_modifies_or_deletes_a_customer_or_a_simulation(
    client: TestClient, database: Database, method: str, path: str
) -> None:
    """SPEC-03/E-18: 405 `method_not_allowed` and the stored data do not change (CA-09)."""
    before = stored_rows(database)
    body = None if method in ("GET", "DELETE") else VALID_SIMULATION
    response = client.request(method, path, json=body)
    assert_problem(response, 405, "method_not_allowed")
    assert stored_rows(database) == before
    assert [len(rows) for rows in before] == [3, 1, 1]
