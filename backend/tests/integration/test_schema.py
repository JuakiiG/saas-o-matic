"""Database schema and its creation on startup (SPEC-03, 2.6 and 5.5)."""

import sqlite3
from contextlib import closing
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import load_settings
from app.main import create_app
from app.repositories.database import Database

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
TABLES = ["customers", "simulation_tiers", "simulations"]
INSERT_CUSTOMER = (
    "INSERT INTO customers (id, company_name, company_name_search, tax_id, contact_email,"
    " country, plan, created_at) VALUES (:id, 'Acme', 'acme', :tax_id, 'a@acme.example',"
    " :country, 'starter', '2026-11-13T10:00:00Z')"
)
INSERT_SIMULATION = (
    "INSERT INTO simulations (customer_id, active_users, storage_gb, estimated_api_calls,"
    " country, base_cents, tax_rate_bp, tax_cents, total_cents, created_at) VALUES"
    " (:customer_id, :active_users, :storage_gb, :estimated_api_calls, 'ES', :base_cents,"
    " :tax_rate_bp, :tax_cents, :total_cents, '2026-11-13T10:00:00Z')"
)
INSERT_TIER = (
    "INSERT INTO simulation_tiers (simulation_id, position, from_users, to_users,"
    " unit_price_cents, users, subtotal_cents) VALUES (:simulation_id, :position, :from_users,"
    " :to_users, :unit_price_cents, :users, :subtotal_cents)"
)
CUSTOMER = {"id": 1, "tax_id": "B12345674", "country": "ES"}
# 15 users in Spain: the worked example of SPEC-02.
SIMULATION = {
    "customer_id": 1,
    "active_users": 15,
    "storage_gb": 100,
    "estimated_api_calls": 1000,
    "base_cents": 14000,
    "tax_rate_bp": 2100,
    "tax_cents": 2940,
    "total_cents": 16940,
}
TIER = {
    "simulation_id": 1,
    "position": 1,
    "from_users": 1,
    "to_users": 10,
    "unit_price_cents": 1000,
    "users": 10,
    "subtotal_cents": 10000,
}


def start_application(path: Path, monkeypatch: pytest.MonkeyPatch) -> Database:
    """Start and stop the application with `DATABASE_PATH` set, as a real start does."""
    monkeypatch.setenv("DATABASE_PATH", str(path))
    with TestClient(create_app()):
        pass
    assert path.is_file(), "the application did not create the database on startup"
    return Database(path)


@pytest.fixture
def connection(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> sqlite3.Connection:
    """A connection opened as the application opens them, with a customer and a simulation."""
    database = start_application(tmp_path / "data" / "test.db", monkeypatch)
    opened = database.connect()
    opened.execute(INSERT_CUSTOMER, CUSTOMER)
    opened.execute(INSERT_SIMULATION, SIMULATION)
    opened.commit()
    return opened


def test_first_start_creates_the_folder_and_the_three_tables(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """SPEC-03/E-22: when the database does not exist, it is created with all its tables."""
    database = start_application(tmp_path / "missing" / "folder" / "test.db", monkeypatch)
    with closing(database.connect()) as opened:
        rows = opened.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name")
        assert [name for (name,) in rows] == TABLES


def test_second_start_keeps_the_stored_data(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """SPEC-03/E-22: when the database already exists, its data is kept."""
    path = tmp_path / "test.db"
    with closing(start_application(path, monkeypatch).connect()) as opened:
        opened.execute(INSERT_CUSTOMER, CUSTOMER)
        opened.commit()
    with closing(start_application(path, monkeypatch).connect()) as opened:
        assert opened.execute("SELECT id, tax_id FROM customers").fetchall() == [(1, "B12345674")]


def test_database_path_defaults_to_the_data_folder_of_the_backend(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """SPEC-03/E-32: without `DATABASE_PATH`, the path is `backend/data/saas-o-matic.db`."""
    monkeypatch.delenv("DATABASE_PATH", raising=False)
    expected = REPOSITORY_ROOT / "backend" / "data" / "saas-o-matic.db"
    assert load_settings().database_path == expected


def test_money_and_rates_are_integer_and_no_column_is_real(connection: sqlite3.Connection) -> None:
    """SPEC-03/E-19: amounts in integer cents, rates in integer basis points (CA-10)."""
    with closing(connection):
        for table in TABLES:
            columns = connection.execute("SELECT name, type FROM pragma_table_info(?)", (table,))
            for name, declared in columns.fetchall():
                assert declared in ("INTEGER", "TEXT"), (table, name, declared)
                if name.endswith(("_cents", "_bp")):
                    assert declared == "INTEGER", (table, name)


def test_every_column_is_required_except_the_upper_limit_of_a_tier(
    connection: sqlite3.Connection,
) -> None:
    """SPEC-03/E-22: the tables are created with the columns of 2.6, all of them NOT NULL."""
    with closing(connection):
        optional = []
        for table in TABLES:
            rows = connection.execute(
                'SELECT name FROM pragma_table_info(?) WHERE "notnull" = 0 AND pk = 0', (table,)
            )
            optional += [(table, name) for (name,) in rows]
        assert optional == [("simulation_tiers", "to_users")]


@pytest.mark.parametrize(
    "changes",
    [
        {"customer_id": 999},
        {"active_users": -1},
        {"storage_gb": -1},
        {"estimated_api_calls": -1},
        {"base_cents": -1, "total_cents": 2939},
        {"tax_rate_bp": -1},
        {"tax_cents": -1, "total_cents": 13999},
        {"total_cents": 16941},
    ],
    ids=lambda changes: ",".join(changes),
)
def test_database_rejects_an_impossible_simulation(
    connection: sqlite3.Connection, changes: dict[str, int]
) -> None:
    """SPEC-03/E-20, SPEC-03/E-21: unknown customer, negative value or wrong total."""
    with closing(connection), pytest.raises(sqlite3.IntegrityError):
        connection.execute(INSERT_SIMULATION, {**SIMULATION, **changes})


@pytest.mark.parametrize(
    "changes",
    [
        {"simulation_id": 999},
        {"subtotal_cents": 9999},
        {"position": 4},
        {"from_users": 0},
        {"from_users": -1},
        {"from_users": 11, "to_users": 10},
        {"unit_price_cents": -1, "subtotal_cents": -10},
        {"users": -1, "subtotal_cents": -1000},
    ],
    ids=lambda changes: ",".join(changes),
)
def test_database_rejects_an_impossible_tier(
    connection: sqlite3.Connection, changes: dict[str, int]
) -> None:
    """SPEC-03/E-20, SPEC-03/E-21: broken reference, wrong subtotal, position or limits."""
    with closing(connection), pytest.raises(sqlite3.IntegrityError):
        connection.execute(INSERT_TIER, {**TIER, **changes})


@pytest.mark.parametrize(
    ("statement", "valid", "changes"),
    [
        # 14000.5 + 2940 = 16940.5: only the type is wrong, the total adds up.
        (INSERT_SIMULATION, SIMULATION, {"base_cents": 14000.5, "total_cents": 16940.5}),
        (INSERT_SIMULATION, SIMULATION, {"active_users": "abc"}),
        (INSERT_TIER, TIER, {"unit_price_cents": 10.5, "subtotal_cents": 105.0}),
        # Price and subtotal at 0 so that no CHECK rejects the row before its type does.
        (INSERT_TIER, TIER, {"users": "many", "unit_price_cents": 0, "subtotal_cents": 0}),
    ],
    ids=["decimal-amount", "text-in-users", "decimal-price", "text-in-tier-users"],
)
def test_database_rejects_a_value_that_is_not_an_integer(
    connection: sqlite3.Connection,
    statement: str,
    valid: dict[str, int],
    changes: dict[str, object],
) -> None:
    """SPEC-03/E-19, SPEC-03/E-21: an amount with decimals or a text can never be true."""
    with closing(connection), pytest.raises(sqlite3.IntegrityError):
        connection.execute(statement, {**valid, **changes})


def test_database_rejects_a_repeated_tier(connection: sqlite3.Connection) -> None:
    """SPEC-03/E-21: a simulation cannot have the same tier twice."""
    with closing(connection):
        connection.execute(INSERT_TIER, TIER)
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(INSERT_TIER, TIER)


@pytest.mark.parametrize("to_users", [1, None], ids=["equal-to-lower-limit", "open-ended"])
def test_database_accepts_a_tier_with_valid_limits(
    connection: sqlite3.Connection, to_users: int | None
) -> None:
    """SPEC-03/E-21: an upper limit equal to the lower one, or none, is valid."""
    with closing(connection):
        connection.execute(INSERT_TIER, {**TIER, "to_users": to_users})
        assert connection.execute("SELECT count(*) FROM simulation_tiers").fetchone() == (1,)


def test_database_rejects_deleting_a_customer_with_simulations(
    connection: sqlite3.Connection,
) -> None:
    """SPEC-03/E-20: a customer with simulations cannot be deleted; nothing cascades."""
    with closing(connection):
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("DELETE FROM customers WHERE id = 1")
        assert connection.execute("SELECT count(*) FROM simulations").fetchone() == (1,)


def test_database_rejects_a_second_customer_with_the_same_country_and_tax_id(
    connection: sqlite3.Connection,
) -> None:
    """SPEC-03/E-22: `customers` is created with the UNIQUE (country, tax id) of 2.6.

    The rule about duplicates belongs to SPEC-01 and is tested there, with its endpoint;
    it is not cited here so that traceability does not count it as covered.
    """
    with closing(connection):
        connection.execute(INSERT_CUSTOMER, {**CUSTOMER, "id": 2, "country": "PT"})
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(INSERT_CUSTOMER, {**CUSTOMER, "id": 3})
