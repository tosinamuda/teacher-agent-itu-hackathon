"""Assemble the v2 evidence-rich learner state from real DB rows.

Pure translation: focal-case snapshot + the learner's actual item responses
(chosen options, distractor rationales) -> ``ObjectiveLearnerEvidence`` per
objective. Numeric survey scores fall back to the SAME legacy coercion the
production ``SurveyScale`` validator applies to bucket-era submissions
(low -> 2, medium -> 3, high -> 4) — flagged in the run report's provenance.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.assessments.models.student_item_response import StudentItemResponse
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.domains.learner_state.domain.models import (
    LearnerState,
    ObjectiveLearnerState,
    humanise_misconception_code,
)
from experiments.p1_evidence_prompt.requests_v2 import (
    AnswerEvidenceItem,
    ObjectiveLearnerEvidence,
)

# Production legacy coercion (assessments.schemas._coerce_survey_scale).
_BUCKET_TO_SCORE = {"low": 2, "medium": 3, "high": 4}


def bucket_to_score(bucket: str | None) -> int | None:
    """Map a legacy low/medium/high bucket onto the canonical 1-5 scale."""
    return _BUCKET_TO_SCORE.get(bucket) if bucket else None


async def load_answer_evidence(
    db: AsyncSession,
    *,
    student_id: str,
    plan_version_id: str,
) -> dict[str, list[AnswerEvidenceItem]]:
    """The learner's missed items per objective, with chosen-distractor rationales."""
    rows = (
        await db.execute(
            select(ExitTicketItem, StudentItemResponse)
            .join(StudentItemResponse, StudentItemResponse.item_id == ExitTicketItem.id)
            .where(
                StudentItemResponse.student_id == student_id,
                ExitTicketItem.plan_version_id == plan_version_id,
            )
            .order_by(ExitTicketItem.lesson_objective_id)
        )
    ).all()
    by_objective: dict[str, list[AnswerEvidenceItem]] = {}
    for item, response in rows:
        if response.is_correct or not item.lesson_objective_id:
            continue  # spec: evidence items are the WRONG answers (chosen distractors)
        misconceptions = item.option_misconceptions or {}
        code = misconceptions.get(response.choice)
        by_objective.setdefault(item.lesson_objective_id, []).append(
            AnswerEvidenceItem(
                question=item.stem,
                options=dict(item.options or {}),
                correct_option=item.correct_option,
                student_choice=response.choice,
                chosen_option_misconception=(humanise_misconception_code(code) if code else None),
            )
        )
    return by_objective


def to_evidence_state(
    state: ObjectiveLearnerState,
    evidence_items: list[AnswerEvidenceItem],
) -> ObjectiveLearnerEvidence:
    """One objective's v2 LM input from the production state + raw evidence."""
    misconception = state.misconception_description or (
        humanise_misconception_code(state.misconception_code) if state.misconception_code else None
    )
    return ObjectiveLearnerEvidence(
        lesson_objective_id=state.lesson_objective_id,
        status=state.band,
        mastery_score=state.mastery_score,
        confidence_score=bucket_to_score(state.confidence),
        difficulty_score=bucket_to_score(state.perceived_difficulty),
        misconception=misconception,
        evidence_items=evidence_items,
    )


def evidence_states_for_learner(
    learner_state: LearnerState,
    answer_evidence: dict[str, list[AnswerEvidenceItem]],
) -> dict[str, ObjectiveLearnerEvidence]:
    """All v2 objective states for a focal learner, keyed by objective id."""
    return {
        state.lesson_objective_id: to_evidence_state(
            state, answer_evidence.get(state.lesson_objective_id, [])
        )
        for state in learner_state.objective_states
    }
