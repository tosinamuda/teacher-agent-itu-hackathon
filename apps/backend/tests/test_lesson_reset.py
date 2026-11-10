"""Clearing a lesson removes what was made for it and keeps the rest."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
    PlanVersionObjective,
)
from app.domains.content_engine.infrastructure.models import ContentDraftRecord
from app.domains.experiments.infrastructure.models import Experiment
from app.domains.generation_log.models.generation_event import GenerationEvent
from app.domains.ops.application.lesson_reset import plan_reset, reset_lesson
from app.domains.teaching.models import LessonPeriod, SchemeOfWork

pytestmark = pytest.mark.asyncio


async def _lesson(db: AsyncSession, name: str) -> str:
    """A lesson with one approved plan that has one objective; its id as the database spells it."""
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    period, week, version = uuid.uuid4(), uuid.uuid4(), f"V-{name}"
    db.add_all(
        [
            SchemeOfWork(id=week, term_class_subject_id=uuid.uuid4(), week_number=1, title="W"),
            LessonPeriod(id=period, scheme_of_work_id=week, period_number=1),
            LessonPlan(
                plan_id=f"P-{name}",
                lesson_period_id=period,
                title=name,
                subject="Mathematics",
                track="General",
                grade="JSS1",
            ),
            PlanVersion(
                version_id=version,
                plan_id=f"P-{name}",
                source_type="generated",
                session_plan={},
                status=PlanVersionStatus.APPROVED,
            ),
            PlanVersionObjective(
                plan_version_id=version,
                lesson_objective_id="lo1",
                objective_text="Objective",
                objective_order=1,
            ),
        ]
    )
    await db.flush()
    return period.hex


async def _run(db: AsyncSession, function, *args):  # type: ignore[no-untyped-def]
    return await (await db.connection()).run_sync(lambda conn: function(conn, *args))


async def test_clearing_a_lesson_removes_its_plans_and_objectives_and_leaves_other_lessons(
    db: AsyncSession,
) -> None:
    mine, other = await _lesson(db, "mine"), await _lesson(db, "other")

    removed = await _run(db, reset_lesson, mine)

    assert removed["plan_versions"] == 1 and removed["plan_version_objectives"] == 1
    left = (await db.execute(select(PlanVersion.version_id))).scalars().all()
    assert left == ["V-other"]
    assert (await _run(db, plan_reset, other)).total == 3


async def test_a_lesson_the_study_ran_on_is_refused(db: AsyncSession) -> None:
    study = await _lesson(db, "study")
    db.add(
        Experiment(
            experiment_id="E-1",
            experiment_code="E-1",
            investigation_db_id=uuid.uuid4(),
            teacher_workspace_id=uuid.uuid4(),
            plan_version_id="V-study",
        )
    )
    await db.flush()

    plan = await _run(db, plan_reset, study)

    assert plan.blocked == ["the study ran on this lesson (experiments)"]
    with pytest.raises(ValueError, match="study"):
        await _run(db, reset_lesson, study)


async def test_clearing_a_lesson_takes_the_logged_model_calls_of_its_drafts_with_it(
    db: AsyncSession,
) -> None:
    mine, other = await _lesson(db, "mine"), await _lesson(db, "other")
    for name in ("mine", "other"):
        db.add_all(
            [
                ContentDraftRecord(
                    draft_id=f"DR-{name}",
                    plan_version_id=f"V-{name}",
                    type="slide-deck",
                    kind="slide_deck",
                    spec_revision=1,
                    unit="step",
                    units=[],
                    parts={},
                    status="submitted",
                    created_by="engine",
                ),
                GenerationEvent(kind="engine_content", model="m", correlation_id=f"DR-{name}"),
            ]
        )
    await db.flush()

    removed = await _run(db, reset_lesson, mine)

    assert removed["content_drafts"] == 1 and removed["generation_events"] == 1
    ours = GenerationEvent.correlation_id.in_(["DR-mine", "DR-other"])
    assert (
        await db.execute(select(GenerationEvent.correlation_id).where(ours))
    ).scalars().all() == ["DR-other"]
    assert (await _run(db, plan_reset, other)).counts["generation_events"] == 1
