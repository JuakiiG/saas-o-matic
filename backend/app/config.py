"""Configuration from environment variables, with defaults for local use.

Read when the application is built, not on import, so each test can start the
application with its own values.
"""

import os
from dataclasses import dataclass

CORS_ORIGINS_VARIABLE = "CORS_ORIGINS"
# The frontend in local development (SPEC-03/E-26).
DEFAULT_CORS_ORIGINS = "http://localhost:4200"


@dataclass(frozen=True)
class Settings:
    cors_origins: tuple[str, ...]


def _split_list(value: str) -> tuple[str, ...]:
    """Entries of a comma separated list, without surrounding spaces or empty entries."""
    return tuple(entry.strip() for entry in value.split(",") if entry.strip())


def load_settings() -> Settings:
    """Settings of this process. An undefined variable takes its default; an empty one does not."""
    origins = os.environ.get(CORS_ORIGINS_VARIABLE, DEFAULT_CORS_ORIGINS)
    return Settings(cors_origins=_split_list(origins))
