"""Evaluation-domain enum types (typed status vocab for audit items)."""

from __future__ import annotations

from enum import Enum


class AuditItemStatus(str, Enum):
    """An ``EvaluationAuditItem`` is ``READY`` once paired with a rated source excerpt."""

    READY = "ready"
