"""Comparing the engine's loops head to head on judged runs."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from experiments.lesson_note_engine import judging
from experiments.lesson_note_engine.compare_harnesses import (
    finishing,
    head_to_head,
    pair,
    sign_test,
)
from experiments.lesson_note_engine.judging import comparable, write_packets

#: The engine's note in slot A, the control's in B, the teacher's in C.
LABELS = {"A": "engine", "B": "current", "C": "teacher"}


def _run(folder: Path, *, notes: dict[str, str], failure: str | None = None) -> None:
    """One lesson of two steps: the engine's notes are ``notes``."""
    folder.mkdir(parents=True)
    steps = [
        {"step_id": step, "title": step, "kind": "core", "objective": "o", "activities": []}
        for step in ("s1", "s2")
    ]
    made = {
        "rounds": 4,
        "calls": 30,
        "prompt_tokens": 200_000,
        "completion_tokens": 40_000,
        "seconds": 300.0,
        "failure": failure,
    }
    lesson = {
        "plan_version_id": "LPV-1",
        "context": {"subject": "Maths", "grade": "JSS1", "topic": "t"},
        "steps": steps,
        "notes": {
            "engine": notes,
            "current": {"s1": "#### s1\nc1", "s2": "#### s2\nc2"},
            "teacher": {"s1": "t1", "s2": "t2"},
        },
        "engine_run": made,
    }
    (folder / "LPV-1.json").write_text(json.dumps(lesson))


def _judged(folder: Path, *, engine: list[int], control: list[int], placed: list[str]) -> None:
    """Verdicts of one judge: each item's engine and control mean scores, and its ranking."""
    (folder / "judging").mkdir()
    keys = {str(n): LABELS for n in range(1, len(engine) + 1)}
    (folder / "judging-keys.json").write_text(json.dumps({"1": keys}))
    items = [
        {
            "item": n,
            "scores": {
                "A": {"correctness": engine[n - 1], "fit": engine[n - 1]},
                "B": {"correctness": control[n - 1], "fit": control[n - 1]},
                "C": {"correctness": 4, "fit": 4},
            },
            "ranking": placed[n - 1],
        }
        for n in range(1, len(engine) + 1)
    ]
    (folder / "judging" / "verdict-1.json").write_text(json.dumps({"items": items}))


def test_a_draft_that_could_not_be_finished_has_no_note_to_judge(tmp_path: Path) -> None:
    _run(tmp_path / "failed", notes={"s1": "", "s2": ""}, failure="stopped")

    assert comparable(tmp_path / "failed") == []


def test_pairing_puts_the_controls_engine_notes_where_the_current_notes_were(
    tmp_path: Path,
) -> None:
    _run(tmp_path / "control", notes={"s1": "control 1", "s2": "control 2"})
    _run(tmp_path / "run", notes={"s1": "run 1", "s2": "run 2"})

    kept = pair(tmp_path / "control", tmp_path / "run", tmp_path / "run-vs-control")

    paired = json.loads((tmp_path / "run-vs-control" / "LPV-1.json").read_text())
    assert kept == ["LPV-1"]
    assert paired["notes"]["engine"] == {"s1": "run 1", "s2": "run 2"}
    assert paired["notes"]["current"] == {"s1": "control 1", "s2": "control 2"}
    assert paired["paired_with"] == "control"


def test_a_lesson_only_one_run_has_is_left_out_of_the_pairing(tmp_path: Path) -> None:
    _run(tmp_path / "control", notes={"s1": "c", "s2": "c"})
    _run(tmp_path / "run", notes={"s1": "r", "s2": "r"})
    (tmp_path / "control" / "LPV-1.json").rename(tmp_path / "control" / "LPV-9.json")

    assert pair(tmp_path / "control", tmp_path / "run", tmp_path / "paired") == []


def test_the_control_engine_notes_keep_their_heading_but_the_generators_do_not(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Only the current generator's note has a title heading the judge already has."""
    runs = tmp_path / "runs"
    _run(runs / "control", notes={"s1": "#### Explain\nc1", "s2": "#### Explain\nc2"})
    _run(runs / "run", notes={"s1": "r1", "s2": "r2"})
    pair(runs / "control", runs / "run", runs / "run-vs-control")
    monkeypatch.setattr(judging, "HERE", tmp_path)

    write_packets("run", 1, 1)
    write_packets("run-vs-control", 1, 1)

    unpaired = (runs / "run" / "judging" / "packet-1.md").read_text()
    paired = (runs / "run-vs-control" / "judging" / "packet-1.md").read_text()
    assert "#### s1" not in unpaired
    assert paired.count("#### Explain") == 2


def test_each_verdict_is_read_as_the_runs_engine_note_against_the_controls(
    tmp_path: Path,
) -> None:
    folder = tmp_path / "run-vs-control"
    _run(folder, notes={"s1": "r1", "s2": "r2"})
    _judged(folder, engine=[5, 3], control=[3, 3], placed=[["A", "C", "B"], ["C", "B", "A"]])

    result = head_to_head(folder)

    assert (result.judged, result.higher, result.lower, result.same) == (2, 1, 0, 1)
    assert (result.above, result.below) == (1, 1)
    assert (result.run_score, result.control_score) == (4.0, 3.0)
    assert (result.steps, result.steps_higher, result.steps_lower) == (2, 1, 0)
    assert (result.run_words, result.control_words) == (2, 6)


def test_a_steps_verdicts_count_once_in_the_test_by_step(tmp_path: Path) -> None:
    """Three judges who all prefer the run on one step are one step's evidence, not three."""
    folder = tmp_path / "run-vs-control"
    _run(folder, notes={"s1": "r1", "s2": "r2"})
    (folder / "judging").mkdir()
    (folder / "judging-keys.json").write_text(
        json.dumps({j: {"1": LABELS, "2": LABELS} for j in "123"})
    )
    for judge in "123":
        items = [
            {
                "item": n,
                "scores": {"A": {"c": engine}, "B": {"c": 3}, "C": {"c": 4}},
                "ranking": ["A", "C", "B"],
            }
            for n, engine in ((1, 5), (2, 2))
        ]
        (folder / "judging" / f"verdict-{judge}.json").write_text(json.dumps({"items": items}))

    result = head_to_head(folder)

    assert (result.higher, result.lower) == (3, 3)
    assert (result.steps, result.steps_higher, result.steps_lower) == (2, 1, 1)
    assert result.p_steps == 1.0


def test_what_finishing_took_is_added_up_with_its_cost_for_the_lessons_asked(
    tmp_path: Path,
) -> None:
    _run(tmp_path / "run", notes={"s1": "a", "s2": "b"}, failure="x")

    made = finishing(tmp_path / "run", {"LPV-1"})

    assert (made.lessons, made.failed, made.rounds, made.calls) == (1, 1, 4, 30)
    assert made.cost == pytest.approx(200_000 * 0.15e-6 + 40_000 * 0.60e-6)
    assert finishing(tmp_path / "run", {"LPV-9"}).lessons == 0


@pytest.mark.parametrize(
    ("higher", "lower", "p"),
    [(0, 0, 1.0), (3, 3, 1.0), (8, 0, 2 / 256), (7, 1, 18 / 256), (1, 4, 12 / 32)],
)
def test_the_sign_test_is_exact_and_two_sided(higher: int, lower: int, p: float) -> None:
    assert sign_test(higher, lower) == pytest.approx(p)
