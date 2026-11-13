"""`GET /customers/{id}` and `GET /customers?q=` (SPEC-01: 4.2, 4.3 and tables 5.9 and 5.10)."""

import logging
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from httpx2 import Response

from app.main import create_app
from tests.customer_cases import customer_with
from tests.integration.test_generic_errors import assert_problem

PROBLEM_JSON = "application/problem+json"
MAX_ID = 9223372036854775807
# The customers of 5.9, in the order of their `id`: name, identifier and country.
SEARCH_CUSTOMERS = [
    ("Zeta Datos SL", "B12345674", "ES"),
    ("alfa Ejemplo SA", "A24680241", "ES"),
    ("Alfa Ejemplo SA", "AB1234", "FR"),
    ("Ñandú Pruebas SL", "B99999997", "ES"),
    ("100% Ejemplo SL", "E99999997", "ES"),
    ("Ejemplo_Uno SL", "H00000000", "ES"),
    ("José Pruebas SL", "P1234567D", "ES"),
]
EVERY_CUSTOMER = [5, 2, 3, 6, 7, 4, 1]
# Table 5.9: the text searched and the `id` returned, in order.
SEARCH_ROWS = [
    ("alfa", [2, 3]),
    ("EJEMPLO", [5, 2, 3, 6]),
    ("ñandú", [4]),
    ("nandu", [4]),
    ("jose", [7]),
    ("JOSÉ", [7]),
    ("b-12345", [1]),
    ("b.1234", [3, 1]),
    ("9999999", [5, 4]),
    ("%", [5]),
    ("_", [6]),
    ("\\", []),
    ("' OR 1=1 --", []),
    ("noexiste", []),
    ("", EVERY_CUSTOMER),
    ("   ", EVERY_CUSTOMER),
    # Not a row of the table: 100 characters is the limit, and it is valid.
    ("x" * 100, []),
]
ITEM_FIELDS = ["id", "company_name", "tax_id", "country", "plan"]
CUSTOMER_FIELDS = ["id", "company_name", "tax_id", "contact_email", "country", "plan", "created_at"]


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    """The real application, started, with an empty database."""
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "data" / "read.db"))
    with TestClient(create_app()) as started:
        yield started


@pytest.fixture
def searchable(client: TestClient) -> TestClient:
    """The application with the seven customers of 5.9, created through the API."""
    for name, tax_id, country in SEARCH_CUSTOMERS:
        changes = {"company_name": name, "tax_id": tax_id, "country": country}
        assert client.post("/customers", json=customer_with(changes)).status_code == 201
    return client


def field_codes(response: Response) -> list[tuple[str, str]]:
    errors = assert_problem(response, 422, "validation_error")["errors"]
    assert isinstance(errors, list)
    return [(error["field"], error["code"]) for error in errors]


def found_ids(response: Response) -> list[int]:
    assert response.status_code == 200
    assert list(response.json()) == ["items"]
    return [item["id"] for item in response.json()["items"]]


def test_customer_is_read_with_the_seven_fields_that_its_creation_answered(
    client: TestClient,
) -> None:
    """SPEC-01/E-22, SPEC-01/E-01, SPEC-01/E-08: the example of 4.1, read back (CA-06)."""
    changes: dict[str, object] = {"company_name": "  Ejemplo Uno SL ", "tax_id": "b-1234567 4"}
    created = client.post("/customers", json=customer_with(changes))
    assert created.status_code == 201
    response = client.get(created.headers["location"])
    assert response.status_code == 200
    body = response.json()
    assert {field: body.get(field) for field in CUSTOMER_FIELDS} == created.json()
    assert body["tax_id"] == "B12345674"


@pytest.mark.parametrize("customer_id", [999, MAX_ID], ids=["999", "largest-id"])
def test_customer_that_does_not_exist_returns_404(client: TestClient, customer_id: int) -> None:
    """SPEC-01/E-23: 404 `customer_not_found`, without `errors` (5.10, CA-12)."""
    assert client.post("/customers", json=customer_with({})).status_code == 201
    body = assert_problem(client.get(f"/customers/{customer_id}"), 404, "customer_not_found")
    assert "errors" not in body


@pytest.mark.parametrize(
    ("customer_id", "code"),
    [
        ("0", "out_of_range"),
        ("-1", "out_of_range"),
        (str(MAX_ID + 1), "out_of_range"),
        ("abc", "not_an_integer"),
        ("1.5", "not_an_integer"),
        # The only form of an integer in the route: the customer 1 exists, and only `1` reads it.
        ("1.0", "not_an_integer"),
        ("+1", "not_an_integer"),
        ("01", "not_an_integer"),
        ("1_0", "not_an_integer"),
        ("%201", "not_an_integer"),
        ("1%20", "not_an_integer"),
        # Not rows of the table: other writings that the rule leaves out.
        ("-0", "not_an_integer"),
        ("00", "not_an_integer"),
        ("-01", "not_an_integer"),
        ("1%0A", "not_an_integer"),
        ("%D9%A1", "not_an_integer"),
    ],
)
def test_customer_with_an_invalid_id_returns_422_in_the_field_id(
    client: TestClient, customer_id: str, code: str
) -> None:
    """SPEC-01/E-24: the error is of the field `id`, whatever the route calls it (5.10, CA-12)."""
    assert client.post("/customers", json=customer_with({})).status_code == 201
    assert field_codes(client.get(f"/customers/{customer_id}")) == [("id", code)]


@pytest.mark.parametrize(("text", "expected"), SEARCH_ROWS, ids=ascii)
def test_search_returns_the_customers_of_the_table_in_its_order(
    searchable: TestClient, text: str, expected: list[int]
) -> None:
    """SPEC-01/E-25, SPEC-01/E-26, SPEC-01/E-27, SPEC-01/E-29, SPEC-01/E-31: rows of 5.9 (CA-13)."""
    assert found_ids(searchable.get("/customers", params={"q": text})) == expected


def test_search_without_text_returns_the_first_customers_by_name(searchable: TestClient) -> None:
    """SPEC-01/E-29: `q` absent is the initial list; `Ñandú` sorts as `nandu` (5.9, CA-13)."""
    assert found_ids(searchable.get("/customers")) == EVERY_CUSTOMER


def test_search_returns_five_fields_of_each_customer(searchable: TestClient) -> None:
    """SPEC-01/E-25: the items of 4.3, without email or date."""
    response = searchable.get("/customers", params={"q": "zeta"})
    assert response.status_code == 200
    items = response.json()["items"]
    assert items == [
        {
            "id": 1,
            "company_name": "Zeta Datos SL",
            "tax_id": "B12345674",
            "country": "ES",
            "plan": "professional",
        }
    ]
    assert list(items[0]) == ITEM_FIELDS


def test_search_returns_at_most_the_first_20_customers_by_name(client: TestClient) -> None:
    """SPEC-01/E-26: 25 customers with `Ejemplo` in the name, the first 20 by name (CA-13)."""
    # Created from the last name to the first, so that the order by name is not the order of id.
    for number in range(25, 0, -1):
        changes = {
            "company_name": f"Ejemplo {number:02d} SL",
            "tax_id": f"EJ{number:04d}",
            "country": "FR",
        }
        assert client.post("/customers", json=customer_with(changes)).status_code == 201
    assert found_ids(client.get("/customers", params={"q": "ejemplo"})) == list(range(25, 5, -1))


@pytest.mark.parametrize("text", ["x" * 101, "x" * 100 + " "], ids=["101", "100-and-a-space"])
def test_search_text_over_100_characters_returns_422_too_long(
    searchable: TestClient, text: str
) -> None:
    """SPEC-01/E-30: the limit is measured before trimming, in the field `q` (5.9, CA-13)."""
    assert field_codes(searchable.get("/customers", params={"q": text})) == [("q", "too_long")]


def test_search_with_an_undocumented_parameter_returns_422(searchable: TestClient) -> None:
    """SPEC-01/E-30: `limit` is not a parameter of the contract (5.9, CA-13)."""
    response = searchable.get("/customers", params={"q": "alfa", "limit": "5"})
    assert field_codes(response) == [("limit", "unknown_field")]


@pytest.mark.parametrize("path", ["/customers/1", "/customers?q=alfa"])
def test_reading_customers_without_database_returns_503(
    client: TestClient, tmp_path: Path, path: str, caplog: pytest.LogCaptureFixture
) -> None:
    """SPEC-03/E-29: an endpoint that cannot read the database answers 503."""
    (tmp_path / "data" / "read.db").rename(tmp_path / "moved-away.db")
    with caplog.at_level(logging.ERROR):
        response = client.get(path)
    assert_problem(response, 503, "service_unavailable")
    assert not (tmp_path / "data" / "read.db").exists()


def test_openapi_declares_the_contract_of_reading_customers(client: TestClient) -> None:
    """SPEC-01/E-22, SPEC-01/E-25: parameters, statuses and fields of 4.2 and 4.3 (CA-16)."""
    document = client.get("/openapi.json").json()
    schemas = document["components"]["schemas"]
    one = document["paths"].get("/customers/{id}", {}).get("get", {})
    assert sorted(one.get("responses", {})) == ["200", "404", "422", "503"]
    assert [(p["name"], p["in"], p["schema"]["type"]) for p in one["parameters"]] == [
        ("id", "path", "integer")
    ]
    limits = one["parameters"][0]["schema"]
    assert (limits.get("minimum"), limits.get("maximum")) == (1, MAX_ID)
    answered = one["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
    # The profile adds the history of simulations to the fields of the creation (SPEC-03, 4.2).
    profile_fields = [*CUSTOMER_FIELDS, "simulation_count", "simulations"]
    assert list(schemas[answered.rsplit("/", maxsplit=1)[-1]]["properties"]) == profile_fields
    search = document["paths"].get("/customers", {}).get("get", {})
    assert sorted(search.get("responses", {})) == ["200", "422", "503"]
    (parameter,) = search["parameters"]
    assert (parameter["name"], parameter["in"], parameter["required"]) == ("q", "query", False)
    problems = (("404", one), ("422", one), ("503", one), ("422", search), ("503", search))
    for status, operation in problems:
        assert list(operation["responses"][status]["content"]) == [PROBLEM_JSON]
