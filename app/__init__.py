"""Main factory builder of ``FastAPI`` server."""
from fastapi import Depends, FastAPI

from app.configuration import __containers__
from app.configuration.server import Server
from app.internal.pkg.middlewares.static import AuthStaticFiles
from app.internal.pkg.middlewares.x_auth_token import get_x_token_key
from app.pkg.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(dependencies=[Depends(get_x_token_key)])
    app.mount(
        path="/static",
        app=AuthStaticFiles(
            x_static_token=settings.X_STATIC_TOKEN,
            directory=settings.STATIC_DIR_INTERNAL,
        ),
        name="static",
    )
    __containers__.wire_packages(app=app)
    return Server(app).get_app()
