"""What a learner revising alone needs in a section, so a thin one goes back to the writer."""

from __future__ import annotations

import json
from collections.abc import Mapping

from ..text_checks import (
    FALSE_SIZE_RULE_FIX,
    SECOND_THOUGHT_FIX,
    corrects_itself,
    question_stem,
    states_false_size_rule,
    text_chars,
    wrong_roundings,
)
from .config import MIN_EXPLANATION_CHARS, MIN_PRACTICE_QUESTIONS, MIN_WORKED_EXAMPLES


def _items(part: dict[str, object], name: str) -> list[dict[str, object]]:
    value = part.get(name)
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def section_faults(part: dict[str, object]) -> list[str]:
    """What one section lacks for a learner to revise from it alone."""
    faults: list[str] = []
    explained = text_chars(part.get("explanation"))
    if explained < MIN_EXPLANATION_CHARS:
        faults.append(
            f"the explanation holds {explained} characters; state the rule or idea in full, "
            "with its reason and a short instance, until a learner can revise from it alone"
        )
    if len(_items(part, "worked_examples")) < MIN_WORKED_EXAMPLES:
        faults.append(f"give at least {MIN_WORKED_EXAMPLES} worked examples, from simple to harder")
    questions = [item.get("question") for item in _items(part, "practice")]
    if len(questions) < MIN_PRACTICE_QUESTIONS:
        faults.append(
            f"give at least {MIN_PRACTICE_QUESTIONS} practice questions, each with its answer "
            "and a worked solution where the answer alone would not show the method"
        )
    if len({question_stem(question) for question in questions}) < len(questions):
        faults.append("two practice questions are the same; vary what each one asks")
    problems = {question_stem(item.get("problem")) for item in _items(part, "worked_examples")}
    if any(question_stem(question) in problems for question in questions):
        faults.append(
            "a practice question is a worked example again; change its numbers or what it asks"
        )
    text = json.dumps(part, ensure_ascii=False)
    if states_false_size_rule(text):
        faults.append(FALSE_SIZE_RULE_FIX)
    faults.extend(wrong_roundings(text))
    if corrects_itself(text):
        faults.append(SECOND_THOUGHT_FIX)
    return faults


def review(payload: Mapping[str, object]) -> list[str]:
    """One line for each fault of each section of the draft a payload holds."""
    draft = payload.get("draft")
    sections = draft.get("sections") if isinstance(draft, dict) else None
    return [
        f"{section['unit_id']}: {fault}"
        for section in (sections if isinstance(sections, list) else [])
        if isinstance(section, dict) and isinstance(section.get("part"), dict)
        for fault in section_faults(section["part"])
    ]
