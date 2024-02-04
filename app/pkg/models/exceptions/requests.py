from fastapi import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "UnknownITRequestsError",
    "BadBase64OfImage",
    "TooManyImagesError",
    "UnknownCommentsError",
]


class UnknownITRequestsError(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Unknown error when create/update request to IT"


class BadBase64OfImage(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Bad base64 of image"


class TooManyImagesError(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Too many images. Max=10."


class UnknownCommentsError(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Unknown error when create comment to request"
