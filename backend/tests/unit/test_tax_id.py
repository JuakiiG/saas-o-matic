"""Tax identifier: normalization and validation (SPEC-01: rules 2.2 to 2.8, tables 5.1 to 5.6)."""

import pytest

from app.domain.tax_id import TaxIdProblem, normalize_tax_id, tax_id_problem

FORMAT = TaxIdProblem.FORMAT
CHECK = TaxIdProblem.CHECK_CHARACTER
DNI_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"
ENTITY_LETTERS = "ABCDEFGHJNPQRSUVW"
LETTER_ONLY = "PQRSNW"
DIGIT_ONLY = "ABEH"
CONTROL_LETTERS = "JABCDEFGHI"
# Written by code point: they look like `8`, a space, `f` and `fi`, and are not.
FULLWIDTH_EIGHT = chr(0xFF18)
NO_BREAK_SPACE = chr(0x00A0)
LONG_S = chr(0x017F)
LIGATURE_FI = chr(0xFB01)
# Table 5.1: what is received and its normalized form.
NORMALIZATION_ROWS = [
    ("12345678Z", "12345678Z"),
    ("12345678z", "12345678Z"),
    ("12345678-Z", "12345678Z"),
    ("12.345.678-Z", "12345678Z"),
    (" 12 345 678 z ", "12345678Z"),
    ("x-1234567-l", "X1234567L"),
    ("b-1234567 4", "B12345674"),
]
# Table 5.2: valid Spanish identifiers.
VALID_SPANISH = [
    *("12345678Z", "00000000T", "99999997E", "99999998T", "99999999R"),
    *("X0000000T", "X1234567L", "Y0000000Z", "Y1234567X", "Z0000000M", "Z9999999H"),
    *("A12345674", "B12345674", "E99999997", "H00000000", "A24680241"),
    *("P1234567D", "Q9999999G", "S0000000J", "P1111111I"),
]
# Table 5.3: the pattern fits and the last character is not the right one.
WRONG_CHECK_CHARACTER = [
    *("12345678A", "12345678I", "X1234567T", "Y0000000T"),
    *("A12345675", "A1234567D", "P12345674", "P1234567E", "P1234567K"),
]
# Table 5.4: no Spanish pattern fits. The first row of the table gives two entries.
WRONG_FORMAT = [
    *("", " - - ", "1234567Z", "123456789Z", "12345678", "12345678/Z", "ES12345678Z"),
    *("1234567AZ", "X123456L", "I12345674", "O12345674", "T12345674", "K1234567D"),
    # A digit and a letter that are not ASCII, and a space that is not U+0020.
    *(f"1234567{FULLWIDTH_EIGHT}Z", "1234567ÑZ", f"12345678{NO_BREAK_SPACE}Z"),
    # Unicode `upper()` would turn it into `12345679S`, a DNI with the right letter.
    f"12345679{LONG_S}",
]
# Table 5.5: entity letters whose form has no official source (D-01). Number 1234567, C = 4.
CIF_FORM_ROWS = [
    *[(f"{letter}1234567D", None) for letter in "NRW"],
    *[(f"{letter}12345674", CHECK) for letter in "NRW"],
    *[(f"{letter}12345674", None) for letter in "CDFGJUV"],
    *[(f"{letter}1234567D", None) for letter in "CDFGJUV"],
    ("C12345675", CHECK),
    ("C1234567E", CHECK),
]
# Table 5.6: country, what is received, its normalized form and the result.
FOREIGN_ROWS = [
    ("FR", "ab-12 34", "AB1234", None),
    ("PT", "1234", "1234", None),
    ("DE", "A1B2C3D4E5F6G7H8I9J0", "A1B2C3D4E5F6G7H8I9J0", None),
    ("PT", "123", "123", FORMAT),
    ("DE", "A1B2C3D4E5F6G7H8I9J0K", "A1B2C3D4E5F6G7H8I9J0K", FORMAT),
    ("IT", "1234.5678", "12345678", None),
    ("IT", "1234/5678", "1234/5678", FORMAT),
    ("FR", "12345678A", "12345678A", None),
    # Unicode `upper()` would turn the ligature into `FI1234`, which would be valid.
    ("FR", f"{LIGATURE_FI}1234", f"{LIGATURE_FI}1234", FORMAT),
    ("FR", f"AB{NO_BREAK_SPACE}1234", f"AB{NO_BREAK_SPACE}1234", FORMAT),
]
UNTOUCHED_BY_NORMALIZATION = [LIGATURE_FI, LONG_S, "ñ", "é", NO_BREAK_SPACE, "/", "\t"]


def spanish_problem(received: str) -> TaxIdProblem | None:
    return tax_id_problem("ES", normalize_tax_id(received))


@pytest.mark.parametrize(("received", "normalized"), NORMALIZATION_ROWS)
def test_tax_id_is_normalized_before_it_is_validated(received: str, normalized: str) -> None:
    """SPEC-01/E-08: no spaces, hyphens or dots, and `a`-`z` in upper case (5.1, CA-01)."""
    assert normalize_tax_id(received) == normalized
    assert tax_id_problem("ES", normalized) is None


@pytest.mark.parametrize("received", UNTOUCHED_BY_NORMALIZATION, ids=ascii)
def test_normalization_changes_nothing_outside_its_three_signs_and_ascii_letters(
    received: str,
) -> None:
    """SPEC-01/E-08: an explicit letter by letter mapping, never Unicode `upper()` (2.2)."""
    assert normalize_tax_id(f"a{received}b") == f"A{received}B"


@pytest.mark.parametrize("received", VALID_SPANISH)
def test_spanish_identifier_with_the_right_check_character_is_valid(received: str) -> None:
    """SPEC-01/E-10, SPEC-01/E-11, SPEC-01/E-12, SPEC-01/E-13: every row of 5.2 (CA-02)."""
    assert normalize_tax_id(received) == received
    assert spanish_problem(received) is None


@pytest.mark.parametrize("received", WRONG_CHECK_CHARACTER)
def test_spanish_identifier_with_a_wrong_check_character_is_rejected(received: str) -> None:
    """SPEC-01/E-16: every row of 5.3 is an error of check character, not of format (CA-02)."""
    assert spanish_problem(received) is CHECK


@pytest.mark.parametrize("received", WRONG_FORMAT, ids=ascii)
def test_spanish_identifier_that_fits_no_pattern_is_a_format_error(received: str) -> None:
    """SPEC-01/E-15, SPEC-01/E-09, SPEC-01/E-10: every row of 5.4; nothing is padded (CA-02)."""
    assert spanish_problem(received) is FORMAT


@pytest.mark.parametrize("received", ["123456789", "X12345678", "Y00000001"])
def test_dni_or_nie_that_ends_in_a_digit_is_a_format_error(received: str) -> None:
    """SPEC-01/E-10, SPEC-01/E-15: the patterns of DNI and NIE end in a letter (2.3).

    Not a row of the tables: only the CIF admits a digit as its last character.
    """
    assert spanish_problem(received) is FORMAT


@pytest.mark.parametrize("remainder", range(23))
def test_dni_accepts_only_the_letter_of_its_remainder(remainder: int) -> None:
    """SPEC-01/E-11: the 23 letters of the table, one number per remainder (CA-03)."""
    # 99999975 is a multiple of 23, so the remainder of the number is `remainder`.
    number = 99_999_975 + remainder
    results = {letter: tax_id_problem("ES", f"{number}{letter}") for letter in DNI_LETTERS}
    expected = dict.fromkeys(DNI_LETTERS, CHECK) | {DNI_LETTERS[remainder]: None}
    assert number % 23 == remainder
    assert results == expected


@pytest.mark.parametrize("entity", ENTITY_LETTERS)
def test_cif_accepts_exactly_the_form_of_the_group_of_its_entity_letter(entity: str) -> None:
    """SPEC-01/E-13: the 17 entity letters by the 10 control values, in both forms (CA-04)."""
    for second_digit in range(10):
        # Only the second digit is not zero, so the sum is that digit.
        control = (10 - second_digit) % 10
        body = f"{entity}0{second_digit}00000"
        as_digit = tax_id_problem("ES", f"{body}{control}")
        as_letter = tax_id_problem("ES", f"{body}{CONTROL_LETTERS[control]}")
        assert as_digit is (CHECK if entity in LETTER_ONLY else None), body
        assert as_letter is (CHECK if entity in DIGIT_ONLY else None), body
        assert tax_id_problem("ES", f"{body}{(control + 1) % 10}") is CHECK, body


@pytest.mark.parametrize(("received", "problem"), CIF_FORM_ROWS)
def test_cif_of_an_entity_letter_without_official_source_follows_its_group(
    received: str, problem: TaxIdProblem | None
) -> None:
    """SPEC-01/E-13: every row of 5.5 (CA-04)."""
    assert spanish_problem(received) is problem


@pytest.mark.parametrize(("country", "received", "normalized", "problem"), FOREIGN_ROWS, ids=ascii)
def test_identifier_outside_spain_only_needs_4_to_20_alphanumeric_characters(
    country: str, received: str, normalized: str, problem: TaxIdProblem | None
) -> None:
    """SPEC-01/E-14, SPEC-01/E-15: every row of 5.6; no check character is calculated (CA-05)."""
    assert normalize_tax_id(received) == normalized
    assert tax_id_problem(country, normalized) is problem
