"""Write the delivery audit as a pack a researcher can print and mark up.

Joins :mod:`step_delivery` to the WeasyPrint renderer. One combined PDF for the
whole cohort, and one per lesson so a single lesson can be carried to its source
pages on its own.

    uv run python -m scripts.prompt_snapshots.delivery_pack
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from app.domains.evaluation.application.worksheet_html.delivery_renderer import (
    render_delivery_audit_pdf,
)
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from scripts.prompt_snapshots.cohort_audit import MANIPULATION_KEYS
from scripts.prompt_snapshots.note_tasks import DISPOSITION_MEANING
from scripts.prompt_snapshots.step_delivery import LessonDelivery, StepDelivery, cohort_delivery

OUT_DIR = EVAL_SET_PATH.parent / "delivery-audit"
KEY_HEADS = tuple(key.split(".")[-1].replace("_", " ") for key in MANIPULATION_KEYS)

#: Emphasis and inline-math delimiters are the transcription's, not hers. This page
#: is read beside her handwriting, so stripping them brings the printed line closer
#: to the page it is being checked against. Nothing else about the text is touched.
_MARKUP = re.compile(r"\*\*|\$")
#: The only LaTeX commands that reach this page — counted across the cohort, not
#: guessed at. A command outside this map is left as written rather than mangled.
_SYMBOLS = {r"^\circ": "\u00b0", r"\circ": "\u00b0", r"\angle ": "\u2220"}
_LATEX = re.compile("|".join(re.escape(command) for command in _SYMBOLS))
_CONTEXT_CHARS = 150


def _plain(text: str) -> str:
    """Her line as it reads on paper: markers gone, her own line breaks kept."""
    written = _LATEX.sub(lambda match: _SYMBOLS[match.group()], _MARKUP.sub("", text))
    return re.sub(r"[ \t]+", " ", written).strip()


def _context(text: str) -> str:
    """The paragraph that decides a line, short enough to sit under it."""
    single = " ".join(_plain(text).split())
    return single if len(single) <= _CONTEXT_CHARS else single[:_CONTEXT_CHARS].rstrip() + "\u2026"


def _step_detail(step: StepDelivery) -> dict[str, Any]:
    return {
        "position": step.position,
        "step_id": step.step_id,
        "title": _plain(step.title),
        "objective_id": step.objective_id,
        "objective_text": _plain(step.objective_text),
        "marks": [{"present": key in step.delivered} for key in MANIPULATION_KEYS],
        "missing": [{"short": miss.short, "reason": miss.reason} for miss in step.missing],
        "tasks": [
            {
                "line": _plain(task.line),
                "followed_by": _context(task.followed_by),
                "meaning": DISPOSITION_MEANING[task.disposition],
            }
            for task in step.tasks
        ],
    }


def _lesson_detail(lesson: LessonDelivery) -> dict[str, Any]:
    return {
        "lesson": lesson.lesson,
        "topic": lesson.topic,
        "subtopic": lesson.subtopic,
        "term": lesson.term,
        "week": lesson.week,
        "calls": len(lesson.steps),
        "evaluation_steps": lesson.evaluation_steps,
        "steps": [_step_detail(step) for step in lesson.steps],
    }


def _summary(cohort: list[LessonDelivery]) -> dict[str, Any]:
    total = sum(len(lesson.steps) for lesson in cohort)
    rows = []
    for key, short in zip(MANIPULATION_KEYS, KEY_HEADS, strict=True):
        carried = [lesson.carried(key) for lesson in cohort]
        got = sum(carried)
        rows.append(
            {
                "short": short,
                "cells": [
                    f"{count}/{len(lesson.steps)}"
                    for count, lesson in zip(carried, cohort, strict=True)
                ],
                "cohort": f"{got}/{total} ({got / total:.0%})",
            }
        )
    return {"lessons": [lesson.lesson for lesson in cohort], "rows": rows}


def detail(cohort: list[LessonDelivery], *, with_summary: bool) -> dict[str, Any]:
    """The mapping the renderer takes, for one lesson or for the whole cohort."""
    return {
        "pack_code": "delivery-audit",
        "key_heads": list(KEY_HEADS),
        "summary": _summary(cohort) if with_summary else None,
        "lessons": [_lesson_detail(lesson) for lesson in cohort],
    }


def write_pack(out_dir: Path) -> list[Path]:
    """The combined pack, then one per lesson. Returns what was written."""
    cohort = cohort_delivery()
    out_dir.mkdir(parents=True, exist_ok=True)
    written = [out_dir / "DELIVERY-AUDIT.pdf"]
    written[0].write_bytes(render_delivery_audit_pdf(detail(cohort, with_summary=True)))
    for lesson in cohort:
        path = out_dir / f"delivery-{lesson.lesson}.pdf"
        path.write_bytes(render_delivery_audit_pdf(detail([lesson], with_summary=False)))
        written.append(path)
    return written


def main() -> int:
    for path in write_pack(OUT_DIR):
        print(f"wrote {path.relative_to(EVAL_SET_PATH.parents[2])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
