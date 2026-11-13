"""The SQLite database file and its connections."""

import sqlite3
from contextlib import closing
from pathlib import Path


class DatabaseUnavailableError(Exception):
    """The database cannot be opened or does not answer."""


class Database:
    """Opens connections to the SQLite file; one per use, never shared (ADR-001)."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._path)

    def ping(self) -> None:
        """Run a trivial query that touches no business data."""
        try:
            with closing(self.connect()) as connection:
                connection.execute("SELECT 1").fetchone()
        except sqlite3.Error as error:
            raise DatabaseUnavailableError("the database does not answer") from error
