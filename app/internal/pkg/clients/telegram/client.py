import asyncio
from typing import List

from pydantic import SecretStr
from aiogram import Bot, Dispatcher, types

from app.internal.pkg.clients import ElementClient
from app.pkg import models
from app.pkg.logger import Logger


class Telegram:
    _bot: Bot
    _dp: Dispatcher
    _chat_id: int

    def __init__(
            self,
            logger: Logger,
            element_client: ElementClient,
            api_token: SecretStr,
            chat_id: int,
            element_room_id: str,
            element_room_id_no_notification: str,
    ):
        self._logger = logger.get_logger(__name__)
        self.element_client = element_client
        self.element_room_id = element_room_id
        self.element_room_id_no_notification = element_room_id_no_notification
        self._bot = Bot(token=api_token.get_secret_value())
        self._dp = Dispatcher()
        self._chat_id = chat_id

    async def send_element(self, caption: str, disable_notification: bool):
        try:
            if disable_notification or 'обновился' in caption.lower():
                room_id = self.element_room_id_no_notification
            else:
                room_id = self.element_room_id
            model = models.ElementNotify(body=caption, room_id=room_id)
            status_code = await self.element_client.send_message(model)
            if str(status_code) == '200':
                self._logger.info("Success - send alert to matrix")
        except Exception:
            self._logger.exception("Error to send to element data")

    async def send_notify(
            self,
            assets: List[str],
            caption: str,
            disable_notification: bool = False
    ) -> List[int]:
        try_, traceback = 0, None
        while try_ < 5:
            try:
                media = []
                for ass in assets:
                    media.append(types.InputMediaPhoto(
                        media=types.FSInputFile(ass),
                    ))
                if media:
                    media[0].caption = caption
                    messages = await self._bot.send_media_group(
                        chat_id=self._chat_id,
                        media=media,
                        disable_notification=disable_notification,
                    )
                    await self.send_element(caption, disable_notification)
                    return [m.message_id for m in messages]
                else:
                    await self.send_element(caption, disable_notification)
                    return [(await self._bot.send_message(
                        chat_id=self._chat_id,
                        text=caption,
                        disable_notification=disable_notification,
                    )).message_id]
            except Exception as ex:
                traceback = ex
                try_ += 1
        self._logger.error(f"Can't send notify to chat with id={self._chat_id}\n{traceback}")

    async def delete_messages(
            self,
            messages_ids: List[int],
    ):
        try:
            tasks = [self._bot.delete_message(
                chat_id=self._chat_id,
                message_id=id_,
            ) for id_ in messages_ids]
            await asyncio.gather(*tasks)
        except Exception:
            pass

    async def start(self):
        await self._dp.start_polling(self._bot)

