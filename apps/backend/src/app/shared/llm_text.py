r"""Repairing the damage between the model's string and ours.

Everything here undoes something that happened to the text *in transit* — the
model wrote one thing and a parse step handed us another:

- JSON-style escape sequences that arrive as backslash-pairs rather than the
  characters they encode (e.g. ``\n`` instead of a real newline). Decoded
  generically without hardcoded case-by-case rules.
- LaTeX math regions (``$…$`` / ``$$…$$``) that share the backslash-escape
  syntax with JSON (``\times``, ``\frac``, ``\\``) and must stay intact for
  the downstream math renderer.
- A string field that over-ran its own closing quote and carried the rest of
  the enclosing JSON object into itself.

The decoding is math-region-aware: math runs are passed through verbatim;
only the text between (and outside) them is decoded. :func:`split_math_runs`
is that split, shared with :mod:`app.shared.llm_markup`, which repairs what the
model *wrote* rather than what the transport did to it.
"""

from __future__ import annotations

import re

# Math runs delimited by ``$…$`` / ``$$…$$`` OR ``\(…\)`` / ``\[…\]``. The LLM
# emits the LaTeX-style ``\(…\)`` / ``\[…\]`` delimiters in practice, so both
# families MUST be recognised — otherwise the JSON-escape decode below mangles
# LaTeX commands inside them (``\frac`` -> form-feed + ``rac``, ``\times`` ->
# tab + ``imes``). Inline ``$…$`` is one logical run with no further unescaped
# ``$``; everything tolerates newlines so wrapped math survives.
#
# An inline ``$`` run stops at a markdown emphasis marker or a blank line, which
# bounds the damage a dropped closing ``$`` can do. The model wrote
# ``**Join $A$ to $B**.`` — one delimiter short — and every ``$`` after it in the
# block paired with the wrong partner, so prose was decoded as math (a literal
# ``\n\n`` reached the page) and math was decoded as prose (``\angle``, ``\circ``
# reached it as backslashes). Maths is neither bold nor a paragraph, so a run that
# would have to cross one of those has lost its partner and is left as text.
#
# An environment standing in prose with no delimiter around it (``\begin{array}…``) is
# maths too: its ``\\`` row breaks are not escapes, and wrapping each command in it
# separately would split it. :func:`~app.shared.llm_markup.delimit_bare_math` displays it.
# One still escaped twice is prose until the decode has halved its backslashes.
_ENVIRONMENTS = (
    r"(?:array|aligned|align\*?|gathered|gather\*?|split|cases|[pbBvV]?matrix|eqnarray\*?)"
)
_MATH_RUN_RE = re.compile(
    r"(\$\$.*?\$\$|\$(?:\\\$|(?!\*\*|\n\n)[^$])+?\$|\\\(.*?\\\)|\\\[.*?\\\]"
    rf"|(?<!\\)\\begin\{{{_ENVIRONMENTS}\}}.*?\\end\{{{_ENVIRONMENTS}\}})",
    re.DOTALL,
)


def split_math_runs(text: str) -> list[str]:
    """Split into alternating prose and math runs; test each with :func:`is_math_run`."""
    return _MATH_RUN_RE.split(text)


def is_math_run(part: str) -> bool:
    """Whether a split part is a math run (passed through the decode verbatim)."""
    return part.startswith(("$", "\\(", "\\[")) or is_bare_environment(part)


def is_bare_environment(part: str) -> bool:
    """Whether a split part is an environment standing in prose with no delimiter."""
    return part.startswith("\\begin")


# Standard JSON / Python string-escape sequences. ``\u`` reads a 4-digit hex
# codepoint; the simple single-character escapes map to their corresponding
# control characters. A trailing backslash with no follow-on is left alone so
# we never silently swallow data.
_JSON_ESCAPE_RE = re.compile(r"\\(u[0-9a-fA-F]{4}|[nrtbf\"\\/])")
_SIMPLE_ESCAPES = {
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "b": "\b",
    "f": "\f",
    '"': '"',
    "\\": "\\",
    "/": "/",
}


#: ``\u20a6`` typed as text inside a formula is the naira sign, not a LaTeX command.
_UNICODE_ESCAPE_RE = re.compile(r"\\(u[0-9a-fA-F]{4})")


def _decode_one(match: re.Match[str]) -> str:
    seq = match.group(1)
    if seq.startswith("u"):
        return chr(int(seq[1:], 16))
    return _SIMPLE_ESCAPES.get(seq, match.group(0))


def decode_llm_json_escapes(text: str) -> str:
    r"""Decode JSON-style escape sequences outside LaTeX math regions.

    Handles every JSON escape (``\n``, ``\r``, ``\t``, ``\b``, ``\f``, ``\"``,
    ``\\``, ``\/``, ``\uXXXX``) the LLM might leave behind as literal text.
    Math regions
    (``$…$`` / ``$$…$$`` and ``\(…\)`` / ``\[…\]``) are passed through unchanged, except
    for ``\uXXXX``, because LaTeX shares the rest of the escape syntax (``\times``, ``\frac``,
    ``\\``) and it must not be decoded.

    Idempotent: re-running on already-decoded text is a no-op because none of
    the decoded outputs match the escape pattern again.

    Args:
        text: LLM-authored text — typed model field, manifest content, etc.

    Returns:
        The same text with JSON escapes outside math decoded; math regions
        and unknown escape sequences are left untouched.
    """
    if not text:
        return text
    parts = split_math_runs(text)
    out: list[str] = []
    for part in parts:
        if is_math_run(part):
            out.append(_UNICODE_ESCAPE_RE.sub(_decode_one, part))
        else:
            out.append(_JSON_ESCAPE_RE.sub(_decode_one, part))
    return "".join(out)


# Control characters that stand where a LaTeX command's escape was: a JSON decode
# makes them of ``\b`` ``\f`` ``\n`` ``\r`` ``\t`` (``\frac`` -> form feed + ``rac``), and a
# Python string of ``\a`` ``\v`` (the textbook corpus has ``\angle`` as a bell + ``ngle``).
_CTRL_TO_ESCAPE = {
    "\n": r"\n",
    "\r": r"\r",
    "\t": r"\t",
    "\b": r"\b",
    "\f": r"\f",
    "\a": r"\a",
    "\v": r"\v",
}

# Only where a letter runs straight into one: a tab before whitespace is layout. A
# newline is a real line break, in prose and in a display block written over several
# lines, so it is restored only in maths and only before the rest of a command that
# begins with ``\n`` — two letters at least, as a line may begin with a variable ``u``.
_EATEN_COMMAND_RE = re.compile(r"[\t\b\f\a\v\r](?=[a-zA-Z])")
_EATEN_IN_MATH_RE = re.compile(
    r"[\t\b\f\a\v\r](?=[a-zA-Z])"
    r"|\n(?=(?:ewline|eq|eg|ot|otin|abla|exists|mid|parallel|leq|geq|subseteq|supseteq|cong"
    r"|sim|earrow|warrow|atural|olimits|onumber|ormalsize)(?![a-zA-Z]))"
)


def repair_math_control_chars(text: str) -> str:
    r"""Restore LaTeX commands an escape-decode ate, in math and in prose.

    ``\times`` written with one backslash is valid JSON, so the parser hands
    back a tab and ``imes`` before any of our code sees the string — a reader
    gets "4 imes 5". Two blinded judges marked packs down for it.

    A newline is restored in maths only, and only before a command's remaining
    letters; everywhere else it is the break it looks like. Idempotent — clean text
    has no control characters to find.
    """
    if not text:
        return text
    return "".join(
        (_EATEN_IN_MATH_RE if is_math_run(part) else _EATEN_COMMAND_RE).sub(
            lambda match: _CTRL_TO_ESCAPE[match.group(0)], part
        )
        for part in split_math_runs(text)
    )


# A field that ran past its own closing quote: the value, then the quote that should
# have ended it, then whatever the model was writing next in the enclosing object —
# a comma, and sometimes the following key. ``"answer": "4xy",\n  "worked_solution":``
# arrived as the single string ``4xy",\n  "worked_solution":`` and a learner read the
# punctuation as part of the answer.
_JSON_RESIDUE_RE = re.compile(r'"[ \t]*,?\s*(?:"[a-z_]+"\s*:)?\s*$')


def strip_json_residue(text: str) -> str:
    r"""Cut a trailing run of JSON punctuation a string field swallowed.

    Only where the quote is **unpaired** — an even number of quotes before it means
    it closes one the field opened, and ``write the answer with the unit "cm".`` is
    the model quoting a word rather than leaking its own syntax. Idempotent: what is
    left ends in no quote at all.
    """
    if not text or '"' not in text:
        return text
    match = _JSON_RESIDUE_RE.search(text)
    if match is None or text[: match.start()].count('"') % 2:
        return text
    return text[: match.start()].rstrip()
