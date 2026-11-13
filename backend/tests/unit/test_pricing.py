"""Fee by tiers and tax (SPEC-02: rules 2.1 and 2.2, tables 5.1 to 5.3)."""

from itertools import pairwise

import pytest

from app.domain.countries import COUNTRIES, TaxRateNotDefinedError
from app.domain.pricing import (
    ActiveUsersOutOfRangeError,
    Quote,
    TierCharge,
    calculate_quote,
    tax_cents,
)

# Table 5.1: users, subtotal of each tier, base, tax and total with the rate of Spain.
SPAIN_ROWS = [
    (0, (0, 0, 0), 0, 0, 0),
    (1, (1000, 0, 0), 1000, 210, 1210),
    (10, (10000, 0, 0), 10000, 2100, 12100),
    (11, (10000, 800, 0), 10800, 2268, 13068),
    (15, (10000, 4000, 0), 14000, 2940, 16940),
    (50, (10000, 32000, 0), 42000, 8820, 50820),
    (51, (10000, 32000, 500), 42500, 8925, 51425),
    (100, (10000, 32000, 25000), 67000, 14070, 81070),
    (20000, (10000, 32000, 9975000), 10017000, 2103570, 12120570),
    (100000, (10000, 32000, 49975000), 50017000, 10503570, 60520570),
]
# Table 5.2, one case per country: code, rate, tax and total for 15 users (base 14000).
COUNTRY_ROWS = [
    ("DE", 1900, 2660, 16660),
    ("FR", 2000, 2800, 16800),
    ("GB", 2000, 2800, 16800),
    ("ES", 2100, 2940, 16940),
    ("NL", 2100, 2940, 16940),
    ("BE", 2100, 2940, 16940),
    ("IT", 2200, 3080, 17080),
    ("PT", 2300, 3220, 17220),
    ("IE", 2300, 3220, 17220),
]
# Table 5.3: base, rate and tax. Invented values: no real fee produces fractions of a cent.
ROUNDING_ROWS = [
    (14000, 0, 0),
    (0, 2100, 0),
    (10, 2100, 2),
    (49, 100, 0),
    (50, 100, 1),
    (250, 100, 3),
    (999, 2150, 215),
    (1005, 2100, 211),
]


@pytest.mark.parametrize(
    ("active_users", "subtotals", "base", "tax", "total"),
    SPAIN_ROWS,
    ids=[str(row[0]) for row in SPAIN_ROWS],
)
def test_quote_in_spain_matches_its_row_of_the_table(
    active_users: int, subtotals: tuple[int, int, int], base: int, tax: int, total: int
) -> None:
    """SPEC-02/E-01, SPEC-02/E-02, SPEC-02/E-04, SPEC-02/E-06: every row of 5.1 (CA-01)."""
    quote = calculate_quote(active_users, "ES")
    assert tuple(tier.subtotal_cents for tier in quote.tiers) == subtotals
    assert sum(tier.users for tier in quote.tiers) == active_users
    assert (quote.base_cents, quote.tax_cents, quote.total_cents) == (base, tax, total)


def test_quote_of_15_users_in_spain_is_the_example_of_the_contract() -> None:
    """SPEC-02/E-06: the three tiers, also the empty one, and the rate applied (section 4)."""
    assert calculate_quote(15, "ES") == Quote(
        active_users=15,
        tiers=(
            TierCharge(1, 10, 1000, users=10, subtotal_cents=10000),
            TierCharge(11, 50, 800, users=5, subtotal_cents=4000),
            TierCharge(51, None, 500, users=0, subtotal_cents=0),
        ),
        base_cents=14000,
        country="ES",
        tax_rate_bp=2100,
        tax_cents=2940,
        total_cents=16940,
    )


def test_each_additional_user_costs_the_price_of_its_tier() -> None:
    """SPEC-02/E-01: from 0 to 1000 users, one more user adds the price of its tier (CA-03)."""
    bases = [calculate_quote(users, "ES").base_cents for users in range(1002)]
    increments = [after - before for before, after in pairwise(bases)]
    assert increments == [1000] * 10 + [800] * 40 + [500] * 951


@pytest.mark.parametrize(
    ("code", "rate", "tax", "total"), COUNTRY_ROWS, ids=[row[0] for row in COUNTRY_ROWS]
)
def test_quote_of_15_users_applies_the_rate_of_the_country(
    code: str, rate: int, tax: int, total: int
) -> None:
    """SPEC-02/E-03: every row of 5.2; the tax is calculated on the whole base (CA-02)."""
    quote = calculate_quote(15, code)
    assert (quote.base_cents, quote.country, quote.tax_rate_bp) == (14000, code, rate)
    assert (quote.tax_cents, quote.total_cents) == (tax, total)


@pytest.mark.parametrize(("base", "rate", "tax"), ROUNDING_ROWS)
def test_tax_is_rounded_to_the_nearest_cent_with_half_a_cent_up(
    base: int, rate: int, tax: int
) -> None:
    """SPEC-02/E-03: every row of 5.3 (CA-02)."""
    assert tax_cents(base, rate) == tax


def test_tax_of_an_amount_that_a_float_cannot_hold_is_exact() -> None:
    """SPEC-02/E-05: no floating point in any step; 2^53 + 1 is not a float."""
    assert tax_cents(2**53 + 1, 10_000) == 2**53 + 1


def test_countries_are_the_nine_of_the_spec_with_their_general_rate() -> None:
    """SPEC-02/E-03: the only list of countries of the system, with the rates of 2.2."""
    listed = [(country.code, country.name, country.tax_rate_bp) for country in COUNTRIES]
    assert listed == [
        ("ES", "España", 2100),
        ("PT", "Portugal", 2300),
        ("FR", "Francia", 2000),
        ("DE", "Alemania", 1900),
        ("IT", "Italia", 2200),
        ("NL", "Países Bajos", 2100),
        ("IE", "Irlanda", 2300),
        ("BE", "Bélgica", 2100),
        ("GB", "Reino Unido", 2000),
    ]


@pytest.mark.parametrize("active_users", [-1, 100_001], ids=["negative", "above-maximum"])
def test_quote_with_users_out_of_range_is_rejected(active_users: int) -> None:
    """SPEC-02/E-09: the domain rejects it with an error of its own (CA-04)."""
    with pytest.raises(ActiveUsersOutOfRangeError):
        calculate_quote(active_users, "ES")


def test_quote_for_a_country_without_tax_rate_is_rejected() -> None:
    """SPEC-02/E-10: an error of its own, never a rate of 0 % (CA-04)."""
    with pytest.raises(TaxRateNotDefinedError):
        calculate_quote(15, "US")
