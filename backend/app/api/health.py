"""`GET /health`: the backend is up and its database answers (SPEC-03, 4.4)."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.api.problems import problem_responses
from app.services.health import HealthService

router = APIRouter()


class HealthStatus(BaseModel):
    status: Literal["ok"]


def get_health_service(request: Request) -> HealthService:
    """The service built for this application in the composition root."""
    service: HealthService = request.app.state.health_service
    return service


@router.get(
    "/health",
    response_model=HealthStatus,
    responses=problem_responses({503: "La base de datos no responde"}),
)
def read_health(service: Annotated[HealthService, Depends(get_health_service)]) -> HealthStatus:
    service.check()
    return HealthStatus(status="ok")
