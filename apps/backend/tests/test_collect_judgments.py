"""The step where a blinded pipeline's mistakes are invisible.

``judgments.json`` had been assembled by hand from the judges' output files. Every way
that goes wrong reads as a smaller, or more agreeable, or differently-shaped run rather
than as an error: a dropped candidate looks like a run that judged fewer, a duplicate
looks like two judges agreeing, an id from another run looks like nothing at all. So the
collector refuses rather than reports, and this is the suite that says so.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from experiments.h1_condition_eval import collect_judgments
from experiments.h1_condition_eval.collect_judgments import (
    DIMENSIONS,
    JudgmentError,
    collect,
)

RUN = "test-run"
CANDIDATES = ("cand-aaaa", "cand-bbbb")


def _judgment(candidate_id: str, score: int = 4) -> dict:
    return {
        "candidate_id": candidate_id,
        **{
            dimension: {"score": score, "evidence": ["the pack says so"], "rationale": "because"}
            for dimension in DIMENSIONS
        },
    }


@pytest.fixture
def run(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A run with two candidates in its key, and an empty directory to judge into."""
    monkeypatch.setattr(collect_judgments, "HERE", tmp_path)
    rating = tmp_path / "runs" / RUN / "rating"
    rating.mkdir(parents=True)
    (rating / "_key.json").write_text(
        json.dumps(
            [
                {"candidate_id": cid, "lesson": "t3-w02", "condition": code, "repeat": 1}
                for cid, code in zip(CANDIDATES, ("C0", "C1"), strict=True)
            ]
        )
    )
    judged = tmp_path / "judged"
    judged.mkdir()
    return judged


def _write(judged: Path, judgment: dict, name: str | None = None) -> None:
    (judged / f"{name or judgment['candidate_id']}.json").write_text(json.dumps(judgment))


def test_a_complete_pass_collects_in_key_order(run: Path) -> None:
    """Read order is the filesystem's; report order is the key's."""
    _write(run, _judgment(CANDIDATES[1]))
    _write(run, _judgment(CANDIDATES[0]))
    assert [j["candidate_id"] for j in collect(RUN, run)] == list(CANDIDATES)


def test_an_unjudged_candidate_is_refused(run: Path) -> None:
    """The failure mode with no symptom: the report just describes a smaller run."""
    _write(run, _judgment(CANDIDATES[0]))
    with pytest.raises(JudgmentError, match="1 of 2 candidates unjudged"):
        collect(RUN, run)


def test_a_candidate_judged_twice_is_refused(run: Path) -> None:
    """Two files for one candidate average into what looks like judges agreeing."""
    _write(run, _judgment(CANDIDATES[0]))
    _write(run, _judgment(CANDIDATES[1]))
    _write(run, _judgment(CANDIDATES[1]), name="second-look")
    with pytest.raises(JudgmentError, match="judged more than once"):
        collect(RUN, run)


def test_a_candidate_from_another_run_is_refused(run: Path) -> None:
    """Candidate ids are per-run hashes, so a stale one silently judges nothing."""
    _write(run, _judgment(CANDIDATES[0]))
    _write(run, _judgment(CANDIDATES[1]))
    _write(run, _judgment("cand-ffff"))
    with pytest.raises(JudgmentError, match="this run never produced"):
        collect(RUN, run)


def test_a_missing_dimension_is_refused(run: Path) -> None:
    """The rubric is frozen; a judgment short a dimension is not a judgment."""
    short = _judgment(CANDIDATES[0])
    del short[DIMENSIONS[-1]]
    _write(run, short)
    _write(run, _judgment(CANDIDATES[1]))
    with pytest.raises(JudgmentError, match=f"no {DIMENSIONS[-1]}"):
        collect(RUN, run)


@pytest.mark.parametrize("score", [0, 6, "4", None])
def test_a_score_outside_the_scale_is_refused(run: Path, score: object) -> None:
    """1-5 is the scale the human raters use; anything else silently skews a mean."""
    off = _judgment(CANDIDATES[0])
    off[DIMENSIONS[0]]["score"] = score
    _write(run, off)
    _write(run, _judgment(CANDIDATES[1]))
    with pytest.raises(JudgmentError, match="not 1-5"):
        collect(RUN, run)


def test_a_score_with_no_rationale_is_refused(run: Path) -> None:
    """The report prints the rationale as the evidence for the score."""
    silent = _judgment(CANDIDATES[0])
    silent[DIMENSIONS[0]]["rationale"] = "  "
    _write(run, silent)
    _write(run, _judgment(CANDIDATES[1]))
    with pytest.raises(JudgmentError, match="score and no rationale"):
        collect(RUN, run)


def test_an_empty_directory_is_refused(run: Path) -> None:
    """Otherwise it writes an empty aggregate and the report divides by zero."""
    with pytest.raises(JudgmentError, match="no judgment files"):
        collect(RUN, run)
