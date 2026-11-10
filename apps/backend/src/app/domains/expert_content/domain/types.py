"""Expert-content enum types (typed status vocab for textbook seeding + AO linkage)."""

from __future__ import annotations

from enum import Enum


class TextbookRecordLinkStatus(str, Enum):
    """Curriculum-coverage status of one textbook record.

    ``LINKED`` = uniquely tied to a subtopic; ``AMBIGUOUS`` = could match
    several; ``UNLINKED`` = no curriculum match (out-of-scope content).
    """

    LINKED = "linked"
    AMBIGUOUS = "ambiguous"
    UNLINKED = "unlinked"


class TextbookSeedRunStatus(str, Enum):
    """A textbook-ingestion seed run: in-flight, failed, or completed."""

    STARTED = "started"
    FAILED = "failed"
    COMPLETED = "completed"


class AoTextbookLinkageStatus(str, Enum):
    """How an atomic-objective row resolved against the textbook record set.

    ``MAPPED`` = one or more records selected; ``NEEDS_REVIEW`` = candidate
    records exist but the rules flagged the choice; ``NO_RECORDS`` = no
    candidate textbook record covers the AO at all.
    """

    MAPPED = "mapped"
    NEEDS_REVIEW = "needs_review"
    NO_RECORDS = "no_records"


class AoTextbookLinkageSeedRunStatus(str, Enum):
    """Seed-run lifecycle for the AO->textbook linkage import. Same vocab as the textbook seed."""

    STARTED = "started"
    FAILED = "failed"
    COMPLETED = "completed"
