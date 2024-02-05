"""Client module."""
from starlette import status

from app.pkg.models.base import BaseAPIException


class BaseClientException(BaseAPIException):
    """Base client exception class."""


class ClientException(BaseClientException):
    """Client exception class."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


class EmptyResultResponse(BaseClientException):
    """Emptry result response class."""

    status_code = status.HTTP_404_NOT_FOUND
