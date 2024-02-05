"""Centrifugo server exceptions."""
from fastapi import status

from app.pkg.models.base import BaseAPIException


class CentrifugoServer404(BaseAPIException):
    """Centrifugo server HTTP error 404."""

    status_code = status.HTTP_404_NOT_FOUND
    message = "Centrifugo url for publish return 404 status code"


class CentrifugoServer400(BaseAPIException):
    """Centrifugo server HTTP error 400."""

    status_code = status.HTTP_400_BAD_REQUEST
    message = "Not valid POST data"


class CentrifugoServer403(BaseAPIException):
    """Centrifugo server HTTP error 403."""

    status_code = status.HTTP_403_FORBIDDEN
    message = "Not valid credentials"


class CentrifugoServer500(BaseAPIException):
    """Centrifugo server HTTP error 500."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Unknown error from centrifugo server"
