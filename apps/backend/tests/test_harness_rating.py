"""Rating the bake-off measures the judge before it ranks anything.

The screen the bake-off runs could not separate any candidate: recall moved further between
draws of one harness than the whole table spread. Replacing it with rubric scores only helps
if the rubric carries its own margin — which means rating each pack twice and knowing what
the judge does to prose that did not change.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict

import pytest

from experiments.h1_condition_eval.bakeoff_judge import restore
from experiments.h1_condition_eval.collect_judgments import DIMENSIONS
from experiments.h1_condition_eval.generator_arms import harness_for
from experiments.h1_condition_eval.harness_rating import (
    PASSES,
    Rated,
    artefact,
    blinded_id,
    draw_floor,
    harnesses,
    judge_floor,
    pack_movements,
    plans,
    rate,
    summarise,
)
from experiments.h1_condition_eval.selection_set import LESSONS


def _rated(candidate: str, lesson: str, draw: int, first: float, second: float) -> Rated:
    return Rated(
        candidate=candidate,
        lesson=lesson,
        draw=draw,
        packet_id=f"cand-{candidate}{draw}",
        passes=(
            dict.fromkeys(DIMENSIONS, first),
            dict.fromkeys(DIMENSIONS, second),
        ),
    )


def _cell(candidate: str, lesson: str, draw: int) -> dict:
    return {
        "candidate": candidate,
        "lesson": lesson,
        "draw": draw,
        "dud": False,
        "sections": [{"section_id": "s1", "title": "T", "blocks": [], "practice": []}],
    }


def test_the_judge_floor_is_what_it_did_to_a_whole_row() -> None:
    """`one` averages 3.5 then 4.0 over its two packs; `two` moves the full 2.0."""
    rated = [
        _rated("one", "sel-rich", 1, 4.0, 4.0),
        _rated("one", "sel-rich", 2, 3.0, 4.0),
        _rated("two", "sel-rich", 1, 2.0, 4.0),
    ]

    assert judge_floor(rated) == pytest.approx(2.0)


def test_one_wild_cell_does_not_set_the_floor_for_a_whole_row() -> None:
    """The regression the first judged report shipped with.

    Measured per cell, one lesson of one arm moved 2.12 between its draws and that was held
    against differences between twelve-pack means — a floor no table could ever clear. The
    row is what the table ranks, so the row is what the floor is measured on. Here one
    lesson swings the full 3.0 and the row it belongs to moves a quarter of that.
    """
    steady = [
        _rated("one", lesson, draw, 3.0, 3.0)
        for lesson in ("sel-rich", "sel-noprac", "sel-drawn")
        for draw in (1, 2, 3)
    ]
    wild = [
        _rated("one", "sel-noeval", 1, 1.5, 1.5),
        _rated("one", "sel-noeval", 2, 4.5, 4.5),
        _rated("one", "sel-noeval", 3, 3.0, 3.0),
    ]

    assert max(item.mean() for item in wild) - min(item.mean() for item in wild) == 3.0
    assert draw_floor(steady + wild) == pytest.approx(0.75)


def test_the_draw_floor_is_what_one_harness_did_to_its_own_row() -> None:
    """One arm's row averaged 3.5 on its first draw and 4.5 on its second."""
    rated = [_rated("one", "sel-rich", 1, 3.0, 4.0), _rated("one", "sel-rich", 2, 4.0, 5.0)]

    assert draw_floor(rated) == pytest.approx(1.0)


def test_a_single_draw_has_no_draw_floor_to_report() -> None:
    assert draw_floor([_rated("one", "sel-rich", 1, 3.0, 4.0)]) == 0.0


def test_a_candidates_score_averages_every_pack_and_every_pass() -> None:
    summary = summarise(
        [_rated("one", "sel-rich", 1, 2.0, 4.0), _rated("one", "sel-noeval", 1, 3.0, 3.0)]
    )

    assert summary["one"]["packs"] == 2
    assert summary["one"]["rubric_mean"] == pytest.approx(3.0)


def test_the_packet_id_hides_which_arm_wrote_the_pack() -> None:
    first = blinded_id("run.json", _cell("deepagents", "sel-rich", 1))
    same = blinded_id("run.json", _cell("deepagents", "sel-rich", 1))
    other = blinded_id("run.json", _cell("compose-v2", "sel-rich", 1))

    assert first == same
    assert first != other
    assert "deepagents" not in first


def test_an_artefact_whose_arms_declare_no_harness_is_refused() -> None:
    """Resolving it at rating time would credit the packs to today's installed versions."""
    with pytest.raises(ValueError, match="records no harness"):
        harnesses({"cells": [_cell("langgraph", "sel-rich", 1)]})


def test_an_artefact_that_records_its_harness_round_trips() -> None:
    loaded = {
        "cells": [_cell("langgraph", "sel-rich", 1)],
        "arms": {"langgraph": {"harness": harness_for("langgraph").recorded()}},
    }

    assert harnesses(loaded)["langgraph"]["framework"] == "langgraph"


def test_a_report_is_not_a_set_of_packs(tmp_path) -> None:
    report = tmp_path / "HARNESS-BAKEOFF-2026-01-01.json"
    report.write_text(json.dumps({"summary": "not cells"}))

    with pytest.raises(ValueError, match="no bake-off cells"):
        artefact(report)


def test_the_frozen_selection_set_still_matches_the_lessons_it_was_built_from() -> None:
    """A pack rated against a drifted plan reads back as a bad harness, not a stale file."""
    assert set(plans()) == set(LESSONS)


def test_every_pack_is_rated_by_two_separate_calls(monkeypatch) -> None:
    """One call reused would report a judge that never disagrees with itself."""
    calls: list[str] = []

    async def fake_judge(packet, *, lm):
        """Score by how many times THIS packet has been seen, so every pack moves by one."""
        calls.append(packet["candidate_id"])
        seen = calls.count(packet["candidate_id"])
        return {
            dimension: {"score": 3 + seen % 2, "evidence": ["x"], "rationale": "y"}
            for dimension in DIMENSIONS
        }

    monkeypatch.setattr("experiments.h1_condition_eval.harness_rating.judge_packet", fake_judge)
    loaded = {"cells": [_cell("langgraph", lesson, 1) for lesson in LESSONS]}

    rated = asyncio.run(rate(loaded, source="packs.json", lm=None, concurrency=2))

    assert len(calls) == len(LESSONS) * PASSES
    assert all(len(item.passes) == PASSES for item in rated)
    assert pack_movements(rated) == [1.0] * len(LESSONS)


def test_a_dud_cell_is_not_rated(monkeypatch) -> None:
    async def fake_judge(packet, *, lm):
        raise AssertionError("a dud has no pack to rate")

    monkeypatch.setattr("experiments.h1_condition_eval.harness_rating.judge_packet", fake_judge)
    dud = {**_cell("adk", "sel-rich", 1), "dud": True, "sections": []}

    assert asyncio.run(rate({"cells": [dud]}, source="p.json", lm=None, concurrency=1)) == []


def test_a_written_pass_re_reports_without_rating_again(tmp_path) -> None:
    """Changing how a floor is computed must not cost another two hundred judge calls."""
    written = tmp_path / "HARNESS-JUDGED-2026-01-01.json"
    written.write_text(
        json.dumps(
            {
                "judge_model": "a-judge",
                "rated": [asdict(_rated("one", "sel-rich", 1, 3.0, 4.0))],
            }
        )
    )

    restored, judge_model = restore(written)

    assert judge_model == "a-judge"
    assert restored == [_rated("one", "sel-rich", 1, 3.0, 4.0)]
