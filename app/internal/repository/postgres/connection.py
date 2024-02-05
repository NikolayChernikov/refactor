from contextlib import asynccontextmanager

from aiopg.connection import Cursor
from dependency_injector.wiring import Provide, inject
from psycopg2.extras import RealDictCursor

from app.pkg.connectors import Connectors, Postgres

__all__ = [
    "get_connection",
]


@asynccontextmanager
@inject
async def get_connection(
    postgres: Postgres = Provide[Connectors.postgres],
) -> Cursor:
    """Get async connection to postgresql of pool."""
    async with postgres.get_connect() as connection:
        async with (await connection.cursor(cursor_factory=RealDictCursor)) as cur:
            yield cur
