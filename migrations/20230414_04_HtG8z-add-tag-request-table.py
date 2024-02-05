"""
add tag request table
"""

from yoyo import step

__depends__ = {"20230414_03_Fd6dV-add-request-vectors-table"}

steps = [
    step(
        """
            create table if not exists request_tag (
                id serial primary key,
                tag_id int references tags on delete cascade,
                request_id int references requests on delete cascade,
                unique (tag_id, request_id)
            )
        """,
        """
            drop table if exists request_tag
        """,
    )
]
