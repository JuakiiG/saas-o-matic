"""Validation of a new customer in the domain (SPEC-01: 2.1, 2.10, 2.12 and table 5.7)."""

import pytest

from app.domain.customers import (
    CUSTOMER_FIELDS,
    PLANS,
    CustomerSearch,
    InvalidCustomerError,
    NewCustomer,
    customer_search,
    search_form,
    validate_new_customer,
)
from tests.customer_cases import (
    EXTRA_INVALID_ROWS,
    FIELDS,
    INVALID_ROWS,
    VALID_CUSTOMER,
    VALID_ROWS,
    customer_with,
)

# The names of 5.9 and their search form.
SEARCH_FORMS = [
    ("Zeta Datos SL", "zeta datos sl"),
    ("alfa Ejemplo SA", "alfa ejemplo sa"),
    ("Alfa Ejemplo SA", "alfa ejemplo sa"),
    ("Ñandú Pruebas SL", "nandu pruebas sl"),
    ("100% Ejemplo SL", "100% ejemplo sl"),
    ("Ejemplo_Uno SL", "ejemplo_uno sl"),
    ("José Pruebas SL", "jose pruebas sl"),
    ("JOSE", "jose"),
]


def problems_of(received: dict[str, object]) -> list[tuple[str, str]]:
    """The (field, problem) pairs that the domain finds; empty if the customer is valid."""
    try:
        validate_new_customer(received)
    except InvalidCustomerError as error:
        return [(field, problem.value) for field, problem in error.problems]
    return []


def test_valid_customer_is_returned_as_it_will_be_stored() -> None:
    """SPEC-01/E-01, SPEC-01/E-08, SPEC-01/E-33: the example of 4.1, trimmed and normalized."""
    received = customer_with({"company_name": "  Ejemplo Uno SL ", "tax_id": "b-1234567 4"})
    assert validate_new_customer(received) == NewCustomer(
        company_name="Ejemplo Uno SL",
        company_name_search="ejemplo uno sl",
        tax_id="B12345674",
        contact_email="compras@ejemplo-uno.example",
        country="ES",
        plan="professional",
    )


@pytest.mark.parametrize(("changes", "stored"), VALID_ROWS, ids=ascii)
def test_valid_field_is_accepted_and_stored_trimmed_or_normalized(
    changes: dict[str, object], stored: dict[str, str]
) -> None:
    """SPEC-01/E-02, SPEC-01/E-03, SPEC-01/E-04, SPEC-01/E-34: the valid rows of 5.7."""
    customer = validate_new_customer(customer_with(changes))
    assert {field: getattr(customer, field) for field in stored} == stored


@pytest.mark.parametrize(("changes", "expected"), INVALID_ROWS, ids=ascii)
def test_invalid_field_gives_its_first_problem_in_contract_order(
    changes: dict[str, object], expected: list[tuple[str, str]]
) -> None:
    """SPEC-01/E-03, SPEC-01/E-04, SPEC-01/E-05, SPEC-01/E-06, SPEC-01/E-07: rows of 5.7.

    Also SPEC-01/E-18, SPEC-01/E-34 and SPEC-01/E-35: country and identifier, one problem
    per field and the order of the contract.
    """
    assert problems_of(customer_with(changes)) == expected


@pytest.mark.parametrize(("changes", "expected"), EXTRA_INVALID_ROWS, ids=ascii)
def test_identifier_problems_and_the_order_of_every_field_at_once(
    changes: dict[str, object], expected: list[tuple[str, str]]
) -> None:
    """SPEC-01/E-15, SPEC-01/E-16, SPEC-01/E-35: format, check character and the order of 2.12."""
    assert problems_of(customer_with(changes)) == expected


def test_empty_object_misses_the_five_fields() -> None:
    """SPEC-01/E-07: nothing received is five missing fields, in the order of the contract."""
    assert problems_of({}) == [(field, "missing") for field in CUSTOMER_FIELDS]


def test_fields_of_the_contract_are_the_five_of_the_spec_in_its_order() -> None:
    """SPEC-01/E-35: the order of the fields is the order of the errors (2.12)."""
    assert list(CUSTOMER_FIELDS) == FIELDS
    assert problems_of(VALID_CUSTOMER) == []


@pytest.mark.parametrize(("name", "expected"), SEARCH_FORMS)
def test_search_form_ignores_case_and_accents(name: str, expected: str) -> None:
    """SPEC-01/E-33: NFD, no diacritical marks and `casefold`, for every name of 5.9 (CA-18)."""
    assert search_form(name) == expected


# Written after the code that it tests (session 04, r4): it was never seen failing.
@pytest.mark.parametrize(
    ("text", "name", "tax_id"),
    [
        ("JOSÉ", "jose", "JOSÉ"),
        ("  ñandú ", "nandu", "ñANDú"),
        ("b-12345", "b-12345", "B12345"),
        ("b.1234", "b.1234", "B1234"),
        ("Alfa Uno", "alfa uno", "ALFAUNO"),
        ("100%_\\", "100%_\\", "100%_\\"),
        # Session 05 (H-11): an identifier that is left empty is none to compare with, and
        # it is the domain that says so. These four rows expected `""` until then.
        ("- .", "- .", None),
        ("\t", "\t", "\t"),
        ("", "", None),
        ("   ", "", None),
        (None, "", None),
        # Session 05 (H-05): no stored name or identifier can hold U+0000, wherever it is.
        ("\x00", None, None),
        ("a\x00", None, None),
        ("\x00a", None, None),
        (" b-1\x002 ", None, None),
    ],
    ids=ascii,
)
def test_customer_search_gives_the_two_forms_of_the_trimmed_text(
    text: str | None, name: str | None, tax_id: str | None
) -> None:
    """SPEC-01/E-25, SPEC-01/E-29: search form of the name and normalized identifier (2.10).

    `None` is nothing to compare with: no customer matches by that form.
    """
    assert customer_search(text) == CustomerSearch(name, tax_id)


def test_plans_are_the_three_of_the_spec_with_their_names() -> None:
    """SPEC-01/E-06, SPEC-01/E-32: the closed list of plans, with the names to show (D-04)."""
    assert [(plan.code, plan.name) for plan in PLANS] == [
        ("starter", "Básico"),
        ("professional", "Profesional"),
        ("enterprise", "Empresa"),
    ]
