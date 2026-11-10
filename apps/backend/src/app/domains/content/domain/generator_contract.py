"""What a plugin's spec must keep for the type it adds a generator to."""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path

from app.domains.artefacts.core.domain.part_fields import PartField
from app.domains.artefacts.core.domain.parts import Unit
from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.artefacts.core.domain.types import ArtefactScope
from app.shared.json_types import JsonValue

#: Types that accept a plugin's generator. A type is added here with the destination that
#: stores what a generator writes and the test that holds a generator to it.
TAKES_GENERATORS = frozenset({"lesson-plan", "lesson-note", "class-test", "revision-note"})

#: Types whose generator writes fixed fields, and what reads them.
_FIXED_PARTS = {
    "class-test": "the question fields grading reads",
    "revision-note": "the section fields a learner's pack is made from",
}
_SCHEMAS = ("unit", "parts", "lesson_parts")
#: Types whose consumers read the stored shape part by part, so a generator keeps its schemas.
_KEEPS_SCHEMAS = frozenset({"lesson-plan"})


#: Types whose generator may also write one learner's copy, and what that copy may adapt.
_LEARNER_TYPES = frozenset({"revision-note"})
#: What a learner's revision note may be adapted in, and so what a check holds the rest to.
LEARNER_ADAPTABLE = (
    "depth of explanation",
    "worked support",
    "hints",
    "feedback",
    "practice difficulty",
    "misconception repair",
)


@cache
def fixed_parts(slug: str, learner: bool = False) -> list[JsonValue]:
    """The part a generator of the type writes, in the form a spec stores it."""
    suffix = "_learner" if learner else ""
    path = Path(__file__).parents[1] / f"{slug.replace('-', '_')}{suffix}_parts.json"
    records = json.loads(path.read_text(encoding="utf-8"))
    return [PartField.from_record(record).to_record() for record in records]


def refuse_unfit_spec(slug: str, own: ContentSpecification, plugin: ContentSpecification) -> None:
    """Refuse a plugin spec the type's stored shape cannot take.

    A generator may change the writing skills and the requirements, and the engine builds class
    level only. A lesson plan is read part by part, so its generator keeps its unit and part
    schemas. A lesson note is read as markdown for each plan step, so its generator writes
    parts for each step in any fields: they are set down as markdown when it is saved.
    """
    if slug not in TAKES_GENERATORS:
        raise ValueError(f"{slug} takes no generator from a plugin")
    if plugin.levels == frozenset({ArtefactScope.LEARNER_LEVEL}) and slug in _LEARNER_TYPES:
        _refuse_unfit_learner_spec(slug, plugin)
        return
    if plugin.levels != frozenset({ArtefactScope.CLASS_LEVEL}):
        raise ValueError(f"a generator of {slug} builds class level only")
    if slug in _FIXED_PARTS:
        if plugin.unit is not Unit.LESSON_OBJECTIVE or plugin.lesson_parts:
            raise ValueError(f"a generator of {slug} writes one part for each lesson objective")
        written = [f.to_record() for f in plugin.parts.fields] if plugin.parts else None
        if written != fixed_parts(slug):
            raise ValueError(f"a generator of {slug} keeps {_FIXED_PARTS[slug]}")
        return
    if slug in _KEEPS_SCHEMAS:
        own_record, plugin_record = own.to_record(), plugin.to_record()
        changed = [name for name in _SCHEMAS if own_record[name] != plugin_record[name]]
        if changed:
            raise ValueError(f"a generator of {slug} keeps the type's {', '.join(changed)}")
        return
    if plugin.unit is not Unit.PLAN_STEP or plugin.parts is None or plugin.lesson_parts:
        raise ValueError(f"a generator of {slug} writes one part for each plan step")


def _refuse_unfit_learner_spec(slug: str, plugin: ContentSpecification) -> None:
    """A learner's copy keeps the class parts and adds the misconception repair."""
    if plugin.unit is not Unit.LESSON_OBJECTIVE or plugin.lesson_parts:
        raise ValueError(f"a learner generator of {slug} writes one part for each lesson objective")
    written = [f.to_record() for f in plugin.parts.fields] if plugin.parts else None
    if written != fixed_parts(slug, learner=True):
        raise ValueError(
            f"a learner generator of {slug} keeps the section fields a learner's note is made from"
        )
    if plugin.adaptable != LEARNER_ADAPTABLE:
        raise ValueError(f"a learner generator of {slug} adapts {', '.join(LEARNER_ADAPTABLE)}")
