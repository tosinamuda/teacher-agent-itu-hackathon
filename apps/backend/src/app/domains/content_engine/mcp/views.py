"""Content types and content as MCP clients read them."""

from __future__ import annotations

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.content.application.records import ContentItem
from app.domains.content.domain.types import ContentTypeDefinition
from app.shared.json_types import JsonObject

#: JSON as an MCP client's schema shows it: a plain object. ``JsonObject`` is recursive,
#: and a self-referencing schema sends DSPy's ``$ref`` resolver into endless recursion.
Payload = dict[str, object]


def as_payload(value: JsonObject) -> Payload:
    """JSON the app built, as the plain object an MCP tool returns."""
    return {**value}


def type_json(definition: ContentTypeDefinition, spec: ContentSpecification) -> JsonObject:
    return {
        "type": definition.slug,
        "label": definition.label,
        "audience": definition.audience.value,
        "engine": definition.engine.value,
        "made_from_a_plan_version": definition.made_from_a_plan_version,
        "spec": {
            "revision": spec.revision,
            "material": spec.material,
            "audience": spec.audience,
            "requirements": list(spec.requirements),
            "structure": list(spec.structure),
            "unit": spec.unit.value if spec.unit is not None else None,
            "part_schema": spec.parts.json_schema() if spec.parts is not None else None,
            "skills": [ref.to_record() for ref in spec.skills],
            "mcp": [server.public() for server in spec.mcp],
        },
    }


def content_json(item: ContentItem, spec: ContentSpecification | None = None) -> JsonObject:
    """The item as a reader is given it; ``spec`` adds the order its parts' fields are drawn in.

    Storage does not keep the order of an object's keys, so the spec the content was built
    with is what says it.
    """
    record = item.record
    shown: JsonObject = {
        "content_id": record.content_id,
        "type": record.type,
        "plan_version_id": record.plan_version_id,
        "version": record.version,
        "review_status": record.review_status,
        "content": item.content,
    }
    if spec is not None:
        shown["parts"] = spec.to_record()["parts"]
        shown["lesson_parts"] = spec.to_record()["lesson_parts"]
    return shown
