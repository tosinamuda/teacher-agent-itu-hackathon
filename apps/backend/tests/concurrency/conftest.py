"""Fixtures for DB-backed concurrency tests.

Why these need their own harness
================================

The default ``db`` fixture (``tests/conftest.py``) wraps each test in a single
connection + outer transaction that is rolled back on teardown — every
``commit()`` inside the test is only a SAVEPOINT. That is ideal for isolation
but useless for concurrency: two "concurrent" operations sharing that one
connection are serialized by the connection itself and never actually contend
for an InnoDB row lock or trip a unique constraint *across transactions*.

These tests need the opposite — several INDEPENDENT sessions, each on its own
connection, each committing for real — so the database's locks and constraints
are what arbitrate the race (exactly as in production under concurrent
requests). ``session_factory`` provides that.

Because the writes really commit, rollback-on-teardown can't clean them up, so
each test truncates every table before and after it runs. This is safe: the
test DB (this session's own ``lpcg_test_p<pid>``, provisioned in
``tests/conftest.py``) is disposable, is never the dev DB, and is never shared
with another pytest session.
"""

from __future__ import annotations

import asyncio
from collections import namedtuple
from collections.abc import AsyncGenerator, Awaitable, Callable

import pytest_asyncio
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.db.metadata import target_metadata

# The outcome of a race: the operations that returned (wins), the ones that
# raised the EXPECTED conflict (conflicts), and any UNEXPECTED exceptions
# (others — must always be empty: a lost race must never surface as a 500).
RaceOutcome = namedtuple("RaceOutcome", "wins conflicts others")


async def _truncate_all(engine: AsyncEngine) -> None:
    """Empty every ORM table (FK checks off) so each test starts from clean state.

    Iterates ``target_metadata`` so it tracks the schema automatically. Non-ORM
    tables (``casbin_rule``, ``alembic_version``) aren't in the metadata and are
    left alone. ``TRUNCATE`` implicitly commits in MySQL; ``SET FOREIGN_KEY_CHECKS``
    is a session variable that applies immediately, so child-before-parent order
    doesn't matter.
    """
    async with engine.connect() as conn:
        await conn.exec_driver_sql("SET FOREIGN_KEY_CHECKS=0")
        for table in reversed(target_metadata.sorted_tables):
            await conn.exec_driver_sql(f"TRUNCATE TABLE `{table.name}`")
        await conn.exec_driver_sql("SET FOREIGN_KEY_CHECKS=1")
        await conn.commit()


@pytest_asyncio.fixture
async def session_factory(
    _test_engine: AsyncEngine,
) -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    """Factory for independent, real-committing sessions — one per concurrent task.

    Hand each ``asyncio`` task its OWN session from this factory (a session is
    not safe to share across tasks). Nothing is rolled back on teardown; the
    table truncation around the test is the cleanup. Matches the production
    session config (``autoflush=False``, ``expire_on_commit=False``).
    """
    maker = async_sessionmaker(
        bind=_test_engine,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    await _truncate_all(_test_engine)
    try:
        yield maker
    finally:
        await _truncate_all(_test_engine)


@pytest_asyncio.fixture
def run_race(
    session_factory: async_sessionmaker[AsyncSession],
) -> Callable[..., Awaitable[RaceOutcome]]:
    """Fire ``op`` from ``n`` independent sessions at once; classify the outcome.

    ``op(session, i)`` runs the contended operation on its own fresh session
    (index ``i`` lets callers vary non-keyed fields, e.g. distinct emails so the
    race is on the intended unique key). ``is_conflict(exc)`` decides whether a
    raised exception is the EXPECTED lost-race signal (the domain's 409) versus
    an unexpected failure. Returns a :class:`RaceOutcome`; assert
    ``outcome.others == []`` to prove no race ever became a 500.
    """

    async def _run(
        op: Callable[[AsyncSession, int], Awaitable[object]],
        is_conflict: Callable[[BaseException], bool],
        *,
        n: int = 10,
    ) -> RaceOutcome:
        async def one(i: int) -> object:
            async with session_factory() as session:
                return await op(session, i)

        results = await asyncio.gather(*(one(i) for i in range(n)), return_exceptions=True)
        wins = [r for r in results if not isinstance(r, BaseException)]
        conflicts = [r for r in results if isinstance(r, BaseException) and is_conflict(r)]
        others = [r for r in results if isinstance(r, BaseException) and not is_conflict(r)]
        return RaceOutcome(wins=wins, conflicts=conflicts, others=others)

    return _run


@pytest_asyncio.fixture
def count_rows(
    session_factory: async_sessionmaker[AsyncSession],
) -> Callable[..., Awaitable[int]]:
    """Count rows of ``model`` matching equality ``filters`` on a fresh session.

    Used after a race to assert exactly one row materialized — the duplicate-free
    invariant the unique constraints exist to guarantee.
    """

    async def _count(model: type, **filters: object) -> int:
        async with session_factory() as session:
            stmt = select(func.count()).select_from(model)
            for column, value in filters.items():
                stmt = stmt.where(getattr(model, column) == value)
            return await session.scalar(stmt)

    return _count
