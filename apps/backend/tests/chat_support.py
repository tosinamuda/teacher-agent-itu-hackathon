"""A chat feed over a test's own database session, so its threads are the ones the test made."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.chat_feed import ChatFeed


def feed_over(db: AsyncSession) -> ChatFeed:
    @asynccontextmanager
    async def same_session() -> AsyncIterator[AsyncSession]:
        yield db

    return ChatFeed(same_session)
