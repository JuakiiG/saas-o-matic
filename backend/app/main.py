"""Composition root: builds the FastAPI application.

Run it from this folder with `uv run uvicorn --factory app.main:create_app`.
"""

from fastapi import FastAPI

API_TITLE = "SaaS-O-Matic API"


def create_app() -> FastAPI:
    """Build a new application.

    A factory instead of a module-level instance: nothing is created on import,
    and every test gets an application of its own.
    """
    return FastAPI(title=API_TITLE)
