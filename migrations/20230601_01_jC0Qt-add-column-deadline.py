"""
Add column deadline
"""

from yoyo import step

__depends__ = {'20230414_04_HtG8z-add-tag-request-table', '20230419_02_KWdne-add-default-values_updated'}

steps = [
    step(
        """
            alter table requests add column if not exists deadline varchar default '';
        """,
        """
            alter table requests drop column if exists deadline;
        """
    ),
]
