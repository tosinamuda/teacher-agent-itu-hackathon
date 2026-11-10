"""Backfill curriculum_topics.term / week for JSS1 maths from the scheme of work.

The DB seed left JSS1 curriculum_topics.term='' and week=0 (only SS1 got terms),
so term/week is not queryable. dataset/processed/scheme-of-work/jss1_scheme.json
is the authoritative term/week source. This maps each scheme subtopic_id to its
topic (via curriculum_subtopics.topic_key) and sets the topic's term + week
(min week of its subtopics). Idempotent.

    uv run python scripts/backfill_jss1_terms.py            # apply
    uv run python scripts/backfill_jss1_terms.py --dry-run  # report only
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=False)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # apps/backend root

from sqlalchemy import text  # noqa: E402

from app.db.session import AsyncSessionLocal  # noqa: E402

SCHEME = Path(
    "/Users/dev/workspace/plan-to-tutor/dataset/processed/scheme-of-work/jss1_scheme.json"
)


def _scheme_subtopic_term_week() -> dict[str, tuple[str, int]]:
    data = json.loads(SCHEME.read_text(encoding="utf-8"))
    out: dict[str, tuple[str, int]] = {}
    for term, weeks in data.items():
        for entry in weeks:
            week = int(entry.get("week") or 0)
            for b in entry.get("breakdown", []):
                sid = b.get("subtopic_id")
                if sid and sid not in out:  # first (earliest) occurrence wins
                    out[sid] = (term, week)
    return out


async def main() -> int:
    dry = "--dry-run" in sys.argv
    sub_tw = _scheme_subtopic_term_week()
    async with AsyncSessionLocal() as db:
        # subtopic_id -> topic_key
        rows = (
            await db.execute(text("select subtopic_id, topic_key from curriculum_subtopics"))
        ).fetchall()
        sub_to_topic = {r[0]: r[1] for r in rows}

        # aggregate per topic: term (most common), min week
        topic_terms: dict[str, dict] = {}
        for sid, (term, week) in sub_tw.items():
            tk = sub_to_topic.get(sid)
            if tk is None:
                continue
            agg = topic_terms.setdefault(tk, {"terms": {}, "min_week": week})
            agg["terms"][term] = agg["terms"].get(term, 0) + 1
            agg["min_week"] = min(agg["min_week"], week)

        updated = 0
        for tk, agg in topic_terms.items():
            term = max(agg["terms"], key=agg["terms"].get)
            week = agg["min_week"]
            if dry:
                print(f"  {tk} -> term={term!r} week={week}")
                continue
            await db.execute(
                text(
                    "update curriculum_topics set term=:t, week=:w "
                    "where topic_key=:k and grade='JSS1'"
                ),
                {"t": term, "w": week, "k": tk},
            )
            updated += 1
        if not dry:
            await db.commit()
        print(f"{'DRY-RUN ' if dry else ''}topics mapped: {len(topic_terms)}; updated: {updated}")
        # verify
        chk = (
            await db.execute(
                text("select count(*) from curriculum_topics where grade='JSS1' and term <> ''")
            )
        ).scalar()
        print(f"JSS1 topics with non-empty term now: {chk}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
