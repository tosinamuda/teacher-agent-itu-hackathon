from __future__ import annotations

import re
from pathlib import Path
from time import perf_counter

from app.shared.json_types import JsonObject

from ...infrastructure.dspy.evidence_plan import build_supported_evidence_plan
from ...infrastructure.dspy.kc_compression import (
    LessonStructure,
    build_lesson_structure_from_kcs,
    compress_knowledge_components,
)
from ...infrastructure.dspy.modules.assessment_designer import AssessmentDesigner
from ...infrastructure.dspy.modules.kc_extractor import KCExtractor
from ...infrastructure.dspy.modules.objective_atomizer import ObjectiveAtomizer
from ...infrastructure.dspy.textbook_support import (
    PRACTICE_SUPPORT_TYPES,
    normalize_candidate_kcs_for_support,
    select_textbook_records,
)
from ...schemas.session_plan import (
    AssessmentItem,
    AtomicObjective,
    CandidateKC,
    CandidateKCPlan,
    StepEvidencePlan,
)
from .cache import InfrastructureArtifactCache
from .context import ObjectiveContextBuilder
from .types import (
    KCPlanningResult,
    LessonDraftResult,
    SubtopicResult,
    Violation,
    derive_scope_keys,
    stable_payload_hash,
)
from .verification import DecompositionVerifier


def _stripped_str_list(value: object) -> list[str]:
    """Strip-and-filter narrow on a list of strings; ``[]`` if not a list.

    Local replacement for the retired ``json_coerce.as_str_list``.
    """
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _token_set(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", str(value or "").lower()))


class InfrastructurePlanningPipeline:
    """Build and cache planning infrastructure before drafting lesson content."""

    def __init__(
        self,
        *,
        model_name: str | None = None,
        cache_dir: Path | None = None,
        atomizer: ObjectiveAtomizer | None = None,
        kc_extractor: KCExtractor | None = None,
        assessment_designer: AssessmentDesigner | None = None,
    ) -> None:
        self._atomizer = atomizer or ObjectiveAtomizer()
        self._kc_extractor = kc_extractor or KCExtractor()
        self._assessment_designer = assessment_designer or AssessmentDesigner()
        self._verifier = DecompositionVerifier()
        self._cache = InfrastructureArtifactCache(cache_dir, model_name=model_name)

    def _curriculum_hash(
        self,
        *,
        curriculum_context: JsonObject,
        curriculum_objectives: list[JsonObject],
        topic_key: str,
        subtopic_id: str,
    ) -> str:
        return stable_payload_hash(
            {
                "curriculum_objectives": curriculum_objectives,
                "evaluation_guide": curriculum_context.get("evaluation_guide") or [],
                "entry_behaviour": curriculum_context.get("entry_behaviour") or [],
                "instructional_materials": curriculum_context.get("instructional_materials") or [],
                "topic_key": topic_key,
                "subtopic_id": subtopic_id,
            }
        )

    def _plan_atomic_objectives(
        self,
        *,
        atomic_objectives: list[AtomicObjective],
        objective_context_builder: ObjectiveContextBuilder,
        textbook_records: list[JsonObject],
    ) -> tuple[
        dict[str, CandidateKCPlan],
        dict[str, list[AssessmentItem]],
        list[CandidateKC],
        dict[str, list[Violation]],
        list[Violation],
        int,
    ]:
        kc_plans: dict[str, CandidateKCPlan] = {}
        assessment_items_by_atomic_objective: dict[str, list[AssessmentItem]] = {}
        combined_candidate_kcs: list[CandidateKC] = []
        violations_by_atomic_objective: dict[str, list[Violation]] = {}
        violations: list[Violation] = []
        planning_llm_calls = getattr(self._atomizer, "last_llm_calls", 0)

        for atomic_objective in atomic_objectives:
            objective_context = objective_context_builder.assemble(atomic_objective)
            kc_plan = self._kc_extractor(objective_context=objective_context)
            kc_plans[atomic_objective.atomic_objective_id] = kc_plan
            combined_candidate_kcs.extend(kc_plan.candidate_kcs)
            planning_llm_calls += getattr(self._kc_extractor, "last_llm_calls", 1)

            current_violations = self._verifier.verify_all(kc_plan, objective_context)
            violations_by_atomic_objective[atomic_objective.atomic_objective_id] = (
                current_violations
            )
            violations.extend(current_violations)

            objective_assessments, assessment_call_count = self._build_atomic_objective_assessments(
                kc_plan=kc_plan,
                textbook_records=textbook_records,
            )
            assessment_items_by_atomic_objective[atomic_objective.atomic_objective_id] = (
                objective_assessments
            )
            planning_llm_calls += assessment_call_count

        return (
            kc_plans,
            assessment_items_by_atomic_objective,
            combined_candidate_kcs,
            violations_by_atomic_objective,
            violations,
            planning_llm_calls,
        )

    def build_infrastructure(
        self,
        *,
        scope_context: JsonObject,
        curriculum_context: JsonObject,
        curriculum_objectives: list[JsonObject],
        textbook_records: list[JsonObject],
        topics_enriched: list[JsonObject] | None = None,
        scheme: JsonObject | None = None,
        records_by_subtopic: dict[str, list[JsonObject]] | None = None,
    ) -> KCPlanningResult:
        started_at = perf_counter()
        topic_key, subtopic_id = derive_scope_keys(scope_context)
        textbook_hash = stable_payload_hash(textbook_records)
        curriculum_hash = self._curriculum_hash(
            curriculum_context=curriculum_context,
            curriculum_objectives=curriculum_objectives,
            topic_key=topic_key,
            subtopic_id=subtopic_id,
        )
        cached = self._cache.get(
            subtopic_id=subtopic_id,
            topic_key=topic_key,
            textbook_hash=textbook_hash,
            curriculum_hash=curriculum_hash,
        )
        if cached is not None:
            return cached

        objective_context_builder = ObjectiveContextBuilder(
            scope_context=scope_context,
            curriculum_context=curriculum_context,
            textbook_records=textbook_records,
            topics_enriched=topics_enriched,
            scheme=scheme,
            records_by_subtopic=records_by_subtopic,
        )
        atomic_objectives = self._atomizer(
            curriculum_objectives=curriculum_objectives,
            subtopic_title=str(scope_context.get("subtopic") or ""),
            evaluation_guide=_stripped_str_list(curriculum_context.get("evaluation_guide")),
        )
        (
            kc_plans,
            assessment_items_by_atomic_objective,
            combined_candidate_kcs,
            violations_by_atomic_objective,
            violations,
            planning_llm_calls,
        ) = self._plan_atomic_objectives(
            atomic_objectives=atomic_objectives,
            objective_context_builder=objective_context_builder,
            textbook_records=textbook_records,
        )

        normalized_candidate_kcs = normalize_candidate_kcs_for_support(
            combined_candidate_kcs,
            textbook_records=textbook_records,
        )
        combined_kc_plan = CandidateKCPlan.model_validate(
            {
                "candidate_kcs": [
                    candidate_kc.model_dump() for candidate_kc in normalized_candidate_kcs
                ],
                "theme": scope_context.get("theme"),
                "entry_behaviour": _stripped_str_list(curriculum_context.get("entry_behaviour")),
                "instructional_materials": _stripped_str_list(
                    curriculum_context.get("instructional_materials")
                ),
            }
        )
        resolved_kcs = compress_knowledge_components(combined_kc_plan.candidate_kcs, max_kcs=4)
        lesson_structure = build_lesson_structure_from_kcs(
            resolved_kcs,
            curriculum_objectives=curriculum_objectives,
        )
        step_evidence_plans = self._build_step_evidence_plans(
            lesson_structure=lesson_structure,
            textbook_records=textbook_records,
        )
        assessment_items, fallback_assessment_calls = self._map_assessments_to_lesson_objectives(
            lesson_structure=lesson_structure,
            kc_plans=kc_plans,
            assessment_items_by_atomic_objective=assessment_items_by_atomic_objective,
            textbook_records=textbook_records,
        )
        planning_llm_calls += fallback_assessment_calls
        planning_duration_ms = int(round((perf_counter() - started_at) * 1000))

        planning_result = KCPlanningResult(
            subtopic_id=subtopic_id,
            topic_key=topic_key,
            atomic_objectives=atomic_objectives,
            kc_plans=kc_plans,
            step_evidence_plans=step_evidence_plans,
            assessment_items_by_atomic_objective=assessment_items_by_atomic_objective,
            assessment_items=assessment_items,
            lesson_structure=lesson_structure,
            combined_kc_plan=combined_kc_plan,
            resolved_kcs=resolved_kcs,
            violations_by_atomic_objective=violations_by_atomic_objective,
            violations=violations,
            from_cache=False,
            planning_duration_ms=planning_duration_ms,
            llm_calls_planning=planning_llm_calls,
        )
        metadata = self._cache.put(
            subtopic_id=subtopic_id,
            textbook_hash=textbook_hash,
            curriculum_hash=curriculum_hash,
            planning_result=planning_result,
        )
        return KCPlanningResult(
            subtopic_id=planning_result.subtopic_id,
            topic_key=planning_result.topic_key,
            atomic_objectives=planning_result.atomic_objectives,
            kc_plans=planning_result.kc_plans,
            step_evidence_plans=planning_result.step_evidence_plans,
            assessment_items_by_atomic_objective=planning_result.assessment_items_by_atomic_objective,
            assessment_items=planning_result.assessment_items,
            lesson_structure=planning_result.lesson_structure,
            combined_kc_plan=planning_result.combined_kc_plan,
            resolved_kcs=planning_result.resolved_kcs,
            violations_by_atomic_objective=planning_result.violations_by_atomic_objective,
            violations=planning_result.violations,
            from_cache=False,
            cache_metadata=metadata,
            planning_duration_ms=planning_result.planning_duration_ms,
            llm_calls_planning=planning_result.llm_calls_planning,
        )

    def process(
        self,
        *,
        planning: KCPlanningResult,
        drafting: LessonDraftResult,
    ) -> SubtopicResult:
        is_valid = not any(violation.severity == "error" for violation in planning.violations)
        return SubtopicResult(
            planning=planning,
            drafting=drafting,
            violations=planning.violations,
            is_valid=is_valid,
            cached_planning=planning.from_cache,
        )

    def _build_atomic_objective_assessments(
        self,
        *,
        kc_plan: CandidateKCPlan,
        textbook_records: list[JsonObject],
    ) -> tuple[list[AssessmentItem], int]:
        assessments: list[AssessmentItem] = []
        llm_calls = 0
        for candidate_kc in kc_plan.candidate_kcs:
            source_records = select_textbook_records(
                candidate_kc.supporting_record_ids,
                textbook_records,
            )
            exercise_records = [
                record
                for record in source_records
                if str(record.get("record_type") or "").strip() in PRACTICE_SUPPORT_TYPES
            ]
            assessments.append(
                self._assessment_designer(
                    kc=candidate_kc,
                    source_records=source_records,
                    exercise_records=exercise_records,
                    lesson_objective_id=None,
                )
            )
            llm_calls += getattr(self._assessment_designer, "last_llm_calls", 1)
        return assessments, llm_calls

    def _build_step_evidence_plans(
        self,
        *,
        lesson_structure: LessonStructure,
        textbook_records: list[JsonObject],
    ) -> dict[str, StepEvidencePlan]:
        evidence_plans: dict[str, StepEvidencePlan] = {}
        for lesson_objective in lesson_structure.objectives:
            lesson_objective_id = lesson_objective.lesson_objective_id
            candidate_kc = lesson_structure.kcs_by_objective_id[lesson_objective_id]
            evidence_plan = build_supported_evidence_plan(
                lesson_objective=lesson_objective,
                candidate_kc=candidate_kc,
                textbook_records=textbook_records,
            )
            if evidence_plan is None:
                raise ValueError(
                    "unable to build cached evidence plan for lesson objective: "
                    f"{lesson_objective_id}"
                )
            evidence_plans[lesson_objective_id] = evidence_plan
        return evidence_plans

    def _map_assessments_to_lesson_objectives(
        self,
        *,
        lesson_structure: LessonStructure,
        kc_plans: dict[str, CandidateKCPlan],
        assessment_items_by_atomic_objective: dict[str, list[AssessmentItem]],
        textbook_records: list[JsonObject],
    ) -> tuple[dict[str, AssessmentItem], int]:
        candidate_pairs: list[tuple[CandidateKC, AssessmentItem]] = []
        for atomic_objective_id, kc_plan in kc_plans.items():
            objective_assessments = assessment_items_by_atomic_objective.get(
                atomic_objective_id,
                [],
            )
            for candidate_kc, assessment_item in zip(
                kc_plan.candidate_kcs,
                objective_assessments,
                strict=False,
            ):
                candidate_pairs.append((candidate_kc, assessment_item))

        by_curriculum_objective: dict[str, list[tuple[CandidateKC, AssessmentItem]]] = {}
        for candidate_kc, assessment_item in candidate_pairs:
            by_curriculum_objective.setdefault(candidate_kc.curriculum_objective_id, []).append(
                (candidate_kc, assessment_item)
            )

        lesson_assessments: dict[str, AssessmentItem] = {}
        fallback_calls = 0
        for lesson_objective in lesson_structure.objectives:
            resolved_kc = lesson_structure.kcs_by_objective_id[lesson_objective.lesson_objective_id]
            candidates = by_curriculum_objective.get(resolved_kc.curriculum_objective_id, [])
            if candidates:
                matched_candidate_kc, matched_item = max(
                    candidates,
                    key=lambda item: self._assessment_alignment_score(resolved_kc, item[0]),
                )
                lesson_assessments[lesson_objective.lesson_objective_id] = matched_item.model_copy(
                    update={
                        "kc_id": matched_candidate_kc.kc_id,
                        "lesson_objective_id": lesson_objective.lesson_objective_id,
                    }
                )
                continue

            source_records = select_textbook_records(
                resolved_kc.supporting_record_ids,
                textbook_records,
            )
            exercise_records = [
                record
                for record in source_records
                if str(record.get("record_type") or "").strip() in PRACTICE_SUPPORT_TYPES
            ]
            lesson_assessments[lesson_objective.lesson_objective_id] = self._assessment_designer(
                kc=resolved_kc,
                source_records=source_records,
                exercise_records=exercise_records,
                lesson_objective_id=lesson_objective.lesson_objective_id,
            )
            fallback_calls += getattr(self._assessment_designer, "last_llm_calls", 1)
        return lesson_assessments, fallback_calls

    def _assessment_alignment_score(
        self,
        resolved_kc: CandidateKC,
        candidate_kc: CandidateKC,
    ) -> tuple[int, int, int]:
        support_overlap = len(
            set(resolved_kc.supporting_record_ids) & set(candidate_kc.supporting_record_ids)
        )
        focus_overlap = len(_token_set(resolved_kc.kc_focus) & _token_set(candidate_kc.kc_focus))
        same_type = int(resolved_kc.kc_type == candidate_kc.kc_type)
        return same_type, support_overlap, focus_overlap
