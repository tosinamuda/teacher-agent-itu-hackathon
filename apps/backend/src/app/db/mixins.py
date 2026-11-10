"""Reusable declarative column mixins.

These produce byte-identical column definitions to the inline declarations they
replace, so applying them is schema-neutral (no migration).
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.time import utc_now


class TimestampMixin:
    """``created_at`` / ``updated_at`` (``utc_now`` default, ``now()`` server-default)."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        server_default=text("now()"),
        onupdate=utc_now,
    )
