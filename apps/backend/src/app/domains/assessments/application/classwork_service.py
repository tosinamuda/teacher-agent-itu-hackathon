"""Manually entered classwork → exit-ticket items (FD-02).

The teacher hand-enters the lesson's real classwork; it persists as the same
``ExitTicketItem`` rows the LLM diagnostic writes (so scoring consumes them
unchanged) and a coverage report flags objectives with no items. Entry is
edit-in-place (re-saving replaces the set) and locks once the assessment is
released to students.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Sequence

from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.retry import run_with_deadlock_retry
from app.domains.assessments.application.manual_entry import (
    build_classwork_item_payloads,
    classwork_item_issues,
)
from app.domains.assessments.application.misconception_deriver import MisconceptionDeriver
from app.domains.assessments.application.service import AssessmentApplicationError
from app.domains.assessments.classwork_schemas import (
    ClassworkCoverageResponse,
    ClassworkObjectiveCoverage,
    DerivedItemMisconceptions,
    DeriveMisconceptionsItem,
    DeriveMisconceptionsResponse,
    KnowledgeComponentOption,
    ManualClassworkContextResponse,
    ManualClassworkExistingItem,
    ManualClassworkItem,
    ManualClassworkObjective,
)
from app.domains.assessments.infrastructure.repository import (
    AssessmentRepository,
    ClassTestMaterials,
)
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.shared.session_plan_view import SessionPlanView

logger = logging.getLogger(__name__)


class ClassworkApplicationService:
    def __init__(self, repository: AssessmentRepository | None = None) -> None:
        self.repository = repository or AssessmentRepository()

    async def classwork_context(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
    ) -> ManualClassworkContextResponse:
        """Form prerequisites for the entry form.

        Returns the frozen plan's objectives, the subtopic's knowledge components, and
        any items already entered (so the form edits in place rather than starting blank).
        """
        plan_version = await self.repository.get_plan_version(db, plan_version_id)
        if plan_version is None:
            raise AssessmentApplicationError(404, "plan_version_not_found")
        session_plan = SessionPlanView.model_validate(plan_version.session_plan or {})
        subtopic_id = await self.repository.resolve_subtopic_id(db, plan_version_id)
        kcs = (
            await self.repository.list_knowledge_components(db, subtopic_id) if subtopic_id else []
        )
        items = await self.repository.get_exit_ticket_items(db, plan_version_id)
        return ManualClassworkContextResponse(
            plan_version_id=plan_version_id,
            subject=session_plan.subject,
            topic=session_plan.topic,
            subtopic=session_plan.subtopic,
            objectives=[
                ManualClassworkObjective(
                    lesson_objective_id=objective.lesson_objective_id,
                    objective_text=objective.objective_text,
                    curriculum_objective_id=objective.curriculum_objective_id,
                )
                for objective in session_plan.lesson_plan_objectives
                if objective.lesson_objective_id
            ],
            knowledge_components=[
                KnowledgeComponentOption(
                    id=str(kc.id), kc_code=kc.kc_code, description=kc.description
                )
                for kc in kcs
            ],
            items=[_existing_item(item) for item in items],
            released=await self.repository.is_assessment_released(db, plan_version_id),
        )

    async def create_manual_classwork(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
        items: Sequence[ManualClassworkItem],
    ) -> ClassworkCoverageResponse:
        """Replace the plan's classwork with the entered items; return the coverage report.

        Refuses once the assessment is released (frozen) or any student has answered —
        re-entry must never destroy released work or evidence a student already gave.
        """
        plan_version = await self.repository.get_plan_version(db, plan_version_id)
        if plan_version is None:
            raise AssessmentApplicationError(404, "plan_version_not_found")
        if await self.repository.is_assessment_released(db, plan_version_id):
            raise AssessmentApplicationError(409, "assessment_released")
        if await self.repository.has_student_responses(db, plan_version_id):
            raise AssessmentApplicationError(409, "assessment_has_responses")
        subtopic_id = await self.repository.resolve_subtopic_id(db, plan_version_id)
        if not subtopic_id:
            raise AssessmentApplicationError(409, "subtopic_not_resolved")

        session_plan = SessionPlanView.model_validate(plan_version.session_plan or {})
        valid_objective_ids = {
            objective.lesson_objective_id
            for objective in session_plan.lesson_plan_objectives
            if objective.lesson_objective_id
        }
        valid_kc_ids = {
            str(kc.id) for kc in await self.repository.list_knowledge_components(db, subtopic_id)
        }
        issues = classwork_item_issues(items, valid_objective_ids=valid_objective_ids)
        for index, item in enumerate(items, start=1):
            if item.knowledge_component_id and item.knowledge_component_id not in valid_kc_ids:
                issues.append(f"Item {index}: that knowledge component is not part of this lesson.")
        if issues:
            raise AssessmentApplicationError(422, "; ".join(issues))

        payloads = build_classwork_item_payloads(
            items, subtopic_id=subtopic_id, plan_version_id=plan_version_id
        )

        async def _persist() -> None:
            await db.execute(
                delete(ExitTicketItem).where(ExitTicketItem.plan_version_id == plan_version_id)
            )
            db.add_all([ExitTicketItem(**payload) for payload in payloads])
            await ClassTestMaterials().ensure(
                db, plan_version_id=plan_version_id, source="manual_classwork"
            )
            await db.commit()

        try:
            await run_with_deadlock_retry(db, _persist)
        except IntegrityError as error:
            # Race: a student answered between the guard above and the DELETE, so the
            # RESTRICT FK blocks it (1451). The student's evidence + prior items survive.
            await db.rollback()
            raise AssessmentApplicationError(409, "assessment_has_responses") from error

        return await self.compute_classwork_coverage(db=db, plan_version_id=plan_version_id)

    async def compute_classwork_coverage(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
    ) -> ClassworkCoverageResponse:
        """Items-per-objective over the FROZEN plan's objective list; zero-item ones flagged.

        Driven from the plan's objectives (not the items), so an objective with no
        items still appears as a flagged row — a missing objective means no diagnostic
        signal for it.
        """
        plan_version = await self.repository.get_plan_version(db, plan_version_id)
        if plan_version is None:
            raise AssessmentApplicationError(404, "plan_version_not_found")
        session_plan = SessionPlanView.model_validate(plan_version.session_plan or {})
        counts = await self.repository.item_counts_by_objective(db, plan_version_id)

        objectives: list[ClassworkObjectiveCoverage] = []
        without_items: list[str] = []
        for objective in session_plan.lesson_plan_objectives:
            if not objective.lesson_objective_id:
                continue
            count = counts.get(objective.lesson_objective_id, 0)
            objectives.append(
                ClassworkObjectiveCoverage(
                    lesson_objective_id=objective.lesson_objective_id,
                    objective_text=objective.objective_text,
                    item_count=count,
                    has_items=count > 0,
                )
            )
            if count == 0:
                without_items.append(objective.lesson_objective_id)

        return ClassworkCoverageResponse(
            plan_version_id=plan_version_id,
            total_items=sum(counts.values()),
            objectives=objectives,
            objectives_without_items=without_items,
        )

    async def derive_misconceptions(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
        items: Sequence[DeriveMisconceptionsItem],
    ) -> DeriveMisconceptionsResponse:
        """Suggest a snake_case misconception code for each wrong option (FD-03).

        Per-item LLM derivation run concurrently, with the lesson objective as context.
        Suggestions only — the teacher reviews/edits them before they persist via the
        normal classwork save. A per-item failure yields an empty map, never an error.
        """
        objective_text = await self._objective_text_map(db, plan_version_id)
        deriver = MisconceptionDeriver()

        async def _one(item: DeriveMisconceptionsItem) -> DerivedItemMisconceptions:
            try:
                derived = await deriver.derive(
                    stem=item.stem,
                    options=item.options,
                    correct_option=item.correct_option,
                    objective_text=objective_text.get(item.lesson_objective_id or "", ""),
                )
            except Exception:  # noqa: BLE001 - a derivation failure must not fail the batch
                logger.warning("misconception derivation failed for an item", exc_info=True)
                derived = {}
            return DerivedItemMisconceptions(option_misconceptions=derived)

        results = await asyncio.gather(*[_one(item) for item in items])
        return DeriveMisconceptionsResponse(items=list(results))

    async def _objective_text_map(self, db: AsyncSession, plan_version_id: str) -> dict[str, str]:
        plan_version = await self.repository.get_plan_version(db, plan_version_id)
        if plan_version is None:
            return {}
        session_plan = SessionPlanView.model_validate(plan_version.session_plan or {})
        return {
            objective.lesson_objective_id: objective.objective_text or ""
            for objective in session_plan.lesson_plan_objectives
            if objective.lesson_objective_id
        }


def _existing_item(item: ExitTicketItem) -> ManualClassworkExistingItem:
    return ManualClassworkExistingItem(
        item_id=str(item.id),
        lesson_objective_id=item.lesson_objective_id,
        stem=item.stem,
        options=item.options,
        correct_option=item.correct_option,
        knowledge_component_id=(
            str(item.knowledge_component_id) if item.knowledge_component_id else None
        ),
        difficulty=item.difficulty,
        option_misconceptions=item.option_misconceptions,
    )
