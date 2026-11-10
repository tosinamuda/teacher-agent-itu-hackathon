"""Which learning objective each scoring page of a returned rating document was about.

The released tables number a set's objectives as its pages did. A Part 2 set compares only
the objectives the learner has class work for, so its "Objective 2 of 2" can be the lesson's
third; the page names the objective, and that is what is read here.
"""

from __future__ import annotations

import io
import re
from dataclasses import dataclass
from typing import Any

from docx import Document

_SCORING_PAGE = re.compile(r"^Objective (\d+) of \d+ — your (scores|comparison)$")
_OBJECTIVE = "Learning objective. "
#: Word text, including the text inside equations, which a paragraph's own text leaves out.
_TEXT = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"
_MATH_TEXT = "{http://schemas.openxmlformats.org/officeDocument/2006/math}t"


@dataclass(frozen=True)
class ReturnedDocument:
    #: Each scoring page's objective, as the page names it, by its number in the set.
    objectives: dict[int, str]


def _text(paragraph: Any) -> str:
    """The paragraph as read, equations included, with its line breaks."""
    parts = []
    for node in paragraph._p.iter():
        if node.tag in (_TEXT, _MATH_TEXT):
            parts.append(node.text or "")
        elif node.tag.endswith("}br"):
            parts.append("\n")
    return "".join(parts)


def read_document(data: bytes) -> ReturnedDocument:
    paragraphs = [_text(paragraph) for paragraph in Document(io.BytesIO(data)).paragraphs]
    objectives: dict[int, str] = {}
    for index, text in enumerate(paragraphs):
        page = _SCORING_PAGE.match(text)
        if page is None:
            continue
        named = next(p for p in paragraphs[index + 1 :] if p.startswith(_OBJECTIVE))
        objectives[int(page.group(1))] = named.removeprefix(_OBJECTIVE).split("\n")[0].strip()
    return ReturnedDocument(objectives)
