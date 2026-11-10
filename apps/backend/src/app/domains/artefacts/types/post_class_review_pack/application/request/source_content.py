"""Normalise teacher-authored lesson content before request projection."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any, cast

from app.domains.artefacts.types.lesson_plan.drafting.domain.instructional_events import (
    event_of,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.instructional_events import (
    instructional_events as _instructional_events,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.note_figures import figures_in_text

instructional_events = _instructional_events

REVIEW_MARKUP = re.compile(r"<!--.*?-->|<aside\b[^>]*>.*?</aside>", re.DOTALL)
_DRAWN_NODE = re.compile(r"node\b(?!\s/)[^;{]*\{((?:[^{}]|\{[^{}]*\})*)\}")
_LATEX_NOISE = re.compile(
    r"\\(?:text|mathrm|textbf|small|large|quad|qquad|hspace)\b|\\[,;:!]|[$\\{}]"
)
_TIKZ_SOURCE = re.compile(
    r"(?:\\begin\{center\}\s*)?\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}"
    r"(?:\s*\\end\{center\})?",
    re.DOTALL,
)


def without_review_markup(note: str) -> str:
    """Remove transcription commentary without altering authored prose."""
    return re.sub(r"[ \t]+\n", "\n", REVIEW_MARKUP.sub("", note))


def drawn_labels(tikz: str) -> list[str]:
    """Return the reader-visible labels carried by a TikZ drawing."""
    seen: list[str] = []
    for body in _DRAWN_NODE.findall(tikz):
        label = " ".join(_LATEX_NOISE.sub(" ", body).split())
        if not label or re.fullmatch(r"[\d.,\s\-+()]+", label) or len(label) > 40:
            continue
        if label not in seen:
            seen.append(label)
    return seen


def drawings_as_references(note: str, step_id: str) -> str:
    """Replace TikZ source with labelled references while preserving its labels."""
    refs = iter(figure.get("figure_ref") for figure in figures_in_text(note, step_id))

    def reference(match: re.Match[str]) -> str:
        figure_ref = next(refs, None)
        name = f"as {figure_ref}" if figure_ref else "here, unlabelled"
        written = drawn_labels(match.group(0))
        marked = f", marked {', '.join(written)}" if written else ""
        return f"[drawing attached to this section {name}{marked}]"

    return _TIKZ_SOURCE.sub(reference, note)


def question_as_asked(question: str, *, keep_drawing: bool = False) -> str:
    """Her question as its reader meets it, with the drawing removed or carried.

    Removed by default, and that default is for READERS. A rater's sheet and a
    learner's pack render practice text as markdown, so TikZ source placed there
    is source code on the page — which happened, nine commands deep, on this
    lesson's reference sheet.

    ``keep_drawing`` is for the MODEL, which reads TikZ perfectly well and cannot
    answer without it. The label summary the removal leaves behind is not a
    weaker version of the picture: on t3-w02 item 8 it keeps 1cm, 5cm and 9cm and
    drops both the semicircular arc and the second 1cm, so the only answer those
    three numbers support is 15 against a true 32. A question whose figure cannot
    travel is unanswerable, and it should look unanswerable rather than tidy.
    """

    def replace(match: re.Match[str]) -> str:
        if keep_drawing:
            return f"\n{match.group(0)}\n"
        written = drawn_labels(match.group(0))
        marked = f", marked {', '.join(written)}" if written else ""
        return f"[the figure is not included here{marked}]"

    carried = _TIKZ_SOURCE.sub(replace, question)
    if keep_drawing and carried != question:
        return carried.strip()
    return re.sub(r"\s*\n+\s*", " ", carried).strip()


def block_text(block: Mapping[str, Any]) -> str:
    """Collect all prose-bearing fields from a lesson-plan block."""
    parts = [
        str(block.get(key) or "") for key in ("content", "problem", "question", "final_answer")
    ]
    steps = block.get("steps")
    if isinstance(steps, list):
        parts.extend(str(entry.get("content") or "") for entry in steps if isinstance(entry, dict))
    return "\n\n".join(part.strip() for part in parts if part and part.strip())


#: The Gagne event that means the learner performs. It is the study's own instrument,
#: already reviewed, and it draws exactly the line this needs: "listen", "contribute",
#: "take notes" and "ask questions" are reception and take no code at all.
_WORK_SET = "elicit_performance"


def work_the_step_sets(activities: Sequence[object]) -> list[str]:
    """The tasks a step sets, read from the Student Activity column.

    Narrowly, and for one reason: some of what she sets has no question text. A
    practice block holds "Simplify 4n + 3n x 10"; a construction lesson holds
    "construct angle 90 degrees" in the activity column and nothing in a block, so a
    reader of practice blocks alone concludes she set no work.

    This is not the raw activity narration, which no condition receives. A TEACHER
    activity describes the lesson as an event -- "the teacher explains the drawing" --
    and is what that exclusion is for; it never travels here. A student activity coded
    as performance is the work itself, the same content class as the question text
    beside it, and it is the only slice of the column that crosses.
    """
    return [
        question_as_asked(what)
        for activity in activities
        if _who(activity) == "student" and _sets_work(activity)
        if (what := _what(activity).strip())
    ]


def _sets_work(activity: object) -> bool:
    """Read if she has been read; coded if she has not.

    ``sets_work`` is a verdict somebody reached by reading the activity against its
    step. Where it is present it wins outright, because the alternative is a regex
    deciding a study input — and on the frozen cohort the two disagree once, on
    "identify their properties", which codes as performance and is oral answering
    inside the teacher's exposition.

    Absent, the Gagne coder decides: a teacher's plan entered without the verdict, or a
    drafted activity the drafter left undeclared.
    """
    declared = _field(activity, "sets_work")
    if declared is not None:
        return bool(declared)
    return event_of(activity) == _WORK_SET


def _field(activity: object, name: str) -> object:
    """An activity's field, whether it arrives as a mapping or as a model."""
    if isinstance(activity, Mapping):
        return cast(Mapping[str, object], activity).get(name)
    return getattr(activity, name, None)


def _who(activity: object) -> str:
    return str(_field(activity, "who") or "").strip().lower()


def _what(activity: object) -> str:
    return str(_field(activity, "what") or "")
