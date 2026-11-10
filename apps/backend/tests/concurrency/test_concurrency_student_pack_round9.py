"""DB-backed tests for the two round-9 features.

Student-pack generation lifecycle (StudentPackGeneration job):
* concurrent dispatch creates exactly ONE in-flight job (the dup-guard);
* claim → RUNNING → finalize SUCCEEDED/FAILED, and a terminal job is not re-claimed;
* keep-versions: the learner read collapses several pack rows to the current (latest).

Artefact approve optimistic concurrency (Artefact.version):
* a stale approve (the version moved on, e.g. a revise) is a clean 409, not a blind bless;
* concurrent approves → exactly one wins, the rest 409.

Independent committing sessions per "process" (see this package's conftest).
"""

from __future__ import annotations

import pytest
from sqlalchemy import text

from app.domains.artefacts.core.application.service import (
    ArtefactApplicationError,
)
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.core.infrastructure.repository import ArtefactRepository
from app.domains.artefacts.core.infrastructure.wiring import (
    build_artefact_service,
    build_lifecycle_manager,
)
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.artefacts.types.post_class_review_pack.domain.types import (
    StudentPackGenerationStatus,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.models import (
    StudentPackGeneration,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.repository import (
    StudentPackGenerationRepository,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.wiring import (
    build_generation_job_service,
)
from app.domains.learners.models import LearnerProfile
from app.shared.time import utc_now

pytestmark = pytest.mark.asyncio


async def _seed_student_and_plan(session_factory, *, student_id: str, plan_version_id: str) -> None:
    """Commit the FK parents (student_profiles + plan_versions) a generation job references."""
    async with session_factory() as seed:
        await seed.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        seed.add(
            LearnerProfile(
                student_id=student_id, full_name="Test Student", grade="JSS1", track="science"
            )
        )
        seed.add(PlanVersion(version_id=plan_version_id, plan_id="LP-test", source_type="authored"))
        await seed.commit()


async def _seed_pending_pack(
    session_factory,
    *,
    artefact_id: str,
    plan_version_id: str,
    student_id: str | None,
    version: int = 1,
    created_at=None,
) -> None:
    async with session_factory() as seed:
        await seed.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        seed.add(
            Artefact(
                artefact_id=artefact_id,
                artefact_type="post_class_review_pack",
                scope="learner_level",
                plan_version_id=plan_version_id,
                student_id=student_id,
                manifest={},
                review_status=ArtefactReviewStatus.PENDING,
                version=version,
                created_at=created_at or utc_now(),
            )
        )
        await seed.commit()


# --------------------------------------------------------------------------- #
# Student-pack generation job
# --------------------------------------------------------------------------- #


async def test_concurrent_enqueue_creates_one_job(
    run_race, count_rows, session_factory, monkeypatch
) -> None:
    await _seed_student_and_plan(session_factory, student_id="ST-1", plan_version_id="LPV-1")

    async def op(session, _i):
        job = await build_generation_job_service().enqueue(
            session, student_id="ST-1", plan_version_id="LPV-1"
        )
        return job.generation_id if job is not None else None

    out = await run_race(op, lambda _e: False, n=4)

    assert out.others == [], f"enqueue raced to an error: {out.others}"
    # Exactly one job is created; the rest see it in flight / lose the unique race → None.
    assert await count_rows(StudentPackGeneration, student_id="ST-1", plan_version_id="LPV-1") == 1
    assert sum(1 for win in out.wins if win is not None) == 1


async def test_enqueue_skips_when_already_in_flight(session_factory, monkeypatch) -> None:
    await _seed_student_and_plan(session_factory, student_id="ST-2", plan_version_id="LPV-2")
    jobs = build_generation_job_service()

    async with session_factory() as a:
        first = await jobs.enqueue(a, student_id="ST-2", plan_version_id="LPV-2")
    assert first is not None  # QUEUED

    async with session_factory() as b:
        second = await jobs.enqueue(b, student_id="ST-2", plan_version_id="LPV-2")
    assert second is None  # a generation is already in flight — don't double-generate


async def test_claim_then_finalize_succeeded_and_no_reclaim(session_factory) -> None:
    await _seed_student_and_plan(session_factory, student_id="ST-3", plan_version_id="LPV-3")
    repo = StudentPackGenerationRepository()
    jobs = build_generation_job_service()
    async with session_factory() as seed:
        job = await repo.save(
            seed,
            StudentPackGeneration(
                generation_id="SPG-3",
                student_id="ST-3",
                plan_version_id="LPV-3",
                attempt_number=1,
                status=StudentPackGenerationStatus.QUEUED,
            ),
        )
        gen_id = job.generation_id

    async with session_factory() as worker:
        claimed = await jobs.claim(worker, gen_id)
        assert claimed is not None and claimed.status == StudentPackGenerationStatus.RUNNING
        await jobs.finalize(
            worker,
            gen_id,
            status=StudentPackGenerationStatus.SUCCEEDED,
            produced_artefact_id="AT-3",
        )

    async with session_factory() as check:
        done = await repo.get(check, gen_id)
        assert done is not None
        assert done.status == StudentPackGenerationStatus.SUCCEEDED
        assert done.produced_artefact_id == "AT-3"
        # A redelivery of a terminal job is skipped, not re-run.
        assert await jobs.claim(check, gen_id) is None


async def test_finalize_failed_records_error(session_factory) -> None:
    await _seed_student_and_plan(session_factory, student_id="ST-4", plan_version_id="LPV-4")
    repo = StudentPackGenerationRepository()
    jobs = build_generation_job_service()
    async with session_factory() as seed:
        await repo.save(
            seed,
            StudentPackGeneration(
                generation_id="SPG-4",
                student_id="ST-4",
                plan_version_id="LPV-4",
                attempt_number=1,
                status=StudentPackGenerationStatus.QUEUED,
            ),
        )

    async with session_factory() as worker:
        await jobs.claim(worker, "SPG-4")
        await jobs.finalize(
            worker,
            "SPG-4",
            status=StudentPackGenerationStatus.FAILED,
            error="student_not_found",
            error_category="inputs_missing",
        )

    async with session_factory() as check:
        failed = await repo.get(check, "SPG-4")
        assert failed is not None
        assert failed.status == StudentPackGenerationStatus.FAILED
        assert failed.error_category == "inputs_missing"  # visible to the teacher UI, not opaque


async def test_keep_versions_read_returns_latest_only(session_factory) -> None:
    """Two pack versions for one (student, lesson): the learner read shows only the newest."""
    from datetime import timedelta

    older = utc_now() - timedelta(hours=1)
    await _seed_pending_pack(
        session_factory,
        artefact_id="AT-old",
        plan_version_id="LPV-5",
        student_id="ST-5",
        created_at=older,
    )
    await _seed_pending_pack(
        session_factory,
        artefact_id="AT-new",
        plan_version_id="LPV-5",
        student_id="ST-5",
        created_at=utc_now(),
    )

    async with session_factory() as check:
        rows = await build_lifecycle_manager().list_learner_artefacts(
            db=check, learner_id="ST-5", plan_version_id=None, limit=50, review_status=None
        )
    assert [a.artefact_id for a in rows] == ["AT-new"]  # current = latest; older kept but hidden


# --------------------------------------------------------------------------- #
# Artefact approve optimistic concurrency
# --------------------------------------------------------------------------- #


async def test_stale_approve_is_409_then_current_version_approves(session_factory) -> None:
    await _seed_pending_pack(
        session_factory, artefact_id="AT-9", plan_version_id="LPV-9", student_id="ST-9", version=1
    )
    service = build_artefact_service()

    # The pack was revised since the teacher loaded v1 (version is now 2).
    async with session_factory() as revise:
        artefact = await ArtefactRepository().get_artefact(revise, "AT-9")
        artefact.version = 2
        await revise.commit()

    async with session_factory() as stale:
        artefact = await ArtefactRepository().get_artefact(stale, "AT-9")
        with pytest.raises(ArtefactApplicationError) as exc:
            await service.approve_artefact(
                db=stale, artefact=artefact, reviewed_by="t", expected_version=1
            )
        assert exc.value.status_code == 409
        assert exc.value.detail == "artefact_changed"

    async with session_factory() as fresh:
        artefact = await ArtefactRepository().get_artefact(fresh, "AT-9")
        approved = await service.approve_artefact(
            db=fresh, artefact=artefact, reviewed_by="t", expected_version=2
        )
        assert approved.review_status == ArtefactReviewStatus.APPROVED
        assert approved.version == 2


async def test_concurrent_approve_one_wins_rest_409(run_race, session_factory) -> None:
    await _seed_pending_pack(
        session_factory,
        artefact_id="AT-10",
        plan_version_id="LPV-10",
        student_id="ST-10",
        version=1,
    )

    async def op(session, _i):
        artefact = await ArtefactRepository().get_artefact(session, "AT-10")
        # Every teacher loaded version 1; only the first approve should land.
        return await build_artefact_service().approve_artefact(
            db=session, artefact=artefact, reviewed_by="t", expected_version=1
        )

    out = await run_race(
        op,
        lambda e: isinstance(e, ArtefactApplicationError) and e.status_code == 409,
        n=4,
    )

    assert out.others == [], f"approve raced to a non-409 error: {out.others}"
    assert len(out.wins) == 1  # exactly one approval lands
    assert len(out.conflicts) == 3  # the rest get a clean 409 artefact_changed

    async with session_factory() as check:
        artefact = await ArtefactRepository().get_artefact(check, "AT-10")
        assert artefact.review_status == ArtefactReviewStatus.APPROVED
        assert artefact.version == 1
