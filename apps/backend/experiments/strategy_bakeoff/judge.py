"""LLM-judge primary outcome for the strategy bake-off.

This is the experiment's HEADLINE metric, deliberately INDEPENDENT of the
deterministic semantic_score that drives self-correction/GEPA (judge != target,
pre-registration §4a). The judge scores a generated lesson plan on the project's
REAL expert-evaluation rubric (H1_RUBRIC, mirrored from
app/domains/evaluation/application/service.py) so the experiment predicts the
downstream human expert eval.

Integrity properties:
  * Blind — the judge sees only the plan + reference sheet, never the strategy
    name or which cell produced it.
  * Rubric-anchored — uses the exact criterion ids/descriptions experts use.
  * Independent model — judge LM is configurable (JUDGE_DSPY_MODEL) so it can
    differ from the generation LM, reducing self-preference bias.
  * Proxy, not truth — labelled as an automated proxy; the human expert eval
    remains ground truth. Validate against a few human ratings before trusting.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

import dspy

from app.infra.dspy_lm import active_model_name
from app.shared.json_types import JsonObject

# Mirror of H1_RUBRIC (evaluation/application/service.py), 1-5 scale.
H1_CRITERIA: tuple[tuple[str, str], ...] = (
    (
        "objective_coverage",
        "How fully the lesson plan covers the intended lesson objectives.",
    ),
    (
        "scope_compliance",
        "Whether the plan stays within the lesson scope without drifting.",
    ),
    (
        "textbook_factual_fidelity",
        "Whether explanations and examples stay faithful to the lesson basis.",
    ),
    (
        "pedagogical_appropriateness",
        "Whether the plan matches the lesson purpose and cognitive demand.",
    ),
)
SCALE_MIN = 1
SCALE_MAX = 5


class JudgeLessonPlanSignature(dspy.Signature):
    """Rate a generated lesson plan on the expert rubric.

    You are an expert teacher evaluating a single lesson plan for JSS1
    mathematics. Score ONLY on the rubric criteria. Be strict and consistent.
    Each score is an integer from 1 (poor) to 5 (excellent). Do not reward
    verbosity. Judge against the reference sheet (the intended curriculum scope,
    objectives, and instructional materials), not your own preferences.
    """

    reference_sheet = dspy.InputField(
        desc="The intended lesson: subject/grade/topic/subtopic, curriculum "
        "objectives, instructional materials. The plan should serve THIS."
    )
    lesson_plan = dspy.InputField(
        desc="The generated lesson plan to evaluate (objectives, steps, "
        "assessments). No strategy/source label is provided — judge blind."
    )
    objective_coverage: int = dspy.OutputField(desc="1-5: coverage of intended objectives.")
    scope_compliance: int = dspy.OutputField(desc="1-5: stays within lesson scope.")
    textbook_factual_fidelity: int = dspy.OutputField(desc="1-5: faithful to the lesson basis.")
    pedagogical_appropriateness: int = dspy.OutputField(desc="1-5: fits purpose/cognitive demand.")
    justification: str = dspy.OutputField(desc="One sentence per criterion, terse.")


@dataclass(frozen=True)
class JudgeScore:
    """Per-criterion rubric scores from the LLM judge."""

    scores: dict[str, int] = field(default_factory=dict)
    justification: str = ""
    error: str | None = None

    @property
    def overall(self) -> float | None:
        if not self.scores:
            return None
        return round(sum(self.scores.values()) / len(self.scores), 3)

    @property
    def ok(self) -> bool:
        return self.error is None and len(self.scores) == len(H1_CRITERIA)


def _clamp(value: object) -> int:
    try:
        score = int(value)
    except (TypeError, ValueError):
        return SCALE_MIN
    return max(SCALE_MIN, min(SCALE_MAX, score))


def _reference_sheet(session_plan: JsonObject) -> JsonObject:
    """Intended-lesson view the judge scores against (no strategy hints)."""
    return {
        "subject": session_plan.get("subject"),
        "grade": session_plan.get("grade"),
        "term": session_plan.get("term"),
        "topic": session_plan.get("topic"),
        "subtopic": session_plan.get("subtopic"),
        "curriculum_objectives": session_plan.get("curriculum_objectives"),
        "instructional_materials": session_plan.get("instructional_materials"),
    }


def _plan_view(session_plan: JsonObject) -> JsonObject:
    """The plan content the judge reads — strategy-agnostic, no provenance."""
    return {
        "lesson_plan_objectives": session_plan.get("lesson_plan_objectives"),
        "steps": session_plan.get("steps"),
        "assessments": session_plan.get("assessments"),
    }


class LessonPlanJudge:
    """Wraps the judge signature with an independent (configurable) LM."""

    def __init__(self, *, model: str | None = None) -> None:
        self.model = (
            model or os.getenv("JUDGE_DSPY_MODEL") or os.getenv("DSPY_MODEL") or active_model_name()
        )
        self._lm = dspy.LM(model=self.model)
        self._judge = dspy.ChainOfThought(JudgeLessonPlanSignature)

    def score(self, session_plan: JsonObject | None) -> JudgeScore:
        if not session_plan:
            return JudgeScore(error="no_session_plan")
        try:
            with dspy.context(lm=self._lm):
                result = self._judge(
                    reference_sheet=_reference_sheet(session_plan),
                    lesson_plan=_plan_view(session_plan),
                )
            scores = {
                criterion_id: _clamp(getattr(result, criterion_id, None))
                for criterion_id, _ in H1_CRITERIA
            }
            return JudgeScore(
                scores=scores,
                justification=str(getattr(result, "justification", "") or ""),
            )
        except Exception as exc:  # noqa: BLE001 - judge failure is recorded, not fatal
            return JudgeScore(error=f"{type(exc).__name__}: {exc}")
