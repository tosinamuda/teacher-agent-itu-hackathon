"""Synthetic LLM students that answer a lesson's exit diagnostic from a profile.

Shared core for the CLI script + the browser-triggered job: picks N class
learners without a submission, gives each an ability profile, and has a DSPy "student"
answer every MCQ without seeing the key. Each student's answers go through the REAL
submit path (submit_exit_assessment) — so grading, the objective-indexed learner state,
and the per-student study-pack worker (generate_student_pack) all fire exactly like a
real student. An optional on_progress callback drives the live WS progress.
Clearly synthetic — the profile drives correctness; it's a pre-test, not real learners.
"""

from __future__ import annotations

import logging
import random
import uuid
from collections.abc import Callable

import dspy
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.assessments.application.service import AssessmentApplicationService
from app.domains.assessments.models import ExitTicketSubmission
from app.domains.assessments.schemas import ExitAssessmentAnswer, ExitAssessmentSubmitRequest
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.domains.learners.models.learner import LearnerProfile
from app.infra.dspy_lm import build_dspy_lm
from app.shared.json_types import JsonObject

logger = logging.getLogger(__name__)

PROFILES: list[str] = [
    "a strong, confident student who reasons carefully and is usually correct",
    "an average student who gets most items right but slips on the trickier ones",
    "a struggling student who often picks a plausible-looking wrong option",
    "a student with a specific misconception who confuses related ideas (e.g. LCM vs HCF)",
]

ProgressFn = Callable[[JsonObject], None]


class StudentAnswer(dspy.Signature):
    """Answer a multiple-choice question AS the described student.

    You do NOT know the key. Reason in character, then output only the single
    option letter you'd pick.
    """

    profile: str = dspy.InputField(desc="the student's ability and tendencies")
    question: str = dspy.InputField(desc="the stem followed by options A-D")
    option_letter: str = dspy.OutputField(desc="the chosen option key, e.g. A")


def _question_text(item: ExitTicketItem) -> str:
    options = item.options if isinstance(item.options, dict) else {}
    lines = [str(item.stem)]
    for key in sorted(options):
        lines.append(f"{key}. {options[key]}")
    return "\n".join(lines)


def _clean_letter(raw: str, options: object) -> str:
    keys = sorted(options) if isinstance(options, dict) else []
    for ch in (raw or "").strip().upper():
        if ch in keys:
            return ch
    return keys[0] if keys else "A"


def _emit(on_progress: ProgressFn | None, event: JsonObject) -> None:
    if on_progress is not None:
        on_progress(event)


class SyntheticStudentBatchResult(BaseModel):
    """Completion summary for a synthetic-student diagnostic run."""

    created: int
    students: list[JsonObject]


async def answer_diagnostic(
    db: AsyncSession,
    *,
    plan_version_id: str,
    n_students: int = 4,
    class_id: str | None = None,
    on_progress: ProgressFn | None = None,
) -> JsonObject:
    """Have N synthetic students answer + submit the lesson's diagnostic (real path)."""
    student = dspy.ChainOfThought(StudentAnswer)
    lm = build_dspy_lm()
    assessment = AssessmentApplicationService()

    items = (
        (
            await db.execute(
                select(ExitTicketItem)
                .where(ExitTicketItem.plan_version_id == plan_version_id)
                .where(ExitTicketItem.lesson_objective_id.isnot(None))
            )
        )
        .scalars()
        .all()
    )
    if not items:
        _emit(
            on_progress,
            {
                "type": "done",
                "phase": "students",
                "done": 0,
                "total": 0,
                "message": "No diagnostic items for this lesson.",
            },
        )
        return {"created": 0, "students": [], "note": "no diagnostic items"}

    answered = set(
        (
            await db.execute(
                select(ExitTicketSubmission.student_id).where(
                    ExitTicketSubmission.plan_version_id == plan_version_id
                )
            )
        )
        .scalars()
        .all()
    )
    query = select(LearnerProfile)
    if class_id:
        # ``class_id`` arrives as a str (job args / HTTP). The column is a UUID
        # (CHAR(32) on MySQL) whose bind processor calls ``.hex`` — a bare str
        # raised "'str' object has no attribute 'hex'" on MySQL (Postgres' driver
        # coerced it for us). Coerce explicitly so the filter is dialect-agnostic.
        class_uuid = uuid.UUID(class_id) if isinstance(class_id, str) else class_id
        query = query.where(LearnerProfile.class_id == class_uuid)
    # Pick N unanswered learners at random. Shuffle in Python rather than
    # ``ORDER BY random()``: the rows are all materialised here anyway, and
    # ``func.random()`` compiles to ``random()`` — which MySQL doesn't have (it's
    # ``RAND()``), so the PG-ism would 500 on MySQL.
    pool = [
        learner
        for learner in (await db.execute(query)).scalars().all()
        if learner.student_id not in answered
    ]
    random.shuffle(pool)
    candidates = pool[:n_students]

    total = len(candidates)
    _emit(
        on_progress,
        {
            "type": "start",
            "phase": "students",
            "done": 0,
            "total": total,
            "message": f"Synthetic class answering the diagnostic ({total})…",
        },
    )

    # Snapshot the ORM rows to plain values BEFORE the loop: a per-student failure
    # rolls back, which expires every ORM object in the session; reading an expired
    # `item`/`learner` on the next iteration would raise MissingGreenlet (async) and
    # detonate the rest of the batch the `continue` is meant to isolate.
    item_views = [
        {
            "id": str(item.id),
            "options": item.options if isinstance(item.options, dict) else {},
            "correct_option": item.correct_option,
            "question": _question_text(item),
        }
        for item in items
    ]
    learner_ids = [learner.student_id for learner in candidates]
    total_items = len(item_views)

    summary: list[JsonObject] = []
    for index, student_id in enumerate(learner_ids):
        profile = PROFILES[index % len(PROFILES)]
        answers: list[ExitAssessmentAnswer] = []
        correct = 0
        for view in item_views:
            options = view["options"]
            with dspy.settings.context(lm=lm):
                out = student(profile=profile, question=view["question"])
            choice = _clean_letter(out.option_letter, options)
            answers.append(ExitAssessmentAnswer(item_id=str(view["id"]), selected_option=choice))
            if choice == view["correct_option"]:
                correct += 1
        try:
            await assessment.submit_exit_assessment(
                db=db,
                payload=ExitAssessmentSubmitRequest(
                    student_id=student_id,
                    plan_version_id=plan_version_id,
                    answers=answers,
                    survey=[],
                ),
            )
        except Exception:  # noqa: BLE001 - one student's failure shouldn't abort the batch
            # Isolate this student from the batch, but never swallow silently — an
            # unlogged continue turned a real submit failure into "0 created, task
            # succeeded" (invisible in the worker log).
            logger.exception(
                "synthetic student submit failed: student=%s plan=%s",
                student_id,
                plan_version_id,
            )
            await db.rollback()
            continue
        summary.append(
            {
                "student_id": student_id,
                "correct": correct,
                "total": total_items,
                "profile": profile,
            }
        )
        _emit(
            on_progress,
            {
                "type": "progress",
                "phase": "students",
                "done": len(summary),
                "total": total,
                "message": f"{student_id}: {correct}/{total_items} correct",
            },
        )

    _emit(
        on_progress,
        {
            "type": "done",
            "phase": "students",
            "done": len(summary),
            "total": total,
            "message": f"{len(summary)} synthetic students answered; packs queued",
        },
    )
    return SyntheticStudentBatchResult(created=len(summary), students=summary).model_dump(
        mode="json"
    )
