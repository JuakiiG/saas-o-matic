"""Translation of the framework's validation errors to the errors of the contract.

Index of specs, "Errores de validación": one error per field, the first that
fails, in the order of the fields of the contract; then the unknown fields.
"""

from collections.abc import Iterator, Mapping, Sequence
from typing import Any

from app.api.problems import FieldCode, FieldError

# Error types of Pydantic that have a code in the contract, with the message to show.
# A field is declared strict, so `"15"`, `15.0`, `true` and `null` all arrive as `int_type`.
# The limit of a message comes from the error itself, where it is an exact integer: the
# OpenAPI document publishes the limits as decimals.
TRANSLATIONS = {
    "missing": (FieldCode.MISSING, "Campo obligatorio."),
    "extra_forbidden": (FieldCode.UNKNOWN_FIELD, "Campo no documentado."),
    "int_type": (FieldCode.NOT_AN_INTEGER, "Debe ser un número entero."),
    "greater_than_equal": (FieldCode.OUT_OF_RANGE, "Debe ser mayor o igual que {ge}."),
    "less_than_equal": (FieldCode.OUT_OF_RANGE, "Debe ser menor o igual que {le}."),
}
WHOLE_BODY = ("body",)


class UntranslatedValidationError(Exception):
    """A validation failed with an error that the contract has no code for: a bug of ours."""


# `Any` in the values of both parameters: they are what Pydantic and the OpenAPI document give.
def field_errors(
    raw_errors: Sequence[Mapping[str, Any]], body_schema: Mapping[str, Any]
) -> tuple[FieldError, ...]:
    """The errors of the contract for the raw errors of one request."""
    position = {name: index for index, name in enumerate(body_schema.get("properties", {}))}
    first: dict[str, FieldError] = {}
    for field, raw in _failed_fields(raw_errors, body_schema):
        if field not in first:
            first[field] = _field_error(field, raw)
    # A stable sort: the unknown fields keep the order of the request, after the known ones.
    return tuple(sorted(first.values(), key=lambda error: position.get(error.field, len(position))))


def _failed_fields(
    raw_errors: Sequence[Mapping[str, Any]], body_schema: Mapping[str, Any]
) -> Iterator[tuple[str, Mapping[str, Any]]]:
    """Each failure with the field it belongs to."""
    for raw in raw_errors:
        if tuple(raw["loc"]) == WHOLE_BODY:
            # No body at all: the same as `{}`, every required field fails.
            yield from ((name, raw) for name in body_schema.get("required", []))
        else:
            # The location is (where, field, ...): what follows the field is detail of
            # the framework, such as which of several admitted types failed.
            yield str(raw["loc"][1]), raw


def _field_error(field: str, raw: Mapping[str, Any]) -> FieldError:
    translation = TRANSLATIONS.get(raw["type"])
    if translation is None:
        raise UntranslatedValidationError(f"{field}: {raw['type']}")
    code, message = translation
    return FieldError(field, code, message.format_map(raw.get("ctx", {})))
