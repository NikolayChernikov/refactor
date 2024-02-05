"""
Alter requests add telegram ids
"""

from yoyo import step

__depends__ = {"20230321_02_T6cwj-alter-requests-add-type"}

steps = [
    step(
        """
            alter table requests add column if not exists messages_ids int[] default array[]::int[];
        """,
        """
            alter table requests drop column if exists messages_ids;
        """,
    )
]
