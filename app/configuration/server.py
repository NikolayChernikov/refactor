"""Server configuration."""
from typing import TypeVar

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.internal.pkg.middlewares.handle_http_exceptions import handle_api_exceptions
from app.internal.routes import __routes__
from app.pkg.models.base import BaseAPIException

from .events import on_startup

__all__ = ["Server"]

FastAPIInstance = TypeVar("FastAPIInstance", bound="FastAPI")


class Server:
    """Register all requirements for correct work of server instance."""

    def __init__(self, app: FastAPI):
        self.__app = app
        self._register_containers(app)
        self._register_routes(app)
        self._register_events(app)
        self._register_middlewares(app)
        self._register_http_exceptions(app)

    def get_app(self) -> FastAPIInstance:
        """Get current application instance.

        Returns: ``FastAPI`` application instance.
        """
        return self.__app

    @staticmethod
    def _register_events(app: FastAPIInstance):
        """Register on startup events.

        Args:
            app: ``FastAPI`` application instance.

        Returns: None
        """

        app.on_event("startup")(on_startup)

    @staticmethod
    def _register_routes(app: FastAPIInstance) -> None:
        """Include routers in ``FastAPI`` instance from ``__routes__``.

        Args:
            app: ``FastAPI`` application instance.

        Returns: None
        """

        __routes__.register_routes(app)

    @staticmethod
    def _register_containers(app: FastAPIInstance):
        """Register services __service__ using dependency injection pattern.

        Args:
            app: ``FastAPI`` application instance.

        Returns: None
        """
        ...

    @staticmethod
    def __register_cors_origins(app: FastAPIInstance):
        """Register cors origins."""

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _register_middlewares(self, app):
        """Apply routes middlewares."""

        self.__register_cors_origins(app)

    @staticmethod
    def _register_http_exceptions(app: FastAPIInstance):
        """Register http exceptions.

        FastAPIInstance handle BaseApiExceptions raises inside
        functions.
        """

        app.add_exception_handler(BaseAPIException, handle_api_exceptions)
