"""Validation errors of a body, in the format of the contract and never in the framework's.

Index of specs, "Errores de validación": one error per field, the first that fails,
in the order of the fields of the contract. Tested on a probe route; the rows of
each real endpoint are tested with that endpoint.
"""

import logging
import re

import pytest
from fastapi.testclient import TestClient
from httpx2 import Response

from tests.integration.probe_app import MAX_ID, create_probe_app
from tests.integration.test_generic_errors import assert_problem

MISSING_BOTH = [("id", "missing"), ("count", "missing")]
# Body and the (field, code) pairs expected, in order.
INVALID_BODIES = [
    ({}, MISSING_BOTH),
    ({"id": 1}, [("count", "missing")]),
    ({"id": "1", "count": 5}, [("id", "not_an_integer")]),
    ({"id": 1.0, "count": 5}, [("id", "not_an_integer")]),
    ({"id": 1, "count": 5.5}, [("count", "not_an_integer")]),
    ({"id": 1, "count": True}, [("count", "not_an_integer")]),
    ({"id": None, "count": 5}, [("id", "not_an_integer")]),
    ({"id": 0, "count": 5}, [("id", "out_of_range")]),
    ({"id": MAX_ID + 1, "count": 5}, [("id", "out_of_range")]),
    ({"id": 1, "count": -1}, [("count", "out_of_range")]),
    ({"id": 1, "count": 101}, [("count", "out_of_range")]),
    ({"id": 1, "count": 5, "floor": -1}, [("floor", "out_of_range")]),
    ({"id": 1, "count": 5, "extra": 1}, [("extra", "unknown_field")]),
    # A field that fails twice is reported once, with its first error.
    ({"id": 1, "count": 5, "either": "x"}, [("either", "not_an_integer")]),
    # Fields of the contract in its order, whatever the order of the request; then the
    # unknown ones, in alphabetical order of their name.
    (
        {"zeta": 1, "count": -1, "alpha": 2, "id": "x", "Beta": 3},
        [
            ("id", "not_an_integer"),
            ("count", "out_of_range"),
            ("Beta", "unknown_field"),
            ("alpha", "unknown_field"),
            ("zeta", "unknown_field"),
        ],
    ),
]


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_probe_app())


def assert_contract_422(response: Response) -> list[dict[str, str]]:
    """A 422 with the fields of the contract and nothing else; returns its `errors`."""
    body = assert_problem(response, 422, "validation_error")
    assert sorted(body) == ["code", "detail", "errors", "status", "title", "type"]
    errors = body["errors"]
    assert isinstance(errors, list)
    for error in errors:
        assert sorted(error) == ["code", "field", "message"]
        assert all(isinstance(value, str) and value for value in error.values())
    return errors


@pytest.mark.parametrize(("payload", "expected"), INVALID_BODIES)
def test_invalid_body_returns_422_with_one_error_per_field_in_contract_order(
    client: TestClient, payload: dict[str, object], expected: list[tuple[str, str]]
) -> None:
    """SPEC-02/E-14: `validation_error` with the code of each field, never FastAPI's format."""
    errors = assert_contract_422(client.post("/probe/numbers", json=payload))
    assert [(error["field"], error["code"]) for error in errors] == expected


def test_absent_body_returns_422_with_every_required_field_missing(client: TestClient) -> None:
    """SPEC-02/E-14: no body at all is answered like `{}`, in the format of the contract."""
    errors = assert_contract_422(client.post("/probe/numbers"))
    assert [(error["field"], error["code"]) for error in errors] == MISSING_BOTH


def test_valid_body_passes_the_validation(client: TestClient) -> None:
    """SPEC-02/E-14: only an invalid request is rejected; the limits themselves are valid."""
    response = client.post("/probe/numbers", json={"id": MAX_ID, "count": 0})
    assert response.status_code == 200
    assert response.json() == {"id": MAX_ID, "count": 0}


@pytest.mark.parametrize(
    ("payload", "limit"),
    [
        ({"id": 1, "count": 101}, "100"),
        ({"id": 1, "count": -1}, "0"),
        ({"id": MAX_ID + 1, "count": 5}, str(MAX_ID)),
    ],
    ids=["above-maximum", "below-minimum", "above-largest-id"],
)
def test_out_of_range_message_tells_the_limit_as_an_exact_integer(
    client: TestClient, payload: dict[str, int], limit: str
) -> None:
    """SPEC-02/E-14: the message carries the limit that was crossed, never as a decimal."""
    errors = assert_contract_422(client.post("/probe/numbers", json=payload))
    numbers = re.findall(r"\d[\d.e+]*", errors[0]["message"].rstrip("."))
    assert numbers == [limit]


def test_validation_without_a_code_in_the_contract_returns_500_not_the_framework_format(
    client: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    """SPEC-03/E-29: a failed validation that has no code is our bug: 500, and it is logged."""
    with caplog.at_level(logging.ERROR):
        response = client.post("/probe", json={"name": 5})
    assert_problem(response, 500, "internal_error")
    assert "string_type" not in response.text
    assert caplog.records
