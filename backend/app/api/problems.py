"""Error responses of the API: `application/problem+json` (RFC 9457) with a stable code.

The only module that defines error codes. A code is part of the contract and is
never renamed; `detail` and `message` are Spanish text for people and may change
(index of specs, "Convenciones comunes de la API"; ADR-006).
"""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from fastapi.responses import JSONResponse

PROBLEM_MEDIA_TYPE = "application/problem+json"
# Written out because the phrase of 422 depends on the Python version; the contract says this one.
TITLES = {
    400: "Bad Request",
    404: "Not Found",
    405: "Method Not Allowed",
    409: "Conflict",
    415: "Unsupported Media Type",
    422: "Unprocessable Content",
    500: "Internal Server Error",
    503: "Service Unavailable",
}


class ErrorCode(StrEnum):
    MALFORMED_REQUEST = "malformed_request"
    UNSUPPORTED_MEDIA_TYPE = "unsupported_media_type"
    NOT_FOUND = "not_found"
    METHOD_NOT_ALLOWED = "method_not_allowed"
    VALIDATION_ERROR = "validation_error"
    INTERNAL_ERROR = "internal_error"
    SERVICE_UNAVAILABLE = "service_unavailable"
    CUSTOMER_NOT_FOUND = "customer_not_found"
    TAX_RATE_NOT_DEFINED = "tax_rate_not_defined"
    CUSTOMER_ALREADY_EXISTS = "customer_already_exists"


class FieldCode(StrEnum):
    MISSING = "missing"
    NOT_AN_INTEGER = "not_an_integer"
    OUT_OF_RANGE = "out_of_range"
    UNKNOWN_FIELD = "unknown_field"
    NOT_A_STRING = "not_a_string"
    INVALID_CHARACTERS = "invalid_characters"
    TOO_SHORT = "too_short"
    TOO_LONG = "too_long"
    INVALID_EMAIL = "invalid_email"
    UNSUPPORTED_COUNTRY = "unsupported_country"
    UNSUPPORTED_PLAN = "unsupported_plan"
    INVALID_TAX_ID_FORMAT = "invalid_tax_id_format"
    INVALID_TAX_ID_CHECK_CHARACTER = "invalid_tax_id_check_character"


@dataclass(frozen=True)
class FieldError:
    """One invalid field of a request: which one, why (stable code) and a message to show."""

    field: str
    code: FieldCode
    message: str


@dataclass(frozen=True)
class Problem:
    """An error response. `errors` is only filled for validation errors."""

    status: int
    code: ErrorCode
    detail: str
    errors: tuple[FieldError, ...] = ()


class ProblemError(Exception):
    """Raised inside a request to answer with a problem; translated in `error_handling`."""

    def __init__(self, problem: Problem) -> None:
        super().__init__(problem.code)
        self.problem = problem


MALFORMED_REQUEST = Problem(
    400, ErrorCode.MALFORMED_REQUEST, "El cuerpo de la petición no es un objeto JSON válido."
)
UNSUPPORTED_MEDIA_TYPE = Problem(
    415,
    ErrorCode.UNSUPPORTED_MEDIA_TYPE,
    "El cuerpo de la petición debe enviarse como application/json.",
)
NOT_FOUND = Problem(404, ErrorCode.NOT_FOUND, "La ruta no existe.")
METHOD_NOT_ALLOWED = Problem(405, ErrorCode.METHOD_NOT_ALLOWED, "La ruta no admite ese método.")
INTERNAL_ERROR = Problem(500, ErrorCode.INTERNAL_ERROR, "Error interno del servidor.")
SERVICE_UNAVAILABLE = Problem(
    503, ErrorCode.SERVICE_UNAVAILABLE, "El servicio no está disponible en este momento."
)
CUSTOMER_NOT_FOUND = Problem(404, ErrorCode.CUSTOMER_NOT_FOUND, "No existe un cliente con ese id.")
# Nothing about the customer that already exists, not even its id (SPEC-01, D-06).
CUSTOMER_ALREADY_EXISTS = Problem(
    409,
    ErrorCode.CUSTOMER_ALREADY_EXISTS,
    "Ya existe un cliente con ese identificador fiscal en ese país.",
)
TAX_RATE_NOT_DEFINED = Problem(
    500,
    ErrorCode.TAX_RATE_NOT_DEFINED,
    "El país del cliente no tiene un tipo impositivo definido.",
)


def validation_problem(errors: tuple[FieldError, ...]) -> Problem:
    return Problem(
        422, ErrorCode.VALIDATION_ERROR, "La petición contiene datos no válidos.", errors
    )


def problem_response(problem: Problem, headers: Mapping[str, str] | None = None) -> JSONResponse:
    """Build the HTTP response of a problem; never includes anything but its own fields."""
    body: dict[str, object] = {
        "type": "about:blank",
        "title": TITLES[problem.status],
        "status": problem.status,
        "code": problem.code,
        "detail": problem.detail,
    }
    if problem.errors:
        body["errors"] = [
            {"field": error.field, "code": error.code, "message": error.message}
            for error in problem.errors
        ]
    return JSONResponse(
        body, status_code=problem.status, headers=headers, media_type=PROBLEM_MEDIA_TYPE
    )


_TEXT = {"type": "string"}
_FIELD_ERROR_SCHEMA = {
    "type": "object",
    "properties": {"field": _TEXT, "code": _TEXT, "message": _TEXT},
    "required": ["field", "code", "message"],
}
# Shape of an error response, for the OpenAPI contract. Written inline and not as a
# Pydantic model because FastAPI documents a model under `application/json`, which is
# not the media type the errors are answered with.
PROBLEM_SCHEMA = {
    "type": "object",
    "properties": {
        "type": _TEXT,
        "title": _TEXT,
        "status": {"type": "integer"},
        "code": _TEXT,
        "detail": _TEXT,
        "errors": {"type": "array", "items": _FIELD_ERROR_SCHEMA},
    },
    "required": ["type", "title", "status", "code", "detail"],
}


# `Any` in the values because that is the type of the `responses` parameter of FastAPI.
def problem_responses(descriptions: Mapping[int, str]) -> dict[int | str, dict[str, Any]]:
    """The `responses` of an endpoint: each error status, declared as it is answered."""
    content = {PROBLEM_MEDIA_TYPE: {"schema": PROBLEM_SCHEMA}}
    return {
        status: {"description": description, "content": content}
        for status, description in descriptions.items()
    }
