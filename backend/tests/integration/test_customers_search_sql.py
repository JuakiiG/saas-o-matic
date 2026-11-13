"""The text searched reaches the database only as a parameter (SPEC-01, CA-14)."""

import sqlite3
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import cast

import pytest

from app.domain.customers import CustomerSearch, NewCustomer, customer_search
from app.repositories.customers import CustomerRepository
from app.repositories.database import Database

INJECTION = "' OR 1=1 --"
WILDCARDS = "100%_\\"
CREATED_AT = "2026-11-13T10:00:00Z"
# Values that would change the statement if any of them were written into it. The
# repository stores what it is given: validating it is the job of the domain.
HOSTILE_VALUES = (INJECTION, "' OR 1=1 -- search", "X' OR '1'='1", "'); DROP TABLE customers;--")
HOSTILE_CUSTOMER = NewCustomer(
    company_name=INJECTION,
    company_name_search=HOSTILE_VALUES[1],
    tax_id=HOSTILE_VALUES[2],
    contact_email=INJECTION,
    country="ES",
    plan=HOSTILE_VALUES[3],
)
# An id of several digits, so that it could not be in a statement by chance.
CUSTOMER_ID = 12


class RecordingConnection:
    """A connection that writes down every statement and its parameters before running it."""

    def __init__(self, real: sqlite3.Connection, log: list[tuple[str, tuple[object, ...]]]) -> None:
        self._real = real
        self._log = log

    def execute(self, statement: str, parameters: Sequence[object] = ()) -> sqlite3.Cursor:
        self._log.append((statement, tuple(parameters)))
        return self._real.execute(statement, parameters)

    def commit(self) -> None:
        self._real.commit()


class RecordingDatabase(Database):
    def __init__(self, path: Path) -> None:
        super().__init__(path)
        self.statements: list[tuple[str, tuple[object, ...]]] = []

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        with super().connection() as real:
            # Only `execute` and `commit` are used by the repositories.
            yield cast(sqlite3.Connection, RecordingConnection(real, self.statements))


def recording_repository(tmp_path: Path) -> tuple[CustomerRepository, RecordingDatabase]:
    database = RecordingDatabase(tmp_path / "search.db")
    database.create_schema()
    repository = CustomerRepository(database)
    new = NewCustomer("100%_\\ SL", "100%_\\ sl", "B12345674", "a@b.example", "ES", "starter")
    repository.add(new, "2026-11-13T10:00:00Z")
    database.statements.clear()
    return repository, database


def test_searched_text_is_never_part_of_the_statement(tmp_path: Path) -> None:
    """SPEC-01/E-28: the text is in the parameters and not in the SQL that runs (CA-14)."""
    repository, database = recording_repository(tmp_path)
    assert repository.search(customer_search(INJECTION), 20) == []
    assert len(database.statements) == 1
    statement, parameters = database.statements[0]
    assert "1=1" not in statement
    assert "OR1=1" not in statement.replace(" ", "")
    assert any("or 1=1" in str(parameter) for parameter in parameters)


def test_wildcards_of_the_searched_text_are_escaped_in_the_parameters(tmp_path: Path) -> None:
    """SPEC-01/E-27, SPEC-01/E-28: `%`, `_` and the escape character are searched literally."""
    repository, database = recording_repository(tmp_path)
    found = repository.search(customer_search(WILDCARDS), 20)
    assert [customer.company_name for customer in found] == ["100%_\\ SL"]
    statement, parameters = database.statements[0]
    assert "100" not in statement
    assert "%100\\%\\_\\\\%" in parameters


def test_statement_compares_what_the_domain_gives_and_decides_nothing(tmp_path: Path) -> None:
    """SPEC-01/E-25, SPEC-01/E-28: what is compared is decided in the domain, not in SQL (2.10).

    The domain never gives an empty identifier. Given one by hand, the statement compares
    it like any other text, and every customer contains it: it holds no condition of its own.
    """
    repository, database = recording_repository(tmp_path)
    found = repository.search(CustomerSearch("noexiste", ""), 20)
    assert [customer.tax_id for customer in found] == ["B12345674"]
    assert database.statements[0][1] == ("%noexiste%", "%%", 20)


@pytest.mark.parametrize(
    ("search", "parameters", "found"),
    [
        (CustomerSearch("noexiste", None), ("%noexiste%", None, 20), 0),
        (CustomerSearch(None, None), (None, None, 20), 0),
        (CustomerSearch("", None), ("%%", None, 20), 1),
    ],
    ids=["no-identifier", "nothing-to-compare", "empty-name"],
)
def test_form_that_the_domain_leaves_out_reaches_the_database_as_a_null(
    tmp_path: Path, search: CustomerSearch, parameters: tuple[object, ...], found: int
) -> None:
    """SPEC-01/E-25, SPEC-01/E-28: a form with nothing to compare matches no customer (2.10)."""
    repository, database = recording_repository(tmp_path)
    assert len(repository.search(search, 20)) == found
    assert database.statements[0][1] == parameters


def assert_no_value_in(statement: str) -> None:
    """Neither a number nor a text literal: nothing that could be a value."""
    assert not any(character.isdigit() for character in statement)
    assert "'" not in statement


# Written after the code that it tests (session 05, H-14): it was never seen failing.
def test_values_of_a_new_customer_reach_the_database_only_as_parameters(tmp_path: Path) -> None:
    """SPEC-03/E-23: the statement that stores a customer carries no value (CA-13)."""
    database = RecordingDatabase(tmp_path / "insert.db")
    database.create_schema()
    stored = CustomerRepository(database).add(HOSTILE_CUSTOMER, CREATED_AT)
    assert len(database.statements) == 1
    statement, parameters = database.statements[0]
    assert_no_value_in(statement)
    for value in (*HOSTILE_VALUES, CREATED_AT):
        assert value not in statement
        assert value in parameters
    # Stored as text, to the letter: nothing of it was run.
    assert (stored.id, stored.company_name, stored.contact_email) == (1, INJECTION, INJECTION)


# Written after the code that it tests (session 05, H-14): it was never seen failing.
def test_id_of_a_customer_reaches_the_database_only_as_a_parameter(tmp_path: Path) -> None:
    """SPEC-03/E-23: reading a customer and reading its country carry no value (CA-13)."""
    database = RecordingDatabase(tmp_path / "read.db")
    database.create_schema()
    repository = CustomerRepository(database)
    for number in range(CUSTOMER_ID):
        new = NewCustomer("Acme", "acme", f"FR{number:04d}", "a@b.example", "FR", "starter")
        repository.add(new, CREATED_AT)
    database.statements.clear()
    found = repository.find(CUSTOMER_ID)
    assert found is not None
    assert (found.id, repository.country_of(CUSTOMER_ID)) == (CUSTOMER_ID, "FR")
    assert [parameters for _, parameters in database.statements] == [(CUSTOMER_ID,), (CUSTOMER_ID,)]
    for statement, _ in database.statements:
        assert_no_value_in(statement)
