"""Every TikZ drawing stored content carries, drawn once and kept as SVG."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, Text, text
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.shared.time import utc_now

#: A drawing's source and its SVG can each run past TEXT's 64 KB.
_LONG_TEXT = Text().with_variant(mysql.MEDIUMTEXT(), "mysql")


class FigureState:
    PENDING = "pending"
    DRAWN = "drawn"
    #: TeX was there and the drawing would not compile; its caption stands in for it.
    UNDRAWABLE = "undrawable"


class Figure(Base):
    __tablename__ = "figures"

    #: The SHA-256 of the trimmed ``tikzpicture`` source.
    figure_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source: Mapped[str] = mapped_column(_LONG_TEXT)
    svg: Mapped[str | None] = mapped_column(_LONG_TEXT, nullable=True)
    state: Mapped[str] = mapped_column(
        String(16), default=FigureState.PENDING, server_default=text("'pending'")
    )
    drawn_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, server_default=text("now()")
    )
