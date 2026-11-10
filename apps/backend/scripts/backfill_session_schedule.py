"""Backfill class_sessions.term / week from the scheme of work.

The JSS1 seed wrote term='' / week=0 on every ClassSession (only curriculum_topics
were later backfilled, by backfill_jss1_terms.py), leaving the 78 JSS1 sessions
ungenerable: SessionPlan requires term != '' and week >= 1, so /generate fails at
assembly. This applies the same per-subtopic scheme-of-work mapping the (now fixed)
seed uses to existing session rows. Idempotent.

    uv run python scripts/backfill_session_schedule.py            # apply
    uv run python scripts/backfill_session_schedule.py --dry-run  # report only
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=False)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # apps/backend root

from sqlalchemy import select  # noqa: E402

from app.db.session import AsyncSessionLocal  # noqa: E402
from app.domains.curriculum.models.curriculum import ClassSession  # noqa: E402
from scripts.seed_jss1_curriculum import (  # noqa: E402
    DATASET,
    build_subtopic_schedule,
    load_json_rows,
    load_scheme_data,
)


async def main() -> int:
    dry = "--dry-run" in sys.argv
    scheme_data = load_scheme_data()
    topics_data = load_json_rows(DATASET / "curriculum" / "jss1_topics_enriched.json")
    schedule = build_subtopic_schedule(scheme_data, topics_data)

    async with AsyncSessionLocal() as db:
        sessions = (await db.execute(select(ClassSession))).scalars().all()
        updated = 0
        for session in sessions:
            slot = schedule.get(session.subtopic_id)
            if slot is None:
                continue
            term, week = slot
            if session.term != term or session.week != week:
                if dry:
                    print(f"  {session.session_id} -> term={term!r} week={week}")
                else:
                    session.term = term
                    session.week = week
                updated += 1
        if not dry:
            await db.commit()
        remaining = (
            (await db.execute(select(ClassSession).where(ClassSession.term == ""))).scalars().all()
        )
        print(f"{'DRY-RUN ' if dry else ''}sessions updated: {updated}")
        print(f"sessions still with empty term: {len(remaining)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
