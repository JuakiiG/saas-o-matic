"""Checks that every request passes before reaching an endpoint (SPEC-03/E-29).

In order, which is the precedence of the contract: the body must be declared as
JSON (415), must be a JSON object whose text is Unicode (400) and the query string
may only carry parameters documented for that operation (422).
"""

import json

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.api.contract import JSON_MEDIA_TYPE, query_parameters_of
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

UNKNOWN_PARAMETER_MESSAGE = "Parámetro no documentado."


def _is_json_media_type(content_type: str | None) -> bool:
    """`application/json`, with or without parameters such as `charset`."""
    media_type = (content_type or "").split(";", maxsplit=1)[0]
    return media_type.strip().lower() == JSON_MEDIA_TYPE


def _reject_constant(name: str) -> None:
    """`NaN`, `Infinity` and `-Infinity` are not JSON (RFC 8259); Python accepts them by default."""
    raise ValueError(f"{name} is not valid JSON")


def _is_unicode_text(parsed: object) -> bool:
    """False if a string or a field name, at any depth, holds a lone surrogate.

    The escape `\\ud800` is JSON by its grammar, but that text does not represent Unicode
    characters (RFC 8259, 8.2): it can be neither stored nor answered as UTF-8. The parser
    joins a well-formed pair into one character, so only a lone one fails to encode.
    """
    try:
        json.dumps(parsed, ensure_ascii=False).encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _is_json_object(body: bytes) -> bool:
    try:
        parsed = json.loads(body, parse_constant=_reject_constant)
    except (ValueError, RecursionError):
        # Not UTF-8, not JSON, or nested beyond what the parser accepts.
        return False
    return isinstance(parsed, dict) and _is_unicode_text(parsed)


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


async def received_json_object(request: Request) -> dict[str, object]:
    """Dependency: the JSON object of the body, for an endpoint that validates it by hand.

    The guard has already seen that the body, if there is one, is a JSON object. An
    absent body is an empty object (index of specs, "Errores de validación").
    """
    body = await request.body()
    received: dict[str, object] = json.loads(body) if body else {}
    return received


def reject_undocumented_query_parameters(request: Request) -> None:
    """Dependency of every endpoint: an undocumented query parameter is a 422, not ignored."""
    documented = query_parameters_of(request)
    unknown = [name for name in dict.fromkeys(request.query_params) if name not in documented]
    if unknown:
        errors = (
            FieldError(name, FieldCode.UNKNOWN_FIELD, UNKNOWN_PARAMETER_MESSAGE) for name in unknown
        )
        raise ProblemError(validation_problem(tuple(errors)))
