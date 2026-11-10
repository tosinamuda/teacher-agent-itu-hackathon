"""Request and response bodies for content types and content."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.domains.artefact_revision.api.schemas import RevisionHighlight
from app.domains.artefacts.core.domain.parts import Unit
from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.types.post_class_review_pack.domain.expert_sources import ExpertSources
from app.domains.content.domain.generators import GeneratorBinding
from app.domains.content.domain.types import Audience, ContentTypeDefinition, Engine, Level
from app.shared.json_types import JsonObject
from app.shared.schema_base import StrictRequest, UtcDatetime


class SpecBody(StrictRequest):
    """A spec's content: what content of the type is and must do (α, β, γ, F, R, D)."""

    material: str = Field(..., min_length=1)
    audience: str = Field(..., min_length=1)
    levels: list[Level] = Field(..., min_length=1)
    #: F in words. An engine type may leave it out: its part schema says it.
    structure: list[str] = Field(default_factory=list)
    requirements: list[str] = Field(..., min_length=1)
    adaptable: list[str] = Field(default_factory=list)
    #: What one part covers, for an engine type.
    unit: Unit | None = None
    #: The fields of one part, for an engine type: name, description, type, required, fields.
    parts: list[JsonObject] | None = None
    #: The fields of a part written once for the whole lesson, besides each unit's.
    lesson_parts: list[JsonObject] | None = None
    #: The skills its content is written with: ``{"skill": slug, "revision": n}`` each.
    skills: list[JsonObject] = Field(default_factory=list)
    #: The external MCP servers its content is written with: ``{"server": name, "url": https URL,
    #: "tools": the tools it may use, "secret": the environment variable holding its token}``.
    mcp: list[JsonObject] = Field(default_factory=list)

    def as_fields(self) -> dict[str, object]:
        return {
            "material": self.material,
            "audience": self.audience,
            "levels": [level.stored_as.value for level in self.levels],
            "structure": self.structure,
            "requirements": self.requirements,
            "adaptable": self.adaptable,
            "unit": self.unit.value if self.unit is not None else None,
            "parts": self.parts,
            "lesson_parts": self.lesson_parts,
            "skills": self.skills,
            "mcp": self.mcp,
        }


class SpecResponse(BaseModel):
    revision: int
    material: str
    audience: str
    levels: list[Level]
    structure: list[str]
    requirements: list[str]
    adaptable: list[str]
    unit: Unit | None
    parts: list[JsonObject] | None
    #: The JSON Schema every part is checked against, for an engine type.
    part_schema: JsonObject | None
    lesson_parts: list[JsonObject] | None
    #: The JSON Schema the lesson's own part is checked against, when there is one.
    lesson_part_schema: JsonObject | None
    #: The skills its content is written with, each pinned at a revision.
    skills: list[JsonObject]
    #: The external servers it is written with and the tools of each; where they are is not shown.
    mcp: list[JsonObject]

    @classmethod
    def of(cls, spec: ContentSpecification) -> SpecResponse:
        return cls(
            revision=spec.revision,
            material=spec.material,
            audience=spec.audience,
            levels=sorted(
                (Level.of(scope.value) for scope in spec.levels), key=lambda level: level.value
            ),
            structure=list(spec.structure),
            requirements=list(spec.requirements),
            adaptable=list(spec.adaptable),
            unit=spec.unit,
            parts=spec.parts.to_record() if spec.parts is not None else None,
            part_schema=spec.parts.json_schema() if spec.parts is not None else None,
            lesson_parts=lessons.to_record() if (lessons := spec.lesson_parts) else None,
            lesson_part_schema=lessons.json_schema() if lessons else None,
            skills=[ref.to_record() for ref in spec.skills],
            mcp=[server.public() for server in spec.mcp],
        )


class GeneratorResponse(BaseModel):
    """One way of making a type's content, and whether it is the default."""

    level: Level
    harness: str
    schema_source: str
    ref: str
    status: str
    spec_revision: int | None

    @classmethod
    def of(cls, binding: GeneratorBinding) -> GeneratorResponse:
        return cls(
            level=binding.level,
            harness=binding.harness.value,
            schema_source=binding.schema.value,
            ref=binding.ref,
            status=binding.status.value,
            spec_revision=binding.spec_revision,
        )


class DefaultGeneratorRequest(StrictRequest):
    level: Level = Level.CLASS
    generator: str = Field(..., min_length=1, max_length=128)


class ContentTypeResponse(BaseModel):
    type: str
    label: str
    audience: Audience
    engine: Engine
    made_from_a_plan_version: bool
    spec: SpecResponse
    #: Whether the plugin that added the type has been removed: content stays readable, and
    #: there are no new drafts of it.
    retired: bool = False
    generators: list[GeneratorResponse] = []

    @classmethod
    def of(
        cls,
        type: ContentTypeDefinition,
        spec: ContentSpecification,
        *,
        retired: bool = False,
        generators: list[GeneratorBinding] | None = None,
    ) -> ContentTypeResponse:
        return cls(
            type=type.slug,
            label=type.label,
            audience=type.audience,
            engine=type.engine,
            made_from_a_plan_version=type.made_from_a_plan_version,
            spec=SpecResponse.of(spec),
            retired=retired,
            generators=[GeneratorResponse.of(binding) for binding in generators or []],
        )


class RegisterTypeRequest(StrictRequest):
    """A new content type for the engine to build, with its first spec."""

    #: The slug, such as `worked-examples`.
    type: str = Field(..., min_length=1, max_length=64)
    label: str = Field(..., min_length=1, max_length=120)
    audience: Audience
    made_from_a_plan_version: bool = True
    spec: SpecBody


class GenerateContentRequest(StrictRequest):
    plan_version_id: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1)
    level: Level = Level.CLASS
    #: The generator to use, by its ref: a revision note's pipeline version by date, a plugin's
    #: name, or `builtin` for the original program. The type's default when omitted.
    pipeline: str | None = None
    #: The expert content a revision note is grounded in; the lesson note when omitted.
    sources: ExpertSources | None = None
    #: What to make, in the teacher's own words. An engine type's writer reads it with its brief.
    instructions: str | None = Field(None, min_length=1, max_length=4000)


class ContentSummary(BaseModel):
    id: str
    type: str
    level: Level
    plan_version_id: str
    student_id: str | None
    version: int
    review_status: str
    created_at: UtcDatetime | None
    provenance: JsonObject
    #: Its lesson's study has concluded: it can be read, never changed.
    read_only: bool
    #: Why the teacher rejected it or withdrew it.
    review_reason: str | None = None


class ContentResponse(ContentSummary):
    content: JsonObject
    #: The checks it passed and the passages it cites, as recorded when it was written.
    review: JsonObject | None = None
    #: Its type's plugin lists a tool that makes it into a file, which can be downloaded.
    has_file: bool = False


class RevisionRequest(StrictRequest):
    feedback: str = Field(..., min_length=1)
    #: Where the teacher pointed: a unit, the path of a field in its part, and the text selected.
    highlight: RevisionHighlight | None = None


class RevisionResponse(BaseModel):
    turn_number: int
    feedback: str
    summary: str | None
    created_at: UtcDatetime
    highlight: RevisionHighlight | None = None


class GenerationProgressLine(BaseModel):
    """One thing the agent making content said or did, as the chat keeps it."""

    id: int
    kind: str
    data: JsonObject


class GenerationProgress(BaseModel):
    """What the agent has done since the caller last read, and where to read on from."""

    lines: list[GenerationProgressLine]
    next: int


class ApprovalRequest(StrictRequest):
    #: The version the teacher reviewed; an approval of an older version is refused (409).
    expected_version: int


class RejectionRequest(StrictRequest):
    #: The version the teacher reviewed; a rejection of an older version is refused (409).
    expected_version: int
    #: Why it is rejected or withdrawn, in the teacher's words.
    reason: str = Field(..., min_length=3, max_length=500)


class ApprovalResponse(BaseModel):
    id: str
    approved_version: int
    approved_by: str | None
    approved_at: UtcDatetime
