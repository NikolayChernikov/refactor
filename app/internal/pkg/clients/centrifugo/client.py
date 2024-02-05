"""Centrifugo client module."""
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
    """Centrifugo class."""

    _logger: logging.Logger
    _publish_url: pydantic.HttpUrl
    _headers: CentrifugoServerHeaders

    def __init__(
        self,
        logger: Logger,
        publish_url: pydantic.HttpUrl,
        api_key: pydantic.SecretStr,
    ) -> None:
        """Init service."""
        self._logger = logger.get_logger(__name__)
        self._publish_url = publish_url
        self._headers = CentrifugoServerHeaders(api_key=api_key)
        self._errors_compendium = {
            status.HTTP_404_NOT_FOUND: CentrifugoServer404,
            status.HTTP_400_BAD_REQUEST: CentrifugoServer400,
            status.HTTP_403_FORBIDDEN: CentrifugoServer403,
            status.HTTP_500_INTERNAL_SERVER_ERROR: CentrifugoServer500,
        }

    async def publish(self, data: CentrifugoServerPublish) -> None:
        """Do async publish.

        Args:
            data: Centrifugo server publish data.

        Returns: None
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=self._publish_url,
                    headers=self._headers.to_dict(),
                    data=json.dumps(data.to_dict(), cls=CustomJSONEncoder),
                )
                if self._errors_compendium.get(response.status_code, None):
                    raise self._errors_compendium.get(response.status_code)
                if not response.is_success:
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
