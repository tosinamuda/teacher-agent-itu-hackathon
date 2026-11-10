"""Study-pack revision executor: load the pack artefact, revise, check, re-materialise.

Bridges the generic revision thread to a class or learner post-class review pack.
Unlike the lesson-plan executor there is no artefact versioning — a turn revises
the pack manifest **in place** (same ``artefact_id``) via the spec adapters
(``review_pack_manifest_to_sections`` -> revise -> ``sections_to_review_pack_manifest``).
The revised sections go through the checks and bounded repair the pack's generation
ran; findings still standing after the last round are written into the turn's
summary, and the pack returns to ``review_status="pending"`` so the teacher decides.
The service records the ``RevisionTurn`` and commits.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.errors import ArtefactRevisionError
from app.domains.artefact_revision.application.executor import RevisionExecutionOutcome
from app.domains.artefact_revision.application.highlight import format_highlight
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactScope
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.post_class_review_pack.application.errors import (
    MissingPackInputError,
)
from app.shared.json_types import JsonObject
from app.shared.time import utc_now

# Review-pack DSPy infrastructure is imported lazily inside the functions below:
# importing it at module load (the artefact_revision routes load at app boot)
# would initialize a language-model adapter during API composition. Deferring to
# request time keeps module import side-effect free.
if TYPE_CHECKING:
    from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
        LessonContextForGeneration,
    )
    from app.domains.artefacts.types.post_class_review_pack.application.revision.revised_pack_checks import (  # noqa: E501
        CheckedPack,
    )
    from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
        ReviewPackSection,
    )
    from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.revise_review_pack import (  # noqa: E501
        ReviewPackRevisionResult,
    )


class ReviewPackRevision(Protocol):
    """Apply one teacher instruction to the current review-pack sections."""

    async def revise(
        self,
        *,
        current_sections: list[ReviewPackSection],
        lesson_context: LessonContextForGeneration,
        highlighted_part: str,
        instruction: str,
        conversation_summary: str,
        correlation_id: str,
        thread_id: str,
    ) -> ReviewPackRevisionResult: ...


class ReviewPackArtefacts(Protocol):
    """Load the current review-pack artefact and lock it before mutation."""

    async def get_artefact(self, db: AsyncSession, artefact_id: str) -> Artefact | None: ...

    async def get_artefact_for_update(
        self, db: AsyncSession, artefact_id: str
    ) -> Artefact | None: ...


class ReviewPackChecks(Protocol):
    """The checks one pack was generated under, bound to its rebuilt request."""

    async def check(self, sections: list[ReviewPackSection]) -> CheckedPack: ...


class RevisionChecks(Protocol):
    """Bind a stored pack's checks; raises ``MissingPackInputError`` when an input is gone."""

    async def for_pack(self, db: AsyncSession, pack: Artefact) -> ReviewPackChecks: ...


def _live_reviser() -> ReviewPackRevision:
    from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.revise_review_pack import (  # noqa: E501
        ReviseReviewPack,
    )
    from app.infra.dspy_lm import build_dspy_lm

    return ReviseReviewPack(lm=build_dspy_lm())


def _live_checks() -> RevisionChecks:
    from app.domains.artefacts.types.post_class_review_pack.infrastructure.wiring import (
        build_revised_pack_checks,
    )

    return build_revised_pack_checks()


def _turn_summary(change_summary: str, unresolved: list[str], rewritten: list[str]) -> str:
    """What the turn changed, what repair wrote again, and what the checks still flag."""
    summary = change_summary
    if rewritten:
        summary += (
            f"\n\n**Written again from scratch by the checks:** {'; '.join(rewritten)}. "
            "What you asked for may not be in them: ask again if it is missing."
        )
    if unresolved:
        summary += f"\n\n**Still flagged after repair:** {'; '.join(unresolved)}"
    return summary


def _opt_str(value: object) -> str | None:
    return str(value) if isinstance(value, str) and value else None


def _lesson_context_from_manifest(
    manifest: JsonObject, sections: list[ReviewPackSection]
) -> LessonContextForGeneration:
    from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
        LessonContextForGeneration,
    )

    raw_objectives = manifest.get("lesson_plan_objectives", [])
    objectives = [
        str(item.get("text") or item.get("objective_text") or "")
        for item in (raw_objectives if isinstance(raw_objectives, list) else [])
        if isinstance(item, dict)
    ]
    objectives = [text for text in objectives if text]
    if not objectives:
        objectives = [section.title for section in sections if section.title]
    return LessonContextForGeneration(
        subject=str(manifest.get("subject") or ""),
        grade_level=str(manifest.get("grade") or ""),
        topic=str(manifest.get("topic") or ""),
        subtopic=_opt_str(manifest.get("subtopic")),
        curriculum_scope=_opt_str(manifest.get("theme")),
        lesson_objectives=objectives or ["(objective unavailable)"],
    )


def _personalisation_bands(manifest: JsonObject) -> dict[str, str]:
    bands: dict[str, str] = {}
    steps = manifest.get("steps", [])
    for step in steps if isinstance(steps, list) else []:
        if not isinstance(step, dict):
            continue
        objective_id = step.get("lesson_objective_id")
        band = step.get("personalisation_band")
        if objective_id and band:
            bands[str(objective_id)] = str(band)
    return bands


def _created_at(manifest: JsonObject) -> datetime:
    raw = manifest.get("created_at")
    if isinstance(raw, str):
        try:
            return datetime.fromisoformat(raw)
        except ValueError:
            pass
    return utc_now()


class ReviewPackRevisionExecutor:
    """Revises a review pack, checks it as generation does, and rewrites it in place."""

    artefact_type = "post_class_review_pack"

    def __init__(
        self,
        repository: ReviewPackArtefacts,
        reviser: ReviewPackRevision | None = None,
        checks: RevisionChecks | None = None,
    ) -> None:
        self.reviser = reviser or _live_reviser()
        self.checks = checks or _live_checks()
        self.repository = repository

    async def _pack(self, db: AsyncSession, artefact_id: str) -> Artefact | None:
        """The artefact, only if it is a review pack: other kinds share the table."""
        artefact = await self.repository.get_artefact(db, artefact_id)
        if artefact is None or artefact.artefact_type != self.artefact_type:
            return None
        return artefact

    async def current_artefact(
        self,
        *,
        db: AsyncSession,
        subject_id: str,
    ) -> tuple[str | None, JsonObject | None]:
        """Return the current ``(artefact_id, manifest)`` for the subject id."""
        artefact = await self._pack(db, subject_id)
        if artefact is None:
            return None, None
        return artefact.artefact_id, artefact.manifest

    async def _checks_for(self, db: AsyncSession, artefact: Artefact) -> ReviewPackChecks:
        """Bound before the reviser runs, so a pack that cannot be checked costs no model call."""
        try:
            return await self.checks.for_pack(db, artefact)
        except MissingPackInputError as error:
            raise ArtefactRevisionError(409, f"revision_cannot_be_checked:{error}") from error

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
        artefact = await self._pack(db, subject_id)
        if artefact is None:
            raise LookupError("artefact_not_found")
        checks = await self._checks_for(db, artefact)
        manifest: JsonObject = artefact.manifest or {}
        sections = _stored_sections(manifest)
        lesson_context = _lesson_context_from_manifest(manifest, sections)

        result = await self.reviser.revise(
            current_sections=sections,
            lesson_context=lesson_context,
            highlighted_part=format_highlight(
                highlight, ("step_id", "block_id", "lesson_objective_id")
            ),
            instruction=instruction,
            conversation_summary=conversation_summary,
            correlation_id=artefact.artefact_id,
            thread_id=thread_id,
        )
        checked = await checks.check(result.sections)
        new_manifest = _revised_manifest(artefact, manifest, checked.sections, lesson_context)
        await self._write_back(db, artefact, new_manifest, checked.review)
        return RevisionExecutionOutcome(
            base_version_id=artefact.artefact_id,
            result_version_id=artefact.artefact_id,
            session_plan=new_manifest,
            change_summary=_turn_summary(
                result.change_summary, checked.unresolved, checked.regenerated_titles
            ),
            validation_passed=checked.validation.passed,
        )

    async def _write_back(
        self, db: AsyncSession, artefact: Artefact, manifest: JsonObject, review: JsonObject | None
    ) -> None:
        """Rewrite the pack in place; a revised pack still needs the teacher's approval.

        The row is re-read FOR UPDATE here, not during the slow generation, so the
        manifest+status rewrite serializes against a concurrent teacher approve rather
        than racing it (a lost manifest, or an approval silently undone).
        populate_existing refreshes the loaded object. The service commits.
        """
        locked = await self.repository.get_artefact_for_update(db, artefact.artefact_id)
        target = locked if locked is not None else artefact
        target.manifest = manifest
        target.review_status = ArtefactReviewStatus.PENDING
        # An approve that carries the pre-revise version is then rejected (409) instead of
        # blessing a manifest the teacher never reviewed.
        target.version = target.version + 1
        if review is not None:
            target.artefact_refs = {
                **(target.artefact_refs or {}),
                "review": {**review, "version": target.version},
            }


def _stored_sections(manifest: JsonObject) -> list[ReviewPackSection]:
    from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
        review_pack_manifest_to_sections,
    )
    from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack

    return review_pack_manifest_to_sections(PostClassReviewPack.model_validate(manifest))


def _revised_manifest(
    artefact: Artefact,
    manifest: JsonObject,
    sections: list[ReviewPackSection],
    lesson_context: LessonContextForGeneration,
) -> JsonObject:
    from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
        sections_to_review_pack_manifest,
    )

    raw_objectives = manifest.get("lesson_plan_objectives")
    return sections_to_review_pack_manifest(
        sections=sections,
        artefact_id=artefact.artefact_id,
        plan_version_id=artefact.plan_version_id,
        scope=ArtefactScope(artefact.scope),
        lesson_context=lesson_context,
        created_at=_created_at(manifest),
        lesson_plan_objectives=(
            [item for item in raw_objectives if isinstance(item, dict)]
            if isinstance(raw_objectives, list)
            else []
        ),
        student_id=artefact.student_id,
        personalisation_bands=_personalisation_bands(manifest),
    )
