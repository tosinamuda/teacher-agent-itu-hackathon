from __future__ import annotations

from typing import cast

from app.domains.learner_state.domain.models import (
    AnswerEvidence,
    LearnerCurriculumProfile,
    LearnerPreferences,
    LearnerState,
    ObjectiveBand,
    ObjectiveLearnerState,
    SessionSurvey,
    SignalLevel,
    humanise_misconception_code,
)
from app.shared.json_types import JsonObject

MASTERED_STEP_IDS_KEY = "mastered_step_ids"
OBJECTIVES_KEY = "objectives"

# Mastery -> band thresholds (learner-state-plan.md §5).
REMEDIATE_BELOW = 0.50
EXTEND_AT_OR_ABOVE = 0.75

_SIGNAL_LEVELS = {"low", "medium", "high"}


def _band_for_mastery(mastery: float) -> ObjectiveBand:
    if mastery < REMEDIATE_BELOW:
        return "remediate"
    if mastery < EXTEND_AT_OR_ABOVE:
        return "reinforce"
    return "extend"


class LearnerStateService:
    def build(
        self,
        *,
        student_id: str,
        student_profile: object,
        diagnostic_id: str | None = None,
        diagnostic_results: JsonObject | None = None,
    ) -> LearnerState:
        return LearnerState(
            student_id=student_id,
            diagnostic_id=diagnostic_id,
            curriculum_profile=LearnerCurriculumProfile(
                field_of_study=getattr(student_profile, "field_of_study", None),
                trade_subject=getattr(student_profile, "trade_subject", None),
                field_core_subjects=getattr(student_profile, "field_core_subjects", None),
            ),
            preferences=LearnerPreferences(
                language_level=getattr(student_profile, "language_level", None),
                pace_preference=getattr(student_profile, "pace_preference", None),
                time_budget_minutes=getattr(student_profile, "time_budget_minutes", None),
            ),
            mastered_step_ids=self._mastered_step_ids(diagnostic_results),
            objective_states=self._objective_states(diagnostic_results),
            session_survey=self._session_survey(diagnostic_results),
        )

    @staticmethod
    def _session_survey(diagnostic_results: JsonObject | None) -> SessionSurvey | None:
        """Read the session-level Interest/Affect block recorded by the scorer."""
        if diagnostic_results is None:
            return None
        raw = diagnostic_results.get("session")
        if not isinstance(raw, dict):
            return None
        interest = raw.get("interest")
        affect = raw.get("affect")
        survey = SessionSurvey(
            interest=interest if isinstance(interest, int) and 1 <= interest <= 5 else None,
            affect=affect if isinstance(affect, int) and 1 <= affect <= 5 else None,
        )
        return survey if (survey.interest is not None or survey.affect is not None) else None

    def _mastered_step_ids(self, diagnostic_results: JsonObject | None) -> list[str]:
        if diagnostic_results is None:
            return []
        raw_step_ids = diagnostic_results.get(MASTERED_STEP_IDS_KEY, [])
        if not isinstance(raw_step_ids, list):
            return []
        return [step_id for step_id in raw_step_ids if isinstance(step_id, str) and step_id]

    def _objective_states(
        self, diagnostic_results: JsonObject | None
    ) -> list[ObjectiveLearnerState]:
        """Derive one ObjectiveLearnerState per diagnostic objective.

        Expects diagnostic_results["objectives"] = [{lesson_objective_id, score,
        max_score, confidence?, perceived_difficulty?/difficulty?,
        misconception_code?, misconception_description?, evidence_refs?}, ...].
        """
        if diagnostic_results is None:
            return []
        raw = diagnostic_results.get(OBJECTIVES_KEY)
        if not isinstance(raw, list):
            return []

        states: list[ObjectiveLearnerState] = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            objective_id = item.get("lesson_objective_id")
            if not isinstance(objective_id, str) or not objective_id:
                continue

            mastery = self._mastery(item.get("score"), item.get("max_score"))
            band = _band_for_mastery(mastery if mastery is not None else 0.0)
            questions_correct = self._count(item.get("score"))
            questions_total = self._count(item.get("max_score"))
            misconception_code = self._opt_str(item.get("misconception_code"))
            misconception_description = self._opt_str(item.get("misconception_description"))
            if misconception_description is None and misconception_code is not None:
                # Distractors carry only a code — derive readable prose so the
                # misconception is never silently dropped downstream.
                misconception_description = humanise_misconception_code(misconception_code)
            states.append(
                ObjectiveLearnerState(
                    lesson_objective_id=objective_id,
                    mastery_score=mastery,
                    questions_correct=questions_correct,
                    questions_total=questions_total,
                    band=band,
                    misconception_code=misconception_code,
                    misconception_description=misconception_description,
                    confidence=self._signal(item.get("confidence")),
                    perceived_difficulty=self._signal(
                        item.get("perceived_difficulty") or item.get("difficulty")
                    ),
                    confidence_score=self._score(item.get("confidence_score")),
                    difficulty_score=self._score(item.get("difficulty_score")),
                    evidence_refs=self._evidence_refs(item),
                    evidence=self._answer_evidence(item),
                )
            )
        return states

    @staticmethod
    def _mastery(score: object, max_score: object) -> float | None:
        if not isinstance(score, (int, float, str)) or not isinstance(max_score, (int, float, str)):
            return None
        try:
            score_value = float(score)
            max_value = float(max_score)
        except (TypeError, ValueError):
            return None
        if max_value <= 0:
            return None
        return max(0.0, min(1.0, score_value / max_value))

    @staticmethod
    def _opt_str(value: object) -> str | None:
        return value if isinstance(value, str) and value.strip() else None

    @staticmethod
    def _signal(value: object) -> SignalLevel | None:
        if isinstance(value, str) and value in _SIGNAL_LEVELS:
            return cast(SignalLevel, value)
        # 1-5 survey answers bucket onto the 3-level signal (1-2/3/4-5).
        if isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 5:
            return "low" if value <= 2 else "medium" if value == 3 else "high"
        return None

    @staticmethod
    def _score(value: object) -> int | None:
        """Narrow a canonical 1-5 survey score; None for anything else."""
        if isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 5:
            return value
        return None

    @staticmethod
    def _count(value: object) -> int | None:
        """Narrow a non-negative question count; None for anything else."""
        if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            return value
        return None

    @staticmethod
    def _evidence_refs(item: JsonObject) -> list[str]:
        """Narrow ``item['evidence_refs']`` to a list of strings; ``[]`` if not a list."""
        raw = item.get("evidence_refs")
        if not isinstance(raw, list):
            return []
        return [str(ref) for ref in raw if isinstance(ref, str)]

    @staticmethod
    def _answer_evidence(item: JsonObject) -> list[AnswerEvidence]:
        """Read the missed-item evidence recorded by the scorer (empty pre-evidence)."""
        raw = item.get("evidence")
        if not isinstance(raw, list):
            return []
        evidence: list[AnswerEvidence] = []
        for entry in raw:
            if not isinstance(entry, dict) or not entry.get("stem"):
                continue
            options = entry.get("options")
            evidence.append(
                AnswerEvidence(
                    stem=str(entry["stem"]),
                    options=(
                        {str(k): str(v) for k, v in options.items()}
                        if isinstance(options, dict)
                        else {}
                    ),
                    correct_option=str(entry.get("correct_option") or ""),
                    chosen_option=str(entry.get("chosen_option") or ""),
                    misconception_code=(
                        str(entry["misconception_code"])
                        if entry.get("misconception_code")
                        else None
                    ),
                )
            )
        return evidence
