"""`GET /health` (SPEC-03, 2.7, 4.4 and 5.6)."""

import logging
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

PROBLEM_JSON = "application/problem+json"


def client_for(database_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """The application started with `DATABASE_PATH` pointing to `database_path`."""
    monkeypatch.setenv("DATABASE_PATH", str(database_path))
    return TestClient(create_app())


def test_health_with_database_that_answers_returns_200_ok(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """SPEC-03/E-27: the backend is up and the database answers a trivial query."""
    response = client_for(tmp_path / "health.db", monkeypatch).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_with_database_that_does_not_answer_returns_503(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """SPEC-03/E-28: 503 `service_unavailable`, without traces or internal details.

    The failing connection is a real one: the path is a folder, not a file.
    """
    with caplog.at_level(logging.ERROR):
        response = client_for(tmp_path, monkeypatch).get("/health")
    assert response.status_code == 503
    assert response.headers.get("content-type") == PROBLEM_JSON
    body = response.json()
    assert (body["status"], body["code"]) == (503, "service_unavailable")
    assert body["title"] == "Service Unavailable"
    for leak in (str(tmp_path), tmp_path.name, "Traceback", "sqlite", "OperationalError", ".py"):
        assert leak not in response.text
    # Whoever operates the backend finds the cause in the log.
    assert caplog.records


def test_openapi_declares_the_contract_of_health(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """SPEC-03/E-27, SPEC-03/E-28: the generated OpenAPI declares the 200 and the 503 (CA-14)."""
    document = client_for(tmp_path / "health.db", monkeypatch).get("/openapi.json").json()
    operation = document["paths"].get("/health", {}).get("get", {})
    assert sorted(operation.get("responses", {})) == ["200", "503"]
    schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
    name = schema["$ref"].rsplit("/", maxsplit=1)[-1]
    assert list(document["components"]["schemas"][name]["properties"]) == ["status"]
