"""A teacher's revision of a revision note passes the checks its generation ran.

The revised sections go through the pack's policy checks and bounded repair before the
pack returns to pending, the turn reports the real outcome, and findings still standing
are written where the teacher reads the turn. A pack whose inputs are gone is refused.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable

import pytest
from condition_leakage_support import SilentCritic
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.errors import ArtefactRevisionError
from app.domains.artefact_revision.application.executor import RevisionExecutionOutcome
from app.domains.artefact_revision.application.review_pack_executor import (
    ReviewPackRevisionExecutor,
)
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactScope
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.core.infrastructure.repository import ArtefactRepository
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
    sections_to_review_pack_manifest,
)
from app.domains.artefacts.types.post_class_review_pack.application.pack_inputs import PackInputs
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    LessonContextForGeneration,
    ReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.finalise_pack import (
    FinaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.revised_pack_checks import (  # noqa: E501
    RevisedPackChecks,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.schemas import (
    CheckResult,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ValidationCheck,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import ReviewPackPipeline
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackPracticeItem,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.revise_review_pack import (  # noqa: E501
    ReviewPackRevisionResult,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.generation_wiring import (
    class_note_requests,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.lesson_notes import (
    SqlAlchemyApprovedLessonNotes,
)
from app.domains.assessments.models import ExitTicketSubmission
from app.domains.learners.models import LearnerProfile
from app.shared.json_types import JsonObject
from app.shared.time import utc_now

PLAN = "LPV-RVC"
STUDENT = "ST-RVC"
SESSION_PLAN: JsonObject = {
    "subject": "Mathematics",
    "grade": "JSS1",
    "topic": "Area",
    "lesson_plan_objectives": [
        {"lesson_objective_id": "lo1", "objective_text": "Find the area of a rectangle."},
        {"lesson_objective_id": "lo2", "objective_text": "Find the area of a square."},
    ],
    "steps": [
        {"step_id": "s1", "step_kind": "core", "lesson_objective_id": "lo1", "title": "One"},
        {"step_id": "s2", "step_kind": "core", "lesson_objective_id": "lo2", "title": "Two"},
    ],
}
GROUNDING = {
    "expert_sources": "lesson-note",
    "lesson_note": {"id": "AT-RVC-note", "version": 1, "origin": "teacher"},
}
_CONTEXT = LessonContextForGeneration(
    subject="Mathematics", grade_level="JSS1", topic="Area", lesson_objectives=["lo1", "lo2"]
)

Edit = Callable[[ReviewPackSection], ReviewPackSection]


def _note() -> Artefact:
    return Artefact(
        artefact_id="AT-RVC-note",
        artefact_type="lesson_note",
        scope="class_level",
        plan_version_id=PLAN,
        manifest={
            "plan_version_id": PLAN,
            "sections": [
                {"step_id": "s1", "body": "Area of a rectangle is length times width."},
                {"step_id": "s2", "body": "Area of a square is side times side."},
            ],
        },
        artefact_refs={"origin": "teacher"},
        review_status=ArtefactReviewStatus.APPROVED,
    )


async def _seed_lesson(db: AsyncSession) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add_all(
        [
            LessonPlan(
                plan_id="LP-RVC",
                lesson_period_id=uuid.uuid4(),
                title="Area",
                subject="Mathematics",
                track="General",
                grade="JSS1",
                created_by="Teacher One",
            ),
            PlanVersion(
                version_id=PLAN,
                plan_id="LP-RVC",
                source_type="manual",
                session_plan=SESSION_PLAN,
                status=PlanVersionStatus.APPROVED,
            ),
            _note(),
        ]
    )
    await db.flush()


EXPLANATION = (
    "The area of a rectangle is the number of unit squares that cover it. A rectangle 2 units "
    "wide and 3 units long is covered by 2 rows of 3 squares, so its area is 2 times 3, which is "
    "6 square units. In general, multiply the two side lengths. The units of area are square "
    "units because each cover is a square, not a length, so write cm squared and not cm."
)


def _section(unit: SectionGenerationUnit) -> ReviewPackSection:
    """A section that passes every structural check against its unit."""
    return ReviewPackSection(
        section_id=unit.unit_id,
        title=unit.objective_text,
        lesson_objective_id=unit.lesson_objective_id,
        blocks=[
            ReviewPackBlock(
                block_id=f"{unit.unit_id}:b0",
                block_type="explanation",
                text=EXPLANATION,
                lesson_objective_id=unit.lesson_objective_id,
                source_refs=[unit.source_evidence[0].source_ref],
            )
        ],
        practice=[
            ReviewPackPracticeItem(
                item_id=f"{unit.unit_id}:p0", prompt="Find the area of 2 by 3.", answer="6"
            )
        ],
    )


async def _pack(
    db: AsyncSession, checks: RevisedPackChecks, *, scope: ArtefactScope, artefact_id: str
) -> Artefact:
    """A stored pack whose sections pass the checks it was generated under."""
    student = STUDENT if scope is ArtefactScope.LEARNER_LEVEL else None
    pack = Artefact(
        artefact_id=artefact_id,
        artefact_type="post_class_review_pack",
        scope=scope.value,
        plan_version_id=PLAN,
        student_id=student,
        manifest={},
        artefact_refs=GROUNDING,
        review_status=ArtefactReviewStatus.APPROVED,
    )
    units = (await checks.for_pack(db, pack)).request.units
    pack.manifest = sections_to_review_pack_manifest(
        sections=[_section(unit) for unit in units],
        artefact_id=artefact_id,
        plan_version_id=PLAN,
        scope=scope,
        lesson_context=_CONTEXT,
        created_at=utc_now(),
        student_id=student,
    )
    db.add(pack)
    await db.flush()
    return pack


class _Reviser:
    """Applies one edit to every section, as a teacher's instruction would."""

    def __init__(self, edit: Edit) -> None:
        self.edit = edit
        self.calls = 0

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
    ) -> ReviewPackRevisionResult:
        self.calls += 1
        revised = [self.edit(section.model_copy(deep=True)) for section in current_sections]
        return ReviewPackRevisionResult(sections=revised, change_summary="Simplified the wording.")


class _Repairer:
    """Repairs a failed section with ``fix``; without one it hands the section back unchanged."""

    def __init__(self, fix: Edit | None = None) -> None:
        self.fix = fix
        self.rounds: list[list[str]] = []

    async def repair_section(
        self,
        *,
        request: ReviewPackRequest,
        unit: SectionGenerationUnit,
        failed_section: ReviewPackSection,
        issues: list[str],
    ) -> ReviewPackSection:
        self.rounds.append(issues)
        copy = failed_section.model_copy(deep=True)
        return self.fix(copy) if self.fix else copy


class _Regenerating:
    """Writes a section again from its unit, with practice, as a regeneration would."""

    def __init__(self) -> None:
        self.units: list[str] = []

    async def generate_section(
        self, *, request: ReviewPackRequest, unit: SectionGenerationUnit
    ) -> ReviewPackSection:
        self.units.append(unit.unit_id)
        return _add_practice(_section(unit))


class _NoRegeneration:
    async def generate_section(
        self, *, request: ReviewPackRequest, unit: SectionGenerationUnit
    ) -> ReviewPackSection:
        raise AssertionError("a revision with few findings is repaired, never regenerated")


def _checks(repairer: _Repairer) -> RevisedPackChecks:
    def finalise_for(pipeline: ReviewPackPipeline) -> FinaliseReviewPack:
        return FinaliseReviewPack(
            generator=_NoRegeneration(), repairer=repairer, critic=SilentCritic()
        )

    return RevisedPackChecks(
        inputs=PackInputs(SqlAlchemyApprovedLessonNotes(), None),
        finalise_for=finalise_for,
        class_requests=class_note_requests(),
    )


def _reword(section: ReviewPackSection) -> ReviewPackSection:
    for block in section.blocks:
        block.text = f"Length times width gives the area. {EXPLANATION}"
    return section


def _drop_practice(section: ReviewPackSection) -> ReviewPackSection:
    section.practice = []
    return section


def _add_practice(section: ReviewPackSection) -> ReviewPackSection:
    item = ReviewPackPracticeItem(item_id="p-new", prompt="Area of 4 by 5?", answer="20")
    section.practice = [item]
    return section


def _cite_unseen_source(section: ReviewPackSection) -> ReviewPackSection:
    for block in section.blocks:
        block.source_refs = ["REF-99"]
    return section


async def _revise(
    db: AsyncSession, pack: Artefact, reviser: _Reviser, checks: RevisedPackChecks
) -> RevisionExecutionOutcome:
    executor = ReviewPackRevisionExecutor(ArtefactRepository(), reviser=reviser, checks=checks)
    return await executor.revise(
        db=db,
        subject_id=pack.artefact_id,
        thread_id="TH-RVC",
        instruction="Make the wording simpler.",
        highlight=None,
        conversation_summary="",
    )


def _practice_blocks(pack: Artefact) -> int:
    return sum(
        block["type"] == "practice" for step in pack.manifest["steps"] for block in step["blocks"]
    )


@pytest.mark.asyncio
async def test_a_revision_that_keeps_the_checks_passes_without_repair(db: AsyncSession) -> None:
    await _seed_lesson(db)
    repairer = _Repairer()
    checks = _checks(repairer)
    pack = await _pack(db, checks, scope=ArtefactScope.CLASS_LEVEL, artefact_id="AT-RVC-1")

    outcome = await _revise(db, pack, _Reviser(_reword), checks)

    assert outcome.validation_passed is True
    assert outcome.change_summary == "Simplified the wording."
    assert repairer.rounds == []
    assert "Length times width" in str(pack.manifest)
    assert (pack.review_status, pack.version) == (ArtefactReviewStatus.PENDING, 2)
    review = pack.artefact_refs["review"]
    assert review["version"] == 2
    assert {check["check"]: check["passed"] for check in review["checks"]}["explanation_present"]


@pytest.mark.asyncio
async def test_a_revision_that_fails_the_checks_is_repaired_and_reports_what_remains(
    db: AsyncSession,
) -> None:
    await _seed_lesson(db)
    repairer = _Repairer()
    checks = _checks(repairer)
    pack = await _pack(db, checks, scope=ArtefactScope.CLASS_LEVEL, artefact_id="AT-RVC-2")

    outcome = await _revise(db, pack, _Reviser(_drop_practice), checks)

    assert outcome.validation_passed is False
    # Two sections, each repaired once per round, for the class policy's two rounds.
    assert len(repairer.rounds) == 4
    assert all(any("practice_is_checkable" in issue for issue in r) for r in repairer.rounds)
    assert outcome.change_summary.startswith("Simplified the wording.")
    assert "Still flagged after repair:" in outcome.change_summary
    assert "practice_is_checkable" in outcome.change_summary
    assert _practice_blocks(pack) == 0
    assert (pack.review_status, pack.version) == (ArtefactReviewStatus.PENDING, 2)


@pytest.mark.asyncio
async def test_a_revision_the_repair_round_fixes_passes(db: AsyncSession) -> None:
    await _seed_lesson(db)
    repairer = _Repairer(fix=_add_practice)
    checks = _checks(repairer)
    pack = await _pack(db, checks, scope=ArtefactScope.CLASS_LEVEL, artefact_id="AT-RVC-3")

    outcome = await _revise(db, pack, _Reviser(_drop_practice), checks)

    assert outcome.validation_passed is True
    assert len(repairer.rounds) == 2
    assert outcome.change_summary == "Simplified the wording."
    assert _practice_blocks(pack) == 2
    assert "Area of 4 by 5?" in str(pack.manifest)


@pytest.mark.asyncio
async def test_a_learner_revision_is_checked_under_the_learner_policy(db: AsyncSession) -> None:
    await _seed_lesson(db)
    repairer = _Repairer()
    checks = _checks(repairer)
    await _pack(db, checks, scope=ArtefactScope.CLASS_LEVEL, artefact_id="AT-RVC-class")
    db.add_all(
        [
            LearnerProfile(student_id=STUDENT, full_name="Ada", grade="JSS1", track="General"),
            ExitTicketSubmission(
                diagnostic_id="DG-RVC",
                student_id=STUDENT,
                plan_version_id=PLAN,
                results={
                    "objectives": [
                        {"lesson_objective_id": "lo1", "score": 1, "max_score": 2, "items": []},
                        {"lesson_objective_id": "lo2", "score": 2, "max_score": 2, "items": []},
                    ]
                },
            ),
        ]
    )
    await db.flush()
    pack = await _pack(db, checks, scope=ArtefactScope.LEARNER_LEVEL, artefact_id="AT-RVC-4")

    outcome = await _revise(db, pack, _Reviser(_cite_unseen_source), checks)

    assert outcome.validation_passed is False
    # The learner policy allows one repair round.
    assert len(repairer.rounds) == 2
    assert "source_refs_valid" in outcome.change_summary
    assert "REF-99" in outcome.change_summary
    assert pack.review_status == ArtefactReviewStatus.PENDING


@pytest.mark.asyncio
async def test_a_learner_pack_without_its_evidence_is_refused_before_the_reviser_runs(
    db: AsyncSession,
) -> None:
    await _seed_lesson(db)
    checks = _checks(_Repairer())
    await _pack(db, checks, scope=ArtefactScope.CLASS_LEVEL, artefact_id="AT-RVC-class2")
    db.add(LearnerProfile(student_id=STUDENT, full_name="Ada", grade="JSS1", track="General"))
    await db.flush()
    pack = Artefact(
        artefact_id="AT-RVC-5",
        artefact_type="post_class_review_pack",
        scope=ArtefactScope.LEARNER_LEVEL.value,
        plan_version_id=PLAN,
        student_id=STUDENT,
        manifest={"steps": []},
        artefact_refs=GROUNDING,
        review_status=ArtefactReviewStatus.APPROVED,
    )
    db.add(pack)
    await db.flush()
    reviser = _Reviser(_reword)

    with pytest.raises(ArtefactRevisionError) as refused:
        await _revise(db, pack, reviser, checks)

    assert (refused.value.status_code, refused.value.detail) == (
        409,
        "revision_cannot_be_checked:diagnostic_not_found",
    )
    assert reviser.calls == 0


@pytest.mark.asyncio
async def test_a_pack_whose_plan_version_is_gone_is_refused_and_left_unchanged(
    db: AsyncSession,
) -> None:
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    pack = Artefact(
        artefact_id="AT-RVC-6",
        artefact_type="post_class_review_pack",
        scope=ArtefactScope.CLASS_LEVEL.value,
        plan_version_id="LPV-RVC-GONE",
        manifest={"steps": []},
        review_status=ArtefactReviewStatus.APPROVED,
    )
    db.add(pack)
    await db.flush()
    reviser = _Reviser(_reword)

    with pytest.raises(ArtefactRevisionError) as refused:
        await _revise(db, pack, reviser, _checks(_Repairer()))

    assert (refused.value.status_code, refused.value.detail) == (
        409,
        "revision_cannot_be_checked:plan_version_not_found",
    )
    assert reviser.calls == 0
    assert (pack.review_status, pack.version, pack.manifest) == (
        ArtefactReviewStatus.APPROVED,
        1,
        {"steps": []},
    )


class _FindingCritic:
    """Finds four problems in the first objective's section the first time it reads, then none."""

    def __init__(self) -> None:
        self.reads = 0

    async def review(
        self,
        *,
        request: ReviewPackRequest,
        sections: list[ReviewPackSection],
        checks: tuple[ValidationCheck, ...],
    ) -> list[CheckResult]:
        self.reads += 1
        first = self.reads == 1
        return [
            CheckResult(
                check=check,
                passed=not (first and check == "content_grounding"),
                message="the section drifts from the lesson" if first else None,
                details=(
                    {
                        "sections_with_findings": ["lo1"],
                        "findings": [f"finding {number}" for number in range(4)],
                    }
                    if first and check == "content_grounding"
                    else {}
                ),
            )
            for check in checks
        ]


@pytest.mark.asyncio
async def test_a_section_the_checks_write_again_is_named_in_the_turn_summary(
    db: AsyncSession,
) -> None:
    await _seed_lesson(db)
    regenerating = _Regenerating()

    def finalise_for(pipeline: ReviewPackPipeline) -> FinaliseReviewPack:
        return FinaliseReviewPack(
            generator=regenerating, repairer=_Repairer(), critic=_FindingCritic()
        )

    checks = RevisedPackChecks(
        inputs=PackInputs(SqlAlchemyApprovedLessonNotes(), None),
        finalise_for=finalise_for,
        class_requests=class_note_requests(),
    )
    pack = await _pack(db, checks, scope=ArtefactScope.CLASS_LEVEL, artefact_id="AT-RVC-9")

    outcome = await _revise(db, pack, _Reviser(_reword), checks)

    assert len(regenerating.units) == 1
    assert outcome.change_summary.startswith("Simplified the wording.")
    assert "Written again from scratch by the checks:" in outcome.change_summary
    assert "ask again if it is missing" in outcome.change_summary
    assert outcome.validation_passed is True
