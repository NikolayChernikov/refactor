from dependency_injector import containers, providers

from app.internal.repository.postgres.comments import Comments
from app.internal.repository.postgres.connection import get_connection
from app.internal.repository.postgres.requests import Requests
from app.internal.repository.postgres.tags import Tags
from app.internal.repository.postgres.vectors import Vectors


__all__ = [
    "get_connection",
    "Postgres",
    "Requests",
    "Comments",
    "Tags",
    "Vectors",
]


class Postgres(containers.DeclarativeContainer):
    requests = providers.Factory(Requests)
    comments = providers.Factory(Comments)
    tags = providers.Factory(Tags)
    vectors = providers.Factory(Vectors)
