"""Element module."""
from app.pkg.models.base import BaseModel

__all__ = ["ElementNotify"]


class BaseElement(BaseModel):
    """Base element class."""


class ElementNotify(BaseModel):
    """Element notify class."""

    body: str
    room_id: str
