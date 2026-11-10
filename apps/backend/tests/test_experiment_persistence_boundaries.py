"""Transaction-lifetime contracts for experiment workflow infrastructure.

The store never commits by itself. That is what makes H1's deliberate
mid-workflow commit unambiguous: if nobody committed, nothing was written.
"""

from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.experiments.infrastructure.sqlalchemy_experiment_store import (
    open_experiment_store,
)
from app.domains.experiments.review_pack_study.condition_runs.records import CompletedConditionRun
from app.domains.experiments.review_pack_study.condition_runs.store import record_condition_runs

pytestmark = pytest.mark.architecture


class _FakeSession(AsyncSession):
    def __init__(self) -> None:
        self.commits = 0
        self.rollbacks = 0
        self.closes = 0

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        self.rollbacks += 1

    async def close(self) -> None:
        self.closes += 1

    async def __aenter__(self) -> _FakeSession:
        return self

    async def __aexit__(self, *_exc: object) -> None:
        await self.close()


class _SessionFactory:
    def __init__(self) -> None:
        self.created: list[_FakeSession] = []

    def __call__(self) -> AsyncSession:
        session = _FakeSession()
        self.created.append(session)
        return session


@pytest.mark.asyncio
async def test_the_store_opens_only_when_entered() -> None:
    sessions = _SessionFactory()
    store = open_experiment_store(sessions)

    assert sessions.created == []

    async with store as unit_of_work:
        assert len(sessions.created) == 1
        await unit_of_work.commit()

    assert sessions.created[0].commits == 1
    assert sessions.created[0].closes == 1


@pytest.mark.asyncio
async def test_the_store_never_commits_on_its_own() -> None:
    sessions = _SessionFactory()

    async with open_experiment_store(sessions):
        pass

    assert sessions.created[0].commits == 0
    assert sessions.created[0].closes == 1


@pytest.mark.asyncio
async def test_an_exceptional_batch_closes_without_committing() -> None:
    sessions = _SessionFactory()

    with pytest.raises(RuntimeError, match="write failed"):
        async with open_experiment_store(sessions):
            raise RuntimeError("write failed")

    assert sessions.created[0].commits == 0
    assert sessions.created[0].rollbacks == 1
    assert sessions.created[0].closes == 1


@pytest.mark.asyncio
async def test_recording_a_batch_commits_exactly_once() -> None:
    """The whole condition grid is one unit of work, or none of it."""
    recorded: list[tuple[int, int]] = []

    class _Runs:
        async def record(self, *, completed: list[CompletedConditionRun], failed: list) -> None:
            recorded.append((len(completed), len(failed)))

    class _Store:
        def __init__(self) -> None:
            self.condition_runs = _Runs()
            self.commits = 0

        async def __aenter__(self) -> _Store:
            return self

        async def __aexit__(self, *_exc: object) -> None:
            return None

        async def commit(self) -> None:
            self.commits += 1

        async def rollback(self) -> None:
            raise AssertionError("nothing here should roll back")

    store = _Store()
    await record_condition_runs(lambda: store, completed=[], failed=[])

    assert recorded == [(0, 0)]
    assert store.commits == 1
