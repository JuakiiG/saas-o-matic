"""Countries the system admits, each with its general tax rate (SPEC-02, 2.2)."""

from dataclasses import dataclass


class TaxRateNotDefinedError(Exception):
    """The country has no tax rate: stored data is inconsistent (SPEC-02/E-10)."""


@dataclass(frozen=True)
class Country:
    code: str
    name: str
    tax_rate_bp: int


# The only list of countries of the system. General VAT rates, in basis points (A4).
COUNTRIES: tuple[Country, ...] = (
    Country("ES", "España", 2100),
    Country("PT", "Portugal", 2300),
    Country("FR", "Francia", 2000),
    Country("DE", "Alemania", 1900),
    Country("IT", "Italia", 2200),
    Country("NL", "Países Bajos", 2100),
    Country("IE", "Irlanda", 2300),
    Country("BE", "Bélgica", 2100),
    Country("GB", "Reino Unido", 2000),
)
_TAX_RATES_BP = {country.code: country.tax_rate_bp for country in COUNTRIES}


def tax_rate_bp_of(country_code: str) -> int:
    """The rate of a country. A country without one is an error, never a rate of 0 %."""
    try:
        return _TAX_RATES_BP[country_code]
    except KeyError:
        raise TaxRateNotDefinedError(country_code) from None
