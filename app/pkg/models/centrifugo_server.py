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
    PUBLISH = "publish"


class BaseCentrifugoServer(BaseModel):
    ...


class CentrifugoServerHeaders(BaseCentrifugoServer):
    api_key: pydantic.SecretStr
    content_type: str = pydantic.Field(default="application/json")

    def to_dict(self, show_secrets: bool = False, values: Dict[Any, Any] = None, **kwargs) -> Dict[Any, Any]:
        return {
            "Authorization": f"apikey {self.api_key.get_secret_value()}",
            "Content-type": self.content_type,
        }


class CentrifugoServerParams(BaseCentrifugoServer):
    channel: str
    data: Any


class CentrifugoServerPublish(BaseCentrifugoServer):
    method: CentrifugoServerMethod
    params: CentrifugoServerParams
