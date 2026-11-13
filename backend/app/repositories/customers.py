"""The stored customers."""

import sqlite3

from app.domain.customers import Customer, NewCustomer
from app.repositories.database import Database

INSERT_CUSTOMER = (
    "INSERT INTO customers (company_name, company_name_search, tax_id, contact_email, country,"
    " plan, created_at) VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING id"
)
# What SQLite calls the violation of a UNIQUE constraint; any other one is not a duplicate.
UNIQUE_VIOLATION = "SQLITE_CONSTRAINT_UNIQUE"


class DuplicateCustomerError(Exception):
    """There is already a customer with that country and tax identifier."""


class CustomerRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def add(self, new: NewCustomer, created_at: str) -> Customer:
        """Store a customer. The UNIQUE constraint decides what a duplicate is, not a query."""
        values = (
            new.company_name,
            new.company_name_search,
            new.tax_id,
            new.contact_email,
            new.country,
            new.plan,
            created_at,
        )
        try:
            with self._database.connection() as connection:
                customer_id: int = connection.execute(INSERT_CUSTOMER, values).fetchone()[0]
                connection.commit()
        except sqlite3.IntegrityError as error:
            if error.sqlite_errorname == UNIQUE_VIOLATION:
                raise DuplicateCustomerError(new.country) from error
            raise
        return Customer(
            customer_id,
            new.company_name,
            new.tax_id,
            new.contact_email,
            new.country,
            new.plan,
            created_at,
        )

    def country_of(self, customer_id: int) -> str | None:
        """Country of the customer, or None if there is no customer with that id."""
        with self._database.connection() as connection:
            row = connection.execute(
                "SELECT country FROM customers WHERE id = ?", (customer_id,)
            ).fetchone()
        if row is None:
            return None
        country: str = row[0]
        return country
