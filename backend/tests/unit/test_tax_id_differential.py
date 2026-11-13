"""The validator of the domain against an independent one, `python-stdnum` (SPEC-01, CA-19).

The cases of the spec were generated with the algorithm they test, so on their own
they only prove that it is consistent with itself. Expected: whatever the domain
accepts, `python-stdnum` accepts too, and the only identifiers that `python-stdnum`
accepts and the domain rejects are CIF with the right control value written in a
form that the group of its entity letter does not admit (D-01). Any other
difference fails the test, and the Tech Lead decides about it.
"""

import random

from stdnum.es import nif

from app.domain.tax_id import tax_id_problem

SEED = 20261112
RANDOM_NUMBERS = 10_000
DNI_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"
NIE_PREFIXES = "XYZ"
ENTITY_LETTERS = "ABCDEFGHJNPQRSUVW"
LETTER_ONLY = "PQRSNW"
DIGIT_ONLY = "ABEH"
CONTROL_LETTERS = "JABCDEFGHI"


def cif_control(digits: str) -> int:
    """The control value of 2.6, written again here so that the test owes nothing to the domain."""
    evens = sum(int(digit) for digit in digits[1::2])
    odds = sum(sum(divmod(2 * int(digit), 10)) for digit in digits[0::2])
    return (10 - (evens + odds) % 10) % 10


def is_right_value_in_a_form_not_admitted(identifier: str) -> bool:
    """The only difference that D-01 explains."""
    entity, digits, last = identifier[0], identifier[1:8], identifier[8]
    control = cif_control(digits)
    digit_where_letter = entity in LETTER_ONLY and last == str(control)
    letter_where_digit = entity in DIGIT_ONLY and last == CONTROL_LETTERS[control]
    return entity in ENTITY_LETTERS and (digit_where_letter or letter_where_digit)


def every_cif_form() -> list[str]:
    """17 entity letters x 10 control values x 2 forms: 340 identifiers with the right value."""
    identifiers = []
    for entity in ENTITY_LETTERS:
        for second_digit in range(10):
            digits = f"0{second_digit}00000"
            control = cif_control(digits)
            identifiers += [
                f"{entity}{digits}{control}",
                f"{entity}{digits}{CONTROL_LETTERS[control]}",
            ]
    return identifiers


def random_identifiers() -> list[str]:
    """For each random number: a DNI, a NIE and a CIF, each right and each wrong."""
    generator = random.Random(SEED)  # noqa: S311 -- fixed seed for a repeatable test, no secret
    identifiers = []
    for _ in range(RANDOM_NUMBERS):
        number = generator.randrange(10**8)
        dni, short = f"{number:08d}", f"{number % 10**7:07d}"
        prefix = number % 3
        nie_remainder = int(f"{prefix}{short}") % 23
        entity = ENTITY_LETTERS[number % 17]
        control = cif_control(short)
        # The form of the right CIF: the one of its group, or one of the two in turn.
        as_letter = entity in LETTER_ONLY or (entity not in DIGIT_ONLY and number % 2 == 0)
        right = CONTROL_LETTERS[control] if as_letter else str(control)
        wrong = CONTROL_LETTERS[(control + 1) % 10] if as_letter else str((control + 1) % 10)
        identifiers += [
            f"{dni}{DNI_LETTERS[number % 23]}",
            f"{dni}{DNI_LETTERS[(number + 1) % 23]}",
            f"{NIE_PREFIXES[prefix]}{short}{DNI_LETTERS[nie_remainder]}",
            f"{NIE_PREFIXES[prefix]}{short}{DNI_LETTERS[(nie_remainder + 1) % 23]}",
            f"{entity}{short}{right}",
            f"{entity}{short}{wrong}",
        ]
    return identifiers


def differences(identifiers: list[str]) -> tuple[list[str], list[str]]:
    """Identifiers that only the domain accepts and identifiers that only `python-stdnum` does."""
    only_domain, only_stdnum = [], []
    for identifier in identifiers:
        domain_accepts = tax_id_problem("ES", identifier) is None
        stdnum_accepts = nif.is_valid(identifier)
        if domain_accepts and not stdnum_accepts:
            only_domain.append(identifier)
        if stdnum_accepts and not domain_accepts:
            only_stdnum.append(identifier)
    return only_domain, only_stdnum


def test_every_form_of_cif_differs_from_stdnum_only_in_the_form_of_the_control() -> None:
    """SPEC-01/E-13: the 340 CIF with the right control value, in both forms (CA-19)."""
    identifiers = every_cif_form()
    only_domain, only_stdnum = differences(identifiers)
    assert len(set(identifiers)) == 340
    assert only_domain == []
    assert [item for item in only_stdnum if not is_right_value_in_a_form_not_admitted(item)] == []
    # 6 entity letters demand a letter and 4 a digit: 10 letters x 10 values in the other form.
    assert len(only_stdnum) == 100


def test_random_identifiers_are_judged_as_stdnum_judges_them() -> None:
    """SPEC-01/E-11, SPEC-01/E-12, SPEC-01/E-13: 10000 numbers with a fixed seed (CA-19)."""
    identifiers = random_identifiers()
    only_domain, only_stdnum = differences(identifiers)
    accepted = [item for item in identifiers if tax_id_problem("ES", item) is None]
    assert len(identifiers) == 6 * RANDOM_NUMBERS
    assert only_domain == []
    assert only_stdnum == []
    # Half of them were built right and half wrong.
    assert len(accepted) == 3 * RANDOM_NUMBERS
