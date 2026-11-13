"""The problems that the domain finds in a new customer, as errors of the contract."""

from app.api.problems import FieldCode, FieldError
from app.domain.customers import (
    MAX_EMAIL_LENGTH,
    MAX_NAME_LENGTH,
    MAX_TAX_ID_INPUT_LENGTH,
    MIN_NAME_LENGTH,
    FieldProblem,
)

NAME_LENGTH = f"Debe tener entre {MIN_NAME_LENGTH} y {MAX_NAME_LENGTH} caracteres."
# Fixed texts: the two of the identifier never change with the value received, so that
# an error cannot tell which the right check character is (SPEC-01/E-17).
MESSAGES = {
    FieldProblem.MISSING: "Campo obligatorio.",
    FieldProblem.NOT_A_STRING: "Debe ser un texto.",
    FieldProblem.INVALID_CHARACTERS: "Contiene caracteres no admitidos.",
    FieldProblem.TOO_SHORT: NAME_LENGTH,
    FieldProblem.INVALID_EMAIL: "El email no tiene un formato válido.",
    FieldProblem.UNSUPPORTED_COUNTRY: "País no admitido.",
    FieldProblem.UNSUPPORTED_PLAN: "Plan no admitido.",
    FieldProblem.INVALID_TAX_ID_FORMAT: "El identificador fiscal no tiene un formato válido.",
    FieldProblem.INVALID_TAX_ID_CHECK_CHARACTER: (
        "El carácter de control del identificador fiscal no es correcto."
    ),
    FieldProblem.UNKNOWN_FIELD: "Campo no documentado.",
}
# The only problem whose text depends on the field: each one has its own maximum.
TOO_LONG_MESSAGES = {
    "company_name": NAME_LENGTH,
    "tax_id": f"Debe tener {MAX_TAX_ID_INPUT_LENGTH} caracteres como máximo.",
    "contact_email": f"Debe tener {MAX_EMAIL_LENGTH} caracteres como máximo.",
}


def customer_field_errors(problems: tuple[tuple[str, FieldProblem], ...]) -> tuple[FieldError, ...]:
    """One error of the contract per problem, in the order the domain gives them."""
    return tuple(_field_error(field, problem) for field, problem in problems)


def _field_error(field: str, problem: FieldProblem) -> FieldError:
    message = TOO_LONG_MESSAGES[field] if problem is FieldProblem.TOO_LONG else MESSAGES[problem]
    # The codes of the domain and of the contract are the same words; a test checks them all.
    return FieldError(field, FieldCode(problem.value), message)
