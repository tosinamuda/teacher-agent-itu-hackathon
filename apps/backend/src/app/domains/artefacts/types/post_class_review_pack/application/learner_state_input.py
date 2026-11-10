"""Single owner of the production-state → spec-state translation.

Two call sites used to keep their own copy of this mapper (``_to_spec_state``
in `student_pack_service.py`, ``_to_spec_objective_state`` in
`execution_service.py`) — P4.7 extracted the one authoritative function so
adding/removing a field on either side updates a single spot.

This is the LM boundary, so it RENDERS rather than copies: survey numbers
become self-describing phrases built from the exact anchor labels the student
answered with ("a little sure (2/5)"), and mastery becomes counts ("1 of 2
diagnostic questions correct") so thin evidence reads as thin. Frozen
bucket-era snapshots (no numerics, no counts, no evidence) degrade gracefully:
buckets coerce onto the canonical scale exactly like the production
``SurveyScale`` validator (low → 2, medium → 3, high → 4), mastery falls back
to an approximate percentage, and evidence stays empty.
"""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    AnswerEvidenceItem,
    SessionSignals,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState as SpecObjectiveLearnerState,
)
from app.domains.learner_state.domain.models import (
    AnswerEvidence,
    LearnerState,
    ObjectiveLearnerState,
    humanise_misconception_code,
)

# Production legacy coercion (assessments.schemas._coerce_survey_scale).
_BUCKET_TO_SCORE = {"low": 2, "medium": 3, "high": 4}

# The anchor labels of the post-class survey — the exact wording the student
# answered with (learner-model spec / the student survey UI options).
_CONFIDENCE_LABELS = {
    1: "not sure at all",
    2: "a little sure",
    3: "somewhat sure",
    4: "mostly sure",
    5: "very sure",
}
_DIFFICULTY_LABELS = {1: "very easy", 2: "easy", 3: "okay", 4: "difficult", 5: "very difficult"}
_INTEREST_LABELS = {
    1: "not interested",
    2: "a little interested",
    3: "somewhat interested",
    4: "interested",
    5: "very interested",
}
_FEELING_LABELS = {1: "very confused", 2: "confused", 3: "okay", 4: "good", 5: "very good"}


def _bucket_to_score(bucket: str | None) -> int | None:
    return _BUCKET_TO_SCORE.get(bucket) if bucket else None


def _scale_phrase(value: int | None, labels: dict[int, str]) -> str | None:
    """Render a 1-5 survey answer as its anchor label plus the raw value."""
    if value is None or value not in labels:
        return None
    return f"{labels[value]} ({value}/5)"


def _mastery_phrase(state: ObjectiveLearnerState) -> str | None:
    """Render performance as counts; fall back to a rounded percentage.

    Counts make thin evidence legible ("0 of 2" vs a confident-looking 0.0);
    bucket-era snapshots carry only the fraction, flagged as approximate.
    """
    if state.questions_total:
        return (
            f"{state.questions_correct or 0} of {state.questions_total} "
            "diagnostic questions correct"
        )
    if state.mastery_score is not None:
        return (
            f"about {round(state.mastery_score * 100)}% of diagnostic questions "
            "correct (exact counts not recorded)"
        )
    return None


def _to_evidence_item(evidence: AnswerEvidence) -> AnswerEvidenceItem:
    """Canonical assessment vocabulary → the LM-facing names."""
    return AnswerEvidenceItem(
        question=evidence.stem,
        options=dict(evidence.options),
        correct_option=evidence.correct_option,
        student_choice=evidence.chosen_option,
        chosen_option_misconception=(
            humanise_misconception_code(evidence.misconception_code)
            if evidence.misconception_code
            else None
        ),
    )


def to_spec_objective_state(state: ObjectiveLearnerState) -> SpecObjectiveLearnerState:
    """Map production learner state to the generation contract."""
    misconception = state.misconception_description or (
        humanise_misconception_code(state.misconception_code) if state.misconception_code else None
    )
    confidence = state.confidence_score or _bucket_to_score(state.confidence)
    difficulty = state.difficulty_score or _bucket_to_score(state.perceived_difficulty)
    return SpecObjectiveLearnerState(
        lesson_objective_id=state.lesson_objective_id,
        mastery_band=state.band,
        mastery=_mastery_phrase(state),
        confidence=_scale_phrase(confidence, _CONFIDENCE_LABELS),
        perceived_difficulty=_scale_phrase(difficulty, _DIFFICULTY_LABELS),
        misconception=misconception,
        evidence_items=[_to_evidence_item(evidence) for evidence in state.evidence],
    )


def to_session_signals(learner_state: LearnerState) -> SessionSignals | None:
    """The focal learner's session-level survey as the LM-facing tone modifiers."""
    survey = learner_state.session_survey
    if survey is None or (survey.interest is None and survey.affect is None):
        return None
    return SessionSignals(
        interest=_scale_phrase(survey.interest, _INTEREST_LABELS),
        end_of_lesson_feeling=_scale_phrase(survey.affect, _FEELING_LABELS),
    )
