"""Live progress from a job's process to whoever is watching, through one MySQL table.

A job runs in a process of its own, so what it reports has to cross processes to reach the
API's websocket. Each event is a row on a channel; a watcher reads the rows written after the
last one it saw. The id is auto-incremented, so it orders events exactly and tells a watcher
what is new. Events are for watching, not keeping: a day later they are deleted.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from sqlalchemy import BigInteger, String, delete, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.coltypes import JSON, MICROSECOND_DATETIME
from app.db.session import sync_engine
from app.shared.json_types import JsonObject
from app.shared.time import utc_now

logger = logging.getLogger(__name__)

#: How long an event is kept for a watcher that connects late.
_KEPT_FOR = timedelta(days=1)
#: Far longer than a one-row insert takes to commit.
_SETTLE = timedelta(seconds=1)


class ProgressEvent(Base):
    """One event reported on one channel."""

    __tablename__ = "progress_events"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    channel: Mapped[str] = mapped_column(String(128), index=True)
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(MICROSECOND_DATETIME, default=utc_now, index=True)


def publish(channel: str, event: JsonObject) -> None:
    """Report one event. Best effort: progress is never worth failing the work it reports."""
    try:
        with sync_engine.begin() as connection:
            connection.execute(
                insert(ProgressEvent).values(channel=channel, payload=event, created_at=utc_now())
            )
    except Exception:  # noqa: BLE001 - a lost progress event must not fail the job
        logger.warning("progress on %s was not recorded", channel, exc_info=True)


async def latest(session: AsyncSession, channel: str) -> int:
    """The id a watcher connecting now starts after: it sees only what comes next."""
    return (
        await session.scalar(
            select(func.coalesce(func.max(ProgressEvent.id), 0)).where(
                ProgressEvent.channel == channel
            )
        )
        or 0
    )


async def after(session: AsyncSession, channel: str, seen: int) -> list[tuple[int, JsonObject]]:
    """The channel's settled events written after ``seen``, oldest first.

    Two jobs reporting at once can commit out of id order, so an event is read only once it
    is a moment old: by then any event with a lower id has committed too, and none is skipped.
    """
    settled = utc_now() - _SETTLE
    rows = await session.execute(
        select(ProgressEvent.id, ProgressEvent.payload)
        .where(
            ProgressEvent.channel == channel,
            ProgressEvent.id > seen,
            ProgressEvent.created_at <= settled,
        )
        .order_by(ProgressEvent.id)
    )
    return [(event_id, payload) for event_id, payload in rows.tuples()]


async def forget_old(session: AsyncSession) -> None:
    """Delete events older than a day, on every channel."""
    await session.execute(
        delete(ProgressEvent).where(ProgressEvent.created_at < utc_now() - _KEPT_FOR)
    )
    await session.commit()
