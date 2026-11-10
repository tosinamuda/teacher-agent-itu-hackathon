"""Store the class pack the content engine wrote, as the pipeline's is stored."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.specification import ContentSpecification, specification_ref
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactScope
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.artefacts.types.lesson_plan.infrastructure.repository import get_plan_row
from app.domains.artefacts.types.post_class_review_pack.application.grounding import (
    Grounding,
    chosen_grounding,
)
from app.domains.artefacts.types.post_class_review_pack.application.pack_inputs import (
    PackInputs,
    materialise_pack,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
)
from app.domains.artefacts.types.post_class_review_pack.application.review_record import (
    review_record,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.schemas import (
    ValidationResult,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.structural import (
    ReviewPackStructuralValidator,
)
from app.domains.artefacts.types.post_class_review_pack.domain.expert_sources import ExpertSources
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    BASE_REVIEW_PACK_POLICY,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.assembly import (
    assemble_section,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.engine_draft import (
    draft_from_part,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    DraftBlock,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.lesson_pack import (
    the_lessons_class_pack,
)
from app.shared.json_types import JsonObject


class EngineBasePackError(Exception):
    """The pack the engine wrote cannot be stored, and why."""


@dataclass(frozen=True)
class _Built:
    """The pack as the engine's parts make it, with what the structural checks found."""

    grounding: Grounding
    specification: ContentSpecification
    request: ReviewPackRequest
    sections: list[ReviewPackSection]
    checked: ValidationResult

    @property
    def faults(self) -> list[str]:
        return [c.message or c.check for c in self.checked.checks if not c.passed]


class EngineBasePack:
    def __init__(self, inputs: PackInputs) -> None:
        self._inputs = inputs

    async def faults(
        self, db: AsyncSession, plan_version_id: str, written: Mapping[str, JsonObject]
    ) -> list[str]:
        """Why the engine's parts cannot be stored as the class pack; empty when they can."""
        row = await get_plan_row(db, plan_or_version_id=plan_version_id)
        if row is None:
            return ["plan_version_not_found"]
        return (await self._built(db, row[0], plan_version_id, written)).faults

    async def _built(
        self,
        db: AsyncSession,
        plan_version: PlanVersion,
        plan_version_id: str,
        written: Mapping[str, JsonObject],
    ) -> _Built:
        grounding = await chosen_grounding(
            self._inputs.lesson_notes, db, plan_version_id, ExpertSources.LESSON_NOTE
        )
        session_plan, sources = await self._inputs.lesson_inputs(db, plan_version, grounding)
        specification = await self._inputs.specification(db)
        request = BaseReviewPackRequestBuilder().build(
            session_plan=session_plan,
            policy=BASE_REVIEW_PACK_POLICY,
            sources=sources,
            specification=specification,
        )
        sections = [
            assemble_section(
                title=draft.title,
                blocks=[
                    *([DraftBlock(block_type="explanation", text=draft.instructional_support)]
                      if draft.instructional_support.strip() else []),
                    *draft.worked_examples,
                ],
                practice=draft.practice,
                unit=unit,
            )
            for unit in request.units
            for draft in [draft_from_part(written[unit.lesson_objective_id])]
        ]  # fmt: skip
        checked = ReviewPackStructuralValidator().validate(
            policy=BASE_REVIEW_PACK_POLICY, sections=sections, request=request
        )
        return _Built(grounding, specification, request, sections, checked)

    async def store(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
        written: Mapping[str, JsonObject],
        generator: JsonObject,
    ) -> str:
        """The id of the lesson's class pack, made from what the engine wrote for each objective.

        The sections are built and checked as the pipeline's are: the same units and evidence,
        the same assembly, and the policy's structural checks. A pack that fails them is
        refused with the reasons, and nothing is stored.
        """
        row = await get_plan_row(db, plan_or_version_id=plan_version_id)
        if row is None:
            raise EngineBasePackError("plan_version_not_found")
        await self._inputs.lock_plan_version(db, plan_version_id)
        if await the_lessons_class_pack(db, plan_version_id, lock=True) is not None:
            raise EngineBasePackError("the lesson already has a class revision note")
        built = await self._built(db, row[0], plan_version_id, written)
        if built.faults:
            raise EngineBasePackError("; ".join(built.faults))
        artefact = materialise_pack(
            db=db,
            sections=built.sections,
            lesson_context=built.request.lesson_context,
            plan_version_id=plan_version_id,
            scope=ArtefactScope.CLASS_LEVEL,
            student_id=None,
            review_status=ArtefactReviewStatus.PENDING,
            artefact_refs={
                **specification_ref(built.specification),
                **built.grounding.refs(),
                "review": review_record(built.checked, built.request),
                "origin": "generated",
                "generator": generator,
            },
        )
        await db.commit()
        return str(artefact.artefact_id)
