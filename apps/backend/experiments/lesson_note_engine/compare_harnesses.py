"""Compare the engine's loops head to head: a run's engine notes against a control run's.

Run from ``apps/backend``. Each run to compare is paired with the control, then judged with
``judging.py``, then reported::

    uv run python -m experiments.lesson_note_engine.compare_harnesses pair CONTROL RUN
    uv run python -m experiments.lesson_note_engine.judging RUN-vs-control --judges 3
    (the judges write their verdicts)
    uv run python -m experiments.lesson_note_engine.compare_harnesses report CONTROL RUN [RUN ...]

``pair`` writes the folder ``RUN-vs-control``: the run's lessons with the control's engine
notes in the place of the current generator's. The judges then see, for each step, the teacher's
note, the control's and the run's, in one packet, so one judge ranks the two loops side by side.
``report`` prints what finishing the drafts took, and which engine note the judges liked
better. The step is the unit: each step's score difference is the mean over its judges, and the
steps that favour the run are counted against those that favour the control, with the exact
two-sided sign test. The counts by verdict are printed too, but a step's verdicts are not
independent, so their test overstates the evidence. The notes' lengths are printed because
judges tend to reward longer notes. Pair two runs of the same loop to measure the noise the
others are read against.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from math import comb
from pathlib import Path

from experiments.lesson_note_engine.judging import comparable

HERE = Path(__file__).parent
SUFFIX = "-vs-control"
#: Bedrock's price for gpt-oss-120b, per token.
PROMPT_RATE = 0.15e-6
COMPLETION_RATE = 0.60e-6


@dataclass
class Finishing:
    """What finishing a run's drafts took, added up over its lessons."""

    lessons: int = 0
    failed: int = 0
    rounds: int = 0
    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    seconds: float = 0.0

    @property
    def cost(self) -> float:
        return self.prompt_tokens * PROMPT_RATE + self.completion_tokens * COMPLETION_RATE


def finishing(folder: Path, only: set[str] | None = None) -> Finishing:
    """What a run's drafts took, for the lessons in ``only`` when it is given."""
    total = Finishing()
    for path in sorted(folder.glob("LPV-*.json")):
        lesson = json.loads(path.read_text(encoding="utf-8"))
        if only is not None and lesson["plan_version_id"] not in only:
            continue
        made = lesson.get("engine_run") or {}
        total.lessons += 1
        total.failed += bool(made.get("failure"))
        total.rounds += made.get("rounds", 0)
        total.calls += made.get("calls", 0)
        total.prompt_tokens += made.get("prompt_tokens", 0)
        total.completion_tokens += made.get("completion_tokens", 0)
        total.seconds += made.get("seconds", 0.0)
    return total


def pair(control: Path, run: Path, into: Path) -> list[str]:
    """Write ``into``: ``run``'s lessons, with ``control``'s engine notes as the current notes.

    Only the lessons both runs have are kept. Returns their plan version IDs.
    """
    into.mkdir(exist_ok=True)
    kept = []
    for path in sorted(run.glob("LPV-*.json")):
        held = control / path.name
        if not held.exists():
            continue
        lesson = json.loads(path.read_text(encoding="utf-8"))
        lesson["notes"]["current"] = json.loads(held.read_text(encoding="utf-8"))["notes"]["engine"]
        lesson["paired_with"] = control.name
        (into / path.name).write_text(json.dumps(lesson, indent=1, ensure_ascii=False))
        kept.append(lesson["plan_version_id"])
    return kept


def sign_test(higher: int, lower: int) -> float:
    """The exact two-sided p of ``higher`` against ``lower`` if each were as likely as the other."""
    counted = higher + lower
    if counted == 0:
        return 1.0
    tail = sum(comb(counted, k) for k in range(min(higher, lower) + 1)) / 2**counted
    return min(1.0, 2 * tail)


@dataclass(frozen=True)
class HeadToHead:
    """What the judges made of the run's engine notes against the control's."""

    judged: int
    run_score: float
    control_score: float
    higher: int
    lower: int
    same: int
    above: int
    below: int
    steps: int
    steps_higher: int
    steps_lower: int
    run_words: int
    control_words: int

    @property
    def p_steps(self) -> float:
        return sign_test(self.steps_higher, self.steps_lower)

    @property
    def p_score(self) -> float:
        return sign_test(self.higher, self.lower)

    @property
    def p_rank(self) -> float:
        return sign_test(self.above, self.below)


def _mean(marks: dict[str, int]) -> float:
    return sum(marks.values()) / len(marks)


def head_to_head(folder: Path) -> HeadToHead:
    """Tally every verdict of a paired folder: the engine note (the run's) against the control's."""
    keys = json.loads((folder / "judging-keys.json").read_text())
    items = comparable(folder)
    judged = higher = lower = same = above = below = 0
    run_total = control_total = 0.0
    by_step: dict[int, list[float]] = defaultdict(list)
    for path in sorted((folder / "judging").glob("verdict-*.json")):
        judge = path.stem.split("-")[1]
        for verdict in json.loads(path.read_text())["items"]:
            named = {source: label for label, source in keys[judge][str(verdict["item"])].items()}
            run, control = named["engine"], named["current"]
            run_score, control_score = (_mean(verdict["scores"][x]) for x in (run, control))
            judged += 1
            run_total += run_score
            control_total += control_score
            by_step[verdict["item"]].append(run_score - control_score)
            higher += run_score > control_score
            lower += run_score < control_score
            same += run_score == control_score
            placed_above = verdict["ranking"].index(run) < verdict["ranking"].index(control)
            above += placed_above
            below += not placed_above
    means = [sum(scores) / len(scores) for scores in by_step.values()]
    return HeadToHead(
        judged,
        run_total / (judged or 1),
        control_total / (judged or 1),
        higher,
        lower,
        same,
        above,
        below,
        len(means),
        sum(mean > 0 for mean in means),
        sum(mean < 0 for mean in means),
        sum(len(str(item["notes"]["engine"]).split()) for item in items),
        sum(len(str(item["notes"]["current"]).split()) for item in items),
    )


def _report(name: str, made: Finishing, against: HeadToHead | None) -> str:
    lines = [
        f"{name}: finished {made.lessons - made.failed}/{made.lessons} drafts; "
        f"{made.rounds} rounds, {made.calls} calls, "
        f"{made.prompt_tokens:,}/{made.completion_tokens:,} tokens, ${made.cost:.2f}, "
        f"{made.seconds / 60:.0f} min"
    ]
    if against is not None:
        lines.append(
            f"    by step, {against.steps} judged: the run's engine note averaged higher in "
            f"{against.steps_higher}, lower in {against.steps_lower} (p = {against.p_steps:.3f}); "
            f"engine score {against.run_score:.2f} against the control's "
            f"{against.control_score:.2f}; notes {against.run_words} words against "
            f"{against.control_words}"
        )
        lines.append(
            f"    by verdict, {against.judged} judged (not independent): scored higher "
            f"{against.higher}, lower {against.lower}, same {against.same} "
            f"(p = {against.p_score:.3f}); placed above {against.above}, below {against.below} "
            f"(p = {against.p_rank:.3f})"
        )
    return "\n".join(lines)


def report(control: str, runs: list[str]) -> None:
    for name in runs:
        paired = HERE / "runs" / f"{name}{SUFFIX}"
        lessons = {json.loads(p.read_text())["plan_version_id"] for p in paired.glob("LPV-*.json")}
        made = finishing(HERE / "runs" / name, lessons)
        held = finishing(HERE / "runs" / control, lessons)
        print(_report(f"{control} (same lessons)", held, None))
        print(_report(name, made, head_to_head(paired)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("pair", "report"):
        sub = commands.add_parser(command)
        sub.add_argument("control", help="The control run's folder under runs/")
        sub.add_argument("runs", nargs="+" if command == "report" else 1)
    arguments = parser.parse_args()
    if arguments.command == "pair":
        folder = arguments.runs[0]
        kept = pair(
            HERE / "runs" / arguments.control,
            HERE / "runs" / folder,
            HERE / "runs" / f"{folder}{SUFFIX}",
        )
        print(f"{folder}{SUFFIX}: {len(kept)} lessons paired: {kept}")
    else:
        report(arguments.control, arguments.runs)
