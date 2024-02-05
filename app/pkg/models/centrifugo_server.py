"""Centrifugo server module."""
from enum import Enum
from typing import Any, Dict

import pydantic

from app.pkg.models.base import BaseModel

__all__ = [
    "CentrifugoServerMethod",
    "CentrifugoServerHeaders",
    "CentrifugoServerParams",
    "CentrifugoServerPublish",
]


class CentrifugoServerMethod(str, Enum):
    """Centrifugo server method class."""

    PUBLISH = "publish"


class BaseCentrifugoServer(BaseModel):
    """Base centrifugo server class."""


class CentrifugoServerHeaders(BaseCentrifugoServer):
    """Centrifugo server headers class."""

    api_key: pydantic.SecretStr
    content_type: str = pydantic.Field(default="application/json")

    def to_dict(self, show_secrets: bool = False, values: Dict[Any, Any] = None, **kwargs) -> Dict[Any, Any]:
        """Apply dict

        Args:
            show_secrets: bool arg.
            values: dict values.
            **kwargs: ...

        Returns: dict with dump data.
        """
        return {
            "Authorization": f"apikey {self.api_key.get_secret_value()}",
            "Content-type": self.content_type,
        }


class CentrifugoServerParams(BaseCentrifugoServer):
    """Centrifugo server params class."""

    channel: str
    data: Any


class CentrifugoServerPublish(BaseCentrifugoServer):
    """Centrifugo server publish class."""

    method: CentrifugoServerMethod
    params: CentrifugoServerParams
