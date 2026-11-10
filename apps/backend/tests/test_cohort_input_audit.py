"""The manipulation C1 was designed to carry did not fully reach the frozen cohort.

These pin the audit's findings so a later data fix, or a projection change, shows up as a
failure here rather than as a quietly different report. The numbers are the study's, read
off `eval_set.json` through the same rendering path the snapshots use.

Regenerate the artefact with:

    uv run python -m scripts.prompt_snapshots.cohort_audit
"""

from __future__ import annotations

import pytest

from scripts.prompt_snapshots.cohort_audit import (
    MANIPULATION_KEYS,
    REPORT_PATH,
    audit,
    frozen_lessons,
    report,
)

AUDITS = {(a.lesson, a.condition): a for a in audit()}
LESSONS = sorted({lesson for lesson, _ in AUDITS})
C1_UNITS = sum(AUDITS[(lesson, "C1")].units for lesson in LESSONS)


def _delivered(key: str) -> int:
    return sum(AUDITS[(lesson, "C1")].carried(key) for lesson in LESSONS)


def test_the_audit_covers_the_whole_frozen_set() -> None:
    assert LESSONS == ["t2-w09", "t3-w02", "t3-w04", "t3-w05", "t3-w06", "t3-w09"]
    assert C1_UNITS == 17


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
def test_how_much_of_the_manipulation_reached_the_cohort(key: str, delivered: int) -> None:
    """Three keys arrived everywhere; two did not, and one barely."""
    assert _delivered(key) == delivered


def test_student_tasks_is_still_the_thinnest_key_and_still_uneven() -> None:
    """The headline: C1 is not one condition across the cohort but a ragged set of them.

    It reached 4 of 17 while the field read question-shaped blocks alone, and 9 of 17
    once it also read a Student Activity her Gagné coder scores as performance. Still
    the thinnest key by a distance, and still uneven across the lessons.
    """
    assert _delivered("unit_context.student_tasks") / C1_UNITS < 0.6
    assert (
        min(AUDITS[(lesson, "C1")].carried("unit_context.student_tasks") for lesson in LESSONS) == 0
    )


def test_the_thin_rows_are_thin_for_a_structural_reason_not_a_bug() -> None:
    """Every delivering call has a source in her plan, and the two sources partition.

    Her question blocks carry four. Five more steps set work in the Student Activity
    column with no question text to hold it — a construction has none — and nothing
    else in the plan is read. The count is the sum, so a delivery figure can always be
    traced back to something she wrote.
    """
    from app.domains.artefacts.types.post_class_review_pack.application.request.source_content import (  # noqa: E501
        work_the_step_sets,
    )

    core = [
        step
        for plan in frozen_lessons().values()
        for step in plan.steps
        if step.step_kind == "core"
    ]
    practice = [s for s in core if any(str(b.get("type") or "") == "practice" for b in s.blocks)]
    from_activity = [s for s in core if s not in practice and work_the_step_sets(s.activities)]

    assert len(practice) == 4
    assert len(from_activity) == 5
    assert _delivered("unit_context.student_tasks") == len(practice) + len(from_activity)


def test_a_lesson_with_no_evaluation_step_carries_no_assessment_points() -> None:
    without = [
        lesson
        for lesson, plan in frozen_lessons().items()
        if not any(step.step_kind == "evaluation" for step in plan.steps)
    ]

    assert without == ["t3-w06"]
    assert AUDITS[("t3-w06", "C1")].carried("unit_context.assessment_points") == 0


def test_no_c0_call_carries_any_of_the_manipulation() -> None:
    """The floor of the comparison: whatever C1 got, C0 got none of it."""
    leaked = {
        (lesson, key)
        for lesson in LESSONS
        for key in MANIPULATION_KEYS
        if AUDITS[(lesson, "C0")].carried(key)
    }

    assert leaked == set()


def test_the_evidence_step_reached_every_grounded_call() -> None:
    """Unlike the plan fields, the C2/C3 manipulation is fully delivered."""
    for lesson in LESSONS:
        for condition in ("C2", "C3"):
            entry = AUDITS[(lesson, condition)]
            assert entry.evidence_units == entry.units, f"{lesson} {condition}"
        assert AUDITS[(lesson, "C0")].evidence_units == 0
        assert AUDITS[(lesson, "C1")].evidence_units == 0


def test_the_committed_artefact_matches_a_fresh_run() -> None:
    assert REPORT_PATH.exists(), "the dated cohort audit is not committed"
    assert REPORT_PATH.read_text(encoding="utf-8") == report(), (
        "the cohort audit is stale — regenerate with "
        "`uv run python -m scripts.prompt_snapshots.cohort_audit`"
    )
