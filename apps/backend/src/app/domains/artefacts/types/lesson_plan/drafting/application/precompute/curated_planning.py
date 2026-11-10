"""Authoritative lesson planning from expert-curated AO->textbook linkage.

This module builds the lesson-planning artefacts (knowledge components, evidence
plans, assessments) DIRECTLY from the curated `ao_textbook_*` rows, instead of
letting the LLM re-derive them. The expert curation already decided, per atomic
objective, which textbook record plays which role (foundation / instruction /
worked_example / exercise) and which assessment to reuse — so honoring that
structurally prevents the failures the LLM path produces, namely:

  * `reused_modeling_record` — each objective gets ITS OWN curated worked example,
    so a single modeling record is never shared across distinct objectives.
  * `ungrounded_evaluation_material` — assessments come from curated exercises,
    not invented ("worksheet", "answer key") content.

It is deliberately a SEPARATE module from the LLM precompute pipeline so the two
grounding strategies stay independent and independently testable. The pipeline
branches here when `grounding_mode == "manual_linkage"`.

Input shape (one dict per atomic objective, as loaded from the DB linkage):

    {
      "ao_id": str,
      "ao_order": int,
      "curriculum_objective_id": str,
      "objective_text": str,
      "bloom_level": str,
      "assessment": {"question": str, "expected_answer": str, ...} | None,
      "record_links": [{"record_id": str, "role": str, "link_order": int}, ...],
      "practice_record_ids": [str, ...],
    }
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from app.shared.json_types import JsonObject

from ...schemas.session_plan import (
    AssessmentItem,
    AtomicObjective,
    CandidateKC,
    CandidateKCPlan,
    StepEvidencePlan,
)
from .curated_compression import compress_curated_objectives
from .curated_objectives import CuratedObjective, normalize_curated_objective


@dataclass(frozen=True)
class CuratedPlanningArtifacts:
    """Authoritative artefacts built directly from curated linkage."""

    atomic_objectives: list[AtomicObjective]
    kc_plans: dict[str, CandidateKCPlan]
    combined_kc_plan: CandidateKCPlan
    resolved_kcs: list[CandidateKC]
    step_evidence_plans: dict[str, StepEvidencePlan]
    assessment_items: dict[str, AssessmentItem]


def _build_candidate_kc(objective: CuratedObjective) -> CandidateKC:
    return CandidateKC.model_validate(
        {
            "kc_id": objective.kc_id,
            "kc_type": objective.kc_type,
            "objective_text": objective.objective_text,
            "curriculum_objective_id": objective.curriculum_objective_id,
            "kc_focus": objective.objective_text,
            "supporting_record_ids": objective.supporting_record_ids,
            "bloom_level": objective.normalized_bloom,
        }
    )


def _build_evidence_plan(objective: CuratedObjective) -> StepEvidencePlan:
    return StepEvidencePlan.model_validate(
        {
            "lesson_objective_id": objective.lesson_objective_id,
            "selected_record_ids": objective.supporting_record_ids,
            "concept_record_ids": objective.concept_record_ids,
            "modeling_record_ids": objective.modeling_record_ids,
            "practice_record_ids": objective.practice_record_ids,
            "visual_record_ids": [],
        }
    )


def _build_assessment_item(objective: CuratedObjective) -> AssessmentItem | None:
    if not objective.assessment:
        return None
    question = str(objective.assessment.get("question") or "").strip()
    expected = str(objective.assessment.get("expected_answer") or "").strip()
    if not question or not expected:
        return None
    return AssessmentItem.model_validate(
        {
            "kc_id": objective.kc_id,
            "lesson_objective_id": objective.lesson_objective_id,
            "question": question,
            "expected_answer": expected,
            "bloom_justification": (
                f"Reused curated exercise assessing this objective at the "
                f"{objective.normalized_bloom} level."
            ),
        }
    )


def _curriculum_texts(curriculum_objectives: Sequence[Mapping[str, object]]) -> dict[str, str]:
    """Each curriculum objective's own wording, by its id."""
    return {
        str(item["curriculum_objective_id"]): str(item["objective_text"]).strip()
        for item in curriculum_objectives
        if item.get("curriculum_objective_id") and str(item.get("objective_text") or "").strip()
    }


def build_curated_planning(
    *,
    curated_objectives: list[JsonObject],
    theme: str | None = None,
    entry_behaviour: list[str] | None = None,
    instructional_materials: list[str] | None = None,
    curriculum_objectives: Sequence[Mapping[str, object]] = (),
) -> CuratedPlanningArtifacts:
    """Build authoritative planning artefacts from curated AO linkage rows.

    Only objectives that actually carry textbook evidence become KCs; an AO with
    no curated records cannot be grounded here and is skipped (the caller may
    cold-start it separately).
    """
    normalized = [normalize_curated_objective(payload) for payload in curated_objectives]
    grounded = [
        objective for objective in normalized if objective.ao_id and objective.supporting_record_ids
    ]
    grounded.sort(key=lambda objective: objective.ao_order)

    if not grounded:
        raise ValueError("no curated objective has supporting textbook records")

    # A single lesson may define at most MAX_LESSON_OBJECTIVES core objectives.
    # When the curation decomposes a subtopic more finely than that, consolidate
    # toward the curriculum-objective level so the request succeeds deterministically
    # instead of hard-failing at the strict validator.
    grounded = compress_curated_objectives(
        grounded, curriculum_texts=_curriculum_texts(curriculum_objectives)
    )

    atomic_objectives: list[AtomicObjective] = []
    kc_plans: dict[str, CandidateKCPlan] = {}
    resolved_kcs: list[CandidateKC] = []
    step_evidence_plans: dict[str, StepEvidencePlan] = {}
    assessment_items: dict[str, AssessmentItem] = {}

    for order, objective in enumerate(grounded, start=1):
        words = objective.objective_text.split()
        bloom_verb = words[0].lower() if words else "apply"
        atomic_objectives.append(
            AtomicObjective.model_validate(
                {
                    "atomic_objective_id": objective.ao_id,
                    "curriculum_objective_id": objective.curriculum_objective_id,
                    "objective_text": objective.objective_text,
                    "bloom_verb": bloom_verb,
                    "bloom_level": objective.normalized_bloom,
                    "objective_order": order,
                }
            )
        )

        candidate_kc = _build_candidate_kc(objective)
        resolved_kcs.append(candidate_kc)
        kc_plans[objective.ao_id] = CandidateKCPlan.model_validate(
            {
                "candidate_kcs": [candidate_kc.model_dump()],
                "theme": theme,
                "entry_behaviour": entry_behaviour or [],
                "instructional_materials": instructional_materials or [],
            }
        )

        step_evidence_plans[objective.lesson_objective_id] = _build_evidence_plan(objective)

        assessment_item = _build_assessment_item(objective)
        if assessment_item is not None:
            assessment_items[objective.lesson_objective_id] = assessment_item

    combined_kc_plan = CandidateKCPlan.model_validate(
        {
            "candidate_kcs": [kc.model_dump() for kc in resolved_kcs],
            "theme": theme,
            "entry_behaviour": entry_behaviour or [],
            "instructional_materials": instructional_materials or [],
        }
    )

    return CuratedPlanningArtifacts(
        atomic_objectives=atomic_objectives,
        kc_plans=kc_plans,
        combined_kc_plan=combined_kc_plan,
        resolved_kcs=resolved_kcs,
        step_evidence_plans=step_evidence_plans,
        assessment_items=assessment_items,
    )
