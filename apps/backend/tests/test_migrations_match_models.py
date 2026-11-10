"""The migrations after the last released schema bring a database level with the models.

``0001_baseline`` builds a fresh database from the models, so a fresh database cannot show a
model change that lacks a migration. This test starts from the schema at ``0025_job_results``,
which production runs, applies every later migration, and compares the result with the models.
After a release, replace ``schema_baseline/schema_0025.sql`` with the released schema.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, make_url

from app.db.config import get_sync_database_url

BACKEND = Path(__file__).resolve().parents[1]
BASELINE = Path(__file__).with_name("schema_baseline") / "schema_0025.sql"
BASELINE_REVISION = "0025_job_results"


@pytest.fixture
def scratch_database() -> Iterator[str]:
    """A database of its own, named so the test user may create and drop it."""
    base = make_url(get_sync_database_url())
    name = f"lpcg_test_migrations_p{os.getpid()}"
    admin = create_engine(base, isolation_level="AUTOCOMMIT")
    with admin.connect() as connection:
        connection.execute(text(f"DROP DATABASE IF EXISTS `{name}`"))
        connection.execute(text(f"CREATE DATABASE `{name}`"))
    try:
        yield base.set(database=name).render_as_string(hide_password=False)
    finally:
        with admin.connect() as connection:
            connection.execute(text(f"DROP DATABASE IF EXISTS `{name}`"))
        admin.dispose()


def _load_baseline(engine: Engine) -> None:
    statements = [s.strip() for s in BASELINE.read_text(encoding="utf-8").split(";\n") if s.strip()]
    with engine.begin() as connection:
        connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        for statement in statements:
            connection.exec_driver_sql(statement.replace("%", "%%"))
        connection.execute(
            text("INSERT INTO alembic_version (version_num) VALUES (:revision)"),
            {"revision": BASELINE_REVISION},
        )


def test_migrations_applied_to_the_released_schema_leave_no_difference_with_the_models(
    scratch_database: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    engine = create_engine(scratch_database)
    _load_baseline(engine)
    engine.dispose()
    monkeypatch.setenv("DATABASE_URL", scratch_database)
    monkeypatch.chdir(BACKEND)
    config = Config(str(BACKEND / "alembic.ini"))

    command.upgrade(config, "head")

    command.check(config)
