"""Use cases of the customers: registering one."""

from collections.abc import Callable, Mapping
from datetime import datetime

from app.domain.customers import Customer, validate_new_customer
from app.repositories.customers import CustomerRepository, DuplicateCustomerError

# UTC, ISO 8601, to the second (index of specs, "Fechas con hora").
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class CustomerAlreadyExistsError(Exception):
    """There is already a customer with that country and normalized tax identifier."""


class CustomerService:
    def __init__(self, customers: CustomerRepository, utc_now: Callable[[], datetime]) -> None:
        self._customers = customers
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
