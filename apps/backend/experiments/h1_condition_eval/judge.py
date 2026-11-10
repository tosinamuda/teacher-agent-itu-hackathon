"""The blinded rating pass, in code.

Every judged run so far was rated by hand-dispatched agents: one per candidate, a
prompt pasted per call, the JSON collected off disk. That works and it produced the
study's 144 judgments, but it cannot be repeated cheaply, cannot be pointed at a
bake-off, and the prompt lives in whoever ran it rather than in the repository.

This is the same pass as a function. The packet is byte-identical — it comes from
:mod:`rater_packets`, the module that built the packets the hand-dispatched judges
read — so a score from here and a score from there are comparable, and the
instructions below are the ones those judges were given, moved into the repository
where a diff can show them changing.

Two properties the design has to keep, both of them the reason the study is blinded:

- **One candidate per call.** A judge holding two packs rates them side by side and
  decides which is meant to win, which breaks the pairing the frozen analysis
  assumes. The concurrency here is over candidates, never within a call.
- **Not the generator's model.** A model marking its own homework is not a
  measurement. :func:`build_judge_lm` refuses a judge model equal to the generator's.

    uv run python -m experiments.h1_condition_eval.judge <run-label> --pass a \\
        --judge-model bedrock/converse/global.anthropic.claude-sonnet-4-6
    uv run python -m experiments.h1_condition_eval.judge <run-label> --pass b

Run it twice. The second pass is not a check on the first — it measures how far the
judge moves on prose it has already seen, which on this rubric was about 0.45. A
margin under that is not a finding, and the analysis cannot say so with one pass.

Defaults to ``JUDGE_MODEL``/``JUDGE_PROVIDER``, else the judge named in
``llm_models.ROLES``.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from typing import Any

import dspy
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from app.domains.evaluation.application.constants import H1_RUBRIC
from app.infra.dspy_lm import (
    LLM_RATE_LIMIT_RETRIES,
    LLM_REQUEST_TIMEOUT_SECONDS,
    active_model_name,
    configured_model,
    custom_endpoint,
)
from app.infra.llm_models import model_family
from experiments.h1_condition_eval.collect_judgments import DIMENSIONS, collect
from experiments.h1_condition_eval.rater_packets import build, rating_protocol

HERE = Path(__file__).parent
DEFAULT_CONCURRENCY = 12


class DimensionRating(BaseModel):
    """One rubric dimension, scored the way the collector requires it."""

    score: int = Field(ge=1, le=5)
    evidence: list[str] = Field(min_length=1, max_length=3)
    rationale: str = Field(min_length=1)


class RatePacket(dspy.Signature):
    """You are an experienced JSS1 mathematics teacher in Nigeria, asked to rate a
    take-home revision pack that a student would use alone at home.

    The packet contains: the lesson as its teacher planned it, then a revision pack
    produced for that lesson, then a rubric.

    Rate the pack on each of the four rubric dimensions, 1-5 (5 is best). For each:
    `score` is an integer 1-5; `evidence` is 1-3 short concrete observations of what
    you actually saw in the packet; `rationale` is one or two sentences.

    Judge only what is in front of you. Do not speculate about how the pack was
    produced.
    """

    packet: str = dspy.InputField(desc="The whole rating packet, as a rater receives it.")
    objective_curriculum_alignment: DimensionRating = dspy.OutputField()
    taught_lesson_alignment: DimensionRating = dspy.OutputField()
    scope_conceptual_correctness: DimensionRating = dspy.OutputField()
    clarity_usefulness: DimensionRating = dspy.OutputField()


class JudgeModelError(SystemExit):
    """A refusal to let a model mark its own homework."""


def build_judge_lm(model: str) -> dspy.LM:
    """The judge's own LM, which may not be the model that wrote the packs.

    Uncached on purpose. dspy caches to disk by default, so rating one packet twice would
    replay the first rating and report a judge that never disagrees with itself — the same
    trap that made a stochastic generator arm look perfectly reproducible across eight
    cells. Measuring what the judge does to identical prose depends on this being off.

    A judge may live behind its own endpoint — ``JUDGE_API_BASE`` and ``JUDGE_API_KEY``,
    falling back to the generator's. Bedrock mantle speaks two protocols and litellm picks
    by model prefix, not by URL:

    The base follows *model*, not the environment: one host serves both protocols at
    different paths, so ``--judge-model`` has to be able to change the path it is sent to.

    - ``anthropic/<id>`` — the native path for a Claude judge. Structured output rides
      Anthropic tool-use, which the model does natively, so the four typed
      ``DimensionRating`` fields come back as a schema rather than as prose to be parsed.
    - ``openai/<id>`` — the compatibility layer. It accepts ``response_format`` but
      Bedrock does not enforce a schema, which is exactly how the ReAct loop broke: see
      ``build_dspy_lm``.

    Prefer ``anthropic/`` for the judge. Neither needs boto3 or SigV4.
    """
    generator = active_model_name()
    if model == generator:
        raise JudgeModelError(
            f"judge model {model!r} is the generator's model. A model marking its own "
            "homework is not a measurement; every judged run in this study has used a "
            "different one on purpose."
        )
    # JUDGE_API_* when the judge lives somewhere else, the generator's otherwise — which
    # is the normal case, since one Bedrock host serves both roles and both protocols.
    endpoint = custom_endpoint("judge", model)
    if _same_model(model, generator):
        raise JudgeModelError(
            f"judge model {model!r} and generator {generator!r} are the same model under "
            "two provider ids. A model marking its own homework is not a measurement."
        )
    for role, name in (("judge", model), ("generator", generator)):
        if model_family(name) is None:
            print(
                f"  WARNING: no recorded id for the {role} {name!r}, so this run cannot "
                f"prove the judge is not the generator. Add it to judge.MODEL_IDS."
            )
    return dspy.LM(
        model=model,
        timeout=LLM_REQUEST_TIMEOUT_SECONDS,
        num_retries=LLM_RATE_LIMIT_RETRIES,
        cache=False,
        **endpoint,
    )


def _same_model(judge: str, generator: str) -> bool:
    """Whether two ids name one model. Looked up in ``llm_models``, never inferred."""
    mine, theirs = model_family(judge), model_family(generator)
    return mine is not None and mine == theirs


def _as_judgment(candidate_id: str, prediction: Any) -> dict[str, Any]:
    """The prediction in the shape ``collect_judgments`` validates and stores."""
    return {
        "candidate_id": candidate_id,
        **{d: getattr(prediction, d).model_dump() for d in DIMENSIONS},
    }


async def judge_packet(packet: dict[str, Any], *, lm: dspy.LM) -> dict[str, Any]:
    """One candidate, one call. Never two packs to one judge."""
    rater = dspy.Predict(RatePacket)
    with dspy.settings.context(lm=lm):
        prediction = await rater.acall(packet=packet["body"])
    return _as_judgment(packet["candidate_id"], prediction)


class RunNotReadyError(RuntimeError):
    """A precondition that must be checked BEFORE any judging is paid for."""


def _ready(run_label: str) -> None:
    """Refuse a run whose packets were never built.

    The de-anonymisation key is only read at collection, which is after every call has
    been made and paid for. Judging a run without it spent the whole pass and then
    raised FileNotFoundError, leaving the judgments on disk under `_judged_<pass>` with
    nothing to collect them against. Checking here costs a stat.
    """
    key = HERE / "runs" / run_label / "rating" / "_key.json"
    if not key.exists():
        raise RunNotReadyError(
            f"{run_label} has no rating/_key.json, so nothing could de-anonymise this "
            f"pass. Build the packets first:\n"
            f"    uv run python -m experiments.h1_condition_eval.rater_packets {run_label}"
        )


async def judge_run(
    run_label: str, *, lm: dspy.LM, concurrency: int = DEFAULT_CONCURRENCY
) -> list[dict[str, Any]]:
    """Every candidate of a run, judged independently and concurrently."""
    _ready(run_label)
    packets, _ = build(run_label)
    gate = asyncio.Semaphore(concurrency)

    async def one(packet: dict[str, Any]) -> dict[str, Any]:
        async with gate:
            judgment = await judge_packet(packet, lm=lm)
        print(f"  judged {packet['candidate_id']}")
        return judgment

    return list(await asyncio.gather(*(one(packet) for packet in packets)))


def _write(
    run_label: str, judgments: list[dict[str, Any]], source: Path, model: str, rating_pass: str
) -> Path:
    """Through the collector, so an in-code pass meets the same refusals as a hand one.

    Named by its pass. Every candidate is rated twice — the second pass measures the
    judge's own spread, not the first pass's correctness — and both have to survive to
    be compared. Writing them to one filename does not raise anything; it silently
    leaves the run holding pass B twice, which is indistinguishable from a judge that
    agreed with itself perfectly.
    """
    source.mkdir(parents=True, exist_ok=True)
    for judgment in judgments:
        (source / f"{judgment['candidate_id']}.json").write_text(json.dumps(judgment, indent=2))
    out = HERE / "runs" / run_label / "rating" / f"judgments_pass_{rating_pass}.json"
    if out.exists():
        raise JudgeModelError(
            f"{out.name} already exists for {run_label}. Choose another --pass, or move it "
            "aside; a rating pass is never overwritten."
        )
    out.write_text(
        json.dumps(
            {
                "judge_model": model,
                "judges_per_candidate": 1,
                "generation_draw": "every repeat",
                "protocol": rating_protocol(),
                "run": run_label,
                "judgments": collect(run_label, source),
            },
            indent=2,
        )
        + "\n"
    )
    # The collector, the trace tooling and the analysis all still look for this name.
    (out.parent / "judgments.json").write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    return out


def main() -> int:
    # Every entry point loads it for itself. litellm happens to load .env when IT is
    # imported, which made this work by luck of import order — and stopped working the
    # moment a caller reached the config without touching litellm first.
    load_dotenv(override=False)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_label")
    parser.add_argument(
        "--judge-model",
        default="",
        help="must not be the generator's model; defaults to JUDGE_MODEL/JUDGE_PROVIDER",
    )
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    parser.add_argument(
        "--pass",
        dest="rating_pass",
        default="a",
        help="which rating pass this is; names judgments_pass_<x>.json and _judged_<x>",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="where the per-candidate JSON is written before collection",
    )
    args = parser.parse_args()

    judge_model = args.judge_model or configured_model("judge")
    if not judge_model:
        raise JudgeModelError(
            "No judge model. Pass --judge-model, or set JUDGE_MODEL and JUDGE_PROVIDER."
        )
    lm = build_judge_lm(judge_model)
    judgments = asyncio.run(judge_run(args.run_label, lm=lm, concurrency=args.concurrency))
    rating = HERE / "runs" / args.run_label / "rating"
    source = args.out or rating / f"_judged_{args.rating_pass}"
    print(f"wrote {_write(args.run_label, judgments, source, judge_model, args.rating_pass)}")
    print(f"rubric dimensions: {[c['criterion_id'] for c in H1_RUBRIC]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
