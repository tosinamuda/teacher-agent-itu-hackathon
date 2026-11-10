"""The study's ratings, as its raters recorded them, against the revision notes they rated.

Part 1 scored one class revision note per packet; the note is named by lesson, condition and
draw. Part 2 compared a learner's P0 and P1 notes, shown as A and B in an order the rater did
not know; ``a_was`` and ``b_was`` unblind it. Criteria are numbered as on the rating documents,
in the order the study's protocol lists them.

Each scoring page names its learning objective. Part 1's recorded objective is checked against
it; Part 2 recorded only the objective's number in the set, so its objective is read from it.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from app.domains.evaluation.domain.study_instrument import H1_CRITERIA, H2_CRITERIA
from app.domains.evaluation.infrastructure.study_rating_models import (
    StudyComparativeJudgement,
    StudyCriterionScore,
    StudyRatingDocument,
)
from experiments.study_import.dataset import DatasetMismatchError
from experiments.study_import.documents import ReturnedDocument
from experiments.study_import.raters import Raters
from experiments.study_import.runs import part_1_note_id, part_2_note_id

Documents = Mapping[str, ReturnedDocument]


def _comment(row: dict[str, str]) -> str | None:
    return row["comment"].strip() or None


def _comparable(text: str) -> str:
    """An objective as words and numbers, however its maths was typeset."""
    return " ".join(re.findall(r"[a-z0-9]+", re.sub(r"\\[a-zA-Z]+", " ", text).lower()))


class ObjectiveNames:
    """Each lesson's objectives, found by the text a rating page names them with."""

    def __init__(self, plans: Mapping[str, Mapping[str, Any]]) -> None:
        self._ids = {
            lesson: {
                _comparable(str(objective["objective_text"])): str(objective["lesson_objective_id"])
                for objective in plan["lesson_plan_objectives"]
            }
            for lesson, plan in plans.items()
        }

    def on_page(self, row: dict[str, str], documents: Documents) -> str:
        named = documents[row["document"]].objectives.get(int(row["objective_index"]), "")
        found = self._ids[row["lesson"]].get(_comparable(named))
        if found is None:
            raise DatasetMismatchError(
                f"{row['document']}: objective {row['objective_index']} names {named!r}, "
                f"which is not an objective of {row['lesson']}"
            )
        return found


def part_1_scores(
    rows: list[dict[str, str]], documents: Documents, objectives: ObjectiveNames, raters: Raters
) -> list[StudyCriterionScore]:
    scores = []
    for row in rows:
        if objectives.on_page(row, documents) != row["lesson_objective_id"]:
            raise DatasetMismatchError(
                f"{row['document']}: objective {row['objective_index']} is recorded as "
                f"{row['lesson_objective_id']} but its page names another"
            )
        scores.append(
            StudyCriterionScore(
                artefact_id=part_1_note_id(row["lesson"], row["condition"], int(row["draw"])),
                rater=row["rater"],
                rater_db_id=raters[row["rater"]].id,
                delivery_order=int(row["delivery_order"]),
                packet=row["external_packet_id"],
                objective_index=int(row["objective_index"]),
                lesson_objective_id=row["lesson_objective_id"],
                criterion_id=H1_CRITERIA[int(row["criterion"]) - 1].id,
                score=int(row["score"]),
                comment=_comment(row),
                document=row["document"],
            )
        )
    return scores


def part_2_judgements(
    rows: list[dict[str, str]], documents: Documents, objectives: ObjectiveNames, raters: Raters
) -> list[StudyComparativeJudgement]:
    return [
        StudyComparativeJudgement(
            artefact_a_id=part_2_note_id(row["lesson"], row["student"], row["a_was"]),
            artefact_b_id=part_2_note_id(row["lesson"], row["student"], row["b_was"]),
            rater=row["rater"],
            rater_db_id=raters[row["rater"]].id,
            delivery_order=int(row["delivery_order"]),
            packet=row["external_packet_id"],
            ability_stratum=row["ability_stratum"],
            objective_index=int(row["objective_index"]),
            lesson_objective_id=objectives.on_page(row, documents),
            criterion_id=H2_CRITERIA[int(row["criterion"]) - 1].id,
            choice=row["chose"],
            favoured_condition=row["favoured_arm"] or None,
            comment=_comment(row),
            document=row["document"],
        )
        for row in rows
    ]


def _pseudonym(student: str) -> str:
    """The allocation's ``s07`` is the ratings' ``student-07``; every comparison checks it."""
    return f"student-{student.removeprefix('s')}"


def part_2_notes(
    allocation: list[dict[str, Any]], judgements: list[dict[str, str]]
) -> dict[str, tuple[str, str]]:
    """Each Part 2 set's notes, A then B, from the allocation, which every comparison agrees with.

    The allocation names a set's two notes by internal id; which is P0 and which P1 is read by
    matching those ids, never by their order. A set returned blank has no comparison to read
    them from, so the allocation is the only record of what it held.
    """
    notes: dict[str, tuple[str, str]] = {}
    unblinded: dict[str, tuple[str, str, str, str]] = {}
    for row in allocation:
        arms = {row["internal_p0_id"]: "P0", row["internal_p1_id"]: "P1"}
        lesson, student = str(row["lesson_code"]), _pseudonym(str(row["student_id"]))
        a, b = arms[row["candidate_a_internal_id"]], arms[row["candidate_b_internal_id"]]
        packet = str(row["external_packet_id"])
        unblinded[packet] = (lesson, student, a, b)
        notes[packet] = (part_2_note_id(lesson, student, a), part_2_note_id(lesson, student, b))
    for row in judgements:
        recorded = (row["lesson"], row["student"], row["a_was"], row["b_was"])
        if unblinded.get(row["external_packet_id"]) != recorded:
            raise DatasetMismatchError(
                f"{row['external_packet_id']}: the allocation and the comparison disagree"
            )
    return notes


def rating_documents(
    index: list[dict[str, str]],
    part_1: list[dict[str, str]],
    part_2_notes: Mapping[str, tuple[str, str]],
    raters: Raters,
) -> list[StudyRatingDocument]:
    """Every returned document, answered or not, with what the rater wrote on it."""
    part_1_notes = {
        row["document"]: part_1_note_id(row["lesson"], row["condition"], int(row["draw"]))
        for row in part_1
    }
    documents = []
    for row in index:
        if row["part"] == "1":
            if row["document"] not in part_1_notes:
                raise DatasetMismatchError(f"{row['document']}: a Part 1 set with no scores")
            a, b = part_1_notes[row["document"]], None
        else:
            a, b = part_2_notes[row["external_packet_id"]]
        documents.append(
            StudyRatingDocument(
                document=row["document"],
                rater=row["rater"],
                rater_db_id=raters[row["rater"]].id,
                delivery_order=int(row["delivery_order"]),
                packet=row["external_packet_id"],
                artefact_a_id=a,
                artefact_b_id=b,
                part=int(row["part"]),
                answer_sheets=int(row["answer_sheets"]),
                marks=int(row["marks"]),
                rows_unanswered=int(row["rows_unanswered"]),
                state=row["state"],
                date_completed=row["date_completed"] or None,
                closing_comment=row["closing_comment"] or None,
            )
        )
    return documents
