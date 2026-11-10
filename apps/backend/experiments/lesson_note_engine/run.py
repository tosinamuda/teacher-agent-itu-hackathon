"""Run both arms over the frozen set and write the blinded review. See the package docstring."""

from __future__ import annotations

import argparse
import asyncio
import json
from dataclasses import dataclass
from pathlib import Path

import dspy
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.db.session import engine as db_engine
from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import PlanVersion
from app.domains.content_engine.infrastructure.harness.choice import EngineLoop, SkillsMode
from app.infra.dspy_lm import build_dspy_lm
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanStepView, SessionPlanView
from experiments.lesson_note_engine.current_arm import current_notes
from experiments.lesson_note_engine.engine_arm import (
    GENERATOR,
    PLUGIN,
    engine_notes,
    without_blocks,
)
from experiments.lesson_note_engine.review import blinded
from experiments.lesson_note_engine.teacher_arm import teacher_notes
from experiments.run_folders import add_run_arguments, open_run

HERE = Path(__file__).parent
SEED = 20260926


async def _plan(plan_version_id: str) -> SessionPlanView:
    async with AsyncSessionLocal() as db:
        stored = await db.scalar(
            select(PlanVersion.session_plan).where(PlanVersion.version_id == plan_version_id)
        )
    if stored is None:
        raise SystemExit(f"there is no plan version {plan_version_id}")
    return SessionPlanView.model_validate(stored)


def _step(plan: SessionPlanView, step: SessionPlanStepView) -> JsonObject:
    """A step as a reviewer reads it beside its notes: what it teaches and what happens."""
    objectives = {o.lesson_objective_id: o.objective_text for o in plan.lesson_plan_objectives}
    return {
        "step_id": step.step_id,
        "title": step.title or "",
        "kind": step.step_kind,
        "objective": objectives.get(step.lesson_objective_id or "") or "",
        "activities": [*step.activities],
    }


@dataclass(frozen=True)
class Condition:
    """What a run changes: the engine's candidate, the plan's blocks, and arm A's source."""

    #: An earlier run whose arm A notes this run reuses, when arm A is unchanged.
    earlier: Path | None = None
    #: The engine's candidate type and spec as JSON, for the older ablations.
    candidate: JsonObject | None = None
    #: The plugin whose type the engine writes; the lesson-note plugin when not given.
    plugin: Path = PLUGIN
    #: The generator of that plugin the engine writes with.
    generator: str = GENERATOR
    #: Whether both arms read the plan's blocks.
    blocks: bool = True
    #: The loop the engine's writer and checker run on.
    harness: EngineLoop = EngineLoop.DSPY
    #: Where the engine's writer gets the skills its type pins.
    skills: SkillsMode = SkillsMode.PINNED


async def _current(
    plan: SessionPlanView, plan_version_id: str, lm: dspy.BaseLM, earlier: Path | None
) -> JsonObject:
    """Arm A's notes: written now, or taken from an earlier run of the same generator."""
    written = earlier / f"{plan_version_id}.json" if earlier is not None else None
    if written is None or not written.exists():
        return {**await current_notes(plan, plan_version_id, lm)}
    return json.loads(written.read_text(encoding="utf-8"))["notes"]["current"]


async def _lesson(plan_version_id: str, folder: Path, condition: Condition) -> JsonObject:
    """Both arms' notes for one lesson, kept in the run folder so a resumed run skips it."""
    done = folder / f"{plan_version_id}.json"
    if done.exists():
        return json.loads(done.read_text(encoding="utf-8"))
    full = await _plan(plan_version_id)
    plan = full if condition.blocks else without_blocks(full)
    lm = build_dspy_lm()
    engine = await engine_notes(
        plan,
        plan_version_id,
        lm,
        candidate=condition.candidate,
        plugin=condition.plugin,
        generator=condition.generator,
        blocks=condition.blocks,
        harness=condition.harness,
        skills=condition.skills,
    )
    notes: JsonObject = {
        "engine": {**engine.notes},
        "current": await _current(plan, plan_version_id, lm, condition.earlier),
    }
    if teacher := await teacher_notes(plan_version_id):
        notes["teacher"] = {**teacher}
    lesson: JsonObject = {
        "plan_version_id": plan_version_id,
        "title": plan.title or plan.topic or plan_version_id,
        "context": {"subject": plan.subject, "grade": plan.grade, "topic": plan.topic},
        "steps": [_step(plan, step) for step in plan.steps],
        "notes": notes,
        "current_from": condition.earlier.name if condition.earlier is not None else None,
        "blocks": condition.blocks,
        "engine_run": engine.measures,
    }
    done.write_text(json.dumps(lesson, indent=1, ensure_ascii=False), encoding="utf-8")
    return lesson


async def main(label: str, resume: str | None, frozen: str, condition: Condition) -> None:
    plan_version_ids = json.loads((HERE / frozen).read_text())["plan_version_ids"]
    run_label, folder = open_run(HERE / "runs", stem=label, resume=resume)
    lessons = []
    try:
        for plan_version_id in plan_version_ids:
            lessons.append(await _lesson(plan_version_id, folder, condition))
            print(
                f"{plan_version_id}: both arms written; engine {lessons[-1]['engine_run']}",
                flush=True,
            )
    finally:
        await db_engine.dispose()
    items, key = blinded(lessons, SEED)
    (folder / "review.json").write_text(json.dumps(items, indent=1, ensure_ascii=False))
    (folder / "key.json").write_text(json.dumps(key, indent=1))
    print(f"{run_label}: {len(items)} steps to review in {folder / 'review.json'}")


if __name__ == "__main__":
    from app.environment import prepare_environment

    prepare_environment()
    from app.dspy_setup import configure_dspy
    from app.infra.dspy_lm import set_sampling_override

    configure_dspy()
    # A cached reply replays an earlier sample, so a repeated run would look reproducible.
    set_sampling_override(cache=False)
    parser = argparse.ArgumentParser(description=__doc__)
    add_run_arguments(parser, stem_help="What this run compares, e.g. pre.")
    parser.add_argument(
        "--current-from",
        help="A run whose current-generator notes to reuse, when only the engine arm changed",
    )
    parser.add_argument(
        "--frozen",
        default="frozen_set.json",
        help="The lesson set to run, e.g. frozen_set_study.json for the teachers' own lessons",
    )
    parser.add_argument("--candidate", help="The engine's candidate file, in this package")
    parser.add_argument(
        "--plugin", type=Path, default=PLUGIN, help="The plugin folder whose type the engine writes"
    )
    parser.add_argument(
        "--generator", default=GENERATOR, help="The generator of that plugin the engine writes with"
    )
    parser.add_argument(
        "--harness",
        choices=[harness.value for harness in EngineLoop],
        default=EngineLoop.DSPY.value,
        help="The loop the engine's writer and checker run on",
    )
    parser.add_argument(
        "--skills",
        choices=[mode.value for mode in SkillsMode],
        default=SkillsMode.PINNED.value,
        help="Whether the writer gets its skills in the brief, or as files its harness loads",
    )
    parser.add_argument(
        "--without-blocks",
        action="store_true",
        help="Hide the plan's blocks from both arms, so neither sees content the plan carries",
    )
    arguments = parser.parse_args()
    condition = Condition(
        earlier=HERE / "runs" / arguments.current_from if arguments.current_from else None,
        candidate=(
            json.loads((HERE / arguments.candidate).read_text(encoding="utf-8"))
            if arguments.candidate
            else None
        ),
        plugin=arguments.plugin,
        generator=arguments.generator,
        blocks=not arguments.without_blocks,
        harness=EngineLoop(arguments.harness),
        skills=SkillsMode(arguments.skills),
    )
    asyncio.run(main(arguments.label or "compare", arguments.resume, arguments.frozen, condition))
