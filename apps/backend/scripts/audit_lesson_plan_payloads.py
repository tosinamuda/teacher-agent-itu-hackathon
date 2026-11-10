from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING, cast

from sqlalchemy import create_engine, text

from app.shared.json_types import JsonObject

if TYPE_CHECKING:
    from migrations.data.lesson_plan_payload_repairs import PlanVersionPayloadSnapshot

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


DEFAULT_AUDIT_PATH = Path("migrations/data/records/lesson_plan_payload_audit.json")
DEFAULT_REPAIRS_PATH = Path("migrations/data/records/lesson_plan_payload_repairs.jsonl")


def _json_object(value: object) -> JsonObject:
    if not isinstance(value, dict):
        return {}
    return cast(JsonObject, value)


def _json_rows(value: object) -> list[JsonObject]:
    if not isinstance(value, list):
        return []
    return cast(list[JsonObject], [row for row in value if isinstance(row, dict)])


def _json_int(value: object) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def _load_snapshots(database_url: str) -> list[PlanVersionPayloadSnapshot]:
    from migrations.data.lesson_plan_payload_repairs import (
        PlanVersionPayloadSnapshot,
    )

    engine = create_engine(database_url)
    snapshots: list[PlanVersionPayloadSnapshot] = []
    with engine.begin() as connection:
        result = connection.execute(
            text(
                """
                SELECT version_id, plan_id, session_plan
                FROM plan_versions
                ORDER BY created_at, version_id
                """
            )
        )
        for row in result:
            session_plan = row.session_plan
            if isinstance(session_plan, str):
                session_plan = json.loads(session_plan)
            snapshots.append(
                PlanVersionPayloadSnapshot(
                    version_id=str(row.version_id),
                    plan_id=str(row.plan_id),
                    session_plan=session_plan or {},
                )
            )
    return snapshots


def _apply(database_url: str) -> None:
    from migrations.data.lesson_plan_payload_repairs import apply_payload_repairs

    engine = create_engine(database_url)
    with engine.begin() as connection:
        applied = apply_payload_repairs(connection)
    print(
        json.dumps(
            {
                "applied_rows": len(applied),
                "applied_version_ids": [record.version_id for record in applied],
            },
            indent=2,
        )
    )


def main() -> None:
    from app.db.config import get_database_url
    from migrations.data.lesson_plan_payload_repairs import (
        build_audit_report,
        repair_session_plan_snapshot,
        write_payload_repairs_jsonl,
    )

    parser = argparse.ArgumentParser(
        description="Audit stored lesson plan payloads and generate strict repair records.",
    )
    parser.add_argument("--database-url", default=get_database_url())
    parser.add_argument("--audit-path", default=str(DEFAULT_AUDIT_PATH))
    parser.add_argument("--repairs-path", default=str(DEFAULT_REPAIRS_PATH))
    parser.add_argument(
        "--apply",
        action="store_true",
        help=(
            "Repair invalid payloads in the database in place (idempotent, derived "
            "from current rows) instead of writing the audit/repair provenance files."
        ),
    )
    args = parser.parse_args()

    if args.apply:
        _apply(args.database_url)
        return

    snapshots = _load_snapshots(args.database_url)
    audit_report = build_audit_report(snapshots)
    summary = _json_object(audit_report.get("summary"))
    invalid_rows = _json_rows(audit_report.get("invalid_rows"))
    invalid_version_ids = {str(row["version_id"]) for row in invalid_rows}
    repair_records = [
        repair_session_plan_snapshot(snapshot)
        for snapshot in snapshots
        if snapshot.version_id in invalid_version_ids
    ]

    audit_path = Path(args.audit_path)
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.write_text(
        json.dumps(audit_report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    write_payload_repairs_jsonl(repair_records, args.repairs_path)

    print(
        json.dumps(
            {
                "audit_path": str(audit_path),
                "repairs_path": str(args.repairs_path),
                "total_rows": _json_int(summary.get("total_rows")),
                "invalid_rows": _json_int(summary.get("invalid_rows")),
                "repair_rows": len(repair_records),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
