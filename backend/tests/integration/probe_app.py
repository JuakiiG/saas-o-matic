"""The real application plus a few probe routes.

The common machinery (generic errors, CORS) is specified for every endpoint, but
the business endpoints do not exist yet. These routes stand in for them: one
that accepts a JSON body, one with a declared query parameter and two that fail.
"""

from typing import Annotated

from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt

from app.main import create_app

INTERNAL_DETAIL = "detail that must stay inside the server"
# The largest INTEGER of SQLite: the maximum of every identifier of the contract.
MAX_ID = 9223372036854775807


class ProbeBody(BaseModel):
    name: str


class ProbeNumbers(BaseModel):
    """Integers validated as the contract asks: strict, bounded, no unknown fields."""

    model_config = ConfigDict(extra="forbid")

    id: Annotated[int, Field(strict=True, ge=1, le=MAX_ID)]
    count: Annotated[int, Field(strict=True, ge=0, le=100)]
    # Optional: only validated when the request carries it.
    floor: Annotated[int, Field(strict=True, ge=0)] = 0
    # Two types: a wrong value fails twice, once per type, in the same field.
    either: StrictInt | StrictBool = 0


probes = APIRouter()


@probes.post("/probe")
def accept_body(payload: ProbeBody) -> dict[str, str]:
    return {"name": payload.name}


@probes.post("/probe/numbers")
def accept_numbers(payload: ProbeNumbers) -> dict[str, int]:
    return {"id": payload.id, "count": payload.count}


@probes.get("/probe")
def read_with_declared_query(q: str | None = None) -> dict[str, str | None]:
    return {"q": q}


@probes.get("/probe/failure")
def fail_unexpectedly() -> None:
    raise RuntimeError(INTERNAL_DETAIL)


@probes.get("/probe/teapot")
def fail_with_an_undefined_status() -> None:
    raise HTTPException(status_code=418, detail=INTERNAL_DETAIL)


def create_probe_app() -> FastAPI:
    """Build the application exactly as in production and add the probe routes."""
    app = create_app()
    app.include_router(probes)
    return app
