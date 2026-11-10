"""Materialise a successful condition run as a review-pack artefact.

Lives here, not in ``experiments``, because it needs this domain's manifest
adapter and the ``Artefact`` row — and experiments already supplies the pack
schemas the adapter reads, so building it on that side would close a cycle.
"""

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import (
    ArtefactReviewStatus,
    ArtefactScope,
    ArtefactType,
)
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
    sections_to_review_pack_manifest,
)
from app.domains.artefacts.types.post_class_review_pack.application.materialisation import (
    ReviewPackMaterialisation,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generated_review_pack import (
    GeneratedReviewPack,
)
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.json_types import JsonObject
from app.shared.time import utc_now


def build_review_pack_artefact(
    *,
    materialisation: ReviewPackMaterialisation,
) -> Artefact:
    """Build the rater-visible artefact linked to one completed condition run."""
    artefact_id = new_public_id(PublicIdPrefix.ARTEFACT)
    review_status = (
        ArtefactReviewStatus.PENDING
        if materialisation.requires_teacher_review
        else ArtefactReviewStatus.APPROVED
    )
    return Artefact(
        artefact_id=artefact_id,
        artefact_type=ArtefactType.POST_CLASS_REVIEW_PACK.value,
        scope=materialisation.scope.value,
        plan_version_id=materialisation.plan_version_id,
        student_id=materialisation.learner_id,
        experiment_condition_run_id=materialisation.condition_run_id,
        manifest=review_pack_manifest(
            materialisation.result,
            artefact_id=artefact_id,
            plan_version_id=materialisation.plan_version_id,
            scope=materialisation.scope,
            student_id=materialisation.learner_id,
            created_at=utc_now(),
        ),
        review_status=review_status,
        artefact_refs=materialisation.artefact_refs or None,
    )


def review_pack_manifest(
    result: GeneratedReviewPack,
    *,
    artefact_id: str,
    plan_version_id: str,
    scope: ArtefactScope,
    student_id: str | None,
    created_at: datetime,
) -> JsonObject:
    """Project a generated pack into the rater-visible artefact manifest."""
    units = result.request.units
    return sections_to_review_pack_manifest(
        sections=result.sections,
        artefact_id=artefact_id,
        plan_version_id=plan_version_id,
        scope=scope,
        lesson_context=result.request.lesson_context,
        created_at=created_at,
        lesson_plan_objectives=[
            {
                "lesson_objective_id": unit.lesson_objective_id,
                "objective_text": unit.objective_text,
            }
            for unit in units
        ],
        student_id=student_id,
        personalisation_bands={
            unit.lesson_objective_id: unit.objective_learner_state.mastery_band
            for unit in units
            if unit.objective_learner_state is not None
        },
    )


class SqlAlchemyReviewPackArtefactWriter:
    """Stage the review pack a condition run produced, for the store to commit."""

    def __init__(self, session: AsyncSession) -> None:
        self._db = session

    def stage(
        self,
        materialisation: ReviewPackMaterialisation,
    ) -> None:
        """Build the artefact for one completed run and stage it on the session."""
        self._db.add(build_review_pack_artefact(materialisation=materialisation))
