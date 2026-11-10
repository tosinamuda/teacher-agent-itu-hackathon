"""What the model actually wrote, before the harness made it reader-ready.

``pack_metrics`` measures stored sections, and a stored section has been through
``reader_ready`` — since the HTML step landed, a pack can show zero tags whatever
the model emitted. The trace keeps the loop as it ran, and inside it every tool
call's arguments are the model's own words at the moment it wrote them. This reads
those arguments and nothing else: not the prompt, not the observations that echo a
draft back, so nothing is counted twice and nothing the harness supplied is counted
at all.

A trace record names its unit, not its condition, so the split is by lesson.

    uv run python -m experiments.h1_condition_eval.raw_markup c0c3-prism-objective
"""

from __future__ import annotations

import argparse
import ast
import collections
import json
import re
from typing import Any

from app.shared.llm_html import count_html_tags
from app.shared.llm_markup import count_bare_math
from experiments.h1_condition_eval.config import RUNS_DIR

_CALL_ARGS = re.compile(r"args=\{")
# A unit id spells its lesson without the hyphen: `objective:lo-t3w02-02`, `step:step-t3w05-02`.
_LESSON = re.compile(r"t(\d)w(\d\d)")


def _balanced_end(text: str, start: int) -> int:
    """Index of the brace closing the one at *start*, honouring quoted strings."""
    depth, quote, escaped = 0, "", False
    for index in range(start, len(text)):
        char = text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = ""
        elif char in "\"'":
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    return -1


def tool_call_arguments(trajectory: str) -> list[dict[str, Any]]:
    """Every ``args={...}`` literal in a rendered trajectory, as the dict it spells."""
    found: list[dict[str, Any]] = []
    for match in _CALL_ARGS.finditer(trajectory):
        start = match.end() - 1
        end = _balanced_end(trajectory, start)
        if end < 0:
            continue
        try:
            value = ast.literal_eval(trajectory[start : end + 1])
        except (ValueError, SyntaxError):
            continue
        if isinstance(value, dict):
            found.append(value)
    return found


def _strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in _strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in _strings(v)]
    return []


def measure(run_label: str) -> dict[str, collections.Counter]:
    """Per lesson: tool calls read, characters written, HTML tags, bare commands."""
    per_lesson: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    with (RUNS_DIR / run_label / "traces.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            match = _LESSON.search(record.get("unit_id") or "")
            lesson = f"t{match[1]}-w{match[2]}" if match else "?"
            tally = per_lesson[lesson]
            tally["units"] += 1
            unit_tags = 0
            for arguments in tool_call_arguments(record.get("trajectory") or ""):
                text = "\n".join(_strings(arguments))
                tally["calls"] += 1
                tally["chars"] += len(text)
                unit_tags += count_html_tags(text)
                tally["bare_latex"] += count_bare_math(text)
            tally["html_tags"] += unit_tags
            # Whether the model wrote HTML is decided per unit, not per tag: a unit that
            # starts a section in HTML tends to finish it that way, so the share of units
            # is the rate a single run can actually estimate.
            tally["units_with_html"] += unit_tags > 0
    return per_lesson


_HEADER = (
    "| lesson | units | with HTML | calls | chars | HTML tags | bare LaTeX |",
    "|---|---:|---:|---:|---:|---:|---:|",
)


def _row(name: str, tally: collections.Counter, *, bold: bool = False) -> str:
    share = f"{tally['units_with_html']} ({100 * tally['units_with_html'] / tally['units']:.0f}%)"
    counts = [tally["units"], share, tally["calls"], tally["chars"]]
    markup = [tally["html_tags"], tally["bare_latex"]]
    shown = [str(c) for c in counts] + [f"**{m}**" if bold else str(m) for m in markup]
    return f"| {name} | " + " | ".join(shown) + " |"


def report(run_label: str) -> str:
    per_lesson = measure(run_label)
    total: collections.Counter = collections.Counter()
    for tally in per_lesson.values():
        total.update(tally)
    rows = [f"# Raw markup — `{run_label}`", "", *_HEADER]
    rows += [_row(lesson, per_lesson[lesson]) for lesson in sorted(per_lesson)]
    rows.append(_row("**all**", total, bold=True))
    per_kchar = 1000 * total["html_tags"] / total["chars"] if total["chars"] else 0.0
    rows += ["", f"**{per_kchar:.2f} tags per 1,000 characters** the model wrote."]
    return "\n".join(rows) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_label")
    args = parser.parse_args()
    print(report(args.run_label))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
