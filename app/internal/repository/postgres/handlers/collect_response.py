"""Collect response module."""
import functools
from datetime import datetime
from functools import wraps
from typing import Dict, List, Union

import pydantic
from psycopg2.extras import RealDictRow

from app.internal.repository.postgres.handlers.handle_exception import handle_exception
from app.pkg.models.base import Model
from app.pkg.models.exceptions.repository import EmptyResult


def collect_response(  # noqa: C901
    fn=None,
    convert_to_pydantic=True,
    nullable=False,
) -> None:
    """Save image.

    Args:
        fn: bool arg.
        convert_to_pydantic: bool arg.
        nullable: bool arg.

    Returns: None.
    """
    # fn is None when params for decorator are provided
    if fn is None:
        return functools.partial(
            collect_response,
            convert_to_pydantic=convert_to_pydantic,
            nullable=nullable,
        )

    @wraps(fn)
    @handle_exception
    async def inner(*args: object, **kwargs: object) -> Union[List[Model], Model, None]:
        response = await fn(*args, **kwargs)
        if not response:
            # some responses are empty lists we should allow them.
            # isinstance cannot digest List[int], only List, so __origin__ is used

            if "return" in fn.__annotations__:
                return_class = fn.__annotations__["return"]
                if hasattr(return_class, "__origin__"):
                    return_class = return_class.__origin__
                if isinstance([], return_class):
                    return []
                if nullable:
                    return None

            raise EmptyResult

        if convert_to_pydantic:
            return pydantic.parse_obj_as(
                (ann := fn.__annotations__["return"]),
                await __convert_response(response=response, annotations=str(ann)),
            )

        return response

    return inner


async def __convert_response(response: RealDictRow, annotations: str):
    """
    Converts the response of the request to a List of models or to a single model.
    Args:
        response: Response of aiopg query.
        annotations: Annotations of `fn`.

    Returns: List[`Model`] if List is specified in the type annotations,
            or a single `Model` if `Model` is specified in the type annotations.
    """
    r = response.copy()
    if annotations.replace("typing.", "").startswith("List"):
        return [await __convert_memory_viewer(item) for item in r]
    return await __convert_memory_viewer(r)


async def __convert_memory_viewer(r: Union[RealDictRow, Dict]):  # noqa: C901
    """Convert memory viewer in bytes.

    Notes: aiopg returns memory viewer in query response,
        when in database type of cell `bytes`.
    """
    for key, value in r.items():
        if isinstance(value, memoryview):
            r[key] = value.tobytes()
        elif isinstance(value, datetime):
            r[key] = int(value.timestamp())
        elif key == "time":
            try:
                new_time = datetime.strptime(str(value), "%Y-%m-%dT%H:%M:%S.%f")
            except Exception:  # pylint: disable=broad-exception-raised
                new_time = datetime.strptime(str(value), "%Y-%m-%d% H:%M:%S.%f")
            new_time_to_int = int(new_time.strftime("%s"))
            r[key] = new_time_to_int
        elif isinstance(value, List):
            result = []
            for i in value:
                if i and isinstance(i, Dict):
                    convert_list = await __convert_memory_viewer(i)
                    result.append(convert_list)
                else:
                    result.append(i)
            r[key] = result
    return r
