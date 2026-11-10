"""The blinded-rating report has to read every draw of a cell, not the last one.

``_scores`` keyed judgments by ``(lesson, condition)`` alone. The design generates three
repeats per cell, so judging all three and reporting them through this would have kept
whichever judgment happened to be read last and printed it as the cell's score — a run
judged on three draws would look exactly like a run judged on one, with no error and
nothing in the output to say so.
"""

from __future__ import annotations

import pytest

from experiments.h1_condition_eval.rating_report import (
    DIMENSIONS,
    _conditions,
    _endpoint,
    _how_much_moves_anyway,
    _ladder,
    _margin,
    _mean,
    _scores,
)


def _judgment(score: int) -> dict:
    return {d: {"score": score, "evidence": ["e"], "rationale": "r"} for d in DIMENSIONS}


def _fixture(scores: dict[tuple[str, int], int]) -> tuple[dict, dict]:
    """`scores` maps (condition, repeat) -> the score on every dimension."""
    key = {
        f"cand-{condition}{repeat}": {
            "candidate_id": f"cand-{condition}{repeat}",
            "lesson": "t3-w02",
            "condition": condition,
            "repeat": repeat,
        }
        for condition, repeat in scores
    }
    judged = {f"cand-{c}{r}": _judgment(score) for (c, r), score in scores.items()}
    return key, judged


def test_every_draw_of_a_cell_is_kept() -> None:
    key, judged = _fixture({("C0", 1): 2, ("C0", 2): 4, ("C0", 3): 3})
    by = _scores(judged, key)
    assert [j[DIMENSIONS[0]]["score"] for j in by[("t3-w02", "C0")]] == [2, 4, 3]


def test_draws_are_ordered_by_repeat_not_by_read_order() -> None:
    """The evidence section prints them as "draw 1/2/3"; the label has to be true."""
    key, judged = _fixture({("C0", 3): 3, ("C0", 1): 1, ("C0", 2): 2})
    by = _scores(judged, key)
    assert [j[DIMENSIONS[0]]["score"] for j in by[("t3-w02", "C0")]] == [1, 2, 3]


def test_a_cell_scores_as_the_mean_of_its_draws() -> None:
    key, judged = _fixture({("C0", 1): 2, ("C0", 2): 4, ("C0", 3): 3})
    assert _mean(_scores(judged, key), "t3-w02", "C0", DIMENSIONS[0]) == pytest.approx(3.0)


def test_the_margin_is_taken_between_the_two_means() -> None:
    """Not between two single draws — that is the noise the extra draws exist to average."""
    key, judged = _fixture(
        {("C0", 1): 2, ("C0", 2): 2, ("C0", 3): 2, ("C1", 1): 5, ("C1", 2): 3, ("C1", 3): 4}
    )
    assert _margin(_scores(judged, key), "t3-w02", DIMENSIONS[0]) == pytest.approx(2.0)


def test_a_single_draw_run_still_reports() -> None:
    """The two runs judged before this change have to keep reporting their own numbers."""
    key, judged = _fixture({("C0", 1): 3, ("C1", 1): 4})
    by = _scores(judged, key)
    assert len(by[("t3-w02", "C0")]) == 1
    assert _margin(by, "t3-w02", DIMENSIONS[0]) == pytest.approx(1.0)


def test_the_arms_are_read_off_the_run_in_ladder_order() -> None:
    """A four-condition run reports four arms, and reports them C0 first.

    The report named C0 and C1 in nine places. A run that also drew C2 and C3
    would have printed a two-arm report of a four-arm run and said nothing about
    the two it dropped.
    """
    key, judged = _fixture({("C3", 1): 5, ("C0", 1): 2, ("C2", 1): 4, ("C1", 1): 3})
    assert _conditions(_scores(judged, key)) == ["C0", "C1", "C2", "C3"]


def test_the_endpoint_is_still_c1_against_c0_when_the_run_has_four_arms() -> None:
    """H1a was frozen on one comparison; drawing more arms does not re-open it."""
    key, judged = _fixture({("C0", 1): 2, ("C1", 1): 3, ("C2", 1): 5, ("C3", 1): 5})
    by = _scores(judged, key)
    endpoint = "\n".join(_endpoint(by, ["t3-w02"]))
    assert "C1 against C0" in endpoint
    assert "2.00 -> 3.00 (+1.00)" in endpoint
    assert "C2" not in endpoint and "C3" not in endpoint


def test_the_rest_of_the_ladder_is_reported_beside_the_endpoint_not_instead() -> None:
    key, judged = _fixture({("C0", 1): 2, ("C1", 1): 3, ("C2", 1): 4, ("C3", 1): 5})
    by = _scores(judged, key)
    ladder = "\n".join(_ladder(by, ["t3-w02"], _conditions(by)))
    assert "| C2 | 4.00 (+2.00)" in ladder
    assert "| C3 | 5.00 (+3.00)" in ladder
    # The control has no margin over itself to state.
    assert "| C0 | 2.00 |" in ladder


def test_a_two_arm_run_reports_no_ladder_section() -> None:
    """With only C0 and C1 the endpoint IS the whole ladder; a second table repeats it."""
    key, judged = _fixture({("C0", 1): 2, ("C1", 1): 3})
    by = _scores(judged, key)
    assert _ladder(by, ["t3-w02"], _conditions(by)) == []


def test_movement_is_measured_only_on_arms_both_runs_drew() -> None:
    """The earlier run has no C2 to have moved from, and asking for one is a KeyError."""
    key, judged = _fixture({("C0", 1): 2, ("C1", 1): 3, ("C2", 1): 4})
    baseline_key, baseline_judged = _fixture({("C0", 1): 2, ("C1", 1): 4})
    moved = "\n".join(
        _how_much_moves_anyway(
            _scores(judged, key), _scores(baseline_judged, baseline_key), ["t3-w02"]
        )
    )
    assert "| C0 |" in moved and "| C1 |" in moved
    assert "| C2 |" not in moved


def test_a_rating_names_the_notes_its_generation_read(tmp_path):
    """A judged number must say which notes produced the packs it judged.

    Both judged runs of 2026-08-11 were generated from the uncorrected transcription.
    The setting was recorded — as a SHA-256 in ``fingerprint.json``, which is unreadable
    by design — and no report, summary or filename said so, so the study's headline
    number sat on raw notes for nine days without anyone seeing it.
    """
    from experiments.h1_condition_eval.rating_report import HERE, _notes_line

    if not (HERE / "runs" / "clean-six" / "run.json").exists():
        pytest.skip("clean-six is versioned by DVC; run `dvc pull` first")
    line = _notes_line("clean-six")
    assert "CLEAN" in line
    assert "hand-corrected and research-enhanced" in line

    # A run whose run.json predates the arm block must SAY it does not know, and point
    # at the only place that still holds the answer.
    bare = HERE / "runs" / "_probe_no_arm"
    bare.mkdir(parents=True, exist_ok=True)
    try:
        (bare / "run.json").write_text('{"label": "_probe_no_arm", "plans": {}, "cases": []}')
        missing = _notes_line("_probe_no_arm")
        assert "NOT RECORDED" in missing
        assert "fingerprint.json" in missing
    finally:
        (bare / "run.json").unlink(missing_ok=True)
        bare.rmdir()


def test_the_two_note_sources_are_described_as_what_they_are():
    """ "clean" understates it, and the flag cannot be renamed without breaking every
    recorded fingerprint. So the word stays and the meaning travels beside it."""
    from experiments.h1_condition_eval.note_editorial import describe_note_source

    assert "UNCORRECTED" in describe_note_source("raw")
    assert "research-enhanced" in describe_note_source("clean")
    assert "UNKNOWN" in describe_note_source("something-else")
