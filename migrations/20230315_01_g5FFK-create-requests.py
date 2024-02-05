"""
Create requests
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            create table if not exists requests (
                id serial primary key unique not null,
                title varchar(100) not null,
                description text not null,
                status varchar(20) default 'в очереди',
                assets text[] default array[]::text[],
                created_timestamp timestamp default current_timestamp,
                updated_timestamp timestamp not null
            );
        """,
        """
            drop table if exists requests;
        """,
    )
]
