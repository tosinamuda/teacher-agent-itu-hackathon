"""Every path that reads a pack back out of its manifest and re-renders it.

Three production callers recover sections from a stored ``PostClassReviewPack``:
the H2 base pack, the student pack, and the revision turn. Each one puts pack
content back into a prompt and writes a new manifest, so each is a place the
wrong content could enter a pack that a teacher already approved — and each is a
place the recover/render cycle could accumulate.

The H2 base pack is covered in ``test_condition_leakage_downstream``; these are
the other two. The model stand-in echoes its whole input back, so anything a
call is handed shows up in what it produces.
"""

from __future__ import annotations

import random
import re
from datetime import datetime, timezone

import pytest
from condition_leakage_support import (
    PLAN_ONLY,
    ROGUE,
    CanaryPlan,
    EchoModel,
    build_canary_plan,
    classes_in,
    fuzz_seeds,
    stand_in_collaborators,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.review_pack_executor import (
    ReviewPackRevisionExecutor,
)
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactScope
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.post_class_review_pack.application.manifest_adapter import (
    review_pack_manifest_to_sections,
    sections_to_review_pack_manifest,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    LearnerStatus,
    LessonContextForGeneration,
    ObjectiveLearnerState,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.revised_pack_checks import (  # noqa: E501
    CheckedPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.schemas import (
    ValidationResult,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackBlock,
    ReviewPackPracticeItem,
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.revise_review_pack import (  # noqa: E501
    ReviewPackRevisionResult,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.generation_wiring import (
    build_base_review_pack_generator,
    build_review_pack_personaliser,
)
from app.domains.artefacts.types.post_class_review_pack.schemas import PostClassReviewPack
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.shared.json_types import JsonObject

_CREATED_AT = datetime(2026, 8, 11, tzinfo=timezone.utc)


def _sources_lines(manifest: JsonObject) -> list[int]:
    """How many attribution lines each rendered block carries."""
    return [
        str(block.get("content", "")).count("_Sources:")
        for step in manifest["steps"]
        for block in step["blocks"]
    ]


async def _approved_base(plan: CanaryPlan) -> JsonObject:
    """A C3 pack rendered to a manifest — what an approved artefact holds."""
    echo = EchoModel()
    generator = build_base_review_pack_generator(stand_in_collaborators(echo))
    result = await generator.generate(
        session_plan=plan.view,
        policy=profile_for(Hypothesis.H1, ConditionCode.C3),
        sources=plan.sources,
    )
    return sections_to_review_pack_manifest(
        sections=result.sections,
        artefact_id="AT-BASE",
        plan_version_id="LPV-1",
        scope=ArtefactScope.CLASS_LEVEL,
        lesson_context=result.request.lesson_context,
        created_at=_CREATED_AT,
    )


def _recover(manifest: JsonObject) -> list[ReviewPackSection]:
    return review_pack_manifest_to_sections(PostClassReviewPack.model_validate(manifest))


# ===== The student pack: recover the approved base, personalise for ONE learner =====


async def _student_pack(
    plan: CanaryPlan, base: JsonObject, student_id: str, band: LearnerStatus
) -> JsonObject:
    """The transformation ``generate_for_student`` performs, without its DB work."""
    sections = _recover(base)
    echo = EchoModel(marker=student_id)
    personaliser = build_review_pack_personaliser(stand_in_collaborators(echo))
    result = await personaliser.personalise(
        session_plan=plan.view,
        base_sections=sections,
        learner_states={
            section.lesson_objective_id: ObjectiveLearnerState(
                lesson_objective_id=section.lesson_objective_id,
                mastery_band=band,
                misconception=f"{student_id}-only-misconception",
            )
            for section in sections
        },
        base_pack_id="AT-BASE",
        focal_learner_id=student_id,
        policy=profile_for(Hypothesis.H2, ConditionCode.P1),
        sources=plan.sources,
    )
    return sections_to_review_pack_manifest(
        sections=result.sections,
        artefact_id=f"AT-{student_id}",
        plan_version_id="LPV-1",
        scope=ArtefactScope.LEARNER_LEVEL,
        lesson_context=result.request.lesson_context,
        created_at=_CREATED_AT,
        student_id=student_id,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("seed", fuzz_seeds(11, 73))
async def test_a_student_pack_carries_only_that_students_state(seed: int) -> None:
    """Two learners share one approved base; neither may see the other's state.

    The base sections are recovered per student, but a shared mutable base or a
    learner-state mix-up would put one child's diagnostic evidence into another
    child's pack — the same failure class as the H2 shared base pack.
    """
    plan = build_canary_plan(random.Random(seed))
    base = await _approved_base(plan)

    first = await _student_pack(plan, base, "STU-1", "remediate")
    second = await _student_pack(plan, base, "STU-2", "extend")

    assert "STU-1-only-misconception" in str(first)
    assert "STU-1-only-misconception" not in str(second)
    assert "STU-2-only-misconception" in str(second)
    assert "STU-2-only-misconception" not in str(first)
    # The approved base must be unchanged by either render.
    assert base == await _approved_base(plan)


@pytest.mark.asyncio
@pytest.mark.parametrize("seed", fuzz_seeds(11, 73))
async def test_a_student_pack_adds_no_plan_context_and_no_second_attribution(seed: int) -> None:
    plan = build_canary_plan(random.Random(seed))
    base = await _approved_base(plan)
    pack = await _student_pack(plan, base, "STU-1", "remediate")

    assert not classes_in(pack) - classes_in(base)
    assert PLAN_ONLY not in classes_in(pack)
    assert ROGUE not in classes_in(pack)
    assert max(_sources_lines(pack), default=0) <= 1


# ===== The revision turn: recover, revise, re-render IN PLACE =====


def _artefact(manifest: JsonObject) -> Artefact:
    return Artefact(
        artefact_id="AT-BASE",
        artefact_type="post_class_review_pack",
        plan_version_id="LPV-1",
        scope=ArtefactScope.LEARNER_LEVEL.value,
        student_id="STU-1",
        manifest=manifest,
        version=1,
        review_status=ArtefactReviewStatus.APPROVED,
    )


class _FakeRepository:
    def __init__(self, artefact: Artefact) -> None:
        self.artefact = artefact

    async def get_artefact(self, db: AsyncSession, artefact_id: str) -> Artefact:
        return self.artefact

    async def get_artefact_for_update(self, db: AsyncSession, artefact_id: str) -> Artefact:
        return self.artefact


class _PassingChecks:
    """Reports every revision as passing: these tests are about the manifest round trip."""

    async def for_pack(self, db: AsyncSession, pack: Artefact) -> _PassingChecks:
        return self

    async def check(self, sections: list[ReviewPackSection]) -> CheckedPack:
        return CheckedPack(sections=sections, validation=ValidationResult(passed=True, checks=[]))


_REF_MENTION = re.compile(r"REF-\d+")


class _CitingReviser:
    """Keeps the text it was handed and cites the refs it can see in it.

    That is what a real reviser does — the signature tells it to carry source
    refs — and it is the behaviour that compounds: text still carrying an
    attribution line, plus structured refs for the renderer to append again.
    A stub that returned no refs would make the accumulation test vacuous.
    """

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
        revised: list[ReviewPackSection] = []
        for section in current_sections:
            copy = section.model_copy(deep=True)
            for block in copy.blocks:
                seen = dict.fromkeys(_REF_MENTION.findall(block.text) + list(block.source_refs))
                block.source_refs = list(seen)
            revised.append(copy)
        return ReviewPackRevisionResult(sections=revised, change_summary="unchanged")


async def _revise(executor: ReviewPackRevisionExecutor) -> None:
    async with AsyncSession() as db:
        await executor.revise(
            db=db,
            subject_id="AT-BASE",
            thread_id="TH-1",
            instruction="Make the wording simpler.",
            highlight=None,
            conversation_summary="",
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("seed", fuzz_seeds(11, 73))
async def test_repeated_revision_never_stacks_attribution_lines(seed: int) -> None:
    """A turn recovers the manifest and writes a new one, so it can compound.

    Each round previously re-appended the sources trailer the last round had
    already baked into the text, so a pack revised three times told the reader
    four times where it came from.
    """
    plan = build_canary_plan(random.Random(seed))
    artefact = _artefact(await _approved_base(plan))
    executor = ReviewPackRevisionExecutor(
        reviser=_CitingReviser(),
        repository=_FakeRepository(artefact),
        checks=_PassingChecks(),
    )
    before = _sources_lines(artefact.manifest)

    for _ in range(3):
        await _revise(executor)

    assert _sources_lines(artefact.manifest) == before
    assert max(_sources_lines(artefact.manifest), default=0) <= 1


@pytest.mark.asyncio
@pytest.mark.parametrize("seed", fuzz_seeds(11, 73))
async def test_revision_introduces_no_context_the_pack_did_not_have(seed: int) -> None:
    """A revision edits an approved pack; it may not re-open the lesson plan."""
    plan = build_canary_plan(random.Random(seed))
    original = await _approved_base(plan)
    artefact = _artefact(dict(original))
    executor = ReviewPackRevisionExecutor(
        reviser=_CitingReviser(),
        repository=_FakeRepository(artefact),
        checks=_PassingChecks(),
    )

    await _revise(executor)

    assert not classes_in(artefact.manifest) - classes_in(original)
    assert PLAN_ONLY not in classes_in(artefact.manifest)
    # A revised pack goes back to the teacher, and the approval token moves so a
    # concurrent approve of the pre-revision manifest is rejected.
    assert artefact.review_status == ArtefactReviewStatus.PENDING
    assert artefact.version == 2


def test_recovery_keeps_practice_questions_and_their_answers() -> None:
    """Practice must survive the round trip, question and answer still paired.

    A revision turn recovers the stored manifest, revises, and writes it back in
    place. Practice that cannot be read back is therefore not merely missing
    from one render — it is deleted from the pack, and every later turn starts
    from a pack with no practice in it at all.
    """
    section = ReviewPackSection(
        section_id="step:s1",
        title="Rectangle area",
        lesson_objective_id="lop01",
        blocks=[
            ReviewPackBlock(
                block_id="b1",
                block_type="explanation",
                text="Multiply the two side lengths.",
                lesson_objective_id="lop01",
            )
        ],
        practice=[
            ReviewPackPracticeItem(
                item_id="p1",
                prompt="Find the area of a 5cm by 6cm rectangle.",
                answer="30 square cm",
            )
        ],
    )
    kwargs = {
        "artefact_id": "AT-1",
        "plan_version_id": "LPV-1",
        "scope": ArtefactScope.CLASS_LEVEL,
        "lesson_context": LessonContextForGeneration(
            subject="Mathematics", grade_level="JSS1", topic="Area", lesson_objectives=["lop01"]
        ),
        "created_at": _CREATED_AT,
    }
    first = sections_to_review_pack_manifest(sections=[section], **kwargs)
    recovered = _recover(first)

    assert [item.prompt for item in recovered[0].practice] == [
        "Find the area of a 5cm by 6cm rectangle."
    ]
    assert [item.answer for item in recovered[0].practice] == ["30 square cm"]
    # And a second render is byte-identical, so repeated turns are stable.
    assert sections_to_review_pack_manifest(sections=recovered, **kwargs) == first


def test_practice_items_without_ids_get_distinct_ones() -> None:
    """Three unstamped questions must not all answer to the same block id.

    Anything that addresses a block by id — a revision highlight, the editing
    reviser's unique-match premise, the rater UI's keys — cannot tell them apart
    otherwise. Generated sections are stamped upstream, so this bites the
    sections that reach the adapter without that pass: recovered older packs,
    composed sections, manually entered ones.
    """
    section = ReviewPackSection(
        section_id="step:s1",
        title="Rectangle area",
        lesson_objective_id="lop01",
        blocks=[],
        practice=[
            ReviewPackPracticeItem(prompt=f"Question {n}", answer=f"Answer {n}") for n in range(3)
        ],
    )
    manifest = sections_to_review_pack_manifest(
        sections=[section],
        artefact_id="AT-1",
        plan_version_id="LPV-1",
        scope=ArtefactScope.CLASS_LEVEL,
        lesson_context=LessonContextForGeneration(
            subject="Mathematics", grade_level="JSS1", topic="Area", lesson_objectives=["lop01"]
        ),
        created_at=_CREATED_AT,
    )
    ids = [block["id"] for block in manifest["steps"][0]["blocks"]]
    assert len(set(ids)) == len(ids), f"practice blocks share an id: {ids}"
    # And the identity survives recovery, so a second turn addresses the same items.
    assert [item.item_id for item in _recover(manifest)[0].practice] == ids
