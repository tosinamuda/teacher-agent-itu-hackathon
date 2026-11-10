"""How each lesson became data, as the release publishes it: the transcripts of its pages.

A lesson carries its teacher's pages transcribed verbatim (``teacher.md``, never edited), the
same cleaned for the study (``teacher-cleaned.md``) and the log of every change with the
source that licenses it (``_cleaning-log.md``); a lesson Part 2 covered carries each learner's
marked script too (``student-NN.md``). Each file opens with a YAML header naming the
photographed pages it was transcribed from, which stay private.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import yaml

#: A transcript's file name, and the kind of record it is.
KINDS = {
    "teacher.md": "teacher_record",
    "teacher-cleaned.md": "teacher_cleaned",
    "_cleaning-log.md": "cleaning_log",
}
LEARNER_SCRIPT = "learner_script"


@dataclass(frozen=True)
class PublishedTranscript:
    kind: str
    #: The learner's pseudonym, e.g. ``student-03``, for a script.
    pseudonym: str | None
    header: dict[str, Any]
    body: str
    path: str
    sha256: str


def kind_of(name: str) -> str | None:
    """The kind of record a transcript file is, or none for a file that is not one."""
    if name.startswith("student-") and name.endswith(".md"):
        return LEARNER_SCRIPT
    return KINDS.get(name)


def split(text: str) -> tuple[dict[str, Any], str]:
    """The file's YAML header, made JSON-safe, and the text after it."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.index("\n---", 4)
    header = yaml.safe_load(text[4:end]) or {}
    # Dates in a header come back as dates; the record keeps them as the text they were.
    return json.loads(json.dumps(header, default=str)), text[end + 4 :].lstrip("\n")


def pages_of(header: dict[str, Any]) -> list[dict[str, str]]:
    """The photographed pages a transcript came from, each with the part of it the page held."""
    return [
        {"file": str(page.get("file")), "role": str(page.get("role") or "")}
        if isinstance(page, dict)
        else {"file": str(page), "role": "script"}
        for page in header.get("pages") or []
    ]
