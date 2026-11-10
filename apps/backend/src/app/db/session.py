"""Database engine and session factory (MySQL)."""

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.config import get_database_url, get_sync_database_url

DATABASE_URL = get_database_url()
SYNC_DATABASE_URL = get_sync_database_url()

_BASE_URL = make_url(DATABASE_URL)
ASYNC_DATABASE_URL = _BASE_URL.set(drivername="mysql+aiomysql")

# Async engine and session for FastAPI routes
# expire_on_commit=False prevents MissingGreenlet errors when accessing attributes after commit
engine = create_async_engine(ASYNC_DATABASE_URL, future=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)

# Sync engine and session for scripts, and for a job renewing its own claim
sync_engine = create_engine(SYNC_DATABASE_URL, future=True)
SessionLocal = sessionmaker(
    bind=sync_engine, autoflush=False, autocommit=False, future=True, expire_on_commit=False
)

# Imported here, after the engines, so every session this module hands out is guarded, and
# registers the drawings its flushes write.
from app.db import concluded_guard, figure_registration  # noqa: E402

concluded_guard.install()
figure_registration.install()
