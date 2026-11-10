"""A teacher can clear what was made for a lesson, but never the study's lesson."""

from __future__ import annotations

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.assessments.models import StudyClassworkScript
from app.domains.teaching.application.lesson_start_over import LessonStartOver
from app.domains.teaching.application.sequence_service import TeachingSequenceApplicationError
from app.domains.teaching.application.study_results_service import StudyResultsService
from tests.test_study_results_import import STUDY, _seed

pytestmark = pytest.mark.asyncio


async def test_clearing_a_lesson_removes_what_was_made_for_it_and_leaves_the_studys_lesson(
    db: AsyncSession,
) -> None:
    workspace, target_period, _ = await _seed(db)
    await StudyResultsService().import_results(db, workspace, target_period, STUDY)

    preview = await LessonStartOver().preview(db, workspace, target_period)
    removed = await LessonStartOver().clear(db, workspace, target_period)

    assert preview.counts["plan_versions"] == 1 and not preview.blocked
    assert removed["plan_versions"] == 1 and removed["study_classwork_scripts"] == 2
    versions = set((await db.execute(select(PlanVersion.version_id))).scalars())
    assert versions == {STUDY}
    scripts = set((await db.execute(select(StudyClassworkScript.plan_version_id))).scalars())
    assert scripts == {STUDY}


async def test_a_lesson_the_study_ran_on_cannot_be_cleared(db: AsyncSession) -> None:
    workspace, _, study_period = await _seed(db)

    preview = await LessonStartOver().preview(db, workspace, study_period)
    with pytest.raises(TeachingSequenceApplicationError) as refused:
        await LessonStartOver().clear(db, workspace, study_period)

    assert preview.blocked and refused.value.status_code == 409
