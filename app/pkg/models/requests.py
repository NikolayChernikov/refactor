"""Requests model class."""
from enum import Enum
from typing import List, Optional

from pydantic import PositiveInt, root_validator, validator

from app.pkg.models.base import BaseModel
from app.pkg.settings import settings

__all__ = [
    "Statuses",
    "Types",
    "Request",
    "ReadRequest",
    "RequestQuery",
    "CreateRequestCommand",
    "UpdateRequestCommand",
    "DeleteRequestCommand",
    "Priority",
    "Comment",
    "Tag",
    "RequestTagBlock",
    "Message",
    "RequestFull",
]


class Message(BaseModel):
    """Message model."""

    message: str


class Tag(BaseModel):
    """Tag model."""

    id: PositiveInt
    tag: str


class Statuses(str, Enum):
    """Statuses model."""

    CANCELED = "отклонено"
    IN_QUEUE = "в очереди"
    IN_WORK = "в работе"
    READY = "готово"


class Types(str, Enum):
    """Types model."""

    REQUEST = "запрос"
    FIRE = "пожар"
    TASK = "задача"


class Priority(str, Enum):
    """Priority model."""

    LOW = "low"
    MEDIUM = "medium"  # pylint: disable=invalid-name
    HIGH = "high"


class Comment(BaseModel):
    """Comment model."""

    id: Optional[PositiveInt]
    request_id: Optional[PositiveInt]
    comment: str
    author: str
    author_role: Optional[str]
    time: Optional[int]


class Vector(BaseModel):
    """Vector model."""

    request_id: Optional[int]
    vector: str


class BaseRequest(BaseModel):
    """Base request model."""

    title: str
    description: str
    updator: str
    creator: str
    creator_role: Optional[str]
    assets: List[str]
    status: Optional[Statuses]
    type: Optional[Types]
    created_timestamp: Optional[int]
    updated_timestamp: Optional[int]
    comments: bool = False
    comments_objects: Optional[List[Comment]]
    priority: Optional[Priority] = Priority.MEDIUM
    is_tags: Optional[bool]
    sites: Optional[List[str]]
    tags: Optional[List[Tag]]
    is_all_vectors: Optional[bool]
    vectors: Optional[List[Vector]]
    deadline: Optional[str]


class Request(BaseRequest):
    """Request model."""

    id: PositiveInt
    creator: str
    creator_role: Optional[str]
    messages_ids: List[int] = None


class ReadRequest(BaseRequest):
    """Read request model."""

    id: PositiveInt
    creator: str

    @validator("assets")
    def set_static_url_to_assets(cls, ass: List[str]) -> List[str]:  # pylint: disable=no-self-argument
        """Set static url to assets."""
        return list(
            map(
                lambda a: a.replace(str(settings.STATIC_DIR_INTERNAL), str(settings.STATIC_URL)),
                ass,
            )
        )


class RequestQuery(BaseModel):
    """Request query model."""

    id: PositiveInt


class CreateRequestCommand(BaseRequest):
    """Create request command model."""

    messages_ids: Optional[List[int]] = None


class UpdateRequestCommand(BaseRequest):
    """Update request command model."""

    id: PositiveInt
    creator: Optional[str]
    creator_role: Optional[str]
    messages_ids: Optional[List[int]] = None

    @validator("assets")
    def set_internal_dir_to_assets(cls, ass: List[str]) -> List[str]:  # pylint: disable=no-self-argument
        """Set internal dit to assets."""
        return list(
            map(
                lambda a: a.replace(str(settings.STATIC_URL), str(settings.STATIC_DIR_INTERNAL)),
                ass,
            )
        )


class DeleteRequestCommand(BaseModel):
    """Delete request command model."""

    id: PositiveInt


class RequestTagBlock(BaseModel):
    """Request tag block model."""

    request_id: int
    tag_id: int


class RequestFull(BaseModel):
    """Request full model."""

    title: str
    description: str
    updator: str
    creator: str
    creator_role: Optional[str]
    assets: List[str]
    status: Statuses
    type: Types
    created_timestamp: Optional[int]
    updated_timestamp: Optional[int]
    comments: bool
    comments_objects: List[Comment]
    priority: Priority
    is_tags: Optional[bool]
    sites: Optional[List[str]]
    tags: List[Tag]
    is_all_vectors: Optional[bool]
    vectors: List[Vector]
    deadline: Optional[str]
    id: int

    @staticmethod
    def create_list(data):
        """Create list."""
        result = []
        for i in data:
            if i and i not in result:
                result.append(i)
        return result

    @root_validator(pre=True)
    def convert(cls, values):  # pylint: disable=no-self-argument
        """Convert values."""
        values["tags"] = cls.create_list(values["tags"])
        values["vectors"] = cls.create_list(values["vectors"])
        values["comments_objects"] = cls.create_list(values["comments_objects"])
        return values

    @validator("assets")
    def set_static_url_to_assets(cls, ass: List[str]) -> List[str]:  # pylint: disable=no-self-argument
        """Set static url to assets."""
        return list(
            map(
                lambda a: a.replace(str(settings.STATIC_DIR_INTERNAL), str(settings.STATIC_URL)),
                ass,
            )
        )
