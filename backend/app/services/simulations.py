"""Use case: store a simulation of consumption of a customer, with its calculation."""

from collections.abc import Callable
from datetime import datetime

from app.domain.simulations import NewSimulation, Simulation
from app.repositories.simulations import SimulationRepository
from app.services.customers import TIMESTAMP_FORMAT
from app.services.pricing import PricingService


class SimulationService:
    def __init__(
        self,
        pricing: PricingService,
        simulations: SimulationRepository,
        utc_now: Callable[[], datetime],
    ) -> None:
        self._pricing = pricing
        self._simulations = simulations
        # The clock comes from outside, as in the customers: a test can fix it.
        self._utc_now = utc_now

    def register(
        self, customer_id: int, active_users: int, storage_gb: int, estimated_api_calls: int
    ) -> Simulation:
        """Calculate and store. Storage and API calls are kept and change no amount (A3).

        The amounts come from the same use case that answers `POST /pricing/quote`, so
        there is one calculation and one way of finding the customer (SPEC-03/E-02).
        """
        quote = self._pricing.quote(customer_id, active_users)
        new = NewSimulation(customer_id, storage_gb, estimated_api_calls, quote)
        return self._simulations.add(new, self._utc_now().strftime(TIMESTAMP_FORMAT))
