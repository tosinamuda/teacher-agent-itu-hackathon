"""Diagnostic revision executor: load the MCQ items, revise, rewrite in place.

Bridges the generic revision thread to the objective-indexed MCQ diagnostic. The
thread's ``subject_id`` is the ``plan_version_id``; a turn revises the set of
``ExitTicketItem`` rows in place — updating kept items (by item_id), inserting new
ones, and deleting removed ones — and the service commits. There is no diagnostic
versioning. The same payload shape backs the chat seed (``_current_artefact``).
"""

from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING, Literal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.executor import RevisionExecutionOutcome
from app.domains.artefact_revision.application.highlight import format_highlight
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView

if TYPE_CHECKING:
    from app.domains.assessments.application.diagnostic_revision import DiagnosticReviser
    from app.domains.curriculum.models.exit_tickets import ExitTicketItem

logger = logging.getLogger(__name__)


async def _answered_item_ids(db: AsyncSession, item_ids: list[uuid.UUID]) -> set[uuid.UUID]:
    """Of the given items, which already have student responses (can't be deleted)."""
    if not item_ids:
        return set()
    from app.domains.assessments.models.student_item_response import StudentItemResponse

    rows = await db.execute(
        select(StudentItemResponse.item_id).where(StudentItemResponse.item_id.in_(item_ids))
    )
    return set(rows.scalars().all())


def _difficulty(value: object) -> Literal["easy", "medium", "hard"]:
    """Coerce a stored difficulty to the valid set (unknown/None -> medium)."""
    if value == "easy":
        return "easy"
    if value == "hard":
        return "hard"
    return "medium"


def _item_payload(item: ExitTicketItem) -> JsonObject:
    return {
        "item_id": str(item.id),
        "lesson_objective_id": item.lesson_objective_id or "",
        "stem": item.stem,
        "options": item.options or {},
        "correct_option": item.correct_option,
        "distractor_misconceptions": item.option_misconceptions or {},
        "difficulty": item.difficulty or "medium",
    }


async def build_diagnostic_payload(db: AsyncSession, plan_version_id: str) -> JsonObject:
    """Return the current diagnostic as the chat seed: every MCQ item (with answers)."""
    from app.domains.assessments.infrastructure.repository import AssessmentRepository

    items = await AssessmentRepository().get_exit_ticket_items(db, plan_version_id)
    return {
        "plan_version_id": plan_version_id,
        "items": [_item_payload(item) for item in items],
    }


def _objective_texts(plan_version: object | None) -> dict[str, str]:
    raw_session_plan = getattr(plan_version, "session_plan", None)
    if raw_session_plan is None:
        return {}
    session_plan = SessionPlanView.model_validate(raw_session_plan or {})
    return {
        objective.lesson_objective_id: objective.objective_text or ""
        for objective in session_plan.lesson_plan_objectives
    }


class DiagnosticRevisionExecutor:
    """Revises a lesson's MCQ diagnostic and rewrites its items in place."""

    artefact_type = "diagnostic"

    def __init__(self, reviser: DiagnosticReviser | None = None) -> None:
        if reviser is None:
            from app.domains.assessments.application.diagnostic_revision import DiagnosticReviser

            reviser = DiagnosticReviser()
        self.reviser = reviser

    async def current_artefact(
        self,
        *,
        db: AsyncSession,
        subject_id: str,
    ) -> tuple[str | None, JsonObject | None]:
        """Return ``(subject_id, assembled-payload)`` — the diagnostic is read-by-assembly."""
        payload = await build_diagnostic_payload(db, subject_id)
        return subject_id, payload

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
        from app.domains.assessments.application.diagnostic_revision import (
            DiagnosticItemForRevision,
        )
        from app.domains.assessments.infrastructure.repository import AssessmentRepository
        from app.domains.curriculum.models.exit_tickets import ExitTicketItem

        repo = AssessmentRepository()
        items = await repo.get_exit_ticket_items(db, subject_id)
        if not items:
            raise LookupError("diagnostic_not_found")
        plan_version = await repo.get_plan_version(db, subject_id)
        subtopic_id = items[0].subtopic_id

        current = [
            DiagnosticItemForRevision(
                item_id=str(item.id),
                lesson_objective_id=item.lesson_objective_id or "",
                stem=item.stem,
                options=item.options or {},
                correct_option=item.correct_option,
                distractor_misconceptions=item.option_misconceptions or {},
                difficulty=_difficulty(item.difficulty),
            )
            for item in items
        ]
        result = await self.reviser.revise(
            current_items=current,
            objectives=_objective_texts(plan_version),
            highlighted_part=format_highlight(highlight, ("item_id", "lesson_objective_id")),
            instruction=instruction,
            conversation_summary=conversation_summary,
            correlation_id=subject_id,
            thread_id=thread_id,
        )

        existing_by_id = {str(item.id): item for item in items}
        kept_ids: set[str] = set()
        for revised in result.items:
            if revised.item_id and revised.item_id in existing_by_id:
                row = existing_by_id[revised.item_id]
                row.lesson_objective_id = revised.lesson_objective_id or row.lesson_objective_id
                row.stem = revised.stem
                row.options = revised.options
                row.correct_option = revised.correct_option
                row.option_misconceptions = revised.distractor_misconceptions or None
                row.difficulty = revised.difficulty
                kept_ids.add(revised.item_id)
            else:
                db.add(
                    ExitTicketItem(
                        subtopic_id=subtopic_id,
                        plan_version_id=subject_id,
                        lesson_objective_id=revised.lesson_objective_id or None,
                        stem=revised.stem,
                        correct_option=revised.correct_option,
                        options=revised.options,
                        option_misconceptions=revised.distractor_misconceptions or None,
                        difficulty=revised.difficulty,
                    )
                )
        to_delete = [row for item_id, row in existing_by_id.items() if item_id not in kept_ids]
        # A dropped item that students already answered is kept (deleting it would
        # break referential integrity + lose that learner-state evidence).
        answered = await _answered_item_ids(db, [row.id for row in to_delete])
        for row in to_delete:
            if row.id in answered:
                logger.info("keeping diagnostic item %s — it already has student responses", row.id)
                continue
            await db.delete(row)

        # Flush so new rows get ids, then rebuild the payload from the final set.
        await db.flush()
        payload = await build_diagnostic_payload(db, subject_id)
        return RevisionExecutionOutcome(
            base_version_id=subject_id,
            result_version_id=subject_id,
            session_plan=payload,
            change_summary=result.change_summary,
            validation_passed=True,
        )
