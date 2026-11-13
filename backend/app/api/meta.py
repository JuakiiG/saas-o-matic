"""`GET /meta`: what the forms need to offer (SPEC-01, 4.4)."""

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from app.domain.countries import COUNTRIES
from app.domain.customers import PLANS

router = APIRouter()


class CountryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    name: str
    tax_rate_bp: int


class PlanItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    name: str


class MetaResponse(BaseModel):
    countries: list[CountryItem]
    plans: list[PlanItem]


@router.get("/meta", response_model=MetaResponse)
def read_meta() -> MetaResponse:
    """The same constants that the validation and the calculation use, in their order."""
    return MetaResponse(
        countries=[CountryItem.model_validate(country) for country in COUNTRIES],
        plans=[PlanItem.model_validate(plan) for plan in PLANS],
    )
