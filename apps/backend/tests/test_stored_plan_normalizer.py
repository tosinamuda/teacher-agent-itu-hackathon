from app.domains.artefacts.types.lesson_plan.drafting.domain.normalizers import (
    normalize_session_plan_payload,
)


def test_a_step_stored_with_two_activity_lists_reads_as_one_ordered_list() -> None:
    stored = {
        "steps": [
            {
                "step_id": "s1",
                "title": "Intro",
                "mode": "Direct instruction",
                "teacher_activities": ["Show the chart.", " "],
                "student_activities": ["Classify three fractions."],
            }
        ]
    }

    [step] = normalize_session_plan_payload(stored)["steps"]  # type: ignore[misc]

    assert step["activities"] == [
        {"who": "teacher", "what": "Show the chart."},
        {"who": "student", "what": "Classify three fractions."},
    ]
    assert not {"mode", "teacher_activities", "student_activities"} & set(step)


def test_a_step_that_already_has_activities_keeps_them() -> None:
    kept = [{"who": "student", "what": "Answer."}]

    [step] = normalize_session_plan_payload({"steps": [{"step_id": "s1", "activities": kept}]})[  # type: ignore[misc]
        "steps"
    ]

    assert step["activities"] == kept
