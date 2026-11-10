from __future__ import annotations

from dataclasses import dataclass

from app.shared.json_types import JsonObject


@dataclass(frozen=True)
class GeneratedLessonPlan:
    session_plan: JsonObject
    run_metadata: JsonObject


@dataclass(frozen=True)
class NormalizedLessonDraft:
    core_steps: list[JsonObject]
    global_steps: dict[str, JsonObject]
