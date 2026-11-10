r"""Demoting the HTML the model wrote to the markdown a reader can be shown.

Every reader-facing surface XML-escapes a field before converting its markdown —
the WeasyPrint worksheet in ``_render_markdown``, the browser through
``react-markdown`` with no raw-HTML plugin — so a ``<strong>`` the model emitted
reaches the learner as the six literal characters ``<strong>``. The output schema
says "Markdown only, NEVER HTML" on the field and the model wrote 4,727 tags across
the 72 packs of ``c0c3-prism-objective`` regardless: bold, italic, line breaks,
lists, headings and whole tables, in every lesson and every condition.

Nothing here is lost in transit or written in the wrong notation for maths; that
is :mod:`app.shared.llm_text` and :mod:`app.shared.llm_markup`. This is the model
choosing a markup the renderer does not read, demoted to the one it does. Math runs
are never entered — ``$a<b$`` is a comparison, not a tag — and the result contains
no tag, so a second pass is a no-op.
"""

from __future__ import annotations

import re
from html import unescape
from html.parser import HTMLParser

from app.shared.llm_text import is_math_run, split_math_runs

# A tag as the model writes one. Text with a bare ``<`` — "3 < 5", "x<5" — never
# matches, so it never enters the parser and cannot be misread as markup.
_TAG_RE = re.compile(r"</?[a-zA-Z][a-zA-Z0-9]*(?:\s[^<>]*)?/?>")

_EMPHASIS = {"strong": "**", "b": "**", "em": "*", "i": "*"}
_SUPERSCRIPT = str.maketrans("0123456789+-=()n", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ")
_SUBSCRIPT = str.maketrans("0123456789+-=()", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎")

# Entities that spell a tag once decoded. Left as written so a literal ``&lt;strong&gt;``
# stays inert on the way out and again on the way back in.
_INERT_ENTITIES = {"lt", "gt", "amp"}
_MANY_BLANK_LINES_RE = re.compile(r"\n{3,}")
_TRAILING_SPACE_RE = re.compile(r"[ \t]+\n")


def demote_html(text: str) -> str:
    """Rewrite the HTML in *text* as markdown, leaving math runs untouched."""
    if not text or not _TAG_RE.search(text):
        return text
    return "".join(
        part if is_math_run(part) or not _TAG_RE.search(part) else _demote_prose(part)
        for part in split_math_runs(text)
    )


def count_html_tags(text: str) -> int:
    """How many tags would reach a reader as literal angle brackets.

    What :func:`demote_html` rewrites, counted rather than rewritten, so the run
    metric and the repair share one idea of what "HTML" is.
    """
    return sum(
        len(_TAG_RE.findall(part)) for part in split_math_runs(text) if not is_math_run(part)
    )


def _demote_prose(part: str) -> str:
    emitter = _MarkdownEmitter()
    emitter.feed(part)
    emitter.close()
    out = _TRAILING_SPACE_RE.sub("\n", emitter.result())
    return _MANY_BLANK_LINES_RE.sub("\n\n", out).strip("\n")


class _Frame:
    """An open element collecting the text written inside it."""

    __slots__ = ("tag", "parts")

    def __init__(self, tag: str) -> None:
        self.tag = tag
        self.parts: list[str] = []

    def text(self) -> str:
        return "".join(self.parts)


class _MarkdownEmitter(HTMLParser):
    """Walk the model's HTML once and write the markdown it stands for.

    Containers — emphasis, super/subscript, headings, list items, table cells — open a
    frame that collects their text and is rendered when they close, so nesting falls
    out of the stack and emphasis markers land flush against the words they wrap.
    Everything not known is unwrapped: its text kept, its tag dropped.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self._out: list[str] = []
        self._frames: list[_Frame] = []
        self._lists: list[tuple[str, int]] = []
        self._rows: list[list[str]] | None = None
        self._row: list[str] = []

    def result(self) -> str:
        return "".join(self._out)

    # -- where text goes --------------------------------------------------------

    def _write(self, text: str) -> None:
        (self._frames[-1].parts if self._frames else self._out).append(text)

    def _paragraph_break(self) -> None:
        if self._frames:
            return
        written = "".join(self._out)
        if written and not written.endswith("\n\n"):
            self._out.append("\n" if written.endswith("\n") else "\n\n")

    def _ends_with_newline(self) -> bool:
        parts = self._frames[-1].parts if self._frames else self._out
        return bool(parts) and parts[-1].endswith("\n")

    def handle_data(self, data: str) -> None:
        # Whitespace between a table's tags is layout, not a cell; and the space the
        # model puts after a <br> would open the next line indented.
        if self._rows is not None and not self._frames and not data.strip():
            return
        if self._ends_with_newline():
            data = data.lstrip(" \t")
        self._write(data.replace("\xa0", " "))

    def handle_entityref(self, name: str) -> None:
        if name == "nbsp":
            self._write(" ")
        elif name in _INERT_ENTITIES:
            self._write(f"&{name};")
        else:
            self._write(unescape(f"&{name};"))

    def handle_charref(self, name: str) -> None:
        self._write(unescape(f"&#{name};"))

    # -- tags -------------------------------------------------------------------

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if _opens_frame(tag):
            if _heading_level(tag):
                self._paragraph_break()
            self._frames.append(_Frame(tag))
        elif tag == "br":
            self._write("\n")
        elif tag in ("p", "div", "center"):
            self._paragraph_break()
        elif tag in ("ul", "ol"):
            if not self._lists:
                self._paragraph_break()
            self._lists.append((tag, 0))
        elif tag == "li":
            self._start_item()
        elif tag == "table":
            self._paragraph_break()
            self._rows = []
        elif tag == "tr":
            self._row = []

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if self._frames and self._frames[-1].tag == tag:
            self._close_frame(self._frames.pop())
        elif tag in ("p", "div", "center"):
            self._paragraph_break()
        elif tag in ("ul", "ol") and self._lists:
            self._lists.pop()
            if not self._lists:
                self._paragraph_break()
        elif tag == "tr" and self._rows is not None:
            self._rows.append(self._row)
        elif tag == "table" and self._rows is not None:
            self._out.append(_pipe_table(self._rows))
            self._rows = None
            self._paragraph_break()

    # -- rendering a closed container -------------------------------------------

    def _close_frame(self, frame: _Frame) -> None:
        tag, inner = frame.tag, frame.text()
        if tag in _EMPHASIS:
            self._write(_emphasised(inner, _EMPHASIS[tag]))
        elif tag == "sup":
            self._write(_script(inner, _SUPERSCRIPT, "^"))
        elif tag == "sub":
            self._write(_script(inner, _SUBSCRIPT, "_"))
        elif tag in ("td", "th"):
            self._row.append(" ".join(inner.split()))
        else:
            self._out.append("#" * _heading_level(tag) + " " + inner.strip() + "\n\n")

    def _start_item(self) -> None:
        if not self._lists:
            self._lists.append(("ul", 0))
        kind, count = self._lists[-1]
        self._lists[-1] = (kind, count + 1)
        marker = f"{count + 1}." if kind == "ol" else "-"
        written = "".join(self._out)
        if written and not written.endswith("\n"):
            self._out.append("\n")
        self._out.append("  " * (len(self._lists) - 1) + marker + " ")


def _heading_level(tag: str) -> int:
    return int(tag[1:]) if tag[0] == "h" and tag[1:].isdigit() else 0


def _opens_frame(tag: str) -> bool:
    return tag in _EMPHASIS or tag in ("sup", "sub", "td", "th") or _heading_level(tag) > 0


def _emphasised(inner: str, marker: str) -> str:
    """``**word**`` with any surrounding whitespace moved outside the markers."""
    body = inner.strip()
    if not body:
        return inner
    lead = inner[: len(inner) - len(inner.lstrip())]
    trail = inner[len(inner.rstrip()) :]
    return f"{lead}{marker}{body}{marker}{trail}"


def _script(inner: str, table: dict[int, int], fallback: str) -> str:
    """``cm<sup>3</sup>`` as ``cm³``; anything without a glyph as ``cm^3``."""
    body = inner.strip()
    translated = body.translate(table)
    if all(ord(ch) > 127 for ch in translated) and translated:
        return translated
    return f"{fallback}{body}"


def _pipe_table(rows: list[list[str]]) -> str:
    """A GFM table, its first row the header; every row padded to the widest."""
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    padded = [row + [""] * (width - len(row)) for row in rows]
    header, *body = padded
    lines = [
        "| " + " | ".join(header) + " |",
        "|" + "|".join(" --- " for _ in header) + "|",
        *("| " + " | ".join(row) + " |" for row in body),
    ]
    return "\n".join(lines) + "\n"
