"""Model for contain ``APIRouter`` instance."""

from dataclasses import dataclass
from typing import Tuple

from fastapi import APIRouter, FastAPI

__all__ = ["Routes"]


@dataclass(frozen=True)
class Routes:
    """Frozen model for storage all ``APIRouter``."""

    routers: Tuple[APIRouter, ...]

    def register_routes(self, app: FastAPI):
        """Include ``APIRouter`` to the ``FastAPI`` application instance."""

        for router in self.routers:
            app.include_router(router)
