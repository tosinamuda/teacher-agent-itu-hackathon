"""Research enums shared across the ``experiments`` and ``evaluation`` domains.

These three enums are part of the vocabulary both domains exchange:
``Hypothesis`` labels a run, ``PacketStatus`` is the lifecycle of an
``EvaluationPacket`` (owned by ``evaluation``), and ``FocalCaseType`` classifies
a learner case. They live here, in the shared kernel, so neither domain has to
import the other just to name them. ``experiments.domain.types`` re-exports them
for backwards compatibility with that domain's existing call sites.
"""

from __future__ import annotations

from enum import Enum


class Hypothesis(str, Enum):
    H1 = "H1"
    H2 = "H2"


class PacketStatus(str, Enum):
    CREATED = "created"
    READY = "ready"
    FAILED = "failed"


class FocalCaseType(str, Enum):
    REMEDIATE = "remediate"
    REINFORCE = "reinforce"
    EXTEND = "extend"
    MIXED_OR_MISCONCEPTION = "mixed_or_misconception"


__all__ = ["FocalCaseType", "Hypothesis", "PacketStatus"]
