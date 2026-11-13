"""Translation of the framework's validation errors to the errors of the contract.

Index of specs, "Errores de validación": one error per field, the first that
fails, in the order of the fields of the contract; then the unknown fields,
in alphabetical order of their name.
"""

from collections.abc import Iterable, Iterator, Sequence

from pydantic_core import ErrorDetails

from app.api.contract import OpenApiObject
from app.api.problems import FieldCode, FieldError

# Error types of Pydantic that have a code in the contract, with the message to show.
# A field is declared strict, so `"15"`, `15.0`, `true` and `null` all arrive as `int_type`.
# The limit of a message comes from the error itself, where it is an exact integer: the
# OpenAPI document publishes the limits as decimals.
TRANSLATIONS = {
    "missing": (FieldCode.MISSING, "Campo obligatorio."),
    "extra_forbidden": (FieldCode.UNKNOWN_FIELD, "Campo no documentado."),
    "int_type": (FieldCode.NOT_AN_INTEGER, "Debe ser un número entero."),
    # In the route everything is text: what cannot be read as an integer is not one.
    "int_parsing": (FieldCode.NOT_AN_INTEGER, "Debe ser un número entero."),
    # Digits that the library refuses to read as a number because they are too many (more
    # than 4300): it is written as an integer, so it is one, and out of any range.
    "int_parsing_size": (FieldCode.OUT_OF_RANGE, "Está fuera del rango admitido."),
    "string_too_long": (FieldCode.TOO_LONG, "Debe tener {max_length} caracteres como máximo."),
    "greater_than_equal": (FieldCode.OUT_OF_RANGE, "Debe ser mayor o igual que {ge}."),
    "less_than_equal": (FieldCode.OUT_OF_RANGE, "Debe ser menor o igual que {le}."),
}
WHOLE_BODY = ("body",)


class UntranslatedValidationError(Exception):
    """A validation failed with an error that the contract has no code for: a bug of ours."""


def field_errors(
    raw_errors: Sequence[ErrorDetails], body_schema: OpenApiObject
) -> tuple[FieldError, ...]:
    """The errors of the contract for the raw errors of one request.

    The raw errors are the ones of Pydantic, with its own type; the schema of the body
    is the one that the OpenAPI document publishes.
    """
    first: dict[str, FieldError] = {}
    for field, raw in _failed_fields(raw_errors, body_schema):
        if field not in first:
            first[field] = _field_error(field, raw)
    return in_contract_order(first.values(), list(body_schema.get("properties", {})))


def in_contract_order(
    errors: Iterable[FieldError], contract_fields: Sequence[str]
) -> tuple[FieldError, ...]:
    """Fields of the contract in its order; then the unknown ones, by name (SPEC-01, 2.12)."""
    position = {name: index for index, name in enumerate(contract_fields)}

    def order(error: FieldError) -> tuple[bool, int, str]:
        return (error.field not in position, position.get(error.field, 0), error.field)

    return tuple(sorted(errors, key=order))


def _failed_fields(
    raw_errors: Sequence[ErrorDetails], body_schema: OpenApiObject
) -> Iterator[tuple[str, ErrorDetails]]:
    """Each failure with the field it belongs to."""
    for raw in raw_errors:
        if tuple(raw["loc"]) == WHOLE_BODY:
            # No body at all: the same as `{}`, every required field fails.
            yield from ((name, raw) for name in body_schema.get("required", []))
        else:
            # The location is (where, field, ...): what follows the field is detail of
            # the framework, such as which of several admitted types failed.
            yield str(raw["loc"][1]), raw


def _field_error(field: str, raw: ErrorDetails) -> FieldError:
    translation = TRANSLATIONS.get(raw["type"])
    if translation is None:
        raise UntranslatedValidationError(f"{field}: {raw['type']}")
    code, message = translation
    return FieldError(field, code, message.format_map(raw.get("ctx", {})))
