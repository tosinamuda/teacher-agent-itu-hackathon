"""The plugin commands run as a process of their own, as a deploy runs them."""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url

from app.db.metadata import target_metadata
from tests import session_database
from tests.conftest import TEST_DATABASE_URL
from tests.plugin_folder import write_plugin

BACKEND = Path(__file__).resolve().parents[1]


def _run(database: str, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "app.domains.content.plugins", *arguments],
        cwd=BACKEND,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
        env={**os.environ, "DATABASE_URL": database},
    )


@contextmanager
def _own_database() -> Iterator[str]:
    """A database with the app's tables, beside the session's, for a process that commits."""
    with session_database.scratch(TEST_DATABASE_URL, "cli") as database:
        engine = create_engine(make_url(database).set(drivername="mysql+pymysql"))
        target_metadata.create_all(engine)
        engine.dispose()
        yield database


def test_sync_installs_the_plugin_in_a_process_of_its_own_and_changes_nothing_the_second_time(
    tmp_path: Path,
) -> None:
    plugin = write_plugin(tmp_path / "p", "cli-sync-check", "cli-sync-check")
    with _own_database() as database:
        first = _run(database, "sync", str(plugin))
        second = _run(database, "sync", str(plugin))
        listed = _run(database, "list")

    assert first.returncode == 0, first.stderr
    assert "installed, revision 1" in first.stdout
    assert second.returncode == 0, second.stderr
    assert "revision 1" in second.stdout
    assert "cli-sync-check 1.0.0 r1" in listed.stdout


def test_remove_if_installed_retires_what_is_installed_and_ignores_what_is_not(
    tmp_path: Path,
) -> None:
    plugin = write_plugin(tmp_path / "p", "cli-sync-check", "cli-sync-check")
    with _own_database() as database:
        never = _run(database, "remove", "--if-installed", "cli-sync-check")
        _run(database, "sync", str(plugin))
        retired = _run(database, "remove", "--if-installed", "cli-sync-check")
        again = _run(database, "remove", "--if-installed", "cli-sync-check")

    assert (never.returncode, never.stdout.strip()) == (0, "cli-sync-check: not installed")
    assert retired.returncode == 0 and "removed" in retired.stdout
    assert (again.returncode, again.stdout.strip()) == (0, "cli-sync-check: not installed")
