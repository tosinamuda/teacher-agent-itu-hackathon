"""A drafted class-test question as the pipeline writes an item."""

from __future__ import annotations

from app.domains.assessments.application.diagnostic_generator import DiagnosticMCQItem
from app.shared.json_types import JsonObject

_LETTERS = ("A", "B", "C", "D")


def questions_of(part: JsonObject) -> list[JsonObject]:
    questions = part.get("questions")
    return [q for q in questions if isinstance(q, dict)] if isinstance(questions, list) else []


def item_of(question: JsonObject) -> DiagnosticMCQItem:
    """The question as the pipeline writes an item: lettered options, a key, codes."""
    given = question.get("options")
    options = (
        {letter: str(given.get(letter.lower(), "")) for letter in _LETTERS}
        if isinstance(given, dict)
        else {}
    )
    codes: dict[str, str] = {}
    distractors = question.get("distractors")
    for entry in distractors if isinstance(distractors, list) else []:
        if isinstance(entry, dict):
            codes[str(entry.get("option"))] = str(entry.get("misconception_code", "")).strip()
    return DiagnosticMCQItem.model_validate(
        {
            "stem": str(question.get("stem", "")).strip(),
            "options": options,
            "correct_option": str(question.get("correct_option", "")).strip(),
            "distractor_misconceptions": codes,
            "difficulty": question.get("difficulty"),
        }
    )
