"""A lesson note is copied onto another plan that has the same steps."""

from __future__ import annotations

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.lesson_note.infrastructure.repository import SqlAlchemyLessonNotes
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.content.application.errors import ContentError
from app.domains.content.application.note_reuse import NoteReuse
from app.domains.content.infrastructure.records import SqlAlchemyContentRecords
from tests.content_engine_support import PLAN, SESSION_PLAN, seed_lesson

pytestmark = pytest.mark.asyncio

NEW_PLAN = "LPV-REUSE-1"
SOURCE = "AT-NOTE-1"


def _reuse() -> NoteReuse:
    return NoteReuse(SqlAlchemyLessonNotes(), SqlAlchemyContentRecords())


async def _lesson_with_a_second_plan(db: AsyncSession, *, covers_every_step: bool = True) -> None:
    await seed_lesson(db)
    note = await SqlAlchemyLessonNotes().get(db, SOURCE)
    assert note is not None
    sections = [{"step_id": "s1", "body": "Keep the denominator."}]
    if covers_every_step:
        sections.append({"step_id": "s2", "body": "Add the numerators."})
    note.manifest = {**note.manifest, "sections": sections}
    note.artefact_refs = {
        "origin": "teacher",
        "specification": {"kind": "lesson_note", "revision": 1},
    }
    db.add(
        PlanVersion(
            version_id=NEW_PLAN,
            plan_id="P-REUSE-1",
            source_type="experiment_reused",
            session_plan=SESSION_PLAN,
            status=PlanVersionStatus.APPROVED,
        )
    )
    await db.flush()


async def test_the_note_is_copied_in_the_plans_step_order_and_waits_for_review(
    db: AsyncSession,
) -> None:
    await _lesson_with_a_second_plan(db)

    copied = await _reuse()(db, source_id=SOURCE, plan_version_id=NEW_PLAN)

    stored = await SqlAlchemyLessonNotes().get(db, copied)
    assert stored is not None
    assert stored.plan_version_id == NEW_PLAN
    assert stored.review_status.value == "pending"
    assert [(s["step_id"], s["body"]) for s in stored.manifest["sections"]] == [
        ("s1", "Keep the denominator."),
        ("s2", "Add the numerators."),
    ]
    assert (stored.artefact_refs or {})["origin"] == "reused"
    assert (stored.artefact_refs or {})["reused_from"] == SOURCE
    assert (stored.artefact_refs or {})["specification"] == {"kind": "lesson_note", "revision": 1}


async def test_a_note_that_lacks_a_section_for_a_step_is_refused_naming_the_step(
    db: AsyncSession,
) -> None:
    await _lesson_with_a_second_plan(db, covers_every_step=False)

    with pytest.raises(ContentError) as refused:
        await _reuse()(db, source_id=SOURCE, plan_version_id=NEW_PLAN)

    assert (refused.value.status_code, refused.value.detail) == (
        422,
        "the_note_has_no_section_for:s2",
    )


async def test_a_plan_that_already_has_a_note_is_refused(db: AsyncSession) -> None:
    await _lesson_with_a_second_plan(db)

    with pytest.raises(ContentError) as refused:
        await _reuse()(db, source_id=SOURCE, plan_version_id=PLAN)

    assert (refused.value.status_code, refused.value.detail) == (
        409,
        "the_plan_already_has_a_lesson_note",
    )


async def test_a_note_or_a_plan_that_does_not_exist_is_not_found(db: AsyncSession) -> None:
    await _lesson_with_a_second_plan(db)

    with pytest.raises(ContentError) as no_note:
        await _reuse()(db, source_id="AT-NOPE", plan_version_id=NEW_PLAN)
    with pytest.raises(ContentError) as no_plan:
        await _reuse()(db, source_id=SOURCE, plan_version_id="LPV-NOPE")

    assert no_note.value.detail == "source_note_not_found"
    assert no_plan.value.detail == "plan_version_not_found"


async def test_a_plan_that_is_not_approved_is_refused(db: AsyncSession) -> None:
    await _lesson_with_a_second_plan(db)
    draft = await db.get(PlanVersion, await _id_of(db, NEW_PLAN))
    assert draft is not None
    draft.status = PlanVersionStatus.DRAFT
    await db.flush()

    with pytest.raises(ContentError) as refused:
        await _reuse()(db, source_id=SOURCE, plan_version_id=NEW_PLAN)

    assert refused.value.status_code == 409


async def _id_of(db: AsyncSession, version_id: str):  # type: ignore[no-untyped-def]
    from sqlalchemy import select

    return (
        await db.execute(select(PlanVersion.id).where(PlanVersion.version_id == version_id))
    ).scalar_one()


async def test_a_note_may_leave_out_the_plans_evaluation_step(db: AsyncSession) -> None:
    await _lesson_with_a_second_plan(db, covers_every_step=False)
    plan = await db.get(PlanVersion, await _plan_row(db, NEW_PLAN))
    assert plan is not None
    steps = [dict(step) for step in plan.session_plan["steps"]]
    steps[1]["step_kind"] = "evaluation"
    plan.session_plan = {**plan.session_plan, "steps": steps}
    await db.flush()

    copied = await _reuse()(db, source_id=SOURCE, plan_version_id=NEW_PLAN)

    stored = await SqlAlchemyLessonNotes().get(db, copied)
    assert stored is not None
    assert [s["step_id"] for s in stored.manifest["sections"]] == ["s1"]


async def _plan_row(db: AsyncSession, version_id: str):  # type: ignore[no-untyped-def]
    row = await db.scalar(select(PlanVersion.id).where(PlanVersion.version_id == version_id))
    assert row is not None
    return row
