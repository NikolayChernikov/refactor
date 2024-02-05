"""Element client module."""
from app.internal.pkg.clients.baseclient import BaseClient

__all__ = ["ElementClient"]

from app.pkg import models


class ElementClient(BaseClient):
    """Element client class."""

    async def send_message(self, cmd: models.ElementNotify) -> int:
        """Register on startup events.
        Args:
            cmd: body with room number.

        Returns: HTTP status code.
        """
        response = await self.do_request(
            method="POST",
            path="send_message/",
            json=cmd.to_dict(),
        )
        return response.status_code
