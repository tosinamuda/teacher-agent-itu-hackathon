"""The TikZ drawings written into stored content, and the id each is served under.

A drawing's id is the SHA-256 of its ``tikzpicture`` source, trimmed. It is the same wherever
the drawing is written — inside a note's prose or lifted into a figure block's
``source_tikz`` — so one drawing is drawn and stored once, and a reader that holds the
source can name the figure without asking the server. The browser computes it the same way.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterator

# A drawing, with the centring wrapper it is usually placed in.
FIGURE = re.compile(
    r"(?:\\begin\{center\}\s*)?(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})"
    r"(?:\s*\\end\{center\})?",
    re.DOTALL,
)


def figure_id(source: str) -> str:
    return hashlib.sha256(source.strip().encode("utf-8")).hexdigest()


def drawings_in(value: object) -> Iterator[str]:
    """Every drawing's source in a stored JSON value, however deeply it is written."""
    if isinstance(value, str):
        if "tikzpicture" in value:
            yield from (source.strip() for source in FIGURE.findall(value))
    elif isinstance(value, dict):
        for item in value.values():
            yield from drawings_in(item)
    elif isinstance(value, list):
        for item in value:
            yield from drawings_in(item)
