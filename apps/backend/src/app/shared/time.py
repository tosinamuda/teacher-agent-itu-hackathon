from __future__ import annotations

from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def as_utc(moment: datetime) -> datetime:
    """MySQL's DATETIME carries no offset, so a stored value reads back naive. Every one is UTC."""
    return moment if moment.tzinfo is not None else moment.replace(tzinfo=timezone.utc)
