"""Validate a manual linkage row against its source atomic-objective + records.

Top-level entry: ``validate_manual_linkage_row``. Internally it coordinates 6
row-level checks and 5 per-atomic-objective checks (each ``_check_*`` helper
owns one validation concern, behaviour-preserving from the original 800-line
monolith). Imports from ``linkage_models`` for the typed row + return shape,
and from ``linkage_inference`` for bloom-level/AO-flatten helpers.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import cast

from app.domains.expert_content.application.linkage_inference import (
    flatten_atomic_objectives,
    infer_bloom_level,
    infer_bloom_verb,
)
from app.domains.expert_content.application.linkage_models import (
    AtomicObjectiveLinkage,
    BlockType,
    BloomLevel,
    JsonObject,
    ManualLinkageValidationReport,
    ManualSubtopicLinkageRow,
)
from app.domains.expert_content.domain.types import AoTextbookLinkageStatus

# ----- Small pure helpers shared by several checks -----


def _unique_duplicates(items: list[str]) -> list[str]:
    """Return the sorted-unique items that appear more than once."""
    return sorted(item for item, count in Counter(items).items() if count > 1)


def _record_id_list(items: list[JsonObject], key: str) -> list[str]:
    """Extract stripped non-empty string values for ``key`` across ``items``."""
    ids: list[str] = []
    for item in items:
        value = str(item.get(key) or "").strip()
        if value:
            ids.append(value)
    return ids


def _assessment_pool_ids(
    *,
    exercise_ids: list[str],
    practice_ids: list[str],
) -> list[str]:
    """Exercise records that are NOT already serving as practice — the assessment pool."""
    practice_set = set(practice_ids)
    return [record_id for record_id in exercise_ids if record_id not in practice_set]


def _expected_practice_ids(exercise_ids: list[str]) -> list[str]:
    """Derive the expected practice subset: 2 of 3+, 1 of 2, else empty."""
    if len(exercise_ids) >= 3:
        return exercise_ids[:2]
    if len(exercise_ids) == 2:
        return exercise_ids[:1]
    return []


def _expected_block_types(
    *,
    has_worked_example: bool,
    has_practice: bool,
) -> list[BlockType]:
    """Derive the expected ``block_types`` for an AO from what its links contain."""
    block_types: list[BlockType] = ["explanation"]
    if has_worked_example:
        block_types.append("worked_example")
    if has_practice:
        block_types.append("practice")
    return block_types


# ----- Row-level checks -----


def _check_identity(
    row: ManualSubtopicLinkageRow,
    atomic_objective_source: JsonObject,
    source_ao_ids: list[str],
) -> list[str]:
    """Subtopic id/title + AO order must match the source row exactly."""
    errors: list[str] = []
    if row.subtopic_id != str(atomic_objective_source.get("subtopic_id") or "").strip():
        errors.append("subtopic_id does not match the atomic-objective source row")
    if row.subtopic_title != str(atomic_objective_source.get("subtopic_title") or "").strip():
        errors.append("subtopic_title does not match the atomic-objective source row")
    if [item.ao_id for item in row.atomic_objectives] != source_ao_ids:
        errors.append("atomic_objectives order does not match the source AO order")
    return errors


def _check_duplicate_record_ids(
    shared_ids: list[str],
    linked_ids: list[str],
    excluded_ids: list[str],
    review_ids: list[str],
    candidate_ids: list[str],
) -> list[str]:
    """No category of record ids may contain duplicates."""
    errors: list[str] = []
    duplicate_shared = _unique_duplicates(shared_ids)
    duplicate_linked = _unique_duplicates(linked_ids)
    duplicate_excluded = _unique_duplicates(excluded_ids)
    duplicate_review = _unique_duplicates(review_ids)
    duplicate_candidates = _unique_duplicates(candidate_ids)
    if duplicate_shared:
        errors.append(f"shared_foundation_record_ids contains duplicates: {duplicate_shared}")
    if duplicate_linked:
        errors.append(f"record_links contains duplicate record ids: {duplicate_linked}")
    if duplicate_excluded:
        errors.append(f"excluded_records contains duplicates: {duplicate_excluded}")
    if duplicate_review:
        errors.append(f"review_items contains duplicates: {duplicate_review}")
    if duplicate_candidates:
        errors.append(f"candidate_atomic_objectives contains duplicate ids: {duplicate_candidates}")
    return errors


def _check_membership_and_overlap(
    shared_set: set[str],
    linked_set: set[str],
    excluded_set: set[str],
    review_set: set[str],
    source_record_id_set: set[str],
) -> list[str]:
    """Every record id known + categories disjoint + every source row accounted for."""
    errors: list[str] = []
    for category_name, record_ids in {
        "shared_foundation_record_ids": shared_set,
        "record_links": linked_set,
        "excluded_records": excluded_set,
        "review_items": review_set,
    }.items():
        unknown = sorted(record_ids - source_record_id_set)
        if unknown:
            errors.append(f"{category_name} contains unknown record ids: {unknown}")

    for left_name, left_set in {
        "shared_foundation_record_ids": shared_set,
        "record_links": linked_set,
        "excluded_records": excluded_set,
        "review_items": review_set,
    }.items():
        for right_name, right_set in {
            "shared_foundation_record_ids": shared_set,
            "record_links": linked_set,
            "excluded_records": excluded_set,
            "review_items": review_set,
        }.items():
            if left_name >= right_name:
                continue
            overlap = sorted(left_set & right_set)
            if overlap:
                errors.append(f"{left_name} and {right_name} overlap: {overlap}")

    accounted_ids = shared_set | linked_set | excluded_set | review_set
    missing_record_ids = sorted(source_record_id_set - accounted_ids)
    extra_record_ids = sorted(accounted_ids - source_record_id_set)
    if missing_record_ids:
        errors.append(f"source records not accounted for: {missing_record_ids}")
    if extra_record_ids:
        errors.append(f"accounted record ids missing from source input: {extra_record_ids}")
    return errors


def _check_status(row: ManualSubtopicLinkageRow, source_record_ids: list[str]) -> list[str]:
    """Status must agree with (presence of review items, presence of source records)."""
    errors: list[str] = []
    if row.review_items and row.status == AoTextbookLinkageStatus.MAPPED:
        errors.append("status='mapped' is invalid when review_items are present")
    if not source_record_ids and row.status != AoTextbookLinkageStatus.NO_RECORDS:
        errors.append("status must be 'no_records' when the source record set is empty")
    if source_record_ids and row.status == AoTextbookLinkageStatus.NO_RECORDS:
        errors.append("status='no_records' is invalid when source records exist")
    return errors


def _check_candidate_categories_consistency(
    row: ManualSubtopicLinkageRow, row_category_set: set[str]
) -> list[str]:
    """Candidate AOs ↔ ``candidate_new_atomic_objective`` flag ↔ verdict must agree."""
    errors: list[str] = []
    if row.candidate_atomic_objectives:
        if "candidate_new_atomic_objective" not in row_category_set:
            errors.append(
                "candidate_atomic_objectives require "
                "review_categories to include candidate_new_atomic_objective"
            )
        if row.candidate_atomic_objective_review is None:
            errors.append("candidate_atomic_objectives require candidate review metadata")
        elif row.candidate_atomic_objective_review.verdict != "has_candidates":
            errors.append(
                "candidate_atomic_objective_review verdict must be "
                "'has_candidates' when candidate proposals exist"
            )
    elif "candidate_new_atomic_objective" in row_category_set:
        errors.append(
            "review category candidate_new_atomic_objective requires at least "
            "one candidate_atomic_objectives entry"
        )
    elif (
        row.candidate_atomic_objective_review is not None
        and row.candidate_atomic_objective_review.verdict == "has_candidates"
    ):
        errors.append(
            "candidate_atomic_objective_review verdict 'has_candidates' requires "
            "candidate proposals"
        )
    return errors


def _check_needs_review_metadata(row: ManualSubtopicLinkageRow) -> list[str]:
    """``needs_review`` rows require a recorded + reviewed candidate-AO verdict."""
    errors: list[str] = []
    if row.status == AoTextbookLinkageStatus.NEEDS_REVIEW:
        if row.candidate_atomic_objective_review is None:
            errors.append("needs_review rows require candidate review metadata")
        elif not row.candidate_atomic_objective_review.reviewed:
            errors.append("candidate_atomic_objective_review.reviewed must be true")
    return errors


def _check_category_reasons_complete(
    row: ManualSubtopicLinkageRow, row_category_set: set[str]
) -> list[str]:
    """Every review category needs a matching ``category_reasons`` entry."""
    category_reason_set = {item.category for item in row.category_reasons}
    missing_category_reasons = sorted(row_category_set - category_reason_set)
    if not missing_category_reasons:
        return []
    return [f"review_categories missing category_reasons entries: {missing_category_reasons}"]


def _check_review_metadata(row: ManualSubtopicLinkageRow, row_category_set: set[str]) -> list[str]:
    """Compose the three review-metadata checks (candidate consistency, needs-review, reasons)."""
    return (
        _check_candidate_categories_consistency(row, row_category_set)
        + _check_needs_review_metadata(row)
        + _check_category_reasons_complete(row, row_category_set)
    )


def _check_candidate_objectives(
    row: ManualSubtopicLinkageRow,
    source_record_id_set: set[str],
    excluded_set: set[str],
    source_record_map: dict[str, JsonObject],
    source_ao_ids: list[str],
) -> list[str]:
    """Per-candidate AO: duplicates/unknown/excluded sources, evidence quote, bloom inference."""
    errors: list[str] = []
    for candidate in row.candidate_atomic_objectives:
        candidate_source_ids = list(candidate.source_record_ids)
        duplicate_candidate_source_ids = _unique_duplicates(candidate_source_ids)
        if duplicate_candidate_source_ids:
            errors.append(
                "candidate "
                f"{candidate.candidate_ao_id} source_record_ids contains duplicates: "
                f"{duplicate_candidate_source_ids}"
            )

        unknown_candidate_source_ids = sorted(set(candidate_source_ids) - source_record_id_set)
        if unknown_candidate_source_ids:
            errors.append(
                f"candidate {candidate.candidate_ao_id} contains unknown "
                f"source_record_ids: {unknown_candidate_source_ids}"
            )

        excluded_candidate_source_ids = sorted(set(candidate_source_ids) & excluded_set)
        if excluded_candidate_source_ids:
            errors.append(
                f"candidate {candidate.candidate_ao_id} references excluded "
                f"record ids: {excluded_candidate_source_ids}"
            )

        candidate_evidence_sources = [
            source_record_map[record_id]
            for record_id in candidate_source_ids
            if record_id in source_record_map
        ]
        candidate_evidence_text = "\n".join(
            "\n".join(
                [
                    str(record.get("content_text") or ""),
                    str(record.get("prompt_text") or ""),
                    str(record.get("answer_text") or ""),
                ]
            )
            for record in candidate_evidence_sources
        )
        if candidate_evidence_sources and candidate.evidence_quote not in candidate_evidence_text:
            errors.append(
                f"candidate {candidate.candidate_ao_id} evidence_quote must appear "
                "in one of its source records"
            )

        unknown_closest_ao_ids = sorted(set(candidate.closest_existing_ao_ids) - set(source_ao_ids))
        if unknown_closest_ao_ids:
            errors.append(
                f"candidate {candidate.candidate_ao_id} contains unknown "
                f"closest_existing_ao_ids: {unknown_closest_ao_ids}"
            )

        expected_candidate_bloom_verb = infer_bloom_verb(candidate.proposed_objective_text)
        expected_candidate_bloom_level = infer_bloom_level(candidate.proposed_objective_text)
        if candidate.bloom_verb != expected_candidate_bloom_verb:
            errors.append(
                f"candidate {candidate.candidate_ao_id} bloom_verb should be "
                f"'{expected_candidate_bloom_verb}'"
            )
        if candidate.bloom_level != expected_candidate_bloom_level:
            errors.append(
                f"candidate {candidate.candidate_ao_id} bloom_level should be "
                f"'{expected_candidate_bloom_level}'"
            )
    return errors


# ----- Per-atomic-objective checks -----


def _check_ao_field_match(actual_ao: AtomicObjectiveLinkage, expected_ao: JsonObject) -> list[str]:
    """ao_order + curriculum-objective parent + AO text + bloom inference all match the source."""
    errors: list[str] = []
    if actual_ao.ao_order != int(expected_ao["ao_order"]):
        errors.append(f"AO {actual_ao.ao_id} ao_order does not match the source ordering")
    if actual_ao.curriculum_objective_id != str(expected_ao["curriculum_objective_id"]):
        errors.append(f"AO {actual_ao.ao_id} curriculum_objective_id mismatch")
    if actual_ao.curriculum_objective_text != str(expected_ao["curriculum_objective_text"]):
        errors.append(f"AO {actual_ao.ao_id} curriculum_objective_text mismatch")
    if actual_ao.text != str(expected_ao["text"]):
        errors.append(f"AO {actual_ao.ao_id} text mismatch")

    expected_bloom_verb = str(expected_ao["bloom_verb"])
    expected_bloom_level = cast(BloomLevel, expected_ao["bloom_level"])
    if actual_ao.bloom_verb != expected_bloom_verb:
        errors.append(f"AO {actual_ao.ao_id} bloom_verb should be '{expected_bloom_verb}'")
    if actual_ao.bloom_level != expected_bloom_level:
        errors.append(f"AO {actual_ao.ao_id} bloom_level should be '{expected_bloom_level}'")
    return errors


def _check_ao_practice(
    actual_ao: AtomicObjectiveLinkage,
    exercise_ids: list[str],
    source_record_index: dict[str, int],
) -> list[str]:
    """practice_record_ids must be <=2, subset of exercises, and in source order."""
    errors: list[str] = []
    if len(actual_ao.practice_record_ids) > 2:
        errors.append(f"AO {actual_ao.ao_id} practice_record_ids exceeds max length of 2")
    if any(record_id not in exercise_ids for record_id in actual_ao.practice_record_ids):
        errors.append(
            f"AO {actual_ao.ao_id} practice_record_ids must be a subset of exercise links"
        )
    practice_indices = [
        source_record_index[record_id] for record_id in actual_ao.practice_record_ids
    ]
    if practice_indices != sorted(practice_indices):
        errors.append(f"AO {actual_ao.ao_id} practice_record_ids are not in source order")
    expected_practice_ids = _expected_practice_ids(exercise_ids)
    if actual_ao.practice_record_ids != expected_practice_ids:
        errors.append(f"AO {actual_ao.ao_id} practice_record_ids should be {expected_practice_ids}")
    return errors


def _check_ao_block_types(
    actual_ao: AtomicObjectiveLinkage,
    exercise_ids: list[str],
    has_worked_example: bool,
) -> list[str]:
    """step_blueprint.block_types must match the value derived from links + practice."""
    errors: list[str] = []
    assessment_pool_ids = _assessment_pool_ids(
        exercise_ids=exercise_ids,
        practice_ids=actual_ao.practice_record_ids,
    )
    expected_block_types = _expected_block_types(
        has_worked_example=has_worked_example,
        has_practice=bool(actual_ao.practice_record_ids or assessment_pool_ids),
    )
    if actual_ao.step_blueprint.block_types != expected_block_types:
        errors.append(f"AO {actual_ao.ao_id} block_types should be {expected_block_types}")
    return errors


def _check_ao_reused_assessment(
    actual_ao: AtomicObjectiveLinkage, source_record_map: dict[str, JsonObject]
) -> list[str]:
    """Validate a reused assessment references an exercise_item with matching prompt + answer."""
    errors: list[str] = []
    if actual_ao.assessment is not None and actual_ao.assessment.method == "reused":
        source_exercise_id = str(actual_ao.assessment.source_exercise_id or "").strip()
        source_record = source_record_map.get(source_exercise_id)
        if source_record is None:
            errors.append(
                f"AO {actual_ao.ao_id} assessment references unknown exercise {source_exercise_id}"
            )
        else:
            source_record_type = str(source_record.get("record_type") or "").strip()
            if source_record_type != "exercise_item":
                errors.append(
                    f"AO {actual_ao.ao_id} reused assessment must reference an exercise_item"
                )
            source_prompt = str(source_record.get("prompt_text") or "")
            source_answer = str(source_record.get("answer_text") or "")
            if actual_ao.assessment.question != source_prompt:
                errors.append(
                    f"AO {actual_ao.ao_id} reused assessment question must match prompt_text"
                )
            if actual_ao.assessment.expected_answer != source_answer:
                errors.append(
                    f"AO {actual_ao.ao_id} reused assessment expected_answer must match answer_text"
                )
    return errors


@dataclass(frozen=True)
class _AORecordLinksState:
    """Per-AO derived state from walking ``record_links``: roles + exercises + flags + errors."""

    role_errors: list[str]
    exercise_ids: list[str]
    has_worked_example: bool


def _walk_ao_record_links(
    actual_ao: AtomicObjectiveLinkage,
    shared_set: set[str],
    source_record_index: dict[str, int],
) -> _AORecordLinksState:
    """Walk an AO's record_links once and derive (errors, exercise_ids, has_worked_example)."""
    errors: list[str] = []
    role_to_indices: dict[str, list[int]] = {}
    exercise_ids: list[str] = []
    has_worked_example = False
    for link in actual_ao.record_links:
        if link.record_id in shared_set:
            errors.append(
                f"AO {actual_ao.ao_id} references shared foundation record {link.record_id}"
            )
        record_index = source_record_index.get(link.record_id)
        if record_index is None:
            continue
        role_to_indices.setdefault(link.role, []).append(record_index)
        if link.role == "exercise":
            exercise_ids.append(link.record_id)
        if link.role == "worked_example":
            has_worked_example = True

    for role, indices in role_to_indices.items():
        if indices != sorted(indices):
            errors.append(f"AO {actual_ao.ao_id} role '{role}' is not in source textbook order")
    return _AORecordLinksState(
        role_errors=errors,
        exercise_ids=exercise_ids,
        has_worked_example=has_worked_example,
    )


def _check_ao_mapped_completeness(
    actual_ao: AtomicObjectiveLinkage, row: ManualSubtopicLinkageRow
) -> list[str]:
    """``status=mapped`` requires every AO to have at least one link + an assessment."""
    if row.status != AoTextbookLinkageStatus.MAPPED:
        return []
    errors: list[str] = []
    if not actual_ao.record_links:
        errors.append(f"AO {actual_ao.ao_id} has no accepted record links")
    if actual_ao.assessment is None:
        errors.append(f"AO {actual_ao.ao_id} is missing an assessment")
    return errors


def _check_one_atomic_objective(
    actual_ao: AtomicObjectiveLinkage,
    expected_ao: JsonObject,
    row: ManualSubtopicLinkageRow,
    shared_set: set[str],
    source_record_index: dict[str, int],
    source_record_map: dict[str, JsonObject],
) -> list[str]:
    """Compose all per-AO checks (fields, link ordering, practice, blocks, reused assessment)."""
    state = _walk_ao_record_links(actual_ao, shared_set, source_record_index)
    return (
        _check_ao_field_match(actual_ao, expected_ao)
        + state.role_errors
        + _check_ao_practice(actual_ao, state.exercise_ids, source_record_index)
        + _check_ao_block_types(actual_ao, state.exercise_ids, state.has_worked_example)
        + _check_ao_reused_assessment(actual_ao, source_record_map)
        + _check_ao_mapped_completeness(actual_ao, row)
    )


def _check_atomic_objective_links(
    row: ManualSubtopicLinkageRow,
    source_atomic_objectives: list[JsonObject],
    shared_set: set[str],
    source_record_index: dict[str, int],
    source_record_map: dict[str, JsonObject],
) -> list[str]:
    """Iterate the (source, row) AO pairs and run every per-AO check."""
    errors: list[str] = []
    for expected_ao, actual_ao in zip(
        source_atomic_objectives, row.atomic_objectives, strict=False
    ):
        errors += _check_one_atomic_objective(
            actual_ao, expected_ao, row, shared_set, source_record_index, source_record_map
        )
    return errors


# ----- Top-level orchestrator -----


def validate_manual_linkage_row(
    *,
    row_payload: JsonObject,
    atomic_objective_source: JsonObject,
    textbook_records: list[JsonObject],
) -> ManualLinkageValidationReport:
    """Validate a curated linkage row against its source AO + textbook records.

    The orchestrator builds the shared lookup state (record id lists, sets,
    index, map; AO order; row category set), runs each ``_check_*`` group, and
    rolls the errors + warnings into a ``ManualLinkageValidationReport``.
    """
    row = ManualSubtopicLinkageRow.model_validate(row_payload)
    source_record_ids = [str(record.get("record_id") or "").strip() for record in textbook_records]
    source_record_ids = [record_id for record_id in source_record_ids if record_id]
    source_record_id_set = set(source_record_ids)
    source_record_index = {record_id: index for index, record_id in enumerate(source_record_ids)}
    source_record_map = {
        str(record.get("record_id") or "").strip(): record for record in textbook_records
    }
    source_atomic_objectives = flatten_atomic_objectives(atomic_objective_source)
    source_ao_ids = [str(item["ao_id"]) for item in source_atomic_objectives]
    shared_ids = list(row.shared_foundation_record_ids)
    linked_ids = [link.record_id for ao in row.atomic_objectives for link in ao.record_links]
    excluded_ids = [item.record_id for item in row.excluded_records]
    review_ids = [item.record_id for item in row.review_items]
    candidate_ids = [item.candidate_ao_id for item in row.candidate_atomic_objectives]
    shared_set = set(shared_ids)
    linked_set = set(linked_ids)
    excluded_set = set(excluded_ids)
    review_set = set(review_ids)
    row_category_set: set[str] = {str(category) for category in row.review_categories}

    errors: list[str] = []
    errors += _check_identity(row, atomic_objective_source, source_ao_ids)
    errors += _check_duplicate_record_ids(
        shared_ids, linked_ids, excluded_ids, review_ids, candidate_ids
    )
    errors += _check_membership_and_overlap(
        shared_set, linked_set, excluded_set, review_set, source_record_id_set
    )
    errors += _check_status(row, source_record_ids)
    errors += _check_review_metadata(row, row_category_set)
    errors += _check_candidate_objectives(
        row, source_record_id_set, excluded_set, source_record_map, source_ao_ids
    )
    errors += _check_atomic_objective_links(
        row, source_atomic_objectives, shared_set, source_record_index, source_record_map
    )

    warnings: list[str] = []
    if row.status == AoTextbookLinkageStatus.MAPPED and row.status_reasons:
        warnings.append("status_reasons is non-empty for a mapped row")

    return ManualLinkageValidationReport(
        valid=not errors,
        errors=errors,
        warnings=warnings,
        total_source_records=len(source_record_ids),
        assigned_record_count=len(linked_set | shared_set),
        shared_foundation_count=len(shared_set),
        excluded_record_count=len(excluded_set),
        review_record_count=len(review_set),
    )
