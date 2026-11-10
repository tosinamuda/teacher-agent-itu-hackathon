"""Seed optional demo-only workspace data.

This does not define the canonical JSS1 Mathematics baseline. Use
`scripts/seed_jss1_curriculum.py` for the research baseline.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.bootstrap import SyntheticDataSeeder
from app.db.default_school import ensure_default_school
from app.db.metadata import target_metadata  # noqa: F401
from app.db.session import AsyncSessionLocal


async def main() -> None:
    async with AsyncSessionLocal() as db:
        await ensure_default_school(session=db)
        seeder = SyntheticDataSeeder(db)
        await seeder.seed()
        print("Demo workspace seed completed.")


if __name__ == "__main__":
    asyncio.run(main())
