"""Postgresql connector."""

from contextlib import asynccontextmanager

import aiopg
import pydantic
from aiopg import Connection

from .base_connector import BaseConnector

__all__ = ["Postgres"]


class Postgres(BaseConnector):
    """Postgres class."""

    _username: str
    _password: str
    _host: str
    _port: pydantic.PositiveInt
    _database_name: str

    def __init__(  # pylint: disable=too-many-arguments
        self,
        username: str,
        password: pydantic.SecretStr,
        host: str,
        port: pydantic.PositiveInt,
        database_name: str,
    ):
        self._pool = None
        self._username = username
        self._password = password.get_secret_value()
        self._host = host
        self._port = port
        self._database_name = database_name

    def get_dsn(self):
        """Description of ``BaseConnector.get_dsn``."""
        return (
            f"postgresql://"
            f"{self._username}:"
            f"{self._password}@"
            f"{self._host}:{self._port}/"
            f"{self._database_name}"
        )

    @asynccontextmanager
    async def get_connect(self) -> Connection:
        if self._pool is None:
            self._pool = aiopg.create_pool(dsn=self.get_dsn())

        async with self._pool as pool:
            async with pool.acquire() as conn:
                yield conn
