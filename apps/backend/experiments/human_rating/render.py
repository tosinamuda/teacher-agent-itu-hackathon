"""Markdown to a Google-Docs-ready .docx: pandoc for the body, python-docx for the look.

pandoc does the body, by way of HTML: the packs carry the HTML the model wrote — tables,
lists, line breaks, superscripts — and read straight into docx those tags are dropped
with their structure, while an HTML round trip keeps them. TeX becomes native Word
equations, which Google Docs imports as equations, and pipe tables become tables a rater
can type into. The page, the type and every table's width come from
:mod:`template`'s reference document, so pandoc sizes them correctly rather than being
corrected afterwards. :mod:`layout` supplies what a reference document cannot: the
footer fields, the page breaks, and the ruling on the forms.

The leak scan is the last thing that runs before a document is written, and it runs
again on the document as written. Every token that could de-anonymise a set — a
condition, a version, a student id, a lesson code, a candidate hash — refuses the build
rather than warning about it.
"""

from __future__ import annotations

import re
import subprocess
import zipfile
from pathlib import Path

from docx import Document

from . import layout, template

#: fancy_lists is off: a teacher's "(a) Define statistic" is an item's text, not a nested
#: lettered list.
PANDOC_FROM = "markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+raw_html-fancy_lists"

#: Anything a rater must never read. Word-bounded where the token is short enough to
#: occur inside ordinary prose or mathematics.
FORBIDDEN: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("condition label", re.compile(r"\b[CP][0-4]\b")),
    ("student id", re.compile(r"\bstudent-\d\d\b")),
    ("lesson code", re.compile(r"\bt[23]-w\d\d\b")),
    ("internal packet id", re.compile(r"\bh[12]-l\d\d-")),
    ("candidate hash", re.compile(r"\bcand-[0-9a-f]{8}\b")),
    ("run label", re.compile(r"\b(deepseek|gpt-oss|c0c3-)\b", re.I)),
)
#: Vocabulary that would tell a rater how the material was made. Reported, not refused:
#: "model" is a word mathematics uses.
SENSITIVE_WORDS = re.compile(
    r"\b(generated|generation|LLM|language model|artificial intelligence"
    r"|personalis(ed|ation) system)\b",
    re.I,
)


class LeakError(ValueError):
    pass


def leak_scan(text: str) -> None:
    hits = [(label, m.group(0)) for label, pattern in FORBIDDEN for m in pattern.finditer(text)]
    if hits:
        shown = ", ".join(f"{label}: {token!r}" for label, token in hits[:6])
        raise LeakError(f"{len(hits)} identifying token(s) in a rater document — {shown}")


def sensitive_words(text: str) -> list[str]:
    return sorted({m.group(0) for m in SENSITIVE_WORDS.finditer(text)})


def to_docx(markdown: str, path: Path, *, rater_number: int, set_id: str) -> None:
    leak_scan(markdown)
    path.parent.mkdir(parents=True, exist_ok=True)
    html = subprocess.run(
        ["pandoc", "-f", PANDOC_FROM, "-t", "html", "--mathml"],
        input=markdown.encode("utf-8"),
        check=True,
        capture_output=True,
    ).stdout
    subprocess.run(
        [
            "pandoc",
            "-f",
            "html",
            "-t",
            "docx",
            "--reference-doc",
            str(template.PATH),
            "-o",
            str(path),
        ],
        input=html,
        check=True,
        capture_output=True,
    )
    footer_left = f"Rater {rater_number} | {set_id}"
    document = Document(str(path))
    layout.finish(document, footer_left)
    document.save(str(path))
    _check_written(path, footer_left)


def _check_written(path: Path, footer_left: str) -> None:
    """The document as written, not the markdown, is what a rater opens."""
    text = docx_text(path)
    leak_scan(text)
    if footer_left not in text or "Page" not in text:
        raise RuntimeError(f"{path.name}: footer not stamped")
    for sentinel in (layout.PAGE_BREAK, layout.RULE):
        if sentinel in text:
            raise RuntimeError(f"{path.name}: {sentinel} reached the page")


def docx_text(path: Path) -> str:
    """Every string in the document, body and footers, for a check that reads the artefact."""
    with zipfile.ZipFile(path) as archive:
        parts = [n for n in archive.namelist() if n.startswith("word/") and n.endswith(".xml")]
        xml = "".join(archive.read(n).decode("utf-8", "replace") for n in parts)
    return re.sub(r"\s+", " ", " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", xml)))
