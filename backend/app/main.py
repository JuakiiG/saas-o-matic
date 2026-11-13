"""Composition root: builds the FastAPI application.

Run it from this folder with `uv run uvicorn --factory app.main:create_app`.
"""

from fastapi import Depends, FastAPI

from app.api.error_handling import install_error_handling
from app.api.request_guard import RequestBodyGuard, reject_undocumented_query_parameters

API_TITLE = "SaaS-O-Matic API"


def create_app() -> FastAPI:
    """Build a new application.

    A factory instead of a module-level instance: nothing is created on import,
    and every test gets an application of its own.
    """
    app = FastAPI(title=API_TITLE, dependencies=[Depends(reject_undocumented_query_parameters)])
    # The middleware added last is the outermost: the error guard wraps the body guard.
    app.add_middleware(RequestBodyGuard)
    install_error_handling(app)
    return app
