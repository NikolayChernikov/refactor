"""Logger module."""
from .base import BaseEnum

__all__ = [
    "Logger",
]


class BaseLogger(BaseEnum):
    """Base logger class."""


class Logger(str, BaseLogger):
    """Logger class."""

    WARNING = "WARNING"
    INFO = "INFO"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"
    NOTSET = "NOTSET"
