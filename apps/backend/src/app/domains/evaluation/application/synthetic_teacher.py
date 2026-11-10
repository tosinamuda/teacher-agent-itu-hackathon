"""Synthetic LLM-as-teacher review gate — shared core for a CLI script + browser-triggered job.

Stands in for the human teacher-validation step (condition C4 / per-student approval):
an expert-teacher persona reads each *pending* experiment study pack and either
**approves** it or **requests changes** with one concrete instruction. A requested
change is applied through the real revision pipeline (``ArtefactRevisionService``),
which re-materialises the pack in place and keeps it ``pending``; the teacher then
re-reviews. The loop is bounded — after ``max_rounds`` revisions the pack is given a
final approval so the experiment can proceed. Clearly labelled as synthetic; not a
substitute for the expert-teacher evaluation in the thesis design.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import cast

import dspy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.infrastructure.wiring import (
    build_artefact_revision_service,
)
from app.domains.artefacts.core.domain.types import ArtefactReviewStatus
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.artefacts.core.infrastructure.wiring import build_artefact_service
from app.domains.evaluation.application.synthetic_rater import _pack_text
from app.domains.experiments.infrastructure.repository import ExperimentRepository
from app.infra.dspy_lm import build_dspy_lm
from app.shared.json_types import JsonObject

REVIEW_PACK_ARTEFACT_TYPE = "post_class_review_pack"
SYNTHETIC_REVIEWER = "Synthetic Teacher"

DEFAULT_TEACHER_PERSONA = (
    "a meticulous NERDC mathematics teacher doing the final classroom check on an "
    "auto-generated student review pack before it reaches the learner — protective of "
    "correctness, curriculum scope, and clarity, and willing to send a pack back for "
    "one concrete fix rather than approve something not yet ready"
)

REVIEW_RUBRIC = (
    "- Every lesson objective is covered by at least one section.\n"
    "- Explanations and worked examples are mathematically correct and age-appropriate.\n"
    "- Practice is clear, unambiguous, and solvable from the material given.\n"
    "- Content stays within the lesson's scope (no off-syllabus material).\n"
    "- Any sources or figures referenced are used faithfully."
)

ProgressFn = Callable[[JsonObject], None]


def _emit(on_progress: ProgressFn | None, event: JsonObject) -> None:
    if on_progress is not None:
        on_progress(event)


class TeacherReviewPack(dspy.Signature):
    """Review a student review pack as the described expert teacher before it reaches the learner.

    Approve ONLY if it is correct, covers every objective, stays on scope, and
    is pedagogically sound. Otherwise request changes with exactly ONE concrete,
    actionable instruction the author can apply to fix the most important
    problem.
    """

    persona: str = dspy.InputField(desc="the reviewing teacher's disposition")
    lesson_context: str = dspy.InputField(
        desc="subject, grade, topic, and the lesson objectives the pack must cover"
    )
    rubric: str = dspy.InputField(desc="the checklist to satisfy before approving")
    pack_text: str = dspy.InputField(desc="the review pack content under review")
    decision: str = dspy.OutputField(desc="exactly 'approve' or 'request_changes'")
    feedback: str = dspy.OutputField(
        desc="if request_changes: one concrete instruction to fix the pack; else empty"
    )
    rationale: str = dspy.OutputField(desc="one short sentence explaining the decision")


def _parse_decision(raw: str) -> str:
    """Map a free-text decision to 'approve' or 'request_changes' (default: approve).

    Defaulting an ambiguous answer to approve keeps the bounded loop terminating; a
    genuine request must say so explicitly.
    """
    text = (raw or "").strip().lower()
    if any(word in text for word in ("request", "change", "revise", "reject", "not ready")):
        return "request_changes"
    if "approve" in text:
        return "approve"
    return "approve"


def _lesson_context(manifest: object) -> str:
    if not isinstance(manifest, dict):
        return "(lesson context unavailable)"
    data = cast("dict[str, object]", manifest)
    header_parts = [
        str(data.get(key)) for key in ("subject", "grade", "topic", "subtopic") if data.get(key)
    ]
    objectives: list[str] = []
    raw_objectives = data.get("lesson_plan_objectives")
    for item in raw_objectives if isinstance(raw_objectives, list) else []:
        if isinstance(item, dict):
            entry = cast("dict[str, object]", item)
            text = str(entry.get("objective_text") or entry.get("text") or "").strip()
            if text:
                objectives.append(f"- {text}")
    header = " · ".join(header_parts) if header_parts else "(topic unavailable)"
    objective_block = "\n".join(objectives) if objectives else "- (objectives unavailable)"
    return f"{header}\nObjectives:\n{objective_block}"


async def _experiment_condition_run_ids(db: AsyncSession, experiment_id: str) -> set[str]:
    """Every condition-run id belonging to one experiment (across its executions)."""
    repository = ExperimentRepository(db)
    experiment = await repository.get_experiment(experiment_id)
    if experiment is None:
        return set()
    executions = await repository.list_executions_for_experiment(experiment.id)
    if not executions:
        return set()
    run_ids: set[str] = set()
    for execution in executions:
        for run in await repository.list_condition_runs(execution.id):
            if run.experiment_condition_run_id:
                run_ids.add(run.experiment_condition_run_id)
    return run_ids


async def _pending_experiment_artefact_ids(db: AsyncSession, experiment_id: str) -> list[str]:
    """Pack artefacts awaiting teacher approval for this experiment, in creation order."""
    run_ids = await _experiment_condition_run_ids(db, experiment_id)
    if not run_ids:
        return []
    rows = (
        (
            await db.execute(
                select(Artefact.artefact_id)
                .where(Artefact.experiment_condition_run_id.in_(run_ids))
                .where(Artefact.review_status == ArtefactReviewStatus.PENDING)
                .order_by(Artefact.created_at.asc())
            )
        )
        .scalars()
        .all()
    )
    return list(rows)


async def _load_artefact(db: AsyncSession, artefact_id: str) -> Artefact | None:
    return (
        await db.execute(select(Artefact).where(Artefact.artefact_id == artefact_id))
    ).scalar_one_or_none()


async def review_experiment(
    db: AsyncSession,
    *,
    experiment_id: str,
    persona: str | None = None,
    max_rounds: int = 2,
    on_progress: ProgressFn | None = None,
) -> JsonObject:
    """Synthetically teacher-review every pending pack of an experiment.

    For each pending pack: review → if approved, approve; else apply the requested
    change through the revision pipeline and re-review, up to ``max_rounds`` times,
    then give a final approval so the export gate can release the packet.
    """
    reviewer = dspy.ChainOfThought(TeacherReviewPack)
    lm = build_dspy_lm()
    persona_text = persona or DEFAULT_TEACHER_PERSONA
    revision = build_artefact_revision_service()
    artefacts = build_artefact_service()

    pending_ids = await _pending_experiment_artefact_ids(db, experiment_id)
    total = len(pending_ids)
    _emit(
        on_progress,
        {
            "type": "start",
            "phase": "teacher_review",
            "done": 0,
            "total": total,
            "message": f"Synthetic teacher reviewing {total} pending pack(s)…",
        },
    )

    approved = 0
    revisions = 0
    done = 0
    for artefact_id in pending_ids:
        artefact = await _load_artefact(db, artefact_id)
        if artefact is None:
            continue
        rounds = 0
        while True:
            with dspy.settings.context(lm=lm):
                out = reviewer(
                    persona=persona_text,
                    lesson_context=_lesson_context(artefact.manifest),
                    rubric=REVIEW_RUBRIC,
                    pack_text=_pack_text(artefact.manifest),
                )
            decision = _parse_decision(out.decision)
            if decision == "approve" or rounds >= max_rounds:
                break
            instruction = (out.feedback or "").strip() or (
                "Improve clarity and correctness and ensure every lesson objective is covered."
            )
            thread = await revision.get_or_create_thread(
                db=db,
                artefact_type=REVIEW_PACK_ARTEFACT_TYPE,
                subject_id=artefact.artefact_id,
                created_by="synthetic_teacher",
            )
            await revision.submit_turn(
                db=db,
                thread_id=thread.revision_thread_id,
                instruction=instruction,
                highlight=None,
            )
            revisions += 1
            rounds += 1
            _emit(
                on_progress,
                {
                    "type": "progress",
                    "phase": "teacher_review",
                    "done": done,
                    "total": total,
                    "message": f"Requested change (round {rounds}): {instruction[:80]}",
                },
            )
            reloaded = await _load_artefact(db, artefact_id)
            if reloaded is None:
                break
            artefact = reloaded

        # Final approval — either the teacher approved, or the feedback rounds are spent
        # and we release the pack so the experiment can proceed (logged as forced).
        forced = decision != "approve"
        await artefacts.approve_artefact(db=db, artefact=artefact, reviewed_by=SYNTHETIC_REVIEWER)
        approved += 1
        done += 1
        _emit(
            on_progress,
            {
                "type": "progress",
                "phase": "teacher_review",
                "done": done,
                "total": total,
                "message": (
                    f"Approved after {rounds} revision(s) (forced)"
                    if forced
                    else f"Approved (round {rounds + 1})"
                ),
            },
        )

    _emit(
        on_progress,
        {
            "type": "done",
            "phase": "teacher_review",
            "done": done,
            "total": total,
            "message": f"{approved} pack(s) approved, {revisions} revision(s) requested",
        },
    )
    return {"approved": approved, "revisions": revisions, "pending_reviewed": total}
