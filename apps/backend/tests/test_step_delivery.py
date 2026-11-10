"""Where C1's manipulation stopped, step by step, and how the pack reports it.

`cohort_audit` says how much arrived; this says where. These pin the two together
— the per-step rows must sum to the ratios the cohort report publishes — and pin
the mechanism each miss is explained by, because an explanation counted from the
plan is the difference between a finding and a guess.

Regenerate the printable pack with:

    uv run python -m scripts.prompt_snapshots.delivery_pack
"""

from __future__ import annotations

import pytest

from app.domains.evaluation.application.worksheet_html.delivery_renderer import (
    render_delivery_audit_html,
)
from scripts.prompt_snapshots.cohort_audit import MANIPULATION_KEYS, frozen_lessons
from scripts.prompt_snapshots.delivery_pack import _context, _plain, detail
from scripts.prompt_snapshots.note_tasks import Disposition
from scripts.prompt_snapshots.step_delivery import _no_events, cohort_delivery

COHORT = cohort_delivery()
BY_LESSON = {lesson.lesson: lesson for lesson in COHORT}
STEPS = {step.step_id: step for lesson in COHORT for step in lesson.steps}


def test_every_core_step_is_one_call_and_the_cohort_is_seventeen() -> None:
    assert sum(len(lesson.steps) for lesson in COHORT) == 17


@pytest.mark.parametrize(
    ("key", "delivered"),
    [
        ("lesson_context.entry_behaviour", 17),
        ("lesson_context.instructional_materials", 17),
        ("unit_context.current_step", 17),
        ("unit_context.instructional_events", 16),
        ("unit_context.student_tasks", 9),
        ("unit_context.assessment_points", 10),
    ],
)
def test_the_per_step_rows_sum_to_the_published_cohort_ratio(key: str, delivered: int) -> None:
    assert sum(lesson.carried(key) for lesson in COHORT) == delivered


def test_only_t2_w09_carried_the_whole_manipulation_on_every_call() -> None:
    complete = {lesson.lesson for lesson in COHORT if all(step.complete for step in lesson.steps)}
    assert complete == {"t2-w09"}


def _reason(step_id: str, key: str) -> str:
    (miss,) = [m for m in STEPS[step_id].missing if m.key == key]
    return miss.reason


def test_a_step_whose_activity_codes_to_no_event_is_named_as_the_reason() -> None:
    assert "its 1 recorded activity coded to no Gagné event" in _reason(
        "step-t3w02-04", "unit_context.instructional_events"
    )


def test_a_step_with_no_activity_is_named_as_the_reason_events_are_missing() -> None:
    plan = frozen_lessons()["t3-w02"]
    step = next(s for s in plan.steps if s.step_id == "step-t3w02-04")
    bare = step.model_copy(update={"activities": []})
    assert "records no teacher or student activity" in _no_events(bare, plan)


def test_a_lesson_with_no_evaluation_step_is_named_rather_than_left_blank() -> None:
    assert BY_LESSON["t3-w06"].evaluation_steps == 0
    for step in BY_LESSON["t3-w06"].steps:
        reason = _reason(step.step_id, "unit_context.assessment_points")
        assert "no evaluation step at all" in reason


def test_an_objective_her_questions_skipped_is_told_which_ones_they_named() -> None:
    reason = _reason("step-t3w05-02", "unit_context.assessment_points")
    assert "her evaluation questions name" in reason
    assert "lo-t3w05-01" in reason


def test_a_missing_student_task_names_the_block_types_the_step_does_carry() -> None:
    reason = _reason("step-t3w04-02", "unit_context.student_tasks")
    assert "no block on this step is typed practice (3x explanation)" in reason
    assert "'take notes in their notebooks', which is reception" in reason
    # A step with neither route says so about both.
    assert "records no student activity" in _reason("step-t3w09-03", "unit_context.student_tasks")


def test_no_candidate_task_line_in_the_cohort_is_left_open() -> None:
    """Every task-shaped line she wrote is one she then solved or drew.

    This is what the delivery finding's R1 was raised to settle, and it says the
    thin `student_tasks` row is an absence in her plans rather than a
    transcription defect that a retype would recover.
    """
    dispositions = {task.disposition for step in STEPS.values() for task in step.tasks}
    assert dispositions == {Disposition.WORKED, Disposition.DEMONSTRATED}


def test_the_printed_line_drops_transcription_markup_and_keeps_her_line_breaks() -> None:
    assert _plain("**Example 1.** Calculate $V$") == "Example 1. Calculate V"
    assert _plain("1. Draw AB\n2. Mark O") == "1. Draw AB\n2. Mark O"
    assert _plain(r"angle $90^\circ$") == "angle 90°"
    assert _plain(r"$\angle ZOA$") == "∠ZOA"


def test_a_context_quote_is_one_line_and_bounded() -> None:
    quoted = _context("word " * 80)
    assert "\n" not in quoted
    assert quoted.endswith("…")
    assert len(quoted) <= 151


def test_the_rendered_pack_states_the_miss_and_offers_the_decision() -> None:
    html = render_delivery_audit_html(detail(COHORT, with_summary=True))
    assert "Lesson-plan delivery audit" in html
    assert "the lesson has no evaluation step at all" in html
    assert "work she demonstrated" in html
    # The summary carries every key the manipulation is made of, none dropped.
    for key in MANIPULATION_KEYS:
        assert key.split(".")[-1].replace("_", " ") in html


def test_a_single_lesson_pack_stands_alone_without_the_cohort_summary() -> None:
    html = render_delivery_audit_html(detail([BY_LESSON["t3-w06"]], with_summary=False))
    assert "The manipulation, per lesson" not in html
    assert "step-t3w06-06" in html


def test_work_she_set_without_question_text_now_reaches_c1() -> None:
    r"""A construction is work set, and it has no question to carry it.

    `student_tasks` read `practice` blocks only, so steps whose Student Activity column
    says *construct parallel lines* / *construct angle 90 degrees* delivered nothing.
    Reading the column too takes the key from 4/17 to 9/17, every one of the five gained
    a construction on t3-w06.

    Nine, not ten: the Gagné coder also scores *identify their properties* on
    t3-w02 as performance, and reading it against her step says otherwise — she draws,
    the class answers, she writes the properties up. `student_work.json` carries the
    read verdict and the coder's beside it.
    """
    assert sum(lesson.carried("unit_context.student_tasks") for lesson in COHORT) == 9
    assert BY_LESSON["t3-w06"].carried("unit_context.student_tasks") == 5


def test_only_performance_crosses_from_the_activity_column() -> None:
    """Reception is not work set, and the teacher's narration is never work at all."""
    from app.domains.artefacts.types.post_class_review_pack.application.request.source_content import (  # noqa: E501
        work_the_step_sets,
    )

    assert work_the_step_sets([{"who": "student", "what": "construct angle 90 degrees"}]) == [
        "construct angle 90 degrees"
    ]
    # A read verdict outranks the coder in both directions.
    assert (
        work_the_step_sets(
            [{"who": "student", "what": "construct angle 90 degrees", "sets_work": False}]
        )
        == []
    )
    assert work_the_step_sets(
        [{"who": "student", "what": "take notes in their notebooks", "sets_work": True}]
    ) == ["take notes in their notebooks"]
    assert work_the_step_sets([{"who": "student", "what": "take notes in their notebooks"}]) == []
    assert work_the_step_sets([{"who": "student", "what": "listen and ask questions"}]) == []
    # The exclusion this narrows: narration about the room never crosses, whatever verb
    # it uses. "Teacher draws the shapes" is the lesson as an event, not work set.
    assert work_the_step_sets([{"who": "teacher", "what": "draws the various shapes"}]) == []


def test_her_own_questions_win_where_a_step_has_both() -> None:
    """The activity is a label for the questions, not a second task.

    Every cohort step carrying both has an activity that points at the block beside it
    — "solve some questions independently" against four listed questions — so appending
    it would send a contentless task and say nothing the block has not.
    """
    from app.domains.artefacts.types.post_class_review_pack.application.request.units import (
        SectionGenerationUnitProjector,
    )
    from app.shared.session_plan_view import SessionPlanStepView

    step = SessionPlanStepView(
        step_id="step-x",
        step_kind="core",
        activities=[{"who": "student", "what": "solve some questions independently"}],
        blocks=[{"type": "practice", "question": "Simplify 4n + 3n"}],
    )
    assert SectionGenerationUnitProjector._student_tasks(step) == ["Simplify 4n + 3n"]


def test_the_runner_defaults_to_the_harness_production_ships() -> None:
    """A run left on its defaults must measure the system that deploys.

    The study judged compose-v2/leveled while production wired GenerateSection, and
    nothing said so — the arm travelled in the run record, but no check compared it
    with the wiring. Reads the parsed defaults rather than the source, so a refactor
    that moves the argument definitions cannot make this pass vacuously.
    """
    import inspect

    from app.domains.artefacts.types.post_class_review_pack.infrastructure import (
        generation_wiring,
    )
    from experiments.h1_condition_eval.runner import _parser

    defaults = _parser().parse_args([])
    assert defaults.generator == "compose-v2"
    assert defaults.signatures == "leveled"

    wired = inspect.getsource(generation_wiring.section_collaborators)
    assert "ComposeSection(" in wired
    assert 'contract_mode="leveled"' in wired
    assert "dspy.ReActV2" in wired
