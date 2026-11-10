"""A concluded study's record is read-only: nothing that belongs to its lessons changes."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.concluded_record import is_concluded
from app.domains.artefact_revision.application.errors import ArtefactRevisionError
from app.domains.artefact_revision.application.service import ArtefactRevisionService
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.content.application.errors import ContentError
from app.domains.content.application.generation import GenerationChoices
from app.domains.content.domain.types import BuiltIn, Level
from app.domains.content.infrastructure.records import SqlAlchemyContentRecords
from app.domains.content.infrastructure.wiring import build_content_service
from app.domains.evaluation.infrastructure.models import (
    EvaluationPacket,
    EvaluationRating,
    RaterAssignment,
)
from app.domains.experiments.domain.types import ExecutionStatus, ExperimentLifecycleStatus
from app.domains.experiments.infrastructure.lesson_conclusions import (
    SqlAlchemyLessonConclusions,
)
from app.domains.experiments.infrastructure.models import Experiment, ExperimentExecution
from app.shared.concluded import ConcludedLessonError
from app.shared.experiment_enums import PacketStatus
from migrations.data.content_registry_seed import seed_content_generators, seed_content_types

CONCLUDED, OPEN = "LPV-CONCLUDED", "LPV-OPEN"


def _version(version_id: str, plan_id: str, *, concluded: bool = False) -> PlanVersion:
    return PlanVersion(
        version_id=version_id,
        plan_id=plan_id,
        source_type="study_record",
        session_plan={"lesson_plan_objectives": []},
        status=PlanVersionStatus.APPROVED,
        concluded_at=datetime(2026, 9, 1, tzinfo=timezone.utc) if concluded else None,
    )


def _artefact(artefact_id: str, plan_version_id: str) -> Artefact:
    return Artefact(
        artefact_id=artefact_id,
        artefact_type="lesson_note",
        scope="class_level",
        plan_version_id=plan_version_id,
        manifest={"sections": []},
        review_status=ArtefactReviewStatus.PENDING,
    )


async def _seed(db: AsyncSession) -> None:
    await (await db.connection()).run_sync(seed_content_types)
    await (await db.connection()).run_sync(seed_content_generators)
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add_all(
        [
            _version(CONCLUDED, "P-CONCLUDED", concluded=True),
            _version(OPEN, "P-OPEN"),
            _artefact("AT-concluded", CONCLUDED),
            _artefact("AT-open", OPEN),
        ]
    )
    await db.flush()


async def _artefact_row(db: AsyncSession, artefact_id: str) -> Artefact:
    return (
        await db.execute(select(Artefact).where(Artefact.artefact_id == artefact_id))
    ).scalar_one()


@pytest.mark.asyncio
async def test_nothing_of_a_concluded_lesson_is_changed_added_or_removed(db) -> None:  # type: ignore[no-untyped-def]
    await _seed(db)

    (await _artefact_row(db, "AT-concluded")).manifest = {"sections": [{"step_id": "s1"}]}
    with pytest.raises(ConcludedLessonError):
        await db.flush()
    await db.rollback()

    await _seed(db)
    db.add(_artefact("AT-new", CONCLUDED))
    with pytest.raises(ConcludedLessonError):
        await db.flush()
    await db.rollback()

    await _seed(db)
    db.add(_version("LPV-CONCLUDED-2", "P-CONCLUDED"))
    with pytest.raises(ConcludedLessonError):
        await db.flush()


@pytest.mark.asyncio
async def test_an_open_lesson_is_untouched_and_a_lesson_can_be_concluded(db) -> None:  # type: ignore[no-untyped-def]
    await _seed(db)

    (await _artefact_row(db, "AT-open")).manifest = {"sections": [{"step_id": "s1"}]}
    open_version = (
        await db.execute(select(PlanVersion).where(PlanVersion.version_id == OPEN))
    ).scalar_one()
    open_version.concluded_at = datetime(2026, 9, 2, tzinfo=timezone.utc)
    await db.flush()

    assert await is_concluded(db, OPEN)


@pytest.mark.asyncio
async def test_a_plan_its_versions_and_its_content_all_answer_as_concluded(db) -> None:  # type: ignore[no-untyped-def]
    await _seed(db)

    assert [await is_concluded(db, s) for s in (CONCLUDED, "P-CONCLUDED", "AT-concluded")] == [
        True,
        True,
        True,
    ]
    assert [await is_concluded(db, s) for s in (OPEN, "P-OPEN", "AT-open")] == [
        False,
        False,
        False,
    ]


@pytest.mark.asyncio
async def test_content_of_a_concluded_lesson_is_refused_before_any_work(db) -> None:  # type: ignore[no-untyped-def]
    await _seed(db)
    service = build_content_service()

    with pytest.raises(ContentError) as generating:
        await service.generate(
            db,
            plan_version_id=CONCLUDED,
            type=BuiltIn.LESSON_NOTE.value,
            level=Level.CLASS,
            choices=GenerationChoices(),
        )
    with pytest.raises(ContentError) as approving:
        await service.approve(
            db, content_id="AT-concluded", expected_version=1, approved_by="Teacher"
        )
    with pytest.raises(ContentError) as revising:
        await service.revise(db, content_id="AT-concluded", feedback="x", requested_by="T")

    assert {error.value.status_code for error in (generating, approving, revising)} == {409}
    assert await SqlAlchemyContentRecords().concluded(db, CONCLUDED)


@pytest.mark.asyncio
async def test_a_revision_of_a_concluded_lesson_is_refused_before_the_model_is_asked(db) -> None:  # type: ignore[no-untyped-def]
    await _seed(db)

    class _NeverCalled:
        artefact_type = "lesson_note"

        async def revise(self, **_: object) -> None:
            raise AssertionError("the model was asked")

        async def current_artefact(self, **_: object) -> tuple[None, None]:
            return None, None

    service = ArtefactRevisionService((_NeverCalled(),))  # type: ignore[arg-type]
    thread = await service.get_or_create_thread(
        db=db, artefact_type="lesson_note", subject_id="AT-concluded", created_by="T"
    )

    with pytest.raises(ArtefactRevisionError) as refused:
        await service.submit_turn(
            db=db, thread_id=thread.revision_thread_id, instruction="x", highlight=None
        )
    assert refused.value.status_code == 409


def _experiment(plan_version_id: str, status: ExperimentLifecycleStatus) -> Experiment:
    return Experiment(
        id=uuid.uuid4(),
        experiment_id=f"EXP-{uuid.uuid4().hex[:8]}",
        experiment_code=f"C-{uuid.uuid4().hex[:8]}",
        investigation_db_id=uuid.uuid4(),
        teacher_workspace_id=uuid.uuid4(),
        plan_version_id=plan_version_id,
        lifecycle_status=status,
    )


@pytest.mark.asyncio
async def test_a_lesson_concludes_when_no_experiment_on_it_is_still_active(db) -> None:  # type: ignore[no-untyped-def]
    await _seed(db)
    db.add_all(
        [
            _version("LPV-SHARED", "P-SHARED"),
            _experiment(OPEN, ExperimentLifecycleStatus.ENDED),
            _experiment("LPV-SHARED", ExperimentLifecycleStatus.ENDED),
            _experiment("LPV-SHARED", ExperimentLifecycleStatus.ACTIVE),
        ]
    )
    await db.flush()

    await SqlAlchemyLessonConclusions(db).conclude_where_no_experiment_is_active(
        [OPEN, "LPV-SHARED"]
    )
    await db.flush()

    assert await is_concluded(db, OPEN)
    assert not await is_concluded(db, "LPV-SHARED")


async def _ended_experiment_on(db: AsyncSession, plan_version_id: str) -> Experiment:
    """An ended experiment on the lesson, written before the lesson concluded."""
    experiment = _experiment(plan_version_id, ExperimentLifecycleStatus.ENDED)
    db.add(experiment)
    await db.flush()
    await SqlAlchemyLessonConclusions(db).conclude_where_no_experiment_is_active([plan_version_id])
    await db.flush()
    return experiment


def _assignment(experiment: Experiment) -> RaterAssignment:
    return RaterAssignment(
        assignment_id=f"RA-{uuid.uuid4().hex[:8]}",
        experiment_db_id=experiment.id,
        rater_db_id=uuid.uuid4(),
        hypothesis="H2",
        scope_id="EFC-1",
    )


@pytest.mark.asyncio
async def test_an_experiment_on_a_concluded_lesson_takes_no_raters_runs_or_learners(db) -> None:  # type: ignore[no-untyped-def]
    for change in ("assign a rater", "run it again", "pick its learners"):
        await _seed(db)
        experiment = await _ended_experiment_on(db, OPEN)
        if change == "assign a rater":
            db.add(_assignment(experiment))
        elif change == "run it again":
            db.add(
                ExperimentExecution(
                    execution_id=f"EX-{uuid.uuid4().hex[:8]}",
                    experiment_db_id=experiment.id,
                    hypothesis="H2",
                    attempt_number=2,
                )
            )
        else:
            experiment.focal_learner_ids = ["ST-1"]
        with pytest.raises(ConcludedLessonError):
            await db.flush()
        await db.rollback()


@pytest.mark.asyncio
async def test_a_concluded_lessons_packets_take_no_new_ratings(db) -> None:  # type: ignore[no-untyped-def]
    await _seed(db)
    experiment = _experiment(OPEN, ExperimentLifecycleStatus.ENDED)
    execution = ExperimentExecution(
        execution_id="EX-rated",
        experiment_db_id=experiment.id,
        hypothesis="H1",
        attempt_number=1,
        status=ExecutionStatus.SUCCEEDED,
    )
    db.add_all([experiment, execution])
    await db.flush()
    packet = EvaluationPacket(
        evaluation_packet_id="EP-rated",
        execution_db_id=execution.id,
        packet_code="PKT-rated",
        hypothesis="H1",
        status=PacketStatus.READY,
        primary_condition_run_id="ECR-1",
        condition_run_ids=["ECR-1"],
    )
    db.add(packet)
    await db.flush()
    await SqlAlchemyLessonConclusions(db).conclude_where_no_experiment_is_active([OPEN])
    await db.flush()

    db.add(
        EvaluationRating(
            rating_id="RT-offline",
            evaluation_packet_db_id=packet.id,
            rater_db_id=uuid.uuid4(),
            hypothesis="H1",
            overall_score=4.0,
            rubric_scores={},
        )
    )
    with pytest.raises(ConcludedLessonError):
        await db.flush()


@pytest.mark.asyncio
async def test_an_open_lesson_takes_raters_and_an_ended_experiment_stays_ended(db) -> None:  # type: ignore[no-untyped-def]
    await _seed(db)
    db.add(_version("LPV-ACTIVE", "P-ACTIVE"))
    active = _experiment("LPV-ACTIVE", ExperimentLifecycleStatus.ACTIVE)
    db.add(active)
    await db.flush()
    db.add(_assignment(active))
    await db.flush()

    concluded = await _ended_experiment_on(db, OPEN)
    concluded.ended_by = "researcher"
    await db.flush()


@pytest.mark.asyncio
async def test_content_of_a_concluded_lesson_says_it_is_read_only(db) -> None:  # type: ignore[no-untyped-def]
    await _seed(db)
    records = SqlAlchemyContentRecords()

    concluded, open_ = await records.get(db, "AT-concluded"), await records.get(db, "AT-open")
    plan = await records.get(db, "P-CONCLUDED")

    assert (concluded.read_only, open_.read_only, plan.read_only) == (True, False, True)  # type: ignore[union-attr]


def test_a_write_that_reaches_a_concluded_lesson_answers_409() -> None:
    import asyncio

    from app.main import app

    handler = app.exception_handlers[ConcludedLessonError]
    response = asyncio.run(handler(None, ConcludedLessonError()))  # type: ignore[arg-type]

    assert (response.status_code, response.body) == (
        409,
        b'{"detail":"concluded_lesson_is_read_only"}',
    )
