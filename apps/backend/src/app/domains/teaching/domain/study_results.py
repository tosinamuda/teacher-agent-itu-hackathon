"""The evaluation's marks for a lesson, read as a class's results: each learner's band by objective.

The study's classwork was written answers, marked correct or incorrect by the teacher, and a
mark the teacher left out is no answer to count. A learner is placed as a class test places one:
by the weakest of their objectives.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from app.domains.learner_state.domain.models import ObjectiveBand
from app.domains.teaching.domain.class_test_outcome import objective_outcomes, outcome_of
from app.shared.json_types import JsonObject


@dataclass(frozen=True)
class MarkedAnswer:
    lesson_objective_id: str
    #: `correct`, `incorrect` or `unmarked`, as the teacher marked it.
    mark: str
    misconception_code: str | None


@dataclass(frozen=True)
class MarkedScript:
    student_id: str
    full_name: str
    #: The total the teacher wrote on the script, such as `1/4`.
    teacher_total: str
    answers: list[MarkedAnswer]


@dataclass(frozen=True)
class ObjectiveResult:
    lesson_objective_id: str
    band: ObjectiveBand
    correct: int
    out_of: int
    misconceptions: list[str]


@dataclass(frozen=True)
class LearnerStudyResult:
    student_id: str
    full_name: str
    teacher_total: str
    band: ObjectiveBand
    correct: int
    out_of: int
    objectives: list[ObjectiveResult]


def _diagnostic_results(answers: list[MarkedAnswer]) -> JsonObject:
    """The marks as the learner state reads a test's results: a score for each objective."""
    scores: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    codes: dict[str, str] = {}
    for answer in answers:
        if answer.mark == "unmarked":
            continue
        score = scores[answer.lesson_objective_id]
        score[1] += 1
        if answer.mark == "correct":
            score[0] += 1
        elif answer.misconception_code and answer.lesson_objective_id not in codes:
            codes[answer.lesson_objective_id] = answer.misconception_code
    return {
        "objectives": [
            {
                "lesson_objective_id": objective,
                "score": correct,
                "max_score": total,
                **({"misconception_code": codes[objective]} if objective in codes else {}),
            }
            for objective, (correct, total) in scores.items()
        ]
    }


def _misconceptions(answers: list[MarkedAnswer]) -> dict[str, list[str]]:
    found: dict[str, list[str]] = defaultdict(list)
    for answer in answers:
        code = answer.misconception_code
        if answer.mark == "incorrect" and code and code not in found[answer.lesson_objective_id]:
            found[answer.lesson_objective_id].append(code)
    return found


def learner_results(scripts: list[MarkedScript]) -> list[LearnerStudyResult]:
    """Each learner who answered something, the weakest first, then by name."""
    results: list[LearnerStudyResult] = []
    for script in scripts:
        diagnostic = _diagnostic_results(script.answers)
        outcome = outcome_of(script.student_id, diagnostic)
        if outcome is None or outcome.correct is None or outcome.out_of is None:
            continue
        codes = _misconceptions(script.answers)
        results.append(
            LearnerStudyResult(
                student_id=script.student_id,
                full_name=script.full_name,
                teacher_total=script.teacher_total,
                band=outcome.band,
                correct=outcome.correct,
                out_of=outcome.out_of,
                objectives=[
                    ObjectiveResult(
                        lesson_objective_id=o.lesson_objective_id,
                        band=o.band,
                        correct=o.correct or 0,
                        out_of=o.out_of or 0,
                        misconceptions=codes.get(o.lesson_objective_id, []),
                    )
                    for o in objective_outcomes(script.student_id, diagnostic)
                ],
            )
        )
    order = ("remediate", "reinforce", "extend")
    return sorted(results, key=lambda r: (order.index(r.band), r.full_name))
