"""Generate the packs a harness is chosen on, off the frozen eval set.

Every candidate runs the same lessons, the same condition and the same rendering path, so
the harness is the only thing varying. The lessons are the held-out selection set, never
the six H1a is measured on.

This pass generates and screens. Recall against the lesson note is a dud screen and a
floor check: re-running one harness on unchanged data moves it by a median of 0.094, and
the candidates have moved it by more than they differ, so it has never separated anything.
The packs are kept, and `bakeoff_judge` rates those same packs on the study's H1 rubric —
which is the comparison.

    uv run python -m experiments.h1_condition_eval.bakeoff --repeats 3
    uv run python -m experiments.h1_condition_eval.bakeoff_judge HARNESS-BAKEOFF-<date>.json \
        --judge-model bedrock/converse/global.anthropic.claude-sonnet-4-6
"""

from __future__ import annotations

import argparse
import asyncio
import json
import statistics
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from dspy.utils.exceptions import AdapterParseError

from app.domains.artefacts.types.post_class_review_pack.application.generate_base import (
    GenerateBaseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.application.revision.finalise_pack import (
    FinaliseReviewPack,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.critique_sections import (  # noqa: E501
    CritiqueSections,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.repair_section import (
    RepairGeneratedSection,
)
from app.domains.experiments.review_pack_study.conditions.profiles import H1_CONDITION_PROFILES
from app.infra.dspy_lm import build_dspy_lm, set_sampling_override
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.generator_arms import GENERATOR_ARMS, harness_for
from experiments.h1_condition_eval.metrics import score
from experiments.h1_condition_eval.selection_set import (
    LESSONS,
    SCREENING_CONDITION,
    SELECTION_SET_PATH,
)

RECALL_FLOOR = 0.094
"""Median movement of recall when one harness is re-run on unchanged data. A lead smaller
than this is a redraw."""

CANDIDATES = (
    "packed",
    "compose",
    "compose-v2",
    "compose-read",
    "agentic",
    "agentic2",
    "langgraph",
    "adk",
    "deepagents",
)
"""Every harness in use that can run a grounded condition: six dspy programs and the three
frameworks that drive the same composition tools through their own loop. The workspace
readers are excluded: they need materialised note files, which is a dataset shape rather
than a harness (HARNESS-001A found they occupy the same point in the dimension)."""

CELL_CONCURRENCY = 4
"""Cells in flight at once. Nine candidates over four lessons at three draws is 108 packs,
and a cell is minutes of agent loop; run sequentially the screen takes longer than the
runs it screens. Held low because the shared upstream pool 429s with `Retry-After: 59`."""


@dataclass(frozen=True)
class Cell:
    """One candidate on one lesson, one draw."""

    candidate: str
    lesson: str
    draw: int
    recall: float
    invention: float
    section_count: int
    dud: bool
    sections: list[dict[str, Any]] = field(default_factory=list)
    """The pack itself. Kept so the judged pass reads the same artefact this one scored,
    rather than regenerating and rating a different draw."""


def _notes() -> dict[str, str]:
    return {
        key: "\n\n".join(step["note"] for step in plan["steps"] if step.get("note"))
        for key, plan in LESSONS.items()
    }


async def _one(candidate: str, lesson: str, plan_dict: dict, draw: int, notes: str) -> Cell:
    plan = SessionPlanView.model_validate(plan_dict)
    profile = H1_CONDITION_PROFILES[SCREENING_CONDITION]
    arm = GENERATOR_ARMS[candidate]
    section_generator = arm.build(
        profile=profile,
        case={"lesson": lesson, "plan": plan_dict},
        workspace_root=Path("/tmp/bakeoff-unused"),
        signatures="leveled",
    )
    lm = build_dspy_lm()
    generator = GenerateBaseReviewPack(
        generator=section_generator,
        request_builder=BaseReviewPackRequestBuilder(figures="source"),
        # C2 runs no validation, so the critic and repairer are wired but never reached.
        # They are still supplied: a candidate that could not be constructed the way the
        # runner constructs it would not be the same harness.
        finalise=FinaliseReviewPack(
            generator=section_generator,
            repairer=RepairGeneratedSection(lm=lm),
            critic=CritiqueSections(lm=lm),
            reviser=None,
        ),
    )
    try:
        result = await generator.generate(
            session_plan=plan,
            policy=profile.generation_policy(),
            sources=LessonSources.unresolved(plan.references),
        )
    except (AdapterParseError, ValueError) as error:
        print(f"  {candidate:14s} {lesson:12s} draw {draw}  DUD: {type(error).__name__}")
        return Cell(candidate, lesson, draw, 0.0, 0.0, 0, dud=True)

    sections = [section.model_dump(mode="json") for section in result.sections]
    measured = score(notes, sections)
    cell = Cell(
        candidate=candidate,
        lesson=lesson,
        draw=draw,
        recall=float(measured["recall"]),
        invention=float(measured["invention"]),
        section_count=len(sections),
        dud=False,
        sections=sections,
    )
    print(
        f"  {candidate:14s} {lesson:12s} draw {draw}  "
        f"recall={cell.recall:.3f}  invention={cell.invention:.3f}  "
        f"sections={cell.section_count}"
    )
    return cell


async def bake(candidates: tuple[str, ...], repeats: int, temperature: float) -> list[Cell]:
    # dspy caches LM responses to disk by default, so repeated draws replay the first one
    # and every candidate looks perfectly stable. A first pass of this bake-off returned
    # ONE recall value across three draws on 23 of 24 candidate-lesson pairs.
    set_sampling_override(cache=False, temperature=temperature)
    notes = _notes()
    gate = asyncio.Semaphore(CELL_CONCURRENCY)

    async def one(candidate: str, lesson: str, plan: dict, draw: int) -> Cell:
        async with gate:
            return await _one(candidate, lesson, plan, draw, notes[lesson])

    return list(
        await asyncio.gather(
            *(
                one(candidate, lesson, plan, draw)
                for candidate in candidates
                for draw in range(1, repeats + 1)
                for lesson, plan in LESSONS.items()
            )
        )
    )


def observed_floor(cells: list[Cell]) -> float:
    """The largest spread one candidate showed on one lesson across its own draws.

    Measured here rather than imported: a between-candidate gap only means something beside
    the movement these candidates showed when nothing but the draw changed.
    """
    spreads = []
    seen = {(cell.candidate, cell.lesson) for cell in cells if not cell.dud}
    for candidate, lesson in seen:
        draws = [
            cell.recall
            for cell in cells
            if cell.candidate == candidate and cell.lesson == lesson and not cell.dud
        ]
        if len(draws) > 1:
            spreads.append(max(draws) - min(draws))
    return max(spreads) if spreads else 0.0


def summarise(cells: list[Cell]) -> dict[str, dict[str, float]]:
    """Per candidate: median recall over every cell, and how many draws were duds."""
    out: dict[str, dict[str, float]] = {}
    for candidate in dict.fromkeys(cell.candidate for cell in cells):
        mine = [cell for cell in cells if cell.candidate == candidate]
        scored = [cell for cell in mine if not cell.dud]
        out[candidate] = {
            "cells": len(mine),
            "duds": sum(cell.dud for cell in mine),
            "recall_median": statistics.median([c.recall for c in scored]) if scored else 0.0,
            "invention_median": (
                statistics.median([c.invention for c in scored]) if scored else 0.0
            ),
        }
    return out


def report(cells: list[Cell], repeats: int) -> str:
    summary = summarise(cells)
    ranked = sorted(summary.items(), key=lambda item: -item[1]["recall_median"])
    winner, runner_up = ranked[0], ranked[1] if len(ranked) > 1 else ranked[0]
    last = ranked[-1]
    margin = winner[1]["recall_median"] - runner_up[1]["recall_median"]
    spread = winner[1]["recall_median"] - last[1]["recall_median"]
    floor = max(observed_floor(cells), RECALL_FLOOR)
    stamped = datetime.now(timezone.utc).date().isoformat()

    lines = [
        f"# Harness bake-off — {stamped}",
        "",
        "Generated by `uv run python -m experiments.h1_condition_eval.bakeoff`.",
        f"Selection set: `{SELECTION_SET_PATH.name}` ({len(LESSONS)} lessons, held out from the",
        f"frozen eval set). Condition: {SCREENING_CONDITION.value}. Draws per lesson: {repeats}.",
        "",
        "Every candidate ran the same lessons, the same condition and the same rendering path,",
        "so the harness is the only thing varying.",
        "",
        "| Candidate | framework | module | loop | evidence | version | cells | duds "
        "| recall (median) | invention |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for name, values in ranked:
        harness = harness_for(name).recorded()
        lines.append(
            f"| `{name}` | {harness['framework']} | {harness['module']} | "
            f"{harness['loop']} | {harness['evidence_delivery']} | "
            f"{harness['framework_version']} | "
            f"{values['cells']:.0f} | {values['duds']:.0f} | "
            f"{values['recall_median']:.3f} | {values['invention_median']:.3f} |"
        )
    lines += [
        "",
        "## Verdict",
        "",
        f"Leader: **`{winner[0]}`** at recall {winner[1]['recall_median']:.3f}, "
        f"ahead of `{runner_up[0]}` by **{margin:.3f}**.",
        "",
        f"The margin a winner must clear is **{floor:.3f}** — the larger of the movement these "
        f"candidates showed across their own draws ({observed_floor(cells):.3f}) and the "
        f"published run-to-run median ({RECALL_FLOOR}). "
        + (
            "This margin clears it, so the lead is a difference between harnesses."
            if margin > floor
            else "**This margin does not clear it**, so the top of the table is a tie and "
            "no winner is named."
        ),
        "",
        f"The full spread is `{winner[0]}` over `{last[0]}` by **{spread:.3f}**, which "
        + (
            "clears the floor — so the table separates a top group from a bottom group "
            "even where it cannot rank within them."
            if spread > floor
            else "does NOT clear it either. Nothing in this table separates from anything "
            "else: the same harness on the same lesson moves recall further between draws "
            "than any two harnesses differ."
        ),
        "",
        "A dud is a draw that raised rather than returned a pack. A candidate with duds is",
        "not merely behind; it is unreliable, and that is the count to read first.",
        "",
        "## What this does not cover",
        "",
        "Recall and invention are quantity proxies, and recall is the only one with a",
        "published margin. Read this table as a dud screen and a floor check; the rubric",
        "scores in `HARNESS-JUDGED-*.md` are what the arms are compared on.",
        "",
        "The workspace readers are excluded: they need materialised note files, which is a",
        "dataset shape rather than a harness dimension.",
        "",
        "Every framework reaches the same model through the same provider — one litellm",
        "request, read off the LM `build_dspy_lm` returns — so what varies is the loop.",
        "The frameworks are bounded differently even so: dspy and ADK count model turns,",
        "langgraph counts graph supersteps, and deepagents spends supersteps on middleware",
        "the others do not have. A cut-off composition is recorded, not inferred.",
    ]
    return "\n".join(lines) + "\n"


def generated(cells: list[Cell], repeats: int, temperature: float) -> dict[str, Any]:
    """The packs and what produced them, in one self-describing artefact.

    The harness travels WITH the packs rather than being resolved when they are judged. A
    judged pass that looked up today's installed versions would attribute packs to a
    library that had since moved, which is the failure `harness.py` exists to catch — and
    the judged pass refuses a file whose arms do not carry one.
    """
    return {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "selection_set": SELECTION_SET_PATH.name,
        "condition": SCREENING_CONDITION.value,
        "repeats": repeats,
        "temperature": temperature,
        "arms": {
            candidate: {"harness": harness_for(candidate).recorded()}
            for candidate in dict.fromkeys(cell.candidate for cell in cells)
        },
        "cells": [asdict(cell) for cell in cells],
    }


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--candidates", nargs="*", default=list(CANDIDATES))
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.3,
        help="above zero so a draw is a draw; the cache is disabled either way",
    )
    args = parser.parse_args()

    cells = asyncio.run(bake(tuple(args.candidates), args.repeats, args.temperature))
    stamped = datetime.now(timezone.utc).date().isoformat()
    out = Path(__file__).parent / f"HARNESS-BAKEOFF-{stamped}.md"
    out.write_text(report(cells, args.repeats), encoding="utf-8")
    (out.with_suffix(".json")).write_text(
        json.dumps(generated(cells, args.repeats, args.temperature), indent=2), encoding="utf-8"
    )
    print(f"\nwrote {out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
