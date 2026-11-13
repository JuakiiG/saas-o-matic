"""Use cases of the customers: registering one, reading one and searching them."""

from collections.abc import Callable, Mapping
from datetime import datetime

from app.domain.customers import (
    MAX_SEARCH_RESULTS,
    Customer,
    customer_search,
    validate_new_customer,
)
from app.domain.simulations import MAX_HISTORY_SIMULATIONS, CustomerProfile
from app.repositories.customers import CustomerRepository, DuplicateCustomerError
from app.repositories.simulations import SimulationRepository

# UTC, ISO 8601, to the second (index of specs, "Fechas con hora").
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class CustomerAlreadyExistsError(Exception):
    """There is already a customer with that country and normalized tax identifier."""


class CustomerNotFoundError(Exception):
    """There is no customer with that id."""


class CustomerService:
    def __init__(
        self,
        customers: CustomerRepository,
        simulations: SimulationRepository,
        utc_now: Callable[[], datetime],
    ) -> None:
        self._customers = customers
        self._simulations = simulations
        # The clock comes from outside: the domain never reads it and a test can fix it.
        self._utc_now = utc_now

    def register(self, received: Mapping[str, object]) -> Customer:
        """Validate what was received and store the customer.

        Validation goes first: an invalid duplicate is an invalid customer (SPEC-01/E-21).
        """
        new = validate_new_customer(received)
        created_at = self._utc_now().strftime(TIMESTAMP_FORMAT)
        try:
            return self._customers.add(new, created_at)
        except DuplicateCustomerError as error:
            raise CustomerAlreadyExistsError(new.country) from error

    def get(self, customer_id: int) -> CustomerProfile:
        """The stored customer with that id and its last simulations (SPEC-01/E-22, E-23)."""
        customer = self._customers.find(customer_id)
        if customer is None:
            raise CustomerNotFoundError(customer_id)
        history = self._simulations.history(customer_id, MAX_HISTORY_SIMULATIONS)
        return CustomerProfile(customer, history)

    def search(self, text: str | None) -> list[Customer]:
        """The first customers by name that the text matches; without text, the first ones."""
        return self._customers.search(customer_search(text), MAX_SEARCH_RESULTS)
