"""Repositories module."""
from dependency_injector import containers, providers

from app.internal.repository.postgres import Postgres

__all__ = [
    "Repositories",
    "Postgres",
]


class Repositories(containers.DeclarativeContainer):
    """Repositories class."""

    postgres = providers.Container(Postgres)
