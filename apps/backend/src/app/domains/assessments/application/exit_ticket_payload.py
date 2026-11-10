"""One class-test item as the row grading reads it."""

from __future__ import annotations

from app.domains.assessments.application.diagnostic_generator import DiagnosticMCQItem
from app.domains.assessments.domain.item_level import labelled
from app.domains.assessments.domain.option_order import placed


def exit_ticket_payload(
    item: DiagnosticMCQItem,
    *,
    subtopic_id: str,
    plan_version_id: str,
    lesson_objective_id: str,
) -> dict[str, object]:
    """The item with its answer placed, a code on each wrong option, and a label its stem allows."""
    distractors = {
        key: code
        for key, code in item.distractor_misconceptions.items()
        if key in item.options and key != item.correct_option
    }
    options = placed(item.options, item.correct_option, distractors, stem=item.stem)
    return {
        "subtopic_id": subtopic_id,
        "plan_version_id": plan_version_id,
        "lesson_objective_id": lesson_objective_id,
        "stem": item.stem,
        "correct_option": options.correct_option,
        "options": options.options,
        "option_misconceptions": options.misconceptions or None,
        "difficulty": labelled(item.difficulty, item.stem),
    }
