"""Verify seeded textbook_* tables against the project-local linked corpus.

Usage:
    cd apps/backend
    uv run python scripts/verify_seeded_textbook_records.py
    uv run python scripts/verify_seeded_textbook_records.py --packet packet-0001
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import TypedDict

from sqlalchemy import select

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app.db.metadata  # noqa: F401
from app.db.session import AsyncSessionLocal
from app.domains.expert_content.models import (
    TextbookPacket,
    TextbookRecord,
    TextbookRecordSubtopic,
)
from scripts.textbook_corpus_lib import build_expected_snapshot

REPORT_PATH = Path("/tmp/textbook_seed_verification_report.json")


class SnapshotReport(TypedDict):
    packet_ids: list[str]
    record_ids: list[str]
    record_subtopic_pairs: list[tuple[str, str]]
    packet_count: int
    record_count: int
    link_count: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--packet",
        help="Verify only one packet, for example packet-0001.",
    )
    return parser.parse_args()


async def build_actual_snapshot(packet_id: str | None = None) -> SnapshotReport:
    async with AsyncSessionLocal() as db:
        packet_stmt = select(TextbookPacket.packet_id)
        record_stmt = select(TextbookRecord.record_id)
        link_stmt = select(TextbookRecordSubtopic.record_id, TextbookRecordSubtopic.subtopic_id)

        if packet_id:
            packet_stmt = packet_stmt.where(TextbookPacket.packet_id == packet_id)
            record_stmt = record_stmt.where(TextbookRecord.packet_id == packet_id)
            link_stmt = link_stmt.join(
                TextbookRecord,
                TextbookRecord.record_id == TextbookRecordSubtopic.record_id,
            ).where(TextbookRecord.packet_id == packet_id)

        packet_ids = sorted((await db.execute(packet_stmt)).scalars().all())
        record_ids = sorted((await db.execute(record_stmt)).scalars().all())
        record_subtopic_pairs = sorted(
            (record_id, subtopic_id)
            for record_id, subtopic_id in (await db.execute(link_stmt)).all()
        )

    return {
        "packet_ids": packet_ids,
        "record_ids": record_ids,
        "record_subtopic_pairs": record_subtopic_pairs,
        "packet_count": len(packet_ids),
        "record_count": len(record_ids),
        "link_count": len(record_subtopic_pairs),
    }


async def main() -> None:
    args = parse_args()
    expected = build_expected_snapshot(packet_id=args.packet)
    actual = await build_actual_snapshot(packet_id=args.packet)

    report = {
        "status": "pass" if expected == actual else "fail",
        "packet_id": args.packet,
        "expected_packet_count": expected["packet_count"],
        "actual_packet_count": actual["packet_count"],
        "expected_record_count": expected["record_count"],
        "actual_record_count": actual["record_count"],
        "expected_link_count": expected["link_count"],
        "actual_link_count": actual["link_count"],
        "missing_packets": sorted(set(expected["packet_ids"]) - set(actual["packet_ids"])),
        "unexpected_packets": sorted(set(actual["packet_ids"]) - set(expected["packet_ids"])),
        "missing_records": sorted(set(expected["record_ids"]) - set(actual["record_ids"])),
        "unexpected_records": sorted(set(actual["record_ids"]) - set(expected["record_ids"])),
        "missing_record_subtopic_pairs": sorted(
            set(expected["record_subtopic_pairs"]) - set(actual["record_subtopic_pairs"])
        ),
        "unexpected_record_subtopic_pairs": sorted(
            set(actual["record_subtopic_pairs"]) - set(expected["record_subtopic_pairs"])
        ),
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

    if report["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
