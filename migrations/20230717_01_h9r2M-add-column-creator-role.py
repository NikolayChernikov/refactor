"""
Add column creator_role
"""

from yoyo import step

__depends__ = {'20230601_01_jC0Qt-add-column-deadline'}

steps = [
    step(
        """
            alter table requests add column if not exists creator_role varchar;
        """,
        """
            alter table requests drop column if exists creator_role;
        """
    ),
]
