"""The model-backed seams of conditioned generation, as protocols.

Everything here is answered by a language model, so nothing here can run in a
test. Naming the seams lets a caller supply any implementation — the live DSPy
modules in production, a stand-in offline — without a test having to mimic the
shape of a concrete class it does not otherwise care about.

Keeping them together also makes the rule visible: a collaborator in this file
performs I/O when it is CALLED, and its implementations open a client when they
are CONSTRUCTED. The generation entrypoints therefore require them rather than
defaulting to one, so a caller that forgets fails at construction with a missing
argument instead of at request time with an authentication error.
"""

from __future__ import annotations

from typing import Protocol

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
    PersonalisedReviewPackRequest,
    ReviewPackRequest,
    SectionGenerationUnit,
)
from app.domains.artefacts.types.post_class_review_pack.application.validation.schemas import (
    CheckResult,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ValidationCheck,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)


class SectionGenerator(Protocol):
    """Produce one section from one condition-filtered unit."""

    async def generate_section(
        self, *, request: ReviewPackRequest, unit: SectionGenerationUnit
    ) -> ReviewPackSection: ...


class SectionRepairer(Protocol):
    """Repair one generated section under explicit validation findings."""

    async def repair_section(
        self,
        *,
        request: ReviewPackRequest,
        unit: SectionGenerationUnit,
        failed_section: ReviewPackSection,
        issues: list[str],
    ) -> ReviewPackSection: ...


class SectionPersonaliser(Protocol):
    """Adapts an approved base section to one learner's objective state."""

    async def personalise_section(
        self,
        *,
        request: PersonalisedReviewPackRequest,
        unit: SectionGenerationUnit,
        base_section: ReviewPackSection,
        learner_state: ObjectiveLearnerState,
    ) -> ReviewPackSection: ...


class SectionCritic(Protocol):
    """Reads generated sections against the teaching evidence behind them."""

    async def review(
        self,
        *,
        request: ReviewPackRequest,
        sections: list[ReviewPackSection],
        checks: tuple[ValidationCheck, ...],
    ) -> list[CheckResult]: ...


class SectionReviser(Protocol):
    """Edits a flagged section in place rather than rewriting it whole."""

    async def revise(
        self, *, section: ReviewPackSection, findings: list[str]
    ) -> ReviewPackSection: ...
