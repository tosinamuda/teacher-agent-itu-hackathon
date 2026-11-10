"""Deterministic assembly of the lesson-plan evaluation step.

The evaluation step is a no-latitude transcription of the per-objective curated
``AssessmentItem``s. Letting the LLM re-author it was the source of the stochastic
"evaluation steps require at least one practice block" crash. ``build_evaluation_step``
now assembles it deterministically — these tests pin: one practice block per item, the
``lesson_objective_id`` dict-key fallback, the strict ``PlannerPlanStep`` evaluation
invariant is satisfied, the empty-input guard, and that the assembled ``GlobalStepSet``
validates.
"""

from __future__ import annotations

import pytest

from app.domains.artefacts.types.lesson_plan.drafting.domain.evaluation_step import (
    build_evaluation_step,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    AssessmentItem,
    GlobalStepSet,
    PlannerPlanStep,
)


def _item(
    question: str,
    *,
    expected_answer: str = "42",
    lesson_objective_id: str | None = None,
    kc_id: str = "kc01",
) -> AssessmentItem:
    return AssessmentItem(
        kc_id=kc_id,
        lesson_objective_id=lesson_objective_id,
        question=question,
        expected_answer=expected_answer,
        bloom_justification="Assesses the objective at the apply level.",
    )


def test_one_practice_block_per_item_in_objective_order() -> None:
    step = build_evaluation_step(
        {
            "lop01": _item(
                "What is 2,000,000 + 1,000,000?",
                expected_answer="3,000,000",
                lesson_objective_id="lop01",
            ),
            "lop02": _item(
                "Write 4,500,000 in words.",
                expected_answer="four million five hundred thousand",
                lesson_objective_id="lop02",
            ),
        }
    )

    assert step.step_kind == "evaluation"
    # The strict PlannerPlanStep validator sets instructional_type for evaluation steps.
    assert step.instructional_type == "check"
    assert [block.type for block in step.blocks] == ["practice", "practice"]
    assert [block.question for block in step.blocks] == [
        "What is 2,000,000 + 1,000,000?",
        "Write 4,500,000 in words.",
    ]
    assert [block.answer for block in step.blocks] == [
        "3,000,000",
        "four million five hundred thousand",
    ]
    assert [block.lesson_objective_id for block in step.blocks] == ["lop01", "lop02"]


def test_lesson_objective_id_falls_back_to_dict_key() -> None:
    # The item omits its own lesson_objective_id; the dict key (objective id) supplies it
    # so the evaluation invariant (every practice block carries a lesson_objective_id) holds.
    step = build_evaluation_step({"lop07": _item("Q", lesson_objective_id=None)})
    assert step.blocks[0].lesson_objective_id == "lop07"


def test_skips_items_without_any_objective_but_keeps_the_rest() -> None:
    # An empty dict key + missing item id cannot satisfy the invariant for that one,
    # but the others still assemble (graceful, never a crash).
    step = build_evaluation_step(
        {
            "": _item("orphan", lesson_objective_id=None),
            "lop03": _item("kept", lesson_objective_id="lop03"),
        }
    )
    assert [block.lesson_objective_id for block in step.blocks] == ["lop03"]


def test_raises_only_when_no_usable_item_exists() -> None:
    with pytest.raises(ValueError):
        build_evaluation_step({})
    with pytest.raises(ValueError):
        build_evaluation_step({"": _item("orphan", lesson_objective_id=None)})


def test_assembled_global_step_set_validates() -> None:
    intro = PlannerPlanStep(
        step_id="step-intro",
        step_kind="intro",
        title="Recap",
        content="Activate prior knowledge on place value.",
        estimated_minutes=5,
    )
    evaluation = build_evaluation_step({"lop01": _item("Q1", lesson_objective_id="lop01")})

    global_steps = GlobalStepSet(intro_step=intro, evaluation_step=evaluation)

    assert global_steps.intro_step.instructional_type is None
    assert global_steps.evaluation_step.step_kind == "evaluation"
    assert len(global_steps.evaluation_step.blocks) == 1
