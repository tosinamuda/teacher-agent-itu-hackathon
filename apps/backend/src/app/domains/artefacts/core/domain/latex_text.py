r"""Text that carries mathematics: LaTeX between $ signs, and nothing else that shows as code.

A model leaks what it meant as formatting: ``\n`` for a new line, ``\;`` for a space, a ``$``
it never closes. Each reaches a learner as the characters themselves, so a part with one is
refused and the writer corrects the text.
"""

from __future__ import annotations

import re

_MATHS = re.compile(r"\$\$.+?\$\$|\$.+?\$", re.DOTALL)
_ESCAPED_DOLLAR = re.compile(r"\\\$")
#: A backslash escape a model uses for formatting, which only means something inside maths.
_STRAY = re.compile(r"(?<!\\)\\([ntr;,!])")
#: A command such as \times written outside $ signs starts with \t, so it is reported as one.
_COMMAND_HINT = (
    "; if it is a command such as \\times or \\text, put the whole formula between $ signs"
)
_NAMES = {"n": "\\n", "t": "\\t", "r": "\\r", ";": r"\;", ",": "\\,", "!": "\\!"}


def problems(text: str) -> list[str]:
    """What in ``text`` would show as code instead of text or mathematics; empty when nothing."""
    found: list[str] = []
    plain = _ESCAPED_DOLLAR.sub("", text)
    if plain.count("$") % 2:
        found.append("a $ is never closed: write each formula between a pair of $ signs")
    outside = _MATHS.sub(" ", plain)
    for stray in sorted({match.group(1) for match in _STRAY.finditer(outside)}):
        found.append(
            f"{_NAMES[stray]} outside a formula shows as those characters: "
            "start a new line by starting a new line, and leave out spacing codes"
            + (_COMMAND_HINT if stray == "t" else "")
        )
    return found
