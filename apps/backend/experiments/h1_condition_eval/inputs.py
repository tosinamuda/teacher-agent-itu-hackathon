"""Dump what each condition actually puts in front of the model.

A condition is defined by its prompt, so the prompt is the thing to inspect when a
result needs explaining — not the policy object that produced it. This renders the
REAL adapter messages (the same ``dspy.ChatAdapter`` the generator calls), writes one
file per lesson/condition/unit, and reports which lesson-plan strings survive into
them verbatim.

Written under the run label, so a dump is tied to the code and data that produced it.

    uv run python -m experiments.h1_condition_eval.inputs
    uv run python -m experiments.h1_condition_eval.inputs --lessons t3-w05
"""

from __future__ import annotations

import argparse
import json
from typing import Any

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    BaseReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    WriteSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prompt_projection import (  # noqa: E501
    prompt_unit,
)
from app.domains.experiments.review_pack_study.conditions.variants import profiles_for_variant
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.config import H1_EVAL_CONDITIONS, RUNS_DIR
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.fingerprints import fingerprint


def render_prompt(request: BaseReviewPackRequest, unit: SectionGenerationUnit) -> str:
    """The exact messages the generator sends for one unit."""
    messages = dspy.ChatAdapter().format(
        WriteSection,
        [],
        {
            "artefact_spec": request.artefact_spec,
            "policy": request.policy,
            "lesson_context": request.lesson_context,
            "unit_context": prompt_unit(unit),
            "source_evidence": unit.source_evidence,
        },
    )
    return "\n\n".join(f"===== {m['role'].upper()} =====\n{m['content']}" for m in messages)


def _plan_strings(plan: SessionPlanView) -> dict[str, list[str]]:
    """The lesson-plan text a pack must never simply copy out."""
    steps = [step for step in plan.steps if step.step_kind == "core"]
    return {
        "step_title": [step.title for step in steps if step.title],
        "activity_what": [
            str(activity.get("what") or "")
            for step in steps
            for activity in (step.activities or [])
        ],
        "step_content": [step.content for step in steps if step.content],
    }


def _leak_report(prompt: str, plan: SessionPlanView) -> dict[str, Any]:
    """Which plan strings reach the model verbatim — the only ones it can copy."""
    return {
        kind: [value for value in values if value and value.strip() in prompt]
        for kind, values in _plan_strings(plan).items()
    }


def dump(label: str, lessons: list[str] | None, context_variant: str = "v3") -> int:
    cases = json.loads(EVAL_SET_PATH.read_text())["cases"]
    if lessons:
        cases = [case for case in cases if case["lesson"] in lessons]
    builder = BaseReviewPackRequestBuilder()
    profiles = profiles_for_variant(context_variant)
    out_root = RUNS_DIR / label / "inputs"
    summary: list[dict[str, Any]] = []

    for case in cases:
        plan = SessionPlanView.model_validate(case["plan"])
        for code in H1_EVAL_CONDITIONS:
            profile = profiles[code]
            request = builder.build(
                session_plan=plan,
                policy=profile.generation_policy(),
                sources=LessonSources.unresolved(plan.references),
            )
            out_dir = out_root / case["lesson"]
            out_dir.mkdir(parents=True, exist_ok=True)
            prompts = [render_prompt(request, unit) for unit in request.units]
            (out_dir / f"{code.value}.txt").write_text("\n\n\n".join(prompts), encoding="utf-8")
            whole = "\n".join(prompts)
            leaks = _leak_report(whole, plan)
            summary.append(
                {
                    "lesson": case["lesson"],
                    "condition": code.value,
                    "units": len(request.units),
                    "prompt_chars": len(whole),
                    "evidence_chars": sum(
                        len(item.excerpt) for unit in request.units for item in unit.source_evidence
                    ),
                    **{f"verbatim_{kind}": len(values) for kind, values in leaks.items()},
                    "leaked_step_titles": leaks["step_title"],
                }
            )

    (out_root / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    header = (
        f"{'lesson':9s} {'cond':4s} {'units':>5s} {'chars':>7s} {'evid':>6s} "
        f"{'title':>5s} {'activ':>5s} {'contnt':>6s}"
    )
    print(header)
    print("-" * len(header))
    for row in summary:
        print(
            f"{row['lesson']:9s} {row['condition']:4s} {row['units']:5d} {row['prompt_chars']:7d} "
            f"{row['evidence_chars']:6d} {row['verbatim_step_title']:5d} "
            f"{row['verbatim_activity_what']:5d} {row['verbatim_step_content']:6d}"
        )
    print(f"\nwrote {out_root}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", default=None, help="run label (defaults to the fingerprint)")
    parser.add_argument("--lessons", nargs="*", default=None)
    args = parser.parse_args()
    return dump(args.label or fingerprint(), args.lessons)


if __name__ == "__main__":
    raise SystemExit(main())
