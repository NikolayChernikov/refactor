import pathlib
from functools import lru_cache

import pydantic
from dotenv import find_dotenv
from pydantic import validator
from pydantic.env_settings import BaseSettings

from app.pkg.models import Logger


class _Settings(BaseSettings):
    class Config:
        env_file_encoding = "utf-8"
        arbitrary_types_allowed = True


class Settings(_Settings):
    # FastAPI
    X_API_TOKEN: pydantic.SecretStr

    # Static
    X_STATIC_TOKEN: pydantic.SecretStr
    STATIC_DIR: pathlib.Path
    STATIC_DIR_INTERNAL: pathlib.Path
    STATIC_URL: pathlib.Path

    # Timezone
    TZ: str

    # Postgres
    POSTGRES_HOST: pydantic.StrictStr
    POSTGRES_PORT: pydantic.PositiveInt
    POSTGRES_USER: pydantic.StrictStr
    POSTGRES_PASSWORD: pydantic.SecretStr
    POSTGRES_DB: pydantic.StrictStr

    # Telegram
    TELEGRAM_API_TOKEN: pydantic.SecretStr
    TELEGRAM_CHAT_ID: int

    # Logger
    LOGGER_LEVEL: Logger

    CENT_API_KEY: pydantic.SecretStr
    CENT_IT_REQUEST_CHANNEL: str
    CENT_HOST: str
    CENT_PORT: pydantic.PositiveInt

    # matrix
    ELEMENT_URL: pydantic.HttpUrl
    ELEMENT_X_ACCESS_TOKEN: pydantic.SecretStr
    ELEMENT_ROOM_ID_REQUESTS: str
    ELEMENT_ROOM_ID_REQUESTS_NO_NOTIFICATION: str

    @validator("STATIC_DIR_INTERNAL")
    def create_directory(cls, v: pathlib.Path) -> pathlib.Path:
        if not v.exists():
            v.mkdir(parents=True, exist_ok=True)
        return v


@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    return Settings(_env_file=find_dotenv(env_file))
