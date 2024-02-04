"""All connectors in declarative container."""

from dependency_injector import containers, providers

from app.pkg.settings import settings
from app.pkg.connectors.postgres import Postgres

__all__ = [
    "Connectors",
    "Postgres",
]


class Connectors(containers.DeclarativeContainer):
    """Declarative container with connectors."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )

    postgres = providers.Factory(
        Postgres,
        username=configuration.POSTGRES_USER,
        password=configuration.POSTGRES_PASSWORD,
        host=configuration.POSTGRES_HOST,
        port=configuration.POSTGRES_PORT,
        database_name=configuration.POSTGRES_DB,
    )
