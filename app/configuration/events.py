"""Events startup module."""
import asyncio

from dependency_injector.wiring import Provide, inject

from app.internal.pkg.clients import Clients, Telegram


@inject
async def on_startup(
    telegram: Telegram = Provide[Clients.telegram],
) -> None:
    """Create task on startup

    Returns: None
    """
    asyncio.create_task(telegram.start())
