"""Put a teacher-revised pack through the checks and bounded repair its generation ran.

The request is rebuilt from what the stored pack records: its plan version, its grounding,
the pipeline that wrote it and, for a learner's pack, the approved class pack it adapts and
the learner's evidence. A pack whose inputs cannot be found is refused, never passed.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.core.domain.types import ArtefactScope
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.infrastructure.repository import get_plan_row
from app.domains.artefacts.types.post_class_review_pack.application.errors import (
    MissingPackInputError,
)
from app.domains.artefacts.types.post_class_review_pack.application.grounding import (
    written_grounding,
)
from app.domains.artefacts.types.post_class_review_pack.application.learner_inputs import (
    learner_inputs,
)
from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
    review_pack_manifest_to_sections,
)
from app.domains.artefacts.types.post_class_review_pack.application.pack_inputs import (
    PackInputs,
    base_pack_id,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.personalised.builder import (  # noqa: E501
    PersonalisedReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.application.review_record import (
    review_record,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.decisions import (
    issue_messages,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.finalise_pack import (
    FinaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.schemas import (
    ValidationResult,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    BASE_REVIEW_PACK_POLICY,
    PERSONALISED_REVIEW_PACK_POLICY,
    ReviewPackGenerationPolicy,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    ReviewPackPipeline,
    pipeline_that_wrote,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.lesson_pack import (
    the_lessons_approved_class_pack,
)
from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.domains.learner_state.application.service import LearnerStateService
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView


@dataclass(frozen=True)
class CheckedPack:
    """The sections after the last repair round, and the checks' verdict on them."""

    sections: list[ReviewPackSection]
    validation: ValidationResult
    #: Section ids the repair rounds wrote again from scratch.
    regenerated: tuple[str, ...] = ()
    #: The checks and the passages, as the pack records them beside its sections.
    review: JsonObject | None = None

    @property
    def regenerated_titles(self) -> list[str]:
        """The titles of the sections written again, as the teacher reads them."""
        titles = {section.section_id: section.title for section in self.sections}
        return [titles.get(section_id, section_id) for section_id in self.regenerated]

    @property
    def unresolved(self) -> list[str]:
        """The findings still standing, as the repair step was told them."""
        return issue_messages(self.validation)


@dataclass(frozen=True)
class PackChecks:
    """The checks one stored pack was generated under, ready for its revised sections."""

    policy: ReviewPackGenerationPolicy
    request: ReviewPackRequest
    base_sections: list[ReviewPackSection] | None
    finalise: FinaliseReviewPack

    async def check(self, sections: list[ReviewPackSection]) -> CheckedPack:
        """Validate, repair within the policy's retry budget, and report what remains."""
        result = await self.finalise.finalise(
            policy=self.policy,
            request=self.request,
            sections=sections,
            base_sections=self.base_sections,
        )
        if result.validation is None:
            raise RuntimeError("revision_policy_runs_no_checks")
        return CheckedPack(
            sections=result.sections,
            validation=result.validation,
            regenerated=tuple(result.regenerated),
            review=review_record(result.validation, self.request),
        )


@dataclass(frozen=True)
class _Lesson:
    pack: Artefact
    session_plan: SessionPlanView
    sources: LessonSources
    specification: ContentSpecification


def _stored_sections(pack: Artefact) -> list[ReviewPackSection]:
    return review_pack_manifest_to_sections(PostClassReviewPack.model_validate(pack.manifest))


class RevisedPackChecks:
    """Rebuild a stored pack's generation request and bind the checks it ran."""

    def __init__(
        self,
        *,
        inputs: PackInputs,
        finalise_for: Callable[[ReviewPackPipeline], FinaliseReviewPack],
        class_requests: BaseReviewPackRequestBuilder,
        learner_requests: PersonalisedReviewPackRequestBuilder | None = None,
        learner_states: LearnerStateService | None = None,
    ) -> None:
        self._inputs = inputs
        self._finalise_for = finalise_for
        self._class_requests = class_requests
        self._learner_requests = learner_requests or PersonalisedReviewPackRequestBuilder()
        self._learner_states = learner_states or LearnerStateService()

    async def for_pack(self, db: AsyncSession, pack: Artefact) -> PackChecks:
        """The checks for ``pack``; raises ``MissingPackInputError`` when an input is gone."""
        lesson = await self._lesson(db, pack)
        finalise = self._finalise_for(pipeline_that_wrote(pack.artefact_refs))
        if pack.scope == ArtefactScope.LEARNER_LEVEL.value:
            return await self._learner_checks(db, lesson, finalise)
        request = self._class_requests.build(
            session_plan=lesson.session_plan,
            policy=BASE_REVIEW_PACK_POLICY,
            sources=lesson.sources,
            specification=lesson.specification,
        )
        return PackChecks(BASE_REVIEW_PACK_POLICY, request, None, finalise)

    async def _lesson(self, db: AsyncSession, pack: Artefact) -> _Lesson:
        row = await get_plan_row(db, plan_or_version_id=pack.plan_version_id)
        if row is None:
            raise MissingPackInputError("plan_version_not_found")
        grounding = await written_grounding(
            self._inputs.lesson_notes, db, pack.artefact_refs, pack.plan_version_id
        )
        session_plan, sources = await self._inputs.lesson_inputs(db, row[0], grounding)
        specification = await self._inputs.specification(db)
        return _Lesson(pack, session_plan, sources, specification)

    async def _learner_checks(
        self, db: AsyncSession, lesson: _Lesson, finalise: FinaliseReviewPack
    ) -> PackChecks:
        pack = lesson.pack
        if pack.student_id is None:
            raise MissingPackInputError("learner_pack_without_student")
        class_pack = await the_lessons_approved_class_pack(db, pack.plan_version_id)
        if class_pack is None:
            raise MissingPackInputError("class_pack_not_approved")
        learner = await learner_inputs(
            db,
            self._learner_states,
            student_id=pack.student_id,
            plan_version_id=pack.plan_version_id,
        )
        request = self._learner_requests.build(
            session_plan=lesson.session_plan,
            base_pack_id=base_pack_id(pack.plan_version_id),
            focal_learner_id=pack.student_id,
            learner_states=learner.states,
            policy=PERSONALISED_REVIEW_PACK_POLICY,
            session_signals=learner.signals,
            sources=lesson.sources,
            specification=lesson.specification,
        )
        return PackChecks(
            PERSONALISED_REVIEW_PACK_POLICY, request, _stored_sections(class_pack), finalise
        )
