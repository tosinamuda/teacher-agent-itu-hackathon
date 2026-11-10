"""Rate the packs a harness bake-off produced, and measure the judge while doing it.

The screen the bake-off runs cannot separate anything and says so: recall moves further
between draws of one harness than the whole table spreads, and invention is reported with
no margin at all. Neither is what the study measures. The study measures four rubric
dimensions, rated blind, one candidate per call — so that is what the arms are compared on
here, through the packet builder the hand-dispatched judges read from.

Two properties make the number readable.

**Every pack is rated twice.** In the study's own noise measurement the same prose given to
the same judge twice moved more than half of every arm's scores by about 0.45. A lead is
only a lead once it clears what the judge does to text that did not change.

**The harness travels with the packs.** Arms are read out of the bake-off artefact, which
records what produced each one. A file that does not say is refused rather than credited to
whatever happens to be installed today.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import statistics
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import dspy

from experiments.h1_condition_eval.collect_judgments import DIMENSIONS
from experiments.h1_condition_eval.harness import require_recorded
from experiments.h1_condition_eval.judge import judge_packet
from experiments.h1_condition_eval.rater_packets import packet
from experiments.h1_condition_eval.selection_set import SELECTION_SET_PATH, freeze

PASSES = 2
"""How many times each pack is rated by default. Two is the least that measures the judge:
with one, a lead of 0.3 and the judge's own movement of 0.45 are indistinguishable. More is
a flag, and the reported floor widens or narrows with whatever was actually run."""


@dataclass(frozen=True)
class Rated:
    """One pack, rated independently as many times as the pass asked for."""

    candidate: str
    lesson: str
    draw: int
    packet_id: str
    passes: tuple[dict[str, float], ...]

    def per_pass(self) -> tuple[float, ...]:
        """Each pass's mean over the four rubric dimensions."""
        return tuple(statistics.fmean(scores.values()) for scores in self.passes)

    def mean(self) -> float:
        """The pack's score: every dimension, every pass."""
        return statistics.fmean(self.per_pass())

    def movement(self) -> float:
        """How far the judge moved on prose that did not change."""
        marks = self.per_pass()
        return max(marks) - min(marks)


def artefact(path: Path) -> dict[str, Any]:
    """The bake-off's own output, refusing anything that is not one."""
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict) or not isinstance(loaded.get("cells"), list):
        raise ValueError(
            f"{path.name} carries no bake-off cells. Rate the JSON written beside "
            "HARNESS-BAKEOFF-<date>.md, not the report."
        )
    return loaded


def harnesses(loaded: dict[str, Any]) -> dict[str, dict[str, str]]:
    """What produced each arm in the file, refusing one that does not record it."""
    declared = loaded.get("arms")
    arms: dict[str, Any] = declared if isinstance(declared, dict) else {}
    return {
        candidate: require_recorded(arms.get(candidate) or {}, f"bake-off arm {candidate!r}")
        for candidate in dict.fromkeys(cell["candidate"] for cell in loaded["cells"])
    }


def plans() -> dict[str, dict[str, Any]]:
    """The held-out lessons, read from the frozen file and checked against their source.

    The bake-off generates from `selection_set.LESSONS` and this rates against
    `selection_set.json`. If the two ever drift, a pack is rated against a lesson that did
    not produce it — and that reads back as a bad harness rather than as a stale file.
    """
    frozen = json.loads(SELECTION_SET_PATH.read_text(encoding="utf-8"))["cases"]
    live = {case["lesson"]: case["plan_sha256"] for case in freeze()["cases"]}
    drifted = [case["lesson"] for case in frozen if live.get(case["lesson"]) != case["plan_sha256"]]
    if drifted or set(live) != {case["lesson"] for case in frozen}:
        raise ValueError(
            f"{SELECTION_SET_PATH.name} no longer matches selection_set.py "
            f"({drifted or sorted(set(live) ^ {c['lesson'] for c in frozen})}). Re-freeze it "
            "before rating, or the packs are judged against a different lesson."
        )
    return {case["lesson"]: case["plan"] for case in frozen}


def blinded_id(source: str, cell: dict[str, Any]) -> str:
    """An opaque, stable id: the judge must not read the arm off the packet it is given."""
    seed = f"{source}|{cell['lesson']}|{cell['candidate']}|{cell['draw']}"
    return "cand-" + hashlib.sha256(seed.encode()).hexdigest()[:8]


async def rate(
    loaded: dict[str, Any], *, source: str, lm: dspy.LM, concurrency: int, passes: int = PASSES
) -> list[Rated]:
    """Every pack in the artefact, rated `passes` times, one candidate per call."""
    lessons = plans()
    gate = asyncio.Semaphore(concurrency)
    cells = [cell for cell in loaded["cells"] if not cell["dud"] and cell["sections"]]

    async def one(cell: dict[str, Any]) -> Rated:
        built = packet(blinded_id(source, cell), lessons[cell["lesson"]], cell["sections"])
        marks = [await _one_pass(built, lm, gate) for _ in range(passes)]
        print(
            f"  rated {built['candidate_id']}  {cell['candidate']:14s} {cell['lesson']:12s} "
            f"draw {cell['draw']}  "
            + "  ".join(f"{statistics.fmean(m.values()):.2f}" for m in marks)
        )
        return Rated(
            candidate=cell["candidate"],
            lesson=cell["lesson"],
            draw=cell["draw"],
            packet_id=built["candidate_id"],
            passes=tuple(marks),
        )

    return list(await asyncio.gather(*(one(cell) for cell in cells)))


async def _one_pass(
    built: dict[str, Any], lm: dspy.LM, gate: asyncio.Semaphore
) -> dict[str, float]:
    async with gate:
        judgment = await judge_packet(built, lm=lm)
    return {dimension: float(judgment[dimension]["score"]) for dimension in DIMENSIONS}


def summarise(rated: list[Rated]) -> dict[str, dict[str, float]]:
    """Per candidate: the rubric mean, and each dimension over every pack and pass."""
    out: dict[str, dict[str, float]] = {}
    for candidate in dict.fromkeys(item.candidate for item in rated):
        mine = [item for item in rated if item.candidate == candidate]
        out[candidate] = {
            "packs": float(len(mine)),
            "rubric_mean": statistics.fmean(item.mean() for item in mine),
            **{
                dimension: statistics.fmean(
                    marks[dimension] for item in mine for marks in item.passes
                )
                for dimension in DIMENSIONS
            },
        }
    return out


# Both floors are measured on a candidate's WHOLE ROW — its mean over every pack — because
# that is what the table compares. Measured per cell instead, the draw floor came out at
# 2.12 on one lesson of one arm (1.38 against 3.50, from the two draws that survived a dud)
# and would have been held against differences between twelve-pack means. Comparing a mean
# to a single cell's spread is the level error the recall screen already makes; repeating it
# in a new metric would buy nothing but a second unfalsifiable table.


def judge_floor(rated: list[Rated]) -> float:
    """What the judge does to a whole row when nothing in it changed.

    Every pack is rated twice, so each candidate has two row means over identical prose.
    The widest gap between them is what a lead has to beat before it is about the harness.
    """
    return _widest(
        rated, lambda mine: [_pass_mean(mine, index) for index in range(passes_per_pack(mine))]
    )


def draw_floor(rated: list[Rated]) -> float:
    """What one harness does to its own row when only the draw changed."""
    return _widest(
        rated,
        lambda mine: [
            statistics.fmean([item.mean() for item in mine if item.draw == draw])
            for draw in sorted({item.draw for item in mine})
        ],
    )


def passes_per_pack(rated: list[Rated]) -> int:
    """How many times each pack was actually rated, read off the ratings themselves."""
    return min((len(item.passes) for item in rated), default=0)


def pack_movements(rated: list[Rated]) -> list[float]:
    """Per pack, how far the judge moved between its two readings of the same prose.

    Descriptive, not a floor: a pack is a level finer than anything the table compares.
    """
    return [item.movement() for item in rated]


def _pass_mean(rated: list[Rated], index: int) -> float:
    return statistics.fmean([item.per_pass()[index] for item in rated])


def _widest(rated: list[Rated], rows: Callable[[list[Rated]], list[float]]) -> float:
    """The largest spread any one candidate showed between versions of its own row."""
    spreads = []
    for candidate in dict.fromkeys(item.candidate for item in rated):
        marks = rows([item for item in rated if item.candidate == candidate])
        if len(marks) > 1:
            spreads.append(max(marks) - min(marks))
    return max(spreads) if spreads else 0.0
