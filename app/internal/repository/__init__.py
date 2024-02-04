from dependency_injector import containers, providers

from app.internal.repository.postgres import Postgres

__all__ = [
    "Repositories",
    "Postgres",
]


class Repositories(containers.DeclarativeContainer):
    postgres = providers.Container(Postgres)
