"""Smoke tests for the test-DB isolation fixture (``db`` in ``conftest.py``).

Proves two invariants:

1. The ``db`` fixture binds to the configured *test* DB, NOT the dev DB.
   Writing into the dev DB from a test run would be a critical incident;
   this assertion is the canary.
2. Per-test SAVEPOINT rollback works: a row inserted in one test is
   gone by the next test. Without isolation, suite state would compound
   and ordering would matter.

The fixture itself is documented in ``conftest.py``.
"""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import select, text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import get_database_url
from app.domains.users.models.user import User


@pytest.mark.asyncio
async def test_db_fixture_targets_test_database(db: AsyncSession) -> None:
    """The ``db`` fixture must NEVER bind to the dev DB.

    If this assertion ever flips, every other DB-backed test in the suite
    has been mutating the dev DB. The live connection's database is read via
    ``DATABASE()`` and compared to the database named in the configured test URL.
    """
    # ``DATABASE_URL`` was pinned to the test URL by conftest before any app
    # import, so this is the test DB name.
    expected = make_url(get_database_url()).database
    result = await db.execute(text("SELECT DATABASE()"))
    name = result.scalar_one()
    assert name == expected, (
        f"db fixture is bound to {name!r} — must be {expected!r}. "
        "Check TEST_DATABASE_URL + conftest.py."
    )


@pytest.mark.asyncio
async def test_db_fixture_rollback_isolates_writes_step_one(db: AsyncSession) -> None:
    """Write a teacher row, prove it's there before the test ends.

    Companion to ``..._step_two`` below: those tests run sequentially.
    Without per-test rollback, this insert would survive into step two.
    """
    marker = f"code|isolation-canary-{uuid.uuid4()}"
    db.add(User(auth_id=marker, email="canary@test.local", role="teacher"))
    await db.flush()

    found = await db.execute(select(User).where(User.auth_id == marker))
    assert found.scalar_one_or_none() is not None


@pytest.mark.asyncio
async def test_db_fixture_rollback_isolates_writes_step_two(db: AsyncSession) -> None:
    """After step one's rollback, no isolation-canary row survives.

    Confirms the per-test SAVEPOINT rollback in ``conftest.py::db``.
    """
    found = await db.execute(select(User).where(User.auth_id.like("code|isolation-canary-%")))
    assert found.scalar_one_or_none() is None, (
        "isolation-canary row survived the previous test — per-test rollback "
        "is broken. Check conftest.py::db's outer.rollback() teardown."
    )
