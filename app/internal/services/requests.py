"""Services requests module."""
import asyncio
import logging
import re
from datetime import datetime
from typing import List, Union

import pydantic
from pydantic import PositiveInt

from app.internal.pkg import clients, utils
from app.internal.repository import postgres
from app.pkg import models
from app.pkg.logger import Logger
from app.pkg.models import Message, UpdateRequestCommand
from app.pkg.models.centrifugo_server import (
    CentrifugoServerMethod,
    CentrifugoServerParams,
    CentrifugoServerPublish,
)
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg.models.exceptions.requests import (
    BadBase64OfImage,
    TooManyImagesError,
    UnknownCommentsError,
    UnknownITRequestsError,
)
from app.pkg.settings import settings

__all__ = [
    "Requests",
]


class Requests:  # pylint: disable=too-many-instance-attributes
    """Requests class."""

    _logger: logging.Logger
    _filer: utils.Filer
    _requests_repository: postgres.Requests
    _telegram: clients.Telegram
    _comments_repository: postgres.Comments
    _tags_repository: postgres.Tags
    _vectors_repository: postgres.Vectors
    _centrifugo: clients.Centrifugo

    def __init__(  # pylint: disable=too-many-arguments
        self,
        logger: Logger,
        filer: utils.Filer,
        requests_repository: postgres.Requests,
        comments_repository: postgres.Comments,
        tags_repository: postgres.Tags,
        vectors_repository: postgres.Vectors,
        telegram: clients.Telegram,
        centrifugo: clients.Centrifugo,
    ):
        self._logger = logger.get_logger(__name__)
        self._filer = filer
        self._requests_repository = requests_repository
        self._comments_repository = comments_repository
        self._tags_repository = tags_repository
        self._vectors_repository = vectors_repository
        self._telegram = telegram
        self._centrifugo = centrifugo

    async def __read_by_id(self, id: PositiveInt) -> models.Request:  # pylint: disable=redefined-builtin
        return await self._requests_repository.read(
            query=models.RequestQuery(id=id),
        )

    async def __publish_to_centrifugo(
        self,
        data: Message,
        channel: str,
    ):
        await self._centrifugo.publish(
            CentrifugoServerPublish(
                method=CentrifugoServerMethod.PUBLISH,
                params=CentrifugoServerParams(
                    channel=channel,
                    data=data.to_dict(),
                ),
            )
        )

    @staticmethod
    def __collect_caption(
        request: Union[models.CreateRequestCommand, models.UpdateRequestCommand],
        new_comment: bool = False,
    ) -> str:
        created = datetime.fromtimestamp(request.created_timestamp)
        updated = datetime.fromtimestamp(request.updated_timestamp)
        message = (
            f"#{request.type.upper()}\n"
            f'Created "{request.creator}" "{created}"\n'
            f'Updated "{request.updator}" "{updated}"\n'
            f'Status "{request.status.capitalize()}"\n\n'
            f"{request.title}\n\n"
            f"{request.description}\n"
        )
        if new_comment:
            message += "Появился новый комментарий!"
        return message

    @staticmethod
    def __collect_caption_update(
        request: Union[models.CreateRequestCommand, models.UpdateRequestCommand],
        new_comment: bool = False,
    ) -> str:
        created = datetime.fromtimestamp(request.created_timestamp)
        updated = datetime.fromtimestamp(request.updated_timestamp)
        message = (
            f"#{request.type.upper()}\n"
            f'Created "{request.creator}" "{created}"\n'
            f'Updated "{request.updator}" "{updated}"\n'
            f'Status "{request.status.capitalize()}"\n\n'
            f"{request.title}\n\n"
            f"Запрос обновился\n"
        )
        if new_comment:
            message += "Появился новый комментарий!"
        return message

    async def create_tags(self, cmd: models.CreateRequestCommand, result: models.Request) -> None:
        """Create tags.

        Args:
            cmd: create request command.
            result: request.

        Returns: None.
        """
        try:
            if cmd.tags:
                await self._tags_repository.create(result.id, cmd.tags)
                result.tags = cmd.tags
        except Exception:  # pylint: disable=broad-exception-raised
            self._logger.exception("Error to add tags in db")

    async def create_vectors(self, cmd: models.CreateRequestCommand, result: models.Request) -> None:
        """Create vectors.

        Args:
            cmd: create request command.
            result: request.

        Returns: None.
        """
        try:

            if not cmd.is_all_vectors:
                vectors = await self._vectors_repository.create(result.id, cmd.vectors)
                result.vectors = vectors
        except Exception:  # pylint: disable=broad-exception-raised
            self._logger.exception("Error to add vectors in db")

    async def create_request_cent_pub(self, cmd: models.CreateRequestCommand, result: models.Request) -> None:
        """Create request cent pub.

        Args:
            cmd: create request command.
            result: request.

        Returns: None.
        """
        try:
            await self.__publish_to_centrifugo(
                data=Message(
                    message=f"Новый запрос к IT {cmd.title} добавлен пользователем {cmd.creator} \n"
                    f"ID запроса - {result.id}"
                ),
                channel=settings.CENT_IT_REQUEST_CHANNEL,
            )
        except Exception:  # pylint: disable=broad-exception-raised
            self._logger.exception("Error to add to cent")

    async def create(  # noqa: C901
        self,
        cmd: models.CreateRequestCommand,
    ) -> models.Request:
        """Create.

        Args:
            cmd: create request command.

        Returns: request.
        """
        assets = []
        try:
            if len(cmd.assets) > 10:
                raise ValueError
            for num, base64_ in enumerate(cmd.assets, start=1):
                item = await self._filer.save_image(base64_=base64_, name=num)
                assets.append(str(item))
            cmd.assets = assets
            cmd.created_timestamp = int(datetime.now().timestamp())
            cmd.updated_timestamp = cmd.created_timestamp
            cmd.status = models.Statuses.IN_QUEUE
            if not cmd.deadline:
                cmd.deadline = ""
            caption = self.__collect_caption(cmd)

            try:
                cmd.messages_ids = await self._telegram.send_notify(
                    assets=cmd.assets,
                    caption=caption,
                )
            except Exception as exc:
                self._logger.exception(exc)

            result = await self._requests_repository.create(cmd=cmd)

            tasks = [
                self.create_tags(cmd, result),
                self.create_vectors(cmd, result),
                self.create_request_cent_pub(cmd, result),
            ]
            await asyncio.gather(*tasks)

            return result
        except BadBase64OfImage:
            self._filer.delete(files=assets)
            self._logger.exception("Bad base64 of image")
            raise BadBase64OfImage
        except ValueError as exc:
            self._logger.exception(exc)
            raise TooManyImagesError
        except Exception:  # pylint: disable=broad-exception-raised
            self._filer.delete(files=assets)
            self._logger.exception("Unknown error when create request to IT")
            raise UnknownITRequestsError

    async def read(self, id: PositiveInt) -> models.Request:  # pylint: disable=redefined-builtin # noqa: C901
        """Read by id.

        Args:
            id: request id.

        Returns: request.
        """
        try:  # pylint: disable=no-else-raise
            request = await self.__read_by_id(id=id)
        except Exception:  # pylint: disable=broad-exception-raised
            self._logger.exception("Ошибка выгрузки запроса из БД")
            raise UnknownITRequestsError
        else:
            if not request.is_all_vectors:
                try:
                    vectors = await self._vectors_repository.read(request.id)
                    request.vectors = vectors
                except Exception:  # pylint: disable=broad-exception-raised
                    self._logger.exception("Ошибка выгрузки векторов запроса")
            if request.comments:
                try:
                    comments = await self._comments_repository.read(request.id)
                    request.comments_objects = comments
                except Exception:  # pylint: disable=broad-exception-raised
                    self._logger.exception("Ошибка выгрузки комментариев")
            return request

    async def delete(self, id: PositiveInt) -> models.Request:  # pylint: disable=redefined-builtin
        """Delete by id.

        Args:
            id: request id.

        Returns: request.
        """
        deleted = await self._requests_repository.delete(cmd=models.DeleteRequestCommand(id=id))
        self._filer.delete(files=deleted.assets)
        try:
            await self._telegram.delete_messages(deleted.messages_ids)
        except Exception as exc:
            self._logger.exception(exc)
        return deleted

    async def read_all_by_time(self, time_from: int, time_to: int) -> List[models.RequestFull]:
        """Read all by time.

        Args:
            time_from: time from.
            time_to: time to.

        Returns: list with request full.
        """
        try:
            time_from_new = datetime.fromtimestamp(time_from)
            time_to_new = datetime.fromtimestamp(time_to)
            return await self._requests_repository.read_full_data(time_from_new, time_to_new)
        except EmptyResult:
            return []

    async def read_all(self) -> List[models.Request]:  # noqa: C901
        """Read all.

        Returns: list with request.
        """
        try:  # pylint: disable=no-else-return
            requests = await self._requests_repository.read_all()
            vectors = await self._vectors_repository.read_all()
        except EmptyResult:
            return []
        else:
            for el in requests:
                el.vectors = []
                if not el.is_all_vectors:
                    for vector in vectors:
                        if vector.request_id == el.id:
                            el.vectors.append(vector)
                if el.is_tags:
                    try:
                        tags = await self._tags_repository.read(el.id)
                        el.tags = tags
                    except Exception:  # pylint: disable=broad-exception-raised
                        self._logger.exception("Ошибка выгрузки тэгов")
                if el.comments:
                    try:
                        comments = await self._comments_repository.read(el.id)
                    except Exception:  # pylint: disable=broad-exception-raised
                        self._logger.exception("Ошибка выгрузки комментариев")
                    else:
                        el.comments_objects = comments
            return requests

    async def get_comments_by_id(self, cmd, result) -> None:
        """Get comments by id.

        Args:
            cmd: cmd.
            result: result.

        Returns: None.
        """
        try:
            comments = await self._comments_repository.read(cmd.id)
        except Exception:  # pylint: disable=broad-exception-raised
            self._logger.exception("Ошибка выгрузки комментариев")
        else:
            result.comments_objects = comments

    async def update_tags(self, cmd, result) -> None:
        """Update tags.

        Args:
            cmd: cmd.
            result: result.

        Returns: None.
        """
        if cmd.is_tags:
            await self._tags_repository.delete(result.id)
            await self._tags_repository.create(result.id, cmd.tags)
            result.tags = cmd.tags
        if not cmd.is_tags:
            await self._tags_repository.delete(result.id)
            result.tags = []

    async def update_vectors(self, cmd, result) -> None:
        """Update vectors.

        Args:
            cmd: cmd.
            result: result.

        Returns: None.
        """
        if cmd.is_all_vectors:
            await self._vectors_repository.delete(result.id)
        if not cmd.is_all_vectors:
            await self._vectors_repository.delete(result.id)
            vectors = await self._vectors_repository.create(result.id, cmd.vectors)
            result.vectors = vectors if vectors else []
        else:
            await self._vectors_repository.delete(result.id)

        if not result.vectors:
            result.vectors = []

    async def update(self, cmd: models.UpdateRequestCommand) -> models.Request:  # noqa: C901
        """Update.

        Args:
            cmd: update request command.

        Returns: request.
        """
        old_assets, new_assets = [], []
        try:
            if len(cmd.assets) > 10:
                raise ValueError
            for num, item in enumerate(cmd.assets, start=1):
                if not re.search(r"\.jpeg|\.png|\.jpg|\.webp|\.svg", item.lower()):
                    item = await self._filer.save_image(base64_=item, name=num)
                    new_assets.append(str(item))
                else:
                    old_assets.append(item)
            cmd.assets = old_assets + new_assets
            previous = await self.__read_by_id(id=cmd.id)
            self._filer.delete(files=[item for item in previous.assets if item not in cmd.assets])
            try:
                await self._telegram.delete_messages(messages_ids=previous.messages_ids)
            except Exception as exc:
                self._logger.exception(exc)
            cmd.created_timestamp = previous.created_timestamp
            cmd.updated_timestamp = int(datetime.now().timestamp())
            cmd.creator = previous.creator
            caption = self.__collect_caption_update(request=cmd)
            try:
                cmd.messages_ids = await self._telegram.send_notify(
                    assets=[],
                    caption=caption,
                    disable_notification=True,
                )
            except Exception as exc:
                self._logger.exception(exc)
            if not cmd.vectors:
                cmd.is_all_vectors = True
            if not cmd.tags:
                cmd.is_tags = False
            result = await self._requests_repository.update(cmd=cmd)

            tasks = [
                self.update_tags(cmd, result),
                self.update_vectors(cmd, result),
                self.get_comments_by_id(cmd, result),
            ]
            await asyncio.gather(*tasks)

            asyncio.create_task(
                self.__publish_to_centrifugo(
                    data=Message(
                        message=f"Обновлен запрос к IT {cmd.title} пользователем {cmd.updator} \n"
                        f"ID запроса - {cmd.id}"
                    ),
                    channel=settings.CENT_IT_REQUEST_CHANNEL,
                )
            )
            return result
        except EmptyResult:
            self._filer.delete(files=new_assets)
            raise EmptyResult
        except ValueError:
            raise TooManyImagesError
        except Exception:  # pylint: disable=broad-exception-raised
            self._filer.delete(files=new_assets)
            self._logger.exception("Unknown error when update request to IT")
            raise UnknownITRequestsError

    async def add_comment(self, request_id: int, cmd: models.Comment) -> models.Comment:  # noqa: C901
        """Add comment.

        Args:
            request_id: request id.
            cmd: comment.

        Returns: comment.
        """
        try:  # pylint: disable=no-else-raise
            cmd.request_id = request_id
            comment = await self._comments_repository.create(cmd)
        except Exception:  # pylint: disable=broad-exception-raised
            self._logger.exception("Ошибка создания коммента в БД")
            raise UnknownCommentsError
        else:
            try:  # pylint: disable=no-else-raise
                request = await self._requests_repository.update_comment(cmd)
                data = pydantic.parse_obj_as(UpdateRequestCommand, request)
                caption = self.__collect_caption_update(data, new_comment=True)
                try:
                    await self._telegram.send_notify(
                        assets=[],
                        caption=caption,
                    )
                except Exception as exc:
                    self._logger.exception(exc)
            except Exception:  # pylint: disable=broad-exception-raised
                self._logger.exception("Ошибка замены времени обновления")
                raise UnknownCommentsError
            else:
                await self.__publish_to_centrifugo(
                    data=Message(
                        message=f"Добавлен комментарий на запрос IT {request.title} пользователем {cmd.author} \n"
                        f"ID запроса - {cmd.request_id}"
                    ),
                    channel=settings.CENT_IT_REQUEST_CHANNEL,
                )
                return comment

    async def get_all_tags(self) -> List[models.Tag]:
        """Get all tags.

        Returns: list with tag.
        """
        try:
            return await self._tags_repository.read_all()
        except Exception:  # pylint: disable=broad-exception-raised
            self._logger.exception("Ошибка выгрузки тэгов из БД")
            raise UnknownITRequestsError
