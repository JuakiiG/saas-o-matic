"""Tax identifier of a customer: normalization and validation by country (SPEC-01, 2.2 to 2.8).

Nothing here uses `str.upper()`, `str.isdigit()` or `str.isalnum()`: they follow Unicode,
and would take a full-width digit for a digit or turn a ligature into two ASCII letters.
"""

from enum import Enum

SPAIN = "ES"
DIGITS = "0123456789"
UPPER_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER_LETTERS = "abcdefghijklmnopqrstuvwxyz"
# Removed wherever they are: the space U+0020, the hyphen and the dot. Nothing else.
IGNORED_SIGNS = " -."
_TO_UPPER = dict(zip(LOWER_LETTERS, UPPER_LETTERS, strict=True))

SPANISH_LENGTH = 9
DNI_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"
NIE_PREFIXES = {"X": "0", "Y": "1", "Z": "2"}
# Entity letters of a CIF, by the form of control that each one demands (D-01).
CIF_LETTER_ONLY = "PQRSNW"
CIF_DIGIT_ONLY = "ABEH"
CIF_EITHER_FORM = "CDFGJUV"
CIF_CONTROL_LETTERS = "JABCDEFGHI"
FOREIGN_MIN_LENGTH = 4
FOREIGN_MAX_LENGTH = 20


class TaxIdProblem(Enum):
    """Why a normalized identifier is not valid for its country."""

    FORMAT = "format"
    CHECK_CHARACTER = "check_character"


def normalize_tax_id(raw: str) -> str:
    """Drop spaces, hyphens and dots and put `a`-`z` in upper case, letter by letter."""
    kept = (character for character in raw if character not in IGNORED_SIGNS)
    return "".join(_TO_UPPER.get(character, character) for character in kept)


def tax_id_problem(country_code: str, normalized: str) -> TaxIdProblem | None:
    """What is wrong with a normalized identifier in its country, or None if it is valid."""
    if country_code == SPAIN:
        return _spanish_problem(normalized)
    return _foreign_problem(normalized)


def _foreign_problem(normalized: str) -> TaxIdProblem | None:
    """Outside Spain no check character is calculated (A10): only length and alphabet."""
    right_length = FOREIGN_MIN_LENGTH <= len(normalized) <= FOREIGN_MAX_LENGTH
    if right_length and _all_in(normalized, DIGITS + UPPER_LETTERS):
        return None
    return TaxIdProblem.FORMAT


def _spanish_problem(normalized: str) -> TaxIdProblem | None:
    """DNI, NIE or CIF. No pattern: format. A pattern and another last character: control."""
    if len(normalized) != SPANISH_LENGTH:
        return TaxIdProblem.FORMAT
    first, middle, last = normalized[0], normalized[1:8], normalized[8]
    if not _all_in(middle, DIGITS):
        return TaxIdProblem.FORMAT
    if first in DIGITS or first in NIE_PREFIXES:
        # DNI or NIE: the pattern ends in a letter; a NIE is a DNI once its prefix is a digit.
        last_alphabet = UPPER_LETTERS
        accepted = _dni_letter(NIE_PREFIXES.get(first, first) + middle)
    else:
        # CIF: the pattern ends in a digit or a letter; no accepted control, no entity letter.
        last_alphabet = DIGITS + UPPER_LETTERS
        accepted = _cif_controls(first, middle)
    if not accepted or last not in last_alphabet:
        return TaxIdProblem.FORMAT
    return None if last in accepted else TaxIdProblem.CHECK_CHARACTER


def _dni_letter(eight_digits: str) -> str:
    return DNI_LETTERS[int(eight_digits) % len(DNI_LETTERS)]


def _cif_controls(entity: str, seven_digits: str) -> str:
    """The control of a CIF as a digit, as a letter or both, by the group of its entity letter."""
    value = _cif_control_value(seven_digits)
    digit, letter = DIGITS[value], CIF_CONTROL_LETTERS[value]
    if entity in CIF_LETTER_ONLY:
        return letter
    if entity in CIF_DIGIT_ONLY:
        return digit
    if entity in CIF_EITHER_FORM:
        return digit + letter
    return ""


def _cif_control_value(seven_digits: str) -> int:
    evens = sum(int(digit) for digit in seven_digits[1::2])
    # Of the digits in odd positions, the sum of the figures of their double.
    odds = sum(sum(divmod(2 * int(digit), 10)) for digit in seven_digits[0::2])
    return (10 - (evens + odds) % 10) % 10


def _all_in(text: str, alphabet: str) -> bool:
    return all(character in alphabet for character in text)
