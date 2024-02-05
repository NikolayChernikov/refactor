"""Services module."""
from dependency_injector import containers, providers

from app.internal.pkg.clients import Clients
from app.internal.pkg.utils import Utils
from app.internal.repository import Repositories
from app.internal.services.requests import Requests
from app.pkg.logger import LoggerContainer

__all__ = [
    "Services",
    "Requests",
]


class Services(containers.DeclarativeContainer):
    """Services class."""

    repositories = providers.Container(Repositories)
    postgres = providers.Container(repositories.postgres)
    logger = providers.Container(LoggerContainer)
    utils = providers.Container(Utils)
    clients = providers.Container(Clients)

    requests = providers.Factory(
        Requests,
        logger=logger.logger,
        requests_repository=postgres.requests,
        filer=utils.filer,
        telegram=clients.telegram,
        comments_repository=postgres.comments,
        tags_repository=postgres.tags,
        vectors_repository=postgres.vectors,
        centrifugo=clients.centrifugo,
    )
