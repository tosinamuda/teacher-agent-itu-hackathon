from __future__ import annotations

from typing import Protocol

from app.domains.artefacts.core.domain.specification import ArtefactSpec
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime.types import (
    GeneratedLessonPlan,
)
from app.domains.artefacts.types.lesson_plan.drafting.validation.validator_service import (
    SessionPlanValidationResult,
)
from app.shared.json_types import JsonObject


class LessonPlanGeneratorPort(Protocol):
    async def generate(
        self,
        session_context: JsonObject,
        curriculum_context: JsonObject,
        reference_context: list[JsonObject],
        evidence_selection_strategy: str | None = None,
        grounding_mode: str = "manual_linkage",
        curated_objectives: list[JsonObject] | None = None,
        brief: ArtefactSpec | None = None,
    ) -> GeneratedLessonPlan: ...


class SessionPlanValidatorPort(Protocol):
    def validate(
        self,
        session_plan: JsonObject,
        session_context: JsonObject,
    ) -> SessionPlanValidationResult: ...
