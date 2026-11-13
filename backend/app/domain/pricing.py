"""Monthly fee by tiers and its tax (SPEC-02). Integer cents and basis points only."""

from dataclasses import dataclass

from app.domain.countries import tax_rate_bp_of

MAX_ACTIVE_USERS = 100_000
# A rate in basis points divides by 10000; half of it rounds half a cent up.
BASIS_POINT_SCALE = 10_000
HALF_BASIS_POINT_SCALE = 5_000


class ActiveUsersOutOfRangeError(Exception):
    """The number of users is negative or above the maximum (SPEC-02/E-09)."""


@dataclass(frozen=True)
class Tier:
    """One tier of the fee: the users it covers and the price of each of them."""

    from_users: int
    # None in the last tier, which has no upper limit.
    to_users: int | None
    unit_price_cents: int


TIERS = (Tier(1, 10, 1000), Tier(11, 50, 800), Tier(51, None, 500))


@dataclass(frozen=True)
class TierCharge:
    """What one tier of the fee adds to a quote."""

    from_users: int
    # None in the last tier, which has no upper limit.
    to_users: int | None
    unit_price_cents: int
    users: int
    subtotal_cents: int


@dataclass(frozen=True)
class Quote:
    """A complete calculation: the breakdown by tiers, the tax applied and the total."""

    active_users: int
    tiers: tuple[TierCharge, ...]
    base_cents: int
    country: str
    tax_rate_bp: int
    tax_cents: int
    total_cents: int


def _users_in_tier(tier: Tier, active_users: int) -> int:
    """How many of the users fall in the tier: each user pays the price of its own tier."""
    last = active_users if tier.to_users is None else min(active_users, tier.to_users)
    return max(last - tier.from_users + 1, 0)


def _charge(tier: Tier, active_users: int) -> TierCharge:
    users = _users_in_tier(tier, active_users)
    return TierCharge(
        tier.from_users, tier.to_users, tier.unit_price_cents, users, tier.unit_price_cents * users
    )


def tax_cents(base_cents: int, tax_rate_bp: int) -> int:
    """Tax on the whole base, to the nearest cent, half a cent up. Integers only."""
    return (base_cents * tax_rate_bp + HALF_BASIS_POINT_SCALE) // BASIS_POINT_SCALE


def calculate_quote(active_users: int, country_code: str) -> Quote:
    """The only calculation of the system: the quote and the saved simulation both use it."""
    if not 0 <= active_users <= MAX_ACTIVE_USERS:
        raise ActiveUsersOutOfRangeError(active_users)
    rate = tax_rate_bp_of(country_code)
    tiers = tuple(_charge(tier, active_users) for tier in TIERS)
    base = sum(tier.subtotal_cents for tier in tiers)
    tax = tax_cents(base, rate)
    return Quote(active_users, tiers, base, country_code, rate, tax, base + tax)
