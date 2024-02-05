"""Logger module."""
import logging

from app.pkg.settings import settings


class Logger:
    """Logger class."""

    def __init__(self) -> None:
        self._log_format = (
            "%(asctime)s - %(levelname)s - %(name)s"
            " - %(filename)s - %(funcName)s - %(lineno)d - %(message)s"  # pylint: disable=implicit-str-concat
        )

    def get_stream_handler(self):
        """Get stream handler.

        Returns: ...
        """
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(self._log_format))
        return stream_handler

    def get_logger(self, name):
        """Get logger.

        Args:
            name: logger name.

        Returns: logger.
        """
        logger = logging.getLogger(name)

        stream_handler = self.get_stream_handler()
        if not logger.hasHandlers():
            logger.addHandler(stream_handler)
        logger.setLevel(settings.LOGGER_LEVEL)
        return logger
