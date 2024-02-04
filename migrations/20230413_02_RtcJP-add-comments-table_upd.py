"""
add comments table
"""

from yoyo import step

__depends__ = {'20230413_01_ROaQO-alter-requests-upd'}

steps = [
    step(
        """
            create table if not exists comments (
                id serial primary key,
                request_id int references requests on delete cascade,
                comment text not null,
                author text not null,
                time timestamp not null
            )
        """,
        """
            drop table if exists comments
        """
    ),
    step(
        """
            alter table comments add column if not exists author_role text
        """,
        """
            alter table comments drop column if exists author_role text
        """
    ),

]
