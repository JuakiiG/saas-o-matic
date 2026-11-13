"""Read access to the stored customers."""

from contextlib import closing

from app.repositories.database import Database


class CustomerRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def country_of(self, customer_id: int) -> str | None:
        """Country of the customer, or None if there is no customer with that id."""
        with closing(self._database.connect()) as connection:
            row = connection.execute(
                "SELECT country FROM customers WHERE id = ?", (customer_id,)
            ).fetchone()
        if row is None:
            return None
        country: str = row[0]
        return country
