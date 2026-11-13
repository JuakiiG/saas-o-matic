"""The single place where errors become HTTP responses (`.claude/rules/backend.md`).

Nothing internal leaves the server: an unexpected error is logged here and the
client only gets `internal_error`.
"""

import logging
from http import HTTPStatus

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.api.contract import body_schema_of, methods_of
from app.api.customer_errors import customer_field_errors
from app.api.problems import (
    CUSTOMER_ALREADY_EXISTS,
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
from app.domain.customers import InvalidCustomerError
from app.services.customers import CustomerAlreadyExistsError, CustomerNotFoundError

logger = logging.getLogger(__name__)


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


def install_error_handling(app: FastAPI, unavailable: type[Exception]) -> None:
    """Register the handlers and the guard on the application.

    `unavailable` is the error that means "the database cannot be read now" (503). The
    composition root hands it over because this layer does not import `repositories/`.
    """
    _install_request_handlers(app)
    _install_use_case_handlers(app, unavailable)
    app.add_middleware(UnexpectedErrorGuard)


def _install_request_handlers(app: FastAPI) -> None:
    """Errors of the request itself, found before any use case runs."""

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
        if error.status_code == HTTPStatus.NOT_FOUND:
            return problem_response(NOT_FOUND)
        if error.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
            allowed = ", ".join(_admitted_methods(request, error))
            return problem_response(METHOD_NOT_ALLOWED, {"Allow": allowed})
        # An HTTP error that the contract does not define is a bug of ours, not of the caller.
        logger.error("HTTP error outside the contract: %s", error.status_code)
        return problem_response(INTERNAL_ERROR)


def _admitted_methods(request: Request, error: HTTPException) -> list[str]:
    """The methods that the route of a 405 admits, for its `Allow` header.

    The framework names only the methods of the first route that fits the path; the
    contract knows them all. A route outside the contract (`/docs`, `/openapi.json`) is
    a single route, so there what the framework names is all there is, `HEAD` included.
    """
    declared = methods_of(request)
    if declared:
        return declared
    named = (error.headers or {}).get("Allow", "")
    # Sorted: the framework writes them in the order of a set, which changes between runs.
    return sorted(method.strip() for method in named.split(","))


def _install_use_case_handlers(app: FastAPI, unavailable: type[Exception]) -> None:
    """Errors that a service, the domain or the database raise while answering."""

    @app.exception_handler(InvalidCustomerError)
    async def handle_invalid_customer(request: Request, error: InvalidCustomerError) -> Response:
        return problem_response(validation_problem(customer_field_errors(error.problems)))

    @app.exception_handler(CustomerAlreadyExistsError)
    async def handle_duplicate(request: Request, error: CustomerAlreadyExistsError) -> Response:
        return problem_response(CUSTOMER_ALREADY_EXISTS)

    @app.exception_handler(CustomerNotFoundError)
    async def handle_unknown_customer(request: Request, error: CustomerNotFoundError) -> Response:
        return problem_response(CUSTOMER_NOT_FOUND)

    @app.exception_handler(TaxRateNotDefinedError)
    async def handle_missing_rate(request: Request, error: TaxRateNotDefinedError) -> Response:
        # Stored data is inconsistent: a failure of ours, logged, and never a rate of 0 %.
        logger.error("Country without tax rate: %s", error)
        return problem_response(TAX_RATE_NOT_DEFINED)

    @app.exception_handler(unavailable)
    async def handle_unavailable(request: Request, error: Exception) -> Response:
        # Whatever the endpoint: not available now, which is not a failure of ours (500).
        logger.error("Service unavailable: %s", error, exc_info=error)
        return problem_response(SERVICE_UNAVAILABLE)
