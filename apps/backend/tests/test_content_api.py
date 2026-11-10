"""Content of every type through one interface: find, read, generate, revise, approve."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from fastapi.routing import APIRoute
from sqlalchemy import select, text

from app.domains.artefact_revision.application.service import RevisionRecord
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.core.infrastructure.repository import ArtefactRepository
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.content.application.errors import ContentError
from app.domains.content.application.generation import GenerationChoices
from app.domains.content.application.kinds import ArtefactContent
from app.domains.content.application.service import ContentService
from app.domains.content.domain.types import BuiltIn, Level
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.records import SqlAlchemyContentRecords
from app.domains.content.infrastructure.review import LifecycleApprover
from app.domains.content.infrastructure.wiring import content_kinds
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.domains.experiments.domain.types import ExperimentLifecycleStatus
from app.domains.experiments.infrastructure.models import Experiment
from migrations.data.content_registry_seed import (
    seed_content_generators,
    seed_content_registry,
    seed_content_types,
)

PLAN = "LPV-M1"


class _Generator:
    def __init__(self, content_id: str) -> None:
        self.content_id = content_id
        self.calls: list[tuple[str, Level, GenerationChoices]] = []

    def check(self, level: Level, choices: GenerationChoices) -> None:
        """Every level and choice is one this fake makes."""

    async def generate(
        self, db, *, plan_version_id: str, type: str, level: Level, choices: GenerationChoices
    ) -> str:  # type: ignore[no-untyped-def]
        self.calls.append((plan_version_id, level, choices))
        return self.content_id


class _Revisions:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    async def revise(
        self, db, *, stored_type, subject_id, feedback, requested_by, highlight=None, chat_id=None
    ) -> RevisionRecord:  # type: ignore[no-untyped-def]
        self.calls.append((stored_type, subject_id))
        return RevisionRecord(1, feedback, "Changed it.", None, datetime.now(timezone.utc))

    async def history(self, db, *, stored_type, subject_id) -> list[RevisionRecord]:  # type: ignore[no-untyped-def]
        return []


def _service(
    revisions: _Revisions | None = None, generator: _Generator | None = None
) -> ContentService:
    generator = generator or _Generator("AT-pack")
    records = SqlAlchemyContentRecords()
    return ContentService(
        catalogue=build_content_catalogue(),
        records=records,
        kinds=content_kinds(records),
        generators={t.value: generator for t in BuiltIn if t is not BuiltIn.LESSON_PLAN},
        engine_kind=ArtefactContent(LifecycleApprover(), ArtefactRepository()),
        engine_generator=generator,
        revisions=revisions or _Revisions(),
    )


def _artefact(
    artefact_id: str, kind: str, *, scope: str = "class_level", student: str | None = None
) -> Artefact:
    return Artefact(
        artefact_id=artefact_id,
        artefact_type=kind,
        scope=scope,
        plan_version_id=PLAN,
        student_id=student,
        manifest={"steps": []},
        artefact_refs={"specification": {"kind": kind, "revision": 1}, "pipeline": "2026-08-25"},
        review_status=ArtefactReviewStatus.PENDING,
    )


async def _seed(db) -> None:  # type: ignore[no-untyped-def]
    await (await db.connection()).run_sync(seed_content_types)
    await (await db.connection()).run_sync(seed_content_generators)
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add_all(
        [
            PlanVersion(
                version_id=PLAN,
                plan_id="P-M1",
                source_type="experiment_manual",
                session_plan={"lesson_plan_objectives": []},
                status=PlanVersionStatus.APPROVED,
            ),
            _artefact("AT-pack", "post_class_review_pack"),
            _artefact(
                "AT-learner", "post_class_review_pack", scope="learner_level", student="ST-1"
            ),
            _artefact("AT-test", "diagnostic"),
            _artefact("AT-note", "lesson_note"),
            _artefact("AT-plan", "lesson_plan"),
            ExitTicketItem(
                subtopic_id="sub",
                plan_version_id=PLAN,
                lesson_objective_id="lop01",
                stem="2 + 3 × 4 = ?",
                correct_option="B",
                options={"A": "20", "B": "14", "C": "24", "D": "9"},
                difficulty="easy",
            ),
        ]
    )
    await db.flush()


def test_types_is_routed_before_a_content_id() -> None:
    from app.main import app

    paths = [route.path for route in app.routes if isinstance(route, APIRoute)]
    assert paths.index("/content/types") < paths.index("/content/{content_id}")
    assert "/materials" not in paths


@pytest.mark.asyncio
async def test_find_returns_content_only_and_filters_by_type_level_and_learner(db) -> None:
    await _seed(db)
    service = _service()

    everything = {r.content_id for r in await service.find(db, plan_version_id=PLAN)}
    packs = await service.find(db, plan_version_id=PLAN, type=BuiltIn.REVISION_NOTE.value)
    learners = await service.find(db, plan_version_id=PLAN, level=Level.LEARNER, student_id="ST-1")

    assert everything == {"AT-pack", "AT-learner", "AT-test", "AT-note", "P-M1"}
    assert {r.content_id for r in packs} == {"AT-pack", "AT-learner"}
    assert [r.content_id for r in learners] == ["AT-learner"]
    assert packs[0].provenance == {
        "specification": {"kind": "post_class_review_pack", "revision": 1},
        "pipeline": "2026-08-25",
    }
    with pytest.raises(ContentError) as not_content:
        await service.get(db, "AT-plan")
    assert not_content.value.status_code == 404


@pytest.mark.asyncio
async def test_a_class_tests_content_is_its_questions(db) -> None:
    await _seed(db)

    item = await _service().get(db, "AT-test")

    assert item.record.type == BuiltIn.CLASS_TEST.value
    assert [item["stem"] for item in item.content["items"]] == ["2 + 3 × 4 = ?"]


@pytest.mark.asyncio
async def test_generation_goes_to_the_types_generator_with_the_revision_notes_choices(db) -> None:
    await _seed(db)
    generator = _Generator("AT-pack")
    service = _service(generator=generator)
    choices = GenerationChoices(pipeline="2026-08-25", sources="textbook")

    made = await service.generate(
        db,
        plan_version_id=PLAN,
        type=BuiltIn.REVISION_NOTE.value,
        level=Level.CLASS,
        choices=choices,
    )

    assert made.record.content_id == "AT-pack"
    assert made.record.provenance["generator"] == {
        "harness": "dspy-pipeline",
        "schema": "code",
        "ref": "2026-08-25",
    }
    assert generator.calls == [(PLAN, Level.CLASS, choices)]
    for choice in (GenerationChoices(pipeline="2026-08-25"), GenerationChoices(sources="both")):
        with pytest.raises(ContentError) as not_a_revision_note:
            await service.generate(
                db,
                plan_version_id=PLAN,
                type=BuiltIn.CLASS_TEST.value,
                level=Level.CLASS,
                choices=choice,
            )
        assert not_a_revision_note.value.status_code == 422


async def _experiment_on_the_lesson(db, status: ExperimentLifecycleStatus) -> None:  # type: ignore[no-untyped-def]
    db.add(
        Experiment(
            id=uuid.uuid4(),
            experiment_id=f"EXP-{uuid.uuid4().hex[:8]}",
            experiment_code=f"CONTENT-{uuid.uuid4().hex[:8]}",
            investigation_db_id=uuid.uuid4(),
            teacher_workspace_id=uuid.uuid4(),
            plan_version_id=PLAN,
            lifecycle_status=status,
        )
    )
    await db.flush()


async def _generate_class_note(db, service: ContentService):  # type: ignore[no-untyped-def]
    return await service.generate(
        db,
        plan_version_id=PLAN,
        type=BuiltIn.REVISION_NOTE.value,
        level=Level.CLASS,
        choices=GenerationChoices(),
    )


@pytest.mark.asyncio
async def test_a_running_experiment_s_lesson_gets_its_class_note_from_the_experiment(db) -> None:
    await _seed(db)
    await db.execute(text("DELETE FROM artefacts WHERE artefact_id = 'AT-pack'"))
    await _experiment_on_the_lesson(db, ExperimentLifecycleStatus.ACTIVE)
    generator = _Generator("AT-pack")

    with pytest.raises(ContentError) as refused:
        await _generate_class_note(db, _service(generator=generator))

    assert (refused.value.status_code, refused.value.detail) == (
        409,
        "class_revision_note_is_made_by_the_lessons_experiment",
    )
    assert generator.calls == []


@pytest.mark.asyncio
async def test_a_lesson_s_existing_class_note_or_ended_experiment_leaves_generation_open(
    db,
) -> None:
    await _seed(db)
    await _experiment_on_the_lesson(db, ExperimentLifecycleStatus.ACTIVE)

    existing = await _generate_class_note(db, _service())

    await db.execute(text("DELETE FROM artefacts WHERE artefact_id = 'AT-pack'"))
    await db.execute(text("UPDATE experiments SET lifecycle_status = 'ended'"))
    after_the_study = await _generate_class_note(db, _service(generator=_Generator("AT-learner")))

    assert existing.record.content_id == "AT-pack"
    assert after_the_study.record.content_id == "AT-learner"


@pytest.mark.asyncio
async def test_approving_keeps_the_approval_and_sends_a_class_test_to_students(db) -> None:
    await _seed(db)
    service = _service()

    await service.approve(db, content_id="AT-note", expected_version=1, approved_by="Teacher One")
    await service.approve(db, content_id="AT-test", expected_version=1, approved_by="Teacher One")

    note_approvals = await service.approvals(db, "AT-note")
    assert [(a.approved_version, a.approved_by) for a in note_approvals] == [(1, "Teacher One")]
    released = (
        await db.execute(
            select(PlanVersion.assessment_released_by).where(PlanVersion.version_id == PLAN)
        )
    ).scalar_one()
    assert released == "Teacher One"


@pytest.mark.asyncio
async def test_a_pending_note_is_rejected_with_the_teachers_reason(db) -> None:
    await _seed(db)
    service = _service()

    rejected = await service.reject(
        db, content_id="AT-note", expected_version=1, rejected_by="Teacher One", reason="Too thin."
    )

    assert (rejected.record.review_status, rejected.record.review_reason) == (
        "rejected",
        "Too thin.",
    )
    with pytest.raises(ContentError) as again:
        await service.reject(
            db, content_id="AT-note", expected_version=1, rejected_by="T", reason="Again."
        )
    assert (again.value.status_code, again.value.detail) == (409, "artefact_already_rejected")


@pytest.mark.asyncio
async def test_a_rejection_of_a_version_the_teacher_did_not_review_is_refused(db) -> None:
    await _seed(db)

    with pytest.raises(ContentError) as stale:
        await _service().reject(
            db, content_id="AT-note", expected_version=7, rejected_by="T", reason="No."
        )

    assert (stale.value.status_code, stale.value.detail) == (409, "artefact_changed")


@pytest.mark.asyncio
async def test_withdrawing_the_class_revision_note_withdraws_the_learner_notes_made_from_it(
    db,
) -> None:
    await _seed(db)
    service = _service()
    await service.approve(db, content_id="AT-pack", expected_version=1, approved_by="Teacher One")

    await service.reject(
        db,
        content_id="AT-pack",
        expected_version=1,
        rejected_by="Teacher One",
        reason="Wrong rule.",
    )

    learner = await service.record(db, "AT-learner")
    assert learner.review_status == "rejected"
    assert learner.review_reason == "The class revision note was withdrawn: Wrong rule."


@pytest.mark.asyncio
async def test_rejecting_a_pending_class_note_leaves_the_learner_notes_alone(db) -> None:
    await _seed(db)
    service = _service()

    await service.reject(
        db, content_id="AT-pack", expected_version=1, rejected_by="Teacher One", reason="Redo it."
    )

    assert (await service.record(db, "AT-learner")).review_status == "pending"


@pytest.mark.asyncio
async def test_a_class_test_sent_to_students_is_not_withdrawn(db) -> None:
    await _seed(db)
    service = _service()
    await service.approve(db, content_id="AT-test", expected_version=1, approved_by="Teacher One")

    with pytest.raises(ContentError) as sent:
        await service.reject(
            db, content_id="AT-test", expected_version=1, rejected_by="T", reason="Oops."
        )

    assert sent.value.detail == "class_test_already_sent_to_students"


@pytest.mark.asyncio
async def test_a_class_test_is_revised_by_its_plan_version_and_becomes_a_new_version(db) -> None:
    await _seed(db)
    revisions = _Revisions()
    service = _service(revisions=revisions)

    await service.revise(db, content_id="AT-test", feedback="Harder numbers.", requested_by="T")
    await service.revise(db, content_id="AT-note", feedback="Shorter.", requested_by="T")

    assert revisions.calls == [("diagnostic", PLAN), ("lesson_note", "AT-note")]
    revised = await service.record(db, "AT-test")
    assert (revised.version, revised.review_status) == (2, "pending")


@pytest.mark.asyncio
async def test_a_class_test_already_sent_to_students_is_not_revised(db) -> None:
    await _seed(db)
    service = _service()
    await service.approve(db, content_id="AT-test", expected_version=1, approved_by="Teacher One")

    with pytest.raises(ContentError) as sent:
        await service.revise(db, content_id="AT-test", feedback="Change it.", requested_by="T")
    assert sent.value.status_code == 409


@pytest.mark.asyncio
async def test_a_spec_revision_is_added_as_the_next_and_an_invalid_one_is_refused(db) -> None:
    connection = await db.connection()
    await connection.run_sync(seed_content_registry)
    catalogue = build_content_catalogue()
    current = await catalogue.current(db, BuiltIn.LESSON_NOTE.value)

    added = await catalogue.add(
        db,
        BuiltIn.LESSON_NOTE.value,
        {**current.to_record(), "requirements": ["Keep it to one page per step."]},
        "Researcher",
    )

    assert added.revision == 2
    assert (await catalogue.current(db, BuiltIn.LESSON_NOTE.value)).revision == 2
    assert [spec.revision for spec in await catalogue.history(db, BuiltIn.LESSON_NOTE.value)] == [
        1,
        2,
    ]
    assert [t.slug for t, _ in await catalogue.types(db)] == [
        *(t.value for t in BuiltIn),
        "exam-questions",
    ]
    with pytest.raises(ContentError) as invalid:
        await catalogue.add(
            db,
            BuiltIn.LESSON_NOTE.value,
            {**current.to_record(), "levels": ["class_level", "learner_level"], "adaptable": []},
            "Researcher",
        )
    assert invalid.value.status_code == 422


@pytest.mark.asyncio
async def test_research_condition_runs_are_not_a_lessons_content_but_c4_is(db) -> None:
    import uuid

    from app.domains.experiments.domain.types import ConditionRunStatus
    from app.domains.experiments.infrastructure.models import ExperimentConditionRun

    await _seed(db)
    for run_id, condition in (("ECR-c0", "C0"), ("ECR-c4", "C4")):
        db.add(
            ExperimentConditionRun(
                experiment_condition_run_id=run_id,
                execution_db_id=uuid.uuid4(),
                hypothesis="H1",
                condition_code=condition,
                status=ConditionRunStatus.SUCCEEDED,
            )
        )
    research = _artefact("AT-c0", "post_class_review_pack")
    research.experiment_condition_run_id = "ECR-c0"
    reviewed = _artefact("AT-c4", "post_class_review_pack")
    reviewed.experiment_condition_run_id = "ECR-c4"
    db.add_all([research, reviewed])
    await db.flush()
    service = _service()

    packs = {r.content_id for r in await service.find(db, type=BuiltIn.REVISION_NOTE.value)}

    assert "AT-c4" in packs and "AT-c0" not in packs
    with pytest.raises(ContentError):
        await service.get(db, "AT-c0")


async def _plan_versions(db, *statuses: PlanVersionStatus) -> None:  # type: ignore[no-untyped-def]
    """Plan P-LP: a teacher's first version, then revisions, created a minute apart."""
    await (await db.connection()).run_sync(seed_content_types)
    await (await db.connection()).run_sync(seed_content_generators)
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    for number, status in enumerate(statuses, start=1):
        db.add(
            PlanVersion(
                version_id=f"LPV-LP{number}",
                plan_id="P-LP",
                source_type="manual" if number == 1 else "revised",
                session_plan={"title": f"version {number}", "lesson_plan_objectives": []},
                run_metadata={"generator": {"ref": "plan-writer"}} if number == 2 else None,
                status=status,
                approved_at=datetime(2026, 9, 1, tzinfo=timezone.utc)
                if status == PlanVersionStatus.APPROVED
                else None,
                approved_by="Teacher One" if status == PlanVersionStatus.APPROVED else None,
                created_at=datetime(2026, 9, 1, 8, number, tzinfo=timezone.utc),
            )
        )
    await db.flush()


@pytest.mark.asyncio
async def test_a_lesson_plan_is_content_found_through_any_of_its_versions(db) -> None:
    await _plan_versions(db, PlanVersionStatus.APPROVED, PlanVersionStatus.DRAFT)
    service = _service()

    found = await service.find(db, plan_version_id="LPV-LP1", type=BuiltIn.LESSON_PLAN.value)
    plan = await service.get(db, "P-LP")

    assert [record.content_id for record in found] == ["P-LP"]
    assert (plan.record.version, plan.record.review_status) == (2, "pending")
    assert plan.record.plan_version_id == "LPV-LP2"
    assert plan.record.provenance == {"origin": "teacher", "generator": {"ref": "plan-writer"}}
    assert plan.content == {"title": "version 2", "lesson_plan_objectives": []}


@pytest.mark.asyncio
async def test_approving_a_lesson_plan_freezes_the_version_the_teacher_saw(db) -> None:
    await _plan_versions(db, PlanVersionStatus.APPROVED, PlanVersionStatus.DRAFT)
    service = _service()

    with pytest.raises(ContentError) as stale:
        await service.approve(db, content_id="P-LP", expected_version=1, approved_by="T")
    assert stale.value.status_code == 409

    approved = await service.approve(db, content_id="P-LP", expected_version=2, approved_by="T")
    assert approved.record.review_status == "approved"
    assert [(a.approval_id, a.approved_version) for a in await service.approvals(db, "P-LP")] == [
        ("LPV-LP1", 1),
        ("LPV-LP2", 2),
    ]
    with pytest.raises(ContentError) as again:
        await service.approve(db, content_id="P-LP", expected_version=2, approved_by="T")
    assert again.value.status_code == 409


@pytest.mark.asyncio
async def test_a_lesson_plan_is_revised_as_a_plan_and_not_generated_from_a_version(db) -> None:
    await _plan_versions(db, PlanVersionStatus.DRAFT)
    revisions = _Revisions()
    service = _service(revisions=revisions)

    await service.revise(db, content_id="P-LP", feedback="Shorter intro.", requested_by="T")

    assert revisions.calls == [("lesson_plan", "P-LP")]
    with pytest.raises(ContentError) as refused:
        await service.generate(
            db,
            plan_version_id="LPV-LP1",
            type=BuiltIn.LESSON_PLAN.value,
            level=Level.CLASS,
            choices=GenerationChoices(),
        )
    assert refused.value.status_code == 422


@pytest.mark.asyncio
async def test_rejecting_a_draft_plan_discards_it_and_keeps_why(db) -> None:
    await _plan_versions(db, PlanVersionStatus.DRAFT)
    service = _service()

    rejected = await service.reject(
        db, content_id="P-LP", expected_version=1, rejected_by="T", reason="Too much lecturing."
    )

    assert (rejected.record.review_status, rejected.record.review_reason) == (
        "rejected",
        "Too much lecturing.",
    )
    with pytest.raises(ContentError) as approve:
        await service.approve(db, content_id="P-LP", expected_version=1, approved_by="T")
    assert approve.value.detail == "a_closed_lesson_plan_cannot_be_approved"


@pytest.mark.asyncio
async def test_rejecting_a_revision_returns_the_plan_to_its_approved_version(db) -> None:
    await _plan_versions(db, PlanVersionStatus.APPROVED, PlanVersionStatus.DRAFT)
    service = _service()

    await service.reject(db, content_id="P-LP", expected_version=2, rejected_by="T", reason="No.")

    plan = await service.get(db, "P-LP")
    assert (plan.record.review_status, plan.record.plan_version_id) == ("approved", "LPV-LP1")


@pytest.mark.asyncio
async def test_withdrawing_an_approved_plan_takes_it_back_and_stops_new_content(db) -> None:
    await _plan_versions(db, PlanVersionStatus.APPROVED)
    service = _service()

    withdrawn = await service.reject(
        db, content_id="P-LP", expected_version=1, rejected_by="T", reason="Wrong objective."
    )

    assert withdrawn.record.review_status == "rejected"
    assert await service.approvals(db, "P-LP") == []
    with pytest.raises(ContentError) as refused:
        await service.generate(
            db,
            plan_version_id="LPV-LP1",
            type=BuiltIn.LESSON_NOTE.value,
            level=Level.CLASS,
            choices=GenerationChoices(),
        )
    assert refused.value.detail == "lesson_plan_not_approved"


@pytest.mark.asyncio
async def test_a_closed_plan_cannot_be_closed_again(db) -> None:
    await _plan_versions(db, PlanVersionStatus.DRAFT)
    service = _service()
    await service.reject(db, content_id="P-LP", expected_version=1, rejected_by="T", reason="No.")

    with pytest.raises(ContentError) as again:
        await service.reject(
            db, content_id="P-LP", expected_version=1, rejected_by="T", reason="Again."
        )

    assert again.value.detail == "lesson_plan_is_already_closed"


@pytest.mark.asyncio
async def test_a_plan_a_running_study_froze_cannot_be_withdrawn(db) -> None:
    await _plan_versions(db, PlanVersionStatus.APPROVED)
    db.add(
        Experiment(
            id=uuid.uuid4(),
            experiment_id="EXP-FROZEN",
            experiment_code="FROZEN",
            investigation_db_id=uuid.uuid4(),
            teacher_workspace_id=uuid.uuid4(),
            plan_version_id="LPV-LP1",
            lifecycle_status=ExperimentLifecycleStatus.ACTIVE,
        )
    )
    await db.flush()

    with pytest.raises(ContentError) as refused:
        await _service().reject(
            db, content_id="P-LP", expected_version=1, rejected_by="T", reason="Changed my mind."
        )

    assert refused.value.detail == "lesson_plan_is_frozen_into_a_running_study"


@pytest.mark.asyncio
async def test_content_is_made_only_from_the_newest_approved_version_of_a_plan(db) -> None:
    await _plan_versions(db, PlanVersionStatus.APPROVED, PlanVersionStatus.APPROVED)
    db.add(_artefact("AT-pack", "lesson_note"))
    await db.flush()
    service = _service()

    with pytest.raises(ContentError) as old:
        await service.generate(
            db,
            plan_version_id="LPV-LP1",
            type=BuiltIn.LESSON_NOTE.value,
            level=Level.CLASS,
            choices=GenerationChoices(),
        )

    assert old.value.detail == "a_newer_plan_version_is_approved"
    await service.generate(
        db,
        plan_version_id="LPV-LP2",
        type=BuiltIn.LESSON_NOTE.value,
        level=Level.CLASS,
        choices=GenerationChoices(),
    )
