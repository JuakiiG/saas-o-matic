"""A simulation of consumption: what was asked and what was calculated (SPEC-03, 2.1 and 2.2).

Storage and API calls are validated and stored, and take no part in any amount (A3).
The amounts are the complete result of the one calculation of the system (SPEC-02).
"""

from dataclasses import dataclass

from app.domain.pricing import Quote

MAX_STORAGE_GB = 1_000_000
MAX_ESTIMATED_API_CALLS = 1_000_000_000


@dataclass(frozen=True)
class NewSimulation:
    """A simulation ready to be stored. `quote` carries the users, the country and the amounts."""

    customer_id: int
    storage_gb: int
    estimated_api_calls: int
    quote: Quote


@dataclass(frozen=True)
class Simulation:
    """A stored simulation. `created_at` is UTC, ISO 8601, to the second.

    `quote` is what was calculated when it was stored: it is never calculated again.
    """

    id: int
    customer_id: int
    storage_gb: int
    estimated_api_calls: int
    quote: Quote
    created_at: str
