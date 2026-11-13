"""The customers: registering one, reading one and searching them.

SPEC-01 (4.1 to 4.3) and, for the history inside a customer, SPEC-03 (4.2).
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from app.api.identifiers import PathId
from app.api.problems import problem_responses
from app.api.request_guard import received_json_object
from app.api.simulations import SimulationResponse, simulation_response
from app.domain.customers import (
    COUNTRY_CODES,
    MAX_SEARCH_TEXT_LENGTH,
    MAX_TAX_ID_INPUT_LENGTH,
    PLAN_CODES,
)
from app.domain.simulations import CustomerProfile
from app.services.customers import CustomerService

router = APIRouter()
# Every operation here reads or writes the database, and declares what it answers without it.
UNAVAILABLE = "La base de datos no responde"


class CustomerRequest(BaseModel):
    # Documents the contract in the OpenAPI and validates nothing: the domain does (ADR-009).
    # It only publishes limits that the code applies exactly so to the value received: the
    # lengths of the name and of the email are measured after trimming, and are not here.
    model_config = ConfigDict(extra="forbid")

    company_name: str
    tax_id: Annotated[str, Field(max_length=MAX_TAX_ID_INPUT_LENGTH)]
    contact_email: str
    country: Annotated[str, Field(json_schema_extra={"enum": list(COUNTRY_CODES)})]
    plan: Annotated[str, Field(json_schema_extra={"enum": list(PLAN_CODES)})]


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_name: str
    tax_id: str
    contact_email: str
    country: str
    plan: str
    created_at: str


class CustomerProfileResponse(CustomerResponse):
    # The customer and its history: the total, and the simulations stored last (SPEC-03, 4.2).
    simulation_count: int
    simulations: list[SimulationResponse]


def profile_response(profile: CustomerProfile) -> CustomerProfileResponse:
    """The profile as the API shows it: each simulation exactly as its creation answered it."""
    customer = CustomerResponse.model_validate(profile.customer)
    return CustomerProfileResponse(
        **customer.model_dump(),
        simulation_count=profile.history.simulation_count,
        simulations=[simulation_response(stored) for stored in profile.history.simulations],
    )


class CustomerItem(BaseModel):
    # A customer in a list: without the email and the date (SPEC-01, 4.3).
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_name: str
    tax_id: str
    country: str
    plan: str


class CustomerListResponse(BaseModel):
    items: list[CustomerItem]


REQUEST_BODY = {
    "required": True,
    "content": {"application/json": {"schema": CustomerRequest.model_json_schema()}},
}


def get_customer_service(request: Request) -> CustomerService:
    """The service built for this application in the composition root."""
    service: CustomerService = request.app.state.customer_service
    return service


@router.post(
    "/customers",
    status_code=201,
    response_model=CustomerResponse,
    responses=problem_responses(
        {
            409: "Ya hay un cliente con ese país e identificador normalizado",
            422: "La petición no es válida",
            503: UNAVAILABLE,
        }
    ),
    openapi_extra={"requestBody": REQUEST_BODY},
)
def create_customer(
    received: Annotated[dict[str, object], Depends(received_json_object)],
    service: Annotated[CustomerService, Depends(get_customer_service)],
    response: Response,
) -> CustomerResponse:
    customer = service.register(received)
    response.headers["Location"] = f"/customers/{customer.id}"
    return CustomerResponse.model_validate(customer)


@router.get(
    "/customers/{id}",
    response_model=CustomerProfileResponse,
    responses=problem_responses(
        {
            404: "No existe un cliente con ese `id`",
            422: "El `id` no es un entero de 1 a 9223372036854775807",
            503: UNAVAILABLE,
        }
    ),
)
def read_customer(
    customer_id: PathId, service: Annotated[CustomerService, Depends(get_customer_service)]
) -> CustomerProfileResponse:
    return profile_response(service.get(customer_id))


@router.get(
    "/customers",
    response_model=CustomerListResponse,
    responses=problem_responses(
        {422: "`q` es demasiado largo o hay un parámetro desconocido", 503: UNAVAILABLE}
    ),
)
def search_customers(
    service: Annotated[CustomerService, Depends(get_customer_service)],
    # The length is measured on what is received: the service trims it afterwards.
    q: Annotated[str | None, Query(max_length=MAX_SEARCH_TEXT_LENGTH)] = None,
) -> CustomerListResponse:
    items = [CustomerItem.model_validate(customer) for customer in service.search(q)]
    return CustomerListResponse(items=items)
