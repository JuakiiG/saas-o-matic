"""Checks that every request passes before reaching an endpoint (SPEC-03/E-29).

In order, which is the precedence of the contract: the body must be declared as
JSON (415), must be a JSON object (400) and the query string may only carry
parameters documented for that operation (422).
"""

import json

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.api.problems import (
    MALFORMED_REQUEST,
    UNSUPPORTED_MEDIA_TYPE,
    FieldCode,
    FieldError,
    Problem,
    ProblemError,
    problem_response,
    validation_problem,
)

JSON_MEDIA_TYPE = "application/json"
UNKNOWN_PARAMETER_MESSAGE = "Parámetro no documentado."


def _is_json_media_type(content_type: str | None) -> bool:
    """`application/json`, with or without parameters such as `charset`."""
    media_type = (content_type or "").split(";", maxsplit=1)[0]
    return media_type.strip().lower() == JSON_MEDIA_TYPE


def _reject_constant(name: str) -> None:
    """`NaN`, `Infinity` and `-Infinity` are not JSON (RFC 8259); Python accepts them by default."""
    raise ValueError(f"{name} is not valid JSON")


def _is_json_object(body: bytes) -> bool:
    try:
        return isinstance(json.loads(body, parse_constant=_reject_constant), dict)
    except (ValueError, RecursionError):
        # Not UTF-8, not JSON, or nested beyond what the parser accepts.
        return False


def body_problem(content_type: str | None, body: bytes) -> Problem | None:
    """What is wrong with the body of a request, if anything. No body, no problem."""
    if not body:
        return None
    if not _is_json_media_type(content_type):
        return UNSUPPORTED_MEDIA_TYPE
    if not _is_json_object(body):
        return MALFORMED_REQUEST
    return None


class RequestBodyGuard(BaseHTTPMiddleware):
    """Rejects a body that is not a JSON object before any endpoint parses it.

    It runs before routing, so it also applies to a route that does not exist.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        problem = body_problem(request.headers.get("content-type"), await request.body())
        if problem is not None:
            return problem_response(problem)
        return await call_next(request)


def _documented_query_parameters(request: Request) -> set[str]:
    """Query parameters that the OpenAPI contract declares for the matched operation."""
    paths = request.app.openapi()["paths"]
    operation = paths.get(request.scope["route"].path, {}).get(request.method.lower(), {})
    return {
        parameter["name"]
        for parameter in operation.get("parameters", [])
        if parameter["in"] == "query"
    }


def reject_undocumented_query_parameters(request: Request) -> None:
    """Dependency of every endpoint: an undocumented query parameter is a 422, not ignored."""
    documented = _documented_query_parameters(request)
    unknown = [name for name in dict.fromkeys(request.query_params) if name not in documented]
    if unknown:
        errors = (
            FieldError(name, FieldCode.UNKNOWN_FIELD, UNKNOWN_PARAMETER_MESSAGE) for name in unknown
        )
        raise ProblemError(validation_problem(tuple(errors)))
