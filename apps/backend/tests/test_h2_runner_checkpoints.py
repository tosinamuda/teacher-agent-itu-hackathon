"""A learner's work reaches disk when it is made, and is never redone or mixed.

Nothing used to be written until all 26 learners were finished, so a run stopped at
eleven lost eleven learners of paid calls. These pin the three properties that fixes:
saved on completion, reused on resume, and refused when the checkpoint belongs to a
different arm.
"""

from __future__ import annotations

import json

import pytest

from experiments.h2_personalisation_eval.runner import (
    BASE_CONDITION,
    BASE_REPEAT,
    BASE_RUN,
    _checkpoint,
    _resume,
    _save,
)

MODEL = "openai/deepseek-v4-flash"
ROWS = [{"condition": "P0", "student": "student-01"}, {"condition": "P1", "student": "student-01"}]


@pytest.fixture
def path(tmp_path, monkeypatch):
    monkeypatch.setattr("experiments.h2_personalisation_eval.runner.RUNS", tmp_path)
    return _checkpoint("a-run", "t3-w05", "student-01")


def test_a_saved_learner_comes_back_unchanged(path) -> None:
    _save(path, MODEL, ROWS)
    assert _resume(path, MODEL) == ROWS


def test_a_learner_never_generated_is_not_resumed(path) -> None:
    assert _resume(path, MODEL) is None


def test_the_file_is_named_for_its_learner(path) -> None:
    assert path.name == "t3-w05.student-01.json"


def test_a_checkpoint_from_another_model_is_refused(path) -> None:
    _save(path, "openai/openai.gpt-oss-120b", ROWS)
    with pytest.raises(SystemExit, match="different arm"):
        _resume(path, MODEL)


def test_a_checkpoint_from_another_base_pack_is_refused(path) -> None:
    _save(path, MODEL, ROWS)
    saved = json.loads(path.read_text())
    saved["base"] = {"run": "some-older-run", "condition": BASE_CONDITION, "repeat": BASE_REPEAT}
    path.write_text(json.dumps(saved))
    with pytest.raises(SystemExit, match="different arm"):
        _resume(path, MODEL)


def test_the_current_base_is_what_a_fresh_save_records(path) -> None:
    _save(path, MODEL, ROWS)
    assert json.loads(path.read_text())["base"] == {
        "run": BASE_RUN,
        "condition": BASE_CONDITION,
        "repeat": BASE_REPEAT,
    }


def test_a_save_leaves_no_partial_file_behind(path) -> None:
    _save(path, MODEL, ROWS)
    assert [p.name for p in path.parent.iterdir()] == [path.name]


def test_a_second_save_replaces_the_first(path) -> None:
    _save(path, MODEL, ROWS)
    _save(path, MODEL, [{"condition": "P1", "student": "student-01", "redrawn": True}])
    assert _resume(path, MODEL) == [{"condition": "P1", "student": "student-01", "redrawn": True}]
