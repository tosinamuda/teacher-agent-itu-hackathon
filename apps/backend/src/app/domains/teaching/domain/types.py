"""Teaching-domain enum types (typed status vocab for the lesson-delivery lifecycle)."""

from __future__ import annotations

from enum import Enum


class LessonDeliveryStatus(str, Enum):
    """Where a ``LessonDelivery`` row is in its lifecycle.

    Today only ``PLANNED`` is assigned by code — the delivered-on column and the
    delivered-vs-cancelled split move into this enum as the teaching workflow
    grows; that's the right shape to grow into.
    """

    PLANNED = "planned"
