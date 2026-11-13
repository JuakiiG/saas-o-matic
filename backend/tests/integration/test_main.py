"""Smoke test of the application skeleton."""

from fastapi.testclient import TestClient

from app.main import create_app

MODIFYING_METHODS = {"put", "patch", "delete"}


def test_openapi_of_new_app_offers_no_update_or_delete_operation() -> None:
    """SPEC-03/E-18: the API offers no operation that modifies or deletes data.

    Smoke test: the application is built, answers over HTTP and publishes its
    OpenAPI contract. The assertion keeps guarding E-18 as routes are added.
    """
    client = TestClient(create_app())

    response = client.get("/openapi.json")

    assert response.status_code == 200
    offered = {method for operations in response.json()["paths"].values() for method in operations}
    assert offered.isdisjoint(MODIFYING_METHODS)
