"""
Add default value
"""

from yoyo import step

__depends__ = {'20230413_01_ROaQO-alter-requests-upd'}

steps = [
    
    step(
        """
            alter table requests alter column priority set default 'medium';
        """,
        """
            alter table requests alter column priority drop default;
        """
    ),
    step(
        """
            alter table requests alter column tags set default false;
        """,
        """
            alter table requests alter column tags drop default;
        """
    ),
    step(
        """
            alter table requests alter column is_all_vectors set default true
        """,
        """
            alter table requests alter column is_all_vectors drop default;
        """
    ),
    step(
        """
            alter table requests alter column is_all_vectors set default true
        """,
        """
            alter table requests alter column is_all_vectors drop default;
        """
    ),
    step(
        """
            update requests set priority = 'medium' where priority = 'средний'
        """,
        """
        """
    )

]
