from functools import lru_cache

from app.domains.artefacts.types.lesson_plan.drafting.application.runtime import (
    LessonGenerationService,
)
from app.domains.artefacts.types.lesson_plan.drafting.validation.validator_service import (
    SessionPlanValidatorService,
)


@lru_cache(maxsize=1)
def get_lesson_generation_service() -> LessonGenerationService:
    return LessonGenerationService()


@lru_cache(maxsize=1)
def get_session_plan_validator() -> SessionPlanValidatorService:
    return SessionPlanValidatorService()
