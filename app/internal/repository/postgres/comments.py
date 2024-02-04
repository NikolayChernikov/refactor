from typing import List

from app.internal.repository.postgres.handlers.collect_response import collect_response
from app.internal.repository.postgres.connection import get_connection
from app.internal.repository.repository import Repository
from app.pkg import models
from app.pkg.models.base import Model


__all__ = [
    "Comments",
]


class Comments(Repository):

    @collect_response
    async def create(self, cmd: models.Comment) -> models.Comment:
        q = """
                insert into comments (request_id, comment, author, time, author_role)
                values (%(request_id)s, %(comment)s, %(author)s, now(), %(author_role)s)
                returning id, request_id, comment, author, time, author_role
            """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, request_id: int) -> List[models.Comment]:
        q = """
                select id, comment, author, time, author_role, request_id from comments
                where request_id = %(request_id)s
            """
        async with get_connection() as cur:
            await cur.execute(q, {"request_id": request_id})
            return await cur.fetchall()

    async def read_all(self) -> List[Model]:
        raise NotImplementedError

    async def update(self, cmd: Model) -> Model:
        raise NotImplementedError

    async def delete(self, cmd: Model) -> Model:
        raise NotImplementedError

