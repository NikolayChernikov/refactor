"""Logger container module."""
from dependency_injector import containers, providers

from app.pkg.logger.logger import Logger

__all__ = [
    "LoggerContainer",
    "Logger",
]


class LoggerContainer(containers.DeclarativeContainer):
    """Logger container."""

    logger = providers.Singleton(Logger)
