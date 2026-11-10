"""Report which subtopics can be generated AUTHORITATIVELY from curated linkage.

"Authoritative" = build the lesson structure directly from the curated
ao_textbook_* rows (bypassing LLM KC/evidence derivation). A subtopic is
eligible only if the curated data alone is structurally clean enough to pass the
deterministic semantic checks — chiefly that no worked-example (modeling) record
is shared across distinct atomic objectives (the `reused_modeling_record` rule).

Tiers per subtopic:
  READY            - every AO grounded, every procedure-AO has its OWN modeling
                     record, no cross-AO modeling reuse, every grounded AO has an
                     assessment. Expect authoritative generation to pass.
  PARTIAL          - has grounded AOs but some AO lacks records / a procedure-AO
                     lacks a worked example / an assessment is missing. Usable but
                     incomplete (uncovered AOs would cold-start).
  MODELING_CONFLICT- a worked-example record is reused across AOs in the curated
                     data, so even authoritative drafting would trip
                     reused_modeling_record. Needs curation fix.
  NOT_ELIGIBLE     - no_records / zero grounded AOs. Pure cold-start (LLM path).

Usage:
    cd apps/backend && uv run python scripts/report_authoritative_coverage.py
"""

from __future__ import annotations

import asyncio
import sys
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select  # noqa: E402

from app.db.session import AsyncSessionLocal
from app.domains.expert_content.domain.types import AoTextbookLinkageStatus  # noqa: E402
from app.domains.expert_content.models import (  # noqa: E402
    AoTextbookLinkage,
    AoTextbookObjectiveLink,
    AoTextbookRecordLink,
)


async def _load() -> tuple[
    Sequence[AoTextbookLinkage],
    dict[str, list[AoTextbookObjectiveLink]],
    dict[tuple[str, str], list[AoTextbookRecordLink]],
]:
    async with AsyncSessionLocal() as db:
        linkages = (
            (await db.execute(select(AoTextbookLinkage).order_by(AoTextbookLinkage.subtopic_id)))
            .scalars()
            .all()
        )
        objectives = (await db.execute(select(AoTextbookObjectiveLink))).scalars().all()
        record_links = (await db.execute(select(AoTextbookRecordLink))).scalars().all()

    aos_by_subtopic: dict[str, list[AoTextbookObjectiveLink]] = {}
    for ao in objectives:
        aos_by_subtopic.setdefault(ao.subtopic_id, []).append(ao)

    links_by_ao: dict[tuple[str, str], list[AoTextbookRecordLink]] = {}
    for link in record_links:
        links_by_ao.setdefault((link.subtopic_id, link.ao_id), []).append(link)

    return linkages, aos_by_subtopic, links_by_ao


@dataclass(frozen=True)
class CoverageRow:
    """One linkage row's authoritative-coverage verdict."""

    subtopic_id: str
    status: AoTextbookLinkageStatus
    tier: str
    n_aos: int
    grounded: int
    with_modeling: int
    missing_assessment: int
    procedure_without_modeling: int
    reused_modeling: list[str]


def _classify(
    linkage: AoTextbookLinkage,
    aos: list[AoTextbookObjectiveLink],
    links_by_ao: dict[tuple[str, str], list[AoTextbookRecordLink]],
) -> CoverageRow:
    subtopic_id = linkage.subtopic_id
    n_aos = len(aos)
    grounded = 0
    with_modeling = 0
    with_assessment = 0
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
        if modeling:
            with_modeling += 1
            for record_id in modeling:
                modeling_usage[record_id] += 1
        # procedure = has practice but no worked example to model it
        if practice and not modeling:
            procedure_without_modeling += 1
        if ao.assessment:
            with_assessment += 1
        elif record_ids:
            missing_assessment += 1

    reused_modeling = sorted(r for r, c in modeling_usage.items() if c > 1)

    if grounded == 0:
        tier = "NOT_ELIGIBLE"
    elif reused_modeling:
        tier = "MODELING_CONFLICT"
    elif grounded == n_aos and missing_assessment == 0 and procedure_without_modeling == 0:
        tier = "READY"
    else:
        tier = "PARTIAL"

    return CoverageRow(
        subtopic_id=subtopic_id,
        status=linkage.status,
        tier=tier,
        n_aos=n_aos,
        grounded=grounded,
        with_modeling=with_modeling,
        missing_assessment=missing_assessment,
        procedure_without_modeling=procedure_without_modeling,
        reused_modeling=reused_modeling,
    )


async def main() -> int:
    linkages, aos_by_subtopic, links_by_ao = await _load()
    rows = [
        _classify(linkage, aos_by_subtopic.get(linkage.subtopic_id, []), links_by_ao)
        for linkage in linkages
    ]

    tiers = Counter(row.tier for row in rows)
    total = len(rows)
    print("=" * 78)
    print("AUTHORITATIVE COVERAGE REPORT")
    print("=" * 78)
    print(f"Linkage rows: {total}")
    for tier in ("READY", "PARTIAL", "MODELING_CONFLICT", "NOT_ELIGIBLE"):
        print(f"  {tier:18} {tiers.get(tier, 0)}")
    total_aos = sum(r.n_aos for r in rows)
    grounded_aos = sum(r.grounded for r in rows)
    modeling_aos = sum(r.with_modeling for r in rows)
    print(
        f"\nAOs: {total_aos} total | {grounded_aos} grounded | {modeling_aos} with worked-example"
    )

    for tier in ("MODELING_CONFLICT", "PARTIAL", "READY", "NOT_ELIGIBLE"):
        members = [r for r in rows if r.tier == tier]
        if not members:
            continue
        print(f"\n--- {tier} ({len(members)}) ---")
        for r in sorted(members, key=lambda x: x.subtopic_id):
            detail = f"AOs {r.grounded}/{r.n_aos} model={r.with_modeling}"
            if r.reused_modeling:
                detail += f" REUSED={r.reused_modeling}"
            if r.missing_assessment:
                detail += f" no_assess={r.missing_assessment}"
            if r.procedure_without_modeling:
                detail += f" proc_no_model={r.procedure_without_modeling}"
            print(f"  [{r.status.value:12}] {r.subtopic_id}  ({detail})")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
