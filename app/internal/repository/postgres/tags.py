from typing import List

from app.internal.repository.postgres.connection import get_connection
from app.internal.repository.postgres.handlers.collect_response import collect_response
from app.internal.repository.repository import Repository
from app.pkg import models
from app.pkg.models import RequestTagBlock, Tag
from app.pkg.models.base import Model

__all__ = [
    "Tags",
]


class Tags(Repository):
    def get_tmp(self, request_id: int, cmd: List[Tag]):
        res = []
        for i in cmd:
            res.append(
                f"({request_id}, {i.id})",
            )
        return ", ".join(res)

    @collect_response
    async def create(self, request_id: int, cmd: List[Tag]) -> List[RequestTagBlock]:
        params = self.get_tmp(request_id, cmd)
        q = f"""
                insert into request_tag (request_id, tag_id)
                values {params}
                on conflict (request_id, tag_id) do nothing
                returning request_id, tag_id
            """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def read(self, request_id: int) -> List[Tag]:
        q = """
                select tags.id, tags.tag from tags
                join request_tag on request_tag.tag_id = tags.id
                where request_tag.request_id = %(request_id)s
            """
        async with get_connection() as cur:
            await cur.execute(q, {"request_id": request_id})
            return await cur.fetchall()

    @collect_response
    async def read_all(self) -> List[models.Tag]:
        q = """
                select id, tag from tags
            """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    async def update(self, cmd: Model) -> Model:
        raise NotImplementedError

    @collect_response
    async def delete(self, request_id: int) -> List[models.RequestTagBlock]:
        q = """
                delete from request_tag where 
                request_id = %(request_id)s
                returning request_id, tag_id
            """
        async with get_connection() as cur:
            await cur.execute(q, {"request_id": request_id})
            return await cur.fetchall()
