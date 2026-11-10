"""Database configuration.

``DATABASE_URL`` wins if set; otherwise the DSN is composed from the ``DB_*``
parts. The app database is MySQL.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database connection settings, sourced from the environment / ``.env``."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str | None = None
    db_host: str = "localhost"
    db_port: str = "3306"
    db_name: str = "lpcg"
    db_user: str = "lpcg"
    db_password: str = "lpcg"

    @property
    def url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


def get_database_url() -> str:
    return DatabaseSettings().url


def get_sync_database_url() -> str:
    """Return a sync-driver URL suitable for ``sqlalchemy.create_engine``.

    When ``DATABASE_URL`` is set to an async driver (``mysql+aiomysql``),
    callers that need a sync engine (data-migrations, jobs, tests) would
    fail.  This normalises to ``mysql+pymysql``.
    """
    from sqlalchemy.engine import make_url

    url = make_url(get_database_url())
    if url.drivername == "mysql+aiomysql":
        url = url.set(drivername="mysql+pymysql")
    return url.render_as_string(hide_password=False)
