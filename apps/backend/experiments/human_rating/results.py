"""Every rating of these artefacts, from both instruments, joined to the key.

The answer sheets are the record: a rater types into the .docx in Google Docs and there
is no database behind it. This reads the delivered folder, pairs every mark with the
internal id it was blind to, and writes one workbook the analysis can open.

The same packs were scored by an LLM judge, twice, and were produced under a generation
record that says whether each condition's components ran and whether validation closed.
Both are read from the run folder into the same workbook, because a reader comparing the
two instruments should not have to join two files to do it.

An answer sheet is found by two headings, not one. Three tables on a page begin with
"Criterion" — the sheet, the criteria reference and the worked example — and two carry
the comparison columns. Only the sheet carries both, and keying on either alone has
already counted a neighbour.

Run with::

    uv run python -m experiments.human_rating.results "<delivered folder>" ratings.xlsx
"""

from __future__ import annotations

import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import openpyxl

from app.domains.evaluation.domain.study_instrument import COMPARISON

from . import mapping, reference, sources

JUDGE_DIMENSIONS = (
    "objective_curriculum_alignment",
    "taught_lesson_alignment",
    "scope_conceptual_correctness",
    "clarity_usefulness",
)

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
DOCUMENT = re.compile(
    r"^R(?P<rater>\d)-P(?P<part>\d)-(?P<order>\d+) (?P<external>h\d-pkt-\d+)\.docx$"
)
SCORE = re.compile(r"^\s*([1-5])\s*$")
SCORED_COLUMN = re.compile(r" score \(1–5\)$")
#: The heading of the box on a set's last page where the rater may comment on the whole set.
CLOSING_BOX = "Your comments on this set"
DATE_COMPLETED = re.compile(r"^Date completed:(.*)$")


@dataclass(frozen=True)
class Answer:
    """One mark, before it is joined to anything."""

    objective: int
    """Which answer sheet in the document, counting from one."""
    criterion: int
    column: str
    """The score column's material, or the comparison point that was chosen."""
    value: str
    comment: str


def _cell(cell) -> str:
    return "".join(t.text or "" for t in cell.iter(f"{W}t")).strip()


def answers(path: Path) -> tuple[list[Answer], int, int]:
    """Every mark in one document, with how many sheets it had and how many are unanswered."""
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    found: list[Answer] = []
    sheets = unanswered = 0
    for table in root.iter(f"{W}tbl"):
        rows = [[_cell(c) for c in r.findall(f"{W}tc")] for r in table.findall(f"{W}tr")]
        if not rows or not rows[0] or rows[0][0] != "Criterion":
            continue
        header = rows[0]
        comparative = COMPARISON[0] in header
        if not comparative and not any(SCORED_COLUMN.search(h) for h in header):
            continue
        sheets += 1
        # A rater who presses Tab in the last cell adds a row to the table in Google
        # Docs. One such row exists across the 144 Part 1 documents, entirely blank, and
        # counting it as unanswered reported a rating missing that was never asked for.
        body = [row for row in rows[1:] if row and row[0].strip()]
        for criterion, row in enumerate(body, start=1):
            marked = False
            for offset, raw in enumerate(row[1:-1]):
                column = header[1 + offset]
                if comparative and raw.strip():
                    found.append(Answer(sheets, criterion, column, raw.strip(), row[-1]))
                    marked = True
                elif not comparative and (m := SCORE.match(raw)):
                    label = SCORED_COLUMN.sub("", column)
                    found.append(Answer(sheets, criterion, label, m.group(1), row[-1]))
                    marked = True
            unanswered += not marked
    return found, sheets, unanswered


def _objective_ids(lesson: str, plans: dict[str, Any]) -> list[str]:
    return [objective_id for objective_id, _ in reference.objectives(plans[lesson])]


def h1_rows(folder: Path, plans: dict[str, Any]) -> list[dict[str, Any]]:
    """Every Part 1 score, against the condition and draw the rater could not see."""
    key = {(a.rater, a.external_id): a for a in mapping.load_h1()}
    out = []
    for path in sorted(folder.glob("Part 1*/Rater */*.docx")):
        match = DOCUMENT.match(path.name)
        if not match:
            continue
        assignment = key[(f"rater-{match['rater']}", match["external"])]
        ids = _objective_ids(assignment.lesson, plans)
        for answer in answers(path)[0]:
            out.append(
                {
                    "rater": assignment.rater,
                    "delivery_order": assignment.order,
                    "external_packet_id": assignment.external_id,
                    "internal_packet_id": assignment.internal_id,
                    "lesson": assignment.lesson,
                    "condition": assignment.condition,
                    "draw": assignment.version,
                    "objective_index": answer.objective,
                    "lesson_objective_id": (
                        ids[answer.objective - 1] if answer.objective <= len(ids) else ""
                    ),
                    "criterion": answer.criterion,
                    "score": int(answer.value),
                    "comment": answer.comment,
                }
            )
    return out


def h2_rows(folder: Path) -> list[dict[str, Any]]:
    """Every Part 2 comparison, with the chosen side resolved to the arm it was."""
    key = {(a.rater, a.external_id): a for a in mapping.load_h2()}
    stratum = {row["student"]: row["ability_stratum"] for row in students()}
    out = []
    for path in sorted(folder.glob("Part 2*/Rater */*.docx")):
        match = DOCUMENT.match(path.name)
        if not match:
            continue
        assignment = key[(f"rater-{match['rater']}", match["external"])]
        for answer in answers(path)[0]:
            side = next((s for s in "AB" if answer.column.startswith(f"{s} ")), "")
            out.append(
                {
                    "rater": assignment.rater,
                    "delivery_order": assignment.order,
                    "external_packet_id": assignment.external_id,
                    "internal_packet_id": assignment.internal_id,
                    "lesson": assignment.lesson,
                    "student": assignment.student,
                    "ability_stratum": stratum.get(assignment.student, ""),
                    "objective_index": answer.objective,
                    "criterion": answer.criterion,
                    "chose": answer.column,
                    "favoured_arm": {"A": assignment.a, "B": assignment.b}.get(side, "neither"),
                    "a_was": assignment.a,
                    "b_was": assignment.b,
                    "comment": answer.comment,
                }
            )
    return out


def judge(run: str) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    """The run's de-anonymisation key, and each judging pass by candidate id."""
    folder = sources.H1_RUNS / run / "rating"
    key = {row["candidate_id"]: row for row in json.loads((folder / "_key.json").read_text())}
    passes = {}
    for name in ("judgments_pass_a.json", "judgments_pass_b.json"):
        record = json.loads((folder / name).read_text())
        passes[name[-6]] = {j["candidate_id"]: j for j in record["judgments"]}
    return key, passes


def judge_rows(run: str) -> list[dict[str, Any]]:
    """One row per candidate, pass and dimension, with the reason the judge gave."""
    key, passes = judge(run)
    out = []
    for letter, judged in sorted(passes.items()):
        for candidate, record in judged.items():
            meta = key[candidate]
            for dimension in JUDGE_DIMENSIONS:
                scored = record[dimension]
                out.append(
                    {
                        "candidate_id": candidate,
                        "lesson": meta["lesson"],
                        "condition": meta["condition"],
                        "draw": int(meta["repeat"]),
                        "pass": letter,
                        "dimension": dimension,
                        "score": scored["score"],
                        "evidence": " | ".join(scored.get("evidence") or []),
                    }
                )
    return out


#: What the run recorded about producing each pack. ``passed`` and ``failed_checks`` are
#: the validation rung's own verdict on itself and exist only where validation ran.
GENERATION_FIELDS = (
    "lesson",
    "condition",
    "repeat",
    "units",
    "blocks",
    "blocks_with_source_refs",
    "evidence_items",
    "evidence_chars",
    "chars",
    "recall",
    "validated",
    "passed",
    "findings",
    "repaired",
    "repair_rounds",
    "failed_checks",
)


def generation_rows(run: str) -> list[dict[str, Any]]:
    """Whether each condition's components ran, and whether validation closed."""
    record = json.loads((sources.H1_RUNS / run / "run.json").read_text())
    return [{field: case.get(field) for field in GENERATION_FIELDS} for case in record["cases"]]


#: The nine were drawn at random from three ability categories in a class of forty. The
#: category itself was never written down, but the teacher's own totals were, so the
#: grouping is recovered from the record rather than from anyone's memory of the draw.
STRATA = ("top", "middle", "lower")
MARK = re.compile(r"(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)")


def _share(total: Any) -> float | None:
    """A teacher's mark, written "6/8", as the share of the paper they got right."""
    found = MARK.search(str(total or ""))
    return float(found.group(1)) / float(found.group(2)) if found else None


def students(lessons: tuple[str, ...] = ("t2-w09", "t3-w02", "t3-w05")) -> list[dict[str, Any]]:
    """Each student, what the teacher marked them across the lessons, and their third.

    Ranked on the mean share rather than a raw total: the three papers are out of four,
    eight and six, so totals are not comparable and a sum would weight the longest paper
    heaviest.
    """
    from experiments.h2_personalisation_eval.students import load

    marked: dict[str, dict[str, Any]] = {}
    for lesson in lessons:
        for script in load(lesson).students:
            marked.setdefault(script.id, {})[lesson] = script.teacher_total
    rows = []
    for student, totals in marked.items():
        shares = [v for v in (_share(t) for t in totals.values()) if v is not None]
        rows.append(
            {
                "student": student,
                **{lesson: totals.get(lesson) for lesson in lessons},
                "mean_share_correct": round(sum(shares) / len(shares), 3) if shares else None,
                "lessons_sat": len(shares),
            }
        )
    rows.sort(key=lambda r: r["mean_share_correct"] or 0, reverse=True)
    for rank, row in enumerate(rows):
        row["ability_rank"] = rank + 1
        row["ability_stratum"] = STRATA[min(rank * len(STRATA) // len(rows), len(STRATA) - 1)]
    return rows


def coverage(folder: Path) -> list[dict[str, Any]]:
    """One row per document: how much of it is answered, when, and the rater's closing comment."""
    out = []
    for path in sorted(folder.glob("Part */Rater */*.docx")):
        match = DOCUMENT.match(path.name)
        if not match:
            continue
        marks, sheets, unanswered = answers(path)
        date, comment = written_on(path)
        out.append(
            {
                "part": int(match["part"]),
                "rater": f"rater-{match['rater']}",
                "delivery_order": int(match["order"]),
                "external_packet_id": match["external"],
                "answer_sheets": sheets,
                "marks": len(marks),
                "rows_unanswered": unanswered,
                "state": _state(len(marks), unanswered),
                "date_completed": date,
                "closing_comment": comment,
            }
        )
    return out


def _paragraphs(element: ET.Element) -> list[str]:
    return ["".join(t.text or "" for t in p.iter(f"{W}t")) for p in element.iter(f"{W}p")]


def written_on(path: Path) -> tuple[str, str]:
    """The date the rater wrote on the set, and their closing comment; each empty if none.

    Neither is tied to an objective, so neither is in a scoring table: the closing comment is
    on the set's last page, the date on its cover.
    """
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    date = next(
        (
            m.group(1).strip().strip("_").strip()
            for text in _paragraphs(root)
            if (m := DATE_COMPLETED.match(text))
        ),
        "",
    )
    comment = ""
    for table in root.iter(f"{W}tbl"):
        rows = table.findall(f"{W}tr")
        cells = rows[0].findall(f"{W}tc") if rows else []
        if cells and _cell(cells[0]).startswith(CLOSING_BOX):
            comment = "\n".join(text for row in rows[1:] for text in _paragraphs(row)).strip()
    return date, comment


def _state(marks: int, unanswered: int) -> str:
    if not marks:
        return "untouched"
    return "complete" if not unanswered else "partial"


def _sheet(book, title: str, rows: list[dict[str, Any]]) -> None:
    page = book.create_sheet(title)
    if not rows:
        page.append([f"no {title.lower()} yet"])
        return
    page.append(list(rows[0]))
    for row in rows:
        page.append(list(row.values()))
    page.freeze_panes = "A2"
    for index, name in enumerate(rows[0], start=1):
        width = max(len(name), *(len(str(r[name])) for r in rows))
        page.column_dimensions[page.cell(1, index).column_letter].width = min(width + 2, 60)


def workbook(folder: Path, out: Path, run: str = "c0c3-prism-objective") -> Path:
    """The de-anonymised record: every mark, every comment, and what is still outstanding."""
    plans = sources.plans()
    book = openpyxl.Workbook()
    book.remove(book.active)
    _sheet(book, "H1 scores", h1_rows(folder, plans))
    _sheet(book, "H2 comparisons", h2_rows(folder))
    _sheet(book, "Students", students())
    _sheet(book, "Judge scores", judge_rows(run))
    _sheet(book, "Generation record", generation_rows(run))
    _sheet(book, "Coverage", coverage(folder))
    out.parent.mkdir(parents=True, exist_ok=True)
    book.save(out)
    return out


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    written = workbook(Path(sys.argv[1]), Path(sys.argv[2]))
    print(f"wrote {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
