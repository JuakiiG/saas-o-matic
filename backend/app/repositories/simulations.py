"""The stored simulations: a row with the calculation and three rows with its breakdown."""

import sqlite3
from itertools import groupby
from typing import NamedTuple

from app.domain.pricing import Quote, TierCharge
from app.domain.simulations import NewSimulation, Simulation, SimulationHistory
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
BEGIN = "BEGIN"
COUNT_SIMULATIONS = "SELECT count(*) FROM simulations WHERE customer_id = ?"
# One row per tier, the simulation repeated in each. LEFT JOIN, so that a simulation without
# tiers (only a direct insertion can leave one) is still listed, as the total counts it.
SELECT_HISTORY = (
    "SELECT s.id, s.customer_id, s.active_users, s.storage_gb, s.estimated_api_calls,"
    " s.country, s.base_cents, s.tax_rate_bp, s.tax_cents, s.total_cents, s.created_at,"
    " t.position, t.from_users, t.to_users, t.unit_price_cents, t.users, t.subtotal_cents"
    " FROM simulations AS s LEFT JOIN simulation_tiers AS t ON t.simulation_id = s.id"
    " WHERE s.id IN (SELECT id FROM simulations WHERE customer_id = ? ORDER BY id DESC LIMIT ?)"
    " ORDER BY s.id DESC, t.position"
)
# Where the columns of the tier start in a row of `SELECT_HISTORY`: at its position.
TIER_POSITION = 11


class SimulationColumns(NamedTuple):
    """The columns of a simulation in a row of `SELECT_HISTORY`, in the order it selects them.

    The types are the ones that the STRICT tables guarantee for each column.
    """

    id: int
    customer_id: int
    active_users: int
    storage_gb: int
    estimated_api_calls: int
    country: str
    base_cents: int
    tax_rate_bp: int
    tax_cents: int
    total_cents: int
    created_at: str


class HistoryRow(NamedTuple):
    """A row of `SELECT_HISTORY`: a simulation and one of its tiers, or none (LEFT JOIN)."""

    simulation: SimulationColumns
    tier: TierCharge | None


def _history_rows(cursor: sqlite3.Cursor) -> list[HistoryRow]:
    """Every row of `SELECT_HISTORY`, typed here, where it leaves the database untyped."""
    return [
        HistoryRow(
            SimulationColumns(*row[:TIER_POSITION]),
            None if row[TIER_POSITION] is None else TierCharge(*row[TIER_POSITION + 1 :]),
        )
        for row in cursor.fetchall()
    ]


def _stored_simulation(rows: list[HistoryRow]) -> Simulation:
    """A simulation from its rows of `SELECT_HISTORY`, with the amounts exactly as stored."""
    stored = rows[0].simulation
    tiers = tuple(row.tier for row in rows if row.tier is not None)
    quote = Quote(
        stored.active_users,
        tiers,
        stored.base_cents,
        stored.country,
        stored.tax_rate_bp,
        stored.tax_cents,
        stored.total_cents,
    )
    return Simulation(
        stored.id,
        stored.customer_id,
        stored.storage_gb,
        stored.estimated_api_calls,
        quote,
        stored.created_at,
    )


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

    def history(self, customer_id: int, limit: int) -> SimulationHistory:
        """The simulations of a customer stored last, and how many it has in all.

        Everything comes from what was stored with each simulation: nothing is
        calculated again and the customer is not read (SPEC-03/E-16).
        """
        with self._database.connection() as connection:
            # One read transaction: the total and the list are of the same moment.
            connection.execute(BEGIN)
            count: int = connection.execute(COUNT_SIMULATIONS, (customer_id,)).fetchone()[0]
            rows = _history_rows(connection.execute(SELECT_HISTORY, (customer_id, limit)))
        by_simulation = groupby(rows, key=lambda row: row.simulation.id)
        simulations = tuple(_stored_simulation(list(group)) for _, group in by_simulation)
        return SimulationHistory(count, simulations)
