"""Repository module."""
from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "UniqueViolation",
    "EmptyResult",
    "DriverError",
    "InvalidDataRequest",
    "EmptyResultResponse",
    "VectorAlreadyExist",
    "CityAlreadyExist",
    "XmlUrlAlreadyExist",
]


class UniqueViolation(BaseAPIException):
    """Unique violation module."""

    message = "Not unique"
    status_code = status.HTTP_409_CONFLICT


class EmptyResult(BaseAPIException):
    """Empty result class."""

    status_code = status.HTTP_404_NOT_FOUND
    message = "Empty result"


class InvalidDataRequest(BaseAPIException):
    """Invalid data request class."""

    status_code = status.HTTP_404_NOT_FOUND
    message = "Invalid data."


class EmptyResultResponse(BaseAPIException):
    """Empty result response class."""

    message = "Empty result"
    status_code = status.HTTP_404_NOT_FOUND


class DriverError(BaseAPIException):
    """Driver error class."""

    def __init__(self, message: str = None) -> None:  # pylint: disable=super-init-not-called
        if message:
            self.message = message

    message = "Internal error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class VectorAlreadyExist(BaseAPIException):
    """Vector already exist class."""

    status_code = status.HTTP_409_CONFLICT
    message = "Vector already exists."


class CityAlreadyExist(BaseAPIException):
    """City already exist class."""

    status_code = status.HTTP_409_CONFLICT
    message = "City already exists."


class XmlUrlAlreadyExist(BaseAPIException):
    """Xml url already exist class."""

    status_code = status.HTTP_409_CONFLICT
    message = "XML url already exist."
