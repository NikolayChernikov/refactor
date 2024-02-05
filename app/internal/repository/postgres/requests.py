from typing import List

from app.internal.repository.postgres.connection import get_connection
from app.internal.repository.postgres.handlers.collect_response import collect_response
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = [
    "Requests",
]


class Requests(Repository):
    @collect_response
    async def read_all(self) -> List[models.Request]:
        q = """
            select
                id,
                title,
                description,
                assets,
                status,
                created_timestamp,
                updated_timestamp,
                type,
                creator,
                creator_role,
                updator,
                messages_ids,
                priority,
                comments,
                tags as is_tags,
                is_all_vectors,
                sites,
                deadline
            from requests
            order by created_timestamp desc;
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def read_full_data(self, time_from, time_to) -> List[models.RequestFull]:
        q = f"""
                select
                    requests.id, title, description, assets, status, created_timestamp, updated_timestamp,
                    type, creator, updator, messages_ids, priority, comments, tags as is_tags,
                    is_all_vectors, sites, deadline, creator_role,
                    json_strip_nulls(
                                    json_agg(
                                        json_build_object(
                                            'request_id', vectors.request_id,
                                            'vector', vectors.vector
                                        )
                                    )
                                ) as vectors,
                
                        json_strip_nulls(
                                    json_agg(
                                        json_build_object(
                                            'id', tags.id,
                                            'tag', tags.tag
                                        )
                                    )
                                ) as tags,
                        json_strip_nulls(
                            json_agg(
                                json_build_object(
                                    'id', comments.id,
                                    'request_id', comments.request_id,
                                    'comment', comments.comment,
                                    'author', comments.author,
                                    'author_role', comments.author_role,
                                    'time', comments.time
                                )
                                order by time asc
                            )
                        ) as comments_objects
                from requests
                left join vectors on vectors.request_id = requests.id
                left join request_tag on requests.id = request_tag.request_id
                left join tags on tags.id = request_tag.tag_id
                left join comments on requests.id = comments.request_id
                where (updated_timestamp > '{time_from}' and updated_timestamp < '{time_to}') or 
                (status = 'в работе' or status = 'в очереди')
                group by requests.id, title, description, assets, status, created_timestamp, updated_timestamp,
                    type, creator, updator, priority, comments, is_tags, creator_role,
                    is_all_vectors, sites, deadline
                order by updated_timestamp desc;
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def create(self, cmd: models.CreateRequestCommand) -> models.Request:
        q = """
            insert into requests (
                title, 
                description, 
                assets, 
                updated_timestamp,
                type,
                creator,
                updator,
                messages_ids,
                priority,
                tags,
                is_all_vectors,
                sites,
                creator_role,
                deadline
            ) values (
                %(title)s, 
                %(description)s, 
                %(assets)s, 
                current_timestamp,
                %(type)s,
                %(creator)s,
                %(updator)s,
                %(messages_ids)s,
                %(priority)s,
                %(is_tags)s,
                %(is_all_vectors)s,
                %(sites)s,
                %(creator_role)s,
                %(deadline)s
            ) returning 
                id, 
                title, 
                description, 
                assets, 
                status, 
                created_timestamp, 
                updated_timestamp,
                type,
                creator,
                updator,
                messages_ids,
                priority,
                comments,
                creator_role,
                tags as is_tags,
                is_all_vectors,
                sites,
                deadline
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.RequestQuery) -> models.Request:
        q = """
            select
                id,
                title,
                description,
                assets,
                status,
                created_timestamp,
                updated_timestamp,
                type,
                creator,
                creator_role,
                updator,
                messages_ids,
                priority,
                comments,
                tags as is_tags,
                is_all_vectors,
                sites,
                deadline
            from requests
            where id = %(id)s;
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def update(self, cmd: models.UpdateRequestCommand) -> models.Request:
        q = """
            update requests
            set title = %(title)s,
                description = %(description)s,
                assets = %(assets)s,
                status = %(status)s,
                updated_timestamp = current_timestamp,
                type = %(type)s,
                updator = %(updator)s,
                messages_ids = %(messages_ids)s,
                tags = %(is_tags)s,
                priority = %(priority)s,
                is_all_vectors = %(is_all_vectors)s,
                sites = %(sites)s,
                deadline = %(deadline)s
            where id = %(id)s
            returning 
                id, 
                title, 
                description, 
                assets, 
                status, 
                created_timestamp, 
                updated_timestamp,
                type,
                creator,
                updator,
                messages_ids,
                priority,
                comments,
                tags as is_tags,
                is_all_vectors,
                sites,
                deadline
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteRequestCommand) -> models.Request:
        q = """
            delete from requests
            where id = %(id)s
            returning 
                id, 
                title, 
                description, 
                assets, 
                status, 
                created_timestamp, 
                updated_timestamp,
                type,
                creator,
                updator,
                messages_ids,
                prioriy,
                comments,
                tags as is_tags,
                is_all_vectors,
                sites,
                deadline
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def update_comment(self, cmd: models.Comment) -> models.Request:
        q = """
                update requests
                set updated_timestamp = now(),
                updator = %(author)s,
                comments = true
                where id = %(request_id)s
                returning 
                id, 
                title, 
                description, 
                assets, 
                status, 
                created_timestamp, 
                updated_timestamp,
                type,
                creator,
                updator,
                messages_ids,
                priority,
                comments,
                tags as is_tags,
                is_all_vectors,
                sites,
                deadline
            """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
