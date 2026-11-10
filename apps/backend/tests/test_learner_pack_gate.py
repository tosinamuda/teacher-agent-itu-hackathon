"""A learner's pack is made only once the class pack is approved and their evidence is in."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.core.infrastructure.wiring import build_artefact_service
from app.domains.artefacts.types.lesson_plan.domain.types import PlanVersionStatus
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.artefacts.types.post_class_review_pack.application import student_pack_service
from app.domains.artefacts.types.post_class_review_pack.application.errors import (
    StudentPackGenerationError,
)
from app.domains.artefacts.types.post_class_review_pack.application.student_pack_service import (
    StudentPackGenerationService,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.models import (
    StudentPackGeneration,
)
from app.domains.assessments.application.service import AssessmentApplicationService
from app.domains.assessments.schemas import ExitAssessmentSurveyAttachRequest
from app.domains.learners.models import LearnerProfile
from app.infra.jobs.kinds import GENERATE_STUDENT_PACK
from app.infra.jobs.models import Job

_OBJECTIVES = {
    "lesson_plan_objectives": [{"lesson_objective_id": "lop01", "objective_text": "Add"}]
}
_RESULTS = {
    "objectives": [
        {"lesson_objective_id": "lop01", "score": 1, "max_score": 2, "items": []},
    ]
}


async def _queued(db: AsyncSession, plan: str) -> list[str]:
    """The learners whose generation has the job that runs it."""
    statement = (
        select(StudentPackGeneration.student_id)
        .join(Job, Job.subject == StudentPackGeneration.generation_id)
        .where(StudentPackGeneration.plan_version_id == plan, Job.kind == GENERATE_STUDENT_PACK)
        .order_by(StudentPackGeneration.student_id)
    )
    return list((await db.execute(statement)).scalars())


async def _lesson(db: AsyncSession, plan: str, *students: str) -> Artefact:
    """A lesson with a pending class pack and the given learners."""
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(
        PlanVersion(
            version_id=plan,
            plan_id=f"P-{plan}",
            source_type="experiment_manual",
            session_plan=_OBJECTIVES,
            status=PlanVersionStatus.APPROVED,
        )
    )
    for student in students:
        db.add(LearnerProfile(student_id=student, full_name=student, grade="JSS1", track="General"))
    class_pack = Artefact(
        artefact_id=f"AT-{plan}",
        artefact_type="post_class_review_pack",
        scope="class_level",
        plan_version_id=plan,
        manifest={"steps": []},
        review_status=ArtefactReviewStatus.PENDING,
    )
    db.add(class_pack)
    await db.flush()
    return class_pack


async def _submit(
    db: AsyncSession, plan: str, student: str, *, survey_pending: bool = False
) -> str:
    submission = await AssessmentApplicationService().persist_diagnostic(
        db=db,
        student_id=student,
        plan_version_id=plan,
        results=_RESULTS,
        diagnostic_id=f"DG-{plan}-{student}",
        survey_pending=survey_pending,
    )
    return submission.diagnostic_id


async def _approve(db: AsyncSession, class_pack: Artefact) -> None:
    await build_artefact_service().approve_artefact(db=db, artefact=class_pack, reviewed_by="T")


async def _jobs(db: AsyncSession, plan: str) -> list[str]:
    rows = await db.execute(
        select(StudentPackGeneration.student_id).where(
            StudentPackGeneration.plan_version_id == plan
        )
    )
    return sorted(rows.scalars())


@pytest.mark.asyncio
async def test_a_submission_before_approval_waits_and_approval_generates_it(
    db: AsyncSession,
) -> None:
    class_pack = await _lesson(db, "LPV-G1", "ST-G1a", "ST-G1b")

    await _submit(db, "LPV-G1", "ST-G1a")
    await _submit(db, "LPV-G1", "ST-G1b")
    assert await _queued(db, "LPV-G1") == []
    assert await _jobs(db, "LPV-G1") == []

    await _approve(db, class_pack)

    assert await _queued(db, "LPV-G1") == ["ST-G1a", "ST-G1b"]
    assert await _jobs(db, "LPV-G1") == ["ST-G1a", "ST-G1b"]


@pytest.mark.asyncio
async def test_a_submission_after_approval_generates_at_once(
    db: AsyncSession,
) -> None:
    class_pack = await _lesson(db, "LPV-G2", "ST-G2")
    await _approve(db, class_pack)
    assert await _queued(db, "LPV-G2") == []

    await _submit(db, "LPV-G2", "ST-G2")

    assert await _queued(db, "LPV-G2") == ["ST-G2"]


@pytest.mark.asyncio
async def test_a_learner_whose_survey_is_due_waits_for_it_even_after_approval(
    db: AsyncSession,
) -> None:
    class_pack = await _lesson(db, "LPV-G3", "ST-G3")
    diagnostic_id = await _submit(db, "LPV-G3", "ST-G3", survey_pending=True)
    await _approve(db, class_pack)
    assert await _queued(db, "LPV-G3") == []

    await AssessmentApplicationService().attach_exit_assessment_survey(
        db=db,
        diagnostic_id=diagnostic_id,
        student_id="ST-G3",
        payload=ExitAssessmentSurveyAttachRequest(survey=[], session_survey=None),
    )

    assert await _queued(db, "LPV-G3") == ["ST-G3"]


@pytest.mark.asyncio
async def test_generation_never_reads_a_pending_class_pack(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    await _lesson(db, "LPV-G4", "ST-G4")
    touched: list[str] = []

    class _Refuses:
        async def generate(self, **_: object) -> None:
            touched.append("base")

        async def personalise(self, **_: object) -> None:
            touched.append("personalise")

    async def _plan_row(_db: AsyncSession, *, plan_or_version_id: str) -> tuple[object, object]:
        return SimpleNamespace(session_plan=_OBJECTIVES), SimpleNamespace()

    monkeypatch.setattr(student_pack_service, "get_plan_row", _plan_row)
    service = StudentPackGenerationService(
        base_generator=_Refuses(),  # type: ignore[arg-type]
        learner_personaliser=_Refuses(),  # type: ignore[arg-type]
        lesson_notes=SimpleNamespace(),  # type: ignore[arg-type]
    )

    with pytest.raises(StudentPackGenerationError, match="class_pack_not_approved"):
        await service.generate_for_student(db=db, student_id="ST-G4", plan_version_id="LPV-G4")
    assert touched == []
    class_packs = await db.execute(
        select(Artefact.artefact_id).where(Artefact.plan_version_id == "LPV-G4")
    )
    assert list(class_packs.scalars()) == ["AT-LPV-G4"]
