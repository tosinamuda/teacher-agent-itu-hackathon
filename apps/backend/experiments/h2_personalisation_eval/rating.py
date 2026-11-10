"""Blinded rating of P0 and P1 packs, one learner at a time.

The packet shows the lesson as the teacher planned it, a profile of ONE learner
assembled from their marked classwork, and one candidate pack. Nothing names the
condition: P0 (the base pack unchanged) and P1 (personalised) read identically, and
the judge rates each against the same learner profile — which is the point, since
the H2 question is whether personalisation fits the pack to the learner better than
the base pack already did.

The lesson reference is imported from the H1 packet builder so both hypotheses show
a rater the identical rendering of her plan. Everything written here lands in the
run's own directory, which DVC versions: the packets embed learner evidence.

    uv run python -m experiments.h2_personalisation_eval.rating h2-deepseek-native --pass a
    uv run python -m experiments.h2_personalisation_eval.rating h2-deepseek-native --pass b
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from typing import Any

import dspy
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from app.domains.evaluation.application.constants import H2_RUBRIC
from app.domains.evaluation.application.lesson_reference import lesson_reference
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.judge import (
    DEFAULT_CONCURRENCY,
    DimensionRating,
    JudgeModelError,
    build_judge_lm,
)
from experiments.h1_condition_eval.rater_packets import _candidate, _plan_reference, _reader_ready

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"

DIMENSIONS = tuple(str(c["criterion_id"]) for c in H2_RUBRIC)


class OptionalDimensionRating(BaseModel):
    """A dimension that may not apply — misconception support with none recorded."""

    applicable: bool
    score: int = Field(ge=1, le=5)
    evidence: list[str] = Field(min_length=1, max_length=3)
    rationale: str = Field(min_length=1)


class RatePersonalisedPacket(dspy.Signature):
    """You are an experienced JSS1 mathematics teacher in Nigeria. A learner sat a
    marked classwork after the lesson below, and a revision pack was then prepared
    for them to use alone at home. The packet contains: the lesson as its teacher
    planned it, a profile of the learner built only from their marked classwork,
    and the revision pack.

    Rate the pack FOR THIS LEARNER on each rubric dimension, 1-5 (5 is best). For
    each: `score` is an integer 1-5; `evidence` is 1-3 short concrete observations
    from the packet; `rationale` is one or two sentences.

    For misconception_support only: judge how well the pack addresses the
    misconception RECORDED in the learner profile — the line reading "Recorded
    misconception". If the profile records none, set `applicable` to false and
    score 3; the analysis discards inapplicable scores. Do not infer misconceptions
    of your own. Judge only what is in front of you; do not speculate about how the
    pack was produced.
    """

    packet: str = dspy.InputField(desc="The whole rating packet, as a rater receives it.")
    learner_state_suitability: DimensionRating = dspy.OutputField()
    scaffolding_appropriateness: DimensionRating = dspy.OutputField()
    challenge_calibration: DimensionRating = dspy.OutputField()
    misconception_support: OptionalDimensionRating = dspy.OutputField()
    objective_preservation: DimensionRating = dspy.OutputField()


def _candidate_id(label: str, lesson: str, student: str, condition: str) -> str:
    seed = f"{label}|{lesson}|{student}|{condition}"
    return "cand-" + hashlib.sha256(seed.encode()).hexdigest()[:8]


def _learner_profile(states: dict[str, Any], plan: dict[str, Any]) -> list[str]:
    """The learner as the rater meets them: counts, band, and their own working."""
    titles = {o["lesson_objective_id"]: o["objective_text"] for o in plan["lesson_plan_objectives"]}
    lines = ["\n## The learner, from their marked classwork\n"]
    lines.append(
        "Assembled from the teacher's marking of this learner's classwork. Objectives "
        "not listed here carry no evidence for this learner.\n"
    )
    for objective_id, state in states.items():
        lines.append(f"**{titles.get(objective_id, objective_id)}** — {state['mastery']}; ")
        lines.append(f"personalisation band: **{state['mastery_band']}**.")
        if state.get("misconception"):
            lines.append(f"Recorded misconception: **{state['misconception']}**.")
        lines.append("")
        for item in state.get("evidence_items") or []:
            lines.append(f"- Question: {item['question']}")
            if item.get("correct_option"):
                lines.append(f"  - Expected answer: {item['correct_option']}")
            lines.append(f"  - The learner wrote: {item['student_choice']}")
            if item.get("chosen_option_misconception"):
                lines.append(
                    f"  - Recorded misconception for this response: "
                    f"{item['chosen_option_misconception']}"
                )
        lines.append("")
    return lines


def _rubric() -> list[str]:
    lines = ["\n## How to rate it\n"]
    lines.append("Score each dimension 1-5 (5 is best), for THIS learner:\n")
    for criterion in H2_RUBRIC:
        lines.append(f"- **{criterion['label']}** — {criterion['description']}")
    return lines


def build(run_label: str) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    run = json.loads((RUNS / run_label / "run.json").read_text())
    plans = {c["lesson"]: c["plan"] for c in json.loads(EVAL_SET_PATH.read_text())["cases"]}
    packets, key = [], []
    for case in run["cases"]:
        cid = _candidate_id(run_label, case["lesson"], case["student"], case["condition"])
        plan = plans[case["lesson"]]
        reference = lesson_reference(SessionPlanView.model_validate(plan))
        body = "\n".join(
            [
                f"# Rating packet {cid}\n",
                "A revision pack was prepared for one learner after the lesson below.",
                "Judge the pack for that learner, using the rubric at the end. Nothing",
                "here tells you how the pack was produced.\n",
            ]
            + _plan_reference(reference)
            + _learner_profile(case["learner_states"], plan)
            + _candidate(_reader_ready(case["sections"]))
            + _rubric()
        )
        packets.append({"candidate_id": cid, "body": body})
        key.append(
            {
                "candidate_id": cid,
                "lesson": case["lesson"],
                "student": case["student"],
                "condition": case["condition"],
            }
        )
    return packets, key


def _as_judgment(cid: str, prediction: Any) -> dict[str, Any]:
    out: dict[str, Any] = {"candidate_id": cid}
    for dim in DIMENSIONS:
        rating = getattr(prediction, dim)
        out[dim] = rating.model_dump()
    return out


async def judge_run(run_label: str, *, lm: dspy.LM, concurrency: int) -> list[dict[str, Any]]:
    packets, _ = build(run_label)
    rater = dspy.Predict(RatePersonalisedPacket)
    gate = asyncio.Semaphore(concurrency)

    async def one(packet: dict[str, Any]) -> dict[str, Any]:
        async with gate:
            with dspy.settings.context(lm=lm):
                prediction = await rater.acall(packet=packet["body"])
        print(f"  judged {packet['candidate_id']}")
        return _as_judgment(packet["candidate_id"], prediction)

    return list(await asyncio.gather(*(one(packet) for packet in packets)))


def _write(run_label: str, judgments: list[dict[str, Any]], model: str, rating_pass: str) -> Path:
    _, key = build(run_label)
    known = {row["candidate_id"] for row in key}
    seen = {j["candidate_id"] for j in judgments}
    if seen != known:
        raise JudgeModelError(f"judged {len(seen)} of {len(known)} candidates; refusing to write")
    rating = RUNS / run_label / "rating"
    rating.mkdir(parents=True, exist_ok=True)
    key_path = rating / "_key.json"
    key_path.write_text(json.dumps(key, indent=2) + "\n")
    out = rating / f"judgments_pass_{rating_pass}.json"
    if out.exists():
        raise JudgeModelError(f"{out.name} exists; a rating pass is never overwritten")
    out.write_text(
        json.dumps(
            {"judge_model": model, "run": run_label, "judgments": judgments},
            indent=2,
        )
        + "\n"
    )
    return out


def main() -> int:
    load_dotenv(override=False)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_label")
    parser.add_argument(
        "--judge-model", default="bedrock/converse/global.anthropic.claude-sonnet-4-6"
    )
    parser.add_argument("--pass", dest="rating_pass", required=True)
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    args = parser.parse_args()
    lm = build_judge_lm(args.judge_model)
    judgments = asyncio.run(judge_run(args.run_label, lm=lm, concurrency=args.concurrency))
    print(f"wrote {_write(args.run_label, judgments, args.judge_model, args.rating_pass)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
