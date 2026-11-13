"""Simulations for the tests of `POST /simulations` (SPEC-03: 4.1 and tables 5.1 and 5.2)."""

from collections.abc import Mapping
from dataclasses import replace

from app.domain.pricing import Quote

ABSENT = object()
MAX_ID = 9223372036854775807
# The request of 4.1, to the letter. Customer 1 is Spanish.
VALID_SIMULATION: dict[str, object] = {
    "customer_id": 1,
    "active_users": 15,
    "storage_gb": 500,
    "estimated_api_calls": 250000,
}
REQUEST_FIELDS = list(VALID_SIMULATION)
# The fields of the response of 4.1, in its order.
RESPONSE_FIELDS = [
    "id",
    "customer_id",
    "active_users",
    "storage_gb",
    "estimated_api_calls",
    "currency",
    "tiers",
    "base_cents",
    "country",
    "tax_rate_bp",
    "tax_cents",
    "total_cents",
    "created_at",
]
# Table 5.1: customer (1 is ES, 2 is DE), users, storage and calls; base, rate, tax and total.
VALID_ROWS = [
    (1, 15, 500, 250000, 14000, 2100, 2940, 16940),
    (1, 15, 0, 0, 14000, 2100, 2940, 16940),
    (1, 15, 1000000, 1000000000, 14000, 2100, 2940, 16940),
    (1, 0, 500, 250000, 0, 2100, 0, 0),
    (1, 51, 500, 250000, 42500, 2100, 8925, 51425),
    (1, 100000, 500, 250000, 50017000, 2100, 10503570, 60520570),
    (2, 15, 500, 250000, 14000, 1900, 2660, 16660),
]
# What a request changes of the valid one, and the field codes that it must answer.
InvalidRow = tuple[dict[str, object], list[tuple[str, str]]]


def _rows(field: str, values: list[object], code: str) -> list[InvalidRow]:
    return [({field: value}, [(field, code)]) for value in values]


# Table 5.2, and the rows of `active_users` of SPEC-02 (5.4), which are valid here too.
INVALID_ROWS: list[InvalidRow] = [
    *_rows("storage_gb", [-1, 1000001], "out_of_range"),
    *_rows("storage_gb", [500.5, 500.0, "500", True, None], "not_an_integer"),
    *_rows("storage_gb", [ABSENT], "missing"),
    *_rows("estimated_api_calls", [-1, 1000000001], "out_of_range"),
    *_rows("estimated_api_calls", [1.5, "1000", True, None], "not_an_integer"),
    *_rows("estimated_api_calls", [ABSENT], "missing"),
    *_rows("customer_id", ["1", 1.0, None], "not_an_integer"),
    *_rows("customer_id", [0, -1, MAX_ID + 1], "out_of_range"),
    *_rows("customer_id", [ABSENT], "missing"),
    *_rows("active_users", [-1, 100001], "out_of_range"),
    *_rows("active_users", [15.5, 15.0, "15", True, None], "not_an_integer"),
    *_rows("active_users", [ABSENT], "missing"),
    ({"total_cents": 16940}, [("total_cents", "unknown_field")]),
    ({"tax_rate_bp": 0}, [("tax_rate_bp", "unknown_field")]),
    ({"country": "ES"}, [("country", "unknown_field")]),
    ({"created_at": "2026-11-12T15:00:00Z"}, [("created_at", "unknown_field")]),
    (
        {"storage_gb": -1, "estimated_api_calls": ABSENT},
        [("storage_gb", "out_of_range"), ("estimated_api_calls", "missing")],
    ),
    # Validation wins over a customer that does not exist.
    ({"customer_id": 999, "active_users": -1}, [("active_users", "out_of_range")]),
]


def simulation_with(changes: Mapping[str, object]) -> dict[str, object]:
    """The valid simulation with some fields changed; `ABSENT` leaves a field out."""
    fields = {**VALID_SIMULATION, **changes}
    return {name: value for name, value in fields.items() if value is not ABSENT}


def row_id(changes: Mapping[str, object]) -> str:
    """A name for a row that does not change from one run to another."""
    values = {name: "absent" if value is ABSENT else value for name, value in changes.items()}
    return ascii(values)


def with_wrong_subtotal(quote: Quote, position: int) -> Quote:
    """The quote with a tier that the database rejects: its subtotal is not price by users."""
    tiers = list(quote.tiers)
    wrong = tiers[position - 1]
    tiers[position - 1] = replace(wrong, subtotal_cents=wrong.subtotal_cents + 1)
    return replace(quote, tiers=tuple(tiers))
