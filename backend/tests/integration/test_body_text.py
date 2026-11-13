"""The text of a request body (index of specs, "El texto del cuerpo"; SPEC-03/E-29).

Against the three real endpoints that take a body: the guard runs before any of them.
"""

import json
from collections.abc import Iterator
from contextlib import closing
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.repositories.database import Database
from tests.customer_cases import VALID_CUSTOMER
from tests.integration.test_generic_errors import assert_problem
from tests.integration.test_pricing_quote import COUNT_QUERIES, CUSTOMERS, INSERT_CUSTOMER
from tests.simulation_cases import VALID_SIMULATION

JSON = {"content-type": "application/json"}
# Half of a pair: `json.dumps` writes it as the escape `\ud800`, six ASCII characters.
LONE_SURROGATE = "\ud800"
# U+1F600 written as a well-formed pair of escapes, and as the character itself.
EMOJI_AS_ESCAPES = '"Ejemplo \\ud83d\\ude00 SL"'
EMOJI = "Ejemplo \U0001f600 SL"
NEW_CUSTOMER: dict[str, object] = {**VALID_CUSTOMER, "tax_id": "A24680241"}
VALID_QUOTE: dict[str, object] = {"customer_id": 1, "active_users": 15}
# Path and body: a lone surrogate in a value and in a field name, in the three POST.
LONE_SURROGATE_ROWS: list[tuple[str, dict[str, object]]] = [
    ("/customers", {**NEW_CUSTOMER, "company_name": f"Ab{LONE_SURROGATE}c"}),
    ("/customers", {**NEW_CUSTOMER, "contact_email": f"a{LONE_SURROGATE}@b.example"}),
    ("/customers", {**NEW_CUSTOMER, f"x{LONE_SURROGATE}": 1}),
    ("/pricing/quote", {**VALID_QUOTE, "active_users": LONE_SURROGATE}),
    ("/pricing/quote", {**VALID_QUOTE, f"x{LONE_SURROGATE}": 1}),
    ("/simulations", {**VALID_SIMULATION, "storage_gb": LONE_SURROGATE}),
    ("/simulations", {**VALID_SIMULATION, f"x{LONE_SURROGATE}": 1}),
    # Not in the decision of the finding: the second half alone, the two halves in the
    # wrong order, and a lone one deep inside a value and inside a name.
    ("/customers", {**NEW_CUSTOMER, "company_name": "Ab\udc00c"}),
    ("/customers", {**NEW_CUSTOMER, "company_name": "Ab\udc00\ud800c"}),
    ("/simulations", {**VALID_SIMULATION, "extra": [{"deep": [LONE_SURROGATE]}]}),
    ("/simulations", {**VALID_SIMULATION, "extra": [{LONE_SURROGATE: 1}]}),
]


@pytest.fixture
def database(tmp_path: Path) -> Database:
    return Database(tmp_path / "data" / "body.db")


@pytest.fixture
def client(
    tmp_path: Path, database: Database, monkeypatch: pytest.MonkeyPatch
) -> Iterator[TestClient]:
    """The real application, started, with the three customers of the quote tests."""
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "data" / "body.db"))
    with TestClient(create_app()) as started:
        with closing(database.connect()) as connection:
            connection.executemany(INSERT_CUSTOMER, CUSTOMERS)
            connection.commit()
        yield started


def stored_counts(database: Database) -> list[int]:
    """How many customers, simulations and tiers there are."""
    with closing(database.connect()) as connection:
        return [connection.execute(query).fetchone()[0] for query in COUNT_QUERIES]


@pytest.mark.parametrize(
    ("path", "body"),
    LONE_SURROGATE_ROWS,
    ids=[f"{path} {index}" for index, (path, _) in enumerate(LONE_SURROGATE_ROWS)],
)
def test_body_with_a_lone_surrogate_returns_400_and_stores_nothing(
    client: TestClient, database: Database, path: str, body: dict[str, object]
) -> None:
    """SPEC-03/E-29: in a value or in a field name, `malformed_request` and never a 500."""
    content = json.dumps(body).encode()
    assert b"\\ud" in content
    response = client.post(path, content=content, headers=JSON)
    assert_problem(response, 400, "malformed_request")
    assert stored_counts(database) == [3, 0, 0]


@pytest.mark.parametrize(
    "written", [EMOJI_AS_ESCAPES, json.dumps(EMOJI, ensure_ascii=False)], ids=["escapes", "utf-8"]
)
def test_customer_with_an_emoji_in_its_name_is_still_created(
    client: TestClient, written: str
) -> None:
    """SPEC-03/E-29, SPEC-01/E-01: a well-formed pair is valid text, however it is written."""
    content = json.dumps(NEW_CUSTOMER).replace('"Ejemplo Uno SL"', written).encode()
    response = client.post("/customers", content=content, headers=JSON)
    assert response.status_code == 201
    assert response.json()["company_name"] == EMOJI
    assert client.get(response.headers["location"]).json()["company_name"] == EMOJI


@pytest.mark.parametrize("path", ["/pricing/quote", "/simulations"])
def test_field_name_with_an_emoji_is_an_unknown_field_and_not_a_malformed_body(
    client: TestClient, path: str
) -> None:
    """SPEC-03/E-29: only a lone surrogate makes the body malformed; a pair is a name."""
    body = {**(VALID_QUOTE if path == "/pricing/quote" else VALID_SIMULATION), "\U0001f600": 1}
    response = client.post(path, content=json.dumps(body).encode(), headers=JSON)
    errors = assert_problem(response, 422, "validation_error")["errors"]
    assert isinstance(errors, list)
    assert [(error["field"], error["code"]) for error in errors] == [
        ("\U0001f600", "unknown_field")
    ]
