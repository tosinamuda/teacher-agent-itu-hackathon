from __future__ import annotations

from app.domains.artefacts.types.lesson_plan.drafting.application.precompute.types import (
    ObjectiveContext,
    Violation,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.bloom import bloom_level_rank
from app.domains.artefacts.types.lesson_plan.drafting.domain.textbook import textbook_record_id
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.textbook_support import (
    CONCEPT_SUPPORT_TYPES,
    MODELING_SUPPORT_TYPES,
    PRACTICE_SUPPORT_TYPES,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import CandidateKCPlan


class DecompositionVerifier:
    """Algorithmic checks on KC decomposition output."""

    def verify_all(
        self,
        decomposition: CandidateKCPlan,
        context: ObjectiveContext,
    ) -> list[Violation]:
        return [
            *self.check_source_ids_exist(decomposition, context),
            *self.check_bloom_coverage(decomposition, context),
            *self.check_type_consistency(decomposition, context),
            *self.check_dag_acyclic(decomposition, context),
        ]

    def check_source_ids_exist(
        self,
        decomposition: CandidateKCPlan,
        context: ObjectiveContext,
    ) -> list[Violation]:
        valid_record_ids = {
            textbook_record_id(record)
            for record in context.primary_records
            if textbook_record_id(record)
        }
        violations: list[Violation] = []
        for candidate_kc in decomposition.candidate_kcs:
            missing_ids = sorted(set(candidate_kc.supporting_record_ids) - valid_record_ids)
            if not missing_ids:
                continue
            violations.append(
                Violation(
                    code="source_id_not_found",
                    message=(
                        f"KC {candidate_kc.kc_id} references missing textbook records: "
                        f"{missing_ids}"
                    ),
                    atomic_objective_id=context.atomic_objective.atomic_objective_id,
                    kc_id=candidate_kc.kc_id,
                )
            )
        return violations

    def check_bloom_coverage(
        self,
        decomposition: CandidateKCPlan,
        context: ObjectiveContext,
    ) -> list[Violation]:
        taught_kcs = [
            candidate_kc
            for candidate_kc in decomposition.candidate_kcs
            if not candidate_kc.is_prior_knowledge
        ]
        if not taught_kcs:
            return [
                Violation(
                    code="bloom_coverage_gap",
                    message="All extracted KCs were marked as prior knowledge.",
                    atomic_objective_id=context.atomic_objective.atomic_objective_id,
                )
            ]
        target_rank = bloom_level_rank(context.atomic_objective.bloom_level)
        best_rank = max(bloom_level_rank(candidate_kc.bloom_level) for candidate_kc in taught_kcs)
        if best_rank >= target_rank:
            return []
        return [
            Violation(
                code="bloom_coverage_gap",
                message=(
                    "No extracted KC reaches the target Bloom level "
                    f"{context.atomic_objective.bloom_level}."
                ),
                atomic_objective_id=context.atomic_objective.atomic_objective_id,
            )
        ]

    def check_type_consistency(
        self,
        decomposition: CandidateKCPlan,
        context: ObjectiveContext,
    ) -> list[Violation]:
        record_types = {
            textbook_record_id(record): str(record.get("record_type") or "").strip()
            for record in context.primary_records
            if textbook_record_id(record)
        }
        violations: list[Violation] = []
        for candidate_kc in decomposition.candidate_kcs:
            support_types = {
                record_types[record_id]
                for record_id in candidate_kc.supporting_record_ids
                if record_id in record_types
            }
            if (
                candidate_kc.kc_type == "concept"
                and support_types
                and support_types <= (PRACTICE_SUPPORT_TYPES | MODELING_SUPPORT_TYPES)
            ):
                violations.append(
                    Violation(
                        code="type_inconsistency",
                        message=(
                            f"KC {candidate_kc.kc_id} is typed as concept but only cites "
                            "modeling or practice records."
                        ),
                        atomic_objective_id=context.atomic_objective.atomic_objective_id,
                        kc_id=candidate_kc.kc_id,
                    )
                )
            if candidate_kc.kc_type in {"procedure", "representation"}:
                has_concept_support = bool(support_types & CONCEPT_SUPPORT_TYPES)
                has_model_or_practice = bool(
                    support_types & (MODELING_SUPPORT_TYPES | PRACTICE_SUPPORT_TYPES)
                )
                if has_concept_support and has_model_or_practice:
                    continue
                violations.append(
                    Violation(
                        code="type_inconsistency",
                        message=(
                            f"KC {candidate_kc.kc_id} is typed as {candidate_kc.kc_type} "
                            "without both concept and modeling/practice support."
                        ),
                        atomic_objective_id=context.atomic_objective.atomic_objective_id,
                        kc_id=candidate_kc.kc_id,
                    )
                )
        return violations

    def check_dag_acyclic(
        self,
        decomposition: CandidateKCPlan,
        context: ObjectiveContext,
    ) -> list[Violation]:
        graph = {
            candidate_kc.kc_id: list(candidate_kc.prerequisite_kc_ids)
            for candidate_kc in decomposition.candidate_kcs
        }
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str) -> bool:
            if node in visited:
                return False
            if node in visiting:
                return True
            visiting.add(node)
            for neighbor in graph.get(node, []):
                if visit(neighbor):
                    return True
            visiting.remove(node)
            visited.add(node)
            return False

        for node in graph:
            if visit(node):
                return [
                    Violation(
                        code="dag_cycle",
                        message="KC prerequisite graph contains a cycle.",
                        atomic_objective_id=context.atomic_objective.atomic_objective_id,
                    )
                ]
        return []
