from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, TypeVar

import pydantic

__all__ = ["BaseModel", "Model"]

Model = TypeVar("Model", bound="BaseModel")


class BaseModel(pydantic.BaseModel):
    def to_dict(self, show_secrets: bool = False, values: Dict[Any, Any] = None, **kwargs) -> Dict[Any, Any]:
        """Make transfer model to Dict object."""
        values = self.dict(**kwargs).items() if not values else values.items()
        r = {}
        for k, v in values:
            if isinstance(v, pydantic.SecretBytes):
                v = v.get_secret_value().decode() if show_secrets else str(v)
            elif isinstance(v, pydantic.SecretStr):
                v = v.get_secret_value() if show_secrets else str(v)
            elif isinstance(v, Dict):
                v = self.to_dict(show_secrets=show_secrets, values=v)
            r[k] = v
        return r

    def to_list(self, show_secrets: bool = False, **kwargs) -> List[Any]:
        r = []
        for v in self.dict(**kwargs).values():
            if isinstance(v, pydantic.SecretBytes):
                v = v.get_secret_value().decode() if show_secrets else str(v)
            elif isinstance(v, pydantic.SecretStr):
                v = v.get_secret_value() if show_secrets else str(v)
            r.append(v)
        return r

    def to_string(self, show_secrets: bool = False, **kwargs) -> str:
        values = []
        for v in self.to_list(show_secrets=show_secrets, **kwargs):
            if isinstance(v, datetime) or isinstance(v, str):
                values.append(f"'{v}'")
            else:
                values.append(str(v))
        return f"({', '.join(values)})"

    def delete_attribute(self, attr: str) -> BaseModel:
        """Delete `attr` field from model.

        Args:
            attr: str value, implements name of field.

        Returns: self object.
        """
        delattr(self, attr)
        return self

    class Config:
        use_enum_values = True
        json_encoders = {
            pydantic.SecretStr: lambda v: v.get_secret_value() if v else None,
            pydantic.SecretBytes: lambda v: v.get_secret_value() if v else None,
            bytes: lambda v: v.decode() if v else None,
        }
