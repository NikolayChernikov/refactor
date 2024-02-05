"""Server configuration.

Collect or build all requirements for startup. Provide global point to
``Server`` instance.
"""

from app.internal.pkg.clients import Clients
from app.internal.pkg.utils import Utils
from app.internal.repository import Repositories
from app.internal.services import Services
from app.pkg.connectors import Connectors
from app.pkg.logger import LoggerContainer
from app.pkg.models.core import Container, Containers

__all__ = ["__containers__"]

__containers__ = Containers(
    pkg_name=__name__,
    containers=[
        Container(container=Repositories),
        Container(container=Services),
        Container(container=Connectors),
        Container(container=LoggerContainer),
        Container(container=Clients),
        Container(container=Utils),
    ],
)
