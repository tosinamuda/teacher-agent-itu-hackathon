"""Text with LaTeX maths between $ signs, as plain text a slide program shows and lets you edit."""

from __future__ import annotations

import re

_MATHS = re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$|(?<!\\)\$(.+?)(?<!\\)\$", re.DOTALL)
#: A character that a writer escapes outside maths, as in ``about \_\_\_ m`` or ``50\%``.
_ESCAPED = re.compile(r"\\([$_%&#{}])")
#: A blank to fill in, as in ``\underline{\hspace{1cm}}``, and the spacing commands beside it.
_BLANK = re.compile(r"\\underline\s*\{\s*\\hspace\*?\s*\{[^{}]*\}\s*\}")
_SPACE = re.compile(r"\\[hv]space\*?\s*\{[^{}]*\}")
_DEGREE = re.compile(r"\^\s*(?:\\circ|\{\\circ\})")
_SYMBOLS = {
    r"\times": " × ",
    r"\div": " ÷ ",
    r"\cdot": "·",
    r"\approx": " ≈ ",
    r"\neq": " ≠ ",
    r"\leq": " ≤ ",
    r"\le": " ≤ ",
    r"\geq": " ≥ ",
    r"\ge": " ≥ ",
    r"\pm": "±",
    r"\pi": "π",
    r"\circ": "°",
    r"\degree": "°",
    r"\%": "%",
    r"\$": "$",
    r"\rightarrow": " → ",
    r"\to": " → ",
    r"\Rightarrow": " ⇒ ",
    r"\therefore": "∴",
    r"\ldots": "…",
    r"\dots": "…",
    r"\quad": "  ",
    r"\qquad": "    ",
    r"\,": " ",
    r"\;": " ",
    r"\:": " ",
    r"\!": "",
    r"\ ": " ",
}
_SUPERSCRIPTS = str.maketrans("0123456789+-n", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ⁿ")
_SUBSCRIPTS = str.maketrans("0123456789+-", "₀₁₂₃₄₅₆₇₈₉₊₋")
_WORDS = re.compile(r"\\(?:text|textbf|mathrm|mathbf|operatorname|mbox)\s*\{([^{}]*)\}")
_FRACTION = re.compile(r"\\d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}")
_ROOT = re.compile(r"\\sqrt\s*\{([^{}]*)\}")
_POWER = re.compile(r"\^\s*(?:\{([^{}]*)\}|(\w))")
_INDEX = re.compile(r"_\s*(?:\{([^{}]*)\}|(\w))")
#: Longest first, so \le does not take the front of \leq.
_COMMANDS: list[str] = sorted(_SYMBOLS, key=lambda name: -len(name))
#: A named command ends where its letters end; a symbol command such as ``\ `` ends at once.
_SYMBOL = re.compile(
    "|".join(
        re.escape(name) + (r"(?![A-Za-z])" if name[-1].isalpha() else "") for name in _COMMANDS
    )
)
_LEFTOVER_COMMAND = re.compile(r"\\([A-Za-z]+)")
#: Characters that many slide fonts lack, written as the plain ones beside them.
_PLAIN_SPACING = str.maketrans({"\u2010": "-", "\u2011": "-", "\u202f": " ", "\u00a0": " "})
_RELATION = re.compile(r"\s*([=<>])\s*")
#: Spacing commands: a thin space reads as a space, and a negative one is nothing.
_THIN_SPACE = re.compile(r"\\[,;:]")


def _maths(expression: str) -> str:
    text = _SPACE.sub("", _BLANK.sub("\x00", expression))
    text = _DEGREE.sub("°", _WORDS.sub(r"\1", text))
    text = _FRACTION.sub(lambda found: f"{_term(found[1])}/{_term(found[2])}", text)
    text = _ROOT.sub(r"√(\1)", text)
    text = _SYMBOL.sub(lambda found: _SYMBOLS[found.group(0)], text)
    text = _POWER.sub(lambda found: _raised(found.group(1) or found.group(2)), text)
    text = _INDEX.sub(lambda found: _lowered(found.group(1) or found.group(2)), text)
    text = text.replace("{,}", ",").replace("{", "").replace("}", "")
    text = _LEFTOVER_COMMAND.sub(r"\1", text)
    text = _RELATION.sub(r" \1 ", text)
    return re.sub(r"[ \t]{2,}", " ", text).strip().replace("\x00", "____")


def _term(written: str) -> str:
    """A fraction's numerator or denominator, in brackets only when it is more than one word."""
    return written if re.fullmatch(r"[\w.,]+", written.strip()) else f"({written})"


def _raised(written: str) -> str:
    return (
        written.translate(_SUPERSCRIPTS) if re.fullmatch(r"[0-9+\-n]+", written) else f"^{written}"
    )


def _lowered(written: str) -> str:
    return written.translate(_SUBSCRIPTS) if re.fullmatch(r"[0-9+\-]+", written) else f"_{written}"


def plain_maths(text: str) -> str:
    """The text with each $…$ span written in symbols and plain letters."""
    spaced = _THIN_SPACE.sub(" ", text).replace("\\!", "")
    typeset = _MATHS.sub(lambda found: _maths(found.group(1) or found.group(2)), spaced)
    return _ESCAPED.sub(r"\1", typeset).translate(_PLAIN_SPACING)
