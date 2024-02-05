"""Auth static files module."""
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from pydantic import SecretStr

from app.pkg.models.exceptions.repository import EmptyResult

__all__ = [
    "AuthStaticFiles",
]


class AuthStaticFiles(StaticFiles):
    """Auth static files class."""

    _x_static_token: SecretStr

    def __init__(self, x_static_token: SecretStr, *args, **kwargs):
        self._x_static_token = x_static_token
        super().__init__(*args, **kwargs)

    async def __call__(self, scope, receive, send) -> None:
        request = Request(scope, receive)
        is_denied = True
        for k, v in request.headers.items():
            if k.upper() == "X-STATIC-TOKEN" and v == self._x_static_token.get_secret_value():
                is_denied = False
                break
        if is_denied:
            raise EmptyResult
        await super().__call__(scope, receive, send)
