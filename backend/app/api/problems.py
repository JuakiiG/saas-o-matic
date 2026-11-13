"""Error responses of the API: `application/problem+json` (RFC 9457) with a stable code.

The only module that defines error codes. A code is part of the contract and is
never renamed; `detail` and `message` are Spanish text for people and may change
(index of specs, "Convenciones comunes de la API"; ADR-006).
"""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum

from fastapi.responses import JSONResponse

PROBLEM_MEDIA_TYPE = "application/problem+json"
# Written out because the phrase of 422 depends on the Python version; the contract says this one.
TITLES = {
    400: "Bad Request",
    404: "Not Found",
    405: "Method Not Allowed",
    415: "Unsupported Media Type",
    422: "Unprocessable Content",
    500: "Internal Server Error",
}


class ErrorCode(StrEnum):
    MALFORMED_REQUEST = "malformed_request"
    UNSUPPORTED_MEDIA_TYPE = "unsupported_media_type"
    NOT_FOUND = "not_found"
    METHOD_NOT_ALLOWED = "method_not_allowed"
    VALIDATION_ERROR = "validation_error"
    INTERNAL_ERROR = "internal_error"


class FieldCode(StrEnum):
    UNKNOWN_FIELD = "unknown_field"


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
