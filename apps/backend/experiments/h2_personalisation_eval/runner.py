"""Run P0 and P1 for every transcribed learner, over the judged base packs.

P0 is the base pack unchanged — the C3 artefact from the clean-harness ladder run,
reused rather than regenerated, so the H2 base is a condition-run artefact with its
own judgments behind it. P1 personalises that same pack for one learner through the
production pipeline (`build_review_pack_personaliser`), with the learner's state
derived from their marked script and nothing else.

The run directory is written under this package and versioned by DVC. A run.json
carries pseudonymous student-NN ids and derived learner state; check a new run against
the five checks in ``apps/backend/.gitignore`` before ``dvc add``.

Each run has a folder of its own, `<label>-<UTC start>`. Each learner is saved as it
finishes, under `<run>/learners/`, and `--resume <run>` picks up where it stopped.
Nothing used to reach disk until all 26 were done, so a run interrupted at 11 learners
lost all eleven — an hour of calls that were already paid for.

    uv run python -m experiments.h2_personalisation_eval.runner --label h2-deepseek
    uv run python -m experiments.h2_personalisation_eval.runner --resume h2-20260925T183005Z
"""

from __future__ import annotations

import argparse
import ast
import asyncio
import json
from pathlib import Path

import dspy
from dotenv import load_dotenv

from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.generation_wiring import (
    build_review_pack_personaliser,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import profile_for
from app.infra.dspy_lm import set_model_override, set_sampling_override, transport_for
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.note_editorial import clean_plan
from experiments.h2_personalisation_eval.learner_states import states_for
from experiments.h2_personalisation_eval.students import LESSONS, load
from experiments.run_folders import add_run_arguments, open_run

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
H1_RUNS = HERE.parent / "h1_condition_eval" / "runs"

#: Where the base packs come from: the judged C3 packs of the clean-harness ladder.
#: Moved to `c0c3-prism-objective` on 2026-08-25 — the same arm re-run over the corrected
#: eval set, so `t3-w05`'s base is built from an objective that names the prism its note
#: teaches. The other five lessons' inputs are byte-identical between the two runs.
#:
#: The base is DeepSeek-generated whichever LM personalises it. That is the design, not a
#: confound: P0 is the base reused unchanged, so holding it fixed across generator arms is
#: what makes a P1 − P0 difference attributable to the personaliser rather than to whoever
#: wrote the pack underneath.
BASE_RUN = "c0c3-prism-objective"
BASE_CONDITION = "C3"
BASE_REPEAT = 1


def _configure(model: str) -> None:
    load_dotenv(override=False)
    set_model_override(model)
    set_sampling_override(cache=False, temperature=0.0)
    # The endpoint and the adapter come from the model's own record. Hardcoding DeepSeek's
    # pair here put gpt-oss on JSONAdapter with no schema to enforce it, and it invented a
    # block field on the tenth learner.
    dspy.configure(adapter=transport_for(model))


def _base_sections(lesson: str) -> list[ReviewPackSection]:
    run = json.loads((H1_RUNS / BASE_RUN / "run.json").read_text())
    case = next(
        c
        for c in run["cases"]
        if c["lesson"] == lesson
        and c["condition"] == BASE_CONDITION
        and c.get("repeat") == BASE_REPEAT
    )
    raw = case["sections_json"]
    sections = raw if isinstance(raw, list) else ast.literal_eval(raw)
    return [ReviewPackSection.model_validate(section) for section in sections]


def _plan(lesson: str) -> SessionPlanView:
    frozen = {c["lesson"]: c["plan"] for c in json.loads(EVAL_SET_PATH.read_text())["cases"]}
    runner_plan, _ = clean_plan({**frozen[lesson], "lesson_key": lesson})
    return SessionPlanView.model_validate(runner_plan)


#: Learners personalised at once. Every learner is an independent call over the same frozen
#: base, so the only reason this was ever serial is that nobody made it otherwise: 26 learners
#: took two hours at roughly five minutes each. DeepSeek allows 2,500 concurrent connections
#: per account on flash, and one learner is two or three section calls, so even the whole
#: cohort at once is under a hundred in flight. The default matches the H1 grid's gate rather
#: than the provider's ceiling, because the mantle gateway the gpt-oss arm uses publishes no
#: limit and this is shared credit.
DEFAULT_CONCURRENCY = 6


def _checkpoint(label: str, lesson: str, student_id: str) -> Path:
    return RUNS / label / "learners" / f"{lesson}.{student_id}.json"


def _identity(model: str) -> dict[str, object]:
    """What a checkpoint must match to be reused: the arm, and the pack it personalises."""
    return {
        "model": model,
        "base": {"run": BASE_RUN, "condition": BASE_CONDITION, "repeat": BASE_REPEAT},
    }


def _save(path: Path, model: str, rows: list[dict]) -> None:
    """Write one learner's rows the moment they exist, atomically.

    Through a temporary file and a rename, so a run killed mid-write leaves either the
    previous file or the new one, never half of either.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    scratch = path.with_suffix(".partial")
    scratch.write_text(json.dumps({**_identity(model), "rows": rows}, indent=1) + "\n")
    scratch.replace(path)


def _resume(path: Path, model: str) -> list[dict] | None:
    """A finished learner's rows, or None if this run has to generate them.

    A checkpoint from a different model or a different base pack is a different
    experiment's answer to the same question. Refused rather than reused: silently
    mixing two arms into one run is the failure this guards against, and it would be
    invisible in the result.
    """
    if not path.exists():
        return None
    saved = json.loads(path.read_text())
    if {key: saved.get(key) for key in _identity(model)} != _identity(model):
        raise SystemExit(
            f"{path.name} was generated by a different arm "
            f"({saved.get('model')}, base {saved.get('base')}). Delete "
            f"{path.parent} to regenerate, or run under a new --label."
        )
    return saved["rows"]


async def _one_learner(
    *,
    personaliser: object,
    lesson: str,
    plan: SessionPlanView,
    base: list[ReviewPackSection],
    base_dump: list[dict],
    sources: LessonSources,
    student: object,
    states: dict,
    policy: object,
    gate: asyncio.Semaphore,
    label: str,
    model: str,
) -> list[dict]:
    """This learner's P0 and P1 rows, in that order, saved before they are returned.

    P0 is the base reused unchanged, so it is a record of what was reused rather than
    anything generated; only P1 costs a call — and that call is what the checkpoint
    protects. A learner already on disk is returned without calling anything.
    """
    path = _checkpoint(label, lesson, student.id)
    if (done := _resume(path, model)) is not None:
        print(f"  {lesson} {student.id}: already done")
        return done

    dumped_states = {key: value.model_dump(mode="json") for key, value in states.items()}
    async with gate:
        pack = await personaliser.personalise(
            session_plan=plan,
            base_sections=base,
            learner_states=states,
            base_pack_id=f"{BASE_RUN}/{lesson}/{BASE_CONDITION}/r{BASE_REPEAT}",
            focal_learner_id=student.id,
            policy=policy,
            sources=sources,
        )
    personalisation = [outcome.model_dump(mode="json") for outcome in pack.personalisation]
    rows = [
        {
            "lesson": lesson,
            "student": student.id,
            "condition": "P0",
            "learner_states": dumped_states,
            "sections": base_dump,
            "personalisation": None,
        },
        {
            "lesson": lesson,
            "student": student.id,
            "condition": "P1",
            "learner_states": dumped_states,
            "sections": [section.model_dump(mode="json") for section in pack.sections],
            "personalisation": personalisation,
        },
    ]
    _save(path, model, rows)
    print(f"  {lesson} {student.id}: P1 outcomes {[o['outcome'] for o in personalisation]}")
    return rows


async def run(label: str, model: str, concurrency: int = DEFAULT_CONCURRENCY) -> Path:
    _configure(model)
    personaliser = build_review_pack_personaliser()
    policy = profile_for(Hypothesis.H2, ConditionCode.P1).generation_policy()
    gate = asyncio.Semaphore(concurrency)

    pending = []
    for lesson in LESSONS:
        classwork = load(lesson)
        plan = _plan(lesson)
        base = _base_sections(lesson)
        base_dump = [section.model_dump(mode="json") for section in base]
        sources = LessonSources.unresolved(plan.references)
        pending += [
            _one_learner(
                personaliser=personaliser,
                lesson=lesson,
                plan=plan,
                base=base,
                base_dump=base_dump,
                sources=sources,
                student=student,
                states=states_for(classwork, student),
                policy=policy,
                gate=gate,
                label=label,
                model=model,
            )
            for student in classwork.students
        ]

    # gather keeps its inputs' order, so the record is lesson-then-learner-then-condition
    # whatever order the calls actually finish in. Only the progress lines interleave.
    cases = [row for learner in await asyncio.gather(*pending) for row in learner]

    out = RUNS / label
    out.mkdir(parents=True, exist_ok=True)
    (out / "run.json").write_text(
        json.dumps(
            {
                "label": label,
                "model": model,
                "base": {"run": BASE_RUN, "condition": BASE_CONDITION, "repeat": BASE_REPEAT},
                "policy_condition": "P1",
                "cases": cases,
            },
            indent=1,
        )
        + "\n"
    )
    return out / "run.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_run_arguments(parser, stem_help="what this run is called (default h2)")
    parser.add_argument("--model", default="openai/deepseek-v4-flash")
    parser.add_argument(
        "--concurrency",
        type=int,
        default=DEFAULT_CONCURRENCY,
        help=f"learners personalised at once (default {DEFAULT_CONCURRENCY})",
    )
    args = parser.parse_args()
    label, _folder = open_run(RUNS, stem=args.label or "h2", resume=args.resume)
    path = asyncio.run(run(label, args.model, args.concurrency))
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
