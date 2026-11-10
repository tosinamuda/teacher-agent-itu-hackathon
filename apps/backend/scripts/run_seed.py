"""Legacy alias for the optional demo workspace seed."""

import asyncio
import logging
import sys

from app.bootstrap import SyntheticDataSeeder
from app.db.default_school import ensure_default_school
from app.db.metadata import target_metadata  # noqa: F401
from app.db.session import AsyncSessionLocal

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


async def main() -> None:
    async with AsyncSessionLocal() as db:
        await ensure_default_school(session=db)
        seeder = SyntheticDataSeeder(db)
        await seeder.seed()
        print("Demo seed completed.")


if __name__ == "__main__":
    asyncio.run(main())
