"""Give each pytest session a test database no other session can touch.

Why a session needs its own
===========================

A session rebuilds the schema by dropping every table (``conftest._rebuild_schema``),
so two sessions aimed at one database destroy each other: the later session's drop
pulls the tables out from under the earlier one, which then dies inside a fixture
with ``Table '<db>.<table>' doesn't exist``. The wreckage lands wherever the victim
happened to be, so a different subset of tests errors each run and it reads as flaky
concurrency tests rather than as interference.

Sharing is the default rather than an edge case: each git worktree has its own
checkout but no ``.env``, so all of them fall back to the same ``lpcg_test``.

Naming a database after the process that owns it keeps sessions apart — across
worktrees, or several within one. A killed session never drops its database, so
each session first reclaims the ones whose owner is gone; a recycled PID that now
belongs to something else only delays that reclaim by a run.
"""

from __future__ import annotations

import os
import re
from collections.abc import Iterator
from contextlib import contextmanager, suppress

import pymysql
import pymysql.cursors
from sqlalchemy.engine import URL, make_url

_OWNER = re.compile(r"_p(\d+)\Z")

DEFAULT_BASE_URL = "mysql+aiomysql://lpcg:lpcg@localhost:3306/lpcg_test"


def base_url() -> str:
    """The database each session's own is derived from.

    Lives here rather than in ``conftest`` because ``tests/`` and
    ``tests/concurrency/`` both hold a module named ``conftest`` and neither is a
    package, so ``import conftest`` resolves to whichever pytest loaded first.
    """
    return os.environ.get("TEST_DATABASE_URL", DEFAULT_BASE_URL)


def claim(base: str) -> str:
    """Create a database owned by this process and return its URL.

    Yields ``base`` untouched when the server refuses the connection or the
    credentials cannot create databases, which keeps the fake-backed majority of the
    suite runnable and lets the DB-backed tests report the real error themselves.
    """
    url = make_url(base)
    if url.database is None:
        return base
    owned = f"{url.database}{_owner_suffix()}"
    try:
        with _server(url) as connection, connection.cursor() as cursor:
            _reclaim_abandoned(cursor, url.database)
            cursor.execute(f"DROP DATABASE IF EXISTS `{owned}`")
            cursor.execute(f"CREATE DATABASE `{owned}`")
    except pymysql.err.OperationalError as exc:
        print(f"session_database: cannot provision {owned!r} ({exc}); sharing {url.database!r}")
        return base
    return url.set(database=owned).render_as_string(hide_password=False)


def release(claimed_url: str) -> None:
    """Drop the database :func:`claim` created for this process.

    The owner-suffix check is the safety rail: a shared database, or one belonging to
    a live sibling session, can never be dropped from here.
    """
    url = make_url(claimed_url)
    if not url.database or not url.database.endswith(_owner_suffix()):
        return
    try:
        with _server(url) as connection, connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS `{url.database}`")
    except pymysql.err.OperationalError as exc:
        print(f"session_database: {url.database!r} left behind ({exc})")


@contextmanager
def scratch(claimed_url: str, label: str) -> Iterator[str]:
    """An empty database beside the session's own, for a test that runs a process of its own.

    The process commits, and a commit is not rolled back with the test's transaction.
    """
    url = make_url(claimed_url)
    name = f"{url.database}_{label}"
    with _server(url) as connection, connection.cursor() as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS `{name}`")
        cursor.execute(f"CREATE DATABASE `{name}`")
    try:
        yield url.set(database=name).render_as_string(hide_password=False)
    finally:
        with _server(url) as connection, connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS `{name}`")


def _owner_suffix() -> str:
    return f"_p{os.getpid()}"


def _server(url: URL) -> pymysql.connections.Connection:
    """Connect to the server with no database selected, so DDL on databases is legal."""
    return pymysql.connect(
        host=url.host or "localhost",
        port=url.port or 3306,
        user=url.username,
        password=url.password,
        autocommit=True,
    )


def _reclaim_abandoned(cursor: pymysql.cursors.Cursor, base_name: str) -> None:
    """Drop the databases whose owning session is no longer running.

    Housekeeping, not correctness: sibling sessions starting together sweep the same
    list, so losing the race to drop one of them must not fail the run that lost.
    """
    cursor.execute("SHOW DATABASES")
    for (name,) in cursor.fetchall():
        owner = _owner_of(name, base_name)
        if owner is None or _process_exists(owner):
            continue
        with suppress(pymysql.err.Error):
            cursor.execute(f"DROP DATABASE IF EXISTS `{name}`")


def _owner_of(name: str, base_name: str) -> int | None:
    """The PID in ``<base_name>_p<pid>``, or None for a database that isn't ours."""
    if not name.startswith(base_name):
        return None
    owner = _OWNER.fullmatch(name.removeprefix(base_name))
    return int(owner.group(1)) if owner else None


def _process_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True
