"""The SQLite database file, its schema and its connections."""

import sqlite3
from contextlib import closing
from pathlib import Path

SCHEMA_FILE = Path(__file__).with_name("schema.sql")


class DatabaseUnavailableError(Exception):
    """The database cannot be opened or does not answer."""


class Database:
    """Opens connections to the SQLite file; one per use, never shared (ADR-001)."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._path)
        # SQLite does not enforce foreign keys unless each connection asks for it (ADR-001).
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def create_schema(self) -> None:
        """Create the file, its folder and the missing tables; existing data is kept."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self.connect()) as connection:
            connection.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))

    def ping(self) -> None:
        """Run a trivial query that touches no business data."""
        try:
            with closing(self.connect()) as connection:
                connection.execute("SELECT 1").fetchone()
        except sqlite3.Error as error:
            raise DatabaseUnavailableError("the database does not answer") from error
