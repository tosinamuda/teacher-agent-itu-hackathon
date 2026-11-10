"""Save a finished class-test draft as the lesson's class test: the rows grading reads."""

from __future__ import annotations

import json

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.retry import run_with_deadlock_retry
from app.domains.artefacts.core.domain.specification import (
    ContentSpecification,
    specification_ref,
)
from app.domains.assessments.application.diagnostic_service import (
    SUBTOPIC_SQL,
    ClassTestMaterialRecords,
)
from app.domains.assessments.application.exit_ticket_payload import exit_ticket_payload
from app.domains.content_engine.application.held_checks import held_checks_record
from app.domains.content_engine.domain.draft import Draft, DraftError
from app.domains.content_engine.infrastructure.class_test_items import item_of, questions_of
from app.domains.content_engine.infrastructure.class_test_reading import SECOND_READING_TOOL
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView

HELD_CHECKS = ("question_shape", "distinct_stems", "scale_reached")
SECOND_READING = "second_reading"


def _held(spec: ContentSpecification) -> tuple[str, ...]:
    """The reviews the draft held: the app's own, and a second reading the plugin lists."""
    listed = any(SECOND_READING_TOOL in ref.checks for ref in spec.mcp)
    return (*HELD_CHECKS, SECOND_READING) if listed else HELD_CHECKS


class ClassTestDestination:
    """The questions are stored as the pipeline stores them, so grading reads them unchanged."""

    def __init__(self, materials: ClassTestMaterialRecords) -> None:
        self._materials = materials

    async def issues(self, db: AsyncSession, draft: Draft) -> list[str]:
        """Nothing: the plugin's check tools read the questions, a second reader among them."""
        return []

    def preview(self, draft: Draft) -> JsonObject:
        return {"content_type": draft.type, "sections": draft.sections()}

    async def save(
        self, db: AsyncSession, draft: Draft, spec: ContentSpecification, generator: JsonObject
    ) -> str:
        plan_version_id = draft.plan_version_id
        if plan_version_id is None:
            raise DraftError("a class test is made from a plan version")
        if draft.saved_as is not None:
            raise DraftError("a class test is revised in its chat, not drafted again")
        row = (await db.execute(SUBTOPIC_SQL, {"version_id": plan_version_id})).first()
        if row is None or not row[0]:
            raise DraftError("the plan version has no subtopic")
        raw = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        plan = SessionPlanView.model_validate(raw)
        payloads = await self._payloads(db, draft, plan_version_id, str(row[0]), plan)
        refs: JsonObject = {
            **specification_ref(spec),
            "origin": "generated",
            "generator": generator,
            "engine": {"draft_id": draft.draft_id},
            "review": held_checks_record(_held(spec)),
        }

        async def persist() -> str:
            await db.execute(
                delete(ExitTicketItem).where(ExitTicketItem.plan_version_id == plan_version_id)
            )
            db.add_all([ExitTicketItem(**payload) for payload in payloads])
            record = await self._materials.ensure(
                db, plan_version_id=plan_version_id, source="generated"
            )
            record.artefact_refs = {**(record.artefact_refs or {}), **refs}
            await db.commit()
            return str(record.artefact_id)

        return await run_with_deadlock_retry(db, persist)

    async def _payloads(
        self,
        db: AsyncSession,
        draft: Draft,
        plan_version_id: str,
        subtopic_id: str,
        plan: SessionPlanView,
    ) -> list[dict[str, object]]:
        payloads: list[dict[str, object]] = []
        for unit, part in draft.written():
            for question in questions_of(part):
                item = item_of(question)
                payloads.append(
                    exit_ticket_payload(
                        item,
                        subtopic_id=subtopic_id,
                        plan_version_id=plan_version_id,
                        lesson_objective_id=unit.unit_id,
                    )
                )
        return payloads
