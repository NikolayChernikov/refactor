from starlette import status

from app.pkg.models.base import BaseAPIException


class BaseClientException(BaseAPIException):
    ...


class ClientException(BaseClientException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


class EmptyResultResponse(BaseClientException):
    status_code = status.HTTP_404_NOT_FOUND
