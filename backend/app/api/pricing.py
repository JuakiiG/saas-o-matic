"""`POST /pricing/quote`: the calculation for a customer, without storing it (SPEC-02, 4)."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict, Field

from app.api.problems import problem_responses
from app.domain.pricing import MAX_ACTIVE_USERS
from app.services.pricing import PricingService

# The largest INTEGER of SQLite: the maximum of every identifier of the contract.
MAX_ID = 9223372036854775807

router = APIRouter()


class QuoteRequest(BaseModel):
    # Strict integers: `"15"`, `15.0`, `true` and `null` are rejected, not converted.
    # A comment and not a docstring: a docstring is published in the OpenAPI document.
    model_config = ConfigDict(extra="forbid")

    customer_id: Annotated[int, Field(strict=True, ge=1, le=MAX_ID)]
    active_users: Annotated[int, Field(strict=True, ge=0, le=MAX_ACTIVE_USERS)]


class TierChargeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    from_users: int
    to_users: int | None
    unit_price_cents: int
    users: int
    subtotal_cents: int


class QuoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    currency: Literal["EUR"] = "EUR"
    active_users: int
    tiers: list[TierChargeResponse]
    base_cents: int
    country: str
    tax_rate_bp: int
    tax_cents: int
    total_cents: int


def get_pricing_service(request: Request) -> PricingService:
    """The service built for this application in the composition root."""
    service: PricingService = request.app.state.pricing_service
    return service


@router.post(
    "/pricing/quote",
    response_model=QuoteResponse,
    responses=problem_responses(
        {
            404: "No existe un cliente con ese `customer_id`",
            422: "La petición no es válida",
            500: "El país del cliente guardado no tiene tipo impositivo",
            503: "La base de datos no responde",
        }
    ),
)
def quote_price(
    payload: QuoteRequest, service: Annotated[PricingService, Depends(get_pricing_service)]
) -> QuoteResponse:
    quote = service.quote(payload.customer_id, payload.active_users)
    return QuoteResponse.model_validate(quote)
