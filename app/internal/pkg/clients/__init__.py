from dependency_injector import containers, providers

from app.internal.pkg.clients.centrifugo.client import Centrifugo
from app.internal.pkg.clients.element.client import ElementClient
from app.pkg.logger import LoggerContainer
from app.pkg.settings import settings
from app.internal.pkg.clients.telegram.client import Telegram

__all__ = [
    "Clients",
    "Telegram",
    "Centrifugo"
]


class Clients(containers.DeclarativeContainer):
    configuration = providers.Configuration(
        name="settings", pydantic_settings=[settings]
    )
    logger = providers.Container(LoggerContainer)

    element_client = providers.Factory(
        ElementClient,
        logger=logger.logger,
        client_name=ElementClient.__name__,
        url=configuration.ELEMENT_URL,
        x_token=configuration.ELEMENT_X_ACCESS_TOKEN,
    )

    telegram = providers.Singleton(
        Telegram,
        logger=logger.logger,
        element_client=element_client,
        api_token=configuration.TELEGRAM_API_TOKEN,
        chat_id=configuration.TELEGRAM_CHAT_ID,
        element_room_id=configuration.ELEMENT_ROOM_ID_REQUESTS,
        element_room_id_no_notification=configuration.ELEMENT_ROOM_ID_REQUESTS_NO_NOTIFICATION,
    )

    centrifugo = providers.Factory(
        Centrifugo,
        logger=logger.logger,
        publish_url=f"http://{settings.CENT_HOST}:{settings.CENT_PORT}/api",
        api_key=settings.CENT_API_KEY,
    )
