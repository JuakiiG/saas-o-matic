"""The identifiers of the contract: integers from 1 to the largest INTEGER of SQLite.

Index of specs, "Identificadores": out of that range, `out_of_range`; not an integer,
`not_an_integer`. One definition for the body and one for the route.
"""

from typing import Annotated

from fastapi import Path
from pydantic import Field

MAX_ID = 9223372036854775807

# In a JSON body: strict, so `"1"`, `1.0`, `true` and `null` are rejected, not converted.
BodyId = Annotated[int, Field(strict=True, ge=1, le=MAX_ID)]
# In the route, where everything is text. The contract calls the field `id`.
PathId = Annotated[int, Path(alias="id", ge=1, le=MAX_ID)]
