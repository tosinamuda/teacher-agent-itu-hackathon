"""Assemble and check hand-entered classwork MCQ items (FD-02).

Pure helpers behind the manual classwork path: the teacher supplies real
classwork items, which become the same ``ExitTicketItem`` rows the LLM diagnostic
writes. ``build_classwork_item_payloads`` emits the identical insert payload as
``diagnostic_service._build_item_payloads`` so downstream scoring consumes manual
and generated items the same way; ``classwork_item_issues`` returns teacher-facing
validation messages (objective tagging, options, correct answer).
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable

from app.domains.assessments.classwork_schemas import ManualClassworkItem


def build_classwork_item_payloads(
    items: Iterable[ManualClassworkItem],
    *,
    subtopic_id: str,
    plan_version_id: str,
) -> list[dict[str, object]]:
    """Insert payloads matching ``ExitTicketItem``'s columns exactly.

    ``subtopic_id`` and ``plan_version_id`` are resolved server-side (never from
    teacher input) so the FKs cannot be wrong. ``option_misconceptions`` is filtered
    to wrong options that exist — empty for now, FD-03 fills it.
    """
    payloads: list[dict[str, object]] = []
    for item in items:
        distractors = {
            key: code
            for key, code in (item.option_misconceptions or {}).items()
            if key in item.options and key != item.correct_option
        }
        payloads.append(
            {
                "subtopic_id": subtopic_id,
                "plan_version_id": plan_version_id,
                "lesson_objective_id": item.lesson_objective_id,
                "stem": item.stem,
                "correct_option": item.correct_option,
                "options": dict(item.options),
                "option_misconceptions": distractors or None,
                "difficulty": item.difficulty,
                "knowledge_component_id": (
                    uuid.UUID(item.knowledge_component_id) if item.knowledge_component_id else None
                ),
            }
        )
    return payloads


def classwork_item_issues(
    items: Iterable[ManualClassworkItem],
    *,
    valid_objective_ids: set[str],
) -> list[str]:
    """Teacher-facing reasons a classwork set cannot be saved (one per offending item).

    An empty list means every item is tagged to a lesson objective, has at least
    two non-empty options, a non-empty stem, and a correct option among its keys —
    the contract the scoring pipeline relies on.
    """
    issues: list[str] = []
    for index, item in enumerate(items, start=1):
        if item.lesson_objective_id not in valid_objective_ids:
            issues.append(f"Item {index}: tag it to one of this lesson's objectives.")
        if len(item.options) < 2:
            issues.append(f"Item {index}: enter at least two options.")
        if any(not str(text).strip() for text in item.options.values()):
            issues.append(f"Item {index}: every option needs text.")
        if item.correct_option not in item.options:
            issues.append(f"Item {index}: mark which option is correct.")
        if not item.stem.strip():
            issues.append(f"Item {index}: enter the question.")
    return issues
