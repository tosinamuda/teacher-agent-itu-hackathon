"""Score a student's exit assessment into the objective-indexed diagnostic shape.

Turns per-item student responses (+ an optional per-objective confidence/difficulty
survey) into exactly the `results` the personalisation pipeline consumes:

    {"objectives": [{"lesson_objective_id","score","max_score",
                     "confidence?","perceived_difficulty?","misconception_code?"}, ...]}

This is the bridge from the student-facing exit assessment to ObjectiveLearnerState
(LearnerStateService) -> the SectionPersonalisation signature -> P1 personalisation.
"""

from __future__ import annotations

from collections import Counter, OrderedDict

from pydantic import BaseModel, Field

from app.domains.assessments.schemas import (
    ExitAssessmentItemResponse,
    ExitAssessmentObjectiveSurvey,
    ExitAssessmentSessionSurvey,
)


def _modal_misconception(codes: list[str]) -> str | None:
    """Miscon(s,o) = mode of the chosen-distractor codes for the objective.

    The most frequently selected misconception is the diagnostic signal; ties
    break to the first-seen code so the result is deterministic.
    """
    if not codes:
        return None
    counts = Counter(codes)
    best = max(counts.values())
    for code in codes:
        if counts[code] == best:
            return code
    return None


def _scale_bucket(value: int | None) -> str | None:
    """Map a 1-5 survey answer onto the 3-bucket signal the policy layer consumes.

    1-2 -> low, 3 -> medium, 4-5 -> high. The numeric answer stays canonical in
    ``confidence_score``/``difficulty_score`` (learner-model spec values ∈ {1..5});
    the bucket keeps every existing consumer (bands, prompts, rater labels) intact.
    """
    if value is None:
        return None
    if value <= 2:
        return "low"
    if value == 3:
        return "medium"
    return "high"


class AnswerEvidenceResult(BaseModel):
    """One missed item's option-level evidence (the chosen distractor)."""

    stem: str
    options: dict[str, str] = Field(default_factory=dict)
    correct_option: str = ""
    chosen_option: str = ""
    misconception_code: str | None = None


class ScoredObjectiveDiagnostic(BaseModel):
    """One objective's diagnostic result in the personalisation `results`."""

    lesson_objective_id: str
    score: int
    max_score: int
    confidence: str | None = None
    perceived_difficulty: str | None = None
    # Canonical 1-5 survey answers (the buckets above derive from these).
    confidence_score: int | None = None
    difficulty_score: int | None = None
    misconception_code: str | None = None
    # The teacher's words for that misconception, where they gave them.
    misconception_description: str | None = None
    # The missed items behind the diagnosis — rides into the learner state and
    # focal-case snapshots so P1 can target the actual chosen distractors.
    evidence: list[AnswerEvidenceResult] = Field(default_factory=list)


class SessionSurveyResult(BaseModel):
    """Session-level Interest + Affect (1-5), asked once per subtopic session."""

    interest: int | None = None
    affect: int | None = None


class ObjectiveDiagnosticResults(BaseModel):
    """The `results` contract consumed by LearnerStateService -> P1."""

    objectives: list[ScoredObjectiveDiagnostic]
    session: SessionSurveyResult | None = None


def score_objective_diagnostic(
    item_responses: list[ExitAssessmentItemResponse],
    survey: list[ExitAssessmentObjectiveSurvey] | None = None,
    session_survey: ExitAssessmentSessionSurvey | None = None,
) -> ObjectiveDiagnosticResults:
    """Aggregate item responses by objective into the diagnostic results shape."""
    survey_by_objective = {entry.lesson_objective_id: entry for entry in (survey or [])}

    aggregates: OrderedDict[str, dict] = OrderedDict()
    for response in item_responses:
        agg = aggregates.setdefault(
            response.lesson_objective_id,
            {"score": 0, "max_score": 0, "misconceptions": [], "whys": {}, "evidence": []},
        )
        agg["max_score"] += 1
        if response.is_correct:
            agg["score"] += 1
            continue
        if response.misconception_code:
            # A missed item's flagged misconception is the diagnostic signal.
            agg["misconceptions"].append(response.misconception_code)
            if response.misconception_why:
                agg["whys"].setdefault(response.misconception_code, response.misconception_why)
        if response.stem:
            # Option-level evidence: the question + chosen distractor (spec:
            # evidence items are the WRONG answers).
            agg["evidence"].append(
                AnswerEvidenceResult(
                    stem=response.stem,
                    options=response.options or {},
                    correct_option=response.correct_option or "",
                    chosen_option=response.chosen_option or "",
                    misconception_code=response.misconception_code,
                )
            )

    objectives: list[ScoredObjectiveDiagnostic] = []
    for objective_id, agg in aggregates.items():
        survey_entry = survey_by_objective.get(objective_id)
        # Only surface a misconception when the objective is not fully mastered.
        surfaces_misconception = bool(agg["misconceptions"]) and agg["score"] < agg["max_score"]
        misconception_code = (
            _modal_misconception(agg["misconceptions"]) if surfaces_misconception else None
        )
        confidence_score = survey_entry.confidence if survey_entry else None
        difficulty_score = survey_entry.perceived_difficulty if survey_entry else None
        objectives.append(
            ScoredObjectiveDiagnostic(
                lesson_objective_id=objective_id,
                score=agg["score"],
                max_score=agg["max_score"],
                confidence=_scale_bucket(confidence_score),
                perceived_difficulty=_scale_bucket(difficulty_score),
                confidence_score=confidence_score,
                difficulty_score=difficulty_score,
                misconception_code=misconception_code,
                misconception_description=agg["whys"].get(misconception_code),
                evidence=agg["evidence"],
            )
        )

    session = (
        SessionSurveyResult(interest=session_survey.interest, affect=session_survey.affect)
        if session_survey is not None
        and (session_survey.interest is not None or session_survey.affect is not None)
        else None
    )
    return ObjectiveDiagnosticResults(objectives=objectives, session=session)


def attach_survey_to_results(
    results: dict,
    survey: list[ExitAssessmentObjectiveSurvey],
    session_survey: ExitAssessmentSessionSurvey | None,
) -> dict:
    """Merge a post-class survey into already-graded diagnostic results.

    Step 2 of the two-step student flow: answers were graded first (the survey
    fields were empty), the survey arrives now. Scores stay untouched; only the
    survey-derived fields (1-5 canonical + derived buckets + session block) are
    filled in.
    """
    parsed = ObjectiveDiagnosticResults.model_validate(results)
    survey_by_objective = {entry.lesson_objective_id: entry for entry in survey}
    for objective in parsed.objectives:
        entry = survey_by_objective.get(objective.lesson_objective_id)
        if entry is None:
            continue
        objective.confidence_score = entry.confidence
        objective.difficulty_score = entry.perceived_difficulty
        objective.confidence = _scale_bucket(entry.confidence)
        objective.perceived_difficulty = _scale_bucket(entry.perceived_difficulty)
    if session_survey is not None and (
        session_survey.interest is not None or session_survey.affect is not None
    ):
        parsed.session = SessionSurveyResult(
            interest=session_survey.interest, affect=session_survey.affect
        )
    return parsed.model_dump(mode="json", exclude_none=True)
