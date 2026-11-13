"""CORS limited to the origin of the frontend (SPEC-03, 2.7 and 5.6).

The rows of 5.6 name `GET /meta`, which does not exist yet; `GET /probe` stands
in for it.
"""

import logging

import pytest
from fastapi.testclient import TestClient

from tests.integration.probe_app import create_probe_app

FRONTEND = "http://localhost:4200"
OTHER = "http://otro.example"
ALLOW_ORIGIN = "access-control-allow-origin"
PREFLIGHT = {
    "Access-Control-Request-Method": "POST",
    "Access-Control-Request-Headers": "content-type",
}
# Standard rejection of Starlette 1.10.0 (through FastAPI 0.162.0), pinned so that a
# change of version does not go unnoticed (SPEC-03, 2.7).
REJECTED_PREFLIGHT_HEADERS = {
    "vary": (
        "Origin, Access-Control-Request-Method, Access-Control-Request-Headers, "
        "Access-Control-Request-Private-Network"
    ),
    "access-control-allow-methods": "GET, POST",
    "access-control-max-age": "600",
    "access-control-allow-headers": "Accept, Accept-Language, Content-Language, Content-Type",
    "content-length": "22",
    "content-type": "text/plain; charset=utf-8",
}


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """The application started without `CORS_ORIGINS`."""
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    return TestClient(create_probe_app())


@pytest.fixture
def client_with_two_origins(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("CORS_ORIGINS", "http://a.example,http://b.example")
    return TestClient(create_probe_app())


def test_default_origin_gets_its_own_origin_back(client: TestClient) -> None:
    """SPEC-03/E-24, SPEC-03/E-26: without configuration, the local frontend is allowed."""
    response = client.get("/probe", headers={"Origin": FRONTEND})
    assert response.status_code == 200
    assert response.headers.get(ALLOW_ORIGIN) == FRONTEND


def test_unlisted_origin_gets_no_allow_origin_header(client: TestClient) -> None:
    """SPEC-03/E-25: any other origin is answered without the header."""
    response = client.get("/probe", headers={"Origin": OTHER})
    assert response.status_code == 200
    assert ALLOW_ORIGIN not in response.headers


def test_default_origin_is_not_allowed_once_origins_are_configured(
    client_with_two_origins: TestClient,
) -> None:
    """SPEC-03/E-25, SPEC-03/E-26: the default only applies while the variable is undefined."""
    response = client_with_two_origins.get("/probe", headers={"Origin": FRONTEND})
    assert ALLOW_ORIGIN not in response.headers


def test_each_configured_origin_gets_its_own_origin_back(
    client_with_two_origins: TestClient,
) -> None:
    """SPEC-03/E-24: with a list, the header carries the requesting origin, never `*`."""
    response = client_with_two_origins.get("/probe", headers={"Origin": "http://b.example"})
    assert response.headers.get(ALLOW_ORIGIN) == "http://b.example"


def test_preflight_from_allowed_origin_returns_200_with_cors_headers(client: TestClient) -> None:
    """SPEC-03/E-30: an admitted preflight answers 200, not 405."""
    response = client.options("/probe", headers={"Origin": FRONTEND, **PREFLIGHT})
    assert response.status_code == 200
    assert response.headers.get(ALLOW_ORIGIN) == FRONTEND
    assert "POST" in response.headers["access-control-allow-methods"]
    assert "content-type" in response.headers["access-control-allow-headers"].lower()


def test_preflight_from_unlisted_origin_gets_the_standard_rejection(client: TestClient) -> None:
    """SPEC-03/E-31: rejected by the middleware, without `access-control-allow-origin`."""
    response = client.options("/probe", headers={"Origin": OTHER, **PREFLIGHT})
    assert response.status_code == 400
    assert dict(response.headers) == REJECTED_PREFLIGHT_HEADERS


def test_preflight_for_unlisted_method_gets_the_standard_rejection(client: TestClient) -> None:
    """SPEC-03/E-31: a preflight for DELETE is rejected by the middleware."""
    headers = {"Origin": FRONTEND, **PREFLIGHT, "Access-Control-Request-Method": "DELETE"}
    response = client.options("/probe", headers=headers)
    assert response.status_code == 400
    assert dict(response.headers) == {**REJECTED_PREFLIGHT_HEADERS, ALLOW_ORIGIN: FRONTEND}


def test_unexpected_failure_keeps_the_cors_header(
    client: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    """SPEC-03/E-24: the 500 also carries the header, so the frontend can read it."""
    with caplog.at_level(logging.ERROR):
        response = client.get("/probe/failure", headers={"Origin": FRONTEND})
    assert response.status_code == 500
    assert response.json()["code"] == "internal_error"
    assert response.headers.get(ALLOW_ORIGIN) == FRONTEND


def test_error_response_keeps_the_cors_header(client: TestClient) -> None:
    """SPEC-03/E-24: the header goes with any response to an allowed origin, errors included."""
    response = client.get("/clientes", headers={"Origin": FRONTEND})
    assert response.status_code == 404
    assert response.headers.get(ALLOW_ORIGIN) == FRONTEND


def test_options_with_origin_but_no_requested_method_returns_405(client: TestClient) -> None:
    """SPEC-03/E-33: without `Access-Control-Request-Method` it is not a preflight."""
    response = client.options("/probe", headers={"Origin": FRONTEND})
    assert response.status_code == 405
    assert response.json()["code"] == "method_not_allowed"


def test_spaces_and_empty_entries_in_the_list_are_ignored(monkeypatch: pytest.MonkeyPatch) -> None:
    """SPEC-03/E-24: the comma separated list tolerates spaces and a trailing comma."""
    monkeypatch.setenv("CORS_ORIGINS", " http://a.example , http://b.example,")
    response = TestClient(create_probe_app()).get("/probe", headers={"Origin": "http://b.example"})
    assert response.headers.get(ALLOW_ORIGIN) == "http://b.example"


def test_empty_list_allows_no_origin(monkeypatch: pytest.MonkeyPatch) -> None:
    """SPEC-03/E-25, SPEC-03/E-26: defined but empty is not undefined; nobody is allowed."""
    monkeypatch.setenv("CORS_ORIGINS", "")
    response = TestClient(create_probe_app()).get("/probe", headers={"Origin": FRONTEND})
    assert ALLOW_ORIGIN not in response.headers
