"""The stored simulations: a row with the calculation and three rows with its breakdown."""

from app.domain.pricing import TierCharge
from app.domain.simulations import NewSimulation, Simulation
from app.repositories.database import Database

INSERT_SIMULATION = (
    "INSERT INTO simulations (customer_id, active_users, storage_gb, estimated_api_calls,"
    " country, base_cents, tax_rate_bp, tax_cents, total_cents, created_at)"
    " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id"
)
INSERT_TIER = (
    "INSERT INTO simulation_tiers (simulation_id, position, from_users, to_users,"
    " unit_price_cents, users, subtotal_cents) VALUES (?, ?, ?, ?, ?, ?, ?)"
)
FIRST_POSITION = 1


def _simulation_values(new: NewSimulation, created_at: str) -> tuple[object, ...]:
    """The values of `INSERT_SIMULATION`, in the order of its columns."""
    quote = new.quote
    return (
        new.customer_id,
        quote.active_users,
        new.storage_gb,
        new.estimated_api_calls,
        quote.country,
        quote.base_cents,
        quote.tax_rate_bp,
        quote.tax_cents,
        quote.total_cents,
        created_at,
    )


def _tier_values(simulation_id: int, position: int, tier: TierCharge) -> tuple[object, ...]:
    """The values of `INSERT_TIER`, in the order of its columns."""
    return (
        simulation_id,
        position,
        tier.from_users,
        tier.to_users,
        tier.unit_price_cents,
        tier.users,
        tier.subtotal_cents,
    )


class SimulationRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def add(self, new: NewSimulation, created_at: str) -> Simulation:
        """Store the simulation and its tiers in one transaction: all the rows or none.

        The only commit is the last statement. If anything fails before it, the
        connection is closed with the transaction open and SQLite undoes it (SPEC-03/E-11).
        """
        with self._database.connection() as connection:
            inserted = connection.execute(INSERT_SIMULATION, _simulation_values(new, created_at))
            simulation_id: int = inserted.fetchone()[0]
            for position, tier in enumerate(new.quote.tiers, start=FIRST_POSITION):
                connection.execute(INSERT_TIER, _tier_values(simulation_id, position, tier))
            connection.commit()
        return Simulation(
            simulation_id,
            new.customer_id,
            new.storage_gb,
            new.estimated_api_calls,
            new.quote,
            created_at,
        )
