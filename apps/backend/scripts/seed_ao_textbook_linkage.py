"""Seed the manual AO->textbook linkage rows into the ao_textbook_* tables.

The lesson-plan pipeline grounds on these expert-validated links instead of
BM25 retrieval. Links are seeded per atomic objective: an AO with no record
links is simply absent (the pipeline cold-starts it from curriculum text).

Validation gate (per the project rule: deterministic, no hacks):
  - the row parses with the expected current schema, and
  - every referenced subtopic_id and record_id exists in the database.
Rows / links that fail are reported and skipped, never silently dropped.

Usage:
    cd apps/backend
    # offline structural check, no DB needed:
    uv run python scripts/seed_ao_textbook_linkage.py --validate-only
    # seed everything (MySQL up, textbook records already seeded):
    uv run python scripts/seed_ao_textbook_linkage.py
    # seed a single subtopic:
    uv run python scripts/seed_ao_textbook_linkage.py --subtopic <subtopic_id>
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
logger = logging.getLogger(__name__)

_SKIP_FILENAMES = {"manifest.json", "review_triage.json"}
_VALID_STATUS = {"mapped", "needs_review", "no_records"}
_VALID_ROLE = {"foundation", "instruction", "worked_example", "exercise"}
_VALID_METHOD = {"rule_type", "rule_heading", "judgment"}


def _project_root() -> Path:
    return Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[3]))


def default_source_dir() -> Path:
    return _project_root() / "dataset" / "processed" / "ao_textbook_linkage" / "manual"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-dir",
        default=str(default_source_dir()),
        help="Directory of manual linkage row JSON files.",
    )
    parser.add_argument(
        "--subtopic",
        default=None,
        help="Seed/validate only this subtopic_id.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Structural validation only. No database access (runs offline).",
    )
    return parser.parse_args()


def iter_row_paths(source_dir: Path, subtopic: str | None) -> list[Path]:
    paths: list[Path] = []
    for path in sorted(source_dir.glob("*.json")):
        if path.name in _SKIP_FILENAMES:
            continue
        if subtopic and path.stem != subtopic:
            continue
        paths.append(path)
    return paths


class RowReport:
    """Structural findings for one linkage row."""

    def __init__(self, subtopic_id: str, status: str | None) -> None:
        self.subtopic_id = subtopic_id
        self.status = status
        self.errors: list[str] = []
        self.objective_count = 0
        self.linked_objective_count = 0
        self.record_link_count = 0
        self.referenced_record_ids: set[str] = set()

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_row_structure(payload: dict[str, Any]) -> RowReport:
    """Validate the parts of a linkage row that we persist. No DB."""
    subtopic_id = str(payload.get("subtopic_id") or "").strip()
    status = payload.get("status")
    report = RowReport(subtopic_id, status if isinstance(status, str) else None)

    if not subtopic_id:
        report.errors.append("missing subtopic_id")
    if not str(payload.get("subtopic_title") or "").strip():
        report.errors.append("missing subtopic_title")
    if status not in _VALID_STATUS:
        report.errors.append(f"invalid status: {status!r}")

    atomic_objectives = payload.get("atomic_objectives")
    if not isinstance(atomic_objectives, list):
        report.errors.append("atomic_objectives is not a list")
        atomic_objectives = []

    seen_ao_ids: set[str] = set()
    for index, atomic_objective in enumerate(atomic_objectives):
        if not isinstance(atomic_objective, dict):
            report.errors.append(f"atomic_objectives[{index}] is not an object")
            continue
        report.objective_count += 1
        ao_id = str(atomic_objective.get("ao_id") or "").strip()
        if not ao_id:
            report.errors.append(f"atomic_objectives[{index}] missing ao_id")
        elif ao_id in seen_ao_ids:
            report.errors.append(f"duplicate ao_id: {ao_id}")
        else:
            seen_ao_ids.add(ao_id)

        record_links = atomic_objective.get("record_links")
        if record_links is None:
            record_links = []
        if not isinstance(record_links, list):
            report.errors.append(f"{ao_id or index}: record_links is not a list")
            record_links = []

        if record_links:
            report.linked_objective_count += 1
        for link_index, link in enumerate(record_links):
            if not isinstance(link, dict):
                report.errors.append(f"{ao_id}: record_links[{link_index}] is not an object")
                continue
            record_id = str(link.get("record_id") or "").strip()
            role = link.get("role")
            method = link.get("method")
            if not record_id:
                report.errors.append(f"{ao_id}: record_link missing record_id")
            else:
                report.referenced_record_ids.add(record_id)
            if role not in _VALID_ROLE:
                report.errors.append(f"{ao_id}: invalid role {role!r}")
            if method not in _VALID_METHOD:
                report.errors.append(f"{ao_id}: invalid method {method!r}")
            report.record_link_count += 1

    return report


def load_row(path: Path) -> dict[str, Any]:
    row = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(row, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return row


def run_validate_only(paths: list[Path]) -> int:
    total = len(paths)
    ok_rows = 0
    total_objectives = 0
    total_linked_objectives = 0
    total_record_links = 0
    failures: list[RowReport] = []

    for path in paths:
        try:
            payload = load_row(path)
        except Exception as exc:  # noqa: BLE001 - report and continue
            logger.error("%s: could not parse JSON: %s", path.name, exc)
            total -= 1
            continue
        report = validate_row_structure(payload)
        total_objectives += report.objective_count
        total_linked_objectives += report.linked_objective_count
        total_record_links += report.record_link_count
        if report.ok:
            ok_rows += 1
        else:
            failures.append(report)

    logger.info("Rows checked:            %d", total)
    logger.info("Structurally valid:      %d", ok_rows)
    logger.info("With errors:             %d", len(failures))
    logger.info("Atomic objectives:       %d", total_objectives)
    logger.info("AOs with >=1 link:       %d", total_linked_objectives)
    logger.info("Record links:            %d", total_record_links)
    for report in failures:
        logger.warning("FAIL %s [%s]", report.subtopic_id, report.status)
        for error in report.errors[:10]:
            logger.warning("     - %s", error)
    return 0 if not failures else 1


async def run_seed(paths: list[Path], source_dir: Path) -> int:
    from datetime import datetime, timezone

    from sqlalchemy import delete, select

    import app.db.metadata  # noqa: F401 - register models
    from app.db.session import AsyncSessionLocal
    from app.domains.curriculum.models.curriculum import CurriculumSubtopic
    from app.domains.expert_content.domain.types import AoTextbookLinkageSeedRunStatus
    from app.domains.expert_content.models import (
        AoTextbookLinkage,
        AoTextbookLinkageSeedRun,
        AoTextbookObjectiveLink,
        AoTextbookRecordLink,
        TextbookRecord,
    )

    rows: list[tuple[dict[str, Any], RowReport]] = []
    for path in paths:
        try:
            payload = load_row(path)
        except Exception as exc:  # noqa: BLE001
            logger.error("%s: could not parse JSON: %s", path.name, exc)
            continue
        report = validate_row_structure(payload)
        if not report.ok:
            logger.warning(
                "Skipping %s (structural errors): %s",
                report.subtopic_id,
                report.errors[:5],
            )
            continue
        rows.append((payload, report))

    async with AsyncSessionLocal() as db:
        known_subtopics = set(
            (await db.execute(select(CurriculumSubtopic.subtopic_id))).scalars().all()
        )
        known_records = set((await db.execute(select(TextbookRecord.record_id))).scalars().all())

        seed_run = AoTextbookLinkageSeedRun(
            seed_name="ao_textbook_linkage_seed",
            source_dir=str(source_dir),
            source_row_count=len(paths),
            status="started",
        )
        db.add(seed_run)
        await db.commit()
        await db.refresh(seed_run)
        seed_run_id = seed_run.id

        inserted_linkages = 0
        inserted_objectives = 0
        inserted_record_links = 0
        skipped = 0

        try:
            for payload, report in rows:
                subtopic_id = report.subtopic_id
                if subtopic_id not in known_subtopics:
                    logger.warning("Skipping %s: subtopic_id not in curriculum", subtopic_id)
                    skipped += 1
                    continue
                missing_records = sorted(report.referenced_record_ids - known_records)
                if missing_records:
                    logger.warning(
                        "Skipping %s: %d referenced record(s) not seeded, e.g. %s",
                        subtopic_id,
                        len(missing_records),
                        missing_records[:3],
                    )
                    skipped += 1
                    continue

                await db.execute(
                    delete(AoTextbookLinkage).where(AoTextbookLinkage.subtopic_id == subtopic_id)
                )
                await db.flush()

                db.add(
                    AoTextbookLinkage(
                        subtopic_id=subtopic_id,
                        subtopic_title=str(payload.get("subtopic_title") or ""),
                        status=str(payload.get("status")),
                        status_reasons=payload.get("status_reasons"),
                        review_categories=payload.get("review_categories"),
                        shared_foundation_record_ids=payload.get("shared_foundation_record_ids"),
                        source_set="manual",
                    )
                )
                inserted_linkages += 1

                for atomic_objective in payload.get("atomic_objectives") or []:
                    ao_id = str(atomic_objective.get("ao_id") or "").strip()
                    db.add(
                        AoTextbookObjectiveLink(
                            subtopic_id=subtopic_id,
                            ao_id=ao_id,
                            ao_order=int(atomic_objective.get("ao_order") or 0),
                            curriculum_objective_id=str(
                                atomic_objective.get("curriculum_objective_id") or ""
                            ),
                            curriculum_objective_text=str(
                                atomic_objective.get("curriculum_objective_text") or ""
                            ),
                            objective_text=str(atomic_objective.get("text") or ""),
                            bloom_verb=str(atomic_objective.get("bloom_verb") or ""),
                            bloom_level=str(atomic_objective.get("bloom_level") or ""),
                            evidence_classification=(
                                str(atomic_objective.get("evidence_classification"))
                                if atomic_objective.get("evidence_classification") is not None
                                else None
                            ),
                            step_blueprint=atomic_objective.get("step_blueprint"),
                            practice_record_ids=atomic_objective.get("practice_record_ids"),
                            assessment=atomic_objective.get("assessment"),
                        )
                    )
                    inserted_objectives += 1
                    await db.flush()

                    for link_order, link in enumerate(atomic_objective.get("record_links") or []):
                        db.add(
                            AoTextbookRecordLink(
                                subtopic_id=subtopic_id,
                                ao_id=ao_id,
                                record_id=str(link.get("record_id") or ""),
                                role=str(link.get("role")),
                                method=str(link.get("method")),
                                rationale=link.get("rationale"),
                                link_order=link_order,
                            )
                        )
                        inserted_record_links += 1

            await db.commit()
        except Exception as exc:  # noqa: BLE001
            await db.rollback()
            run = await db.get(AoTextbookLinkageSeedRun, seed_run_id)
            if run is not None:
                run.status = AoTextbookLinkageSeedRunStatus.FAILED
                run.completed_at = datetime.now(timezone.utc)
                run.notes = f"Seed failed: {exc}"
                await db.commit()
            raise

        run = await db.get(AoTextbookLinkageSeedRun, seed_run_id)
        if run is not None:
            run.status = AoTextbookLinkageSeedRunStatus.COMPLETED
            run.completed_at = datetime.now(timezone.utc)
            run.inserted_linkage_count = inserted_linkages
            run.inserted_objective_count = inserted_objectives
            run.inserted_record_link_count = inserted_record_links
            run.skipped_row_count = skipped
            run.notes = "Seed completed successfully."
            await db.commit()

    logger.info(
        "Seeded AO linkage: linkages=%d objectives=%d record_links=%d skipped=%d",
        inserted_linkages,
        inserted_objectives,
        inserted_record_links,
        skipped,
    )
    return 0


def main() -> int:
    args = parse_args()
    source_dir = Path(args.source_dir)
    if not source_dir.is_dir():
        logger.error("Source directory not found: %s", source_dir)
        return 2
    paths = iter_row_paths(source_dir, args.subtopic)
    if not paths:
        logger.error("No linkage rows found in %s", source_dir)
        return 2

    if args.validate_only:
        return run_validate_only(paths)

    import asyncio

    return asyncio.run(run_seed(paths, source_dir))


if __name__ == "__main__":
    raise SystemExit(main())
