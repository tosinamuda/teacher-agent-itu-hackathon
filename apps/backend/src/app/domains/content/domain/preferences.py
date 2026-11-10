"""Which materials a teacher can switch off."""

from __future__ import annotations

from app.domains.content.domain.types import ContentTypeDefinition

#: The materials a teacher always has: the plan, and what is made from it first. Every other
#: material a plugin adds is the teacher's to turn on or off.
CORE_ORDER = ("lesson-plan", "lesson-note", "revision-note", "class-test")
CORE_TYPES = frozenset(CORE_ORDER)


def is_optional(definition: ContentTypeDefinition, *, retired: bool) -> bool:
    """Whether a teacher can switch the type off: a class material that is not a core one.

    An `-engine` type is a variant kept to compare how a material is made, not a material.
    """
    return (
        definition.made_from_a_plan_version
        and not retired
        and definition.slug not in CORE_TYPES
        and not definition.slug.endswith("-engine")
    )
