"""One answer to "which is the lesson's revision pack", for its teacher and for its learners."""

from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    CURRENT_PIPELINE,
    ReviewPackPipeline,
    pipeline_that_wrote,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.lesson_pack import (
    the_lessons_class_pack,
)
from app.domains.assessments import jobs
from app.domains.content.domain.types import BuiltIn, Level
from app.domains.content.infrastructure.records import SqlAlchemyContentRecords
from app.domains.experiments.domain.types import ConditionRunStatus
from app.domains.experiments.infrastructure.models import ExperimentConditionRun
from migrations.data.content_registry_seed import seed_content_types

PLAN = "LPV-LCP"
_START = datetime(2026, 9, 1, tzinfo=timezone.utc)


def _pack(
    artefact_id: str,
    *,
    minutes: int,
    run: str | None = None,
    status: ArtefactReviewStatus = ArtefactReviewStatus.PENDING,
    student: str | None = None,
    pipeline: str | None = None,
) -> Artefact:
    return Artefact(
        artefact_id=artefact_id,
        artefact_type="post_class_review_pack",
        scope="learner_level" if student else "class_level",
        plan_version_id=PLAN,
        student_id=student,
        experiment_condition_run_id=run,
        manifest={"steps": []},
        artefact_refs={"pipeline": pipeline} if pipeline else None,
        review_status=status,
        created_at=_START + timedelta(minutes=minutes),
    )


async def _seed(db: AsyncSession, *rows: Artefact) -> None:
    await (await db.connection()).run_sync(seed_content_types)
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add_all(
        [
            ExperimentConditionRun(
                experiment_condition_run_id=f"ECR-{condition}",
                execution_db_id=uuid.uuid4(),
                hypothesis="H2" if condition.startswith("P") else "H1",
                condition_code=condition,
                status=ConditionRunStatus.SUCCEEDED,
            )
            for condition in ("C0", "C4", "P1")
        ]
    )
    db.add_all(rows)
    await db.flush()


@pytest.mark.asyncio
async def test_an_experiment_lessons_class_pack_is_c4s_even_beside_a_newer_freestanding_one(
    db: AsyncSession,
) -> None:
    await _seed(
        db,
        _pack("AT-c0", minutes=0, run="ECR-C0", status=ArtefactReviewStatus.APPROVED),
        _pack("AT-c4", minutes=1, run="ECR-C4"),
        _pack("AT-free", minutes=2),
        _pack("AT-p1", minutes=3, run="ECR-P1", student="ST-1"),
        _pack("AT-learner", minutes=4, student="ST-1"),
    )

    packs = await SqlAlchemyContentRecords().find(
        db, plan_version_id=PLAN, type=BuiltIn.REVISION_NOTE.value, level=None, student_id=None
    )

    class_pack = await the_lessons_class_pack(db, PLAN)
    assert class_pack is not None and class_pack.artefact_id == "AT-c4"
    assert {(m.content_id, m.level) for m in packs} == {
        ("AT-c4", Level.CLASS),
        ("AT-learner", Level.LEARNER),
    }


@pytest.mark.asyncio
async def test_a_lesson_without_the_experiment_uses_its_own_pack_preferring_the_approved(
    db: AsyncSession,
) -> None:
    await _seed(
        db,
        _pack("AT-approved", minutes=0, status=ArtefactReviewStatus.APPROVED),
        _pack("AT-newer", minutes=1),
    )

    class_pack = await the_lessons_class_pack(db, PLAN)
    assert class_pack is not None and class_pack.artefact_id == "AT-approved"


def test_a_pack_that_records_no_pipeline_counts_as_the_latest() -> None:
    assert pipeline_that_wrote({"pipeline": "2026-08-25"}) is ReviewPackPipeline.V2026_08_25
    assert pipeline_that_wrote({"specification": {}}) is CURRENT_PIPELINE
    assert pipeline_that_wrote(None) is CURRENT_PIPELINE


@pytest.mark.asyncio
async def test_a_learners_pack_is_written_by_the_version_that_wrote_its_class_pack(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    await _seed(
        db,
        _pack(
            "AT-c4",
            minutes=0,
            run="ECR-C4",
            pipeline="2026-08-25",
            status=ArtefactReviewStatus.APPROVED,
        ),
    )
    built_with: list[ReviewPackPipeline] = []

    class _Jobs:
        async def claim(self, db, generation_id):  # type: ignore[no-untyped-def]
            return SimpleNamespace(student_id="ST-1", plan_version_id=PLAN)

        async def finalize(self, db, generation_id, **_):  # type: ignore[no-untyped-def]
            return None

    class _Packs:
        async def generate_for_student(self, **_):  # type: ignore[no-untyped-def]
            return SimpleNamespace(artefact_id="AT-made")

    def _build(pipeline: ReviewPackPipeline) -> _Packs:
        built_with.append(pipeline)
        return _Packs()

    @asynccontextmanager
    async def _session():  # type: ignore[no-untyped-def]
        yield db

    monkeypatch.setattr(jobs, "AsyncSessionLocal", _session)
    monkeypatch.setattr(jobs, "build_generation_job_service", _Jobs)
    monkeypatch.setattr(jobs, "build_student_pack_service", _build)

    await jobs.generate_student_pack("GEN-1")

    assert built_with == [ReviewPackPipeline.V2026_08_25]
