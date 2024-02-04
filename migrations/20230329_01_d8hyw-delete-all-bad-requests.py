"""
Delete all bad requests
"""

from yoyo import step

__depends__ = {'20230323_01_MZ2MX-alter-requests-set-default-messages-ids'}

steps = [
    step(
        """
            delete from requests where messages_ids is null;
        """,
        """
        """
    )
]
