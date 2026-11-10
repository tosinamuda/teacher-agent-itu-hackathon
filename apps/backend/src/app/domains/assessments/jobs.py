"""The assessment jobs: a student's personalised pack, and synthetic students.

A student's pack is multi-call (C3 base + P1), so it runs as a job once its gate has queued
it; the result is a pending learner-level artefact awaiting teacher review.
"""

from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.domains.artefacts.types.post_class_review_pack.application.errors import (
    StudentPackGenerationError,
)
from app.domains.artefacts.types.post_class_review_pack.domain.pipeline import (
    pipeline_that_wrote,
)
from app.domains.artefacts.types.post_class_review_pack.domain.types import (
    StudentPackGenerationStatus,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.lesson_pack import (
    the_lessons_approved_class_pack,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.wiring import (
    build_generation_job_service,
    build_student_pack_service,
)

logger = logging.getLogger(__name__)


async def _written_by_the_engine(
    db: AsyncSession, student_id: str, plan_version_id: str
) -> str | None:
    """The learner's note when the revision note's learner generator is an engine one."""
    from app.domains.content.application.errors import ContentError
    from app.domains.content.domain.generators import GeneratorKind
    from app.domains.content.domain.types import BuiltIn, Level
    from app.domains.content.infrastructure.catalogue import build_content_catalogue
    from app.domains.content.infrastructure.wiring import build_engine_learner_generator

    catalogue = build_content_catalogue()
    definition = await catalogue.type(db, BuiltIn.REVISION_NOTE.value)
    try:
        binding = await catalogue.generator(db, definition, Level.LEARNER)
    except ContentError:
        return None
    if binding.harness is not GeneratorKind.ENGINE:
        return None
    return await build_engine_learner_generator().generate(
        db,
        plan_version_id=plan_version_id,
        student_id=student_id,
        binding=binding,
    )


async def generate_student_pack(generation_id: str) -> None:
    """Claim the generation job, produce the pack, and record the terminal status.

    Mirrors the experiment-execution worker: claim under a row lock (skip if terminal,
    take over a crashed RUNNING), generate, then finalize SUCCEEDED (+ the produced pack
    id) or FAILED (+ error). A failure is now a persisted FAILED job — visible to the
    teacher — instead of an opaque "no pack appeared", and it still re-raises so the job
    records the failure too.
    """
    async with AsyncSessionLocal() as db:
        jobs = build_generation_job_service()
        claimed = await jobs.claim(db, generation_id)
        if claimed is None:
            return
        # Snapshot the inputs before any rollback can expire the ORM row.
        student_id = claimed.student_id
        plan_version_id = claimed.plan_version_id
        try:
            # A learner's pack is personalised by the version that wrote the class pack it adapts;
            # with no approved class pack, generation refuses (class_pack_not_approved).
            class_pack = await the_lessons_approved_class_pack(db, plan_version_id)
            produced_id = await _written_by_the_engine(db, student_id, plan_version_id)
            if produced_id is None:
                pipeline = pipeline_that_wrote(class_pack.artefact_refs if class_pack else None)
                artefact = await build_student_pack_service(pipeline).generate_for_student(
                    db=db, student_id=student_id, plan_version_id=plan_version_id
                )
                produced_id = artefact.artefact_id
        except Exception as exc:
            # Discard any partial generation (and clear a failed-flush state) before the
            # finalize re-reads the job, so its terminal write lands on a clean session.
            await db.rollback()
            category = (
                "inputs_missing" if isinstance(exc, StudentPackGenerationError) else "generation"
            )
            await jobs.finalize(
                db,
                generation_id,
                status=StudentPackGenerationStatus.FAILED,
                error=str(exc)[:500],
                error_category=category,
            )
            logger.exception(
                "student pack generation failed: generation=%s student=%s plan=%s",
                generation_id,
                student_id,
                plan_version_id,
            )
            raise
        await jobs.finalize(
            db,
            generation_id,
            status=StudentPackGenerationStatus.SUCCEEDED,
            produced_artefact_id=produced_id,
        )


async def synthetic_students(
    plan_version_id: str,
    n_students: int = 4,
    class_id: str | None = None,
    experiment_id: str | None = None,
) -> None:
    from app.domains.assessments.application.synthetic_student import answer_diagnostic
    from app.domains.experiments.application.synthetic_progress import (
        publish_synthetic_progress,
    )

    def on_progress(event: dict) -> None:
        if experiment_id:
            publish_synthetic_progress(experiment_id, {**event, "flow": "students"})

    async with AsyncSessionLocal() as db:
        try:
            await answer_diagnostic(
                db,
                plan_version_id=plan_version_id,
                n_students=n_students,
                class_id=class_id,
                on_progress=on_progress,
            )
        except Exception:  # noqa: BLE001 - best-effort; never crash the worker
            logger.exception("synthetic students failed: plan=%s", plan_version_id)
            on_progress({"type": "error", "phase": "students", "message": "synthetic run failed"})
