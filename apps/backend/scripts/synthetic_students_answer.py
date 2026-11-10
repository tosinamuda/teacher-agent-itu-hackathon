"""CLI wrapper: synthetic LLM students answer a lesson's exit diagnostic.

Thin wrapper over assessments.application.synthetic_student.answer_diagnostic (the same
core the browser-triggered Celery task uses).

Usage:  uv run python scripts/synthetic_students_answer.py <PLAN_VERSION_ID> [N] [class_id]
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app.db.metadata  # noqa: E402,F401  (load ORM models in order — dodges the import cycle)
from app.db.session import AsyncSessionLocal  # noqa: E402
from app.domains.assessments.application.synthetic_student import answer_diagnostic  # noqa: E402


async def main(plan_version_id: str, n_students: int, class_id: str | None) -> None:
    async with AsyncSessionLocal() as db:
        result = await answer_diagnostic(
            db, plan_version_id=plan_version_id, n_students=n_students, class_id=class_id
        )
        students = result.get("students")
        for entry in students if isinstance(students, list) else []:
            if isinstance(entry, dict):
                print(f"  {entry['student_id']}: {entry['correct']}/{entry['total']} correct")
        print(f"done — {result['created']} synthetic students answered the diagnostic")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: synthetic_students_answer.py <PLAN_VERSION_ID> [N] [class_id]")
        raise SystemExit(1)
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    cls = sys.argv[3] if len(sys.argv) > 3 else None
    asyncio.run(main(sys.argv[1], count, cls))
