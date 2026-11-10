"""Whether a written multiple-choice item can be graded as it stands."""

from __future__ import annotations

import re
from collections.abc import Mapping


def _said(text: str) -> str:
    """The option as it reads.

    A capital that opens it is how it is printed. A capital inside it changes what it says, as
    in a question about capital letters.
    """
    spaced = re.sub(r"\s+", " ", text).strip()
    return spaced[:1].lower() + spaced[1:]


def is_sound(options: Mapping[str, str], correct_option: str) -> bool:
    """Its answer is one of its options, and no two options say the same thing.

    An item is graded by the letter chosen, so a learner who picks a copy of the answer
    under another letter would be marked wrong for a right answer.
    """
    said = [_said(text) for text in options.values()]
    return correct_option in options and all(said) and len(set(said)) == len(said)


_ORDERING = re.compile(r"^\s*(arrange|order|sort|rank|put)\b", re.IGNORECASE)
_NO_ANSWER_OPTION = re.compile(r"^(both|neither|all|none|cannot|can't|not enough)\b", re.IGNORECASE)
_PRINTED_NUMBER = re.compile(r"\d|\b(thousand|million|billion|trillion)\b", re.IGNORECASE)
_OWN_CHOICES = re.compile(r"(?:^|\s)\(?[A-D][).]\s", re.MULTILINE)


def says_what_it_asks(stem: str, options: Mapping[str, str]) -> bool:
    """A learner can answer from what is printed: the numbers asked about are in the stem.

    "Arrange the following numbers" with the numbers only inside the options, or "Which is
    larger?" over options such as "Both are equal", leaves the learner without the thing to
    order or compare. "Which of the following lists the numbers in order?" asks about the
    options themselves, so it stands. A stem that carries a lettered list of its own disagrees
    with the real options.
    """
    if len(set(_OWN_CHOICES.findall(stem))) > 1:
        return False
    if _PRINTED_NUMBER.search(stem):
        return True
    if _ORDERING.search(stem):
        return False
    return not any(_NO_ANSWER_OPTION.match(text.strip()) for text in options.values())
