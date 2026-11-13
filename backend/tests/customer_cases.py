"""The cases of SPEC-01 (5.7) for the fields of a new customer, shared by two tests.

The unit test runs them against the domain and the integration test against
`POST /customers`: one table, so that the two cannot drift apart.
"""

from collections.abc import Mapping

ABSENT = object()
VALID_CUSTOMER: dict[str, object] = {
    "company_name": "Ejemplo Uno SL",
    "tax_id": "B12345674",
    "contact_email": "compras@ejemplo-uno.example",
    "country": "ES",
    "plan": "professional",
}
FIELDS = list(VALID_CUSTOMER)
LONG_TAX_ID = "1" * 31
ZERO_WIDTH_SPACE = chr(0x200B)
EMAIL_OF_255 = "a" * 245 + "@b.example"
INVALID_EMAILS = [
    "sin-arroba.example",
    "a@@b.example",
    "@b.example",
    "a@b",
    "a b@c.example",
    "a@.example",
]
# Unicode separators that are not U+0020, by code point so that no editor changes them:
# no-break space and ideographic space (Zs), line separator (Zl), paragraph separator (Zp).
NO_BREAK_SPACE = chr(0x00A0)
SEPARATOR_EMAILS = [
    f"a{NO_BREAK_SPACE}b@c.example",
    # At an end: only U+0020 is trimmed.
    f"a@b.example{NO_BREAK_SPACE}",
    f"a{chr(0x3000)}b@c.example",
    f"a{chr(0x2028)}b@c.example",
    f"a{chr(0x2029)}b@c.example",
]
UNSUPPORTED_COUNTRIES = ["US", "XX", "es", "España", ""]
InvalidRow = tuple[dict[str, object], list[tuple[str, str]]]


def one_field(field: str, value: object, code: str) -> InvalidRow:
    """A row that changes one field and expects one error, in that field."""
    return ({field: value}, [(field, code)])


# What changes in the valid customer and the value that must be stored afterwards.
VALID_ROWS: list[tuple[dict[str, object], dict[str, str]]] = [
    ({"company_name": "  Ejemplo Uno SL "}, {"company_name": "Ejemplo Uno SL"}),
    ({"company_name": "AB"}, {"company_name": "AB"}),
    ({"company_name": "A" * 120}, {"company_name": "A" * 120}),
    # 120 code points, more than 120 bytes: lengths are measured in code points.
    ({"company_name": "ñé" * 60}, {"company_name": "ñé" * 60}),
    # 30 characters before normalizing: the limit of what is received.
    ({"tax_id": "12345678Z" + " " * 21}, {"tax_id": "12345678Z"}),
    ({"contact_email": "a@b.example"}, {"contact_email": "a@b.example"}),
    ({"contact_email": " a@b.example  "}, {"contact_email": "a@b.example"}),
    ({"contact_email": EMAIL_OF_255[1:]}, {"contact_email": EMAIL_OF_255[1:]}),
]

# What changes in the valid customer and the (field, code) pairs expected, in order.
INVALID_ROWS: list[InvalidRow] = [
    ({"company_name": " A "}, [("company_name", "too_short")]),
    ({"company_name": "    "}, [("company_name", "too_short")]),
    ({"company_name": "A" * 121}, [("company_name", "too_long")]),
    ({"company_name": "Ejemplo\nUno"}, [("company_name", "invalid_characters")]),
    ({"company_name": "\nEjemplo Uno"}, [("company_name", "invalid_characters")]),
    ({"company_name": "\tEjemplo Uno "}, [("company_name", "invalid_characters")]),
    ({"company_name": f"Ejemplo{ZERO_WIDTH_SPACE}Uno"}, [("company_name", "invalid_characters")]),
    # One error per field, the first: not `too_short`.
    ({"company_name": "A\n"}, [("company_name", "invalid_characters")]),
    ({"tax_id": LONG_TAX_ID}, [("tax_id", "too_long")]),
    ({"tax_id": LONG_TAX_ID, "country": "FR"}, [("tax_id", "too_long")]),
    ({"contact_email": "a\t@b.example"}, [("contact_email", "invalid_characters")]),
    ({"company_name": 123}, [("company_name", "not_a_string")]),
    *[one_field("contact_email", email, "invalid_email") for email in INVALID_EMAILS],
    *[one_field("contact_email", email, "invalid_email") for email in SEPARATOR_EMAILS],
    ({"contact_email": EMAIL_OF_255}, [("contact_email", "too_long")]),
    *[one_field("country", code, "unsupported_country") for code in UNSUPPORTED_COUNTRIES],
    *[one_field("plan", code, "unsupported_plan") for code in ("premium", "Starter", "")],
    *[one_field(field, ABSENT, "missing") for field in FIELDS],
    *[one_field(field, None, "not_a_string") for field in FIELDS],
    ({"id": 7}, [("id", "unknown_field")]),
    ({"created_at": "2026-11-12T14:30:00Z"}, [("created_at", "unknown_field")]),
    # With a country that is not valid, only what does not depend on it is checked (E-18).
    ({"country": "XX", "tax_id": "12345678A"}, [("country", "unsupported_country")]),
    (
        {"country": "XX", "tax_id": LONG_TAX_ID},
        [("tax_id", "too_long"), ("country", "unsupported_country")],
    ),
    (
        {"country": "XX", "tax_id": ABSENT},
        [("tax_id", "missing"), ("country", "unsupported_country")],
    ),
    (
        {"country": "XX", "tax_id": 123},
        [("tax_id", "not_a_string"), ("country", "unsupported_country")],
    ),
    ({"country": ABSENT, "tax_id": "12345678A"}, [("country", "missing")]),
    (
        {"country": 34, "tax_id": LONG_TAX_ID},
        [("tax_id", "too_long"), ("country", "not_a_string")],
    ),
    (
        {"company_name": "A", "contact_email": "sin-arroba.example"},
        [("company_name", "too_short"), ("contact_email", "invalid_email")],
    ),
    (
        {"plan": "premium", "company_name": "A", "zeta": 1},
        [("company_name", "too_short"), ("plan", "unsupported_plan"), ("zeta", "unknown_field")],
    ),
]

# Not rows of 5.7: the two errors of the identifier (5.3 and 5.4) and the order of 2.12.
EXTRA_INVALID_ROWS: list[InvalidRow] = [
    ({"tax_id": "12345678A"}, [("tax_id", "invalid_tax_id_check_character")]),
    ({"tax_id": "1234567Z"}, [("tax_id", "invalid_tax_id_format")]),
    ({"tax_id": "123", "country": "PT"}, [("tax_id", "invalid_tax_id_format")]),
    ({"contact_email": ""}, [("contact_email", "invalid_email")]),
    ({"contact_email": "a@b.example."}, [("contact_email", "invalid_email")]),
    # Every field with an error at once, and the unknown ones last, by name.
    (
        {
            "zeta": 1,
            "plan": "x",
            "country": "XX",
            "contact_email": "x",
            "tax_id": 1,
            "company_name": "",
            "alfa": 2,
        },
        [
            ("company_name", "too_short"),
            ("tax_id", "not_a_string"),
            ("contact_email", "invalid_email"),
            ("country", "unsupported_country"),
            ("plan", "unsupported_plan"),
            ("alfa", "unknown_field"),
            ("zeta", "unknown_field"),
        ],
    ),
]


def customer_with(changes: Mapping[str, object]) -> dict[str, object]:
    """The valid customer with some fields changed; `ABSENT` leaves a field out."""
    fields = {**VALID_CUSTOMER, **changes}
    return {name: value for name, value in fields.items() if value is not ABSENT}
