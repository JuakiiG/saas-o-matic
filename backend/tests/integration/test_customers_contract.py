"""`GET /meta` and the published contract of `POST /customers` (SPEC-01: 4.1, 4.4; ADR-009)."""

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.domain.countries import COUNTRIES
from app.domain.customers import (
    COUNTRY_CODES,
    CUSTOMER_FIELDS,
    MAX_TAX_ID_INPUT_LENGTH,
    PLAN_CODES,
    PLANS,
    InvalidCustomerError,
    validate_new_customer,
)
from app.main import create_app
from tests.customer_cases import VALID_CUSTOMER, customer_with

PROBLEM_JSON = "application/problem+json"
# The example of 4.4, to the letter.
META = {
    "countries": [
        {"code": "ES", "name": "España", "tax_rate_bp": 2100},
        {"code": "PT", "name": "Portugal", "tax_rate_bp": 2300},
        {"code": "FR", "name": "Francia", "tax_rate_bp": 2000},
        {"code": "DE", "name": "Alemania", "tax_rate_bp": 1900},
        {"code": "IT", "name": "Italia", "tax_rate_bp": 2200},
        {"code": "NL", "name": "Países Bajos", "tax_rate_bp": 2100},
        {"code": "IE", "name": "Irlanda", "tax_rate_bp": 2300},
        {"code": "BE", "name": "Bélgica", "tax_rate_bp": 2100},
        {"code": "GB", "name": "Reino Unido", "tax_rate_bp": 2000},
    ],
    "plans": [
        {"code": "starter", "name": "Básico"},
        {"code": "professional", "name": "Profesional"},
        {"code": "enterprise", "name": "Empresa"},
    ],
}
# What the OpenAPI may say about a field: a limit only if the code applies it exactly so.
ADMITTED_KEYWORDS = {"type", "title", "maxLength", "enum"}
RESPONSE_FIELDS = ["id", *CUSTOMER_FIELDS, "created_at"]


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "meta.db"))
    with TestClient(create_app()) as started:
        yield started


def problems_of(received: dict[str, object]) -> list[tuple[str, str]]:
    try:
        validate_new_customer(received)
    except InvalidCustomerError as error:
        return [(field, problem.value) for field, problem in error.problems]
    return []


def published_request(client: TestClient) -> dict[str, object]:
    """The schema that the OpenAPI publishes for the body of `POST /customers`."""
    operation = client.get("/openapi.json").json()["paths"].get("/customers", {}).get("post", {})
    content = operation.get("requestBody", {}).get("content", {})
    schema: dict[str, object] = content.get("application/json", {}).get("schema", {})
    return schema


def test_meta_returns_the_countries_and_plans_of_the_domain(client: TestClient) -> None:
    """SPEC-01/E-32: the example of 4.4, taken from the constants of the domain (CA-15)."""
    response = client.get("/meta")
    assert response.status_code == 200
    assert response.json() == META
    assert [(c["code"], c["name"], c["tax_rate_bp"]) for c in response.json()["countries"]] == [
        (country.code, country.name, country.tax_rate_bp) for country in COUNTRIES
    ]
    assert [(p["code"], p["name"]) for p in response.json()["plans"]] == [
        (plan.code, plan.name) for plan in PLANS
    ]


def test_every_country_and_plan_of_meta_is_accepted_when_creating_a_customer(
    client: TestClient,
) -> None:
    """SPEC-01/E-32, SPEC-01/E-05, SPEC-01/E-06: what `/meta` offers is admitted (CA-15)."""
    answered = client.get("/meta")
    assert answered.status_code == 200
    meta = answered.json()
    for number, country in enumerate(meta["countries"]):
        plan = meta["plans"][number % 3]["code"]
        changes = {"country": country["code"], "plan": plan, "tax_id": "B12345674"}
        response = client.post("/customers", json=customer_with(changes))
        assert response.status_code == 201, country
        assert (response.json()["country"], response.json()["plan"]) == (country["code"], plan)


def test_openapi_publishes_the_fields_that_the_domain_validates(client: TestClient) -> None:
    """SPEC-01/E-01, SPEC-01/E-07: fields, order, required and type, as validated (CA-16).

    ADR-009, condition 1: the model that documents and the function that validates
    cannot drift apart.
    """
    schema = published_request(client)
    properties = schema.get("properties", {})
    assert isinstance(properties, dict)
    assert list(properties) == list(CUSTOMER_FIELDS)
    assert schema.get("required") == list(CUSTOMER_FIELDS)
    assert schema.get("additionalProperties") is False
    for field in CUSTOMER_FIELDS:
        assert properties[field]["type"] == "string", field
        # Required and of that type in the published contract: so it is for the domain.
        assert problems_of(customer_with({field: 7})) == [(field, "not_a_string")]
        without = {name: value for name, value in VALID_CUSTOMER.items() if name != field}
        assert problems_of(without) == [(field, "missing")]
    assert problems_of(customer_with({"extra": 1})) == [("extra", "unknown_field")]


def test_openapi_publishes_no_limit_that_the_code_does_not_apply_exactly(
    client: TestClient,
) -> None:
    """SPEC-01/E-34, SPEC-01/E-05, SPEC-01/E-06: only limits of the value received (CA-16).

    ADR-009, condition 2: the lengths of the name and of the email are measured after
    trimming, so they are not published as limits of what is received.
    """
    properties = published_request(client).get("properties", {})
    assert isinstance(properties, dict)
    assert list(properties) == list(CUSTOMER_FIELDS)
    for field, published in properties.items():
        assert set(published) <= ADMITTED_KEYWORDS, field
    assert set(properties["company_name"]) <= {"type", "title"}
    assert set(properties["contact_email"]) <= {"type", "title"}
    assert properties["tax_id"]["maxLength"] == MAX_TAX_ID_INPUT_LENGTH
    assert properties["country"]["enum"] == list(COUNTRY_CODES)
    assert properties["plan"]["enum"] == list(PLAN_CODES)
    # The published limit of the identifier is the one the domain applies to what it receives.
    at_limit = "12345678Z" + " " * (MAX_TAX_ID_INPUT_LENGTH - 9)
    assert problems_of(customer_with({"tax_id": at_limit})) == []
    assert problems_of(customer_with({"tax_id": at_limit + " "})) == [("tax_id", "too_long")]


def test_openapi_declares_the_statuses_and_the_response_of_the_creation(
    client: TestClient,
) -> None:
    """SPEC-01/E-01, SPEC-01/E-32: statuses and fields of 4.1 and 4.4 (CA-16)."""
    document = client.get("/openapi.json").json()
    schemas = document["components"]["schemas"]
    creation = document["paths"].get("/customers", {}).get("post", {}).get("responses", {})
    assert sorted(creation) == ["201", "409", "422", "503"]
    for status in ("409", "422", "503"):
        assert list(creation[status]["content"]) == [PROBLEM_JSON]
    created = creation["201"]["content"]["application/json"]["schema"]["$ref"]
    assert list(schemas[created.rsplit("/", maxsplit=1)[-1]]["properties"]) == RESPONSE_FIELDS
    meta = document["paths"].get("/meta", {}).get("get", {}).get("responses", {})
    assert sorted(meta) == ["200"]
    answered = meta["200"]["content"]["application/json"]["schema"]["$ref"]
    assert list(schemas[answered.rsplit("/", maxsplit=1)[-1]]["properties"]) == list(META)
    assert "HTTPValidationError" not in schemas
