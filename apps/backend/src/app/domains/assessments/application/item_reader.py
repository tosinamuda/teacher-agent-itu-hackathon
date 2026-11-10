"""A second reader answers each class-test item without its key.

A distractor that is also right, such as 4/4 offered as "not improper" in a lesson that
defines improper as numerator ≥ denominator, passes every check on the item's shape. Only
answering the item against what the class was taught shows it has two right answers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import dspy

from app.infra.dspy_lm import build_dspy_lm


@dataclass(frozen=True)
class ItemToRead:
    """One item as a student sees it, with what the class was taught."""

    lesson: str
    objective_text: str
    subject: str
    grade: str
    stem: str
    options: dict[str, str]


class ItemReader(Protocol):
    """Answers an item without its key."""

    async def correct_options(self, item: ItemToRead) -> set[str]: ...


def reads_as_keyed(read: set[str], correct_option: str) -> bool:
    """True when the reader found the keyed option, and only it, correct."""
    return read == {correct_option}


class ReadClassTestItemSignature(dspy.Signature):
    """Answer this multiple-choice question as the teacher of this lesson would mark it.

    Judge every option by the lesson's own definitions and examples. List every option
    that is a correct answer; when more than one is correct, list them all.
    """

    lesson: str = dspy.InputField(desc="What the class was taught: definitions and examples.")
    objective_text: str = dspy.InputField(desc="The lesson objective the question assesses.")
    subject: str = dspy.InputField(desc="Subject, e.g. Mathematics.")
    grade: str = dspy.InputField(desc="Grade, e.g. JSS1.")
    stem: str = dspy.InputField(desc="The question.")
    options: dict[str, str] = dspy.InputField(desc="Option key -> option text.")
    correct_options: list[str] = dspy.OutputField(desc="Every option key that is correct.")


class DspyItemReader:
    """The second reader, on the generator's own model."""

    def __init__(self) -> None:
        self.lm = build_dspy_lm()
        self.predict = dspy.ChainOfThought(ReadClassTestItemSignature)

    async def correct_options(self, item: ItemToRead) -> set[str]:
        with dspy.settings.context(lm=self.lm):
            result = await self.predict.acall(
                lesson=item.lesson,
                objective_text=item.objective_text,
                subject=item.subject,
                grade=item.grade,
                stem=item.stem,
                options=item.options,
            )
        return {str(key).strip().upper() for key in result.correct_options}
