"""The plan-field audit finds a leak when there is one, and none where there is none."""

from __future__ import annotations

import json

from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.source_boundary import audit, audit_step

CASES = {c["lesson"]: c for c in json.loads(EVAL_SET_PATH.read_text())["cases"]}


def _step(lesson: str, index: int):
    return SessionPlanView.model_validate(CASES[lesson]["plan"]).steps[index]


def test_the_frozen_corpus_has_no_note_sentence_in_a_plan_field() -> None:
    rows = audit()
    assert len(rows) == 17
    assert sum(r.leaks for r in rows) == 0


def test_a_note_sentence_planted_in_content_is_caught() -> None:
    step = _step("t3-w02", 1)
    assert step.note
    planted = "A polygon is a closed shape that has three or more straight sides."
    assert planted.lower() in step.note.lower()
    leaked = step.model_copy(update={"content": f"{step.content} {planted}"})
    assert audit_step("t3-w02", leaked).content_in_note == 1


def test_a_note_sentence_planted_in_an_activity_is_caught() -> None:
    step = _step("t3-w02", 1)
    planted = "A polygon is a closed shape that has three or more straight sides."
    leaked = step.model_copy(
        update={"activities": [*step.activities, {"who": "teacher", "what": planted}]}
    )
    assert audit_step("t3-w02", leaked).activities_in_note == 1


def test_a_title_standing_in_for_content_is_not_counted_as_narration() -> None:
    step = _step("t3-w02", 3)
    row = audit_step("t3-w02", step.model_copy(update={"content": step.title}))
    assert row.title_stands_in
    assert row.content_sentences == 0


def test_every_core_step_carries_her_narration_rather_than_its_title() -> None:
    assert not [r.step_id for r in audit() if r.title_stands_in]
