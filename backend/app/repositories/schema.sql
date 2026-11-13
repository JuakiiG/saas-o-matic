-- Schema of SaaS-O-Matic (SPEC-03, 2.6; ADR-004).
-- Applied on every start: it only creates what is missing, so existing data is kept.
-- Money is INTEGER cents and tax rates are INTEGER basis points; no column is REAL.
-- The tables are STRICT (SQLite 3.37.0 or later): without it a declared type is only an
-- affinity, and an INTEGER column would store 10.5 as a real and 'abc' as a text.
-- The database only rejects what can never be true (a value of another type, negative
-- values, sums that do not add up, broken references). Business maximums live in the
-- API, because they may change.

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    -- Search form of the name: no accents, case folded (SPEC-01/E-33).
    company_name_search TEXT NOT NULL,
    -- Normalized.
    tax_id TEXT NOT NULL,
    contact_email TEXT NOT NULL,
    country TEXT NOT NULL,
    plan TEXT NOT NULL,
    -- UTC, ISO 8601, precision of seconds.
    created_at TEXT NOT NULL,
    UNIQUE (country, tax_id)
) STRICT;

CREATE TABLE IF NOT EXISTS simulations (
    id INTEGER PRIMARY KEY,
    -- No cascade: a customer with simulations cannot be deleted.
    customer_id INTEGER NOT NULL REFERENCES customers (id),
    active_users INTEGER NOT NULL CHECK (active_users >= 0),
    storage_gb INTEGER NOT NULL CHECK (storage_gb >= 0),
    estimated_api_calls INTEGER NOT NULL CHECK (estimated_api_calls >= 0),
    -- Country of the customer when the amount was calculated.
    country TEXT NOT NULL,
    base_cents INTEGER NOT NULL CHECK (base_cents >= 0),
    tax_rate_bp INTEGER NOT NULL CHECK (tax_rate_bp >= 0),
    tax_cents INTEGER NOT NULL CHECK (tax_cents >= 0),
    total_cents INTEGER NOT NULL CHECK (total_cents = base_cents + tax_cents),
    created_at TEXT NOT NULL
) STRICT;

-- The breakdown of the calculation: three rows per simulation.
CREATE TABLE IF NOT EXISTS simulation_tiers (
    simulation_id INTEGER NOT NULL REFERENCES simulations (id),
    position INTEGER NOT NULL CHECK (position IN (1, 2, 3)),
    from_users INTEGER NOT NULL CHECK (from_users >= 1),
    -- NULL in the last tier, which has no upper limit.
    to_users INTEGER CHECK (to_users IS NULL OR to_users >= from_users),
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0),
    users INTEGER NOT NULL CHECK (users >= 0),
    subtotal_cents INTEGER NOT NULL CHECK (subtotal_cents = unit_price_cents * users),
    PRIMARY KEY (simulation_id, position)
) STRICT;
