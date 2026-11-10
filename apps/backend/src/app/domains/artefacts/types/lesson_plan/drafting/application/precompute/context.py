from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import cast

from pydantic import BaseModel

from app.domains.artefacts.types.lesson_plan.drafting.application.precompute.types import (
    ObjectiveContext,
    derive_scope_keys,
    slugify,
)
from app.domains.artefacts.types.lesson_plan.drafting.domain.generation_inputs import (
    LessonCurriculumContext,
    LessonScope,
    TextbookRecordPayload,
)
from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import AtomicObjective
from app.shared.json_types import JsonObject


def _dict_or_none(value: object) -> JsonObject | None:
    """Return ``value`` cast to a ``JsonObject`` if it is a dict, else ``None``.

    Local replacement for the retired ``json_coerce.as_object``.
    """
    return cast(JsonObject, value) if isinstance(value, dict) else None


def _dict_list(value: object) -> list[JsonObject]:
    """Pass-through list narrowing (keeps non-dict items so the caller can decide).

    Local replacement for the retired ``json_coerce.as_object_list``.
    """
    return cast(list[JsonObject], value) if isinstance(value, list) else []


def _stripped_str_list(value: object) -> list[str]:
    """Strip-and-filter narrow on a list of strings; ``[]`` if not a list.

    Local replacement for the retired ``json_coerce.as_str_list``.
    """
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _json_object_from_mapping(value: Mapping[str, object]) -> JsonObject:
    return cast(JsonObject, dict(value))


def _coerce_textbook_record(record: TextbookRecordPayload | Mapping[str, object]) -> JsonObject:
    if isinstance(record, TextbookRecordPayload):
        return record.model_dump()
    return _json_object_from_mapping(record)


def _coerce_objective_list(value: object) -> list[str]:
    return [str(item).strip() for item in _dict_list(value) if str(item).strip()]


def _optional_int(value: object) -> int | None:
    if not isinstance(value, (int, float, str)):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _optional_str(value: object) -> str | None:
    normalized = str(value or "").strip()
    return normalized or None


class _IndexedSubtopic(BaseModel):
    subtopic_id: str
    title: str
    performance_objectives: list[str]
    entry_behaviour: list[str]
    position: int


class _IndexedTopic(BaseModel):
    topic_key: str
    subtopics: list[_IndexedSubtopic]


class ObjectiveContextBuilder:
    """Build the constrained input for KC extraction using only local data."""

    def __init__(
        self,
        *,
        scope_context: LessonScope | Mapping[str, object],
        curriculum_context: LessonCurriculumContext | Mapping[str, object],
        textbook_records: Sequence[TextbookRecordPayload | Mapping[str, object]],
        topics_enriched: Sequence[Mapping[str, object]] | None = None,
        scheme: Mapping[str, object] | None = None,
        records_by_subtopic: Mapping[
            str,
            Sequence[TextbookRecordPayload | Mapping[str, object]],
        ]
        | None = None,
    ) -> None:
        self._scope_context = (
            scope_context.model_dump()
            if isinstance(scope_context, LessonScope)
            else dict(scope_context)
        )
        self._curriculum_context = (
            curriculum_context.model_dump()
            if isinstance(curriculum_context, LessonCurriculumContext)
            else dict(curriculum_context)
        )
        self._textbook_records: list[JsonObject] = [
            _coerce_textbook_record(record) for record in textbook_records
        ]
        self._topic_key, self._subtopic_id = derive_scope_keys(self._scope_context)
        self._topics_by_key = self._index_topics(topics_enriched or [])
        self._scheme_index = self._index_scheme(_json_object_from_mapping(scheme or {}))
        self._records_by_subtopic: dict[str, list[JsonObject]] = {
            self._subtopic_id: list(self._textbook_records),
        }
        if records_by_subtopic is not None:
            self._records_by_subtopic = {
                subtopic_id: [_coerce_textbook_record(record) for record in records]
                for subtopic_id, records in records_by_subtopic.items()
            }

    def _index_topics(
        self,
        topics_enriched: Sequence[Mapping[str, object]],
    ) -> dict[str, JsonObject]:
        indexed: dict[str, JsonObject] = {}
        for topic in topics_enriched:
            topic_key = str(topic.get("topic_key") or "").strip() or slugify(
                str(topic.get("topic") or "topic")
            )
            subtopics: list[_IndexedSubtopic] = []
            subtopic_rows = _dict_list(topic.get("subtopics"))
            for position, raw_subtopic in enumerate(subtopic_rows, start=1):
                subtopic = _dict_or_none(raw_subtopic)
                if subtopic is None:
                    continue
                subtopic_id = str(subtopic.get("subtopic_id") or "").strip()
                if not subtopic_id:
                    continue
                subtopics.append(
                    _IndexedSubtopic(
                        subtopic_id=subtopic_id,
                        title=str(
                            subtopic.get("subtopic_title") or subtopic.get("title") or ""
                        ).strip(),
                        performance_objectives=_coerce_objective_list(
                            subtopic.get("performance_objectives")
                        ),
                        entry_behaviour=_coerce_objective_list(subtopic.get("entry_behaviour")),
                        position=position,
                    )
                )
            indexed[topic_key] = _IndexedTopic(topic_key=topic_key, subtopics=subtopics).model_dump(
                mode="json"
            )
        return indexed

    def _index_scheme(self, scheme: JsonObject) -> dict[str, JsonObject]:
        indexed: dict[str, JsonObject] = {}
        for term, weeks in scheme.items():
            if not isinstance(weeks, list):
                continue
            for week in weeks:
                week_payload = _dict_or_none(week)
                if week_payload is None:
                    continue
                week_number = _optional_int(week_payload.get("week"))
                breakdown_rows = _dict_list(week_payload.get("breakdown"))
                breakdown: list[JsonObject] = []
                for item in breakdown_rows:
                    item_payload = _dict_or_none(item)
                    if item_payload is None:
                        continue
                    if not str(item_payload.get("subtopic_id") or "").strip():
                        continue
                    breakdown.append(item_payload)
                co_scheduled_ids = [
                    str(item.get("subtopic_id") or "").strip() for item in breakdown
                ]
                for order, item in enumerate(breakdown, start=1):
                    subtopic_id = str(item.get("subtopic_id") or "").strip()
                    indexed[subtopic_id] = {
                        "term": str(term).strip() or None,
                        "week": week_number,
                        "order": order,
                        "co_scheduled_subtopic_ids": [
                            current_id
                            for current_id in co_scheduled_ids
                            if current_id != subtopic_id
                        ],
                    }
        return indexed

    def _prior_subtopic_objectives(self) -> list[str]:
        topic = self._topics_by_key.get(self._topic_key)
        if topic is None:
            return _coerce_objective_list(self._curriculum_context.get("entry_behaviour"))

        prior_objectives: list[str] = []
        for raw_subtopic in _dict_list(topic.get("subtopics")):
            subtopic = _dict_or_none(raw_subtopic)
            if subtopic is None:
                continue
            subtopic_id = str(subtopic.get("subtopic_id") or "").strip()
            if subtopic_id == self._subtopic_id:
                break
            objective_candidates = [
                *_coerce_objective_list(subtopic.get("performance_objectives")),
                *_coerce_objective_list(subtopic.get("entry_behaviour")),
            ]
            for objective in objective_candidates:
                normalized = str(objective).strip()
                if normalized and normalized not in prior_objectives:
                    prior_objectives.append(normalized)

        if prior_objectives:
            return prior_objectives
        return _coerce_objective_list(self._curriculum_context.get("entry_behaviour"))

    def assemble(self, atomic_objective: AtomicObjective) -> ObjectiveContext:
        schedule_info = self._scheme_index.get(self._subtopic_id, {})
        scheduled_term = _optional_str(schedule_info.get("term"))
        scheduled_week = _optional_int(schedule_info.get("week"))
        co_scheduled_subtopic_ids = _stripped_str_list(
            schedule_info.get("co_scheduled_subtopic_ids")
        )
        primary_records = self._records_by_subtopic.get(self._subtopic_id)
        return ObjectiveContext(
            atomic_objective=atomic_objective,
            subtopic_id=self._subtopic_id,
            topic_key=self._topic_key,
            prior_subtopic_objectives=self._prior_subtopic_objectives(),
            primary_records=list(primary_records or self._textbook_records),
            evaluation_guide=[
                str(item).strip()
                for item in _dict_list(self._curriculum_context.get("evaluation_guide"))
                if str(item).strip()
            ],
            scheduled_term=scheduled_term,
            scheduled_week=scheduled_week,
            co_scheduled_subtopic_ids=co_scheduled_subtopic_ids,
        )
