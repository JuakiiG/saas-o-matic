"""Composition root: builds the FastAPI application.

Run it from this folder with `uv run uvicorn --factory app.main:create_app`.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health
from app.api.error_handling import install_error_handling
from app.api.request_guard import RequestBodyGuard, reject_undocumented_query_parameters
from app.config import load_settings
from app.repositories.database import Database
from app.services.health import HealthService

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
    database = Database(settings.database_path)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        # On startup, not when the application is built: building it touches no disk.
        database.create_schema()
        yield

    app = FastAPI(
        title=API_TITLE,
        lifespan=lifespan,
        dependencies=[Depends(reject_undocumented_query_parameters)],
    )
    # Built here and handed to the endpoints through `Depends`: no global state.
    app.state.health_service = HealthService(database)
    app.include_router(health.router)
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
