"""One curated atomic objective, as the curated planning path reads it.

The raw linkage rows (see ``curated_planning``) are normalised here into
``CuratedObjective``: its evidence records bucketed by role, its bloom level and
its curated assessment.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from app.shared.json_types import JsonObject


def _dict_list(value: object) -> list[JsonObject]:
    """List narrowing; ``[]`` if not a list.

    Local replacement for the retired ``json_coerce.as_object_list``.
    """
    return cast(list[JsonObject], value) if isinstance(value, list) else []


def _stripped_str_list(value: object) -> list[str]:
    """Strip+filter on a list of strings; ``[]`` if not a list.

    Local replacement for the retired ``json_coerce.as_str_list``.
    """
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


# Role -> evidence bucket. Foundation + instruction are explanatory (concept);
# worked_example is modeling; exercise/practice are practice.
_CONCEPT_ROLES = frozenset({"foundation", "instruction"})
_MODELING_ROLES = frozenset({"worked_example"})
_PRACTICE_ROLES = frozenset({"exercise"})

_VALID_BLOOM = frozenset({"remember", "understand", "apply", "analyze"})


@dataclass(frozen=True)
class CuratedObjective:
    """Normalised curated atomic objective ready for artefact construction."""

    ao_id: str
    ao_order: int
    curriculum_objective_id: str
    objective_text: str
    bloom_level: str
    concept_record_ids: list[str]
    modeling_record_ids: list[str]
    practice_record_ids: list[str]
    assessment: JsonObject | None

    @property
    def supporting_record_ids(self) -> list[str]:
        """All curated records for this objective, de-duplicated, order-stable."""
        ordered: list[str] = []
        seen: set[str] = set()
        for record_id in (
            *self.concept_record_ids,
            *self.modeling_record_ids,
            *self.practice_record_ids,
        ):
            if record_id and record_id not in seen:
                seen.add(record_id)
                ordered.append(record_id)
        return ordered

    @property
    def kc_type(self) -> str:
        """Derive kc_type from the curated evidence shape.

        A procedure needs a worked example; if there is no modeling record the
        objective is taught as a concept (explanation only). This mirrors
        `required_block_types_for_kc` in the session_plan schema.
        """
        if self.modeling_record_ids:
            return "procedure"
        return "concept"

    @property
    def lesson_objective_id(self) -> str:
        return self.ao_id

    @property
    def kc_id(self) -> str:
        return f"{self.ao_id}-kc01"

    @property
    def normalized_bloom(self) -> str:
        value = (self.bloom_level or "").strip().lower()
        return value if value in _VALID_BLOOM else "apply"


def normalize_curated_objective(payload: JsonObject) -> CuratedObjective:
    """Turn one raw curated AO dict into a normalised CuratedObjective."""
    links = _dict_list(payload.get("record_links"))
    by_role: dict[str, list[tuple[int, str]]] = {}
    for link in links:
        if not isinstance(link, dict):
            continue
        record_id = str(link.get("record_id") or "").strip()
        role = str(link.get("role") or "").strip()
        if not record_id or not role:
            continue
        order = link.get("link_order")
        order = int(order) if isinstance(order, (int, float)) else 0
        by_role.setdefault(role, []).append((order, record_id))

    def ordered_for(roles: frozenset[str]) -> list[str]:
        collected: list[tuple[int, str]] = []
        for role, entries in by_role.items():
            if role in roles:
                collected.extend(entries)
        collected.sort(key=lambda item: item[0])
        result: list[str] = []
        seen: set[str] = set()
        for _, record_id in collected:
            if record_id not in seen:
                seen.add(record_id)
                result.append(record_id)
        return result

    # Practice prefers the explicitly-curated practice_record_ids; fall back to
    # exercise-role links so a procedure always has practice evidence available.
    curated_practice = _stripped_str_list(payload.get("practice_record_ids"))
    practice = curated_practice or ordered_for(_PRACTICE_ROLES)

    assessment = payload.get("assessment")
    assessment_obj = assessment if isinstance(assessment, dict) else None

    ao_order_raw = payload.get("ao_order")
    ao_order = (
        int(ao_order_raw) if isinstance(ao_order_raw, (int, float, str)) and ao_order_raw else 0
    )

    return CuratedObjective(
        ao_id=str(payload.get("ao_id") or "").strip(),
        ao_order=ao_order,
        curriculum_objective_id=str(payload.get("curriculum_objective_id") or "").strip(),
        objective_text=str(payload.get("objective_text") or "").strip(),
        bloom_level=str(payload.get("bloom_level") or "").strip(),
        concept_record_ids=ordered_for(_CONCEPT_ROLES),
        modeling_record_ids=ordered_for(_MODELING_ROLES),
        practice_record_ids=practice,
        assessment=assessment_obj,
    )
