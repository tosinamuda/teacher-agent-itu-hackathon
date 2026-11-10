"""Text a note must not carry: record ids, second thoughts, and a false rule for comparing sizes."""

from __future__ import annotations

import re

from app.shared.json_types import JsonValue

_DASH = "‐‑‒–—―-"
#: A textbook record the lesson plan cites, such as ch01-b044-i01 (any dash the model typed).
_RECORD = rf"ch\d{{2}}[{_DASH}]b\d{{3}}(?:[{_DASH}][a-z]\d{{2}})?"
_BRACKETED = re.compile(
    rf"\s*[(\[]\s*(?:(?:textbook\s+)?records?\s+)?{_RECORD}\s*[)\]]", re.IGNORECASE
)
_NAMED = re.compile(rf"\b(?:the\s+)?(?:textbook\s+)?records?\s+{_RECORD}", re.IGNORECASE)
_BARE = re.compile(rf"\b{_RECORD}", re.IGNORECASE)
_SECOND_THOUGHT = re.compile(
    r"\b(?:wait[,.!]|actually,\s+(?:we|i)\s+(?:made|need|should)|let(?:'s|\s+us|\s+me)\s+(?:re-?compute|re-?check|"
    r"try again)|oops|on second thought|that is wrong|i made a mistake|we made a mistake)",
    re.IGNORECASE,
)
_SIZE = r"(?:larger|bigger|higher|greater)"
_RANKED = r"(?:named\s+)?(?:unit|group|leading\s+digit|first\s+digit)"
_FALSE_SIZE_RULE = re.compile(
    rf"\b{_SIZE}\s+{_RANKED}\b[^.]{{0,40}}\b(?:guarantees?|automatically|wins?|always|decides?)"
    rf"|\b(?:with|has)\s+the\s+{_SIZE}\s+{_RANKED}\b",
    re.IGNORECASE,
)

FALSE_SIZE_RULE_FIX = (
    "the text says the larger unit name or leading digit makes the larger number, which is "
    "false (0.08 trillion is less than 800 billion): convert to one unit, then compare digit "
    "counts and digits"
)


def without_record_ids(text: str) -> str:
    """The text with the plan's textbook record ids taken out, leaving the sentence readable."""
    text = _BRACKETED.sub("", text)
    text = _NAMED.sub("the textbook", text)
    return _BARE.sub("the textbook", text)


def corrects_itself(text: str) -> bool:
    """The writer's own correction is left in the text: "Wait, this contradicts…"."""
    return _SECOND_THOUGHT.search(text) is not None


def text_chars(value: JsonValue) -> int:
    """The characters of text in a part, however deeply its lists and groups nest."""
    if isinstance(value, str):
        return len(value.strip())
    if isinstance(value, list):
        return sum(text_chars(item) for item in value)
    if isinstance(value, dict):
        return sum(text_chars(item) for item in value.values())
    return 0


def states_false_size_rule(text: str) -> bool:
    """A rule that the larger unit name or leading digit makes the larger number, which is false."""
    return _FALSE_SIZE_RULE.search(text) is not None


def question_stem(question: object) -> str:
    """A question as it is compared with another: case and spacing do not tell two apart."""
    return " ".join(str(question).lower().split())
