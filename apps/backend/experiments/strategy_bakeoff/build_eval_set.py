"""Freeze the stratified evaluation set for the strategy bake-off.

Per the pre-registration (§5), the eval set is a FIXED, stratified list of JSS1
subtopics, chosen once and committed so runs cannot cherry-pick. Strata:

  * S1 grounded   — authoritative-READY subtopics (every AO grounded, no modeling
                    reuse, no missing assessment).
  * S2 partial    — has grounded AOs but at least one gap (ungrounded AO / no
                    worked example / missing assessment).
  * S3 no_records — curated but no textbook records (true cold-start).

Each selected subtopic is mapped to a LessonPeriod UUID (the generation entry
point; the ClassSession string-id path rejects on empty term). Selection is
DETERMINISTIC: candidates are sorted by subtopic_id and the first N taken, so
re-running yields the same set. The result is written to eval_set.json and should
be committed and treated as frozen (changes go through the deviation log).

Usage:
    cd apps/backend
    uv run python -m experiments.strategy_bakeoff.build_eval_set            # write
    uv run python -m experiments.strategy_bakeoff.build_eval_set --print    # preview
"""

from __future__ import annotations

import argparse
import asyncio
import json
from collections import Counter
from pathlib import Path

from sqlalchemy import select

import app.db.metadata  # noqa: F401  (registers all ORM models in the mapper registry)
from app.db.session import AsyncSessionLocal
from app.domains.expert_content.models import (
    AoTextbookLinkage,
    AoTextbookObjectiveLink,
    AoTextbookRecordLink,
)
from app.domains.teaching.models import LessonPeriod

# Frozen target sizes per stratum (pre-registration §5).
STRATUM_TARGETS = {"S1_grounded": 4, "S2_partial": 3, "S3_no_records": 2}

EVAL_SET_PATH = Path(__file__).resolve().parent / "eval_set.json"


def _classify(linkage, aos, links_by_ao) -> str:
    subtopic_id = linkage.subtopic_id
    if linkage.status == "no_records":
        return "S3_no_records"

    n_aos = len(aos)
    grounded = 0
    missing_assessment = 0
    procedure_without_modeling = 0
    modeling_usage: Counter[str] = Counter()
    for ao in aos:
        links = links_by_ao.get((subtopic_id, ao.ao_id), [])
        record_ids = [link.record_id for link in links]
        modeling = [link.record_id for link in links if link.role == "worked_example"]
        practice = [link.record_id for link in links if link.role == "exercise"] or list(
            ao.practice_record_ids or []
        )
        if record_ids:
            grounded += 1
        for record_id in modeling:
            modeling_usage[record_id] += 1
        if practice and not modeling:
            procedure_without_modeling += 1
        if ao.assessment:
            pass
        elif record_ids:
            missing_assessment += 1

    reused = any(count > 1 for count in modeling_usage.values())
    if grounded == 0:
        return "S3_no_records"
    if (
        grounded == n_aos
        and missing_assessment == 0
        and procedure_without_modeling == 0
        and not reused
    ):
        return "S1_grounded"
    return "S2_partial"


async def _load() -> tuple[list, dict, dict, dict]:
    async with AsyncSessionLocal() as db:
        linkages = (
            (await db.execute(select(AoTextbookLinkage).order_by(AoTextbookLinkage.subtopic_id)))
            .scalars()
            .all()
        )
        objectives = (await db.execute(select(AoTextbookObjectiveLink))).scalars().all()
        record_links = (await db.execute(select(AoTextbookRecordLink))).scalars().all()
        periods = (
            await db.execute(
                select(LessonPeriod.subtopic_id, LessonPeriod.id).order_by(LessonPeriod.id)
            )
        ).all()

    aos_by_subtopic: dict[str, list] = {}
    for ao in objectives:
        aos_by_subtopic.setdefault(ao.subtopic_id, []).append(ao)
    links_by_ao: dict[tuple[str, str], list] = {}
    for link in record_links:
        links_by_ao.setdefault((link.subtopic_id, link.ao_id), []).append(link)
    # First (lowest-id) period per subtopic, deterministic.
    period_by_subtopic: dict[str, str] = {}
    for subtopic_id, period_id in periods:
        if subtopic_id and subtopic_id not in period_by_subtopic:
            period_by_subtopic[subtopic_id] = str(period_id)

    return linkages, aos_by_subtopic, links_by_ao, period_by_subtopic


async def build(write: bool) -> dict:
    linkages, aos_by_subtopic, links_by_ao, period_by_subtopic = await _load()

    by_stratum: dict[str, list[dict]] = {key: [] for key in STRATUM_TARGETS}
    skipped_no_period: list[str] = []
    for linkage in linkages:
        subtopic_id = linkage.subtopic_id
        stratum = _classify(linkage, aos_by_subtopic.get(subtopic_id, []), links_by_ao)
        period_id = period_by_subtopic.get(subtopic_id)
        if period_id is None:
            # Generation needs a LessonPeriod; record but do not select.
            skipped_no_period.append(subtopic_id)
            continue
        by_stratum[stratum].append(
            {"subtopic_id": subtopic_id, "lesson_period_id": period_id, "status": linkage.status}
        )

    selected: dict[str, list[dict]] = {}
    for stratum, target in STRATUM_TARGETS.items():
        candidates = sorted(by_stratum[stratum], key=lambda row: row["subtopic_id"])
        selected[stratum] = candidates[:target]

    result = {
        "description": "Frozen stratified eval set for the lesson-plan strategy bake-off.",
        "generated_by": "experiments.strategy_bakeoff.build_eval_set",
        "stratum_targets": STRATUM_TARGETS,
        "available_per_stratum": {k: len(v) for k, v in by_stratum.items()},
        "selected": selected,
        "skipped_no_lesson_period_count": len(skipped_no_period),
    }

    if write:
        EVAL_SET_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print", action="store_true", help="Preview without writing.")
    args = parser.parse_args()
    result = asyncio.run(build(write=not args.print))
    available = result["available_per_stratum"]
    selected = result["selected"]
    print("Available per stratum:", available)
    for stratum, rows in selected.items():
        print(f"\n{stratum} ({len(rows)}/{STRATUM_TARGETS[stratum]}):")
        for row in rows:
            print(f"  {row['subtopic_id']}  [{row['status']}]  period={row['lesson_period_id']}")
    print(f"\nskipped (no lesson period): {result['skipped_no_lesson_period_count']}")
    if not args.print:
        print(f"\nWrote {EVAL_SET_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
