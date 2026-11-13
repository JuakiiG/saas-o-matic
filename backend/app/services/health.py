"""Use case: is the backend able to serve requests?"""

from app.repositories.database import Database


class HealthService:
    def __init__(self, database: Database) -> None:
        self._database = database

    def check(self) -> None:
        """Let `DatabaseUnavailableError` through if the database does not answer."""
        self._database.ping()
