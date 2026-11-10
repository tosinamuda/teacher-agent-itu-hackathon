"""Trace one engine draft on one harness: what reached the generator and what came back.

Run from ``apps/backend``, before any batch on a harness::

    uv run python -m experiments.lesson_note_engine.trace --harness opencode --plan-version <id>

With ``--seeded`` instead of ``--plan-version``, the lesson is the tests' two-step fractions
lesson, seeded in the arm's rolled-back transaction, on a database whose schema is created
from the ORM when it has none: for a machine without the lessons' database.

The engine arm writes one lesson's note through a proxy that keeps every exchange with the
generator's endpoint. The run folder holds each exchange as sent and received
(``exchanges.jsonl``), a summary to read (``summary.md``): the tools and part schema as sent,
the native tool calls as returned, the refusals the model was sent back; and what the note took.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path

from app.db.metadata import target_metadata
from app.db.session import engine as db_engine
from app.domains.content_engine.infrastructure.harness.choice import EngineLoop, SkillsMode
from app.infra.dspy_lm import build_dspy_lm, custom_endpoint
from app.shared.session_plan_view import SessionPlanView
from experiments.lesson_note_engine.engine_arm import engine_notes
from experiments.lesson_note_engine.run import _plan
from experiments.lesson_note_engine.trace_summary import summary
from experiments.lesson_note_engine.wire import Exchange, recording
from experiments.run_folders import open_run
from tests.content_engine_support import PLAN, SESSION_PLAN, seed_lesson

HERE = Path(__file__).parent


def _upstream() -> str:
    """The generator's host, before the proxy is put in front of it."""
    base = custom_endpoint("generator").get("api_base", "")
    if not base:
        raise SystemExit("the generator has no OpenAI-compatible endpoint to trace")
    return base.removesuffix("/v1")


def _write(folder: Path, exchanges: list[Exchange], measures: object) -> None:
    lines = [json.dumps(exchange.__dict__, ensure_ascii=False) for exchange in exchanges]
    (folder / "exchanges.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (folder / "measures.json").write_text(json.dumps(measures, indent=1), encoding="utf-8")
    (folder / "summary.md").write_text(summary(exchanges), encoding="utf-8")


async def _seeded() -> SessionPlanView:
    """The tests' lesson; the schema is created first where the database has none."""
    async with db_engine.begin() as connection:
        await connection.run_sync(target_metadata.create_all)
    return SessionPlanView.model_validate(SESSION_PLAN)


async def main(harness: EngineLoop, skills: SkillsMode, plan_version_id: str | None) -> None:
    upstream = _upstream()
    plan = await _plan(plan_version_id) if plan_version_id else await _seeded()
    prepare = None if plan_version_id else seed_lesson
    async with recording(upstream) as (proxy, base_url):
        os.environ["GENERATOR_API_BASE"] = base_url
        lm = build_dspy_lm()
        run = await engine_notes(
            plan, plan_version_id or PLAN, lm, harness=harness, skills=skills, prepare=prepare
        )
    label, folder = open_run(HERE / "runs", stem=f"trace-{harness.value}", resume=None)
    _write(folder, proxy.exchanges, run.measures)
    print(f"{label}: {len(proxy.exchanges)} exchanges; {run.measures}")
    print(f"read {folder / 'summary.md'}")
    await db_engine.dispose()


if __name__ == "__main__":
    from app.environment import prepare_environment

    prepare_environment()
    from app.dspy_setup import configure_dspy
    from app.infra.dspy_lm import set_sampling_override

    configure_dspy()
    # A cached reply replays an earlier sample, so a repeated run would look reproducible.
    set_sampling_override(cache=False)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harness", choices=[h.value for h in EngineLoop], required=True)
    parser.add_argument(
        "--skills", choices=[m.value for m in SkillsMode], default=SkillsMode.PINNED.value
    )
    lesson = parser.add_mutually_exclusive_group(required=True)
    lesson.add_argument("--plan-version", help="One lesson's plan version ID")
    lesson.add_argument("--seeded", action="store_true", help="The tests' two-step lesson")
    arguments = parser.parse_args()
    asyncio.run(
        main(EngineLoop(arguments.harness), SkillsMode(arguments.skills), arguments.plan_version)
    )
