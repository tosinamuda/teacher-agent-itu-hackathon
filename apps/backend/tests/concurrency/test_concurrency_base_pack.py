"""Regression: the base-pack re-check must read CURRENT data, not the snapshot.

``_ensure_base`` / ``ensure_base_artefact`` do find → lock plan_version → re-check →
generate. The re-check used to be a plain (non-locking) read, so under MySQL
REPEATABLE READ the loser — who waited on the plan-version lock — still saw its
PRE-lock snapshot and missed the base the winner had just committed, then generated
a DUPLICATE C3 base. The fix makes the re-check a locking (current) read. Same class
as the rater-cap REPEATABLE-READ bug.

This pins the mechanism the fix relies on: a locking ``the_lessons_class_pack`` sees a
base committed by another session after this session's snapshot formed, while a
plain read does not.
"""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import text

from app.domains.artefacts.core.domain.types import ArtefactScope, ArtefactType
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.post_class_review_pack.infrastructure.lesson_pack import (
    the_lessons_class_pack,
)

pytestmark = pytest.mark.asyncio

_PLAN_VERSION = "LPV-BASELOCK"


def _base_artefact() -> Artefact:
    return Artefact(
        artefact_id=f"AT-{uuid.uuid4().hex[:8]}",
        artefact_type=ArtefactType.POST_CLASS_REVIEW_PACK.value,
        scope=ArtefactScope.CLASS_LEVEL.value,
        plan_version_id=_PLAN_VERSION,
        manifest={},
    )


async def test_base_recheck_reads_current_not_snapshot(session_factory) -> None:
    async with session_factory() as session_a:
        # Establish session A's REPEATABLE READ snapshot with the initial find (none).
        first = await the_lessons_class_pack(session_a, _PLAN_VERSION)
        assert first is None

        # A rival session commits the base AFTER A's snapshot formed.
        async with session_factory() as session_b:
            await session_b.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            session_b.add(_base_artefact())
            await session_b.commit()

        # A plain (snapshot) re-check still misses it — what the lock alone left broken.
        stale = await the_lessons_class_pack(session_a, _PLAN_VERSION)
        assert stale is None

        # A LOCKING re-check sees the committed base — the fix (so no duplicate is generated).
        current = await the_lessons_class_pack(session_a, _PLAN_VERSION, lock=True)
        assert current is not None
