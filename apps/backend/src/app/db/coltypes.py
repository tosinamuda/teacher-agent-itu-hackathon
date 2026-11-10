"""The app's standard column types.

Models import ``UUID`` and ``JSON`` from here for a single, consistent source.

* ``UUID`` is SQLAlchemy's generic ``Uuid`` (stored as ``CHAR(32)``). Call sites
  use ``UUID(as_uuid=True)``.
* ``JSON`` is SQLAlchemy's generic ``JSON`` (MySQL ``JSON``). Call sites use
  ``mapped_column(JSON)``.
* ``MICROSECOND_DATETIME`` keeps microseconds (MySQL ``DATETIME(6)``), for a column rows
  are ordered by: a plain ``DateTime`` is whole seconds in MySQL, so rows written in the
  same second tie.
"""

from __future__ import annotations

from sqlalchemy import JSON, DateTime, Uuid
from sqlalchemy.dialects.mysql import DATETIME

UUID = Uuid
MICROSECOND_DATETIME = DateTime(timezone=True).with_variant(DATETIME(fsp=6), "mysql")

__all__ = ["JSON", "MICROSECOND_DATETIME", "UUID"]
