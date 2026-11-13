"""The history of simulations inside `GET /customers/{id}` (SPEC-03: 2.4, 4.2, 5.3 and 5.4)."""

from collections.abc import Callable, Iterator
from contextlib import closing
from datetime import datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.domain import countries, pricing
from app.domain.pricing import Tier, calculate_quote
from app.domain.simulations import NewSimulation
from app.main import create_app
from app.repositories.database import Database
from app.repositories.simulations import SimulationRepository
from tests.customer_cases import customer_with
from tests.integration.test_customers_search_sql import RecordingDatabase
from tests.integration.test_pricing_quote import CUSTOMERS, INSERT_CUSTOMER
from tests.simulation_cases import RESPONSE_FIELDS, simulation_with

DAY = "2026-11-12"
# The clock of the first four simulations of 5.3; the third and the fourth share the second.
CLOCK = ["15:00:00", "15:01:00", "15:05:00", "15:05:00"]
LATER = "16:00:00"
# The fifth is stored the last, with a date before all the others: a clock set back.
SET_BACK = f"{DAY}T14:00:00Z"
PROFILE_FIELDS = [
    "id",
    "company_name",
    "tax_id",
    "contact_email",
    "country",
    "plan",
    "created_at",
    "simulation_count",
    "simulations",
]
AMOUNT_FIELDS = ["base_cents", "tax_rate_bp", "tax_cents", "total_cents"]
# Simulations of 5.3 stored through the API, in order: customer and users.
STORED_THROUGH_THE_API = [(1, 15), (2, 15), (1, 51), (1, 0)]
Simulations = list[dict[str, object]]


def clock_of(times: list[str]) -> Callable[[], datetime]:
    """A clock that gives each time once, and then always the same later one."""
    pending = iter(times)

    def now() -> datetime:
        return datetime.fromisoformat(f"{DAY}T{next(pending, LATER)}+00:00")

    return now


@pytest.fixture
def database(tmp_path: Path) -> Database:
    return Database(tmp_path / "data" / "history.db")


@pytest.fixture
def client(
    tmp_path: Path, database: Database, monkeypatch: pytest.MonkeyPatch
) -> Iterator[TestClient]:
    """The real application with the clock of 5.3 and three customers: 1 is ES and 2 is DE."""
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "data" / "history.db"))
    monkeypatch.setattr("app.main._utc_now", clock_of(CLOCK))
    with TestClient(create_app()) as started:
        with closing(database.connect()) as connection:
            connection.executemany(INSERT_CUSTOMER, CUSTOMERS)
            connection.commit()
        yield started


def simulate(client: TestClient, customer_id: int, active_users: int) -> dict[str, object]:
    """Store a simulation through the API and give what it answered."""
    changes = {"customer_id": customer_id, "active_users": active_users}
    response = client.post("/simulations", json=simulation_with(changes))
    assert response.status_code == 201
    created: dict[str, object] = response.json()
    return created


@pytest.fixture
def created(client: TestClient, database: Database) -> Simulations:
    """The five simulations of 5.3, as their creation answered them, in the order of `id`."""
    answered = [simulate(client, *row) for row in STORED_THROUGH_THE_API]
    # The fifth goes straight to the repository, which is where a date can be chosen.
    quote = calculate_quote(10, "ES")
    fifth = SimulationRepository(database).add(NewSimulation(1, 500, 250000, quote), SET_BACK)
    assert fifth.id == 5
    return answered


def history_of(client: TestClient, customer_id: int) -> tuple[object, Simulations]:
    """`simulation_count` and `simulations` of a customer, after checking the form of 4.2."""
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    body = response.json()
    assert list(body) == PROFILE_FIELDS
    simulations: Simulations = body["simulations"]
    return body["simulation_count"], simulations


def test_history_is_ordered_by_id_descending_whatever_the_dates(
    client: TestClient, created: Simulations
) -> None:
    """SPEC-03/E-12, SPEC-03/E-13, SPEC-03/E-17: first row of 5.3 (CA-07)."""
    count, simulations = history_of(client, 1)
    assert count == 4
    assert [simulation["id"] for simulation in simulations] == [5, 4, 3, 1]
    # The fifth goes first with the oldest date, and the tie of dates changes nothing.
    dates = [simulation["created_at"] for simulation in simulations]
    assert dates == [SET_BACK, f"{DAY}T15:05:00Z", f"{DAY}T15:05:00Z", f"{DAY}T15:00:00Z"]
    assert [simulation["total_cents"] for simulation in simulations] == [12100, 0, 51425, 16940]
    assert {simulation["customer_id"] for simulation in simulations} == {1}


def test_history_has_only_the_simulations_of_its_customer(
    client: TestClient, created: Simulations
) -> None:
    """SPEC-03/E-17, SPEC-03/E-12: second row of 5.3, with two customers (CA-07)."""
    count, simulations = history_of(client, 2)
    assert count == 1
    assert simulations == [created[1]]
    assert (simulations[0]["id"], simulations[0]["total_cents"]) == (2, 16660)


def test_history_of_a_customer_without_simulations_is_an_empty_list(
    client: TestClient, created: Simulations
) -> None:
    """SPEC-03/E-15: a list that is empty, not absent, and a total of 0 (5.3, CA-07)."""
    assert history_of(client, 3) == (0, [])


def test_history_shows_each_simulation_exactly_as_its_creation_answered_it(
    client: TestClient, created: Simulations
) -> None:
    """SPEC-03/E-12, SPEC-03/E-16: every element has the form of 4.1, to the letter (4.2)."""
    _, simulations = history_of(client, 1)
    assert simulations[1:] == [created[3], created[2], created[0]]
    for simulation in simulations:
        assert list(simulation) == RESPONSE_FIELDS


def test_history_of_a_customer_with_55_simulations_has_the_50_of_highest_id(
    client: TestClient,
) -> None:
    """SPEC-03/E-14, SPEC-03/E-12: the limit of 50 and the real total (5.3, CA-07)."""
    for number in range(55):
        simulate(client, 1, number)
    # One of another customer in between must not take a place among the 50.
    simulate(client, 2, 15)
    count, simulations = history_of(client, 1)
    assert count == 55
    assert [simulation["id"] for simulation in simulations] == list(range(55, 5, -1))


def test_stored_amounts_are_not_calculated_again_nor_the_country_read_again(
    client: TestClient, database: Database, monkeypatch: pytest.MonkeyPatch
) -> None:
    """SPEC-03/E-16: the six steps of 5.4 (CA-08)."""
    first = simulate(client, 1, 15)
    assert [first[field] for field in AMOUNT_FIELDS] == [14000, 2100, 2940, 16940]
    monkeypatch.setattr(pricing, "TIERS", (Tier(1, 10, 2000), *pricing.TIERS[1:]))
    monkeypatch.setitem(countries._TAX_RATES_BP, "ES", 1000)
    assert history_of(client, 1) == (1, [first])
    second = simulate(client, 1, 15)
    assert [second[field] for field in AMOUNT_FIELDS] == [24000, 1000, 2400, 26400]
    with closing(database.connect()) as connection:
        connection.execute("UPDATE customers SET country = 'DE' WHERE id = 1")
        connection.commit()
    assert client.get("/customers/1").json()["country"] == "DE"
    # Both keep the country they were calculated with: it is read from the simulation.
    assert history_of(client, 1) == (2, [second, first])
    assert (first["country"], second["country"]) == ("ES", "ES")


def test_new_customer_is_read_with_an_empty_history(client: TestClient) -> None:
    """SPEC-01/E-22, SPEC-03/E-15: the profile of 4.2 of a customer just created (CA-06)."""
    # Another identifier: the customer 1 of the fixture already has the one of the example.
    response = client.post("/customers", json=customer_with({"tax_id": "A24680241"}))
    assert response.status_code == 201
    profile = client.get(response.headers["location"])
    assert profile.status_code == 200
    assert profile.json() == {**response.json(), "simulation_count": 0, "simulations": []}


def test_openapi_declares_the_history_inside_the_customer(client: TestClient) -> None:
    """SPEC-03/E-12: fields of 4.2, and each simulation with the fields of 4.1 (CA-14)."""
    document = client.get("/openapi.json").json()
    schemas = document["components"]["schemas"]
    responses = document["paths"]["/customers/{id}"]["get"]["responses"]
    answered = responses["200"]["content"]["application/json"]["schema"]["$ref"]
    profile = schemas[answered.rsplit("/", maxsplit=1)[-1]]["properties"]
    assert list(profile) == PROFILE_FIELDS
    assert profile["simulation_count"].get("type") == "integer"
    item = profile["simulations"].get("items", {}).get("$ref", "")
    assert list(schemas[item.rsplit("/", maxsplit=1)[-1]]["properties"]) == RESPONSE_FIELDS


def recording_database(tmp_path: Path) -> RecordingDatabase:
    """A database with the customers, that writes down what runs on it."""
    database = RecordingDatabase(tmp_path / "history-sql.db")
    database.create_schema()
    with closing(database.connect()) as connection:
        connection.executemany(INSERT_CUSTOMER, CUSTOMERS)
        connection.commit()
    return database


def test_history_is_read_with_its_values_only_as_parameters(tmp_path: Path) -> None:
    """SPEC-03/E-23: neither the customer nor the limit is part of a statement (CA-13)."""
    database = recording_database(tmp_path)
    repository = SimulationRepository(database)
    for users in (37, 51):
        repository.add(NewSimulation(1, 500, 250000, calculate_quote(users, "ES")), SET_BACK)
    repository.add(NewSimulation(2, 500, 250000, calculate_quote(15, "DE")), SET_BACK)
    database.statements.clear()
    history = repository.history(1, 1)
    assert history.simulation_count == 2
    assert [simulation.id for simulation in history.simulations] == [2]
    assert history.simulations[0].quote == calculate_quote(51, "ES")
    assert database.statements
    for statement, _ in database.statements:
        assert not any(character.isdigit() for character in statement)
        assert "'" not in statement


def test_simulation_stored_without_tiers_is_listed_with_an_empty_breakdown(
    tmp_path: Path,
) -> None:
    """SPEC-03/E-12: the total and the list agree even if a direct insertion left no tiers."""
    database = recording_database(tmp_path)
    with closing(database.connect()) as connection:
        connection.execute(
            "INSERT INTO simulations VALUES (9, 1, 1, 0, 0, 'ES', 1000, 2100, 210, 1210, ?)",
            (SET_BACK,),
        )
        connection.commit()
    history = SimulationRepository(database).history(1, 50)
    assert history.simulation_count == 1
    assert [(simulation.id, simulation.quote.tiers) for simulation in history.simulations] == [
        (9, ())
    ]
