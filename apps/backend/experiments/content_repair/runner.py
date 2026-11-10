"""Run the ReAct content-repair agent over real defect cases and report.

    cd apps/backend
    uv run python -m experiments.content_repair.runner            # both cases
    uv run python -m experiments.content_repair.runner --case mechanical
    DSPY_MODEL=openai/openai.gpt-oss-120b uv run python -m experiments.content_repair.runner

This RUNS the LLM. For each case it prints: the initial issues, the agent's full
Thought/Action/Observation trajectory, then an INDEPENDENT deterministic gate over the
agent's output (the agent does not grade its own homework).
"""

from __future__ import annotations

import argparse
import copy
import os
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import dspy

from app.infra.dspy_lm import active_model_name
from app.shared.json_types import JsonObject

from .agent import RepairSession, build_agent
from .validators import block_list, validate_step

_IMG_BASE = "https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web"

# A real malformed array: rows separated by a bare \hline with NO `\\` terminator — the
# exact defect the drafter produced for LP-758cda07 (MathJax: "Misplaced \hline").
_MALFORMED_TABLE = (
    "The table below lists the names of large numbers as powers of ten.\n\n"
    "$$\n\\begin{array}{|l|l|l|}\\hline "
    "\\textbf{Name} & \\textbf{Number} & \\textbf{Powers of ten}  \\hline "
    "\\text{Ten} & 10 & 10=10^1    \\hline "
    "\\text{Hundred} & 100 & 10\\times10=10^2    \\hline "
    "\\text{Thousand} & 1{,}000 & 10\\times10\\times10=10^3 "
    "\\end{array}\n$$\n\n"
    "The counting-in-millions chart shows how to count from zero up to ten million."
)


@dataclass
class Case:
    key: str
    title: str
    known_problem: str
    step: JsonObject
    grounded_images: list[JsonObject]


def _mechanical_case() -> Case:
    """Real defect: malformed LaTeX table + two grounded counting charts never embedded."""
    return Case(
        key="mechanical",
        title="Understanding millions",
        known_problem=(
            "The powers-of-ten table looks broken and the counting chart it mentions isn't showing."
        ),
        step={
            "step_id": "step01",
            "step_kind": "core",
            "title": "Understanding millions",
            "content": (
                "Explain the concept of a million using the powers-of-ten table and the "
                "counting-in-millions chart."
            ),
            "blocks": [
                {"id": "step01-exp", "type": "explanation", "content": _MALFORMED_TABLE},
            ],
        },
        grounded_images=[
            {
                "url": f"{_IMG_BASE}/ebw-jss1-01-007.png",
                "source_record_id": "ch01-b035",
                "source_html_path": "dataset/textbook/html/Chapter 01 - Numbers big and small.html",
                "source_anchor_id": "counting-up-to-one-billion",
            },
            {
                "url": f"{_IMG_BASE}/ebw-jss1-01-008.png",
                "source_record_id": "ch01-b035",
                "source_html_path": "dataset/textbook/html/Chapter 01 - Numbers big and small.html",
                "source_anchor_id": "counting-up-to-one-billion",
            },
        ],
    )


def _open_ended_case() -> Case:
    """No tool can fix this: prose points at a diagram that does not exist and has no
    source figure to embed. The agent must reason and rewrite the prose itself."""
    return Case(
        key="open_ended",
        title="Angles in a triangle",
        known_problem="The step keeps pointing at a diagram, but there is no diagram.",
        step={
            "step_id": "step03",
            "step_kind": "core",
            "title": "Angles in a triangle",
            "content": (
                "Study the diagram below to see how the three angles of a triangle always "
                "add up to 180 degrees."
            ),
            "blocks": [
                {
                    "id": "step03-exp",
                    "type": "explanation",
                    "content": (
                        "As shown in the figure above, the three interior angles meet along "
                        "a straight line."
                    ),
                }
            ],
        },
        grounded_images=[],
    )


def _ensure_env() -> None:
    """Load *_API_KEY entries from apps/backend/.env into os.environ if not already set
    (litellm, which DSPy uses, reads keys from the process environment)."""
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if ("API_KEY" in key or "OPENROUTER" in key) and key not in os.environ:
            os.environ[key] = value.strip().strip('"').strip("'")


def _configure_lm() -> str:
    model = os.getenv("DSPY_MODEL") or active_model_name()
    if getattr(dspy.settings, "lm", None) is None:
        dspy.configure(lm=dspy.LM(model=model))
    return model


def _print_trajectory(trajectory: object) -> None:
    if not isinstance(trajectory, dict):
        print("   (no trajectory captured)")
        return
    trajectory = cast(dict[str, object], trajectory)
    index = 0
    while True:
        thought = trajectory.get(f"thought_{index}")
        tool = trajectory.get(f"tool_name_{index}")
        if thought is None and tool is None:
            break
        if thought:
            print(f"   [{index}] THOUGHT: {str(thought).strip()}")
        if tool:
            raw_args = trajectory.get(f"tool_args_{index}")
            args = raw_args if isinstance(raw_args, dict) else {}
            arg_preview = ", ".join(f"{k}={str(v)[:60]!r}" for k, v in args.items())
            print(f"       ACTION: {tool}({arg_preview})")
        observation = trajectory.get(f"observation_{index}")
        if observation is not None:
            obs = str(observation).strip().replace("\n", "\n                ")
            print(f"       OBSERVE: {obs}")
        index += 1


def run_case(case: Case) -> bool:
    print("=" * 88)
    print(f"CASE: {case.key}  —  {case.title!r}")
    print("-" * 88)

    before = validate_step(case.step, case.grounded_images)
    print(f"Initial issues ({len(before.issues)}):")
    for issue in before.issues:
        print(f"  - {issue}")

    session = RepairSession(copy.deepcopy(case.step), copy.deepcopy(case.grounded_images))
    agent = build_agent(session)
    prediction = agent(step_title=case.title, known_problem=case.known_problem)

    print("\nReAct trajectory:")
    _print_trajectory(getattr(prediction, "trajectory", None))
    print(f"\nAgent outcome: {getattr(prediction, 'outcome', '(none)')}")
    print(f"Tool calls: {session.tool_calls}")

    # INDEPENDENT gate over the agent's actual output — the agent never grades itself.
    after = validate_step(session.step, session.grounded_images)
    verdict = "PASS" if after.ok else "FAIL"
    print(f"\nINDEPENDENT GATE: {verdict}")
    if not after.ok:
        for issue in after.issues:
            print(f"  - {issue}")
    blocks = block_list(session.step)
    visual = [b for b in blocks if b.get("type") == "visual"]
    print(f"(final step has {len(blocks)} blocks, {len(visual)} visual)")
    return after.ok


def main() -> None:
    parser = argparse.ArgumentParser(description="ReAct content-repair experiment")
    parser.add_argument("--case", choices=["mechanical", "open_ended", "all"], default="all")
    args = parser.parse_args()

    _ensure_env()
    model = _configure_lm()
    print(f"Model: {model}\n")

    cases = {"mechanical": _mechanical_case(), "open_ended": _open_ended_case()}
    selected = list(cases.values()) if args.case == "all" else [cases[args.case]]

    results = {case.key: run_case(case) for case in selected}
    print("\n" + "=" * 88)
    print("SUMMARY:", {k: ("PASS" if v else "FAIL") for k, v in results.items()})


if __name__ == "__main__":
    main()
