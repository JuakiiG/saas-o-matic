"""Composition root: builds the FastAPI application.

Run it from this folder with `uv run uvicorn --factory app.main:create_app`.
"""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.error_handling import install_error_handling
from app.api.request_guard import RequestBodyGuard, reject_undocumented_query_parameters
from app.config import load_settings

API_TITLE = "SaaS-O-Matic API"
# What the frontend needs and nothing else (SPEC-03, 2.7).
CORS_METHODS = ["GET", "POST"]
CORS_HEADERS = ["Content-Type"]


def create_app() -> FastAPI:
    """Build a new application.

    A factory instead of a module-level instance: nothing is created on import,
    and every test gets an application of its own.
    """
    settings = load_settings()
    app = FastAPI(title=API_TITLE, dependencies=[Depends(reject_undocumented_query_parameters)])
    # The middleware added last is the outermost. CORS goes outside the guards so that
    # every response, error or not, leaves with its headers (SPEC-03/E-24).
    app.add_middleware(RequestBodyGuard)
    install_error_handling(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_methods=CORS_METHODS,
        allow_headers=CORS_HEADERS,
    )
    return app
