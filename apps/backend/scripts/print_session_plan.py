"""Pretty-print a generated session_plan.json as readable text for manual review.

Usage:
    uv run python scripts/print_session_plan.py <path-to-session_plan.json>
    uv run python scripts/print_session_plan.py <dir>   # finds *.session_plan.json inside
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def _block_text(block: dict[str, Any]) -> str:
    for key in (
        "content",
        "text",
        "markdown",
        "body",
        "statement",
        "explanation",
        "prompt",
        "question",
    ):
        value = block.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    # worked example / practice may nest
    for key in ("worked_example", "practice", "items", "steps"):
        value = block.get(key)
        if value:
            return json.dumps(value, ensure_ascii=False)[:600]
    remainder = {k: v for k, v in block.items() if k != "block_type"}
    return json.dumps(remainder, ensure_ascii=False)[:600]


def _print_plan(label: str, plan: dict[str, Any]) -> None:
    nested = plan.get("session_plan")
    session_plan = nested if isinstance(nested, dict) else plan

    print("=" * 88)
    print(f"PLAN: {label}")
    print("=" * 88)
    print(f"  title:    {session_plan.get('title') or session_plan.get('subtopic') or '-'}")
    print(f"  subject:  {session_plan.get('subject', '-')}   term: {session_plan.get('term', '-')}")

    objectives = session_plan.get("lesson_plan_objectives") or session_plan.get("objectives") or []
    print(f"\n  OBJECTIVES ({len(objectives)}):")
    obj_texts = []
    for obj in objectives:
        text = obj.get("objective_text") if isinstance(obj, dict) else str(obj)
        oid = obj.get("lesson_objective_id", "") if isinstance(obj, dict) else ""
        obj_texts.append(text)
        print(f"    - [{oid}] {text}")
    unique = len(set(obj_texts)) == len(obj_texts) if obj_texts else True
    print(
        f"    >>> distinct objective_text? {unique}  "
        f"({len(obj_texts)} total, {len(set(obj_texts))} unique)"
    )

    steps = session_plan.get("steps") or session_plan.get("plan_steps") or []
    print(f"\n  STEPS ({len(steps)}):")
    for index, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            continue
        stype = step.get("step_type") or step.get("type") or "?"
        oid = step.get("lesson_objective_id") or step.get("objective_id") or "-"
        title = step.get("title") or step.get("step_title") or step.get("name") or ""
        print(f"\n    [{index}] type={stype}  objective={oid}")
        if title:
            print(f"        title: {title}")
        blocks = step.get("content_blocks") or step.get("blocks") or step.get("content") or []
        if isinstance(blocks, str):
            print(f"        {blocks[:600]}")
            continue
        for block in _as_list(blocks):
            if not isinstance(block, dict):
                print(f"        {str(block)[:300]}")
                continue
            btype = block.get("block_type") or block.get("type") or "block"
            text = _block_text(block).replace("\n", "\n          ")
            print(f"        <{btype}> {text[:700]}")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    target = Path(sys.argv[1])
    paths: list[Path]
    if target.is_dir():
        paths = sorted(target.glob("*.session_plan.json"))
        if not paths:
            paths = sorted(target.rglob("*session_plan*.json"))
    else:
        paths = [target]

    if not paths:
        print(f"No session_plan json found at {target}")
        return 2

    for path in paths:
        try:
            plan = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            print(f"!! could not read {path.name}: {exc}")
            continue
        _print_plan(path.name, plan)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
