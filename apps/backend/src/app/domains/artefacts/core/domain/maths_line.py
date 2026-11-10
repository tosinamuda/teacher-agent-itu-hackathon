r"""A line of mathematics, as a worked solution writes it: LaTeX between $ signs.

A model asked for working it does not have writes a sentence inside ``\text{}`` so it looks
like working. A line whose mathematics is only words is refused: the words belong in the
commentary, and a step with nothing to calculate has no worked example.
"""

from __future__ import annotations

import re

_MATHS = re.compile(r"\$\$(.+?)\$\$|\$(.+?)\$", re.DOTALL)
_WORDS_IN_TEXT = re.compile(r"\\(?:text|mathrm|textrm|mbox)\s*\{([^{}]*)\}")
_WORD = re.compile(r"[A-Za-z]{2,}")
#: What makes a line mathematics: a number, a symbol, a relation or an operation.
_MATHEMATICS = re.compile(r"\d|\\(?!text|mathrm|textrm|mbox)[A-Za-z]+|[=+\-*/<>^_|]")


def problem(line: str, *, formulas: bool = True) -> str | None:
    """Why ``line`` is not a line of working, or None when it is one.

    ``formulas`` is false for a lesson whose working is not a calculation, such as naming the
    kind of noun a word is: its lines are plain text, and nothing needs to be a formula.
    """
    if not formulas:
        return None
    parts = [first or second for first, second in _MATHS.findall(line)]
    if not parts:
        return "write the working in LaTeX between $ signs"
    maths = " ".join(parts)
    words = sum(len(_WORD.findall(inside)) for inside in _WORDS_IN_TEXT.findall(maths))
    rest = _WORDS_IN_TEXT.sub(" ", maths)
    if words >= 3 and not _MATHEMATICS.search(rest):
        return (
            "this line is a sentence in \\text{}, not working: put the words in the commentary, "
            "and give a step with nothing to calculate no worked example"
        )
    return None
