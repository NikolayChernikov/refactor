"""
add request vectors table
"""

from yoyo import step

__depends__ = {"20230414_02_gSAwf-tags-initial-data"}

steps = [
    step(
        """
            create table if not exists vectors (
                id serial primary key,
                request_id int references requests on delete cascade,
                vector text not null,
                unique (request_id, vector)
            )
        """,
        """
            drop table if exists vectors
        """,
    )
]
