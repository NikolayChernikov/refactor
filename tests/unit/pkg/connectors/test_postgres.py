"""Test Postgres module."""
# pylint: disable=redefined-outer-name
import pytest

from app.pkg.connectors.postgres import Postgres
from app.pkg.settings.settings import Settings, get_settings


@pytest.fixture
def config() -> Settings:
    """get settings."""
    return get_settings()


@pytest.fixture
def postgres_service(config: Settings) -> Postgres:
    """get postgres instance."""
    return Postgres(
        config.POSTGRES_USER, config.POSTGRES_PASSWORD, config.POSTGRES_HOST, config.POSTGRES_PORT, config.POSTGRES_DB
    )


class TestPostgres:
    """Test postgres class."""

    def test_get_dsn(self, postgres_service: Postgres) -> None:
        """test get dsn."""
        assert postgres_service.get_dsn()
