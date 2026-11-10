"""Generate a lesson's packs through the DeepSeek Harness, condition by condition.

A second generator for the same conditions: where `compose-v2` makes one
structured LM call per objective, this gives an agent a workspace, a shell and an
editor and asks for the whole pack as one file. Same model on the same endpoint,
so a comparison changes the harness and not the model.

What the agent is given is derived from the condition's own request, never
hand-written. `inputs/curriculum.json` is the lesson context C0 receives;
`inputs/lesson-plan.json` is what C1 adds and is absent under C0. An arm briefed
from a hand-written file measures the brief: asked for a pack against a
hand-written task, this harness produced 4 practice items to DSPy's 16-21, and
carrying the study's own `artefact_spec` verbatim moved it to 12.

    uv run --group harness python -m experiments.h1_condition_eval.harness_arm \
        --lesson t3-w02 --conditions C0 C1 --repeats 3 --label harness-t3w02
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from lxml import etree

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prompt_projection import (  # noqa: E501
    prompt_lesson,
    prompt_unit,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.variants import profiles_for_variant
from app.infra.dspy_lm import configured_model, custom_endpoint
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.config import RUNS_DIR
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.sections_document import (
    as_sections,
    content_errors,
    shape_errors,
)
from experiments.run_folders import add_run_arguments, open_run

#: Appended to the task per draw. Not part of the brief — the brief is
#: `task.md`, identical for every arm — but the one thing the agent cannot
#: discover reliably. Its shell starts in the workspace, so `ls` works; the
#: string-replace editor REFUSES a relative path and resolves an absolute one
#: against the real filesystem root, where "/sections.xml" is EROFS. Composing
#: `dsh-tool-str-replace-editor` over `dsh-fs-local` gives no sandbox root:
#: fs-local's `cwd` governs relative paths only, and the editor forbids those.
#: So the real path is stated rather than left to be guessed.
_WHERE_YOU_ARE = """

## Where you are working

Your workspace is `{workspace}`. Write the pack to
`{workspace}/sections.xml`, and read the inputs from
`{workspace}/inputs/`.

Give the editor tool absolute paths beginning with that directory. A bare
`/sections.xml` is the root of the machine, not of your workspace, and writing
there fails.
"""

HERE = Path(__file__).resolve().parent
HARNESS = HERE / "dsh-harness"
COPIED = ("task.md", "check_sections.py")


@dataclass(frozen=True)
class Draw:
    lesson: str
    condition: str
    repeat: int
    sections: list[dict[str, Any]]
    finish_reason: str
    problems: tuple[str, ...]


def _curriculum(request: ReviewPackRequest) -> dict[str, Any]:
    """The lesson as C0 has it: identity, and one entry per objective in order.

    `id` is the objective id the agent must put on each section, and the same id
    `check_sections.py` and the ingest grammar check against.
    """
    lesson = prompt_lesson(request.lesson_context)
    return {
        **{k: v for k, v in lesson.items() if k != "lesson_objectives"},
        "objectives": [
            {"id": str(unit.lesson_objective_id), "text": unit.objective_text or ""}
            for unit in request.units
        ],
    }


def _lesson_plan(request: ReviewPackRequest, baseline: ReviewPackRequest) -> dict[str, Any] | None:
    """Only what this condition adds to C0 — nothing if it adds nothing.

    Taking the difference rather than dumping the payload keeps the file honest:
    under C0 there is no plan and the agent is given no file, which is what the
    task's "if `inputs/lesson-plan.json` is present" is for.
    """
    base_lesson, lesson = (
        prompt_lesson(baseline.lesson_context),
        prompt_lesson(request.lesson_context),
    )
    extra_lesson = {k: v for k, v in lesson.items() if k not in base_lesson}
    steps = []
    for unit, base in zip(request.units, baseline.units, strict=True):
        projected, base_projected = prompt_unit(unit), prompt_unit(base)
        extra = {k: v for k, v in projected.items() if k not in base_projected}
        if extra:
            steps.append({"objective": str(unit.lesson_objective_id), **extra})
    if not extra_lesson and not steps:
        return None
    return {**extra_lesson, "steps": steps}


def _workspace(root: Path, request: ReviewPackRequest, baseline: ReviewPackRequest) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "inputs").mkdir(exist_ok=True)
    for name in COPIED:
        shutil.copy2(HARNESS / name, root / name)
    (root / "inputs" / "curriculum.json").write_text(
        json.dumps(_curriculum(request), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    plan = _lesson_plan(request, baseline)
    if plan is not None:
        (root / "inputs" / "lesson-plan.json").write_text(
            json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return root


def _requests(
    plan: SessionPlanView, codes: tuple[ConditionCode, ...], variant: str
) -> dict[ConditionCode, ReviewPackRequest]:
    profiles = profiles_for_variant(variant)
    builder = BaseReviewPackRequestBuilder(figures="source")
    return {
        code: builder.build(
            session_plan=plan,
            policy=profiles[code].generation_policy(),
            sources=LessonSources.unresolved(plan.references),
        )
        for code in codes
    }


def generate(
    *,
    lesson: str,
    plan: SessionPlanView,
    codes: tuple[ConditionCode, ...],
    repeats: int,
    variant: str,
    root: Path,
) -> list[Draw]:
    from deepseek_harness import DeepSeekHarness  # noqa: PLC0415 — optional dependency group

    connection = custom_endpoint("generator", configured_model("generator"))
    os.environ["BEDROCK_MANTLE_BASE_URL"] = str(connection["api_base"])
    os.environ["BEDROCK_MANTLE_API_KEY"] = str(connection["api_key"])
    requests = _requests(plan, (ConditionCode.C0, *codes), variant)
    task = (HARNESS / "task.md").read_text(encoding="utf-8")
    drawn: list[Draw] = []

    for repeat in range(1, repeats + 1):
        for code in codes:
            cell = root / "workspace" / code.value / f"draw-{repeat}"
            _workspace(cell, requests[code], requests[ConditionCode.C0])
            brief = task + _WHERE_YOU_ARE.format(workspace=cell)
            with DeepSeekHarness(
                provider="bedrock-mantle",
                model="openai.gpt-oss-120b",
                cwd=str(cell),
                session_root=str(root / "sessions"),
                cordis=str(HARNESS / "mantle.cordis.yml"),
                # `cwd` sets the agent's shell. It does NOT reach the plugins: the
                # sandbox policy, the editor and our check tool each read DSH_CWD and
                # fall back to the RUNTIME's cwd. Left unset they rooted at the repo,
                # so the editor resolved "/sections.xml" to the filesystem root and
                # returned EROFS, and check_sections looked for a pack that was never
                # there — its verdict was "does not exist yet" on every draw, so the
                # agent's own gate never once ran against its own output.
                env={"DSH_CWD": str(cell), "DSH_SESSION_ROOT": str(root / "sessions")},
            ) as harness:
                result = harness.run(brief, session_id=f"{lesson}-{code.value}-{repeat}")
            drawn.append(_ingest(lesson, code.value, repeat, cell, result.finish_reason))
            print(f"  {lesson} {code.value} draw {repeat}: {drawn[-1].problems or 'ok'}")
    return drawn


def _ingest(lesson: str, condition: str, repeat: int, cell: Path, finish: str) -> Draw:
    """Through the same gate a rater's pack must pass, refusing rather than repairing."""
    xml = cell / "sections.xml"
    if not xml.exists():
        return Draw(lesson, condition, repeat, [], finish, ("no sections.xml was written",))
    curriculum = json.loads((cell / "inputs" / "curriculum.json").read_text(encoding="utf-8"))
    objectives = [str(o["id"]) for o in curriculum["objectives"]]
    try:
        tree = etree.parse(str(xml))
    except etree.XMLSyntaxError as error:
        return Draw(
            lesson, condition, repeat, [], finish, (f"sections.xml will not parse: {error}",)
        )
    problems = tuple(shape_errors(tree)) or tuple(content_errors(tree, objectives))
    sections = [] if problems else as_sections(tree)
    return Draw(lesson, condition, repeat, sections, finish, problems)


def write_run(label: str, drawn: list[Draw], variant: str) -> Path:
    run_dir = RUNS_DIR / label
    run_dir.mkdir(parents=True, exist_ok=True)
    frozen = {c["lesson"]: c["plan_sha256"] for c in json.loads(EVAL_SET_PATH.read_text())["cases"]}
    cases = [
        {
            "lesson": d.lesson,
            "condition": d.condition,
            "repeat": d.repeat,
            "units": len(d.sections),
            "sections": len(d.sections),
            "sections_json": d.sections,
            "finish_reason": d.finish_reason,
            "ingest_problems": list(d.problems),
        }
        for d in drawn
        if d.sections
    ]
    (run_dir / "run.json").write_text(
        json.dumps(
            {
                "label": label,
                "arm": {
                    "model": configured_model("generator"),
                    "generator": "dsh-harness",
                    "harness": {"loop": "dsh-agent-spine", "framework": "deepseek-harness"},
                    "context_variant": variant,
                    "note_source": "n/a — the harness receives the condition payload, not notes",
                },
                "plans": {d.lesson: frozen[d.lesson] for d in drawn},
                "cases": cases,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return run_dir / "run.json"


def main() -> int:
    # Every entry point that resolves an endpoint loads the environment first; this
    # one did not, and failed on a missing key rather than on anything it was doing.
    load_dotenv(override=False)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lesson", required=True)
    parser.add_argument("--conditions", nargs="+", default=["C0", "C1"])
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--context-variant", default="v3")
    add_run_arguments(parser, stem_help="what this run is called")
    args = parser.parse_args()
    label, root = open_run(RUNS_DIR, stem=args.label or "harness", resume=args.resume)

    cases = {c["lesson"]: c for c in json.loads(EVAL_SET_PATH.read_text())["cases"]}
    plan = SessionPlanView.model_validate(cases[args.lesson]["plan"])
    codes = tuple(ConditionCode(c) for c in args.conditions)
    drawn = generate(
        lesson=args.lesson,
        plan=plan,
        codes=codes,
        repeats=args.repeats,
        variant=args.context_variant,
        root=root,
    )
    path = write_run(label, drawn, args.context_variant)
    kept = sum(1 for d in drawn if d.sections)
    print(f"\n  {kept}/{len(drawn)} draws ingested -> {path}")
    return 0 if kept == len(drawn) else 1


if __name__ == "__main__":
    raise SystemExit(main())
