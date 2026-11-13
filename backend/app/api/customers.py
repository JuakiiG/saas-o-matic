"""`POST /customers`: register a customer (SPEC-01, 4.1)."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from app.api.problems import problem_responses
from app.api.request_guard import received_json_object
from app.domain.customers import COUNTRY_CODES, MAX_TAX_ID_INPUT_LENGTH, PLAN_CODES
from app.services.customers import CustomerService

router = APIRouter()


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
