"""A generated cell reaches disk when it is made, and is never redone or mixed.

The grid used to hold all 72 cells in memory until the last one finished, so a run
stopped at hour one lost hour one. A cell is a lesson, a condition and a draw — the
unit the analysis is built from, and so the unit to save and resume from.
"""

from __future__ import annotations

import json

import pytest

from experiments.h1_condition_eval.cell_store import read_cell, write_cell

ARM = {"model": "openai/deepseek-v4-flash", "generator": "compose-v2", "context_variant": "v7-full"}
ROWS = [{"lesson": "t3-w05", "condition": "C1", "repeat": 1, "chars": 4148}]


@pytest.fixture
def path(tmp_path):
    return tmp_path / "cells" / "t3-w05.C1.r1.json"


def test_a_saved_cell_comes_back_unchanged(path) -> None:
    write_cell(path, ARM, ROWS)
    assert read_cell(path, ARM) == ROWS


def test_a_cell_never_generated_is_not_resumed(path) -> None:
    assert read_cell(path, ARM) is None


def test_a_cell_from_another_arm_is_refused(path) -> None:
    write_cell(path, {**ARM, "model": "openai/openai.gpt-oss-120b"}, ROWS)
    with pytest.raises(SystemExit, match="different arm"):
        read_cell(path, ARM)


def test_a_cell_from_another_context_variant_is_refused(path) -> None:
    write_cell(path, {**ARM, "context_variant": "v3"}, ROWS)
    with pytest.raises(SystemExit, match="different arm"):
        read_cell(path, ARM)


def test_the_arm_is_stored_beside_the_rows(path) -> None:
    write_cell(path, ARM, ROWS)
    assert json.loads(path.read_text())["arm"] == ARM


def test_a_save_leaves_no_partial_file_behind(path) -> None:
    write_cell(path, ARM, ROWS)
    assert [p.name for p in path.parent.iterdir()] == [path.name]


def test_a_redraw_replaces_the_cell(path) -> None:
    write_cell(path, ARM, ROWS)
    redrawn = [{**ROWS[0], "chars": 5408}]
    write_cell(path, ARM, redrawn)
    assert read_cell(path, ARM) == redrawn


def test_a_dud_draw_saves_as_no_rows(path) -> None:
    # `run_case` returns [] on AdapterParseError. That is a result — the cell was drawn
    # and produced nothing — so it must resume as [] rather than as "never run".
    write_cell(path, ARM, [])
    assert read_cell(path, ARM) == []
