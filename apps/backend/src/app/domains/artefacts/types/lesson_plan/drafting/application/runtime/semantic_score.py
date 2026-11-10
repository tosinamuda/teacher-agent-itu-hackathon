"""Reusable semantic score for generated lesson plans.

A single deterministic scorer wrapping `SemanticPlanValidator.collect_issues`.
Every strategy that needs a pass/fail or graded judgement uses THIS, so they all
optimise against the same target:

  * dspy.Refine  -> reward_fn   (retry until score == 1.0)
  * dspy.GEPA    -> metric      (prompt optimisation)
  * dspy.ReAct   -> verify tool (agent calls it, reads violations, fixes)
  * bake-off     -> scorer      (compare strategies on equal footing)

Score is 1.0 when there are no semantic violations, otherwise it decays with the
number of violations so partial improvement is visible to optimisers/refiners.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
    LessonCurriculumContext,
    TextbookRecordPayload,
)
from app.shared.json_types import JsonObject

from ...schemas.session_plan import CandidateKC, LessonPlanObjective, StepEvidencePlan
from .semantic_validation import SemanticPlanValidator

_NULL_LOGGER = logging.getLogger("lesson_plan.semantic_score")

_PENALTY_UNIT = 0.34


@dataclass(frozen=True)
class SemanticScore:
    """Graded semantic-validation result."""

    score: float
    violations: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.violations

    def feedback(self) -> str:
        """Human/LLM-readable summary for refine/react feedback loops."""
        if self.passed:
            return "All semantic checks passed."
        return "Fix these semantic violations:\n- " + "\n- ".join(self.violations)


def score_from_issues(issues: list[str]) -> SemanticScore:
    """Grade a list of violation strings. 1.0 = clean; decays per violation."""
    if not issues:
        return SemanticScore(score=1.0, violations=[])
    score = max(0.0, 1.0 - _PENALTY_UNIT * len(issues))
    return SemanticScore(score=score, violations=list(issues))


def score_session_plan(
    *,
    lesson_plan_objectives: list[LessonPlanObjective],
    resolved_kcs: list[CandidateKC],
    step_evidence_by_objective: dict[str, StepEvidencePlan],
    global_steps: dict[str, JsonObject],
    textbook_records: list[TextbookRecordPayload],
    curriculum_context: LessonCurriculumContext,
    validator: SemanticPlanValidator | None = None,
) -> SemanticScore:
    """Score a drafted plan against the semantic constraints.

    1.0 = clean. Each violation subtracts an equal share down to a 0.0 floor, so
    "2 of 3 checks fixed" reads as a higher score than "0 fixed" — useful as a
    Refine reward and a GEPA metric, not just a boolean gate.
    """
    validator = validator or SemanticPlanValidator(logger=_NULL_LOGGER)
    issues = validator.collect_issues(
        lesson_plan_objectives=lesson_plan_objectives,
        resolved_kcs=resolved_kcs,
        step_evidence_by_objective=step_evidence_by_objective,
        global_steps=global_steps,
        textbook_records=textbook_records,
        curriculum_context=curriculum_context,
    )
    return score_from_issues(issues)
