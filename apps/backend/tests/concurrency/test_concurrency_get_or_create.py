"""Concurrent get-or-create converges to a single row (no fork, no 500).

Two shapes are covered:

* a SINGLE-row get-or-create with re-select-on-conflict
  (``ArtefactRevisionService.get_or_create_thread``) — every concurrent caller
  must end up holding the SAME row, and exactly one is persisted; and
* a multi-step PROVISIONING CASCADE
  (``WorkspaceProvisioningApplicationService.create_workspace``) — identical
  concurrent provisions converge to exactly one class/course/TCS/workspace via
  the whole-cascade retry, instead of duplicating the graph or 500ing.

Unlike the duplicate-create tests, the EXPECTED outcome here is that *every*
caller succeeds (the loser re-reads the winner's row) — so ``others`` must be
empty and there are no 409s at all.
"""

from __future__ import annotations

import pytest

from app.domains.artefact_revision.infrastructure.wiring import (
    build_artefact_revision_service,
)
from app.domains.artefact_revision.models.revision import RevisionThread
from app.domains.school.application.workspace_provisioning_service import (
    WorkspaceProvisioningApplicationService,
)
from app.domains.school.models.core import GradeLevel, Subject
from app.domains.school.models.structure import Class, Course, School
from app.domains.school.models.subject_offerings import TermClassSubject
from app.domains.school.schemas import SchoolWorkspaceCreateRequest
from app.domains.teaching.models import TeacherWorkspace
from app.domains.users.models import User

pytestmark = pytest.mark.asyncio


def _never_a_conflict(_exc: BaseException) -> bool:
    """Convergence raises nothing — every concurrent caller should succeed."""
    return False


async def test_concurrent_revision_thread_converges(run_race, count_rows) -> None:
    service = build_artefact_revision_service()

    async def op(session, i):
        return await service.get_or_create_thread(
            db=session,
            artefact_type="post_class_review_pack",
            subject_id="PACK-RACE",
            created_by=f"user-{i}",
        )

    out = await run_race(op, _never_a_conflict, n=10)

    assert out.others == [], f"get-or-create raised instead of converging: {out.others}"
    assert len(out.wins) == 10
    # Every caller converged on the SAME thread...
    assert len({thread.revision_thread_id for thread in out.wins}) == 1
    # ...and exactly one row exists (no fork into two threads).
    assert await count_rows(RevisionThread, subject_id="PACK-RACE") == 1


async def test_concurrent_workspace_provision_converges(
    run_race, count_rows, session_factory
) -> None:
    # Seed the cascade's prerequisites, committed so the racing sessions see them.
    async with session_factory() as seed:
        school = School(name="Race High", code="RACE")
        teacher = User(auth_id="code|RACE-T", email="teacher@x.test", role="teacher")
        seed.add_all(
            [
                school,
                teacher,
                GradeLevel(name="SS1", sequence=4),
                Subject(name="Mathematics", code="MTH", category="Science"),
            ]
        )
        await seed.commit()
        school_id, teacher_id = school.id, teacher.id

    service = WorkspaceProvisioningApplicationService()

    async def op(session, i):
        return await service.create_workspace(
            db=session,
            payload=SchoolWorkspaceCreateRequest(
                school_id=school_id,
                teacher_id=teacher_id,
                grade_level_name="SS1",
                subject_code="MTH",
                class_name="SS1A",
                term="First Term",
                academic_year="2025/2026",
                is_primary=True,
            ),
        )

    out = await run_race(op, _never_a_conflict, n=8)

    assert out.others == [], f"cascade raised instead of converging: {out.others}"
    assert len(out.wins) == 8
    # All callers resolved the SAME workspace...
    assert len({workspace.workspace_id for workspace in out.wins}) == 1
    # ...and the graph exists exactly once — no duplicated class/course/TCS/workspace.
    assert await count_rows(Class, name="SS1A") == 1
    assert await count_rows(Course) == 1
    assert await count_rows(TermClassSubject) == 1
    assert await count_rows(TeacherWorkspace) == 1
