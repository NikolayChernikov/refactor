"""
alter requests add priority and comments
"""

from yoyo import step

__depends__ = {"20230329_01_d8hyw-delete-all-bad-requests"}

steps = [
    step(
        """
            alter table requests
            add column if not exists priority varchar(20) default 'средний',
            add column if not exists comments bool default false
                
        """,
        """
            alter table requests
                drop column if exists priority,
                drop column if exists comments
        """,
    ),
    step(
        """
            alter table requests
            add column if not exists tags bool

        """,
        """
            alter table requests
                drop column if exists tags
        """,
    ),
    step(
        """
            alter table requests
            add column if not exists is_all_vectors bool
        """,
        """
            alter table requests
                drop column if exists is_all_vectors
        """,
    ),
    step(
        """
            alter table requests
            add column if not exists sites text[]

        """,
        """
            alter table requests
                drop column if exists sites
        """,
    ),
]
