from app.pkg.models.base import BaseModel

__all__ = ["ElementNotify"]


class BaseElement(BaseModel):
    ...


class ElementNotify(BaseModel):
    body: str
    room_id: str
