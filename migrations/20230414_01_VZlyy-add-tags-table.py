"""
add tags table
"""

from yoyo import step

__depends__ = {"20230413_02_RtcJP-add-comments-table_upd"}

steps = [
    step(
        """
            create table if not exists tags (
                id serial primary key,
                tag text not null unique
            )
        """,
        """
            drop table if exists tags
        """,
    )
]
