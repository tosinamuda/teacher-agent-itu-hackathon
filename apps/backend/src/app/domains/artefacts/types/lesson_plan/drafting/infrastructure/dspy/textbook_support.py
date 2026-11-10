"""Resolve which textbook records support a candidate KC.

Two responsibilities, both keyed on the KC's ``supporting_record_ids`` and the
loaded textbook records:

- **Inventory**: classify the supporting records into concept / worked-example /
  exercise-item / exercise-block / visual buckets so downstream steps know what
  evidence shapes are available.
- **Supplementation**: if a KC's stated support is missing a required type
  (concept always, plus worked-example + practice for procedure/representation
  KCs), find the best matching record from the pool and add it.

``select_textbook_records`` is the small public lookup helper used by other
modules; the public ``normalize_candidate_kcs_for_support`` is what the
pipeline calls to ensure each KC has the support its type requires.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence

from app.domains.artefacts.types.lesson_plan.drafting.domain.textbook import textbook_record_id
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.model_io import (
    to_record_object,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import CandidateKC
from app.shared.json_types import JsonObject

CONCEPT_SUPPORT_TYPES = {"definition", "exposition", "summary", "note"}
MODELING_FALLBACK_TYPES = {"exercise_item"}
MODELING_SUPPORT_TYPES = {"worked_example", *MODELING_FALLBACK_TYPES}
PRACTICE_SUPPORT_TYPES = {"exercise_block", "exercise_item"}
SUPPORT_RECORD_TYPE_PRIORITY = {
    "definition": 0,
    "exposition": 1,
    "summary": 2,
    "note": 3,
    "worked_example": 4,
    "exercise_block": 5,
    "exercise_item": 6,
}
SUPPORT_TOKEN_RE = re.compile(r"[a-z0-9]+")
SUPPORT_STOPWORDS = {
    "and",
    "for",
    "from",
    "into",
    "that",
    "the",
    "their",
    "them",
    "this",
    "with",
}


def select_textbook_records(
    selected_ids: list[str],
    textbook_records: Sequence[Mapping[str, object]],
) -> list[JsonObject]:
    """Return only the records whose id appears in ``selected_ids`` (preserving order)."""
    record_map = {
        textbook_record_id(record): to_record_object(record) for record in textbook_records
    }
    selected: list[JsonObject] = []
    for record_id in selected_ids:
        record = record_map.get(record_id)
        if record is not None:
            selected.append(record)
    return selected


def kc_support_inventory(
    candidate_kc: CandidateKC,
    textbook_records: Sequence[Mapping[str, object]],
) -> dict[str, list[str]]:
    """Bucket a KC's supporting records into concept / worked-example / exercise / visual lists."""
    record_map = {
        textbook_record_id(record): to_record_object(record)
        for record in textbook_records
        if textbook_record_id(record)
    }
    support_ids = [
        record_id for record_id in candidate_kc.supporting_record_ids if record_id in record_map
    ]

    def ids_for_types(*allowed_types: str) -> list[str]:
        return [
            record_id
            for record_id in support_ids
            if str(record_map[record_id].get("record_type") or "").strip() in allowed_types
        ]

    return {
        "support_ids": support_ids,
        "concept_ids": ids_for_types(*sorted(CONCEPT_SUPPORT_TYPES)),
        "worked_example_ids": ids_for_types("worked_example"),
        "exercise_item_ids": ids_for_types("exercise_item"),
        "exercise_block_ids": ids_for_types("exercise_block"),
        "practice_ids": ids_for_types(*sorted(PRACTICE_SUPPORT_TYPES)),
        "visual_ids": [
            record_id
            for record_id in support_ids
            if _record_has_grounded_image(record_map[record_id])
        ],
    }


def normalize_candidate_kcs_for_support(
    candidate_kcs: list[CandidateKC],
    *,
    textbook_records: Sequence[Mapping[str, object]],
) -> list[CandidateKC]:
    """Supplement each KC's support set + downgrade unrealistic procedure/representation KCs."""
    normalized: list[CandidateKC] = []
    for original_kc in candidate_kcs:
        candidate_kc = _supplement_candidate_kc_support_ids(
            original_kc,
            textbook_records=textbook_records,
        )
        inventory = kc_support_inventory(candidate_kc, textbook_records)
        if candidate_kc.kc_type not in {"procedure", "representation"}:
            normalized.append(candidate_kc)
            continue
        has_concept_support = bool(inventory["concept_ids"])
        has_modeling_support = bool(
            inventory["worked_example_ids"] or inventory["exercise_item_ids"]
        )
        has_practice_support = bool(inventory["practice_ids"])
        if has_concept_support and not (has_modeling_support and has_practice_support):
            normalized.append(candidate_kc.model_copy(update={"kc_type": "concept"}))
            continue
        normalized.append(candidate_kc)
    return normalized


# ===== Private helpers =====


def _record_has_grounded_image(record: JsonObject) -> bool:
    """Whether ``record`` carries an image asset (flag, count, or asset_refs entry)."""
    if bool(record.get("has_image_asset")):
        return True
    count_value = record.get("image_asset_count")
    if isinstance(count_value, (int, float, str)):
        try:
            if int(count_value) > 0:
                return True
        except (TypeError, ValueError):
            pass
    asset_refs = record.get("asset_refs")
    if not isinstance(asset_refs, list):
        return False
    return any(
        isinstance(raw_asset, dict) and str(raw_asset.get("asset_type") or "").strip() == "image"
        for raw_asset in asset_refs
    )


def _record_search_text(record: JsonObject) -> str:
    """Concatenate the fields used for textual similarity matching against a KC."""
    parts = [
        str(record.get("title") or ""),
        str(record.get("retrieval_text") or ""),
        str(record.get("content_excerpt") or ""),
        str(record.get("content") or ""),
        str(record.get("section_ref") or ""),
    ]
    heading_path = record.get("heading_path")
    if isinstance(heading_path, dict):
        parts.extend(str(value or "") for value in heading_path.values())
    return " ".join(part for part in parts if part).strip()


def _support_search_terms(candidate_kc: CandidateKC) -> set[str]:
    """Tokens from the KC's text fields, excluding stopwords + very short tokens."""
    parts = [
        candidate_kc.kc_focus,
        candidate_kc.objective_text,
        candidate_kc.source_form,
        candidate_kc.target_form,
    ]
    return {
        token
        for part in parts
        for token in SUPPORT_TOKEN_RE.findall(str(part or "").lower())
        if len(token) > 2 and token not in SUPPORT_STOPWORDS
    }


def _supplement_candidate_kc_support_ids(
    candidate_kc: CandidateKC,
    *,
    textbook_records: Sequence[Mapping[str, object]],
) -> CandidateKC:
    """Add missing required-type records (concept always, worked-example/practice for procedure)."""
    record_map = {
        textbook_record_id(record): to_record_object(record)
        for record in textbook_records
        if textbook_record_id(record)
    }
    support_ids = [
        record_id for record_id in candidate_kc.supporting_record_ids if record_id in record_map
    ]
    support_terms = _support_search_terms(candidate_kc)

    def record_overlap(record: JsonObject) -> tuple[int, int]:
        record_text_terms = {
            token
            for token in SUPPORT_TOKEN_RE.findall(_record_search_text(record).lower())
            if len(token) > 2 and token not in SUPPORT_STOPWORDS
        }
        title_terms = {
            token
            for token in SUPPORT_TOKEN_RE.findall(str(record.get("title") or "").lower())
            if len(token) > 2 and token not in SUPPORT_STOPWORDS
        }
        return (
            len(support_terms & record_text_terms),
            len(support_terms & title_terms),
        )

    ranked_records = sorted(
        record_map.values(),
        key=lambda record: (
            -record_overlap(record)[0],
            -record_overlap(record)[1],
            SUPPORT_RECORD_TYPE_PRIORITY.get(str(record.get("record_type") or ""), 99),
            textbook_record_id(record),
        ),
    )

    def add_support_record(*allowed_types: str) -> None:
        allowed_type_set = set(allowed_types)
        for record in ranked_records:
            record_id = textbook_record_id(record)
            record_type = str(record.get("record_type") or "").strip()
            if not record_id or record_id in support_ids or record_type not in allowed_type_set:
                continue
            support_ids.append(record_id)
            return

    inventory = kc_support_inventory(
        candidate_kc.model_copy(update={"supporting_record_ids": support_ids}),
        textbook_records,
    )
    if not inventory["concept_ids"]:
        add_support_record(*sorted(CONCEPT_SUPPORT_TYPES))
        inventory = kc_support_inventory(
            candidate_kc.model_copy(update={"supporting_record_ids": support_ids}),
            textbook_records,
        )

    if candidate_kc.kc_type in {"procedure", "representation"}:
        if not (inventory["worked_example_ids"] or inventory["exercise_item_ids"]):
            add_support_record("worked_example", "exercise_item")
            inventory = kc_support_inventory(
                candidate_kc.model_copy(update={"supporting_record_ids": support_ids}),
                textbook_records,
            )
        if not inventory["practice_ids"]:
            add_support_record("exercise_block", "exercise_item")

    return candidate_kc.model_copy(update={"supporting_record_ids": support_ids})
