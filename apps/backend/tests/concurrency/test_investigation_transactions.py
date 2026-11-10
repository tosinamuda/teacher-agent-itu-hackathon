"""MySQL concurrency contract for investigation code allocation."""

from __future__ import annotations

import pytest
from sqlalchemy import select

from app.domains.experiments.application.investigation_service import create_investigation
from app.domains.experiments.infrastructure.models import Investigation
from app.domains.experiments.infrastructure.sqlalchemy_experiment_store import (
    SqlAlchemyExperimentStore,
)

pytestmark = pytest.mark.asyncio


async def test_concurrent_investigation_creation_retries_to_unique_codes(
    session_factory,
    run_race,
) -> None:
    async def create(session, index):
        investigation = await create_investigation(
            SqlAlchemyExperimentStore(session),
            title=f"Concurrent study {index}",
        )
        return investigation.investigation_code

    outcome = await run_race(create, lambda _error: False, n=4)

    assert outcome.others == []
    assert len(outcome.wins) == 4
    assert len(set(outcome.wins)) == 4
    async with session_factory() as check:
        codes = set((await check.execute(select(Investigation.investigation_code))).scalars().all())
    assert codes == set(outcome.wins)
