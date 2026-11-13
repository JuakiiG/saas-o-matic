"""`POST /simulations`: store a simulation with its calculation (SPEC-03, 4.1)."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict, Field

from app.api.identifiers import BodyId
from app.api.pricing import QuoteResponse, TierChargeResponse
from app.api.problems import problem_responses
from app.domain.pricing import MAX_ACTIVE_USERS
from app.domain.simulations import MAX_ESTIMATED_API_CALLS, MAX_STORAGE_GB, Simulation
from app.services.simulations import SimulationService

router = APIRouter()


class SimulationRequest(BaseModel):
    # Strict integers, as in the quote. No amount, rate or country can come in the request:
    # any other field is rejected.
    model_config = ConfigDict(extra="forbid")

    customer_id: BodyId
    active_users: Annotated[int, Field(strict=True, ge=0, le=MAX_ACTIVE_USERS)]
    storage_gb: Annotated[int, Field(strict=True, ge=0, le=MAX_STORAGE_GB)]
    estimated_api_calls: Annotated[int, Field(strict=True, ge=0, le=MAX_ESTIMATED_API_CALLS)]


class SimulationResponse(BaseModel):
    # The fields of the calculation are exactly those of `QuoteResponse`, in its order.
    id: int
    customer_id: int
    active_users: int
    storage_gb: int
    estimated_api_calls: int
    currency: Literal["EUR"]
    tiers: list[TierChargeResponse]
    base_cents: int
    country: str
    tax_rate_bp: int
    tax_cents: int
    total_cents: int
    created_at: str


def simulation_response(simulation: Simulation) -> SimulationResponse:
    """The simulation as the API shows it: its calculation goes through the model of the quote."""
    quote = QuoteResponse.model_validate(simulation.quote)
    return SimulationResponse(
        id=simulation.id,
        customer_id=simulation.customer_id,
        storage_gb=simulation.storage_gb,
        estimated_api_calls=simulation.estimated_api_calls,
        created_at=simulation.created_at,
        **quote.model_dump(),
    )


def get_simulation_service(request: Request) -> SimulationService:
    """The service built for this application in the composition root."""
    service: SimulationService = request.app.state.simulation_service
    return service


@router.post(
    "/simulations",
    status_code=201,
    response_model=SimulationResponse,
    responses=problem_responses(
        {
            404: "No existe un cliente con ese `customer_id`",
            422: "La petición no es válida",
            500: "El país del cliente guardado no tiene tipo impositivo",
            503: "La base de datos no responde",
        }
    ),
)
def create_simulation(
    payload: SimulationRequest,
    service: Annotated[SimulationService, Depends(get_simulation_service)],
) -> SimulationResponse:
    simulation = service.register(
        payload.customer_id, payload.active_users, payload.storage_gb, payload.estimated_api_calls
    )
    return simulation_response(simulation)
