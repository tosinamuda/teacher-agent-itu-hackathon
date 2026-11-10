"""A second reader answers each drafted class-test question; the writer hears of a doubtful key.

It is the model call behind the ``class_test_second_reading`` tool of the app's MCP server.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import Callable, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.assessments.application.diagnostic_generator import DiagnosticMCQItem
from app.domains.assessments.application.diagnostic_service import (
    SUBTOPIC_SQL,
    ApprovedLessonNotes,
)
from app.domains.assessments.application.item_reader import (
    ItemReader,
    ItemToRead,
    reads_as_keyed,
)
from app.domains.content_engine.domain.draft import Draft
from app.domains.content_engine.infrastructure.class_test_items import item_of, questions_of
from app.shared.json_types import JsonValue
from app.shared.session_plan_view import SessionPlanView

#: What the reader said of a question, so a question is read once however often the draft is
#: checked. It is bounded: a long-running app holds the latest reads.
_READ: dict[tuple[object, ...], frozenset[str]] = {}
_LIMIT = 4000
#: The name of the check tool a plugin lists to have a class test read a second time.
SECOND_READING_TOOL = "class_test_second_reading"


class Question:
    """One drafted question, and where it sits in the draft."""

    def __init__(self, where: str, objective_id: str, item: DiagnosticMCQItem) -> None:
        self.where = where
        self.objective_id = objective_id
        self.item = item

    def key(self, plan_version_id: str) -> tuple[object, ...]:
        item = self.item
        return (plan_version_id, self.objective_id, item.stem, tuple(sorted(item.options.items())))


async def plan_of(db: AsyncSession, plan_version_id: str) -> SessionPlanView | None:
    """The plan version's plan as class-test items are written and read against it."""
    row = (await db.execute(SUBTOPIC_SQL, {"version_id": plan_version_id})).first()
    if row is None:
        return None
    raw = json.loads(row[1]) if isinstance(row[1], str) else row[1]
    return SessionPlanView.model_validate(raw)


class SecondReading:
    """Reads the questions of a stored class-test draft with a reader made on first use."""

    def __init__(self, reader: Callable[[], ItemReader], lesson_notes: ApprovedLessonNotes) -> None:
        self._make_reader = reader
        self._reader: ItemReader | None = None
        self._lesson_notes = lesson_notes

    async def faults(self, db: AsyncSession, draft: Draft) -> list[str]:
        """What a second reader finds against the keys of the draft's questions."""
        if draft.plan_version_id is None:
            return []
        readable = [
            Question(f"{unit.unit_id} question {number}", unit.unit_id, item_of(question))
            for unit, part in draft.written()
            for number, question in enumerate(questions_of(part), start=1)
        ]
        if not readable:
            return []
        return await self.problems(db, draft.plan_version_id, readable)

    async def problems(
        self, db: AsyncSession, plan_version_id: str, questions: Sequence[Question]
    ) -> list[str]:
        """What each question's second reading says against its key; empty where it agrees."""
        unread = [q for q in questions if q.key(plan_version_id) not in _READ]
        if unread:
            await self._read(db, plan_version_id, unread)
        found: list[str] = []
        for question in questions:
            read = _READ.get(question.key(plan_version_id))
            if read is not None and not reads_as_keyed(set(read), question.item.correct_option):
                said = ", ".join(sorted(read)) or "no option"
                found.append(
                    f"{question.where}: a second reader found {said} right, not only "
                    f"{question.item.correct_option}: rewrite the question so only the key is right"
                )
        return found

    async def _read(
        self, db: AsyncSession, plan_version_id: str, questions: Sequence[Question]
    ) -> None:
        plan = await plan_of(db, plan_version_id)
        if plan is None:
            return
        taught = await self._taught(db, plan_version_id, plan)
        objectives = {
            o.lesson_objective_id: o.objective_text or "" for o in plan.lesson_plan_objectives
        }
        self._reader = self._reader or self._make_reader()
        reader = self._reader
        reads = await asyncio.gather(
            *(
                reader.correct_options(
                    ItemToRead(
                        lesson=taught,
                        objective_text=objectives.get(q.objective_id, ""),
                        subject=plan.subject or "Mathematics",
                        grade=plan.grade or "JSS1",
                        stem=q.item.stem,
                        options=q.item.options,
                    )
                )
                for q in questions
            )
        )
        if len(_READ) + len(reads) > _LIMIT:
            _READ.clear()
        for question, read in zip(questions, reads, strict=True):
            _READ[question.key(plan_version_id)] = frozenset(read)

    async def _taught(self, db: AsyncSession, plan_version_id: str, plan: SessionPlanView) -> str:
        note = await self._lesson_notes.text(db, plan_version_id)
        if note:
            return note
        steps: list[JsonValue] = [
            step.model_dump(mode="json", exclude_none=True) for step in plan.steps
        ]
        return json.dumps(steps, ensure_ascii=False)
