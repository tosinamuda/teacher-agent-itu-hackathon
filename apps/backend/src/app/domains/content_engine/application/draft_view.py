"""A draft as a writer reads it: what to write, for which units, and what is in so far."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.content_engine.domain.draft import Draft
from app.shared.json_types import JsonObject


def lesson_uri(draft: Draft) -> str:
    """The resource a writer reads the draft's lesson from."""
    if draft.plan_version_id is not None:
        return f"lesson://{draft.plan_version_id}"
    return f"lesson-period://{draft.session_id}"


def learner_uri(draft: Draft) -> str | None:
    """The resource a writer reads the learner's context from, for a draft made for one learner."""
    return f"learner://{draft.draft_id}" if draft.student_id is not None else None


@dataclass(frozen=True)
class DraftView:
    draft: Draft
    spec: ContentSpecification
    brief: JsonObject
    #: What stops the finished draft being saved; checked once every unit has a part.
    issues: list[str] = field(default_factory=list)

    def part_schemas(self) -> JsonObject:
        """The JSON Schema each kind of unit's part must match, by unit."""
        kinds = dict.fromkeys(unit.unit for unit in self.draft.units)
        return {unit.value: self.spec.schema_for(unit).json_schema() for unit in kinds}

    def as_json(self) -> JsonObject:
        draft = self.draft
        view: JsonObject = {
            "draft_id": draft.draft_id,
            "type": draft.type,
            "plan_version_id": draft.plan_version_id,
            "session_id": draft.session_id,
            "lesson_uri": lesson_uri(draft),
            "spec_revision": self.spec.revision,
            "status": draft.status.value,
            "saved_as": draft.saved_as,
            "brief": self.brief,
            "units": [
                {
                    "unit_id": unit.unit_id,
                    "unit": unit.unit.value,
                    "label": unit.label,
                    "has_part": unit.unit_id in draft.parts,
                }
                for unit in draft.units
            ],
            "missing": [*draft.missing()],
            "issues": [*self.issues],
            "parts": {**draft.parts},
            "part_schemas": self.part_schemas(),
        }
        if (learner := learner_uri(draft)) is not None:
            view["student_id"] = draft.student_id
            view["learner_uri"] = learner
        if self.spec.skills:
            view["pinned_skills"] = [ref.to_record() for ref in self.spec.skills]
        if draft.source:
            view["source"] = draft.source
        return view
