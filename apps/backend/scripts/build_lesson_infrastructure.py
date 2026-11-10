"""Build ahead-of-time lesson-planning infrastructure.

See `docs/lesson-plan-infrastructure-cache.md` for the workflow, cache layout,
and examples for single-subtopic and batch runs.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, TypeAlias, cast

if TYPE_CHECKING:
    from app.domains.artefacts.types.lesson_plan.drafting.application.precompute import (
        InfrastructurePlanningPipeline,
        PlanningQualityRow,
        Violation,
    )
    from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
        CurriculumObjectiveRef,
    )
    from app.shared.json_types import JsonObject
else:
    JsonObject: TypeAlias = dict[str, object]


@dataclass(frozen=True)
class RuntimeDependencies:
    infrastructure_planning_pipeline: type[InfrastructurePlanningPipeline]
    planning_quality_row: type[PlanningQualityRow]
    violation: type[Violation]
    render_infrastructure_quality_report: Callable[[list[PlanningQualityRow]], str]
    build_curriculum_objectives: Callable[
        [JsonObject, JsonObject],
        list[CurriculumObjectiveRef],
    ]
    curriculum_path: Path
    scheme_path: Path
    infrastructure_cache_dir: Path
    #: The model the drafting runtime uses, so what this script caches is what it reads.
    model_name: Callable[[], str]
    linked_records_path: Callable[[], Path]
    load_json: Callable[[Path], object]
    load_jsonl: Callable[[Path], list[JsonObject]]


def _load_runtime_dependencies() -> RuntimeDependencies:
    base_dir = Path(__file__).resolve().parents[1]
    if str(base_dir) not in sys.path:
        sys.path.append(str(base_dir))

    from app.config import CONFIG
    from app.domains.artefacts.types.lesson_plan.drafting.application.precompute import (
        InfrastructurePlanningPipeline,
        PlanningQualityRow,
        Violation,
        render_infrastructure_quality_report,
    )
    from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
        build_curriculum_objectives,
    )
    from app.infra.dspy_lm import active_model_name
    from scripts.textbook_corpus_lib import (
        CURRICULUM_PATH,
        SCHEME_PATH,
        linked_records_path,
        load_json,
        load_jsonl,
    )

    return RuntimeDependencies(
        infrastructure_planning_pipeline=InfrastructurePlanningPipeline,
        planning_quality_row=PlanningQualityRow,
        violation=Violation,
        render_infrastructure_quality_report=render_infrastructure_quality_report,
        build_curriculum_objectives=build_curriculum_objectives,
        curriculum_path=CURRICULUM_PATH,
        scheme_path=SCHEME_PATH,
        infrastructure_cache_dir=CONFIG.lesson_plan.infrastructure_cache_dir,
        model_name=active_model_name,
        linked_records_path=linked_records_path,
        load_json=load_json,
        load_jsonl=load_jsonl,
    )


RUNTIME_DEPS = _load_runtime_dependencies()


def _object_list(value: object) -> list[object]:
    if not isinstance(value, list):
        return []
    return cast(list[object], value)


def _as_json_object(value: object) -> JsonObject | None:
    if not isinstance(value, dict):
        return None
    return cast(JsonObject, value)


def _string_list(value: object) -> list[str]:
    return [str(item).strip() for item in _object_list(value) if str(item).strip()]


def _json_object_list(value: object) -> list[JsonObject]:
    rows: list[JsonObject] = []
    for item in _object_list(value):
        payload = _as_json_object(item)
        if payload is not None:
            rows.append(payload)
    return rows


def _optional_int(value: object, *, default: int) -> int:
    if not isinstance(value, (int, float, str)):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build and cache lesson-planning infrastructure across curriculum subtopics.",
    )
    parser.add_argument(
        "--topics",
        default=str(RUNTIME_DEPS.curriculum_path),
        help="Path to topics_enriched.json.",
    )
    parser.add_argument(
        "--scheme",
        default=str(RUNTIME_DEPS.scheme_path),
        help="Path to scheme-of-work JSON.",
    )
    parser.add_argument(
        "--records",
        default=str(RUNTIME_DEPS.linked_records_path()),
        help="Path to linked textbook records JSONL.",
    )
    parser.add_argument(
        "--output",
        "--output-dir",
        dest="output_dir",
        default=str(RUNTIME_DEPS.infrastructure_cache_dir),
        help="Directory for cached infrastructure artifacts.",
    )
    parser.add_argument(
        "--report-path",
        default=None,
        help="Optional path for a text quality report. Defaults inside output-dir.",
    )
    parser.add_argument(
        "--summary-path",
        default=None,
        help="Optional path for a JSON summary. Defaults inside output-dir.",
    )
    parser.add_argument(
        "--subtopic-id",
        default=None,
        help="Optional single subtopic_id to process instead of the full curriculum.",
    )
    return parser.parse_args()


def _records_by_subtopic(records_path: Path) -> dict[str, list[JsonObject]]:
    grouped: dict[str, list[JsonObject]] = {}
    for record in RUNTIME_DEPS.load_jsonl(records_path):
        for subtopic_id in _object_list(record.get("subtopic_ids")):
            if not isinstance(subtopic_id, str) or not subtopic_id:
                continue
            grouped.setdefault(subtopic_id, []).append(
                {
                    "type": "textbook_record",
                    "record_id": record.get("record_id"),
                    "title": record.get("chapter_title") or record.get("record_id") or "",
                    "section_ref": record.get("record_id") or "",
                    "content": record.get("content_text") or record.get("prompt_text") or "",
                    "retrieval_text": record.get("retrieval_text") or "",
                    "record_type": record.get("record_type"),
                    "source_html_path": record.get("source_html_path"),
                    "source_anchor_id": record.get("source_anchor_id"),
                    "asset_refs": record.get("asset_refs") or [],
                }
            )
    return grouped


def _scheme_index(scheme: JsonObject) -> dict[str, JsonObject]:
    indexed: dict[str, JsonObject] = {}
    for term, weeks in scheme.items():
        if not isinstance(weeks, list):
            continue
        for week in weeks:
            week_payload = _as_json_object(week)
            if week_payload is None:
                continue
            week_number = _optional_int(week_payload.get("week"), default=1) or 1
            for order, raw_row in enumerate(
                _object_list(week_payload.get("breakdown")),
                start=1,
            ):
                row = _as_json_object(raw_row)
                if row is None:
                    continue
                subtopic_id = str(row.get("subtopic_id") or "").strip()
                if not subtopic_id:
                    continue
                indexed[subtopic_id] = {
                    "term": str(term).strip() or "First Term",
                    "week": week_number,
                    "order": order,
                }
    return indexed


def _iter_curriculum_subtopics(
    topics: list[JsonObject],
    scheme: JsonObject,
) -> list[JsonObject]:
    scheme_lookup = _scheme_index(scheme)
    rows: list[JsonObject] = []
    for topic in topics:
        topic_key = str(topic.get("topic_key") or "").strip()
        topic_title = str(topic.get("topic") or "").strip()
        theme = str(topic.get("theme") or topic.get("theme_title") or "").strip() or None
        for position, raw_subtopic in enumerate(_object_list(topic.get("subtopics")), start=1):
            subtopic = _as_json_object(raw_subtopic)
            if subtopic is None:
                continue
            subtopic_id = str(subtopic.get("subtopic_id") or "").strip()
            if not subtopic_id:
                continue
            schedule_info = scheme_lookup.get(subtopic_id, {})
            rows.append(
                {
                    "topic_key": topic_key or topic_title,
                    "topic_title": topic_title,
                    "theme": theme,
                    "subtopic_id": subtopic_id,
                    "subtopic_title": str(
                        subtopic.get("subtopic_title") or subtopic.get("title") or ""
                    ).strip(),
                    "performance_objectives": list(
                        _string_list(subtopic.get("performance_objectives"))
                    ),
                    "teacher_activities": list(_string_list(subtopic.get("teacher_activities"))),
                    "student_activities": list(_string_list(subtopic.get("student_activities"))),
                    "teaching_learning_materials": list(
                        _string_list(subtopic.get("teaching_learning_materials"))
                    ),
                    "evaluation_guide": list(_string_list(subtopic.get("evaluation_guide"))),
                    "entry_behaviour": list(_string_list(subtopic.get("entry_behaviour"))),
                    "term": schedule_info.get("term", "First Term"),
                    "week": schedule_info.get("week", position),
                }
            )
    return rows


def _scope_context(row: JsonObject) -> JsonObject:
    return {
        "subject": "Mathematics",
        "track": "General",
        "grade": "JSS1",
        "term": str(row.get("term") or "First Term"),
        "week": _optional_int(row.get("week"), default=1),
        "theme": row.get("theme"),
        "topic": str(row.get("topic_title") or "").strip(),
        "topic_key": str(row.get("topic_key") or "").strip(),
        "subtopic": str(row.get("subtopic_title") or "").strip(),
        "subtopic_id": str(row.get("subtopic_id") or "").strip(),
        "duration_minutes": 40,
    }


def _curriculum_context(row: JsonObject, scope_context: JsonObject) -> JsonObject:
    performance_objectives = _string_list(row.get("performance_objectives"))
    curriculum_objectives = RUNTIME_DEPS.build_curriculum_objectives(
        {**scope_context, "session_objectives": list(performance_objectives)},
        {"curriculum_objectives": list(performance_objectives)},
    )
    return {
        "curriculum_objectives": list(
            curriculum_objective.model_dump() for curriculum_objective in curriculum_objectives
        ),
        "teacher_activities": list(_string_list(row.get("teacher_activities"))),
        "student_activities": list(_string_list(row.get("student_activities"))),
        "instructional_materials": list(_string_list(row.get("teaching_learning_materials"))),
        "evaluation_guide": list(_string_list(row.get("evaluation_guide"))),
        "entry_behaviour": list(_string_list(row.get("entry_behaviour"))),
    }


def _error_row(subtopic_id: str, message: str) -> PlanningQualityRow:
    return RUNTIME_DEPS.planning_quality_row(
        subtopic_id=subtopic_id,
        violations=[
            RUNTIME_DEPS.violation(
                code="zero_linked_textbook_records",
                message=message,
                severity="error",
            )
        ],
    )


def build_subtopic_infrastructure(
    *,
    pipeline: InfrastructurePlanningPipeline,
    row: JsonObject,
    topics: list[JsonObject],
    scheme: JsonObject,
    grouped_records: dict[str, list[JsonObject]],
) -> tuple[PlanningQualityRow, JsonObject]:
    subtopic_id = str(row.get("subtopic_id") or "").strip()
    reference_context = grouped_records.get(subtopic_id)
    if not reference_context:
        return (
            _error_row(subtopic_id, "zero linked textbook records (cannot generate KCs)"),
            {
                "subtopic_id": subtopic_id,
                "topic": row["topic_title"],
                "subtopic": row["subtopic_title"],
                "atomic_objectives": 0,
                "total_kcs": 0,
                "assessment_items": 0,
                "violations": 1,
                "is_valid": False,
                "cached_planning": False,
            },
        )

    scope_context = _scope_context(row)
    curriculum_context = _curriculum_context(row, scope_context)
    planning = pipeline.build_infrastructure(
        scope_context=scope_context,
        curriculum_context=curriculum_context,
        curriculum_objectives=_json_object_list(curriculum_context.get("curriculum_objectives")),
        textbook_records=reference_context,
        topics_enriched=topics,
        scheme=scheme,
        records_by_subtopic=grouped_records,
    )
    return (
        RUNTIME_DEPS.planning_quality_row(
            subtopic_id=planning.subtopic_id,
            violations=list(planning.violations),
            atomic_objectives=list(planning.atomic_objectives),
        ),
        {
            "subtopic_id": subtopic_id,
            "topic": scope_context["topic"],
            "subtopic": scope_context["subtopic"],
            "atomic_objectives": len(planning.atomic_objectives),
            "total_kcs": sum(len(plan.candidate_kcs) for plan in planning.kc_plans.values()),
            "assessment_items": sum(
                len(items) for items in planning.assessment_items_by_atomic_objective.values()
            ),
            "violations": len(planning.violations),
            "is_valid": not any(violation.severity == "error" for violation in planning.violations),
            "cached_planning": planning.from_cache,
        },
    )


def main() -> None:
    args = _parse_args()
    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = (
        Path(args.report_path).expanduser()
        if args.report_path
        else output_dir / "quality-report.txt"
    )
    summary_path = (
        Path(args.summary_path).expanduser() if args.summary_path else output_dir / "summary.json"
    )

    topics_path = Path(args.topics).expanduser()
    scheme_path = Path(args.scheme).expanduser()
    records_path = Path(args.records).expanduser()
    topics_payload = RUNTIME_DEPS.load_json(topics_path)
    scheme_payload = RUNTIME_DEPS.load_json(scheme_path)
    if not isinstance(topics_payload, list):
        raise ValueError("topics file must contain a list of topic rows")
    if not isinstance(scheme_payload, dict):
        raise ValueError("scheme file must contain an object keyed by term")
    topics = cast(list[JsonObject], topics_payload)
    scheme = cast(JsonObject, scheme_payload)

    rows = _iter_curriculum_subtopics(topics, scheme)
    if args.subtopic_id:
        rows = [row for row in rows if row["subtopic_id"] == args.subtopic_id]

    grouped_records = _records_by_subtopic(records_path)
    pipeline = RUNTIME_DEPS.infrastructure_planning_pipeline(
        model_name=RUNTIME_DEPS.model_name(),
        cache_dir=output_dir,
    )
    quality_rows: list[PlanningQualityRow] = []
    summary_rows: list[JsonObject] = []

    for row in rows:
        quality_row, summary_row = build_subtopic_infrastructure(
            pipeline=pipeline,
            row=row,
            topics=topics,
            scheme=scheme,
            grouped_records=grouped_records,
        )
        quality_rows.append(quality_row)
        summary_rows.append(summary_row)

    report_text = RUNTIME_DEPS.render_infrastructure_quality_report(quality_rows)
    report_path.write_text(report_text + "\n", encoding="utf-8")
    summary_path.write_text(json.dumps(summary_rows, indent=2), encoding="utf-8")
    print(report_text)
    print(f"\nSummary written to {summary_path}")


if __name__ == "__main__":
    main()
