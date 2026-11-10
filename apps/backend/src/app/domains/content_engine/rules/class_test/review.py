"""Every fault of a class test's questions: each question's shape, repeated stems, and size."""

from __future__ import annotations

import re
from collections.abc import Mapping

from app.domains.assessments.domain.item_checks import is_sound, says_what_it_asks

from .config import LETTERS
from .scale import reaches_scale

_CODE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$")


class Question:
    """A question as the app grades it: lettered options, a key, a code for each wrong option."""

    def __init__(self, raw: dict[str, object]) -> None:
        given = raw.get("options")
        self.stem = str(raw.get("stem", "")).strip()
        self.options = (
            {letter: str(given.get(letter.lower(), "")) for letter in LETTERS}
            if isinstance(given, dict)
            else {}
        )
        self.correct = str(raw.get("correct_option", "")).strip()
        self.codes: dict[str, str] = {}
        distractors = raw.get("distractors")
        for entry in distractors if isinstance(distractors, list) else []:
            if isinstance(entry, dict):
                self.codes[str(entry.get("option"))] = str(
                    entry.get("misconception_code", "")
                ).strip()


def question_faults(where: str, question: Question) -> list[str]:
    """What stops one question being graded or answered as written."""
    wrong = [letter for letter in LETTERS if letter != question.correct]
    found: list[str] = []
    if not is_sound(question.options, question.correct):
        found.append(f"{where}: the options must differ and the correct option must be one of A-D")
    if not says_what_it_asks(question.stem, question.options):
        found.append(f"{where}: print the numbers the question is about in the stem")
    if sorted(question.codes) != wrong:
        found.append(
            f"{where}: give a misconception code for each wrong option: {', '.join(wrong)}"
        )
    found += [
        f"{where}: the misconception code {code!r} for {letter} is snake_case"
        for letter, code in question.codes.items()
        if not _CODE.match(code)
    ]
    return found


def _questions(part: dict[str, object]) -> list[dict[str, object]]:
    questions = part.get("questions")
    return [q for q in questions if isinstance(q, dict)] if isinstance(questions, list) else []


def _step_faults(step: str, part: dict[str, object], objective: str) -> list[str]:
    raw = _questions(part)
    found: list[str] = []
    for number, question in enumerate(raw, start=1):
        found += question_faults(f"{step} question {number}", Question(question))
    stems = [str(q.get("stem", "")).strip() for q in raw]
    if len(set(stems)) != len(stems):
        found.append(f"{step}: two questions have the same stem")
    items = [(q.stem, q.options) for q in map(Question, raw)]
    if items and not reaches_scale(objective, items):
        found.append(
            f"{step}: the objective names numbers as large as {objective!r}: use that size "
            "in at least one question"
        )
    return found


def review(payload: Mapping[str, object]) -> list[str]:
    """The faults of the draft a payload holds; empty when the test passes."""
    draft, source = payload.get("draft"), payload.get("source")
    sections = draft.get("sections") if isinstance(draft, dict) else None
    named = source.get("objectives_by_step") if isinstance(source, dict) else None
    objectives = named if isinstance(named, dict) else {}
    return [
        fault
        for section in (sections if isinstance(sections, list) else [])
        if isinstance(section, dict) and isinstance(section.get("part"), dict)
        for fault in _step_faults(
            str(section["unit_id"]), section["part"], str(objectives.get(section["unit_id"], ""))
        )
    ]
