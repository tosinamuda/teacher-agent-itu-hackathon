"""The published study's two datasets in miniature, and the curriculum an import needs."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from docx import Document
from openpyxl import Workbook
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.school.models.core import GradeLevel, Subject
from app.domains.school.models.structure import Course
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.note_editorial import CLEAN_DIR
from experiments.study_import.dataset import LESSON_PLANS, RATINGS

PART_1 = Path("experiments/h1_condition_eval/runs/c0c3-prism-objective/run.json")
PART_2 = Path("experiments/h2_personalisation_eval/runs/h2-deepseek-clean/run.json")
#: Rows in the published datasets' shape; the repository holds no rating documents.
PART_1_RATINGS = (
    "rater,delivery_order,external_packet_id,internal_packet_id,lesson,condition,draw,"
    "objective_index,lesson_objective_id,criterion,score,comment,document\n"
    "rater-2,4,h1-pkt-010,x,t3-w05,C2,3,1,lo-t3w05-01,1,4,Covers.,ratings/delivered/R2-P1-04.docx\n"
    "rater-2,4,h1-pkt-010,x,t3-w05,C2,3,1,lo-t3w05-01,3,5,,ratings/delivered/R2-P1-04.docx\n"
)
PART_2_JUDGEMENTS = (
    "rater,delivery_order,external_packet_id,internal_packet_id,lesson,student,ability_stratum,"
    "objective_index,criterion,chose,favoured_arm,a_was,b_was,comment,document\n"
    "rater-1,1,h2-pkt-004,x,t2-w09,student-01,lower,1,2,B clearly better,P1,P0,P1,"
    "Breaks the steps down.,ratings/delivered/R1-P2-01.docx\n"
)

#: A lesson's marked classwork in the release's form; the real scripts never enter the repository.
CLASSWORK = """<?xml version="1.0" encoding="utf-8"?>
<classwork lesson="t2-w09" assessed-set="step-t2w09-02:b4" set-source="step_practice_block">
  <question n="1" objective="lo-t2w09-01">
    <text>$4n + 3n \\times 10$</text>
    <answer source="teacher_correction">$34n$</answer>
  </question>
  <student id="student-06" teacher-total="0/1" capture-complete="true">
    <response n="1" mark="incorrect" uncertain="false">
      <working>$7n \\times 10 = 70n$</working>
      <misconception code="adds_before_multiplying" source="researcher">added first</misconception>
    </response>
  </student>
</classwork>
"""


#: The release's index of returned documents; the last set came back untouched.
DOCUMENTS = (
    "part,rater,delivery_order,external_packet_id,answer_sheets,marks,rows_unanswered,state,"
    "date_completed,closing_comment,document\n"
    '1,rater-2,4,h1-pkt-010,2,6,4,partial,"September 2nd, 2026.",Clear throughout.,'
    "ratings/delivered/R2-P1-04.docx\n"
    "2,rater-1,1,h2-pkt-004,1,3,2,partial,,,ratings/delivered/R1-P2-01.docx\n"
    "2,rater-4,6,h2-pkt-012,2,0,6,untouched,,,ratings/delivered/R4-P2-06.docx\n"
)
#: Which learner's notes each Part 2 set carried, as the allocation workbook records it.
ALLOCATION = (
    (
        "internal_packet_id",
        "assigned_rater",
        "lesson_id",
        "lesson_code",
        "student_id",
        "external_packet_id",
        "internal_p0_id",
        "internal_p1_id",
        "candidate_a_internal_id",
        "candidate_b_internal_id",
    ),
    (
        "h2-l01-s01-c1",
        "rater-1",
        "l01",
        "t2-w09",
        "s01",
        "h2-pkt-004",
        "h2-l01-p0",
        "h2-l01-s01-p1",
        "h2-l01-p0",
        "h2-l01-s01-p1",
    ),
    (
        "h2-l02-s07-c2",
        "rater-4",
        "l02",
        "t3-w02",
        "s07",
        "h2-pkt-012",
        "h2-l02-p0",
        "h2-l02-s07-p1",
        "h2-l02-s07-p1",
        "h2-l02-p0",
    ),
)


def _returned_document(path: Path, page: str | None, objective: str) -> None:
    """A returned rating document in the shape the study's documents have."""
    document = Document()
    if page is not None:
        document.add_paragraph(page)
        document.add_paragraph(f"Learning objective. {objective}")
    path.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(path))


def _allocation(path: Path) -> None:
    book = Workbook()
    sheet = book.active
    sheet.title = "H2_Packet_Map"
    for row in ALLOCATION:
        sheet.append(row)
    path.parent.mkdir(parents=True, exist_ok=True)
    book.save(path)


#: Each lesson's transcripts, as the release carries them: a header naming the pages, then text.
TRANSCRIPTS = {
    "t3-w05/teacher.md": (
        "---\nlesson_key: t3-w05\npages:\n"
        "  - file: lesson-plan-01.jpeg\n    role: plan_header\n"
        "  - file: lesson-plan-02.jpeg\n    role: step_i\n"
        "---\n\nObjectives: (iii) calculate capacity\n"
    ),
    "t3-w05/teacher-cleaned.md": (
        "---\nlesson_key: t3-w05\ncleaned:\n"
        "  - field: lesson_plan_objectives\n    change: dropped (iii)\n"
        "---\n\nObjectives: (i) and (ii)\n"
    ),
    "t3-w05/_cleaning-log.md": "# `t3-w05` cleaning log\n\n## 1. Objective (iii) dropped\n",
    "t3-w05/_question-set.md": "Not a transcript of a page.\n",
    "t2-w09/student-01.md": (
        "---\nstudent: student-01\nteacher_total: 1/1\nteacher_mark_date: 2026-05-21\n"
        "pages:\n  - classwork-01.jpeg\n---\n\n1. 5a + a = 6a\n"
    ),
}


def _provenance(root: Path) -> None:
    files = [
        {"path": str(p.relative_to(root)), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        for p in sorted(root.rglob("*"))
        if p.is_file()
    ]
    (root / "PROVENANCE.json").write_text(json.dumps({"files": files}))


def write_release(tmp_path: Path) -> Path:
    """The study's files as the two datasets publish them, from the repository's copies."""
    shutil.copytree(CLEAN_DIR, tmp_path / LESSON_PLANS / "notes")
    classwork = tmp_path / LESSON_PLANS / "transcripts" / "t2-w09" / "classwork.xml"
    classwork.parent.mkdir(parents=True)
    classwork.write_text(CLASSWORK, encoding="utf-8")
    for name, text in TRANSCRIPTS.items():
        path = tmp_path / LESSON_PLANS / "transcripts" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    ratings = tmp_path / RATINGS
    for source, target in (
        (EVAL_SET_PATH, "inputs/eval_set.json"),
        (PART_1, "runs/h1/c0c3-prism-objective/run.json"),
        (PART_2, "runs/h2/h2-deepseek-clean/run.json"),
    ):
        (ratings / target).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source, ratings / target)
    (ratings / "ratings").mkdir()
    (ratings / "ratings" / "part1_ratings.csv").write_text(PART_1_RATINGS)
    (ratings / "ratings" / "part2_judgements.csv").write_text(PART_2_JUDGEMENTS)
    (ratings / "ratings" / "documents.csv").write_text(DOCUMENTS)
    _allocation(ratings / "ratings/allocation/h2.xlsx")
    _returned_document(
        ratings / "ratings/delivered/R2-P1-04.docx",
        "Objective 1 of 2 — your scores",
        "identify properties of cylinders and spheres",
    )
    _returned_document(
        ratings / "ratings/delivered/R1-P2-01.docx",
        "Objective 1 of 1 — your comparison",
        "carry out order of operation in algebra",
    )
    _returned_document(ratings / "ratings/delivered/R4-P2-06.docx", None, "")
    _provenance(tmp_path / LESSON_PLANS)
    _provenance(ratings)
    return tmp_path


async def seed_curriculum(db: AsyncSession) -> None:
    grade, subject = (
        GradeLevel(name="JSS1", sequence=1),
        Subject(name="Mathematics", code="MATH", category="Science"),
    )
    db.add_all([grade, subject])
    await db.flush()
    db.add(Course(name="JSS1 Mathematics", subject_id=subject.id, grade_level_id=grade.id))
    await db.flush()
