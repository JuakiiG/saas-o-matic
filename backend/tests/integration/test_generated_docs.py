"""The routes that the framework publishes by itself (index of specs, "Documentación generada").

`/docs` and `/openapi.json` stay; `/redoc` and `/docs/oauth2-redirect` do not exist.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from tests.integration.test_generic_errors import assert_problem


@pytest.fixture
def client() -> TestClient:
    # Not started: none of these routes reads the database.
    return TestClient(create_app())


@pytest.mark.parametrize("path", ["/redoc", "/docs/oauth2-redirect"])
def test_route_of_the_framework_that_is_switched_off_returns_404_not_found(
    client: TestClient, path: str
) -> None:
    """SPEC-03/E-29: a second page of documentation and an OAuth page nobody uses are no routes."""
    body = assert_problem(client.get(path), 404, "not_found")
    assert "errors" not in body


def test_docs_page_is_served_and_no_longer_points_at_the_oauth_redirection(
    client: TestClient,
) -> None:
    """SPEC-03/E-29: `/docs` is kept for whoever reviews the API, without the OAuth route."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "/openapi.json" in response.text
    assert "oauth2-redirect" not in response.text


# Written after the code that it tests (session 05, H-09): it was never seen failing.
@pytest.mark.parametrize("path", ["/docs?x=1", "/openapi.json?x=1"])
def test_generated_documentation_does_not_apply_the_rule_of_the_unknown_parameter(
    client: TestClient, path: str
) -> None:
    """SPEC-03/E-29: they are not business endpoints, and an unknown parameter is not a 422."""
    assert client.get(path).status_code == 200


# Written after the code that it tests (session 05, H-09): it was never seen failing.
def test_openapi_document_lists_no_route_of_the_generated_documentation(
    client: TestClient,
) -> None:
    """SPEC-03/E-29: the contract describes the business endpoints, not the pages about it."""
    paths = client.get("/openapi.json").json()["paths"]
    assert not [path for path in paths if path.startswith(("/docs", "/redoc", "/openapi"))]
