"""Use case: is the backend able to serve requests?"""

from app.repositories.database import Database, DatabaseUnavailableError


class ServiceUnavailableError(Exception):
    """Something the backend needs in order to answer is not available."""


class HealthService:
    def __init__(self, database: Database) -> None:
        self._database = database

    def check(self) -> None:
        """Raise `ServiceUnavailableError` if the database does not answer."""
        try:
            self._database.ping()
        except DatabaseUnavailableError as error:
            raise ServiceUnavailableError("database") from error
