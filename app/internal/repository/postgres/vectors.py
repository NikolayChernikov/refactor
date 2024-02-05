from typing import List

from app.internal.repository.postgres.connection import get_connection
from app.internal.repository.postgres.handlers.collect_response import collect_response
from app.internal.repository.repository import Repository
from app.pkg import models
from app.pkg.models import CreateRequestCommand
from app.pkg.models.base import Model
from app.pkg.models.requests import Vector

__all__ = [
    "Vectors",
]


class Vectors(Repository):
    def get_tmp(self, cmd: List[Vector], request_id: int) -> str:
        res = []
        for i in cmd:
            res.append(
                f"({request_id}, '{i.vector}')",
            )
        return ", ".join(res)

    @collect_response
    async def create(self, request_id: int, cmd: List[Vector]) -> List[Vector]:
        params = self.get_tmp(cmd, request_id)
        q = f"""
                insert into vectors (request_id, vector)
                values {params} on conflict (request_id, vector)
                do nothing returning request_id, vector
            """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def read(self, request_id: int) -> Vector:
        q = """
                select request_id, vector
                from vectors
                where request_id = %(request_id)s
            """
        async with get_connection() as cur:
            await cur.execute(q, {"request_id": request_id})
            return await cur.fetchone()

    @collect_response
    async def read_all(self) -> List[Vector]:
        q = """
                select request_id, vector
                from vectors
            """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    async def update(self, cmd: Model) -> Model:
        raise NotImplementedError

    @collect_response
    async def delete(self, request_id: int) -> List[Vector]:
        q = """
                delete from vectors where request_id = %(request_id)s
                returning request_id, vector
            """
        async with get_connection() as cur:
            await cur.execute(q, {"request_id": request_id})
            return await cur.fetchall()
