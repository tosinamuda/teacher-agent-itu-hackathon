"""What a class or learner pack is built from, and how a built pack is stored."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.application.specifications import ContentSpecifications
from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.specifications.seed import seed_specification
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.artefacts.types.post_class_review_pack.application.grounding import (
    ApprovedLessonNotes,
    Grounding,
)
from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
    sections_to_review_pack_manifest,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.lesson_sources import (
    resolve_lesson_sources,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    LessonContextForGeneration,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.expert_content.application.excerpt_resolver import SqlAlchemyExcerpts
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView
from app.shared.time import utc_now


class PackInputs:
    """The lesson's inputs to a pack: its plan and sources, the spec, and the plan's lock."""

    def __init__(
        self, lesson_notes: ApprovedLessonNotes, specifications: ContentSpecifications | None
    ) -> None:
        self.lesson_notes = lesson_notes
        self._specifications = specifications

    async def lesson_inputs(
        self, db: AsyncSession, plan_version: PlanVersion, grounding: Grounding
    ) -> tuple[SessionPlanView, LessonSources]:
        """The plan with its lesson note, and the sources, as this grounding reads them."""
        session_plan = grounding.plan(plan_version.session_plan or {})
        references = await resolve_lesson_sources(SqlAlchemyExcerpts(db), session_plan)
        return session_plan, grounding.sources(references)

    async def specification(self, db: AsyncSession) -> ContentSpecification:
        """The pack's current stored specification; the seed revision when none is wired."""
        if self._specifications is None:
            return seed_specification(ArtefactType.POST_CLASS_REVIEW_PACK.value)
        return await self._specifications.current(db, ArtefactType.POST_CLASS_REVIEW_PACK.value)

    async def lock_plan_version(self, db: AsyncSession, plan_version_id: str) -> None:
        """Row-lock the plan version to serialize class-pack creation.

        Two requests to review a lesson that has no class pack would otherwise each find
        none and each generate one. The lock makes the winner generate + commit while the
        rest wait, then find it.
        """
        await db.execute(
            select(PlanVersion.version_id)
            .where(PlanVersion.version_id == plan_version_id)
            .with_for_update()
        )


def base_pack_id(plan_version_id: str) -> str:
    """The id a learner's request names the class pack it adapts by."""
    return f"c3-base:{plan_version_id}"


def materialise_pack(
    *,
    db: AsyncSession,
    sections: list[ReviewPackSection],
    lesson_context: LessonContextForGeneration,
    plan_version_id: str,
    scope: ArtefactScope,
    student_id: str | None,
    review_status: ArtefactReviewStatus,
    artefact_refs: JsonObject | None = None,
    personalisation_bands: dict[str, str] | None = None,
) -> Artefact:
    artefact_id = new_public_id(PublicIdPrefix.ARTEFACT)
    manifest = sections_to_review_pack_manifest(
        sections=sections,
        artefact_id=artefact_id,
        plan_version_id=plan_version_id,
        scope=scope,
        lesson_context=lesson_context,
        created_at=utc_now(),
        student_id=student_id,
        personalisation_bands=personalisation_bands,
    )
    artefact = Artefact(
        artefact_id=artefact_id,
        artefact_type=ArtefactType.POST_CLASS_REVIEW_PACK.value,
        scope=scope.value,
        plan_version_id=plan_version_id,
        student_id=student_id,
        manifest=manifest,
        artefact_refs=artefact_refs,
        review_status=review_status,
    )
    db.add(artefact)
    return artefact
