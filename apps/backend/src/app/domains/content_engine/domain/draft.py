"""A draft: content of one type being written for one lesson, one checked part per unit.

A part is stored only once it matches the spec's schema for its unit, and a draft is saved
only once every unit has a part, so what is saved always has the shape its spec declares.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from app.domains.artefacts.core.domain.part_fields import PartInvalidError
from app.domains.artefacts.core.domain.parts import Unit
from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.content_engine.domain.lesson import LessonUnit
from app.shared.json_types import JsonObject, JsonValue


class DraftStatus(str, Enum):
    OPEN = "open"
    SUBMITTED = "submitted"


class DraftError(ValueError):
    """A request the draft refuses; the message says what to do instead."""


@dataclass
class Draft:
    draft_id: str
    #: The slug of the type being written.
    type: str
    kind: str
    spec_revision: int
    #: What it is made from: a frozen plan version, or else a lesson period.
    plan_version_id: str | None
    session_id: str | None
    unit: Unit
    units: tuple[LessonUnit, ...]
    #: A document the draft is written from, such as a teacher's own plan.
    source: str = ""
    #: The part for each unit that has one, by unit ID.
    parts: dict[str, JsonObject] = field(default_factory=dict)
    status: DraftStatus = DraftStatus.OPEN
    #: What the draft is saved as: the content it revises, or what it became once submitted.
    saved_as: str | None = None
    #: Who started it; only they work on it.
    created_by: str = ""
    #: The teacher whose work it is, recorded as the author of what it saves.
    author: str | None = None
    #: The learner a draft adapts the lesson's content to; none for class content.
    student_id: str | None = None

    def put(
        self,
        unit_id: str,
        part: object,
        spec: ContentSpecification,
        *,
        replace: bool,
        formulas: bool = True,
    ) -> JsonObject:
        """Store the unit's part, checked against its schema. Returns the part as stored."""
        self._refuse_if_submitted()
        unit = self._unit(unit_id)
        if replace and unit_id not in self.parts:
            raise DraftError(f"unit {unit_id!r} has no part yet; add it with add_part")
        if not replace and unit_id in self.parts:
            raise DraftError(f"unit {unit_id!r} already has a part; change it with revise_part")
        try:
            schema = spec.schema_for(unit.unit)
        except ValueError as error:
            raise DraftError(str(error)) from error
        try:
            stored = schema.validate(part, formulas=formulas)
        except PartInvalidError as error:
            what_next = (
                "The part is unchanged."
                if replace
                else "Nothing was stored: correct it and call add_part again."
            )
            raise DraftError(f"the part does not match its schema: {error}. {what_next}") from error
        self.parts[unit_id] = stored
        return stored

    def _unit(self, unit_id: str) -> LessonUnit:
        for unit in self.units:
            if unit.unit_id == unit_id:
                return unit
        raise DraftError(f"unknown unit {unit_id!r}; the units are: {', '.join(self.unit_ids())}")

    def unit_ids(self) -> list[str]:
        return [unit.unit_id for unit in self.units]

    def missing(self) -> list[str]:
        """The units still without a part, in order."""
        return [unit_id for unit_id in self.unit_ids() if unit_id not in self.parts]

    def written(self) -> list[tuple[LessonUnit, JsonObject]]:
        """Each unit that has a part, with it, in order."""
        return [
            (unit, self.parts[unit.unit_id]) for unit in self.units if unit.unit_id in self.parts
        ]

    def sections(self) -> list[JsonValue]:
        """The parts written so far, one section per unit, in the lesson's order."""
        return [
            {"unit_id": unit.unit_id, "unit": unit.unit.value, "label": unit.label, "part": part}
            for unit, part in self.written()
        ]

    def refuse_if_incomplete(self) -> None:
        missing = self.missing()
        if missing:
            raise DraftError(f"every unit needs a part first; missing: {', '.join(missing)}")

    def submitted(self, saved_as: str) -> None:
        """Close the draft as saved."""
        self._refuse_if_submitted()
        self.refuse_if_incomplete()
        self.status = DraftStatus.SUBMITTED
        self.saved_as = saved_as

    def _refuse_if_submitted(self) -> None:
        if self.status is DraftStatus.SUBMITTED:
            raise DraftError(f"draft {self.draft_id} is already saved as {self.saved_as}")


def parts_of(manifest: JsonObject) -> dict[str, JsonObject]:
    """The parts of stored engine content, by unit ID, to reopen it as a draft."""
    sections = manifest.get("sections")
    if not isinstance(sections, list):
        raise DraftError("the content has no sections to revise")
    parts: dict[str, JsonObject] = {}
    for section in sections:
        part = section.get("part") if isinstance(section, dict) else None
        if isinstance(section, dict) and isinstance(part, dict):
            parts[str(section.get("unit_id"))] = part
    return parts
