"""What a content type is: the framework's specification Σ = ⟨α, β, γ, F, R, D⟩.

A kind is described here and generated elsewhere. Every field is data, so what a kind
promises can be read, listed and compared without running its generator.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.domains.artefacts.core.domain.mcp_refs import McpServerRef
from app.domains.artefacts.core.domain.parts import PartSchema, Unit
from app.domains.artefacts.core.domain.skill_refs import SkillRef
from app.domains.artefacts.core.domain.types import ArtefactScope
from app.shared.json_types import JsonObject


class ArtefactSpec(BaseModel):
    """What is being produced, for whom, under which requirements — as a generator reads it.

    For the revision pack it is identical across every condition: the conditions differ in
    what they are told about the lesson, never in what they are asked to write.
    """

    model_config = ConfigDict(extra="forbid")

    artefact: str
    audience: str
    requirements: list[str] = Field(default_factory=list)


@dataclass(frozen=True)
class ContentSpecification:
    """One content type, fixed before any of it is generated.

    ``audience`` may name the reader through ``{reader}``, filled from the lesson's grade
    when a request is built. ``adaptable`` empty means the kind is never adapted to a
    learner, and then ``levels`` must be class level only. ``unit`` and ``parts`` are set
    together, for a kind drafted part by part; ``lesson_parts`` adds one part written once
    for the whole lesson, before the part for each unit.
    """

    kind: str
    #: Which stored revision of this kind's specification this is. Every artefact records
    #: the revision it was generated against.
    revision: int
    #: α — what the content is, as the generator is told it.
    material: str
    #: β — who reads it.
    audience: str
    #: γ — the levels it is produced at.
    levels: frozenset[ArtefactScope]
    #: F — its parts, in order.
    structure: tuple[str, ...]
    #: R — the requirements every instance must satisfy.
    requirements: tuple[str, ...]
    #: D — the only dimensions adaptation may change.
    adaptable: tuple[str, ...] = ()
    #: What one part covers, for engine-built content.
    unit: Unit | None = None
    #: F as a checked schema: the part written for each unit.
    parts: PartSchema | None = None
    #: The part written once for the whole lesson, when there is one besides each unit's.
    lesson_parts: PartSchema | None = None
    #: The skills its content is written with, each pinned at a revision.
    skills: tuple[SkillRef, ...] = ()
    #: The external MCP servers its content is written with, and the tools of each it may use.
    mcp: tuple[McpServerRef, ...] = ()

    def __post_init__(self) -> None:
        """Refuse a specification whose levels, adaptation or parts disagree."""
        if not self.levels:
            raise ValueError(f"{self.kind}: content is produced at some level")
        if ArtefactScope.LEARNER_LEVEL in self.levels and not self.adaptable:
            raise ValueError(
                f"{self.kind}: learner-level content must declare what adaptation may change"
            )
        if self.adaptable and ArtefactScope.LEARNER_LEVEL not in self.levels:
            raise ValueError(f"{self.kind}: only learner-level content is adapted")
        if (self.unit is None) != (self.parts is None):
            raise ValueError(f"{self.kind}: unit and parts are set together")
        if self.lesson_parts is not None and self.unit in (None, Unit.LESSON):
            raise ValueError(f"{self.kind}: lesson_parts sit beside the parts of a smaller unit")
        names = [server.name for server in self.mcp]
        if len(set(names)) != len(names):
            raise ValueError(f"{self.kind}: each external server is listed once")

    def schema_for(self, unit: Unit) -> PartSchema:
        """The fields of the part a unit of this kind takes."""
        if unit is Unit.LESSON and self.lesson_parts is not None:
            return self.lesson_parts
        if unit is not self.unit or self.parts is None:
            raise ValueError(f"{self.kind} has no part for a {unit.value.replace('_', ' ')}")
        return self.parts

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> ContentSpecification:
        """Read a stored specification: a database row or a seed-file entry."""
        unit = Unit(record["unit"]) if record.get("unit") is not None else None
        schema = _schema(record.get("parts"))
        lesson_schema = _schema(record.get("lesson_parts"))
        structure = tuple(record.get("structure") or ()) or _structure(unit, schema, lesson_schema)
        return cls(
            kind=str(record["kind"]),
            revision=int(record["revision"]),
            material=str(record["material"]),
            audience=str(record["audience"]),
            levels=frozenset(ArtefactScope(level) for level in record["levels"]),
            structure=structure,
            requirements=tuple(record["requirements"]),
            adaptable=tuple(record.get("adaptable") or ()),
            unit=unit,
            parts=schema,
            lesson_parts=lesson_schema,
            skills=tuple(SkillRef.from_record(ref) for ref in record.get("skills") or ()),
            mcp=tuple(McpServerRef.from_record(ref) for ref in record.get("mcp") or ()),
        )

    def to_record(self) -> dict[str, Any]:
        """The specification as it is stored."""
        return {
            "kind": self.kind,
            "revision": self.revision,
            "material": self.material,
            "audience": self.audience,
            "levels": sorted(level.value for level in self.levels),
            "structure": list(self.structure),
            "requirements": list(self.requirements),
            "adaptable": list(self.adaptable),
            "unit": self.unit.value if self.unit is not None else None,
            "parts": self.parts.to_record() if self.parts is not None else None,
            "lesson_parts": (
                self.lesson_parts.to_record() if self.lesson_parts is not None else None
            ),
            "skills": [ref.to_record() for ref in self.skills],
            "mcp": [server.to_record() for server in self.mcp],
        }

    def audience_for(self, reader: str) -> str:
        """β with the reader named."""
        return self.audience.format(reader=reader)

    def brief(self, reader: str) -> ArtefactSpec:
        """The part of the specification a generator is told: α, β and R."""
        return ArtefactSpec(
            artefact=self.material,
            audience=self.audience_for(reader),
            requirements=list(self.requirements),
        )


def _schema(record: object) -> PartSchema | None:
    return PartSchema.from_record(record) if record is not None else None


def _structure(
    unit: Unit | None, parts: PartSchema | None, lesson_parts: PartSchema | None
) -> tuple[str, ...]:
    """F in words, from the part schemas, for a spec that does not state it."""
    if parts is None or unit is None:
        return ()
    if lesson_parts is None:
        return parts.summary()
    each = unit.value.replace("_", " ")
    return (
        *(f"for the lesson: {line}" for line in lesson_parts.summary()),
        *(f"for each {each}: {line}" for line in parts.summary()),
    )


def specification_ref(specification: ContentSpecification) -> JsonObject:
    """What an artefact records about the specification it was generated against."""
    return {
        "specification": {
            "kind": specification.kind,
            "revision": specification.revision,
        }
    }
