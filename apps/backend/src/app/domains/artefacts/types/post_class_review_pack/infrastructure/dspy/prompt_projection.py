"""Pure transformations from persisted review-pack records to model-visible inputs."""

from __future__ import annotations

import dspy

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    LessonContextForGeneration,
    ObjectiveLearnerState,
    PersonalisedReviewPackRequest,
    ReviewPackRequest,
    SectionGenerationUnit,
    SessionSignals,
    SourceEvidenceItem,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    ReviewPackSection,
)

RECORD_KEYS = (
    "unit_id",
    "source_step_id",
    "section_id",
    "block_id",
    "item_id",
    "lesson_objective_id",
    "curriculum_objective_id",
    "source_refs",
)
FIGURE_PROMPT_KEYS = ("figure_ref", "caption")


def prompt_unit(unit: SectionGenerationUnit) -> dict:
    """Project one unit to meaning only: no record ids, nulls, or drawing source."""
    data = unit.model_dump(exclude_none=True)
    data.pop("source_evidence", None)
    figures = [_prompt_figure(figure) for figure in data.get("source_figures", [])]
    data["source_figures"] = [figure for figure in figures if figure]
    return _without_record_keys(data)


def prompt_section(section: ReviewPackSection) -> dict:
    """Project a finished section to model-authored content only."""
    data = section.model_dump(exclude_none=True)
    data["blocks"] = [
        _without_record_keys(block)
        for block in data.get("blocks", [])
        if block.get("block_type") != "visual"
    ]
    data["practice"] = [_without_record_keys(item) for item in data.get("practice", [])]
    return _without_record_keys(data)


def prompt_state(state: ObjectiveLearnerState) -> dict:
    """Project learner state without the objective record key or hollow fields."""
    data = _without_record_keys(state.model_dump(exclude_none=True))
    data["evidence_items"] = [_with_content(item) for item in data.get("evidence_items", [])]
    return _with_content(data)


def prompt_signals(signals: SessionSignals | None) -> dict:
    """Project answered session signals; absent answers reveal no withheld fields."""
    return _with_content(signals.model_dump(exclude_none=True)) if signals else {}


def prompt_lesson(lesson: LessonContextForGeneration) -> dict:
    """Project lesson context without announcing fields withheld by a condition."""
    return _with_content(lesson.model_dump(exclude_none=True))


def prompt_evidence(evidence: list[SourceEvidenceItem]) -> list[dict]:
    """Project evidence to its source label and excerpt without hollow catalogue fields.

    ``regions`` is dropped, the way ``prompt_unit`` drops ``source_evidence``. A region
    is an ADDRESS for the reading tools, not a second copy of the note: left in, it put
    every character of the excerpt into the prompt again, and t3-w02's C2 evidence
    measured 2.12x the note it came from.
    """
    return [
        _without_record_keys(item.model_dump(exclude_none=True, exclude={"regions"}))
        for item in evidence
    ]


def grounded_lesson_content(
    *,
    unit: SectionGenerationUnit,
    signature: type[dspy.Signature],
) -> list[dict]:
    """The evidence a grounded contract teaches from, refusing to render it empty.

    Two consumers read the retrieval policy independently: ``signature_for``
    selects a grounded contract from ``retrieval.enabled``, while the request
    builder populates evidence under ``provides_evidence`` and the evidence
    scope. When they disagree, the model is told to teach nothing beyond
    ``lesson_content`` and handed nothing — which reads back as a weak evidence
    condition rather than a broken one.

    Raises:
        ValueError: when a contract that teaches only from evidence has none.
    """
    evidence = prompt_evidence(unit.source_evidence)
    if not evidence:
        raise ValueError(
            f"{signature.__name__} teaches only from lesson_content, "
            f"and unit {unit.unit_id} carries no source evidence"
        )
    return evidence


def leveled_inputs(
    *,
    request: ReviewPackRequest,
    unit: SectionGenerationUnit,
    signature: type[dspy.Signature],
) -> dict[str, object]:
    """Build the exact inputs for one per-level base-generation call."""
    inputs: dict[str, object] = {
        "artefact_spec": request.artefact_spec,
        "lesson_context": prompt_lesson(request.lesson_context),
        "unit_context": prompt_unit(unit),
    }
    if "lesson_content" in signature.input_fields:
        inputs["lesson_content"] = grounded_lesson_content(unit=unit, signature=signature)
    return inputs


def shared_inputs(*, request: ReviewPackRequest, unit: SectionGenerationUnit) -> dict[str, object]:
    """Build the exact inputs for one shared-signature base-generation call."""
    return {
        "artefact_spec": request.artefact_spec,
        "policy": request.policy,
        "lesson_context": prompt_lesson(request.lesson_context),
        "unit_context": prompt_unit(unit),
        "source_evidence": prompt_evidence(unit.source_evidence),
    }


def repair_inputs(
    *,
    request: ReviewPackRequest,
    unit: SectionGenerationUnit,
    failed_section: ReviewPackSection,
    issues: list[str],
) -> dict[str, object]:
    """Build the exact inputs for one packed repair call."""
    return {
        "policy": request.policy,
        "lesson_context": prompt_lesson(request.lesson_context),
        "unit_context": prompt_unit(unit),
        "source_evidence": prompt_evidence(unit.source_evidence),
        "failed_section": prompt_section(failed_section),
        "validation_issues": issues,
    }


def personalise_inputs(
    *,
    request: PersonalisedReviewPackRequest,
    unit: SectionGenerationUnit,
    base_section: ReviewPackSection,
    learner_state: ObjectiveLearnerState,
) -> dict[str, object]:
    """Build the exact inputs for one personalisation call."""
    return {
        "personalisation_policy": request.policy,
        "lesson_context": prompt_lesson(request.lesson_context),
        "base_section": prompt_section(base_section),
        "learner_state": prompt_state(learner_state),
        "session_signals": prompt_signals(request.session_signals),
        "source_evidence": prompt_evidence(unit.source_evidence),
    }


def _prompt_figure(figure: dict) -> dict:
    return {key: value for key, value in figure.items() if key in FIGURE_PROMPT_KEYS and value}


def _without_record_keys(data: dict) -> dict:
    return _with_content({key: value for key, value in data.items() if key not in RECORD_KEYS})


def _with_content(data: dict) -> dict:
    return {key: value for key, value in data.items() if value not in ([], {}, "")}
