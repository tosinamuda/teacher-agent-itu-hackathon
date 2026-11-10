"""Seed the record-level linked textbook corpus into textbook_* tables.

Usage:
    cd apps/backend
    uv run python scripts/seed_textbook_records.py
    uv run python scripts/seed_textbook_records.py --packet packet-0001
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app.db.metadata  # noqa: F401
from app.db.session import AsyncSessionLocal
from app.domains.expert_content.domain.types import TextbookSeedRunStatus
from app.domains.expert_content.models import (
    TextbookPacket,
    TextbookRecord,
    TextbookRecordSubtopic,
    TextbookSeedRun,
)
from scripts.textbook_corpus_lib import (
    build_expected_snapshot,
    iter_packets,
    linked_manifest_path,
    verify_corpus,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
logger = logging.getLogger(__name__)


def _coerce_text(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--packet",
        help="Seed only one packet, for example packet-0001.",
    )
    return parser.parse_args()


async def create_seed_run(packet_id: str | None, expected_record_count: int) -> uuid.UUID:
    seed_name = "textbook_records_seed"
    if packet_id:
        seed_name = f"{seed_name}:{packet_id}"

    async with AsyncSessionLocal() as db:
        run = TextbookSeedRun(
            seed_name=seed_name,
            source_manifest_path=str(linked_manifest_path()),
            source_record_count=expected_record_count,
            status=TextbookSeedRunStatus.STARTED,
            notes="Corpus verification passed. Seed run started.",
        )
        db.add(run)
        await db.commit()
        await db.refresh(run)
        return run.id


async def finalize_seed_run(
    seed_run_id: uuid.UUID,
    *,
    status: TextbookSeedRunStatus,
    inserted_packet_count: int,
    inserted_record_count: int,
    inserted_link_count: int,
    notes: str,
) -> None:
    async with AsyncSessionLocal() as db:
        run = await db.get(TextbookSeedRun, seed_run_id)
        if run is None:
            return
        run.status = status
        run.inserted_packet_count = inserted_packet_count
        run.inserted_record_count = inserted_record_count
        run.inserted_link_count = inserted_link_count
        run.completed_at = datetime.now(timezone.utc)
        run.notes = notes
        await db.commit()


class SeedCounts(NamedTuple):
    inserted_packets: int
    inserted_records: int
    inserted_links: int
    present_packets: int
    present_records: int
    present_links: int


async def _existing_keys(
    db: AsyncSession, packet_ids: list[str]
) -> tuple[set[str], set[str], set[tuple[str, str]]]:
    """Keys already in the DB for these packets, so the seed inserts only what's missing."""
    if not packet_ids:
        return set(), set(), set()
    packets = set(
        (
            await db.execute(
                select(TextbookPacket.packet_id).where(TextbookPacket.packet_id.in_(packet_ids))
            )
        ).scalars()
    )
    records = set(
        (
            await db.execute(
                select(TextbookRecord.record_id).where(TextbookRecord.packet_id.in_(packet_ids))
            )
        ).scalars()
    )
    link_rows = (
        await db.execute(
            select(TextbookRecordSubtopic.record_id, TextbookRecordSubtopic.subtopic_id)
            .join(TextbookRecord, TextbookRecordSubtopic.record_id == TextbookRecord.record_id)
            .where(TextbookRecord.packet_id.in_(packet_ids))
        )
    ).all()
    return packets, records, {(record_id, subtopic_id) for record_id, subtopic_id in link_rows}


async def _present_counts(db: AsyncSession, packet_ids: list[str]) -> tuple[int, int, int]:
    """Final DB row counts for these packets — verifies the corpus is fully present."""
    if not packet_ids:
        return 0, 0, 0
    packets = await db.scalar(
        select(func.count())
        .select_from(TextbookPacket)
        .where(TextbookPacket.packet_id.in_(packet_ids))
    )
    records = await db.scalar(
        select(func.count())
        .select_from(TextbookRecord)
        .where(TextbookRecord.packet_id.in_(packet_ids))
    )
    links = await db.scalar(
        select(func.count())
        .select_from(TextbookRecordSubtopic)
        .join(TextbookRecord, TextbookRecordSubtopic.record_id == TextbookRecord.record_id)
        .where(TextbookRecord.packet_id.in_(packet_ids))
    )
    return int(packets or 0), int(records or 0), int(links or 0)


async def seed_packets(db: AsyncSession, packet_id: str | None = None) -> SeedCounts:
    """Insert the corpus for these packets, skipping rows already present (idempotent).

    ``ao_textbook_record_links`` references ``textbook_records`` with ON DELETE RESTRICT,
    so a packet's records can't be removed once the later AO-linkage seed has linked them;
    the seed only adds what's missing, keeping a re-run on a live DB a clean no-op.
    """
    packets = iter_packets(packet_id=packet_id)
    packet_ids = [packet["packet_id"] for packet in packets]
    existing_packets, existing_records, existing_links = await _existing_keys(db, packet_ids)

    inserted_packet_count = 0
    inserted_record_count = 0
    inserted_link_count = 0

    for packet in packets:
        if packet["packet_id"] not in existing_packets:
            source_response_path = _coerce_text(
                packet.get("source_response_path") or packet["_source_path"]
            )
            db.add(
                TextbookPacket(
                    packet_id=packet["packet_id"],
                    source_response_path=source_response_path or "",
                    source_packet_manifest=_coerce_text(packet.get("source_packet_manifest")),
                    record_count=len(packet.get("records") or []),
                )
            )
            inserted_packet_count += 1

        for record in packet.get("records") or []:
            if record["record_id"] not in existing_records:
                db.add(
                    TextbookRecord(
                        record_id=record["record_id"],
                        packet_id=packet["packet_id"],
                        record_type=record["record_type"],
                        parent_block_id=record.get("parent_block_id"),
                        chapter_id=_coerce_text(record.get("chapter_id")),
                        chapter_title=_coerce_text(record.get("chapter_title")),
                        heading_path=record.get("heading_path"),
                        source_html_path=_coerce_text(record.get("source_html_path")),
                        source_anchor_id=_coerce_text(record.get("source_anchor_id")),
                        source_type_guess=_coerce_text(record.get("source_type_guess")),
                        raw_html=_coerce_text(record.get("raw_html")),
                        prompt_text=_coerce_text(record.get("prompt_text")),
                        answer_text=_coerce_text(record.get("answer_text")),
                        content_text=_coerce_text(record.get("content_text")),
                        retrieval_text=record["retrieval_text"],
                        visibility_default=_coerce_text(record.get("visibility_default")),
                        asset_refs=record.get("asset_refs"),
                        llm_review_status=_coerce_text(record.get("llm_review_status")),
                        llm_review_notes=record.get("llm_review_notes"),
                        primary_subtopic_id=_coerce_text(record["primary_subtopic_id"]) or "",
                        link_status=_coerce_text(record["link_status"]) or "",
                        link_notes=record.get("link_notes"),
                    )
                )
                inserted_record_count += 1

            for subtopic_id in record.get("subtopic_ids") or []:
                if (record["record_id"], subtopic_id) not in existing_links:
                    db.add(
                        TextbookRecordSubtopic(
                            record_id=record["record_id"],
                            subtopic_id=subtopic_id,
                            is_primary=subtopic_id == record["primary_subtopic_id"],
                        )
                    )
                    inserted_link_count += 1

    await db.commit()
    present_packets, present_records, present_links = await _present_counts(db, packet_ids)
    return SeedCounts(
        inserted_packet_count,
        inserted_record_count,
        inserted_link_count,
        present_packets,
        present_records,
        present_links,
    )


async def main() -> None:
    args = parse_args()
    report = verify_corpus(packet_id=args.packet)
    if report["status"] != "pass":
        raise SystemExit(f"Corpus verification failed: {report}")

    expected = build_expected_snapshot(packet_id=args.packet)
    seed_run_id = await create_seed_run(args.packet, expected["record_count"])

    try:
        async with AsyncSessionLocal() as db:
            counts = await seed_packets(db, packet_id=args.packet)
        # Insert-if-missing means a re-run inserts 0 rows, so verify the END state
        # (full corpus present), not how many rows this run happened to add.
        if counts.present_packets != expected["packet_count"]:
            raise RuntimeError(
                f"Packet count {counts.present_packets} != expected {expected['packet_count']}"
            )
        if counts.present_records != expected["record_count"]:
            raise RuntimeError(
                f"Record count {counts.present_records} != expected {expected['record_count']}"
            )
        if counts.present_links != expected["link_count"]:
            raise RuntimeError(
                f"Link count {counts.present_links} != expected {expected['link_count']}"
            )
    except Exception as exc:
        await finalize_seed_run(
            seed_run_id,
            status=TextbookSeedRunStatus.FAILED,
            inserted_packet_count=0,
            inserted_record_count=0,
            inserted_link_count=0,
            notes=f"Seed failed: {exc}",
        )
        raise

    await finalize_seed_run(
        seed_run_id,
        status=TextbookSeedRunStatus.COMPLETED,
        inserted_packet_count=counts.inserted_packets,
        inserted_record_count=counts.inserted_records,
        inserted_link_count=counts.inserted_links,
        notes="Seed completed successfully.",
    )
    logger.info(
        "Textbook corpus present: packets=%d records=%d links=%d "
        "(newly inserted this run: %d/%d/%d)",
        counts.present_packets,
        counts.present_records,
        counts.present_links,
        counts.inserted_packets,
        counts.inserted_records,
        counts.inserted_links,
    )


if __name__ == "__main__":
    asyncio.run(main())
