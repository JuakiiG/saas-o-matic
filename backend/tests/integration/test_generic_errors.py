"""Generic errors of the API (index of specs, "Errores genéricos"; SPEC-03, 5.7)."""

import logging

import pytest
from fastapi.testclient import TestClient
from httpx2 import Response

from tests.integration.probe_app import INTERNAL_DETAIL, create_probe_app

PROBLEM_JSON = "application/problem+json"
JSON = {"content-type": "application/json"}
TEXT = {"content-type": "text/plain"}
VALID_BODY = b'{"name": "Acme"}'
CUT_BODY = b'{"name":'
DEEP_BODY = b"[" * 100_000


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_probe_app())


def assert_problem(response: Response, status: int, code: str) -> dict[str, object]:
    """Check the envelope common to every error and return its body."""
    assert response.status_code == status
    assert response.headers["content-type"] == PROBLEM_JSON
    body: dict[str, object] = response.json()
    assert body["type"] == "about:blank"
    assert body["status"] == status
    assert body["code"] == code
    assert isinstance(body["title"], str)
    assert isinstance(body["detail"], str)
    return body


@pytest.mark.parametrize("path", ["/clientes", "/probe/1/extra"])
def test_request_to_unknown_route_returns_404_not_found(client: TestClient, path: str) -> None:
    """SPEC-03/E-29: a route that does not exist answers 404 `not_found`, without `errors`."""
    body = assert_problem(client.get(path), 404, "not_found")
    assert "errors" not in body


@pytest.mark.parametrize("path", ["/health/", "/probe/"])
def test_route_with_trailing_slash_returns_404_without_redirecting(
    client: TestClient, path: str
) -> None:
    """SPEC-03/E-29: a route with a trailing slash is a route that does not exist."""
    response = client.get(path, follow_redirects=False)
    assert_problem(response, 404, "not_found")
    assert "location" not in response.headers


@pytest.mark.parametrize("method", ["PUT", "PATCH", "DELETE"])
def test_request_with_unsupported_method_returns_405_method_not_allowed(
    client: TestClient, method: str
) -> None:
    """SPEC-03/E-29: an existing route answers 405 to a method it does not accept."""
    assert_problem(client.request(method, "/probe"), 405, "method_not_allowed")


@pytest.mark.parametrize(
    ("path", "allowed"),
    [("/probe", "GET, POST"), ("/customers", "GET, POST"), ("/health", "GET"), ("/meta", "GET")],
)
def test_405_tells_every_method_that_the_route_admits(
    client: TestClient, path: str, allowed: str
) -> None:
    """SPEC-03/E-29: `Allow` names all the methods of the route, not only one of them."""
    response = client.delete(path)
    assert_problem(response, 405, "method_not_allowed")
    assert response.headers.get("allow") == allowed


def test_options_that_is_not_a_preflight_returns_405_method_not_allowed(client: TestClient) -> None:
    """SPEC-03/E-33: an OPTIONS without `Origin` is not a preflight and answers 405."""
    assert_problem(client.options("/probe"), 405, "method_not_allowed")


@pytest.mark.parametrize(
    "content",
    [
        CUT_BODY,
        b"[1, 2]",
        b"null",
        b"15",
        b'{"name": "\xff"}',
        DEEP_BODY,
        # Not JSON (RFC 8259), although Python's parser accepts them by default.
        b'{"name": "Acme", "a": NaN}',
        b'{"name": "Acme", "a": Infinity}',
        b'{"name": "Acme", "a": -Infinity}',
    ],
    ids=["cut", "list", "null", "number", "not-utf8", "too-deep", "NaN", "Infinity", "-Infinity"],
)
def test_body_that_is_not_a_json_object_returns_400_malformed_request(
    client: TestClient, content: bytes
) -> None:
    """SPEC-03/E-29: a body that is not valid JSON or not a JSON object answers 400."""
    response = client.post("/probe", content=content, headers=JSON)
    assert_problem(response, 400, "malformed_request")


@pytest.mark.parametrize("headers", [TEXT, {}], ids=["text/plain", "no-content-type"])
def test_body_without_json_content_type_returns_415_unsupported_media_type(
    client: TestClient, headers: dict[str, str]
) -> None:
    """SPEC-03/E-29: a request with a body whose Content-Type is not JSON answers 415."""
    response = client.post("/probe", content=VALID_BODY, headers=headers)
    assert_problem(response, 415, "unsupported_media_type")


def test_json_content_type_with_parameters_is_accepted(client: TestClient) -> None:
    """SPEC-03/E-29: `application/json; charset=utf-8` is a valid Content-Type."""
    headers = {"content-type": "application/json; charset=utf-8"}
    response = client.post("/probe", content=VALID_BODY, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"name": "Acme"}


def test_unsupported_media_type_wins_over_malformed_body_and_unknown_parameter(
    client: TestClient,
) -> None:
    """SPEC-03/E-29: precedence, 415 before 400 and 422."""
    response = client.post("/probe?debug=1", content=CUT_BODY, headers=TEXT)
    assert_problem(response, 415, "unsupported_media_type")


def test_malformed_body_wins_over_unknown_parameter(client: TestClient) -> None:
    """SPEC-03/E-29: precedence, 400 before 422."""
    response = client.post("/probe?debug=1", content=CUT_BODY, headers=JSON)
    assert_problem(response, 400, "malformed_request")


def test_undocumented_query_parameter_returns_422_with_unknown_field(client: TestClient) -> None:
    """SPEC-03/E-29: an undocumented query parameter answers 422 with `unknown_field`."""
    response = client.post("/probe?debug=1", content=VALID_BODY, headers=JSON)
    body = assert_problem(response, 422, "validation_error")
    assert body["title"] == "Unprocessable Content"
    errors = body["errors"]
    assert isinstance(errors, list)
    assert [(error["field"], error["code"]) for error in errors] == [("debug", "unknown_field")]
    assert isinstance(errors[0]["message"], str)


def test_declared_query_parameter_is_accepted(client: TestClient) -> None:
    """SPEC-03/E-29: only undocumented parameters are rejected; a declared one passes."""
    response = client.get("/probe?q=acme")
    assert response.status_code == 200
    assert response.json() == {"q": "acme"}


def test_each_undocumented_parameter_is_reported_once_in_request_order(client: TestClient) -> None:
    """SPEC-03/E-29: one error per field, in the order of the request."""
    body = assert_problem(client.get("/probe?b=1&q=x&a=2&b=3"), 422, "validation_error")
    errors = body["errors"]
    assert isinstance(errors, list)
    assert [error["field"] for error in errors] == ["b", "a"]


@pytest.mark.parametrize("path", ["/probe/failure", "/probe/teapot"])
def test_unexpected_failure_returns_500_without_internal_details(
    client: TestClient, path: str, caplog: pytest.LogCaptureFixture
) -> None:
    """SPEC-03/E-29: an unexpected error answers 500 `internal_error` and leaks nothing."""
    with caplog.at_level(logging.ERROR):
        response = client.get(path)
    assert_problem(response, 500, "internal_error")
    for leak in (INTERNAL_DETAIL, "Traceback", "RuntimeError", ".py"):
        assert leak not in response.text
    # The error is not swallowed: it is logged for whoever operates the backend.
    assert caplog.records
