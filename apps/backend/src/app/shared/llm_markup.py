r"""Supplying the markup the model left out, so its maths reaches a reader as maths.

Distinct from :mod:`app.shared.llm_text`, which undoes damage done to the string in
transit. Nothing here was damaged: the model wrote exactly what we stored, and what
it wrote does not say "this is maths" in the one notation the renderer reads.

Both surfaces of the H1 study depend on that notation. ``pymdownx.arithmatex`` marks
only delimited maths, and only marked maths becomes an SVG in the WeasyPrint
worksheet; anything else reaches the page as source. Blinded across 72 packs, the
teacher-note arms wrote none of this and the two arms the registered endpoint
compares wrote all of it — C0 29 occurrences, C1 39 — so leaving it is not neutral
between the conditions.

Two repairs, both local and both reversible by eye:

- a LaTeX command standing in prose is wrapped in ``\(…\)`` where it stands, never
  extended over the words around it;
- a run opened and never closed is closed, at the end of its paragraph.

:func:`reader_ready` is the entry point everything else should use. It runs those two
after the transport repairs in :mod:`~app.shared.llm_text`, which they depend on
having happened, and is called at generation, at render, and where a frozen
experiment run's packets are built.
"""

from __future__ import annotations

import re

from app.shared.llm_html import demote_html
from app.shared.llm_text import (
    decode_llm_json_escapes,
    is_bare_environment,
    is_math_run,
    repair_math_control_chars,
    split_math_runs,
    strip_json_residue,
)
from app.shared.tikz_figures import FIGURE

# A LaTeX command written in prose with no delimiter around it: "Perimeter = 4
# \times side", which reaches the learner with the backslash showing. The command
# takes its arguments with it so `\frac{22}{7}` and `\sqrt{16}` wrap whole — and the
# OPTIONAL argument too, because `\sqrt[3]{512}` is a cube root and wrapping only the
# command splits it into `\(\sqrt\)[3]{512}`: an unparseable fragment, then literal junk.
#
# It must be the start of an expression, not part of one: after `{`, `^` or `_` the
# command belongs to a larger undelimited expression (`60^{\circ}`) that wrapping
# from the inside would only break — those are left alone rather than corrupted.
# `\\` is a LaTeX line break and `\_` a markdown escape; neither is a command.
#
# Two letters at least. A one-letter sequence here is an undecoded JSON escape —
# `\n` between paragraphs — and the maths this repairs has no one-letter commands
# in it; wrapping a paragraph break as `\(\n\)` would be a worse defect than the one
# being fixed.
_BARE_COMMAND_RE = re.compile(r"(?<![{^_\\])\\[a-zA-Z]{2,}(?:\[[^\[\]]*\])?(?:\{[^{}]*\})*")

# Where a closing delimiter goes when the model dropped it: before the punctuation
# that ends the sentence, not after it. `\(EF = 7\text{ cm} + 7\text{ cm} = 14.`
# closes to `…= 14\).`, leaving the full stop in the prose it belongs to.
_TRAILING_PUNCTUATION_RE = re.compile(r"([.,;:!?]*\s*)$")

# The blank line markdown reads as a paragraph break, which is as far as a run can
# reach: closing at the end of the *field* instead would hand markdown a `\(…\)`
# spanning two paragraphs, which it splits and neither half of which arithmatex can
# mark — the delimiters then reach the reader as literal parentheses.
_PARAGRAPH_BREAK_RE = re.compile(r"(\n[ \t]*\n)")

# An opener or closer, not the ``\\`` line break that ``\\[4pt]`` spaces.
_DELIMITERS = (
    (re.compile(r"(?<!\\)\\\("), re.compile(r"(?<!\\)\\\)"), r"\)"),
    (re.compile(r"(?<!\\)\\\["), re.compile(r"(?<!\\)\\\]"), r"\]"),
)


def delimit_bare_math(text: str) -> str:
    r"""Wrap each undelimited LaTeX command in prose in ``\(…\)``.

    Only the command itself, so ``4 \times side`` becomes ``4 \(\times\) side`` and
    the two words stay prose — extending the run over them would typeset "Perimeter"
    as a product of nine italic letters. Text already inside a math run is untouched.
    An environment standing bare is displayed whole, in ``\[…\]``.

    Wrapping rather than substituting the Unicode character: the worksheet's
    vendored Computer Modern has no glyph for ``×``, so ``\times`` written into the
    prose font renders as a missing-glyph box. Through the math pipeline it gets the
    font fallback that :mod:`~...worksheet_html.math_svg` already does.

    Takes text whose JSON escapes are already decoded — call it through
    :func:`reader_ready`, which orders that. An undecoded ``\nWhy`` is a paragraph
    break and four letters, and nothing in a backslash tells the two apart.
    """
    if not text or "\\" not in text:
        return text
    return "".join(_delimited(part) for part in split_math_runs(text))


def _delimited(part: str) -> str:
    if is_bare_environment(part):
        return rf"\[{part}\]"
    if is_math_run(part):
        return part
    return _BARE_COMMAND_RE.sub(r"\\(\g<0>\\)", part)


def count_bare_math(text: str) -> int:
    r"""How many LaTeX commands would reach a reader as a backslash.

    What :func:`delimit_bare_math` repairs, counted rather than repaired — the run
    metric and the render guard both need the number, and neither should keep its
    own idea of what "raw LaTeX" is.
    """
    return sum(
        1 if is_bare_environment(part) else len(_BARE_COMMAND_RE.findall(part))
        for part in split_math_runs(text)
        if is_bare_environment(part) or not is_math_run(part)
    )


def close_unclosed_math(text: str) -> str:
    r"""Close a math run the model opened and never closed, at the end of its paragraph.

    One missing delimiter in a paragraph is a slip with an unambiguous repair; more
    than one is a guess about which run each belonged to, and a wrong guess reads as
    the model's own words. Those are left for a reader to see.
    """
    return "".join(
        part if _PARAGRAPH_BREAK_RE.fullmatch(part) else _closed(part)
        for part in _PARAGRAPH_BREAK_RE.split(text)
    )


def _closed(paragraph: str) -> str:
    for opener, closer, written in _DELIMITERS:
        if len(opener.findall(paragraph)) - len(closer.findall(paragraph)) == 1:
            paragraph = _TRAILING_PUNCTUATION_RE.sub(rf"{written}\1", paragraph, count=1)
    return paragraph


def reader_ready(text: str) -> str:
    r"""A stored LLM string, as a reader can be shown it.

    The whole chain, in the only order that works, so no caller has to hold it:

    1. decode the escapes the transport left as backslash-pairs — a literal ``\n``
       is a paragraph break the model failed to emit;
    2. restore the commands that decode itself ate, and only then: the decode is a
       way to lose a command, turning a surviving ``\\times`` into a tab;
    3. cut punctuation the field carried in from the enclosing JSON object, before
       any of it can be read as a delimiter;
    4. demote the HTML the model wrote to markdown — before the close, because a
       ``<p>`` is a paragraph break and the paragraph is as far as the close reaches;
    5. close a run the model opened and left open — while it is open the whole tail
       of the field reads as prose, which the next step would then delimit *inside*
       maths;
    6. delimit what is left standing bare.

    Every step is idempotent, so a section cleaned at generation passes through
    unchanged on its way to a page, and one stored before any of this existed is
    repaired on the way. A drawing is TikZ, not maths in prose, so each ``tikzpicture``
    is left exactly as written and only the text around it is cleaned.
    """
    pieces: list[str] = []
    last = 0
    for drawing in FIGURE.finditer(text):
        pieces.extend((_prose_ready(text[last : drawing.start()]), drawing.group(0)))
        last = drawing.end()
    pieces.append(_prose_ready(text[last:]))
    return "".join(pieces)


def _prose_ready(text: str) -> str:
    if not text:
        return text
    decoded = repair_math_control_chars(decode_llm_json_escapes(text))
    prose = demote_html(strip_json_residue(decoded))
    return delimit_bare_math(close_unclosed_math(prose))
