from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ObjectiveBand = Literal["remediate", "reinforce", "extend"]
SignalLevel = Literal["low", "medium", "high"]


def humanise_misconception_code(code: str) -> str:
    """Render a snake_case distractor misconception code as readable prose.

    Distractors carry only a short code (e.g. ``missing_factor_of_two``); no
    description is authored anywhere upstream. Surfaces that need prose derive it
    here ("Missing factor of two") so a recorded misconception is never silently
    shown as "none recorded".
    """
    return code.replace("_", " ").strip().capitalize()


def misconception_codes_for_snapshot(learner_state_snapshot: dict | None) -> list[str]:
    """Distinct misconception codes across a focal case's objective states.

    Reported separately from the band (``focal_case_type``): a learner can sit in
    the ``extend`` band yet still carry a misconception, so the two are orthogonal
    tags. Returns the raw codes (stable grouping keys); humanise at the display
    layer via ``humanise_misconception_code``.
    """
    objective_states = (learner_state_snapshot or {}).get("objective_states")
    if not isinstance(objective_states, list):
        return []
    codes: dict[str, None] = {}
    for objective in objective_states:
        if isinstance(objective, dict):
            code = objective.get("misconception_code")
            if isinstance(code, str) and code:
                codes.setdefault(code, None)
    return list(codes)


class AnswerEvidence(BaseModel):
    """One missed diagnostic item: the question and the distractor the learner chose.

    The option-level evidence behind the objective's diagnosis (learner-model
    spec: the chosen distractor is the primary personalisation signal). Carried
    on the learner state so focal-case snapshots are self-contained and the P1
    prompt can defuse the learner's ACTUAL error, not just the modal label.
    """

    model_config = ConfigDict(extra="forbid")

    stem: str = Field(..., min_length=1)
    options: dict[str, str] = Field(default_factory=dict)
    correct_option: str = ""
    chosen_option: str = ""
    misconception_code: str | None = None


class ObjectiveLearnerState(BaseModel):
    """Per-objective learner state (the thesis personalisation unit).

    Derived from the post-class diagnostic: one record per lesson objective.
    `band` is assigned from mastery (remediate < 0.50 <= reinforce < 0.75 <= extend).
    """

    model_config = ConfigDict(extra="forbid")

    lesson_objective_id: str = Field(..., min_length=1)
    mastery_score: float | None = Field(default=None, ge=0.0, le=1.0)
    # The counts behind the fraction (None on pre-counts snapshots). With as few
    # as 2 items per objective, "1 of 2 correct" is honest evidence where a bare
    # 0.5 reads as calibrated measurement.
    questions_correct: int | None = Field(default=None, ge=0)
    questions_total: int | None = Field(default=None, ge=0)
    band: ObjectiveBand
    misconception_code: str | None = None
    misconception_description: str | None = None
    confidence: SignalLevel | None = None
    perceived_difficulty: SignalLevel | None = None
    # Canonical 1-5 survey answers (the buckets above derive from these;
    # None on bucket-era diagnostics).
    confidence_score: int | None = Field(default=None, ge=1, le=5)
    difficulty_score: int | None = Field(default=None, ge=1, le=5)
    evidence_refs: list[str] = Field(default_factory=list)
    # The missed items behind the diagnosis (empty on pre-evidence snapshots).
    evidence: list[AnswerEvidence] = Field(default_factory=list)


class LearnerCurriculumProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_of_study: str | None = None
    trade_subject: str | None = None
    field_core_subjects: list[str] | None = None


class SessionSurvey(BaseModel):
    """Session-level survey signals, asked once for the whole subtopic session.

    Interest(s,σ) and Affect(s,σ) on the 1-5 scale (learner-model spec). Used as
    pack-level tone/depth modifiers: low interest → shorter, more direct sections;
    low affect (confusion) → reduce cognitive load.
    """

    model_config = ConfigDict(extra="forbid")

    interest: int | None = Field(default=None, ge=1, le=5)
    affect: int | None = Field(default=None, ge=1, le=5)


class LearnerPreferences(BaseModel):
    model_config = ConfigDict(extra="forbid")

    language_level: str | None = None
    pace_preference: str | None = None
    time_budget_minutes: int | None = Field(default=None, ge=1)


class LearnerState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    student_id: str = Field(..., min_length=1)
    diagnostic_id: str | None = None
    curriculum_profile: LearnerCurriculumProfile = Field(default_factory=LearnerCurriculumProfile)
    preferences: LearnerPreferences = Field(default_factory=LearnerPreferences)
    mastered_step_ids: list[str] = Field(default_factory=list)
    objective_states: list[ObjectiveLearnerState] = Field(default_factory=list)
    session_survey: SessionSurvey | None = None

    def objective_state(self, lesson_objective_id: str | None) -> ObjectiveLearnerState | None:
        if not lesson_objective_id:
            return None
        for state in self.objective_states:
            if state.lesson_objective_id == lesson_objective_id:
                return state
        return None
