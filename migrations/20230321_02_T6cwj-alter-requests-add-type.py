"""
Alter requests add type
"""

from yoyo import step

__depends__ = {"20230321_01_ZywyW-alter-requests-add-creator-updator"}

steps = [
    step(
        """
            alter table requests add column if not exists type varchar(20) default '';
        """,
        """
            alter table requests drop column if exists type;
        """,
    )
]
