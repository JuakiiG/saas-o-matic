"""The identifiers of the contract: integers from 1 to the largest INTEGER of SQLite.

Index of specs, "Identificadores": out of that range, `out_of_range`; not an integer,
`not_an_integer`. One definition for the body and one for the route.
"""

import re
from typing import Annotated

from fastapi import Path
from pydantic import BeforeValidator, Field
from pydantic_core import PydanticCustomError

MAX_ID = 9223372036854775807
# The only writing of an integer in the route: `0`, or an optional minus sign and ASCII
# digits without leading zeros. `[0-9]` and not `\d`, which also takes digits of other scripts.
ROUTE_INTEGER = re.compile(r"0|-?[1-9][0-9]*")


def _only_form_of_an_integer(text: str) -> str:
    """The text, if it is written as the one form of an integer; if not, it is not an integer.

    The library would also read `1.0`, `+1`, `01`, ` 1` and `1_0` (as 10): one customer
    would have several addresses.
    """
    if ROUTE_INTEGER.fullmatch(text) is None:
        # The type of error that the library raises for a text that is not an integer.
        raise PydanticCustomError("int_parsing", "not written as an integer")
    return text


# In a JSON body: strict, so `"1"`, `1.0`, `true` and `null` are rejected, not converted.
BodyId = Annotated[int, Field(strict=True, ge=1, le=MAX_ID)]
# In the route, where everything is text. The contract calls the field `id`. The form is
# checked first and the range afterwards: `0` and `-1` are integers out of range. The check
# of the form is written after the limits on purpose: written before them, the OpenAPI
# document publishes `ge` and `le`, which are not JSON Schema, instead of the limits.
PathId = Annotated[
    int, Path(alias="id", ge=1, le=MAX_ID), BeforeValidator(_only_form_of_an_integer)
]
