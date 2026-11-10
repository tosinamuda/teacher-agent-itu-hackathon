"""A plan is held to the study's lesson document and to the lesson-plan spec."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from app.domains.artefacts.types.lesson_plan.domain.lesson_document import as_document, violations
from app.domains.artefacts.types.lesson_plan.domain.plan_requirements import unmet
from experiments.h1_condition_eval.lesson_document import load
from experiments.h1_condition_eval.lesson_plan_projection import plan

LESSONS = Path(__file__).parent.parent / "experiments/h1_condition_eval/lessons"
#: Every lesson the study observed ran for one 40-minute period.
STUDY_LESSON_MINUTES = 40

PLAN = {
    "plan_id": "LP-1",
    "session_id": "s1",
    "subject": "Mathematics",
    "track": "core",
    "grade": "JSS1",
    "term": "First Term",
    "week": 4,
    "topic": "Fractions",
    "subtopic": "Mixed fractions",
    "curriculum_objectives": [
        {"curriculum_objective_id": "co1", "objective_text": "Convert fractions"}
    ],
    "lesson_plan_objectives": [
        {
            "lesson_objective_id": "lo1",
            "objective_text": "convert improper fractions to mixed numbers",
            "curriculum_objective_id": "co1",
            "kc_type": "procedure",
        }
    ],
    "entry_behaviour": ["proper and improper fractions"],
    "instructional_materials": ["fraction charts"],
    "references": [],
    "steps": [
        {
            "step_id": "intro",
            "step_kind": "intro",
            "title": "Warm-up",
            "content": "Recall proper and improper fractions.",
            "estimated_minutes": 5,
            "activities": [
                {"who": "teacher", "what": "Asks for examples."},
                {"who": "student", "what": "Give examples.", "sets_work": False},
            ],
        },
        {
            "step_id": "step1",
            "step_kind": "core",
            "lesson_objective_id": "lo1",
            "title": "Divide and keep the remainder",
            "content": "Work examples on the board.",
            "estimated_minutes": 20,
            "activities": [
                {"who": "teacher", "what": "Works three examples."},
                {"who": "student", "what": "Convert four fractions.", "sets_work": True},
            ],
        },
        {
            "step_id": "evaluation",
            "step_kind": "evaluation",
            "title": "Evaluation",
            "content": "Check mastery.",
            "estimated_minutes": 10,
            "blocks": [
                {
                    "id": "evaluation:q1",
                    "type": "practice",
                    "question": "Convert 22/5.",
                    "answer": "4 2/5",
                    "lesson_objective_id": "lo1",
                }
            ],
        },
    ],
}


def _with(change) -> dict:
    plan = copy.deepcopy(PLAN)
    change(plan)
    return plan


def test_a_plan_that_keeps_the_grammar_and_its_references_has_no_violations() -> None:
    document = as_document(PLAN)

    assert violations(document) == []
    assert document.find("step[@id='evaluation']/questions/question").get("id") == "q1"
    assert document.find("step[@id='step1']/activities/activity[2]").get("sets-work") == "true"


def test_an_objective_citing_an_undeclared_curriculum_objective_is_refused() -> None:
    def cite_nothing(plan):
        plan["lesson_plan_objectives"][0]["curriculum_objective_id"] = "co9"

    assert violations(as_document(_with(cite_nothing))) == [
        "lo1: curriculum objective 'co9' is not declared"
    ]


def test_a_core_step_that_teaches_no_objective_is_refused() -> None:
    def untether(plan):
        del plan["steps"][1]["lesson_objective_id"]

    assert "step1: a core step must name the objective it teaches" in violations(
        as_document(_with(untether))
    )


def test_an_id_the_grammar_cannot_hold_is_refused_by_the_grammar() -> None:
    def colon(plan):
        plan["steps"][1]["step_id"] = "step:1"

    assert violations(as_document(_with(colon)))[0].startswith("lesson.rng:")


def test_the_spec_is_met_by_a_plan_that_says_what_each_activity_sets_and_fits_its_time() -> None:
    assert unmet(PLAN, duration_minutes=40) == []


def test_a_core_student_activity_that_does_not_say_whether_it_sets_work_is_unmet() -> None:
    def unsaid(plan):
        del plan["steps"][1]["activities"][1]["sets_work"]

    assert unmet(_with(unsaid), duration_minutes=40) == [
        "step1: a student activity does not say whether it sets the students work of their "
        "own ('Convert four fractions.')"
    ]


def test_an_introduction_need_not_say_whether_it_sets_work_as_the_study_s_did_not() -> None:
    def unsaid(plan):
        del plan["steps"][0]["activities"][1]["sets_work"]

    assert unmet(_with(unsaid), duration_minutes=40) == []


def test_steps_that_overrun_the_lesson_are_unmet() -> None:
    assert unmet(PLAN, duration_minutes=30) == [
        "the steps take 35 minutes (intro 5, step1 20, evaluation 10); the lesson is 30, "
        "so take 5 minutes off"
    ]


def test_a_lesson_without_an_evaluation_meets_the_spec_as_t3_w06_did() -> None:
    def no_evaluation(plan):
        plan["steps"].pop()

    assert unmet(_with(no_evaluation), duration_minutes=40) == []


def test_a_lesson_that_does_not_open_with_an_introduction_is_unmet() -> None:
    def no_intro(plan):
        plan["steps"].pop(0)

    assert unmet(_with(no_intro), duration_minutes=40) == [
        "steps run ['core', 'evaluation']: an introduction, then the core steps"
    ]


def test_an_objective_no_core_step_teaches_is_unmet() -> None:
    def second_objective(plan):
        plan["lesson_plan_objectives"].append(
            {"lesson_objective_id": "lo2", "objective_text": "x", "curriculum_objective_id": "co1"}
        )

    assert unmet(_with(second_objective), duration_minutes=40) == ["lo2: no core step teaches it"]


@pytest.mark.parametrize("lesson", sorted(LESSONS.glob("t*.xml")), ids=lambda path: path.stem)
def test_the_spec_asks_exactly_what_the_study_s_lesson_plans_did(lesson) -> None:
    study_plan = plan(load(lesson))

    assert violations(as_document(study_plan)) == []
    assert unmet(study_plan, duration_minutes=STUDY_LESSON_MINUTES) == []
