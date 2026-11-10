"""Callers with the same key take turns; a key nobody holds is forgotten."""

from __future__ import annotations

import asyncio

import pytest

from app.shared.keyed_locks import KeyedLocks

pytestmark = pytest.mark.asyncio


async def test_callers_with_one_key_take_turns_in_order_and_other_keys_do_not_wait() -> None:
    locks, journal = KeyedLocks(), []

    async def work(key: str, name: str) -> None:
        async with locks.of(key):
            journal.append(f"start {name}")
            await asyncio.sleep(0.02)
            journal.append(f"end {name}")

    await asyncio.gather(work("a", "1"), work("a", "2"), work("b", "3"))

    assert journal.index("end 1") < journal.index("start 2")
    assert journal.index("start 3") < journal.index("end 1")


async def test_a_key_nobody_holds_or_waits_for_is_dropped() -> None:
    locks = KeyedLocks()
    async with locks.of("a"):
        pass
    assert locks._locks == {}
