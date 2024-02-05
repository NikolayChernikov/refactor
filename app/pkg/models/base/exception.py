"""Base api exceptions."""
import pydantic
from fastapi import HTTPException

__all__ = ["BaseAPIException"]


class BaseAPIException(HTTPException):
    """Base API exception class."""

    message: str
    status_code: pydantic.PositiveInt

    def __init__(self, message=None) -> None:
        """Init service."""
        if message is not None:
            self.message = message

        super().__init__(status_code=self.status_code, detail=self.message)

    def build_docs(self) -> dict:
        """Build docs.

        Returns: dict docs
        """
        return {
            str(self.status_code): {
                "description": "Item requested by ID",
                "content": {"application/json": {"example": {"message": self.message}}},
            },
        }
