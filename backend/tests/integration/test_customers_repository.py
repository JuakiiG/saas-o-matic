"""The repository of customers against a real database (SPEC-01, 2.9)."""

import sqlite3
from pathlib import Path
from typing import cast

import pytest

from app.domain.customers import Customer, NewCustomer
from app.repositories.customers import CustomerRepository, DuplicateCustomerError
from app.repositories.database import Database

CREATED_AT = "2026-11-13T10:00:00Z"
NEW = NewCustomer(
    company_name="Ejemplo Uno SL",
    company_name_search="ejemplo uno sl",
    tax_id="B12345674",
    contact_email="compras@ejemplo-uno.example",
    country="ES",
    plan="professional",
)


@pytest.fixture
def repository(tmp_path: Path) -> CustomerRepository:
    database = Database(tmp_path / "repository.db")
    database.create_schema()
    return CustomerRepository(database)


# Written after the code that it tests (session 04, Y-12): it was never seen failing.
def test_added_customer_comes_back_with_its_id_and_its_date(repository: CustomerRepository) -> None:
    """SPEC-01/E-01: the stored customer, with the id that the database gave it."""
    assert repository.add(NEW, CREATED_AT) == Customer(
        id=1,
        company_name="Ejemplo Uno SL",
        tax_id="B12345674",
        contact_email="compras@ejemplo-uno.example",
        country="ES",
        plan="professional",
        created_at=CREATED_AT,
    )


# Written after the code that it tests (session 04, Y-12): it was never seen failing.
def test_second_customer_with_the_same_country_and_identifier_is_a_duplicate(
    repository: CustomerRepository,
) -> None:
    """SPEC-01/E-19: the UNIQUE constraint, and not a previous query, finds the duplicate."""
    repository.add(NEW, CREATED_AT)
    with pytest.raises(DuplicateCustomerError):
        repository.add(NEW, CREATED_AT)


# Written after the code that it tests (session 04, Y-12): it was never seen failing.
def test_integrity_error_that_is_not_a_duplicate_is_not_reported_as_one(
    repository: CustomerRepository,
) -> None:
    """SPEC-01/E-19: only the UNIQUE of country and identifier means "already exists"."""
    # A value that the types forbid, to make another constraint (NOT NULL) fail.
    without_plan = NewCustomer(**{**NEW.__dict__, "plan": cast(str, None)})
    with pytest.raises(sqlite3.IntegrityError):
        repository.add(without_plan, CREATED_AT)
