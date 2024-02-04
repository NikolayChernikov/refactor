import json
import logging

import httpx
import pydantic
from starlette import status

from app.internal.pkg.utils.json_encoder import CustomJSONEncoder
from app.pkg.logger import Logger
from app.pkg.models.centrifugo_server import (
    CentrifugoServerHeaders,
    CentrifugoServerPublish,
)
from app.pkg.models.exceptions.centrifugo_server import (
    CentrifugoServer400,
    CentrifugoServer403,
    CentrifugoServer404,
    CentrifugoServer500,
)


class Centrifugo:
    _logger: logging.Logger
    _publish_url: pydantic.HttpUrl
    _headers: CentrifugoServerHeaders

    def __init__(
        self,
        logger: Logger,
        publish_url: pydantic.HttpUrl,
        api_key: pydantic.SecretStr,
    ):
        self._logger = logger.get_logger(__name__)
        self._publish_url = publish_url
        self._headers = CentrifugoServerHeaders(api_key=api_key)

    async def publish(self, data: CentrifugoServerPublish):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=self._publish_url,
                    headers=self._headers.to_dict(),
                    data=json.dumps(data.to_dict(), cls=CustomJSONEncoder),
                )
                if response.status_code == status.HTTP_404_NOT_FOUND:
                    raise CentrifugoServer404
                elif response.status_code == status.HTTP_400_BAD_REQUEST:
                    raise CentrifugoServer400
                elif response.status_code == status.HTTP_403_FORBIDDEN:
                    raise CentrifugoServer403
                elif not response.is_success:
                    raise CentrifugoServer500
        except json.JSONDecodeError:
            self._logger.exception(f"Not valid data for encode to json: {data}")
        except (
            CentrifugoServer404,
            CentrifugoServer400,
            CentrifugoServer403,
            CentrifugoServer500,
        ) as ex:
            self._logger.exception(ex.message)