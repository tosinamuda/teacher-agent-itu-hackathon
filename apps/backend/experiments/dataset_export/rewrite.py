"""The only ways a published file may differ from the file in the repository.

There are three, and each concerns a participant rather than the study. The school's
abbreviation is replaced wherever it stands as a word. The warning at the head of each
classwork file, written for a repository the file was never meant to leave, is replaced
with the basis on which it is released. And a path into the private captures, which the
transcriptions record as their source, is replaced by a note that the captures are not
released, since a reader of the release has no such folder. Everything else is copied byte
for byte.

The school rewrite is whole-word on purpose. Development traces record tool-call ids such
as ``call_00_zpQGTC…`` whose letters happen to spell it; rewriting those would change the
record of what was sent to the model, which a published trace must never do.
"""

from __future__ import annotations

import re
from pathlib import PurePosixPath

SCHOOL = re.compile(r"\bgtc\b", re.IGNORECASE)
REPLACEMENT = "sch"

#: Decoded and rewritten. Anything else is copied as bytes: a PDF or a .docx can hold the
#: three letters inside a compressed stream, and rewriting there would corrupt the file.
TEXT_SUFFIXES = frozenset(
    {".csv", ".html", ".json", ".jsonl", ".md", ".rng", ".tex", ".txt", ".xml", ".yaml", ".yml"}
)

CLASSWORK_WARNING = (
    "<!--\n"
    "  Student classwork, structured. Identifiable work by minors: this file and\n"
    "  its sources never leave this repository. Regenerate with build_classwork.py;\n"
    "  the markdown transcriptions remain the record.\n"
    "-->"
)

CLASSWORK_RELEASE = (
    "<!--\n"
    "  Student classwork, structured and de-identified: each learner's marked answers for\n"
    "  one lesson, released with the school's permission, which covers publication. Names\n"
    "  were covered before capture and no key links an id to a child. The photographs it\n"
    "  was transcribed from are not released.\n"
    "-->"
)


#: A path into the private captures: in backticks as prose names it, or as a field's value to
#: the end of its line.
CAPTURES = "original-captures"
PRIVATE_PATH = re.compile(rf"`\.\./{CAPTURES}/[^`\n]*`|\.\./{CAPTURES}/[^\n]*")
PRIVATE_NOTE = "[original captures, not released]"


class ExportError(ValueError):
    """A file could not be published the way the manifest requires."""


def without_school(text: str) -> str:
    """Replace the school's abbreviation wherever it stands as a word, keeping its case."""
    return SCHOOL.sub(_same_case, text)


def _same_case(match: re.Match[str]) -> str:
    return "".join(
        new.upper() if old.isupper() else new
        for old, new in zip(match.group(0), REPLACEMENT, strict=True)
    )


def published(path: str, data: bytes) -> bytes:
    """The bytes a file is published with."""
    if PurePosixPath(path).suffix not in TEXT_SUFFIXES:
        return data
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ExportError(f"{path}: not UTF-8, so it cannot be rewritten safely") from error
    if PurePosixPath(path).name == "classwork.xml":
        text = _released_classwork(path, text)
    return without_private_paths(without_school(text)).encode("utf-8")


def without_private_paths(text: str) -> str:
    """Replace every path into the private captures with a note that they are not released."""
    return PRIVATE_PATH.sub(PRIVATE_NOTE, text)


def _released_classwork(path: str, text: str) -> str:
    if CLASSWORK_WARNING not in text:
        raise ExportError(f"{path}: classwork warning changed; refusing to ship it unreplaced")
    return text.replace(CLASSWORK_WARNING, CLASSWORK_RELEASE, 1)
