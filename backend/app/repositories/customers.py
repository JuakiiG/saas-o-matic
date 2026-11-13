"""The stored customers."""

import sqlite3

from app.domain.customers import Customer, CustomerSearch, NewCustomer
from app.repositories.database import Database

INSERT_CUSTOMER = (
    "INSERT INTO customers (company_name, company_name_search, tax_id, contact_email, country,"
    " plan, created_at) VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING id"
)
# Both statements select the columns of a `Customer` in the order of its fields. The list
# is written twice because no statement is built by formatting strings, not even constants.
SELECT_CUSTOMER = (
    "SELECT id, company_name, tax_id, contact_email, country, plan, created_at"
    " FROM customers WHERE id = ?"
)
# An empty identifier would match every customer, so it is not compared: the text
# searched had nothing of an identifier (SPEC-01, 2.10).
SEARCH_CUSTOMERS = (
    "SELECT id, company_name, tax_id, contact_email, country, plan, created_at"
    " FROM customers"
    " WHERE company_name_search LIKE ? ESCAPE '\\'"
    " OR (? <> '' AND tax_id LIKE ? ESCAPE '\\')"
    " ORDER BY company_name_search, id LIMIT ?"
)
# What SQLite calls the violation of a UNIQUE constraint; any other one is not a duplicate.
UNIQUE_VIOLATION = "SQLITE_CONSTRAINT_UNIQUE"
LIKE_ESCAPE = "\\"
LIKE_WILDCARDS = ("%", "_")


class DuplicateCustomerError(Exception):
    """There is already a customer with that country and tax identifier."""


def _contains(text: str) -> str:
    """The LIKE pattern for "contains this text", with its wildcards taken literally."""
    # The escape character first: escaping it later would escape the escapes just added.
    literal = text.replace(LIKE_ESCAPE, LIKE_ESCAPE + LIKE_ESCAPE)
    for wildcard in LIKE_WILDCARDS:
        literal = literal.replace(wildcard, LIKE_ESCAPE + wildcard)
    return f"%{literal}%"


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

    def find(self, customer_id: int) -> Customer | None:
        """The customer with that id, or None if there is none."""
        with self._database.connection() as connection:
            row = connection.execute(SELECT_CUSTOMER, (customer_id,)).fetchone()
        return None if row is None else Customer(*row)

    def search(self, search: CustomerSearch, limit: int) -> list[Customer]:
        """The first customers by name whose name or tax identifier contains the text.

        One statement, and the text only in its parameters (SPEC-01/E-28).
        """
        parameters = (_contains(search.name), search.tax_id, _contains(search.tax_id), limit)
        with self._database.connection() as connection:
            rows = connection.execute(SEARCH_CUSTOMERS, parameters).fetchall()
        return [Customer(*row) for row in rows]

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
