"""How much of a pack's practice is the teacher's own evaluation, recorded per candidate.

The reference sheet carries her evaluation questions so that assessment congruence
can be rated. The cost is that a pack which reproduces them can look aligned for
it, and under C1 the plan hands the model exactly those questions. The rubric
guidance says reuse alone is not alignment; this records how much reuse there was,
beside each candidate in the blinding key, so the analysis can test whether
overlap predicts the score instead of wondering.

Three measures, strict to loose, each the count of her questions the pack reuses:

- exact: a practice prompt equals an evaluation question after whitespace folding
- normalised: the same after case, punctuation, and maths delimiters are dropped
- numbers: the same after every number is also dropped — "the structure of the
  question with different figures", which is what "adapted" usually means

Never shown to a rater. A rater who knew reuse was being measured would rate it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

_WS = re.compile(r"\s+")
_PUNCT = re.compile(r"[^\w\s]")
_NUMBER = re.compile(r"\d+(?:\.\d+)?")


def _fold(text: str) -> str:
    return _WS.sub(" ", text).strip()


def _normalise(text: str) -> str:
    return _WS.sub(" ", _PUNCT.sub(" ", text.lower())).strip()


def _shape(text: str) -> str:
    return _normalise(_NUMBER.sub(" n ", text))


@dataclass(frozen=True)
class Overlap:
    evaluation_questions: int
    practice_items: int
    exact: int
    normalised: int
    numbers_changed: int

    def as_record(self) -> dict[str, int]:
        return {
            "evaluation_questions": self.evaluation_questions,
            "practice_items": self.practice_items,
            "reused_exact": self.exact,
            "reused_normalised": self.normalised,
            "reused_numbers_changed": self.numbers_changed,
        }


def overlap(evaluation: list[str], sections: list[dict[str, Any]]) -> Overlap:
    prompts = [
        str(item.get("prompt") or "")
        for section in sections
        for item in section.get("practice") or []
    ]
    exact = {_fold(p) for p in prompts}
    normalised = {_normalise(p) for p in prompts}
    shapes = {_shape(p) for p in prompts}
    return Overlap(
        evaluation_questions=len(evaluation),
        practice_items=len(prompts),
        exact=sum(_fold(q) in exact for q in evaluation),
        normalised=sum(_normalise(q) in normalised for q in evaluation),
        numbers_changed=sum(_shape(q) in shapes for q in evaluation),
    )
