"""Clear everything made for one lesson, to start it again from scratch.

Shows what would go and clears nothing unless `--yes` is given:

    uv run python scripts/reset_lesson.py <lesson id>
    uv run python scripts/reset_lesson.py <lesson id> --yes

The lesson, the class and its learners stay. A lesson the study ran on is refused.
The database is the one `DATABASE_URL` names.
"""

from __future__ import annotations

import argparse
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from app.domains.ops.application.lesson_reset import plan_reset, reset_lesson


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson_id", help="the lesson's id, with or without hyphens")
    parser.add_argument("--yes", action="store_true", help="clear it; without this nothing changes")
    args = parser.parse_args()
    lesson = args.lesson_id.replace("-", "")
    engine = create_engine(os.environ["DATABASE_URL"])
    with engine.begin() as conn:
        plan = plan_reset(conn, lesson)
        for table, count in sorted(plan.counts.items()):
            print(f"{count:6d}  {table}")
        print(f"{plan.total:6d}  rows in all")
        if plan.blocked:
            raise SystemExit("Not cleared: " + "; ".join(plan.blocked))
        if not args.yes:
            print("Nothing was cleared. Add --yes to clear these rows.")
            return
        reset_lesson(conn, lesson)
        print("Cleared.")


if __name__ == "__main__":
    main()
