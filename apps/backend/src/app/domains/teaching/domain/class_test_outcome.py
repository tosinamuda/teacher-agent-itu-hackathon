"""How a learner did on a class test: the score, and the band their weakest objective gives."""

from __future__ import annotations

from dataclasses import dataclass

from app.domains.learner_state.application.service import LearnerStateService
from app.domains.learner_state.domain.models import ObjectiveBand
from app.shared.json_types import JsonObject

# Weakest first: a learner is placed by their greatest need, as a focal case is.
_WEAKEST_FIRST: tuple[ObjectiveBand, ...] = ("remediate", "reinforce", "extend")


@dataclass(frozen=True)
class ClassTestOutcome:
    band: ObjectiveBand
    correct: int | None
    out_of: int | None


def outcome_of(student_id: str, results: JsonObject) -> ClassTestOutcome | None:
    """The outcome of one submission, or None when it holds no objective to place the learner by."""
    states = (
        LearnerStateService()
        .build(student_id=student_id, student_profile=None, diagnostic_results=results)
        .objective_states
    )
    if not states:
        return None
    bands = {state.band for state in states}
    band = next(band for band in _WEAKEST_FIRST if band in bands)
    counted = all(
        state.questions_correct is not None and state.questions_total is not None
        for state in states
    )
    if not counted:
        return ClassTestOutcome(band=band, correct=None, out_of=None)
    return ClassTestOutcome(
        band=band,
        correct=sum(state.questions_correct or 0 for state in states),
        out_of=sum(state.questions_total or 0 for state in states),
    )


@dataclass(frozen=True)
class ObjectiveOutcome:
    lesson_objective_id: str
    band: ObjectiveBand
    correct: int | None
    out_of: int | None


def objective_outcomes(student_id: str, results: JsonObject) -> list[ObjectiveOutcome]:
    """How the learner did on each objective the test covered."""
    states = (
        LearnerStateService()
        .build(student_id=student_id, student_profile=None, diagnostic_results=results)
        .objective_states
    )
    return [
        ObjectiveOutcome(
            lesson_objective_id=state.lesson_objective_id,
            band=state.band,
            correct=state.questions_correct,
            out_of=state.questions_total,
        )
        for state in states
    ]
