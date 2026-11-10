"""The released study, read from the two published datasets and checked against their record.

Every file read is checked against the SHA-256 its dataset's ``PROVENANCE.json`` lists, so an
import is of the release as published or of nothing.

The lesson plans are the frozen plans the study's generator read (``inputs/eval_set.json``),
without the notes it carried inline: a lesson note is its own record. The notes are the
corrected notes Part 1 read, one file per step (``notes/<lesson>/<step>.md``). A lesson's
classwork is the learners' marked scripts its learner states were read from
(``transcripts/<lesson>/classwork.xml``), for the lessons Part 2 covered. Its transcripts are
how it became data: its teacher's pages verbatim, then cleaned, with the log of every change,
and the learners' scripts (``transcripts/<lesson>/*.md``).
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from lxml import etree
from openpyxl import load_workbook

from experiments.h2_personalisation_eval.students import Classwork, parse
from experiments.study_import.documents import ReturnedDocument, read_document
from experiments.study_import.transcripts import (
    LEARNER_SCRIPT,
    PublishedTranscript,
    kind_of,
    split,
)

LESSON_PLANS = "ng-jss1-math-lesson-plans"
RATINGS = "ng-jss1-math-alignment-ratings"
#: The rated Part 1 run, and Part 2's run built on its C3 draw 1.
PART_1_RUN = "runs/h1/c0c3-prism-objective/run.json"
PART_2_RUN = "runs/h2/h2-deepseek-clean/run.json"
PART_2_ALLOCATION = "ratings/allocation/h2.xlsx"
#: A step's lesson note, which is its own record, not a field of the plan.
LESSON_NOTE_FIELDS = ("note", "note_file")


class DatasetMismatchError(ValueError):
    """A file is not what the dataset's record says it is."""


@dataclass(frozen=True)
class StudyLesson:
    lesson: str
    plan: dict[str, Any]
    #: Each step's lesson note as Part 1 read it, in plan order.
    note_sections: tuple[tuple[str, str], ...]

    @property
    def term(self) -> str:
        return str(self.plan["term"])

    @property
    def week(self) -> int:
        return int(self.plan["week"])


class _Dataset:
    """One published dataset, whose files are read only after their hash is checked."""

    def __init__(self, root: Path) -> None:
        provenance = json.loads((root / "PROVENANCE.json").read_text(encoding="utf-8"))
        self._root = root
        self._sha256: dict[str, str] = {
            entry["path"]: entry["sha256"] for entry in provenance["files"]
        }

    def read_bytes(self, path: str) -> bytes:
        recorded = self._sha256.get(path)
        if recorded is None:
            raise DatasetMismatchError(f"{self._root.name}/{path} is not in its PROVENANCE.json")
        data = (self._root / path).read_bytes()
        if hashlib.sha256(data).hexdigest() != recorded:
            raise DatasetMismatchError(f"{self._root.name}/{path} differs from its PROVENANCE.json")
        return data

    def lists(self, path: str) -> bool:
        return path in self._sha256

    def listed_under(self, folder: str) -> list[str]:
        """The files its record lists directly in the folder, in name order."""
        prefix = f"{folder}/"
        return sorted(
            path
            for path in self._sha256
            if path.startswith(prefix) and "/" not in path[len(prefix) :]
        )

    def sha256_of(self, path: str) -> str:
        return self._sha256[path]

    def json(self, path: str) -> Any:
        return json.loads(self.read_bytes(path).decode("utf-8"))

    def text(self, path: str) -> str:
        return self.read_bytes(path).decode("utf-8")

    def rows(self, path: str) -> list[dict[str, str]]:
        return list(csv.DictReader(io.StringIO(self.text(path))))


class ReleasedStudy:
    """The study's lessons, runs and ratings, from a folder holding both datasets."""

    def __init__(self, root: Path) -> None:
        self._plans = _Dataset(root / LESSON_PLANS)
        self._ratings = _Dataset(root / RATINGS)

    def lessons(self) -> list[StudyLesson]:
        lessons = []
        for case in self._ratings.json("inputs/eval_set.json")["cases"]:
            plan = case["plan"]
            sections = tuple(
                (step["step_id"], self._plans.text(f"notes/{case['lesson']}/{step['step_id']}.md"))
                for step in plan["steps"]
                if step.get("note")
            )
            steps = [
                {key: value for key, value in step.items() if key not in LESSON_NOTE_FIELDS}
                for step in plan["steps"]
            ]
            lessons.append(StudyLesson(case["lesson"], {**plan, "steps": steps}, sections))
        return lessons

    def classwork(self, lesson: str) -> Classwork | None:
        """The lesson's marked classwork, where the release carries it."""
        path = f"transcripts/{lesson}/classwork.xml"
        if not self._plans.lists(path):
            return None
        return parse(etree.fromstring(self._plans.read_bytes(path)), lesson)

    def transcripts(self, lesson: str) -> list[PublishedTranscript]:
        """The lesson's published transcripts: its teacher's pages and any learners' scripts."""
        found = []
        for path in self._plans.listed_under(f"transcripts/{lesson}"):
            name = path.rsplit("/", 1)[1]
            kind = kind_of(name)
            if kind is None:
                continue
            header, body = split(self._plans.text(path))
            pseudonym = name.removesuffix(".md") if kind == LEARNER_SCRIPT else None
            found.append(
                PublishedTranscript(
                    kind, pseudonym, header, body, path, self._plans.sha256_of(path)
                )
            )
        return found

    def part_1(self) -> dict[str, Any]:
        return dict(self._ratings.json(PART_1_RUN))

    def part_2(self) -> dict[str, Any]:
        return dict(self._ratings.json(PART_2_RUN))

    def document_index(self) -> list[dict[str, str]]:
        """Every returned rating document, answered or not, as the release indexes them."""
        return self._ratings.rows("ratings/documents.csv")

    def part_2_allocation(self) -> list[dict[str, Any]]:
        """Which learner's two notes each Part 2 set carried, and in which order."""
        workbook = load_workbook(
            io.BytesIO(self._ratings.read_bytes(PART_2_ALLOCATION)), read_only=True, data_only=True
        )
        rows = workbook["H2_Packet_Map"].iter_rows(values_only=True)
        header = [str(name) for name in next(rows)]
        return [dict(zip(header, row, strict=True)) for row in rows if any(row)]

    def returned_documents(self, paths: set[str]) -> dict[str, ReturnedDocument]:
        """The returned rating documents the ratings were read from, as the raters left them."""
        return {path: read_document(self._ratings.read_bytes(path)) for path in sorted(paths)}

    def part_1_ratings(self) -> list[dict[str, str]]:
        return self._ratings.rows("ratings/part1_ratings.csv")

    def part_2_judgements(self) -> list[dict[str, str]]:
        return self._ratings.rows("ratings/part2_judgements.csv")
