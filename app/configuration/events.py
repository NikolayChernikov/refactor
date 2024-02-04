import asyncio

from dependency_injector.wiring import inject, Provide

from app.internal.pkg.clients import Clients, Telegram


@inject
async def on_startup(
        telegram: Telegram = Provide[Clients.telegram],
):
    asyncio.create_task(telegram.start())
