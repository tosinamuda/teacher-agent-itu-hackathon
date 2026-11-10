"""Read a run's agent traces as a story: what each loop thought, read, and did.

uv run python -m experiments.h1_condition_eval.traces <label>
uv run python -m experiments.h1_condition_eval.traces <label> --unit step:step-t3w02-04
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterator

from experiments.h1_condition_eval.config import RUNS_DIR


def _steps(trajectory: object) -> Iterator[tuple[int | str, str, str, str]]:
    """ReAct trajectories are flat dicts keyed thought_0/tool_name_0/...; yield per step."""
    if not isinstance(trajectory, dict):
        yield ("?", str(trajectory)[:200], "", "")
        return
    index = 0
    while f"tool_name_{index}" in trajectory or f"thought_{index}" in trajectory:
        yield (
            index,
            str(trajectory.get(f"thought_{index}", "")).strip(),
            "{}({})".format(
                trajectory.get(f"tool_name_{index}", ""), trajectory.get(f"tool_args_{index}", "")
            ),
            str(trajectory.get(f"observation_{index}", "")).strip(),
        )
        index += 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("label")
    parser.add_argument("--unit", help="only this unit_id / section_id")
    args = parser.parse_args()
    path = RUNS_DIR / args.label / "traces.jsonl"
    if not path.exists():
        raise SystemExit(f"no traces recorded for {args.label}")
    for line in path.read_text().splitlines():
        entry = json.loads(line)
        anchor = entry.get("unit_id") or entry.get("section_id") or "?"
        if args.unit and args.unit != anchor:
            continue
        print(f"\n=== {entry['kind']} {anchor} ({entry.get('engine', 'reviser')}) ===")
        for index, thought, call, observation in _steps(entry.get("trajectory")):
            if thought:
                print(f"  [{index}] think: {thought[:160]}")
            if call and call != "()":
                print(f"      call : {call[:160]}")
            if observation:
                head = observation.splitlines()[0][:120]
                print(f"      saw  : {head}  (+{max(len(observation.splitlines()) - 1, 0)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
