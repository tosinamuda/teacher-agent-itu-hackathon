"""Review triage for manually authored AO-to-textbook linkage rows.

This module does not classify rows itself. Manually authored review categories
travel inside each linkage row payload (`review_categories`, `category_reasons`,
and per-AO `evidence_classification` / `review_categories`). This module only
reads those fields and aggregates them into an auditable triage report.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass

from app.domains.expert_content.application.linkage_models import (
    AtomicObjectiveLinkage,
    CandidateAtomicObjective,
    JsonObject,
    ManualSubtopicLinkageRow,
    ReviewCategory,
)

REVIEW_CATEGORY_DESCRIPTIONS: dict[ReviewCategory, str] = {
    "ambiguous_record_scope": (
        "One or more linked textbook records require expert judgment before assignment, "
        "usually because the record scope, direction, or skill does not map cleanly to an AO."
    ),
    "ao_no_evidence": (
        "One or more atomic objectives have no accepted textbook records in this row."
    ),
    "candidate_new_atomic_objective": (
        "One or more inspected textbook records teach a measurable skill that does "
        "not directly match the current atomic objectives and should be reviewed "
        "as a candidate AO proposal."
    ),
    "no_reused_assessment": (
        "One or more atomic objectives cannot reuse a source exercise_item as an assessment."
    ),
    "corpus_gap": "The linked textbook corpus has no records for this subtopic.",
    "curriculum_textbook_mismatch": (
        "The curriculum AO scope and the linked textbook record scope diverge."
    ),
    "prerequisite_only_evidence": (
        "The textbook includes prerequisite or foundation content, but that content does "
        "not directly satisfy the atomic objective."
    ),
}


@dataclass(frozen=True)
class AtomicObjectiveReviewTriage:
    ao_id: str
    categories: list[ReviewCategory]
    record_link_count: int
    linked_roles: list[str]
    has_assessment: bool
    evidence_classification: str | None

    def as_json(self) -> JsonObject:
        return asdict(self)


@dataclass(frozen=True)
class CandidateAtomicObjectiveReviewTriage:
    candidate_ao_id: str
    candidate_kind: str
    proposed_objective_text: str
    bloom_level: str
    source_record_count: int
    source_record_ids: list[str]
    closest_existing_ao_ids: list[str]
    status: str

    def as_json(self) -> JsonObject:
        return asdict(self)


@dataclass(frozen=True)
class ManualLinkageRowReviewTriage:
    subtopic_id: str
    status: str
    categories: list[ReviewCategory]
    category_reasons: dict[ReviewCategory, str]
    review_item_count: int
    review_item_issue_counts: dict[str, int]
    atomic_objectives: list[AtomicObjectiveReviewTriage]
    candidate_atomic_objectives: list[CandidateAtomicObjectiveReviewTriage]
    candidate_atomic_objective_review: JsonObject | None

    def as_json(self) -> JsonObject:
        payload = asdict(self)
        payload["atomic_objectives"] = [item.as_json() for item in self.atomic_objectives]
        payload["candidate_atomic_objectives"] = [
            item.as_json() for item in self.candidate_atomic_objectives
        ]
        return payload


def triage_manual_linkage_row(row_payload: JsonObject) -> ManualLinkageRowReviewTriage:
    """Read manually authored review metadata from a single linkage row."""
    row = ManualSubtopicLinkageRow.model_validate(row_payload)
    category_reasons: dict[ReviewCategory, str] = {
        item.category: item.reason for item in row.category_reasons
    }
    categories: list[ReviewCategory] = sorted(set(row.review_categories))

    return ManualLinkageRowReviewTriage(
        subtopic_id=row.subtopic_id,
        status=row.status,
        categories=categories,
        category_reasons={
            category: category_reasons[category]
            for category in categories
            if category in category_reasons
        },
        review_item_count=len(row.review_items),
        review_item_issue_counts=dict(
            sorted(Counter(item.issue for item in row.review_items).items())
        ),
        atomic_objectives=[_triage_atomic_objective(ao) for ao in row.atomic_objectives],
        candidate_atomic_objectives=[
            _triage_candidate_atomic_objective(candidate)
            for candidate in row.candidate_atomic_objectives
        ],
        candidate_atomic_objective_review=(
            row.candidate_atomic_objective_review.model_dump()
            if row.candidate_atomic_objective_review is not None
            else None
        ),
    )


def build_atomic_objective_rollup(row_payloads: list[JsonObject]) -> JsonObject:
    """Aggregate AO-level totals across all manual linkage row payloads.

    The rollup is derived purely from the manually authored fields in each
    `atomic_objectives[*]` block (`evidence_classification`, `review_categories`,
    and the presence of an `assessment`). It performs no semantic inference.
    """
    total_aos = 0
    evidence_counts: Counter[str] = Counter()
    review_category_counts: Counter[str] = Counter()
    assessment_null = 0
    for row_payload in row_payloads:
        row = ManualSubtopicLinkageRow.model_validate(row_payload)
        for ao in row.atomic_objectives:
            total_aos += 1
            evidence_counts[ao.evidence_classification or "unclassified"] += 1
            for category in ao.review_categories:
                review_category_counts[category] += 1
            if ao.assessment is None:
                assessment_null += 1
    return {
        "total_atomic_objectives": total_aos,
        "evidence_classification_counts": dict(sorted(evidence_counts.items())),
        "review_category_counts": dict(sorted(review_category_counts.items())),
        "atomic_objectives_without_assessment": assessment_null,
    }


def build_candidate_atomic_objective_rollup(row_payloads: list[JsonObject]) -> JsonObject:
    """Aggregate candidate-AO proposal totals from row-authored payloads."""
    total_candidates = 0
    kind_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    source_record_count = 0
    rows_with_candidates: list[JsonObject] = []

    for row_payload in row_payloads:
        row = ManualSubtopicLinkageRow.model_validate(row_payload)
        if not row.candidate_atomic_objectives:
            continue

        row_source_record_count = 0
        candidate_ids: list[str] = []
        candidate_kinds: list[str] = []
        for candidate in row.candidate_atomic_objectives:
            total_candidates += 1
            kind_counts[candidate.candidate_kind] += 1
            status_counts[candidate.status] += 1
            candidate_source_record_count = len(candidate.source_record_ids)
            source_record_count += candidate_source_record_count
            row_source_record_count += candidate_source_record_count
            candidate_ids.append(candidate.candidate_ao_id)
            candidate_kinds.append(candidate.candidate_kind)

        rows_with_candidates.append(
            {
                "subtopic_id": row.subtopic_id,
                "candidate_count": len(row.candidate_atomic_objectives),
                "candidate_ao_ids": candidate_ids,
                "candidate_kinds": sorted(set(candidate_kinds)),
                "source_record_count": row_source_record_count,
            }
        )

    return {
        "total_candidate_atomic_objectives": total_candidates,
        "candidate_kind_counts": dict(sorted(kind_counts.items())),
        "candidate_status_counts": dict(sorted(status_counts.items())),
        "candidate_source_record_count": source_record_count,
        "rows_with_candidates": rows_with_candidates,
    }


def build_manual_linkage_review_triage_report(
    row_payloads: list[JsonObject],
    *,
    generated_at: str,
) -> JsonObject:
    """Build an auditable review-triage report from validated linkage rows."""
    triage_rows = [triage_manual_linkage_row(row_payload) for row_payload in row_payloads]
    status_counts = Counter(row.status for row in triage_rows)
    category_counts: Counter[str] = Counter(
        category for row in triage_rows for category in row.categories
    )
    ao_rollup = build_atomic_objective_rollup(row_payloads)
    candidate_rollup = build_candidate_atomic_objective_rollup(row_payloads)

    return {
        "schema_version": "manual-ao-textbook-linkage-review-triage-v2",
        "generated_at": generated_at,
        "row_count": len(triage_rows),
        "status_counts": dict(sorted(status_counts.items())),
        "category_descriptions": REVIEW_CATEGORY_DESCRIPTIONS,
        "category_counts": dict(sorted(category_counts.items())),
        "atomic_objective_rollup": ao_rollup,
        "candidate_atomic_objective_rollup": candidate_rollup,
        "rows": [row.as_json() for row in triage_rows],
    }


def _triage_atomic_objective(
    atomic_objective: AtomicObjectiveLinkage,
) -> AtomicObjectiveReviewTriage:
    record_links = list(atomic_objective.record_links)
    linked_roles: list[str] = [str(link.role) for link in record_links]
    has_assessment = atomic_objective.assessment is not None
    return AtomicObjectiveReviewTriage(
        ao_id=atomic_objective.ao_id,
        categories=sorted(set(atomic_objective.review_categories)),
        record_link_count=len(record_links),
        linked_roles=linked_roles,
        has_assessment=has_assessment,
        evidence_classification=atomic_objective.evidence_classification,
    )


def _triage_candidate_atomic_objective(
    candidate: CandidateAtomicObjective,
) -> CandidateAtomicObjectiveReviewTriage:
    return CandidateAtomicObjectiveReviewTriage(
        candidate_ao_id=candidate.candidate_ao_id,
        candidate_kind=candidate.candidate_kind,
        proposed_objective_text=candidate.proposed_objective_text,
        bloom_level=candidate.bloom_level,
        source_record_count=len(candidate.source_record_ids),
        source_record_ids=list(candidate.source_record_ids),
        closest_existing_ao_ids=list(candidate.closest_existing_ao_ids),
        status=candidate.status,
    )
