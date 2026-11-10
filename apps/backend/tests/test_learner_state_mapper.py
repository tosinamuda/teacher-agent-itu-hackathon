"""The production-state -> spec-state boundary translation (LM rendering).

Canonical assessment vocabulary (stem / chosen_option / misconception_code)
maps onto the LM-facing names (question / student_choice /
chosen_option_misconception), and survey numbers render as self-describing
phrases built from the survey's anchor labels — bare numbers with a "_score"
suffix invite cross-scale misreading. Bucket-era snapshots degrade gracefully
via the production legacy coercion (low -> 2, medium -> 3, high -> 4).
"""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.application.learner_state_input import (
    to_session_signals,
    to_spec_objective_state,
)
from app.domains.learner_state.domain.models import (
    AnswerEvidence,
    LearnerState,
    ObjectiveLearnerState,
    SessionSurvey,
)


def test_evidence_rich_state_renders_lm_phrases() -> None:
    state = ObjectiveLearnerState(
        lesson_objective_id="lop01",
        mastery_score=0.0,
        questions_correct=0,
        questions_total=2,
        band="remediate",
        misconception_code="missing_factor_of_two",
        confidence_score=2,
        difficulty_score=5,
        evidence=[
            AnswerEvidence(
                stem="Which is a common multiple of 2 and 3?",
                options={"B": "9", "C": "6"},
                correct_option="C",
                chosen_option="B",
                misconception_code="missing_factor_of_two",
            )
        ],
    )
    spec = to_spec_objective_state(state)
    assert spec.mastery_band == "remediate"
    assert spec.mastery == "0 of 2 diagnostic questions correct"
    assert spec.confidence == "a little sure (2/5)"
    assert spec.perceived_difficulty == "very difficult (5/5)"
    assert spec.misconception == "Missing factor of two"  # humanised plain words
    item = spec.evidence_items[0]
    assert item.question == "Which is a common multiple of 2 and 3?"
    assert item.student_choice == "B"
    assert item.correct_option == "C"
    assert item.chosen_option_misconception == "Missing factor of two"


def test_bucket_era_snapshot_falls_back_to_legacy_coercion() -> None:
    # Frozen focal-case snapshots predate the numeric survey + counts: buckets
    # and a bare fraction only. Buckets coerce exactly like the production
    # SurveyScale rule; mastery renders as an approximate percentage.
    state = ObjectiveLearnerState(
        lesson_objective_id="lop01",
        mastery_score=0.5,
        band="reinforce",
        confidence="low",
        perceived_difficulty="high",
    )
    spec = to_spec_objective_state(state)
    assert spec.mastery_band == "reinforce"
    assert spec.mastery == ("about 50% of diagnostic questions correct (exact counts not recorded)")
    assert spec.confidence == "a little sure (2/5)"
    assert spec.perceived_difficulty == "difficult (4/5)"
    assert spec.misconception is None
    assert spec.evidence_items == []


def test_no_performance_data_renders_nothing() -> None:
    state = ObjectiveLearnerState(lesson_objective_id="lop01", band="reinforce")
    spec = to_spec_objective_state(state)
    assert spec.mastery is None
    assert spec.confidence is None
    assert spec.perceived_difficulty is None


def test_session_signals_render_anchor_phrases() -> None:
    learner = LearnerState(student_id="s1", session_survey=SessionSurvey(interest=4, affect=2))
    signals = to_session_signals(learner)
    assert signals is not None
    assert signals.interest == "interested (4/5)"
    assert signals.end_of_lesson_feeling == "confused (2/5)"
    assert to_session_signals(LearnerState(student_id="s1")) is None
