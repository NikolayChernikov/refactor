"""
alter requests add creator, updator
"""

from yoyo import step

__depends__ = {"20230315_01_g5FFK-create-requests"}

steps = [
    step(
        """
            alter table requests add column if not exists creator varchar(30) default '',
                                 add column if not exists updator varchar(30) default '';
        """,
        """
            alter table requests drop column if exists creator,
                                 drop column if exists updator;
        """,
    )
]
