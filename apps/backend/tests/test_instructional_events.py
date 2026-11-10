"""The Gagné coding of the field plans' Presentation activities.

The codebook is frozen before generation and applied identically to every lesson, so the
corpus table below IS the guard: any change to a rule shows up as a changed coding on a
named step rather than as a silent drift in what C1 transmits.
"""

from __future__ import annotations

import json

import pytest

from app.domains.artefacts.types.lesson_plan.drafting.domain.instructional_events import (
    event_of,
    instructional_events,
)
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH

CASES = {c["lesson"]: c for c in json.loads(EVAL_SET_PATH.read_text())["cases"]}

# Every step of every lesson, coded by hand. `()` is a step with nothing to code: t2-w09's and
# t3-w05's intros are the cleaner's scaffold and carry no activity, and t3-w02's perimeter step
# has one — she works the perimeters on the board — that names no Gagné event.
CORPUS: dict[str, tuple[str, ...]] = {
    "step-t2w09-01": (),
    "step-t2w09-02": ("provide_learning_guidance", "elicit_performance", "provide_feedback"),
    "step-t2w09-03": ("provide_learning_guidance", "elicit_performance", "provide_feedback"),
    "step-t2w09-04": ("provide_learning_guidance", "elicit_performance", "provide_feedback"),
    "step-t3w02-01": ("present_content", "elicit_performance", "provide_feedback"),
    "step-t3w02-02": ("present_content", "elicit_performance", "present_content"),
    "step-t3w02-03": ("present_content",),
    "step-t3w02-04": (),
    "step-t3w04-01": ("stimulate_recall", "elicit_performance", "provide_feedback"),
    "step-t3w04-02": ("present_content",),
    "step-t3w04-03": ("present_content",),
    "step-t3w05-01": (),
    "step-t3w05-02": ("present_content", "elicit_performance", "present_content"),
    "step-t3w05-03": ("present_content", "provide_learning_guidance"),
    # Six steps since her compound objective (i) was split into parallel + perpendicular,
    # restoring her own Presentation. step-02 gains her narration back — it had been
    # displaced by a researcher note, so the step coded to nothing at all.
    "step-t3w06-01": ("present_content", "elicit_performance"),
    "step-t3w06-02": ("present_content", "elicit_performance"),
    "step-t3w06-03": ("present_content", "elicit_performance"),
    "step-t3w06-04": ("present_content", "elicit_performance"),
    "step-t3w06-05": ("present_content", "elicit_performance"),
    "step-t3w06-06": ("present_content", "elicit_performance"),
    "step-t3w09-01": ("elicit_performance",),
    "step-t3w09-02": ("present_content",),
    "step-t3w09-03": ("provide_feedback",),
}


@pytest.mark.parametrize("lesson", sorted(CASES))
def test_the_corpus_codes_as_it_was_coded_by_hand(lesson: str) -> None:
    for step in CASES[lesson]["plan"]["steps"]:
        if step["step_kind"] == "evaluation":
            continue
        coded = tuple(instructional_events(step.get("activities") or []))
        assert coded == CORPUS[step["step_id"]], step["step_id"]


def test_every_coded_step_is_in_the_table() -> None:
    """A new step must be coded deliberately, not default to nothing."""
    seen = {
        step["step_id"]
        for case in CASES.values()
        for step in case["plan"]["steps"]
        if step["step_kind"] != "evaluation"
    }
    assert seen == set(CORPUS)


def test_all_five_observed_events_occur() -> None:
    """The four unused Gagné events stay unused; these five are what her plans license."""
    fired = {
        event
        for case in CASES.values()
        for step in case["plan"]["steps"]
        for event in instructional_events(step.get("activities") or [])
    }
    assert fired == {
        "stimulate_recall",
        "present_content",
        "provide_learning_guidance",
        "elicit_performance",
        "provide_feedback",
    }


@pytest.mark.parametrize(
    "what",
    [
        "listen, contribute, and where necessary ask questions where they do not understand",
        "take notes in their notebooks",
        "take them down, as in Step II",
        "listen and ask questions where they do not understand",
    ],
)
def test_reception_takes_no_code(what: str) -> None:
    """A learner receiving is not a learner performing.

    "Ask questions where they do not understand" is the learner seeking clarification —
    the opposite of eliciting performance, and a rule matching "asks questions" without
    regard to the actor codes it backwards.
    """
    assert event_of({"who": "student", "what": what}) is None


def test_a_teacher_putting_questions_to_the_class_elicits() -> None:
    assert event_of({"who": "teacher", "what": "asks questions such as how many boys"}) == (
        "elicit_performance"
    )


def test_marking_beats_the_answering_it_contains() -> None:
    """One activity, one code: the dominant function of a multi-verb entry."""
    activity = {
        "who": "teacher",
        "what": "moves round to monitor their work, answer their questions, "
        "mark their notes and mark correction",
    }
    assert event_of(activity) == "provide_feedback"


def test_the_code_names_the_function_not_the_actor() -> None:
    """ "They copy worked examples" states that the worked-example function operates."""
    assert event_of({"who": "student", "what": "copy worked examples into their notes"}) == (
        "provide_learning_guidance"
    )


def test_the_same_verb_codes_by_who_performs_it() -> None:
    solving = "solve some questions independently"
    assert event_of({"who": "teacher", "what": "solves some questions on the board"}) == (
        "provide_learning_guidance"
    )
    assert event_of({"who": "student", "what": solving}) == "elicit_performance"


def test_prior_knowledge_must_be_planned_as_an_activity() -> None:
    """Listing prerequisites is not planning a recall step, and the difference is signal.

    `t3-w04` plans one and codes `stimulate_recall`; `t3-w05` lists the same kind of
    prerequisites in *Previous knowledge* and plans no activity for them.
    """
    planned = {
        "who": "teacher",
        "what": "asks the students some questions based on their previous knowledge",
    }
    assert event_of(planned) == "stimulate_recall"
    t3w05 = next(s for s in CASES["t3-w05"]["plan"]["steps"] if s["step_kind"] == "intro")
    assert CASES["t3-w05"]["plan"]["entry_behaviour"]
    assert instructional_events(t3w05.get("activities") or []) == []


def test_consecutive_duplicates_collapse() -> None:
    activities = [
        {"who": "teacher", "what": "explains the parts of a circle"},
        {"who": "teacher", "what": "draws the various shapes on the board"},
        {"who": "student", "what": "identify their properties"},
    ]
    assert instructional_events(activities) == ["present_content", "elicit_performance"]
