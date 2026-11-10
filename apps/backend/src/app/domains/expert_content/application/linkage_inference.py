"""Inputs the linkage workflow needs before validation can run.

Three concerns, all input-preparation rather than validation:
- Bloom-level inference from an objective text (``infer_bloom_verb`` /
  ``infer_bloom_level``).
- Flatten the curriculum-objective tree into the ordered atomic-objective list
  (``flatten_atomic_objectives``) that drives ``ao_order``.
- File I/O loaders for the two JSONL source files used by the manual workflow.
- Prompt-template rendering from the loaded inputs.

Imports from ``linkage_models`` for types + constants. Validation
(``linkage_validation``) imports from here in turn.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast

from app.domains.expert_content.application.linkage_models import (
    ATOMIC_OBJECTIVE_PLACEHOLDER,
    BLOOM_VERB_MAP,
    TEXTBOOK_RECORDS_PLACEHOLDER,
    BloomLevel,
    JsonObject,
)


def infer_bloom_verb(objective_text: str) -> str:
    """Lowercased first token of ``objective_text`` (minus trailing punctuation)."""
    words = objective_text.strip().split()
    if not words:
        return ""
    return words[0].lower().strip(".,:;!?")


def infer_bloom_level(objective_text: str) -> BloomLevel:
    """Map ``objective_text``'s first verb to a Bloom level (default ``apply``)."""
    verb = infer_bloom_verb(objective_text)
    return BLOOM_VERB_MAP.get(verb, "apply")


def flatten_atomic_objectives(subtopic_row: JsonObject) -> list[JsonObject]:
    """Walk the curriculum-objective tree and return the ordered atomic-objective list.

    Each output row carries the parent curriculum-objective id + text (so the
    validator can check the mapping) and the bloom verb/level derived from the
    AO text (so the linkage row can be checked field-by-field).
    """
    ordered: list[JsonObject] = []
    order = 1
    for curriculum_objective in subtopic_row.get("curriculum_objectives") or []:
        if not isinstance(curriculum_objective, dict):
            continue
        source = cast(JsonObject, curriculum_objective.get("source") or {})
        curriculum_objective_id = str(source.get("curriculum_objective_id") or "").strip()
        curriculum_objective_text = str(source.get("text") or "").strip()
        for atomic_objective in curriculum_objective.get("atomic_decomposition") or []:
            if not isinstance(atomic_objective, dict):
                continue
            text = str(atomic_objective.get("text") or "").strip()
            ordered.append(
                {
                    "ao_id": str(atomic_objective.get("atomic_objective_id") or "").strip(),
                    "ao_order": order,
                    "curriculum_objective_id": curriculum_objective_id,
                    "curriculum_objective_text": curriculum_objective_text,
                    "text": text,
                    "bloom_verb": infer_bloom_verb(text),
                    "bloom_level": infer_bloom_level(text),
                }
            )
            order += 1
    return ordered


def load_subtopic_atomic_objective_source(path: Path, subtopic_id: str) -> JsonObject:
    """Read the JSONL atomic-objective file and return the row for ``subtopic_id``."""
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            payload = json.loads(line)
            if str(payload.get("subtopic_id") or "").strip() == subtopic_id:
                return cast(JsonObject, payload)
    raise ValueError(f"Unknown subtopic_id in atomic-objective source: {subtopic_id}")


def load_reduced_subtopic_textbook_records(path: Path, subtopic_id: str) -> list[JsonObject]:
    """Read the JSONL textbook-record file and return the reduced records for ``subtopic_id``."""
    reduced: list[JsonObject] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            payload = cast(JsonObject, json.loads(line))
            linked_subtopics = payload.get("subtopic_ids") or []
            if subtopic_id not in linked_subtopics:
                continue
            reduced.append(
                {
                    "record_id": str(payload.get("record_id") or "").strip(),
                    "record_type": str(payload.get("record_type") or "").strip(),
                    "heading_path": payload.get("heading_path"),
                    "content_text": str(payload.get("content_text") or ""),
                    "prompt_text": str(payload.get("prompt_text") or ""),
                    "answer_text": str(payload.get("answer_text") or ""),
                    "primary_subtopic_id": str(payload.get("primary_subtopic_id") or "").strip()
                    or None,
                }
            )
    return reduced


def build_manual_ao_textbook_linkage_prompt(
    *,
    template_text: str,
    atomic_objective_source: JsonObject,
    textbook_records: list[JsonObject],
) -> str:
    """Render the manual-linkage prompt by substituting the two source payloads."""
    atomic_json = json.dumps(atomic_objective_source, ensure_ascii=False, indent=2)
    records_json = json.dumps(textbook_records, ensure_ascii=False, indent=2)
    return template_text.replace(ATOMIC_OBJECTIVE_PLACEHOLDER, atomic_json).replace(
        TEXTBOOK_RECORDS_PLACEHOLDER,
        records_json,
    )
