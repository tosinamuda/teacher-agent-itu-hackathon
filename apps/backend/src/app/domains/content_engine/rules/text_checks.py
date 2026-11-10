"""Text a note must not carry: second thoughts, a false rule for comparing sizes, wrong rounding."""

from __future__ import annotations

import re

_SECOND_THOUGHT = re.compile(
    r"\b(?:wait[,.!]|actually,\s+(?:we|i)\s+(?:made|need|should)|let(?:'s|\s+us|\s+me)\s+"
    r"(?:re-?compute|re-?check|try again)|oops|on second thought|that is wrong|i made a mistake|"
    r"we made a mistake)",
    re.IGNORECASE,
)
_SIZE = r"(?:larger|bigger|higher|greater)"
_RANKED = r"(?:named\s+)?(?:unit|group|leading\s+digit|first\s+digit)"
_FALSE_SIZE_RULE = re.compile(
    rf"\b{_SIZE}\s+{_RANKED}\b[^.]{{0,40}}\b(?:guarantees?|automatically|wins?|always|decides?)"
    rf"|\b(?:with|has)\s+the\s+{_SIZE}\s+{_RANKED}\b",
    re.IGNORECASE,
)
_NUMBER = r"\d{1,3}(?:[,{}]+\d{3})+|\d+"
#: "round 7,500 to 7,000" and "round 7,500 steps to 7,000", never "round down 7,500 to 7,000".
_ROUNDING = re.compile(
    rf"\bround(?:s|ed|ing)?\s+({_NUMBER})(?![.,]?\d)\s+(?:[a-z]+\s+)?to\s+({_NUMBER})(?![.,]?\d)",
    re.IGNORECASE,
)

SECOND_THOUGHT_FIX = (
    "the text leaves a second thought in it ('Wait', 'Actually, we made a mistake'): work it "
    "out first and write only the corrected version"
)
FALSE_SIZE_RULE_FIX = (
    "the text says the larger unit name or leading digit makes the larger number, which is "
    "false (0.08 trillion is less than 800 billion): convert to one unit, then compare digit "
    "counts and digits"
)


def corrects_itself(text: str) -> bool:
    """The writer's own correction is left in the text: "Wait, this contradicts..."."""
    return _SECOND_THOUGHT.search(text) is not None


def states_false_size_rule(text: str) -> bool:
    """A rule that the larger unit name or leading digit makes the larger number, which is false."""
    return _FALSE_SIZE_RULE.search(text) is not None


def text_chars(value: object) -> int:
    """The characters of text in a part, however deeply its lists and groups nest."""
    if isinstance(value, str):
        return len(value.strip())
    if isinstance(value, list):
        return sum(text_chars(item) for item in value)
    if isinstance(value, dict):
        return sum(text_chars(item) for item in value.values())
    return 0


def question_stem(question: object) -> str:
    """A question as it is compared with another: case and spacing do not tell two apart."""
    return " ".join(str(question).lower().split())


def _value(written: str) -> int:
    return int(re.sub(r"[,{}]", "", written))


def _nearest(number: int, place: int) -> int:
    """The number rounded to the nearest place, a half going up."""
    return (number + place // 2) // place * place


def wrong_roundings(text: str) -> list[str]:
    """One line for each "round A to B" whose B is not A rounded to the place B ends in zeros at."""
    faults: list[str] = []
    for match in _ROUNDING.finditer(text):
        number, rounded = _value(match.group(1)), _value(match.group(2))
        zeros = len(str(rounded)) - len(str(rounded).rstrip("0"))
        if zeros == 0 or rounded == 0:
            continue
        right = _nearest(number, 10**zeros)
        if right != rounded:
            faults.append(
                f"the text rounds {number:,} to {rounded:,}, but {number:,} rounds to "
                f"{right:,} at that place: round it correctly, or choose a number that "
                "rounds cleanly"
            )
    return faults
