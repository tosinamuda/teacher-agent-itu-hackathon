"""Can anything tell the arms apart, and can a blinded reader?

Two passes over the same judged packs, cheapest first.

**Surface pass** (no model). Vocabulary overlap between two packs of the same lesson,
measured against the overlap between two DRAWS of the same arm. The second number is the
floor: if re-running one condition changes a pack as much as changing the condition does,
there is no arm signal at the surface to find.

**Reader pass** (one model call per comparison). A forced choice on an anonymised pair —
which of these two was written with more knowledge of how the lesson was actually taught.
Chance is 50%, so this needs no rating scale and never touches the 0.45 judge floor: a
reader who cannot beat chance has told us the arms are indistinguishable, and a margin
inside the floor is not something a discrimination task can produce.

C0 versus C3 runs as a positive control. If a reader cannot separate the baseline from the
arm that topped every rated dimension, the reader is the problem and the C0/C1 result says
nothing.

    uv run python -m experiments.h1_condition_eval.blind_separability --surface
    uv run python -m experiments.h1_condition_eval.blind_separability --read
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

import dspy

from app.infra.dspy_lm import build_dspy_lm

RUN_LABEL = "c0c3-worksheet"
COMPARISONS = (("C0", "C1"), ("C0", "C3"))
_WORD = re.compile(r"[a-z]{3,}")


@dataclass(frozen=True)
class Candidate:
    """One pack, stripped of anything naming its arm."""

    lesson: str
    draw: int
    condition: str
    text: str


def run_dir(label: str = RUN_LABEL) -> Path:
    return Path(__file__).parent / "runs" / label


def candidates(label: str = RUN_LABEL) -> dict[tuple[str, int], dict[str, Candidate]]:
    """Every judged pack, keyed by lesson and draw then by arm."""
    record = json.loads((run_dir(label) / "run.json").read_text(encoding="utf-8"))
    packs: dict[tuple[str, int], dict[str, Candidate]] = defaultdict(dict)
    for case in record["cases"]:
        if not case.get("sections_json"):
            continue
        key = (case["lesson"], int(case.get("repeat", 1)))
        packs[key][case["condition"]] = Candidate(
            lesson=case["lesson"],
            draw=key[1],
            condition=case["condition"],
            text=pack_text(case["sections_json"]),
        )
    return dict(packs)


def pack_text(sections: list[dict]) -> str:
    """The pack as a reader meets it: no ids, no source refs, no arm."""
    parts: list[str] = []
    for section in sections:
        parts.append(section.get("title") or "")
        for block in section.get("blocks") or []:
            parts.append(block.get("text") or "")
        for item in section.get("practice") or []:
            parts += [item.get("prompt") or "", item.get("answer") or ""]
    return "\n".join(part for part in parts if part)


def overlap(left: str, right: str) -> float:
    """Vocabulary Jaccard. Crude on purpose — a floor comparison, not a quality score."""
    a, b = set(_WORD.findall(left.lower())), set(_WORD.findall(right.lower()))
    return len(a & b) / len(a | b) if a | b else 0.0


def surface_pass(label: str = RUN_LABEL) -> dict[str, float]:
    """Between-arm overlap beside the within-arm floor."""
    packs = candidates(label)
    between: dict[str, list[float]] = defaultdict(list)
    for byarm in packs.values():
        for left, right in (("C0", "C1"), ("C1", "C2"), ("C0", "C2"), ("C2", "C3")):
            if left in byarm and right in byarm:
                between[f"{left}-{right}"].append(overlap(byarm[left].text, byarm[right].text))

    by_lesson: dict[tuple[str, str], list[str]] = defaultdict(list)
    for (lesson, _draw), byarm in packs.items():
        for arm, candidate in byarm.items():
            by_lesson[(lesson, arm)].append(candidate.text)
    within: dict[str, list[float]] = defaultdict(list)
    for (_lesson, arm), texts in by_lesson.items():
        for index, left in enumerate(texts):
            for right in texts[index + 1 :]:
                within[arm].append(overlap(left, right))

    return {
        **{f"between {name}": statistics.median(values) for name, values in between.items()},
        **{f"within {arm} (floor)": statistics.median(values) for arm, values in within.items()},
    }


class WhichSawTheLesson(dspy.Signature):
    """Two take-home revision packs for the same lesson, written by different systems.

    One was written with more knowledge of how the lesson was actually taught — what the
    teacher planned to do, in what order, what she set the class to practise and what she
    used to check it. The other was written from the objective and the syllabus alone.

    Decide which is which. If nothing in either pack lets you tell, say so plainly by
    answering "neither" rather than guessing: a forced guess would be indistinguishable
    from a real judgement in the tally.
    """

    pack_a: str = dspy.InputField(desc="The first pack, in full.")
    pack_b: str = dspy.InputField(desc="The second pack, in full.")
    answer: Literal["a", "b", "neither"] = dspy.OutputField(
        desc="Which pack shows more knowledge of the taught lesson, or 'neither'."
    )
    what_told_you: str = dspy.OutputField(
        desc="One sentence naming what distinguished them, or what made them indistinguishable."
    )


def _order(lesson: str, draw: int, comparison: tuple[str, str]) -> bool:
    """Whether the richer arm goes second. Deterministic and roughly balanced."""
    seed = hashlib.sha256(f"{lesson}{draw}{comparison}".encode()).hexdigest()
    return int(seed[0], 16) % 2 == 0


@dataclass(frozen=True)
class Verdict:
    """One blinded comparison."""

    lesson: str
    draw: int
    comparison: str
    correct: bool | None
    """None when the reader said the two were indistinguishable."""
    said: str
    because: str


def reader_pass(label: str = RUN_LABEL) -> list[Verdict]:
    """One forced choice per pair, on packs stripped of anything naming their arm."""
    dspy.configure(lm=build_dspy_lm())
    ask = dspy.Predict(WhichSawTheLesson)
    verdicts: list[Verdict] = []
    for (lesson, draw), byarm in sorted(candidates(label).items()):
        for comparison in COMPARISONS:
            plain, rich = comparison
            if plain not in byarm or rich not in byarm:
                continue
            rich_second = _order(lesson, draw, comparison)
            first, second = (plain, rich) if rich_second else (rich, plain)
            result = ask(pack_a=byarm[first].text, pack_b=byarm[second].text)
            said = str(result.answer).lower().strip()
            chose = {"a": first, "b": second}.get(said)
            verdicts.append(
                Verdict(
                    lesson=lesson,
                    draw=draw,
                    comparison=f"{plain} vs {rich}",
                    correct=None if chose is None else chose == rich,
                    said=said,
                    because=str(result.what_told_you),
                )
            )
    return verdicts


def tally(verdicts: list[Verdict]) -> dict[str, dict[str, int]]:
    """Per comparison: right, wrong, and told-apart-by-nothing."""
    out: dict[str, dict[str, int]] = defaultdict(lambda: {"right": 0, "wrong": 0, "neither": 0})
    for verdict in verdicts:
        key = "neither" if verdict.correct is None else ("right" if verdict.correct else "wrong")
        out[verdict.comparison][key] += 1
    return dict(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--surface", action="store_true", help="the no-model pass")
    parser.add_argument("--read", action="store_true", help="the blinded reader pass")
    parser.add_argument("--label", default=RUN_LABEL)
    args = parser.parse_args()
    if args.surface:
        for name, value in surface_pass(args.label).items():
            print(f"{name:24s} {value:.3f}")
    if args.read:
        verdicts = reader_pass(args.label)
        for comparison, counts in sorted(tally(verdicts).items()):
            total = sum(counts.values())
            print(
                f"{comparison}: right {counts['right']}/{total}, "
                f"wrong {counts['wrong']}, indistinguishable {counts['neither']}"
            )
        (run_dir(args.label) / "blind-separability.json").write_text(
            json.dumps([asdict(v) for v in verdicts], indent=2), encoding="utf-8"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
