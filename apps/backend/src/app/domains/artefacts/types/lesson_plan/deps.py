"""The lesson-plan service, wired to the generator, validator and specification store."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.application.specifications import ContentSpecifications
from app.domains.artefacts.core.infrastructure.specifications import SqlAlchemyContentSpecifications
from app.domains.artefacts.types.lesson_plan.application.service import (
    DiagnosticGenerator,
    LessonPlanApplicationService,
)
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime import (
    LessonGenerationService,
)
from app.domains.artefacts.types.lesson_plan.drafting.deps import (
    get_lesson_generation_service,
    get_session_plan_validator,
)
from app.domains.artefacts.types.lesson_plan.drafting.validation.validator_service import (
    SessionPlanValidatorService,
)
from app.domains.assessments.infrastructure.wiring import build_diagnostic_service


def get_content_specifications() -> ContentSpecifications:
    return SqlAlchemyContentSpecifications()


def lesson_plan_service(
    db: AsyncSession,
    *,
    generator: LessonGenerationService | None = None,
    validator: SessionPlanValidatorService | None = None,
    specifications: ContentSpecifications | None = None,
    diagnostic_service: DiagnosticGenerator | None = None,
) -> LessonPlanApplicationService:
    return LessonPlanApplicationService(
        db=db,
        generator=generator or get_lesson_generation_service(),
        validator=validator or get_session_plan_validator(),
        specifications=specifications or get_content_specifications(),
        diagnostic_service=diagnostic_service or build_diagnostic_service(),
    )
