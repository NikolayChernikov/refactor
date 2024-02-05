"""
alter requests set default messages_ids
"""

from yoyo import step

__depends__ = {"20230322_01_84MVz-alter-requests-add-telegram-ids"}

steps = [
    step(
        """
            delete from requests where messages_ids is null;
        """,
        """
        """,
    )
]
