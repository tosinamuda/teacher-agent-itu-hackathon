"""pytest configuration + shared fixtures.

Test-DB isolation
=================

Tests that touch SQLAlchemy use the ``db`` fixture (defined below). It:

- runs against a SEPARATE database private to this pytest session
  (``lpcg_test_p<pid>``, see ``session_database``) — never the dev DB,
  and never a database another session is rebuilding,
- has its schema applied via ``target_metadata.create_all()`` once per
  session (same engine, same ORM definitions, no in-memory SQLite
  trickery),
- wraps every test in a SAVEPOINT that is rolled back when the test
  exits, so writes never leak between tests.

Tests that use fakes (the majority) don't request ``db`` and are
unaffected.

Configuration
-------------

``TEST_DATABASE_URL`` (defaulting to
``mysql+aiomysql://lpcg:lpcg@localhost:3306/lpcg_test``) names the BASE
database; the one this session actually uses is derived from it and
created per-process by ``session_database``. Before importing any app
module, this conftest sets ``DATABASE_URL`` to that derived URL so any
code that resolves the DSN at import time (Celery worker boot,
``app.db.session.create_async_engine``) gets the session's own database
rather than the dev DB. The dev ``.env`` is NOT consulted because
``alembic/env.py`` and ``app/db/config.py`` both respect external env
vars first.

Schema-from-metadata vs Alembic
-------------------------------

The schema is applied via ``target_metadata.create_all()`` rather than
``alembic upgrade head`` because the migration chain has two known
fresh-deploy bugs surfaced while wiring this up:

1. ``alembic_version.version_num`` was auto-created as ``VARCHAR(32)``
   but several revision IDs exceed 32 chars. (Fixed in ``env.py`` —
   pre-create the table with ``VARCHAR(255)``.)
2. A P5.2 migration ``DROP CONSTRAINT lessons_workspace_id_fkey``
   references a constraint that no fresh-deploy ever creates. (NOT
   fixed in this commit — separate work item to unwind the migration
   chain so ``alembic upgrade head`` succeeds against a fresh DB.)

``create_all()`` against the live ORM metadata is functionally
equivalent for tests (same tables, same columns, same types and FK
constraints we care about), and side-steps the broken history. The
``alembic upgrade head`` path remains the
authoritative production path; tests are the documentation-by-example
for the schema, not its source of truth.

Per-test transaction pattern
----------------------------

The fixture pattern is the SQLAlchemy "join external transaction"
recipe: open a connection, begin an outer transaction, bind a session
to that connection, yield it to the test, then rollback the outer
transaction on teardown. Any ``session.commit()`` inside the test
commits a SAVEPOINT, not the outer transaction, so the rollback at
teardown still discards everything.

The first test to ask for ``db`` triggers schema setup once per session;
subsequent tests reuse the engine. Engine cleanup happens at session
end.
"""

from __future__ import annotations

import os
import sys
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
import pytest_asyncio
import session_database
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Force the app's DATABASE_URL to the test DB BEFORE any app import.
# Once ``app.db.session`` imports, it captures the URL — this is the only
# safe time to redirect it. Tests that don't touch the DB are unaffected.
TEST_DATABASE_URL = session_database.claim(session_database.base_url())
os.environ["DATABASE_URL"] = TEST_DATABASE_URL


#: The LLM role configuration, which no test may inherit from the developer's machine.
#: ``import litellm`` calls ``load_dotenv()`` as an import side effect, so the real .env
#: lands in os.environ during collection. That made the suite's result depend on a
#: gitignored file: adding GENERATOR_MODEL to .env turned three green tests red in the
#: full run only, while each still passed when run alone. Popping at conftest import is
#: too early — litellm has not been imported yet — so it is done per test below.
# Seven test modules import ``app.main``, which builds the generator LM at import
# time and so demands a key during COLLECTION — before any fixture has run. On a
# machine with a .env that passed silently; in a clean checkout every one of them
# failed to collect. A default set here is in place before the first test module
# is imported, and ``load_dotenv`` never overrides a variable that is already set,
# so it cannot be displaced by the developer's real key either.
os.environ.setdefault("BEDROCK_MANTLE_API_KEY", "test-key-not-a-real-one")

ROLE_SETTINGS = (
    "BEDROCK_MANTLE_API_KEY",
    "GENERATOR_API_BASE",
    "GENERATOR_API_KEY",
    "GENERATOR_MODEL",
    "GENERATOR_PROVIDER",
    "JUDGE_API_BASE",
    "JUDGE_API_KEY",
    "JUDGE_MODEL",
    "JUDGE_PROVIDER",
    "LLM_API_BASE",
    "LLM_API_KEY",
    "BEDROCK_ENDPOINT",
    "AWS_BEARER_TOKEN_BEDROCK",
    "OPENROUTER_API_KEY",
)


def pytest_sessionfinish() -> None:
    """Hand this session's database back once the last test has finished."""
    session_database.release(TEST_DATABASE_URL)


@pytest.fixture(autouse=True)
def _kept_agents_in_a_temporary_folder(
    monkeypatch: pytest.MonkeyPatch, tmp_path_factory: pytest.TempPathFactory
) -> None:
    """A kept agent's home is a folder of the test, never the checkout's."""
    from app.domains.content_engine.infrastructure.harness import opencode_home

    monkeypatch.setattr(opencode_home, "SESSIONS_DIR", tmp_path_factory.mktemp("kept-agents"))


@pytest.fixture(autouse=True)
def _no_ambient_llm_config(monkeypatch: pytest.MonkeyPatch) -> None:
    """Every test starts with no LLM endpoint, key or model — see ``ROLE_SETTINGS``.

    A test that needs one sets it with monkeypatch, which also restores it afterwards.
    """
    for setting in ROLE_SETTINGS:
        monkeypatch.delenv(setting, raising=False)
    # A stand-in for the host key. The model assignment lives in code now, so a test that
    # builds an LM resolves a real host and is right to demand a key — but it must be this
    # one and never the developer's. Tests about a MISSING key delete it themselves.
    monkeypatch.setenv("BEDROCK_MANTLE_API_KEY", "test-key-not-a-real-one")


# Load the ORM model graph in the correct order BEFORE any test module imports the
# artefacts/experiments packages. Importing those packages "build-job first" trips a
# pre-existing experiments<->artefacts circular import; importing metadata first
# (which the running app also does, via app.main) establishes the safe order.
import app.db.metadata  # noqa: E402,F401
from app.db.metadata import target_metadata  # noqa: E402


async def _rebuild_schema(engine: AsyncEngine) -> None:
    """Drop every table in the test DB, then recreate it from the ORM metadata.

    ``create_all`` only CREATES missing tables — it never ALTERS an existing one.
    So a database left over from an older schema would silently lack
    newly-added columns/constraints, and tests (e.g. the concurrency suite's
    constraint checks) would pass against a stale shape. Dropping first
    guarantees the schema always matches the current models, with no manual
    "drop the test DB" step.

    Dropping with FK checks off means dependency order doesn't matter, and it
    clears non-ORM tables too (``casbin_rule``, ``alembic_version``) so nothing
    stale survives.
    """
    async with engine.connect() as conn:
        await conn.exec_driver_sql("SET FOREIGN_KEY_CHECKS=0")
        result = await conn.exec_driver_sql(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = DATABASE() AND table_type = 'BASE TABLE'"
        )
        for row in result.fetchall():
            await conn.exec_driver_sql(f"DROP TABLE IF EXISTS `{row[0]}`")
        await conn.exec_driver_sql("SET FOREIGN_KEY_CHECKS=1")
        await conn.commit()
    async with engine.begin() as conn:
        await conn.run_sync(target_metadata.create_all)


@pytest_asyncio.fixture(scope="session")
async def _test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """One engine per test session against a freshly-rebuilt schema.

    The schema is dropped and recreated from the ORM metadata once per session
    (see ``_rebuild_schema``), so successive runs never inherit a stale shape.
    """
    # NullPool: the engine is session-scoped but pytest-asyncio runs each test in
    # its own event loop. A pooled aiomysql connection is bound to the loop that
    # opened it, so reusing it from a later test's loop raises "Future attached to
    # a different loop". NullPool opens a fresh connection per ``connect()`` in the
    # caller's current loop, sidestepping cross-loop reuse.
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    await _rebuild_schema(engine)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db(_test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Per-test ``AsyncSession`` with automatic rollback.

    Uses SQLAlchemy's "join external transaction" pattern: a connection
    holds an outer transaction; the session runs inside it. Whatever the
    test does — ``add``, ``flush``, even ``commit`` — is discarded when
    the outer transaction rolls back on teardown.

    The session has the same config as the production session factory
    (``autoflush=False``, ``expire_on_commit=False``) so test-DB behaviour
    matches dev-DB behaviour at the session boundary.
    """
    connection: AsyncConnection = await _test_engine.connect()
    outer = await connection.begin()
    session_maker = async_sessionmaker(
        bind=connection,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    session = session_maker()
    try:
        yield session
    finally:
        await session.close()
        await outer.rollback()
        await connection.close()


# Hypothesis runs at a regression-guard size by default: enough to catch a
# reintroduced bug on every commit, small enough not to dominate the suite. A
# fuzz campaign is a different job, so it is a profile rather than a new default
# — HYPOTHESIS_PROFILE=deep turns the same properties into a long random search.
import os  # noqa: E402

from hypothesis import HealthCheck, Verbosity  # noqa: E402
from hypothesis import settings as _hypothesis_settings  # noqa: E402

_hypothesis_settings.register_profile(
    "deep",
    max_examples=2000,
    deadline=None,
    derandomize=False,
    print_blob=True,
    suppress_health_check=[HealthCheck.too_slow],
    verbosity=Verbosity.normal,
)
_hypothesis_settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "default"))
