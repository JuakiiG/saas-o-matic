"""What the OpenAPI contract declares for the operation that a request matched.

The generated OpenAPI is the contract (`.claude/rules/backend.md`), so what a
request may carry is read from it and not from the internals of the framework.
"""

from typing import Any

from fastapi import Request

JSON_MEDIA_TYPE = "application/json"


# `Any` in the values: an OpenAPI document is JSON, and FastAPI types it so.
def operation_of(request: Request) -> dict[str, Any]:
    """The operation of the contract for the route and method of the request."""
    paths: dict[str, Any] = request.app.openapi()["paths"]
    operation: dict[str, Any] = paths.get(request.scope["route"].path, {}).get(
        request.method.lower(), {}
    )
    return operation


def query_parameters_of(request: Request) -> set[str]:
    """Names of the query parameters that the operation declares."""
    return {
        parameter["name"]
        for parameter in operation_of(request).get("parameters", [])
        if parameter["in"] == "query"
    }


# `Any` in the values, as above.
def body_schema_of(request: Request) -> dict[str, Any]:
    """Schema of the JSON body of the operation; empty when it takes no body."""
    content = operation_of(request).get("requestBody", {}).get("content", {})
    reference: str = content.get(JSON_MEDIA_TYPE, {}).get("schema", {}).get("$ref", "")
    schemas: dict[str, Any] = request.app.openapi().get("components", {}).get("schemas", {})
    schema: dict[str, Any] = schemas.get(reference.rsplit("/", maxsplit=1)[-1], {})
    return schema
