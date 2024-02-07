"""Base client module."""
from typing import Literal

import httpx
import pydantic

from app.pkg.logger import Logger
from app.pkg.models.exceptions.client import ClientException

__all__ = ["BaseClient"]


class BaseClient:
    """Base client class."""

    client_name: str
    AUTH_X_TOKEN: pydantic.SecretStr
    url: pydantic.AnyUrl

    def __init__(
        self,
        x_token: pydantic.SecretStr,
        url: pydantic.AnyUrl,
        logger: Logger,
        client_name: str,
    ):
        self.AUTH_X_TOKEN = x_token  # pylint: disable=invalid-name
        self.url = url
        self.client_name = client_name
        self._logger = logger.get_logger(__name__)

    async def do_request(self, method: Literal["GET", "POST", "DELETE"], path: str = None, **kwargs) -> httpx.Response:
        """Send async request.

        Args:
            method: HTTP method.
            path: Endpoint path.
            **kwargs: Query params.

        Returns: HTTP response.
        """
        headers = {"X-ACCESS-TOKEN": self.AUTH_X_TOKEN.get_secret_value()}
        async with httpx.AsyncClient(headers=headers, timeout=10) as client:
            try:
                response = await client.request(method=method, url=f"{self.url}/{path}", **kwargs)
            except Exception:  # pylint:  disable=broad-exception-raised
                self._logger.exception("Error while sending request")
                raise ClientException(
                    message=f"{self.client_name} is not available now",
                )
            if response.is_success:
                return response

            self._logger.exception("Response - unsuccess")
            raise ClientException(
                message=f"{self.client_name} is not available now",
            )
