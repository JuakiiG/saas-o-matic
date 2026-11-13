"""The single place where errors become HTTP responses (`.claude/rules/backend.md`).

Nothing internal leaves the server: an unexpected error is logged here and the
client only gets `internal_error`.
"""

import logging

from fastapi import FastAPI, Request, Response
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.api.problems import (
    INTERNAL_ERROR,
    METHOD_NOT_ALLOWED,
    NOT_FOUND,
    SERVICE_UNAVAILABLE,
    ProblemError,
    problem_response,
)
from app.services.health import ServiceUnavailableError

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

    @app.exception_handler(HTTPException)
    async def handle_http_error(request: Request, error: HTTPException) -> Response:
        problem = HTTP_PROBLEMS.get(error.status_code)
        if problem is None:
            # An HTTP error that the contract does not define is a bug of ours, not of the caller.
            logger.error("HTTP error outside the contract: %s", error.status_code)
            return problem_response(INTERNAL_ERROR)
        return problem_response(problem, error.headers)

    @app.exception_handler(ServiceUnavailableError)
    async def handle_unavailable(request: Request, error: ServiceUnavailableError) -> Response:
        logger.error("Service unavailable: %s", error, exc_info=error)
        return problem_response(SERVICE_UNAVAILABLE)

    app.add_middleware(UnexpectedErrorGuard)
