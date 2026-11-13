"""The single place where errors become HTTP responses (`.claude/rules/backend.md`).

Nothing internal leaves the server: an unexpected error is logged here and the
client only gets `internal_error`.
"""

import logging

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.api.contract import body_schema_of
from app.api.problems import (
    CUSTOMER_NOT_FOUND,
    INTERNAL_ERROR,
    METHOD_NOT_ALLOWED,
    NOT_FOUND,
    SERVICE_UNAVAILABLE,
    TAX_RATE_NOT_DEFINED,
    ProblemError,
    problem_response,
    validation_problem,
)
from app.api.validation import field_errors
from app.domain.countries import TaxRateNotDefinedError
from app.services.health import ServiceUnavailableError
from app.services.pricing import CustomerNotFoundError

logger = logging.getLogger(__name__)

# Statuses that the framework raises on its own, mapped to the generic errors of the contract.
HTTP_PROBLEMS = {404: NOT_FOUND, 405: METHOD_NOT_ALLOWED}


class UnexpectedErrorGuard(BaseHTTPMiddleware):
    """Turns any error nobody handled into a 500 `internal_error`.

    A middleware and not an exception handler, so that the response is produced
    inside the CORS middleware and the browser lets the frontend read it.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except Exception:
            logger.exception("Unexpected error in %s %s", request.method, request.url.path)
            return problem_response(INTERNAL_ERROR)


def install_error_handling(app: FastAPI) -> None:
    """Register the handlers and the guard on the application."""

    @app.exception_handler(ProblemError)
    async def handle_problem(request: Request, error: ProblemError) -> Response:
        return problem_response(error.problem)

    @app.exception_handler(RequestValidationError)
    async def handle_invalid_request(request: Request, error: RequestValidationError) -> Response:
        # Replaces the handler of the framework: its format never leaves the server.
        errors = field_errors(error.errors(), body_schema_of(request))
        return problem_response(validation_problem(errors))

    @app.exception_handler(HTTPException)
    async def handle_http_error(request: Request, error: HTTPException) -> Response:
        problem = HTTP_PROBLEMS.get(error.status_code)
        if problem is None:
            # An HTTP error that the contract does not define is a bug of ours, not of the caller.
            logger.error("HTTP error outside the contract: %s", error.status_code)
            return problem_response(INTERNAL_ERROR)
        return problem_response(problem, error.headers)

    @app.exception_handler(CustomerNotFoundError)
    async def handle_unknown_customer(request: Request, error: CustomerNotFoundError) -> Response:
        return problem_response(CUSTOMER_NOT_FOUND)

    @app.exception_handler(TaxRateNotDefinedError)
    async def handle_missing_rate(request: Request, error: TaxRateNotDefinedError) -> Response:
        # Stored data is inconsistent: a failure of ours, logged, and never a rate of 0 %.
        logger.error("Country without tax rate: %s", error)
        return problem_response(TAX_RATE_NOT_DEFINED)

    @app.exception_handler(ServiceUnavailableError)
    async def handle_unavailable(request: Request, error: ServiceUnavailableError) -> Response:
        logger.error("Service unavailable: %s", error, exc_info=error)
        return problem_response(SERVICE_UNAVAILABLE)

    app.add_middleware(UnexpectedErrorGuard)
