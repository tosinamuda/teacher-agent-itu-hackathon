"""The field classwork, read from the canonical XML in the thesis dataset.

The XML lives beside the transcriptions it projects, in the dataset repository —
never here. It holds identifiable work by minors, so this module reads it at
runtime from the researcher's machine. What a run derives from it is pseudonymous and
versioned by DVC.
"""

from __future__ import annotations

from dataclasses import dataclass

from lxml import etree

from experiments.h1_condition_eval.dataset import THESIS

TRANSCRIPTS = THESIS / "Dataset/private/study-record/transcripts"
GRAMMAR = THESIS / "Dataset/private/study-record/classwork.rng"

#: The lessons with transcribed, marked scripts. `t3-w05` joined on 2026-08-25 when its nine
#: scripts were transcribed — they sit in the students' week-4 notebooks and assess volume, so
#: they belong to this lesson and not to `t3-w04`. `t3-w06` has nine transcribed scripts too and
#: is deliberately absent: its construction test is scored out of five an item rather than right
#: or wrong, which this module's response model cannot carry honestly. See that lesson's
#: `_question-set.md`.
LESSONS = ("t2-w09", "t3-w02", "t3-w05")


@dataclass(frozen=True)
class Question:
    n: int
    objective: str
    text: str
    answer: str | None
    answer_source: str | None


@dataclass(frozen=True)
class Response:
    n: int
    mark: str  # correct | incorrect | unmarked
    uncertain: bool
    working: str
    misconception_code: str | None
    misconception_why: str | None


@dataclass(frozen=True)
class StudentScript:
    id: str
    teacher_total: str
    capture_complete: bool
    responses: tuple[Response, ...]


@dataclass(frozen=True)
class Classwork:
    lesson: str
    assessed_set: str
    questions: dict[int, Question]
    students: tuple[StudentScript, ...]


def load(lesson: str) -> Classwork:
    """One lesson's classwork, grammar-validated before anything reads it."""
    path = TRANSCRIPTS / lesson / "classwork.xml"
    if not path.exists():
        raise SystemExit(
            f"{path} is missing. It lives in the thesis dataset repository, not here — "
            "regenerate it there with build_classwork.py."
        )
    tree = etree.parse(str(path))
    grammar = etree.RelaxNG(etree.parse(str(GRAMMAR)))
    if not grammar.validate(tree):
        raise SystemExit(f"{path} fails its own grammar: {list(grammar.error_log)[:3]}")
    return parse(tree.getroot(), lesson)


def _number(element: etree._Element) -> int:
    """A question's or response's ``n``, which every one of them carries."""
    n = element.get("n")
    if n is None:
        raise ValueError(f"<{element.tag}> has no n")
    return int(n)


def parse(root: etree._Element, lesson: str) -> Classwork:
    """One lesson's classwork from its XML, read as written."""
    questions = {}
    for q in root.findall("question"):
        answer = q.find("answer")
        questions[_number(q)] = Question(
            n=_number(q),
            objective=str(q.get("objective")),
            text=str(q.findtext("text") or "").strip(),
            answer=answer.text.strip() if answer is not None and answer.text else None,
            answer_source=answer.get("source") if answer is not None else None,
        )

    students = []
    for s in root.findall("student"):
        responses = []
        for r in s.findall("response"):
            coded = r.find("misconception")
            responses.append(
                Response(
                    n=_number(r),
                    mark=str(r.get("mark")),
                    uncertain=r.get("uncertain") == "true",
                    working=str(r.findtext("working") or "").strip(),
                    misconception_code=coded.get("code") if coded is not None else None,
                    misconception_why=(
                        coded.text.strip() if coded is not None and coded.text else None
                    ),
                )
            )
        students.append(
            StudentScript(
                id=str(s.get("id")),
                teacher_total=str(s.get("teacher-total")),
                capture_complete=s.get("capture-complete") == "true",
                responses=tuple(responses),
            )
        )
    return Classwork(
        lesson=lesson,
        assessed_set=str(root.get("assessed-set")),
        questions=questions,
        students=tuple(students),
    )
