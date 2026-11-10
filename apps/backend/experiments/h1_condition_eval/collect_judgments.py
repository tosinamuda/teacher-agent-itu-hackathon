"""Collect one judgment file per candidate into the run's ``judgments.json``.

The judges write one file each, blind, into a directory outside the run. This reads that
directory against the run's de-anonymisation key and writes the aggregate the report
loads. It had been assembled by hand every time, which is the one step in a blinded
pipeline where a mistake is invisible: a missing candidate reads as a smaller run, a
duplicated one reads as agreement, and a judgment for a candidate that is not in this run
reads as nothing at all.

So the checks are refusals, not warnings. Every candidate in the key is judged, no
candidate is judged twice, no id is unknown, every frozen rubric dimension carries a score
in range with a rationale behind it.

    uv run python -m experiments.h1_condition_eval.collect_judgments <run-label> <dir> \
        --judge-model "claude-sonnet (fixed; deliberately not the generator's model)"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from app.domains.evaluation.application.constants import H1_RUBRIC
from experiments.h1_condition_eval.rater_packets import rating_protocol

HERE = Path(__file__).parent
DIMENSIONS = tuple(str(c["criterion_id"]) for c in H1_RUBRIC)
SCORE_RANGE = range(1, 6)


class JudgmentError(SystemExit):
    """A refusal to write an aggregate that would misreport the run."""


def _read(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        raise JudgmentError(f"{path.name}: not JSON — {error}") from error
    if not isinstance(loaded, dict):
        raise JudgmentError(
            f"{path.name}: expected one judgment object, got {type(loaded).__name__}"
        )
    return loaded


def _check_shape(path: Path, judgment: dict[str, Any]) -> None:
    """Every frozen dimension, scored in range, with a rationale behind it."""
    if not judgment.get("candidate_id"):
        raise JudgmentError(f"{path.name}: no candidate_id, so it cannot be placed")
    for dimension in DIMENSIONS:
        entry = judgment.get(dimension)
        if not isinstance(entry, dict):
            raise JudgmentError(f"{path.name}: no {dimension} — the rubric is frozen")
        if entry.get("score") not in SCORE_RANGE:
            raise JudgmentError(f"{path.name}: {dimension} scored {entry.get('score')!r}, not 1-5")
        if not str(entry.get("rationale") or "").strip():
            raise JudgmentError(f"{path.name}: {dimension} has a score and no rationale")
        if not isinstance(entry.get("evidence", []), list):
            raise JudgmentError(f"{path.name}: {dimension} evidence is not a list")


def _check_coverage(judgments: list[dict[str, Any]], key: list[dict[str, Any]]) -> None:
    """The run's candidates and the judged candidates are the same set, one to one."""
    expected = {row["candidate_id"] for row in key}
    seen: dict[str, int] = {}
    for judgment in judgments:
        seen[judgment["candidate_id"]] = seen.get(judgment["candidate_id"], 0) + 1
    if unknown := sorted(set(seen) - expected):
        raise JudgmentError(f"judged candidates this run never produced: {unknown}")
    if repeated := sorted(cid for cid, count in seen.items() if count > 1):
        raise JudgmentError(f"judged more than once, which would read as agreement: {repeated}")
    if missing := sorted(expected - set(seen)):
        raise JudgmentError(f"{len(missing)} of {len(expected)} candidates unjudged: {missing}")


def collect(run_label: str, source: Path) -> list[dict[str, Any]]:
    """Every judgment in ``source``, checked against the run it claims to judge."""
    rating = HERE / "runs" / run_label / "rating"
    key = json.loads((rating / "_key.json").read_text())
    files = sorted(source.glob("*.json"))
    if not files:
        raise JudgmentError(f"no judgment files in {source}")
    judgments = []
    for path in files:
        judgment = _read(path)
        _check_shape(path, judgment)
        judgments.append(judgment)
    _check_coverage(judgments, key)
    order = {row["candidate_id"]: index for index, row in enumerate(key)}
    return sorted(judgments, key=lambda j: order[j["candidate_id"]])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_label")
    parser.add_argument("source", type=Path, help="directory of one JSON judgment per candidate")
    parser.add_argument("--judge-model", required=True, help="who judged, recorded in the report")
    parser.add_argument("--judges-per-candidate", type=int, default=1)
    parser.add_argument(
        "--pass",
        dest="rating_pass",
        default="",
        help="name this pass, writing judgments_pass_<x>.json beside judgments.json",
    )
    parser.add_argument(
        "--generation-draw",
        default="every repeat",
        help="which draws were judged, recorded in the report",
    )
    args = parser.parse_args()

    judgments = collect(args.run_label, args.source)
    rating = HERE / "runs" / args.run_label / "rating"
    named = f"judgments_pass_{args.rating_pass}.json" if args.rating_pass else "judgments.json"
    out = rating / named
    out.write_text(
        json.dumps(
            {
                "judge_model": args.judge_model,
                "judges_per_candidate": args.judges_per_candidate,
                "generation_draw": args.generation_draw,
                "protocol": rating_protocol(),
                "run": args.run_label,
                "judgments": judgments,
            },
            indent=2,
        )
        + "\n"
    )
    if args.rating_pass:
        # Same as judge.py: the collector, the trace tooling and the analysis all still
        # look for judgments.json, and a named pass is what survives a second one.
        (rating / "judgments.json").write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"collected {len(judgments)} judgments -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
