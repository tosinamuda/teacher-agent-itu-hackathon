"""Where uploaded provenance images live on disk.

A media dir OUTSIDE the app checkout, so the deploy's ``git pull --force`` can't
wipe it; overridable by the ``UPLOADS_DIR`` env var (prod points it at e.g.
/var/lib/lpcg/uploads). Dev defaults to a gitignored ``var/uploads`` under the
backend.
"""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config import BACKEND_DIR

_DEFAULT_UPLOADS_DIR = BACKEND_DIR / "var" / "uploads"


class StorageSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    uploads_dir: str = str(_DEFAULT_UPLOADS_DIR)


def get_uploads_dir() -> Path:
    path = Path(StorageSettings().uploads_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path
