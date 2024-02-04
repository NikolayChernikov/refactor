from .base import BaseEnum

__all__ = [
    "Logger",
]


class BaseLogger(BaseEnum):
    ...


class Logger(str, BaseLogger):
    WARNING = "WARNING"
    INFO = "INFO"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"
    NOTSET = "NOTSET"
