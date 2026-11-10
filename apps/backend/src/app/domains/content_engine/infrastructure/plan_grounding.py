"""What a writer of a lesson plan may read about the lesson besides its facts.

The curriculum's own notes for the lesson, and the textbook records the lesson has, with the
role each plays in teaching each curriculum objective. A writer reads these as the lesson's
sources, so what it writes can be traced to them.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from app.domains.artefacts.types.lesson_plan.application.payload_builder import (
    PlanGenerationPayloads,
)
from app.shared.json_types import JsonObject, JsonValue

_RECORD_FIELDS = ("record_id", "title", "record_type", "content", "prompt_text", "answer_text")


def _texts(values: Sequence[str]) -> list[JsonValue]:
    return [*values]


def _filled(fields: Mapping[str, JsonValue]) -> JsonObject:
    return {name: value for name, value in fields.items() if value not in ("", [], None)}


def _records(payloads: PlanGenerationPayloads) -> list[JsonValue]:
    """Every textbook record the lesson has, once, in the order the curriculum links them."""
    return [
        _filled({name: record.get(name) for name in _RECORD_FIELDS})
        for record in payloads.reference_context
        if record.get("type") == "textbook_record" and record.get("record_id")
    ]


def _by_objective(objective: JsonObject) -> JsonObject:
    links = objective.get("record_links")
    assessment = objective.get("assessment")
    check = (
        _filled(
            {"question": assessment.get("question"), "answer": assessment.get("expected_answer")}
        )
        if isinstance(assessment, dict)
        else {}
    )
    return _filled(
        {
            "curriculum_objective_id": objective.get("curriculum_objective_id"),
            "bloom_level": objective.get("bloom_level"),
            "records": [
                _filled({"record_id": link.get("record_id"), "role": link.get("role")})
                for link in (links if isinstance(links, list) else [])
                if isinstance(link, dict)
            ],
            "check_question_in_the_textbook": check,
        }
    )


def grounding_of(payloads: PlanGenerationPayloads) -> JsonObject:
    """The curriculum's notes and the textbook records of the lesson, for the lesson's resource."""
    session, curriculum = payloads.session_scope, payloads.curriculum_scope
    return {
        "curriculum": _filled(
            {
                "theme": session.theme,
                "general_objectives": _texts(curriculum.general_objectives),
                "performance_objectives": _texts(curriculum.performance_objectives),
                "teacher_activities": _texts(curriculum.teacher_activities),
                "student_activities": _texts(curriculum.student_activities),
                "instructional_materials": _texts(curriculum.instructional_materials),
                "evaluation_guide": _texts(curriculum.evaluation_guide),
                "entry_behaviour": _texts(curriculum.entry_behaviour),
            }
        ),
        "textbook": {
            "records": _records(payloads),
            "by_objective": [_by_objective(o) for o in payloads.curated_objectives],
        },
    }
