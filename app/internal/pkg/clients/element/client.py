from app.internal.pkg.clients.baseclient import BaseClient

__all__ = ["ElementClient"]

from app.pkg import models


class ElementClient(BaseClient):
    async def send_message(self, cmd: models.ElementNotify) -> int:
        response = await self.do_request(
            method="POST",
            path="send_message/",
            json=cmd.to_dict(),
        )
        return response.status_code
