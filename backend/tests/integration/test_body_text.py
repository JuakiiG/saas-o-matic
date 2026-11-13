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
# A valid body of each POST, which answers 201, 200 and 201 when it is sent as UTF-8.
VALID_BODIES: list[tuple[str, dict[str, object]]] = [
    ("/customers", NEW_CUSTOMER),
    ("/pricing/quote", VALID_QUOTE),
    ("/simulations", VALID_SIMULATION),
]
# Python codecs for what is not strict UTF-8: `utf-16` and `utf-32` write a byte order
# mark, the ones with `-le` or `-be` do not, and `utf-8-sig` is UTF-8 with the mark.
OTHER_ENCODINGS = [
    "utf-16",
    "utf-16-le",
    "utf-16-be",
    "utf-32",
    "utf-32-le",
    "utf-32-be",
    "utf-8-sig",
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


@pytest.mark.parametrize("encoding", OTHER_ENCODINGS)
@pytest.mark.parametrize(("path", "body"), VALID_BODIES, ids=[path for path, _ in VALID_BODIES])
def test_body_that_is_not_strict_utf8_returns_400_and_stores_nothing(
    client: TestClient, database: Database, path: str, body: dict[str, object], encoding: str
) -> None:
    """SPEC-03/E-29: UTF-16 and UTF-32, with a byte order mark or without, and UTF-8 with it."""
    content = json.dumps(body).encode(encoding)
    assert content != json.dumps(body).encode()
    response = client.post(path, content=content, headers=JSON)
    assert_problem(response, 400, "malformed_request")
    assert stored_counts(database) == [3, 0, 0]


def test_charset_of_the_content_type_does_not_change_how_the_body_is_read(
    client: TestClient,
) -> None:
    """SPEC-03/E-29: a body in UTF-16 is malformed even if its Content-Type declares it."""
    headers = {"content-type": "application/json; charset=utf-16"}
    content = json.dumps(VALID_QUOTE).encode("utf-16")
    assert_problem(
        client.post("/pricing/quote", content=content, headers=headers), 400, "malformed_request"
    )


# Never seen failing before the code (session 05, H-02): it fixes what must keep working.
# A mutation (a guard that rejects whatever is not ASCII) showed afterwards that it can fail.
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


# Never seen failing before the code (session 05, H-02), as the test above, and the same
# mutation made it fail.
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


# Written after the code that it tests (session 05, H-04): it was never seen failing.
@pytest.mark.parametrize(
    ("digits", "status", "code", "field_errors"),
    [
        (4300, 422, "validation_error", [("active_users", "out_of_range")]),
        (4301, 400, "malformed_request", []),
    ],
)
def test_json_integer_of_more_than_4300_digits_is_a_malformed_body(
    client: TestClient, digits: int, status: int, code: str, field_errors: list[tuple[str, str]]
) -> None:
    """SPEC-03/E-29, SPEC-02/E-14: known limitation L-05, fixed here so that it is not a surprise.

    Up to 4300 digits it is an integer out of range. One more and the parser of Python
    refuses to read it (its protection against denial of service): not valid JSON for us.
    """
    content = b'{"customer_id": 1, "active_users": ' + b"9" * digits + b"}"
    body = assert_problem(
        client.post("/pricing/quote", content=content, headers=JSON), status, code
    )
    errors = body.get("errors", [])
    assert isinstance(errors, list)
    assert [(error["field"], error["code"]) for error in errors] == field_errors
