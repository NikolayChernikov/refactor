import os
import re
import base64
from pathlib import Path
from typing import List, Optional, Union
from datetime import datetime

import aiofiles

from app.pkg.logger import Logger
from app.pkg.models.exceptions.requests import BadBase64OfImage

__all__ = [
    "Filer",
]


class Filer:
    _logger: Logger
    _static_dir: Path
    _static_dir_internal: Path
    _static_url: Path

    def __init__(
            self,
            logger: Logger,
            static_dir: Path,
            static_dir_internal: Path,
            static_url: Path,
    ):
        self._logger = logger.get_logger(__name__)
        self._static_dir = static_dir
        self._static_dir_internal = static_dir_internal
        self._static_url = static_url

    async def save_image(
            self,
            base64_: str,
            name: Optional[Union[str, int]] = None,
    ) -> Path:
        try:
            filename = f"{int(datetime.utcnow().timestamp())}.jpeg"
            if name:
                filename = f"{name}_{filename}"
            path = self._static_dir_internal.joinpath(filename)
            async with aiofiles.open(path, "wb") as f:
                await f.write(base64.urlsafe_b64decode(bytes(base64_, encoding="latin-1")))
            return path
        except Exception:
            raise BadBase64OfImage

    @staticmethod
    def delete(files: List[str]):
        for path in files:
            try:
                os.remove(path)
            except OSError:
                pass
