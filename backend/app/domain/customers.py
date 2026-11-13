"""A new customer: the fields received, their validation and what is stored (SPEC-01).

The validation is written by hand and not with a schema library (ADR-009): the spec
fixes the order of the checks of each field and makes the identifier depend on the
country (2.12). Each check returns the valid value or the first problem it finds.
"""

import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

from app.domain.countries import COUNTRIES
from app.domain.tax_id import TaxIdProblem, normalize_tax_id, tax_id_problem

# The fields of the contract, in its order: also the order of the errors.
CUSTOMER_FIELDS = ("company_name", "tax_id", "contact_email", "country", "plan")
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 120
# Measured on what is received, before normalizing.
MAX_TAX_ID_INPUT_LENGTH = 30
MAX_EMAIL_LENGTH = 254
# Measured on what is received, before trimming.
MAX_SEARCH_TEXT_LENGTH = 100
MAX_SEARCH_RESULTS = 20
# The only character that is trimmed: a tab or a line break at an end is not.
SPACE = " "
# U+0000. A search text that holds it matches no customer (2.10).
NUL = "\x00"
# Unicode categories never admitted: control and invisible format characters.
FORBIDDEN_CATEGORIES = ("Cc", "Cf")
# Unicode categories of the separators: spaces (U+0020 among them), lines and paragraphs.
SEPARATOR_CATEGORIES = ("Zs", "Zl", "Zp")
DIACRITICAL_MARK = "Mn"


@dataclass(frozen=True)
class Plan:
    code: str
    name: str


# Informative: the plan has no effect on the price (A2).
PLANS: tuple[Plan, ...] = (
    Plan("starter", "Básico"),
    Plan("professional", "Profesional"),
    Plan("enterprise", "Empresa"),
)
COUNTRY_CODES = tuple(country.code for country in COUNTRIES)
PLAN_CODES = tuple(plan.code for plan in PLANS)


class FieldProblem(Enum):
    """Why a field of a new customer is not valid. One per field: the first that fails."""

    MISSING = "missing"
    NOT_A_STRING = "not_a_string"
    INVALID_CHARACTERS = "invalid_characters"
    TOO_SHORT = "too_short"
    TOO_LONG = "too_long"
    INVALID_EMAIL = "invalid_email"
    UNSUPPORTED_COUNTRY = "unsupported_country"
    UNSUPPORTED_PLAN = "unsupported_plan"
    INVALID_TAX_ID_FORMAT = "invalid_tax_id_format"
    INVALID_TAX_ID_CHECK_CHARACTER = "invalid_tax_id_check_character"
    UNKNOWN_FIELD = "unknown_field"


TAX_ID_PROBLEMS = {
    TaxIdProblem.FORMAT: FieldProblem.INVALID_TAX_ID_FORMAT,
    TaxIdProblem.CHECK_CHARACTER: FieldProblem.INVALID_TAX_ID_CHECK_CHARACTER,
}


@dataclass(frozen=True)
class NewCustomer:
    """A customer that passed the validation, as it is stored."""

    company_name: str
    company_name_search: str
    tax_id: str
    contact_email: str
    country: str
    plan: str


@dataclass(frozen=True)
class Customer:
    """A stored customer, as the API shows it. `created_at` is UTC, ISO 8601, to the second."""

    id: int
    company_name: str
    tax_id: str
    contact_email: str
    country: str
    plan: str
    created_at: str


class InvalidCustomerError(Exception):
    """The fields received do not make a valid customer."""

    def __init__(self, problems: tuple[tuple[str, FieldProblem], ...]) -> None:
        super().__init__(", ".join(field for field, _ in problems))
        self.problems = problems


@dataclass(frozen=True)
class CustomerSearch:
    """What a search text is compared with: the names and the tax identifiers.

    `None` is nothing to compare with: no customer matches by that form. It is decided
    here and not in the statement that searches (SPEC-01, 2.10 and 2.11).
    """

    name: str | None
    tax_id: str | None


def customer_search(text: str | None) -> CustomerSearch:
    """The two forms of a search text. No text, or only spaces, is the empty search (2.10)."""
    trimmed = (text or "").strip(SPACE)
    if NUL in trimmed:
        # No stored name (it is Cc) or identifier (it is not 0-9 or A-Z) can hold it.
        return CustomerSearch(None, None)
    # An empty identifier would be inside every stored one: the text had nothing of one.
    return CustomerSearch(search_form(trimmed), normalize_tax_id(trimmed) or None)


def search_form(text: str) -> str:
    """How a name is compared and sorted: neither case nor accents tell names apart (D-08)."""
    decomposed = unicodedata.normalize("NFD", text)
    unmarked = (char for char in decomposed if unicodedata.category(char) != DIACRITICAL_MARK)
    return "".join(unmarked).casefold()


def validate_new_customer(received: Mapping[str, object]) -> NewCustomer:
    """The customer to store, or `InvalidCustomerError` with one problem per field.

    The problems come in the order of the contract and then the fields that are not in
    it, by name.
    """
    country = _one_of(received, "country", COUNTRY_CODES, FieldProblem.UNSUPPORTED_COUNTRY)
    checked = {
        "company_name": _company_name(received),
        "tax_id": _tax_id(received, country),
        "contact_email": _contact_email(received),
        "country": country,
        "plan": _one_of(received, "plan", PLAN_CODES, FieldProblem.UNSUPPORTED_PLAN),
    }
    problems = [(name, value) for name, value in checked.items() if isinstance(value, FieldProblem)]
    unknown = sorted(set(received) - set(checked))
    problems += [(name, FieldProblem.UNKNOWN_FIELD) for name in unknown]
    if problems:
        raise InvalidCustomerError(tuple(problems))
    values = {name: str(value) for name, value in checked.items()}
    return NewCustomer(company_name_search=search_form(values["company_name"]), **values)


def _text(received: Mapping[str, object], field: str) -> str | FieldProblem:
    """The first two checks of every field: it is there and it is a string."""
    if field not in received:
        return FieldProblem.MISSING
    value = received[field]
    return value if isinstance(value, str) else FieldProblem.NOT_A_STRING


def _company_name(received: Mapping[str, object]) -> str | FieldProblem:
    value = _text(received, "company_name")
    if isinstance(value, FieldProblem):
        return value
    name = value.strip(SPACE)
    if _has_forbidden_characters(name):
        return FieldProblem.INVALID_CHARACTERS
    if len(name) < MIN_NAME_LENGTH:
        return FieldProblem.TOO_SHORT
    return FieldProblem.TOO_LONG if len(name) > MAX_NAME_LENGTH else name


def _contact_email(received: Mapping[str, object]) -> str | FieldProblem:
    value = _text(received, "contact_email")
    if isinstance(value, FieldProblem):
        return value
    email = value.strip(SPACE)
    if _has_forbidden_characters(email):
        return FieldProblem.INVALID_CHARACTERS
    if len(email) > MAX_EMAIL_LENGTH:
        return FieldProblem.TOO_LONG
    return email if _has_email_form(email) else FieldProblem.INVALID_EMAIL


def _has_email_form(email: str) -> bool:
    """One `@`, text before it and a domain with a dot that is not at either end.

    And no separator of any kind: a no-break space pasted along with the address is
    not U+0020, and an address stored with it is of no use.
    """
    local, _, domain = email.partition("@")
    one_at = email.count("@") == 1
    dotted = "." in domain and not domain.startswith(".") and not domain.endswith(".")
    return one_at and bool(local) and dotted and not _has_category(email, SEPARATOR_CATEGORIES)


def _one_of(
    received: Mapping[str, object], field: str, admitted: tuple[str, ...], problem: FieldProblem
) -> str | FieldProblem:
    """A code of a closed list, written exactly as in the list."""
    value = _text(received, field)
    if isinstance(value, FieldProblem):
        return value
    return value if value in admitted else problem


def _tax_id(received: Mapping[str, object], country: str | FieldProblem) -> str | FieldProblem:
    """The normalized identifier. Without a valid country, only what does not depend on it."""
    value = _text(received, "tax_id")
    if isinstance(value, FieldProblem):
        return value
    if len(value) > MAX_TAX_ID_INPUT_LENGTH:
        return FieldProblem.TOO_LONG
    normalized = normalize_tax_id(value)
    if isinstance(country, FieldProblem):
        return normalized
    problem = tax_id_problem(country, normalized)
    return normalized if problem is None else TAX_ID_PROBLEMS[problem]


def _has_forbidden_characters(text: str) -> bool:
    return _has_category(text, FORBIDDEN_CATEGORIES)


def _has_category(text: str, categories: tuple[str, ...]) -> bool:
    """Whether any character of the text is of one of those Unicode categories."""
    return any(unicodedata.category(character) in categories for character in text)
