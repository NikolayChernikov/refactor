"""X auth token module."""
from fastapi import status

from app.pkg.models.base import BaseAPIException


class InvalidCredentials(BaseAPIException):
    """Invalud credentials class."""

    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Invalid credentials."
