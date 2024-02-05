import logging

from app.pkg.settings import settings


class Logger:
    def __init__(self):
        self._log_format = (
            "%(asctime)s - %(levelname)s - %(name)s" " - %(filename)s - %(funcName)s - %(lineno)d - %(message)s"
        )

    def get_stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(self._log_format))
        return stream_handler

    def get_logger(self, name):
        logger = logging.getLogger(name)

        stream_handler = self.get_stream_handler()
        if not logger.hasHandlers():
            logger.addHandler(stream_handler)
        logger.setLevel(settings.LOGGER_LEVEL)
        return logger
