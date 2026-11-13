"""Use case: how much would a customer pay for a number of users? Nothing is stored."""

from app.domain.pricing import Quote, calculate_quote
from app.repositories.customers import CustomerRepository


class CustomerNotFoundError(Exception):
    """There is no customer with that id."""


class PricingService:
    def __init__(self, customers: CustomerRepository) -> None:
        self._customers = customers

    def quote(self, customer_id: int, active_users: int) -> Quote:
        """The quote with the tax rate of the country of the stored customer (SPEC-02/E-07)."""
        country = self._customers.country_of(customer_id)
        if country is None:
            raise CustomerNotFoundError(customer_id)
        return calculate_quote(active_users, country)
