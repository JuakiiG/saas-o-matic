"""How a simulation is stored: all its rows or none, and its values only as parameters."""

import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from app.domain.pricing import Quote, calculate_quote
from app.domain.simulations import NewSimulation
from app.repositories.simulations import SimulationRepository
from tests.integration.test_customers_search_sql import RecordingDatabase
from tests.integration.test_pricing_quote import CUSTOMERS, INSERT_CUSTOMER
from tests.simulation_cases import with_wrong_subtotal

CREATED_AT = "2026-11-13T15:00:00Z"
# Values that appear nowhere else, so that finding them in a statement means something.
ACTIVE_USERS = 37
STORAGE_GB = 4321
ESTIMATED_API_CALLS = 987654
COUNT_SIMULATION_ROWS = [
    "SELECT count(*) FROM simulations",
    "SELECT count(*) FROM simulation_tiers",
]


@pytest.fixture
def database(tmp_path: Path) -> RecordingDatabase:
    """A database with the schema and the customers, that writes down what runs on it."""
    recording = RecordingDatabase(tmp_path / "simulations.db")
    recording.create_schema()
    with closing(recording.connect()) as connection:
        connection.executemany(INSERT_CUSTOMER, CUSTOMERS)
        connection.commit()
    return recording


def new_simulation(quote: Quote) -> NewSimulation:
    return NewSimulation(
        customer_id=1, storage_gb=STORAGE_GB, estimated_api_calls=ESTIMATED_API_CALLS, quote=quote
    )


def simulation_rows(database: RecordingDatabase) -> list[int]:
    """How many rows the two tables of the simulations have."""
    with closing(database.connect()) as connection:
        return [connection.execute(query).fetchone()[0] for query in COUNT_SIMULATION_ROWS]


@pytest.mark.parametrize("failing_tier", [2, 3])
def test_failure_while_storing_a_tier_leaves_no_row_of_the_simulation(
    database: RecordingDatabase, failing_tier: int
) -> None:
    """SPEC-03/E-11: the simulation and the tiers before the wrong one were written (CA-06)."""
    repository = SimulationRepository(database)
    quote = calculate_quote(ACTIVE_USERS, "ES")
    with pytest.raises(sqlite3.IntegrityError):
        repository.add(new_simulation(with_wrong_subtotal(quote, failing_tier)), CREATED_AT)
    # The failure came in the middle: the simulation and each tier up to the wrong one ran.
    assert len(database.statements) == 1 + failing_tier
    assert simulation_rows(database) == [0, 0]
    # The same simulation without the wrong tier is stored whole: the tier was the cause.
    assert repository.add(new_simulation(quote), CREATED_AT).id == 1
    assert simulation_rows(database) == [1, 3]


def test_values_of_a_simulation_reach_the_database_only_as_parameters(
    database: RecordingDatabase,
) -> None:
    """SPEC-03/E-23: no statement carries a value; they all go in the parameters (CA-13)."""
    quote = calculate_quote(ACTIVE_USERS, "ES")
    stored = SimulationRepository(database).add(new_simulation(quote), CREATED_AT)
    assert stored.id == 1
    # One statement for the simulation and one for each of its three tiers.
    assert len(database.statements) == 4
    for statement, _ in database.statements:
        # Neither a number nor a text literal: nothing that could be a value.
        assert not any(character.isdigit() for character in statement)
        assert "'" not in statement
    sent = [value for _, parameters in database.statements for value in parameters]
    for value in (ACTIVE_USERS, STORAGE_GB, ESTIMATED_API_CALLS, "ES", CREATED_AT):
        assert value in sent
    for value in (quote.base_cents, quote.tax_rate_bp, quote.tax_cents, quote.total_cents):
        assert value in sent
