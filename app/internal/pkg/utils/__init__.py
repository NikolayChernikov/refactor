"""Utils module."""
from dependency_injector import containers, providers

from app.internal.pkg.utils.filer import Filer
from app.pkg.logger import LoggerContainer
from app.pkg.settings import settings

__all__ = [
    "Utils",
    "Filer",
]


class Utils(containers.DeclarativeContainer):
    """Utils class."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )
    logger = providers.Container(LoggerContainer)

    filer = providers.Factory(
        Filer,
        logger=logger.logger,
        static_dir=configuration.STATIC_DIR,
        static_dir_internal=configuration.STATIC_DIR_INTERNAL,
        static_url=configuration.STATIC_URL,
    )
