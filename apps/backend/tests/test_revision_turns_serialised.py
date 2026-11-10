"""Turns on one thread run one at a time, so each reads the turns before it and numbers the next."""

from __future__ import annotations

import asyncio

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.executor import RevisionExecutionOutcome
from app.domains.artefact_revision.application.service import ArtefactRevisionService
from app.shared.json_types import JsonObject

pytestmark = pytest.mark.asyncio


class _Slow:
    artefact_type = "slow"

    def __init__(self) -> None:
        self.journal: list[str] = []

    async def revise(
        self,
        *,
        db: AsyncSession,
        subject_id: str,
        thread_id: str,
        instruction: str,
        highlight: JsonObject | None,
        conversation_summary: str,
    ) -> RevisionExecutionOutcome:
        self.journal.append(f"start {instruction}")
        await asyncio.sleep(0.05)
        self.journal.append(f"end {instruction}")
        return RevisionExecutionOutcome(subject_id, subject_id, {}, instruction, True)

    async def current_artefact(
        self, *, db: AsyncSession, subject_id: str
    ) -> tuple[str | None, JsonObject | None]:
        return subject_id, {}


async def test_two_turns_at_once_on_a_thread_run_in_turn_and_are_numbered_in_order(
    db: AsyncSession,
) -> None:
    executor = _Slow()
    service = ArtefactRevisionService((executor,))
    thread = await service.get_or_create_thread(
        db=db, artefact_type="slow", subject_id="C-1", created_by="T"
    )

    turns = await asyncio.gather(
        *(
            service.submit_turn(
                db=db, thread_id=thread.revision_thread_id, instruction=name, highlight=None
            )
            for name in ("first", "second")
        )
    )

    assert executor.journal == ["start first", "end first", "start second", "end second"]
    assert [turn.turn_number for turn, _ in turns] == [1, 2]
