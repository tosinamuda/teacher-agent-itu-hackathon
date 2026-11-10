"""What a writer of a lesson plan reads about the lesson: curriculum notes and textbook."""

from __future__ import annotations

from app.domains.artefacts.types.lesson_plan.application.payload_builder import (
    SessionContextPayloadBuilder,
)
from app.domains.artefacts.types.lesson_plan.domain.types import SessionContext
from app.domains.content_engine.infrastructure.plan_grounding import grounding_of

OBJECTIVE = "jss1-math-construction-po01"


def _context(**given: object) -> SessionContext:
    fields: dict[str, object] = {
        "session_id": "00000000-0000-0000-0000-000000000901",
        "subject": "Mathematics",
        "track": "General",
        "grade": "JSS1",
        "term": "Third Term",
        "week": 8,
        "day_index": 2,
        "topic": "Construction",
        "subtopic": "Bisection of a line segment",
        "duration_minutes": 45,
        "session_objectives": [],
        "general_objectives": ["use a compass accurately"],
        "reference_materials": [{"type": "textbook", "title": "Siyavula JSS1 Mathematics"}],
        "theme": "Mensuration and Geometry",
        "performance_objectives": ["Bisect a given line segment."],
        "teacher_activities": ["Demonstrate the bisection."],
        "textbook_references": [
            {
                "record_id": "ch14-b021",
                "title": "Bisecting a line segment",
                "content": "Place the compass point on A.",
                "record_type": "instruction",
            },
            {"record_id": "ch14-b001", "title": "Constructions", "content": "A construction is..."},
        ],
        "curated_objectives": [
            {
                "curriculum_objective_id": OBJECTIVE,
                "bloom_level": "apply",
                "assessment": {"question": "Bisect ST.", "expected_answer": "Follow the steps."},
                "record_links": [{"record_id": "ch14-b021", "role": "instruction"}],
            }
        ],
    }
    return SessionContext(**{**fields, **given})  # type: ignore[arg-type]


def test_the_curriculums_notes_are_given_without_what_it_leaves_empty() -> None:
    grounding = grounding_of(SessionContextPayloadBuilder().build(_context()))

    assert grounding["curriculum"] == {
        "theme": "Mensuration and Geometry",
        "general_objectives": ["use a compass accurately"],
        "performance_objectives": ["Bisect a given line segment."],
        "teacher_activities": ["Demonstrate the bisection."],
    }


def test_every_textbook_record_is_given_once_and_each_objective_names_the_ones_it_links() -> None:
    grounding = grounding_of(SessionContextPayloadBuilder().build(_context()))

    textbook = grounding["textbook"]
    assert isinstance(textbook, dict)
    records = textbook["records"]
    assert isinstance(records, list)
    assert [record["record_id"] for record in records if isinstance(record, dict)] == [
        "ch14-b021",
        "ch14-b001",
    ]
    assert textbook["by_objective"] == [
        {
            "curriculum_objective_id": OBJECTIVE,
            "bloom_level": "apply",
            "records": [{"record_id": "ch14-b021", "role": "instruction"}],
            "check_question_in_the_textbook": {
                "question": "Bisect ST.",
                "answer": "Follow the steps.",
            },
        }
    ]


def test_a_lesson_with_no_textbook_has_none_to_give() -> None:
    context = _context(
        textbook_references=[], curated_objectives=[], grounding_mode="curriculum_only"
    )

    grounding = grounding_of(SessionContextPayloadBuilder().build(context))

    assert grounding["textbook"] == {"records": [], "by_objective": []}
