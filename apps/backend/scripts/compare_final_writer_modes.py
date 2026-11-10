"""Compare final lesson drafting with Predict vs ChainOfThought.

Usage:
    cd apps/backend
    uv run python scripts/compare_final_writer_modes.py
    uv run python scripts/compare_final_writer_modes.py --subtopic-id <linked-subtopic-id>
    uv run python scripts/compare_final_writer_modes.py --comparison-scope end_to_end
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from time import perf_counter
from typing import Any

import dspy
from dotenv import load_dotenv
from sqlalchemy import select

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # apps/backend root

import app.db.metadata  # noqa: F401
from app.db.session import AsyncSessionLocal
from app.domains.artefacts.types.lesson_plan.domain.types import SessionContext
from app.domains.artefacts.types.lesson_plan.drafting.application.precompute import (
    KCPlanningResult,
)
from app.domains.artefacts.types.lesson_plan.drafting.application.runtime import (
    LessonGenerationService,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
    PreparedGenerationInputs,
    prepare_generation_inputs,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.textbook import textbook_record_id
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.evidence_plan import (
    build_supported_evidence_plan,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.kc_compression import (
    build_lesson_structure_from_kcs,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.modules.generator import (
    LessonGenerationArtifacts,
)
from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.textbook_support import (
    normalize_candidate_kcs_for_support,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
    CandidateKC,
    CandidateKCPlan,
    StepEvidencePlan,
)
from app.domains.artefacts.types.lesson_plan.drafting.validation.service import (
    validate_session_plan,
)
from app.domains.artefacts.types.lesson_plan.infrastructure.repository import (
    build_session_context,
)
from app.domains.curriculum.models.curriculum import ClassSession
from scripts.textbook_corpus_lib import (
    linked_records_path,
    linked_subtopic_catalog_path,
    load_json,
    load_jsonl,
)

load_dotenv(override=False)

BASE_DIR = Path(__file__).resolve().parents[1]

DEFAULT_OUTPUT_ROOT = BASE_DIR / ".diagnostics" / "final-writer-comparisons"
FINAL_WRITER_MODES = ("predict", "chain_of_thought")
COMPARISON_SCOPES = ("final_writer_only", "end_to_end")

CONCEPT_SUPPORT_TYPES = {"definition", "exposition", "summary", "note"}
MODELING_SUPPORT_TYPES = {"worked_example", "exercise_item"}
PRACTICE_SUPPORT_TYPES = {"exercise_block", "exercise_item"}

OBJECTIVE_KEYWORDS_PROCEDURE = {
    "calculate",
    "construct",
    "convert",
    "determine",
    "draw",
    "find",
    "measure",
    "simplify",
    "solve",
    "work",
}
OBJECTIVE_KEYWORDS_REPRESENTATION = {
    "change",
    "convert",
    "express",
    "represent",
    "rewrite",
    "write",
}
STOPWORDS = {
    "and",
    "are",
    "for",
    "from",
    "into",
    "that",
    "the",
    "their",
    "them",
    "this",
    "these",
    "those",
    "with",
}
TOKEN_RE = re.compile(r"[a-z0-9]+")
TYPE_PRIORITY = {
    "definition": 0,
    "exposition": 1,
    "summary": 2,
    "note": 3,
    "worked_example": 4,
    "exercise_block": 5,
    "exercise_item": 6,
}


def _ensure_lm_configured() -> None:
    if getattr(dspy.settings, "lm", None) is not None:
        return
    dspy.configure(lm=dspy.LM(model=os.getenv("DSPY_MODEL", "openrouter/openai/gpt-oss-120b")))


@dataclass
class ModeRunSummary:
    mode: str
    latency_ms: float
    valid_schema: bool
    error_count: int
    step_count: int
    lesson_objective_count: int
    total_step_content_chars: int
    diagnostic_log_path: str | None
    output_path: str | None
    core_draft_latency_ms: float | None = None
    global_draft_latency_ms: float | None = None
    error: str | None = None


@dataclass
class ComparisonContext:
    session_id: str
    subject: str
    track: str
    grade: str
    term: str
    week: int
    day_index: int
    topic: str
    subtopic: str
    duration_minutes: int
    session_objectives: list[str]
    general_objectives: list[str]
    reference_materials: list[dict[str, Any]]
    theme: str = ""
    performance_objectives: list[str] | None = None
    teacher_activities: list[str] | None = None
    student_activities: list[str] | None = None
    instructional_materials: list[str] | None = None
    evaluation_guide: list[str] | None = None
    textbook_references: list[dict[str, Any]] | None = None
    entry_behaviour: list[str] | None = None
    average_age: int | None = None


@dataclass
class FinalWriterScaffold:
    inputs: PreparedGenerationInputs
    kc_plan: CandidateKCPlan
    lesson_structure: Any
    step_evidence_by_objective: dict[str, StepEvidencePlan]
    scope_context: dict[str, Any]
    curriculum_context: dict[str, Any]
    scaffold_path: str


def _json_list_len(value: object) -> int:
    return len(value) if isinstance(value, list) else 0


def _json_optional_str(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _scaffold_planning_result(scaffold: FinalWriterScaffold) -> KCPlanningResult:
    scope_payload = scaffold.inputs.scope_payload()
    return KCPlanningResult(
        subtopic_id=str(
            scope_payload.get("subtopic_id") or scope_payload.get("subtopic") or "unknown"
        ),
        topic_key=str(scope_payload.get("topic_key") or scope_payload.get("topic") or "unknown"),
        atomic_objectives=[],
        kc_plans={},
        step_evidence_plans=dict(scaffold.step_evidence_by_objective),
        assessment_items_by_atomic_objective={},
        assessment_items={},
        lesson_structure=scaffold.lesson_structure,
        combined_kc_plan=scaffold.kc_plan,
        resolved_kcs=list(scaffold.kc_plan.candidate_kcs),
        planning_duration_ms=0,
        llm_calls_planning=0,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-id", help="Optional class session id to evaluate.")
    parser.add_argument(
        "--subtopic-id",
        help="Optional linked textbook subtopic id to evaluate without using the database.",
    )
    parser.add_argument(
        "--evidence-strategy",
        default="global_rlm",
        choices=["global_rlm", "per_kc_rlm"],
        help="Lesson plan evidence-selection strategy label to use in the comparison.",
    )
    parser.add_argument(
        "--comparison-scope",
        default="final_writer_only",
        choices=list(COMPARISON_SCOPES),
        help=(
            "Choose whether to compare only the final drafting stage or the full lesson-"
            "generation pipeline."
        ),
    )
    parser.add_argument(
        "--output-dir",
        help="Optional output directory for comparison artifacts.",
    )
    args = parser.parse_args()
    if args.session_id and args.subtopic_id:
        parser.error("Use either --session-id or --subtopic-id, not both.")
    return args


def _build_curriculum_objective_refs(session_context: Any) -> list[dict[str, object]]:
    source_objectives = list(session_context.performance_objectives or []) or list(
        session_context.session_objectives or []
    )
    return [
        {
            "curriculum_objective_id": f"cur_obj{index:02d}",
            "objective_text": objective,
            "objective_order": index,
        }
        for index, objective in enumerate(source_objectives, start=1)
        if isinstance(objective, str) and objective.strip()
    ]


def _reference_context(session_context: Any) -> list[dict[str, Any]]:
    reference_context = list(session_context.reference_materials)
    for textbook_ref in session_context.textbook_references:
        reference_context.append(
            {
                "type": "textbook_record",
                "record_id": textbook_ref.get("record_id") or textbook_ref.get("section_ref", ""),
                "title": textbook_ref.get("title", ""),
                "section_ref": textbook_ref.get("section_ref", ""),
                "content": textbook_ref.get("content", ""),
                "retrieval_text": textbook_ref.get("retrieval_text", ""),
                "record_type": textbook_ref.get("record_type"),
                "primary_subtopic_id": textbook_ref.get("primary_subtopic_id"),
                "matched_subtopic_id": textbook_ref.get("matched_subtopic_id"),
                "source_html_path": textbook_ref.get("source_html_path"),
                "source_anchor_id": textbook_ref.get("source_anchor_id"),
                "asset_refs": textbook_ref.get("asset_refs"),
            }
        )
    return reference_context


def _session_payload(session_context: Any) -> dict[str, Any]:
    return {
        "session_id": session_context.session_id,
        "subject": session_context.subject,
        "track": session_context.track,
        "grade": session_context.grade,
        "term": session_context.term,
        "week": session_context.week,
        "day_index": session_context.day_index,
        "topic": session_context.topic,
        "subtopic": session_context.subtopic,
        "duration_minutes": session_context.duration_minutes,
        "session_objectives": session_context.session_objectives,
        "theme": session_context.theme,
        "performance_objectives": session_context.performance_objectives,
        "entry_behaviour": session_context.entry_behaviour,
        "instructional_materials": session_context.instructional_materials,
        "average_age": session_context.average_age,
    }


def _curriculum_payload(session_context: Any) -> dict[str, Any]:
    return {
        "subject": session_context.subject,
        "track": session_context.track,
        "grade": session_context.grade,
        "term": session_context.term,
        "week": session_context.week,
        "theme": session_context.theme,
        "topic": session_context.topic,
        "subtopic": session_context.subtopic,
        "curriculum_objectives": _build_curriculum_objective_refs(session_context),
        "general_objectives": session_context.general_objectives,
        "session_objectives": session_context.session_objectives,
        "performance_objectives": session_context.performance_objectives,
        "teacher_activities": session_context.teacher_activities,
        "student_activities": session_context.student_activities,
        "instructional_materials": session_context.instructional_materials,
        "evaluation_guide": session_context.evaluation_guide,
        "entry_behaviour": session_context.entry_behaviour,
    }


def _step_titles(session_plan: dict[str, Any]) -> list[str]:
    return [
        str(step.get("title") or "").strip()
        for step in session_plan.get("steps", [])
        if isinstance(step, dict) and str(step.get("title") or "").strip()
    ]


def _total_step_content_chars(session_plan: dict[str, Any]) -> int:
    total = 0
    for step in session_plan.get("steps", []):
        if not isinstance(step, dict):
            continue
        total += len(str(step.get("content") or ""))
        for block in step.get("blocks", []):
            if not isinstance(block, dict):
                continue
            for key in ("content", "question", "answer", "problem", "final_answer", "caption"):
                total += len(str(block.get(key) or ""))
            for hint in block.get("hints") or []:
                total += len(str(hint or ""))
            for worked_step in block.get("steps") or []:
                if isinstance(worked_step, dict):
                    total += len(str(worked_step.get("content") or ""))
    return total


def _serialize_plan(session_plan: dict[str, Any]) -> str:
    return json.dumps(session_plan, sort_keys=True, ensure_ascii=False, indent=2)


def _synthetic_textbook_references(subtopic_id: str) -> list[dict[str, Any]]:
    records = load_jsonl(linked_records_path())
    references: list[dict[str, Any]] = []
    for record in records:
        if subtopic_id not in (record.get("subtopic_ids") or []):
            continue
        references.append(
            {
                "record_id": record.get("record_id"),
                "title": record.get("chapter_title") or record.get("record_id") or "",
                "section_ref": record.get("record_id") or "",
                "content": record.get("content_text") or record.get("prompt_text") or "",
                "retrieval_text": record.get("retrieval_text") or "",
                "record_type": record.get("record_type"),
                "primary_subtopic_id": record.get("primary_subtopic_id"),
                "matched_subtopic_id": subtopic_id,
                "source_html_path": record.get("source_html_path"),
                "source_anchor_id": record.get("source_anchor_id"),
                "asset_refs": record.get("asset_refs"),
                "is_primary": record.get("primary_subtopic_id") == subtopic_id,
            }
        )
    references.sort(
        key=lambda item: (
            not bool(item.get("is_primary")),
            str(item.get("record_type") or ""),
            str(item.get("record_id") or ""),
        )
    )
    return references


def _synthetic_context(subtopic_id: str | None) -> ComparisonContext:
    catalog = load_json(linked_subtopic_catalog_path())
    subtopics = catalog["subtopics"] if isinstance(catalog, dict) else catalog
    references_by_subtopic: dict[str, list[dict[str, Any]]] = {}

    selected_row: dict[str, Any] | None = None
    for row in subtopics:
        current_subtopic_id = str(row.get("subtopic_id") or "").strip()
        if not current_subtopic_id:
            continue
        if current_subtopic_id not in references_by_subtopic:
            references_by_subtopic[current_subtopic_id] = _synthetic_textbook_references(
                current_subtopic_id
            )
        if subtopic_id:
            if current_subtopic_id == subtopic_id:
                selected_row = row
                break
            continue
        if references_by_subtopic[current_subtopic_id]:
            selected_row = row
            break

    if selected_row is None:
        if subtopic_id:
            raise RuntimeError(f"Linked subtopic not found or has no records: {subtopic_id}")
        raise RuntimeError("No linked subtopic with textbook records was found.")

    resolved_subtopic_id = str(selected_row["subtopic_id"])
    references = references_by_subtopic[resolved_subtopic_id]
    scheme_ref = (selected_row.get("scheme_refs") or [{}])[0]
    performance_objectives = list(selected_row.get("performance_objectives") or [])

    return ComparisonContext(
        session_id=f"synthetic-{resolved_subtopic_id}",
        subject="Mathematics",
        track="General",
        grade="JSS1",
        term=str(scheme_ref.get("term") or "First Term"),
        week=int(scheme_ref.get("week") or 1),
        day_index=1,
        topic=str(selected_row.get("topic_title") or "").strip(),
        subtopic=str(selected_row.get("subtopic_title") or "").strip(),
        duration_minutes=40,
        session_objectives=performance_objectives,
        general_objectives=[],
        reference_materials=[],
        theme=str(selected_row.get("theme_title") or "").strip(),
        performance_objectives=performance_objectives,
        teacher_activities=list(selected_row.get("teacher_activities") or []),
        student_activities=list(selected_row.get("student_activities") or []),
        instructional_materials=list(selected_row.get("teaching_learning_materials") or []),
        evaluation_guide=list(selected_row.get("evaluation_guide") or []),
        textbook_references=references,
        entry_behaviour=[],
        average_age=None,
    )


async def _resolve_session_id(session_id: str | None) -> str:
    if session_id:
        return session_id
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(ClassSession.session_id).order_by(ClassSession.session_id).limit(1)
        )
        resolved = result.scalars().first()
        if resolved is None:
            raise RuntimeError("No sessions found; seed the database first.")
        return resolved


def _record_has_image(record: dict[str, Any]) -> bool:
    return any(
        isinstance(asset, dict)
        and str(asset.get("asset_type") or "").strip() == "image"
        and str(asset.get("src") or "").strip()
        for asset in (record.get("asset_refs") or [])
    )


def _record_search_text(record: dict[str, Any]) -> str:
    return " ".join(
        str(record.get(key) or "")
        for key in ("title", "retrieval_text", "content", "content_excerpt", "section_ref")
    ).strip()


def _tokenize(text: str) -> list[str]:
    return [
        token
        for token in TOKEN_RE.findall(str(text or "").lower())
        if len(token) > 2 and token not in STOPWORDS
    ]


def _infer_source_target_forms(objective_text: str) -> tuple[str | None, str | None]:
    normalized = " ".join(str(objective_text or "").strip().split())
    patterns = (
        r"^(?:convert|change|express|represent|rewrite|write)\s+(.+?)\s+(?:to|as|in)\s+(.+)$",
        r"^(?:show|state)\s+(.+?)\s+(?:as|in)\s+(.+)$",
    )
    for pattern in patterns:
        match = re.match(pattern, normalized, flags=re.IGNORECASE)
        if not match:
            continue
        source_form = match.group(1).strip(" .,:;")
        target_form = match.group(2).strip(" .,:;")
        if source_form and target_form:
            return source_form, target_form
    return None, None


def _score_record_for_objective(
    record: dict[str, Any],
    objective_terms: set[str],
) -> tuple[int, int]:
    record_terms = set(_tokenize(_record_search_text(record)))
    title_terms = set(_tokenize(str(record.get("title") or "")))
    overlap = len(objective_terms & record_terms)
    title_overlap = len(objective_terms & title_terms)
    return overlap, title_overlap


def _rank_records_for_objective(
    objective_text: str,
    textbook_records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    objective_terms = set(_tokenize(objective_text))
    return sorted(
        textbook_records,
        key=lambda record: (
            -_score_record_for_objective(record, objective_terms)[0],
            -_score_record_for_objective(record, objective_terms)[1],
            TYPE_PRIORITY.get(str(record.get("record_type") or ""), 99),
            textbook_record_id(record),
        ),
    )


def _pick_supporting_record_ids(
    objective_text: str,
    textbook_records: list[dict[str, Any]],
) -> list[str]:
    ranked_records = _rank_records_for_objective(objective_text, textbook_records)

    def take_ids(*, allowed_types: set[str], limit: int) -> list[str]:
        selected: list[str] = []
        for record in ranked_records:
            record_type = str(record.get("record_type") or "").strip()
            record_id = textbook_record_id(record)
            if not record_id or record_type not in allowed_types or record_id in selected:
                continue
            selected.append(record_id)
            if len(selected) >= limit:
                break
        return selected

    visual_ids: list[str] = []
    for record in ranked_records:
        record_id = textbook_record_id(record)
        if not record_id or not _record_has_image(record) or record_id in visual_ids:
            continue
        visual_ids.append(record_id)
        break

    selected_ids = list(
        dict.fromkeys(
            [
                *take_ids(allowed_types=CONCEPT_SUPPORT_TYPES, limit=2),
                *take_ids(allowed_types={"worked_example"}, limit=1),
                *take_ids(allowed_types={"exercise_block"}, limit=1),
                *take_ids(allowed_types={"exercise_item"}, limit=1),
                *visual_ids,
            ]
        )
    )
    if selected_ids:
        return selected_ids

    for record in ranked_records:
        record_id = textbook_record_id(record)
        if record_id:
            return [record_id]
    return []


def _infer_kc_type(
    *,
    objective_text: str,
    supporting_records: list[dict[str, Any]],
    source_form: str | None,
    target_form: str | None,
) -> str:
    record_types = {str(record.get("record_type") or "").strip() for record in supporting_records}
    has_concept_support = bool(record_types & CONCEPT_SUPPORT_TYPES)
    has_modeling_support = bool(record_types & MODELING_SUPPORT_TYPES)
    has_practice_support = bool(record_types & PRACTICE_SUPPORT_TYPES)
    objective_terms = set(_tokenize(objective_text))

    if (
        source_form
        and target_form
        and objective_terms & OBJECTIVE_KEYWORDS_REPRESENTATION
        and has_concept_support
        and has_modeling_support
        and has_practice_support
    ):
        return "representation"

    if (
        objective_terms & OBJECTIVE_KEYWORDS_PROCEDURE
        and has_concept_support
        and has_modeling_support
        and has_practice_support
    ):
        return "procedure"

    return "concept"


def _build_scaffold_candidate_kc_plan(
    *,
    session_context: dict[str, Any],
    inputs: PreparedGenerationInputs,
) -> CandidateKCPlan:
    candidate_kcs: list[CandidateKC] = []
    textbook_record_payloads = inputs.textbook_record_payloads()
    textbook_record_map = {
        textbook_record_id(record): record
        for record in textbook_record_payloads
        if textbook_record_id(record)
    }

    for index, objective in enumerate(inputs.curriculum_objectives[:4], start=1):
        objective_text = objective.objective_text
        supporting_record_ids = _pick_supporting_record_ids(
            objective_text,
            textbook_record_payloads,
        )
        if not supporting_record_ids and textbook_record_payloads:
            supporting_record_ids = [textbook_record_id(textbook_record_payloads[0])]

        source_form, target_form = _infer_source_target_forms(objective_text)
        supporting_records = [
            textbook_record_map[record_id]
            for record_id in supporting_record_ids
            if record_id in textbook_record_map
        ]
        kc_type = _infer_kc_type(
            objective_text=objective_text,
            supporting_records=supporting_records,
            source_form=source_form,
            target_form=target_form,
        )

        candidate_kcs.append(
            CandidateKC.model_validate(
                {
                    "kc_id": f"kc{index:02d}",
                    "kc_type": kc_type,
                    "objective_text": objective_text,
                    "curriculum_objective_id": objective.curriculum_objective_id,
                    "kc_focus": objective_text,
                    "source_form": source_form if kc_type == "representation" else None,
                    "target_form": target_form if kc_type == "representation" else None,
                    "supporting_record_ids": supporting_record_ids,
                    "ordering_notes": "Deterministic comparison scaffold.",
                }
            )
        )

    normalized_kcs = normalize_candidate_kcs_for_support(
        candidate_kcs,
        textbook_records=textbook_record_payloads,
    )
    return CandidateKCPlan.model_validate(
        {
            "candidate_kcs": [item.model_dump() for item in normalized_kcs],
            "theme": session_context.get("theme"),
            "entry_behaviour": inputs.curriculum.entry_behaviour,
            "instructional_materials": inputs.curriculum.instructional_materials,
        }
    )


def _fallback_evidence_plan(
    *,
    lesson_objective_id: str,
    supporting_record_ids: list[str],
    textbook_records: list[dict[str, Any]],
) -> StepEvidencePlan:
    record_map = {
        textbook_record_id(record): record
        for record in textbook_records
        if textbook_record_id(record)
    }
    support_records = [
        record_map[record_id] for record_id in supporting_record_ids if record_id in record_map
    ]

    def first_ids(allowed_types: set[str], *, limit: int) -> list[str]:
        selected: list[str] = []
        for record in support_records:
            record_type = str(record.get("record_type") or "").strip()
            record_id = textbook_record_id(record)
            if not record_id or record_type not in allowed_types or record_id in selected:
                continue
            selected.append(record_id)
            if len(selected) >= limit:
                break
        return selected

    concept_record_ids = first_ids(CONCEPT_SUPPORT_TYPES, limit=1)
    modeling_record_ids = first_ids(MODELING_SUPPORT_TYPES, limit=1)
    practice_record_ids = [
        record_id
        for record_id in first_ids(PRACTICE_SUPPORT_TYPES, limit=2)
        if record_id not in modeling_record_ids
    ][:1]
    if not practice_record_ids and modeling_record_ids:
        practice_record_ids = modeling_record_ids[:1]
    if not modeling_record_ids and practice_record_ids:
        modeling_record_ids = practice_record_ids[:1]
    visual_record_ids = [
        textbook_record_id(record)
        for record in support_records
        if _record_has_image(record) and textbook_record_id(record)
    ][:1]

    selected_record_ids = list(
        dict.fromkeys(
            [
                *concept_record_ids,
                *modeling_record_ids,
                *practice_record_ids,
                *visual_record_ids,
                *(supporting_record_ids[:1] if supporting_record_ids else []),
            ]
        )
    )
    if not selected_record_ids:
        raise ValueError("comparison scaffold could not build any selected_record_ids")

    return StepEvidencePlan.model_validate(
        {
            "lesson_objective_id": lesson_objective_id,
            "selected_record_ids": selected_record_ids,
            "concept_record_ids": [
                record_id for record_id in concept_record_ids if record_id in selected_record_ids
            ],
            "modeling_record_ids": [
                record_id for record_id in modeling_record_ids if record_id in selected_record_ids
            ],
            "practice_record_ids": [
                record_id for record_id in practice_record_ids if record_id in selected_record_ids
            ],
            "visual_record_ids": [
                record_id for record_id in visual_record_ids if record_id in selected_record_ids
            ],
        }
    )


def _build_final_writer_scaffold(
    *,
    session_context: Any,
    evidence_strategy: str,
    output_dir: Path,
) -> FinalWriterScaffold:
    session_payload = _session_payload(session_context)
    curriculum_payload = _curriculum_payload(session_context)
    generator = LessonGenerationService(final_writer_mode="predict")
    inputs = prepare_generation_inputs(
        session_context=session_payload,
        curriculum_context=curriculum_payload,
        reference_context=_reference_context(session_context),
        requested_strategy=evidence_strategy,
        default_strategy=generator.default_evidence_selection_strategy,
    )

    kc_plan = _build_scaffold_candidate_kc_plan(
        session_context=session_payload,
        inputs=inputs,
    )
    lesson_structure = build_lesson_structure_from_kcs(
        kc_plan.candidate_kcs,
        curriculum_objectives=inputs.curriculum_objective_payloads(),
    )

    step_evidence_by_objective: dict[str, StepEvidencePlan] = {}
    for lesson_objective in lesson_structure.objectives:
        candidate_kc = lesson_structure.kcs_by_objective_id[lesson_objective.lesson_objective_id]
        evidence_plan = build_supported_evidence_plan(
            lesson_objective=lesson_objective,
            candidate_kc=candidate_kc,
            textbook_records=inputs.textbook_record_payloads(),
        )
        if evidence_plan is None:
            evidence_plan = _fallback_evidence_plan(
                lesson_objective_id=lesson_objective.lesson_objective_id,
                supporting_record_ids=candidate_kc.supporting_record_ids,
                textbook_records=inputs.textbook_record_payloads(),
            )
        step_evidence_by_objective[lesson_objective.lesson_objective_id] = evidence_plan

    scaffold_payload = {
        "curriculum_objectives": inputs.curriculum_objective_payloads(),
        "candidate_kcs": [item.model_dump() for item in kc_plan.candidate_kcs],
        "lesson_plan_objectives": [item.model_dump() for item in lesson_structure.objectives],
        "core_step_blueprints": [item.model_dump() for item in lesson_structure.blueprints],
        "step_evidence_plans": {
            lesson_objective_id: evidence_plan.model_dump()
            for lesson_objective_id, evidence_plan in step_evidence_by_objective.items()
        },
        "comparison_scope": "final_writer_only",
        "evidence_strategy": inputs.evidence_selection_strategy,
    }
    scaffold_path = output_dir / "shared_scaffold.json"
    scaffold_path.write_text(
        json.dumps(scaffold_payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return FinalWriterScaffold(
        inputs=inputs,
        kc_plan=kc_plan,
        lesson_structure=lesson_structure,
        step_evidence_by_objective=step_evidence_by_objective,
        scope_context=inputs.scope_payload(),
        curriculum_context=inputs.curriculum_payload(),
        scaffold_path=str(scaffold_path),
    )


async def _run_end_to_end_mode(
    *,
    session_context: Any,
    output_dir: Path,
    mode: str,
    evidence_strategy: str,
) -> tuple[ModeRunSummary, dict[str, Any] | None]:
    generator = LessonGenerationService(final_writer_mode=mode)
    started_at = perf_counter()
    try:
        result = await generator.generate(
            session_context=_session_payload(session_context),
            curriculum_context=_curriculum_payload(session_context),
            reference_context=_reference_context(session_context),
            evidence_selection_strategy=evidence_strategy,
        )
    except Exception as exc:
        latency_ms = round((perf_counter() - started_at) * 1000, 1)
        return (
            ModeRunSummary(
                mode=mode,
                latency_ms=latency_ms,
                valid_schema=False,
                error_count=0,
                step_count=0,
                lesson_objective_count=0,
                total_step_content_chars=0,
                diagnostic_log_path=None,
                output_path=None,
                error=str(exc),
            ),
            None,
        )

    latency_ms = round((perf_counter() - started_at) * 1000, 1)
    output_path = output_dir / f"{mode}.session_plan.json"
    output_path.write_text(_serialize_plan(result.session_plan), encoding="utf-8")

    errors = validate_session_plan(result.session_plan)
    summary = ModeRunSummary(
        mode=mode,
        latency_ms=latency_ms,
        valid_schema=not errors,
        error_count=len(errors),
        step_count=_json_list_len(result.session_plan.get("steps")),
        lesson_objective_count=_json_list_len(result.session_plan.get("lesson_plan_objectives")),
        total_step_content_chars=_total_step_content_chars(result.session_plan),
        diagnostic_log_path=_json_optional_str(result.run_metadata.get("diagnostic_log_path")),
        output_path=str(output_path),
    )
    return summary, result.session_plan


async def _run_final_writer_only_mode(
    *,
    session_context: Any,
    output_dir: Path,
    mode: str,
    scaffold: FinalWriterScaffold,
) -> tuple[ModeRunSummary, dict[str, Any] | None]:
    generator = LessonGenerationService(final_writer_mode=mode)
    draft_builder = generator.generation_program.draft_builder

    started_at = perf_counter()
    try:
        core_started_at = perf_counter()
        raw_core_steps, evidence_summaries = draft_builder._draft_core_steps(
            lesson_structure=scaffold.lesson_structure,
            evidence_by_objective=scaffold.step_evidence_by_objective,
            assessment_by_objective={},
            request=scaffold.inputs,
        )
        core_draft_latency_ms = round((perf_counter() - core_started_at) * 1000, 1)

        global_started_at = perf_counter()
        raw_global_steps = draft_builder._draft_global_steps(
            lesson_structure=scaffold.lesson_structure,
            core_steps=raw_core_steps,
            evidence_summaries=evidence_summaries,
            request=scaffold.inputs,
            assessment_by_objective={},
        )
        global_draft_latency_ms = round((perf_counter() - global_started_at) * 1000, 1)

        artifacts = LessonGenerationArtifacts(
            planning_result=_scaffold_planning_result(scaffold),
            kc_plan=scaffold.kc_plan,
            resolved_kcs=list(scaffold.kc_plan.candidate_kcs),
            lesson_plan_objectives=list(scaffold.lesson_structure.objectives),
            core_step_blueprints=list(scaffold.lesson_structure.blueprints),
            assessment_items=[],
            step_evidence_plans=scaffold.step_evidence_by_objective,
            core_steps=raw_core_steps,
            global_steps=raw_global_steps,
            evidence_summaries=evidence_summaries,
            planning_duration_ms=0,
            drafting_duration_ms=int(core_draft_latency_ms + global_draft_latency_ms),
            drafting_llm_call_estimate=0,
        )
        normalized_draft = generator.session_plan_assembler.normalize_draft(
            artifacts=artifacts,
            inputs=scaffold.inputs,
        )
        session_plan_content = generator.session_plan_assembler.build_content(
            session=scaffold.inputs.session,
            inputs=scaffold.inputs,
            artifacts=artifacts,
            draft=normalized_draft,
        )
        session_plan = generator.session_plan_assembler.assemble(
            session=scaffold.inputs.session,
            session_plan_content=session_plan_content,
        )
    except Exception as exc:
        latency_ms = round((perf_counter() - started_at) * 1000, 1)
        return (
            ModeRunSummary(
                mode=mode,
                latency_ms=latency_ms,
                core_draft_latency_ms=None,
                global_draft_latency_ms=None,
                valid_schema=False,
                error_count=0,
                step_count=0,
                lesson_objective_count=0,
                total_step_content_chars=0,
                diagnostic_log_path=None,
                output_path=None,
                error=str(exc),
            ),
            None,
        )

    latency_ms = round((perf_counter() - started_at) * 1000, 1)
    output_path = output_dir / f"{mode}.session_plan.json"
    output_path.write_text(_serialize_plan(session_plan), encoding="utf-8")

    draft_artifact_path = output_dir / f"{mode}.draft_artifacts.json"
    draft_artifact_path.write_text(
        json.dumps(
            {
                "core_steps": raw_core_steps,
                "global_steps": raw_global_steps,
                "evidence_summaries": evidence_summaries,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    errors = validate_session_plan(session_plan)
    summary = ModeRunSummary(
        mode=mode,
        latency_ms=latency_ms,
        core_draft_latency_ms=core_draft_latency_ms,
        global_draft_latency_ms=global_draft_latency_ms,
        valid_schema=not errors,
        error_count=len(errors),
        step_count=_json_list_len(session_plan.get("steps")),
        lesson_objective_count=_json_list_len(session_plan.get("lesson_plan_objectives")),
        total_step_content_chars=_total_step_content_chars(session_plan),
        diagnostic_log_path=None,
        output_path=str(output_path),
    )
    return summary, session_plan


def _comparison_report(
    *,
    source_type: str,
    session_id: str,
    evidence_strategy: str,
    comparison_scope: str,
    summaries: list[ModeRunSummary],
    plans_by_mode: dict[str, dict[str, Any]],
    shared_scaffold_path: str | None,
) -> dict[str, Any]:
    report: dict[str, Any] = {
        "source_type": source_type,
        "session_id": session_id,
        "evidence_strategy": evidence_strategy,
        "comparison_scope": comparison_scope,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runs": [asdict(summary) for summary in summaries],
    }
    if shared_scaffold_path:
        report["shared_scaffold_path"] = shared_scaffold_path

    if set(plans_by_mode) == set(FINAL_WRITER_MODES):
        predict_plan = plans_by_mode["predict"]
        cot_plan = plans_by_mode["chain_of_thought"]
        predict_text = _serialize_plan(predict_plan)
        cot_text = _serialize_plan(cot_plan)
        report["comparison"] = {
            "exact_match": predict_text == cot_text,
            "json_similarity_ratio": round(
                SequenceMatcher(None, predict_text, cot_text).ratio(),
                4,
            ),
            "predict_step_titles": _step_titles(predict_plan),
            "chain_of_thought_step_titles": _step_titles(cot_plan),
        }

    return report


def _render_metric(value: Any) -> str:
    if value is None:
        return "-"
    return str(value)


def _markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Final Writer Mode Comparison",
        "",
        f"- Source Type: `{report['source_type']}`",
        f"- Session ID: `{report['session_id']}`",
        f"- Evidence Strategy: `{report['evidence_strategy']}`",
        f"- Comparison Scope: `{report['comparison_scope']}`",
        f"- Generated At: `{report['generated_at']}`",
    ]
    if report.get("shared_scaffold_path"):
        lines.append(f"- Shared Scaffold: `{report['shared_scaffold_path']}`")
    lines.extend(
        [
            "",
            "| Mode | Total ms | Core Draft ms | Global Draft ms | Valid Schema | Errors | "
            "Steps | Objectives | Step Text Chars |",
            "| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for run in report["runs"]:
        lines.append(
            "| {mode} | {latency_ms} | {core_draft_latency_ms} | {global_draft_latency_ms} "
            "| {valid_schema} | {error_count} | {step_count} | {lesson_objective_count} | "
            "{total_step_content_chars} |".format(
                mode=run["mode"],
                latency_ms=_render_metric(run.get("latency_ms")),
                core_draft_latency_ms=_render_metric(run.get("core_draft_latency_ms")),
                global_draft_latency_ms=_render_metric(run.get("global_draft_latency_ms")),
                valid_schema=run["valid_schema"],
                error_count=run["error_count"],
                step_count=run["step_count"],
                lesson_objective_count=run["lesson_objective_count"],
                total_step_content_chars=run["total_step_content_chars"],
            )
        )
        if run.get("error"):
            lines.append(f"| `{run['mode']}` error |  |  |  |  |  |  |  | `{run['error']}` |")

    comparison = report.get("comparison")
    if comparison:
        lines.extend(
            [
                "",
                f"- Exact Match: `{comparison['exact_match']}`",
                f"- JSON Similarity Ratio: `{comparison['json_similarity_ratio']}`",
            ]
        )
    return "\n".join(lines) + "\n"


async def main() -> None:
    args = parse_args()
    _ensure_lm_configured()

    session_context: ComparisonContext | SessionContext
    if args.subtopic_id:
        source_type = "linked_subtopic"
        session_context = _synthetic_context(args.subtopic_id)
        session_id = session_context.session_id
    elif args.session_id:
        source_type = "session"
        session_id = await _resolve_session_id(args.session_id)
        async with AsyncSessionLocal() as db:
            resolved = await build_session_context(db, session_id)
            if resolved is None:
                raise RuntimeError(f"Session not found: {session_id}")
            session_context = resolved
    else:
        source_type = "linked_subtopic"
        session_context = _synthetic_context(None)
        session_id = session_context.session_id

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output_root = Path(args.output_dir) if args.output_dir else DEFAULT_OUTPUT_ROOT
    output_dir = output_root / f"{session_id}-{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    scaffold: FinalWriterScaffold | None = None
    shared_scaffold_path: str | None = None
    if args.comparison_scope == "final_writer_only":
        scaffold = _build_final_writer_scaffold(
            session_context=session_context,
            evidence_strategy=args.evidence_strategy,
            output_dir=output_dir,
        )
        shared_scaffold_path = scaffold.scaffold_path

    summaries: list[ModeRunSummary] = []
    plans_by_mode: dict[str, dict[str, Any]] = {}
    for mode in FINAL_WRITER_MODES:
        if args.comparison_scope == "final_writer_only":
            assert scaffold is not None
            summary, session_plan = await _run_final_writer_only_mode(
                session_context=session_context,
                output_dir=output_dir,
                mode=mode,
                scaffold=scaffold,
            )
        else:
            summary, session_plan = await _run_end_to_end_mode(
                session_context=session_context,
                output_dir=output_dir,
                mode=mode,
                evidence_strategy=args.evidence_strategy,
            )
        summaries.append(summary)
        if session_plan is not None:
            plans_by_mode[mode] = session_plan

    report = _comparison_report(
        source_type=source_type,
        session_id=session_id,
        evidence_strategy=args.evidence_strategy,
        comparison_scope=args.comparison_scope,
        summaries=summaries,
        plans_by_mode=plans_by_mode,
        shared_scaffold_path=shared_scaffold_path,
    )
    (output_dir / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (output_dir / "report.md").write_text(_markdown_report(report), encoding="utf-8")

    print(_markdown_report(report), end="")
    print(f"Artifacts written to: {output_dir}")


if __name__ == "__main__":
    asyncio.run(main())
