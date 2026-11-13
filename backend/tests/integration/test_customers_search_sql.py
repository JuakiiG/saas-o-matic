"""The text searched reaches the database only as a parameter (SPEC-01, CA-14)."""

import sqlite3
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import cast

from app.domain.customers import NewCustomer, customer_search
from app.repositories.customers import CustomerRepository
from app.repositories.database import Database

INJECTION = "' OR 1=1 --"
WILDCARDS = "100%_\\"


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
