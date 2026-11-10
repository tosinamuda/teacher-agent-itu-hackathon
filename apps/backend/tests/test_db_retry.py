"""Unit tests for the contended-write retry helpers (app/db/retry.py).

These pin the two concurrency behaviours that previously surfaced as 500s:
a duplicate-key race on derived codes, and an InnoDB deadlock under concurrent
writes. No database is needed — the session and the failing commit are faked.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import IntegrityError, OperationalError

from app.db.retry import commit_with_unique_retry, run_with_deadlock_retry


def _operational_error(code: int) -> OperationalError:
    orig = Exception(code, "simulated")
    return OperationalError("stmt", {}, orig)


def _integrity_error(message: str) -> IntegrityError:
    return IntegrityError("stmt", {}, Exception(message))


@pytest.mark.asyncio
async def test_deadlock_retry_recovers_after_transient_1213() -> None:
    db = AsyncMock()
    calls = {"n": 0}

    async def operation() -> str:
        calls["n"] += 1
        if calls["n"] == 1:
            raise _operational_error(1213)  # deadlock on first attempt
        return "ok"

    result = await run_with_deadlock_retry(db, operation, base_delay=0)
    assert result == "ok"
    assert calls["n"] == 2
    db.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_deadlock_retry_does_not_swallow_other_operational_errors() -> None:
    db = AsyncMock()

    async def operation() -> str:
        raise _operational_error(1064)  # syntax error — not transient

    with pytest.raises(OperationalError):
        await run_with_deadlock_retry(db, operation, base_delay=0)
    db.rollback.assert_not_called()


@pytest.mark.asyncio
async def test_deadlock_retry_gives_up_after_attempts() -> None:
    db = AsyncMock()

    async def operation() -> str:
        raise _operational_error(1213)

    with pytest.raises(OperationalError):
        await run_with_deadlock_retry(db, operation, attempts=3, base_delay=0)


@pytest.mark.asyncio
async def test_unique_retry_reallocates_on_code_collision() -> None:
    db = AsyncMock()
    db.commit.side_effect = [_integrity_error("Duplicate entry for key 'experiment_code'"), None]
    build = AsyncMock(return_value="entity")

    result = await commit_with_unique_retry(
        db, build, conflict_token="experiment_code", base_delay=0
    )
    assert result == "entity"
    assert build.await_count == 2  # re-derived the code on the second attempt
    db.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_unique_retry_reraises_unrelated_constraint() -> None:
    db = AsyncMock()
    db.commit.side_effect = _integrity_error("Duplicate entry for key 'some_other_unique'")
    build = AsyncMock(return_value="entity")

    with pytest.raises(IntegrityError):
        await commit_with_unique_retry(db, build, conflict_token="experiment_code", base_delay=0)
    assert build.await_count == 1  # not retried — different constraint
