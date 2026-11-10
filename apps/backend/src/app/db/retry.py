"""Retry contended writes so concurrency surfaces as convergence, not a 500.

Two transient write-conflict classes show up the moment more than one request
mutates the database at once:

* **Unique-code collisions** — a code derived from ``MAX(existing) + 1`` is a
  read-then-write race: two callers read the same max, build the same code, and
  one loses on the unique index (``IntegrityError``). Re-deriving the code against
  the now-committed max and retrying makes the loser take the next number.
* **InnoDB lock conflicts** — concurrent statements can deadlock (MySQL ``1213``)
  or hit a lock-wait timeout (``1205``). Both are transient; the documented remedy
  is to roll back and retry the transaction.

Both helpers own the rollback so the caller's session is clean on each attempt,
and both are bounded so a genuine (non-transient) failure still raises.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

# InnoDB transient lock errors: 1213 = deadlock, 1205 = lock wait timeout.
_TRANSIENT_LOCK_CODES = frozenset({1213, 1205})


def _mysql_errno(exc: BaseException) -> int | None:
    orig = getattr(exc, "orig", None)
    args = getattr(orig, "args", None)
    if args:
        code = args[0]
        if isinstance(code, int):
            return code
    return None


async def run_with_deadlock_retry(
    db: AsyncSession,
    operation: Callable[[], Awaitable[T]],
    *,
    attempts: int = 5,
    base_delay: float = 0.05,
) -> T:
    """Run a self-committing ``operation``, retrying on transient InnoDB lock errors.

    ``operation`` must perform its own ``commit``. On deadlock / lock-wait timeout
    the session is rolled back and the operation re-run after a short exponential
    backoff. Any other error (or the final attempt) propagates unchanged.
    """
    for attempt in range(1, attempts + 1):
        try:
            return await operation()
        except OperationalError as exc:
            if attempt >= attempts or _mysql_errno(exc) not in _TRANSIENT_LOCK_CODES:
                raise
            await db.rollback()
            await asyncio.sleep(base_delay * (2 ** (attempt - 1)))
    raise AssertionError("unreachable: loop exhausts via return or raise")


async def commit_with_unique_retry(
    db: AsyncSession,
    build: Callable[[], Awaitable[T]],
    *,
    conflict_token: str,
    attempts: int = 12,
    base_delay: float = 0.02,
) -> T:
    """Allocate-and-insert an entity whose unique code races under concurrency.

    ``build`` (re)derives the entity — allocating its sequential code from the
    current max — and adds it to ``db``; this helper commits. If the commit loses
    a race on the named unique key (``conflict_token`` appears in the driver error,
    e.g. ``"experiment_code"``), it rolls back and calls ``build`` again, which
    re-derives the code against the now-higher max. Collisions on a *different*
    constraint are real anomalies and propagate immediately.
    """
    for attempt in range(1, attempts + 1):
        entity = await build()
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            is_code_conflict = conflict_token in str(getattr(exc, "orig", exc))
            if attempt >= attempts or not is_code_conflict:
                raise
            await asyncio.sleep(base_delay * attempt)
            continue
        return entity
    raise AssertionError("unreachable: loop exhausts via return or raise")
