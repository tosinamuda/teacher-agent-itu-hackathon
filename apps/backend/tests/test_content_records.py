"""Every approval is kept with the version it approved; the class test has a content record."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sqlalchemy import select, text

from app.domains.artefacts.core.application.service import ArtefactApplicationError
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus, ArtefactType
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.core.infrastructure.repository import ArtefactRepository
from app.domains.artefacts.core.infrastructure.wiring import build_lifecycle_manager
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.assessments.infrastructure.repository import ClassTestMaterials
from app.domains.assessments.infrastructure.wiring import build_diagnostic_service
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from migrations.data.class_test_material_backfill import backfill_class_test_materials


def _plan(version_id: str, *, released: bool = False) -> PlanVersion:
    return PlanVersion(
        version_id=version_id,
        plan_id=f"P-{version_id}",
        source_type="experiment_manual",
        session_plan={"lesson_plan_objectives": []},
        status=PlanVersionStatus.DRAFT,
        assessment_released_at=datetime.now(timezone.utc) if released else None,
        assessment_released_by="Teacher One" if released else None,
    )


def _item(plan_version_id: str) -> ExitTicketItem:
    return ExitTicketItem(
        subtopic_id="sub",
        plan_version_id=plan_version_id,
        lesson_objective_id="lop01",
        stem="2 + 3 × 4 = ?",
        correct_option="B",
        options={"A": "20", "B": "14", "C": "24", "D": "9"},
        difficulty="easy",
    )


async def _seed(db, *rows) -> None:  # type: ignore[no-untyped-def]
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add_all(rows)
    await db.flush()


async def _class_test(db, plan_version_id: str) -> Artefact:  # type: ignore[no-untyped-def]
    return (
        await db.execute(
            select(Artefact)
            .where(Artefact.artefact_type == ArtefactType.DIAGNOSTIC.value)
            .where(Artefact.plan_version_id == plan_version_id)
        )
    ).scalar_one()


@pytest.mark.asyncio
async def test_an_approval_is_kept_with_the_version_the_teacher_saw(db) -> None:
    await _seed(
        db,
        _plan("LPV-A1"),
        Artefact(
            artefact_id="AT-approve-1",
            artefact_type=ArtefactType.LESSON_NOTE.value,
            scope="class_level",
            plan_version_id="LPV-A1",
            manifest={},
            review_status=ArtefactReviewStatus.PENDING,
        ),
    )
    manager = build_lifecycle_manager()

    approved = await manager.approve_artefact(
        db=db, artefact_id="AT-approve-1", reviewed_by="Teacher One", expected_version=1
    )
    approvals = await ArtefactRepository().list_approvals(db, "AT-approve-1")

    assert [(a.approved_version, a.approved_by) for a in approvals] == [(1, "Teacher One")]
    assert approved.version == 1
    with pytest.raises(ArtefactApplicationError) as again:
        await manager.approve_artefact(
            db=db, artefact_id="AT-approve-1", reviewed_by="Teacher One", expected_version=1
        )
    assert (again.value.status_code, again.value.detail) == (409, "artefact_already_approved")


@pytest.mark.asyncio
async def test_the_class_test_record_is_created_then_versioned_with_its_questions(db) -> None:
    await _seed(db, _plan("LPV-C1"))
    records = ClassTestMaterials()

    await records.ensure(db, plan_version_id="LPV-C1", source="generated")
    await db.flush()
    first = await _class_test(db, "LPV-C1")
    assert (first.version, first.review_status) == (1, ArtefactReviewStatus.PENDING)
    assert first.manifest == {"plan_version_id": "LPV-C1", "source": "generated"}

    await records.ensure(db, plan_version_id="LPV-C1", source="manual_classwork")
    await db.flush()
    again = await _class_test(db, "LPV-C1")
    assert again.artefact_id == first.artefact_id
    assert again.version == 2
    assert again.manifest["source"] == "manual_classwork"


@pytest.mark.asyncio
async def test_a_class_test_already_sent_to_students_is_approved(db) -> None:
    await _seed(db, _plan("LPV-C2", released=True))

    await ClassTestMaterials().ensure(db, plan_version_id="LPV-C2", source="generated")
    await db.flush()

    assert (await _class_test(db, "LPV-C2")).review_status == ArtefactReviewStatus.APPROVED


def test_the_generate_route_writes_the_class_test_record() -> None:
    assert isinstance(build_diagnostic_service().materials, ClassTestMaterials)


@pytest.mark.asyncio
async def test_the_backfill_records_existing_class_tests_once(db) -> None:
    await _seed(
        db,
        _plan("LPV-B1", released=True),
        _plan("LPV-B2"),
        _item("LPV-B1"),
        _item("LPV-B1"),
        _item("LPV-B2"),
    )
    connection = await db.connection()

    assert await connection.run_sync(backfill_class_test_materials) == 2
    assert await connection.run_sync(backfill_class_test_materials) == 0

    released = await _class_test(db, "LPV-B1")
    assert (released.review_status, released.version) == (ArtefactReviewStatus.APPROVED, 1)
    approvals = await ArtefactRepository().list_approvals(db, released.artefact_id)
    assert [(a.approved_version, a.approved_by) for a in approvals] == [(1, "Teacher One")]
    assert (await _class_test(db, "LPV-B2")).review_status == ArtefactReviewStatus.PENDING
