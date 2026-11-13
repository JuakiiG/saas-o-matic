"""Every problem of the domain has its code and its message in the contract (SPEC-01, 4.1)."""

import pytest

from app.api.customer_errors import customer_field_errors
from app.api.problems import FieldCode
from app.domain.customers import FieldProblem

# The field codes that 4.1 lists for `POST /customers`.
CONTRACT_CODES = {
    *("missing", "not_a_string", "too_short", "too_long", "invalid_characters", "invalid_email"),
    *("unsupported_country", "unsupported_plan", "invalid_tax_id_format"),
    *("invalid_tax_id_check_character", "unknown_field"),
}
FIELDS_WITH_A_MAXIMUM = ["company_name", "tax_id", "contact_email"]


# Written after the code that it tests (session 04, Y-12): it was never seen failing.
def test_problems_of_the_domain_are_exactly_the_codes_of_the_contract() -> None:
    """SPEC-01/E-07, SPEC-01/E-35: no problem without a code and no code that is never used."""
    assert {problem.value for problem in FieldProblem} == CONTRACT_CODES
    assert {code.value for code in FieldCode} >= CONTRACT_CODES


# Written after the code that it tests (session 04, Y-12): it was never seen failing.
@pytest.mark.parametrize("problem", [p for p in FieldProblem if p is not FieldProblem.TOO_LONG])
def test_problem_becomes_an_error_with_its_code_and_a_message(problem: FieldProblem) -> None:
    """SPEC-01/E-35: the code of the contract and a text to show, whatever the field."""
    (error,) = customer_field_errors((("plan", problem),))
    assert (error.field, error.code.value) == ("plan", problem.value)
    assert error.message.endswith(".")


# Written after the code that it tests (session 04, Y-12): it was never seen failing.
@pytest.mark.parametrize("field", FIELDS_WITH_A_MAXIMUM)
def test_too_long_tells_the_maximum_of_its_own_field(field: str) -> None:
    """SPEC-01/E-03, SPEC-01/E-04, SPEC-01/E-34: each field has its own maximum length."""
    (error,) = customer_field_errors(((field, FieldProblem.TOO_LONG),))
    maximum = {"company_name": "120", "tax_id": "30", "contact_email": "254"}[field]
    assert error.code.value == "too_long"
    assert maximum in error.message
