"""Tests for the per-session test-database provisioning in ``session_database``.

The safety-critical property is negative: a session must drop ONLY the database it
created. Dropping a sibling's would resurrect exactly the cross-session schema
destruction this module exists to prevent, so the ownership checks are pinned here
rather than left to inspection.

The fixtures below use a base name derived from this process's PID so two of these
suites running at once (the case this module makes safe) never share scratch names.
"""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest
import session_database
from sqlalchemy.engine import make_url

_LIVE_FOREIGN_PID = 1  # launchd — always running, never ours


@pytest.fixture
def scratch_base() -> Iterator[str]:
    """A base URL on the configured server whose databases no real session owns.

    The PID in the name keeps two of these suites running at once off each other's
    scratch databases.
    """
    configured = make_url(session_database.base_url())
    base = configured.set(database=f"{configured.database}_sweep{os.getpid()}").render_as_string(
        hide_password=False
    )
    yield base
    _drop_matching(base)


def _drop_matching(base_url: str) -> None:
    url = make_url(base_url)
    with session_database._server(url) as connection, connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES")
        for (name,) in cursor.fetchall():
            if name.startswith(url.database):
                cursor.execute(f"DROP DATABASE IF EXISTS `{name}`")


def _create(base_url: str, suffix: str) -> str:
    url = make_url(base_url)
    name = f"{url.database}{suffix}"
    with session_database._server(url) as connection, connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{name}`")
    return name


def _databases(base_url: str) -> set[str]:
    url = make_url(base_url)
    with session_database._server(url) as connection, connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES")
        return {name for (name,) in cursor.fetchall()}


def test_owner_of_reads_only_our_own_naming() -> None:
    """``<base>_p<pid>`` identifies an owner; anything else is someone else's."""
    assert session_database._owner_of("lpcg_test_p4321", "lpcg_test") == 4321
    assert session_database._owner_of("lpcg_test", "lpcg_test") is None
    assert session_database._owner_of("lpcg_test_w0", "lpcg_test") is None
    assert session_database._owner_of("lpcg_test_p12_extra", "lpcg_test") is None
    assert session_database._owner_of("other_p12", "lpcg_test") is None


def test_release_refuses_a_database_it_does_not_own(monkeypatch: pytest.MonkeyPatch) -> None:
    """A URL without our owner suffix must not even reach the server.

    This is the guard that keeps a fallback-to-shared session from dropping the
    shared database out from under everyone else.
    """

    def _forbidden(url: object) -> object:
        raise AssertionError(f"release opened a connection for a database it does not own: {url}")

    shared = session_database.base_url()
    monkeypatch.setattr(session_database, "_server", _forbidden)
    session_database.release(shared)
    session_database.release(f"{shared}_p{os.getpid() + 1}")


def test_claim_creates_a_private_database_and_release_drops_it(scratch_base: str) -> None:
    claimed = session_database.claim(scratch_base)
    name = make_url(claimed).database

    assert name == f"{make_url(scratch_base).database}_p{os.getpid()}"
    assert name in _databases(scratch_base)

    session_database.release(claimed)
    assert name not in _databases(scratch_base)


def test_claim_reclaims_dead_owners_and_spares_live_ones(scratch_base: str) -> None:
    """The sweep is what stops killed sessions leaking databases forever."""
    abandoned = _create(scratch_base, "_p999999")
    in_use = _create(scratch_base, f"_p{_LIVE_FOREIGN_PID}")

    claimed = session_database.claim(scratch_base)
    surviving = _databases(scratch_base)

    assert abandoned not in surviving
    assert in_use in surviving
    session_database.release(claimed)
