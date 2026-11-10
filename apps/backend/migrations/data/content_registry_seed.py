"""Seed the built-in content types, the shipped skills, and every kind's seed specification.

Idempotent: a type, a (skill, revision) or a (kind, revision) already stored is left as it
is, so what a researcher added later is never overwritten and re-running adds only what is
missing. Skills are seeded before specifications, which pin them.
"""

from __future__ import annotations

import uuid

import sqlalchemy as sa

from app.domains.artefacts.specifications.seed import seed_specifications
from app.domains.content.domain.generators import GeneratorStatus
from app.domains.content.seed import seed_generators, seed_types
from app.domains.content.skill_seed import seed_skills

_TYPES = sa.table(
    "content_types",
    sa.column("id", sa.Uuid),
    sa.column("slug"),
    sa.column("kind"),
    sa.column("label"),
    sa.column("audience"),
    sa.column("engine"),
    sa.column("made_from_a_plan_version", sa.Boolean),
    sa.column("position", sa.Integer),
    sa.column("created_by"),
)

_SPECIFICATIONS = sa.table(
    "content_specifications",
    sa.column("id", sa.Uuid),
    sa.column("kind"),
    sa.column("revision"),
    sa.column("material"),
    sa.column("audience"),
    sa.column("levels", sa.JSON),
    sa.column("structure", sa.JSON),
    sa.column("requirements", sa.JSON),
    sa.column("adaptable", sa.JSON),
    sa.column("unit"),
    sa.column("parts", sa.JSON),
    sa.column("lesson_parts", sa.JSON),
    sa.column("skills", sa.JSON),
    sa.column("mcp", sa.JSON),
    sa.column("generator"),
    sa.column("created_by"),
)

_GENERATORS = sa.table(
    "content_type_generators",
    sa.column("id", sa.Uuid),
    sa.column("type_slug"),
    sa.column("level"),
    sa.column("harness"),
    sa.column("schema_source"),
    sa.column("ref"),
    sa.column("spec_revision", sa.Integer),
    sa.column("status"),
    sa.column("default_key"),
    sa.column("changed_by"),
)

_SKILLS = sa.table(
    "content_skills",
    sa.column("id", sa.Uuid),
    sa.column("slug"),
    sa.column("revision", sa.Integer),
    sa.column("name"),
    sa.column("description"),
    sa.column("instructions"),
    sa.column("files", sa.JSON),
    sa.column("created_by"),
)


def seed_content_skills(conn: sa.Connection) -> int:
    """Insert every shipped skill revision not already stored. Returns how many were added."""
    stored = set(conn.execute(sa.select(_SKILLS.c.slug, _SKILLS.c.revision)).tuples())
    added = 0
    for skill in seed_skills():
        if (skill.slug, skill.revision) in stored:
            continue
        conn.execute(
            _SKILLS.insert().values(
                id=uuid.uuid4(),
                slug=skill.slug,
                revision=skill.revision,
                name=skill.name,
                description=skill.description,
                instructions=skill.instructions,
                files=[{"path": f.path, "text": f.text} for f in skill.files],
                created_by="seed",
            )
        )
        added += 1
    return added


def seed_content_types(conn: sa.Connection) -> int:
    """Insert every built-in type not already stored. Returns how many were added."""
    stored = set(conn.execute(sa.select(_TYPES.c.slug)).scalars())
    added = 0
    for built_in in seed_types():
        if built_in.slug in stored:
            continue
        conn.execute(
            _TYPES.insert().values(
                id=uuid.uuid4(),
                slug=built_in.slug,
                kind=built_in.kind,
                label=built_in.label,
                audience=built_in.audience.value,
                engine=built_in.engine.value,
                made_from_a_plan_version=built_in.made_from_a_plan_version,
                position=built_in.position,
                created_by="seed",
            )
        )
        added += 1
    return added


def _seeded(rows: list[sa.Row], record: dict[str, object]) -> bool:
    """Whether a seed row holds ``record``: by its revision number, or by its content.

    A plugin's revision takes the next number of its kind, so a seed revision may find its number
    taken. The content then says whether the seed was stored under a later number.
    """
    same = {key: value for key, value in record.items() if key != "revision"}
    return any(
        row.generator is None
        and (
            row.revision == record["revision"]
            or all(getattr(row, key) == value for key, value in same.items())
        )
        for row in rows
    )


def seed_content_specifications(conn: sa.Connection) -> int:
    """Insert every seed revision not already stored. Returns how many were added.

    A seed revision whose number a plugin's revision holds is stored as the kind's next revision.
    """
    stored: dict[str, list[sa.Row]] = {}
    for row in conn.execute(sa.select(_SPECIFICATIONS)).all():
        stored.setdefault(row.kind, []).append(row)
    registry = seed_specifications()
    added = 0
    for kind in registry.kinds():
        record = registry.specification(kind).to_record()
        rows = stored.get(kind, [])
        if _seeded(rows, record):
            continue
        taken = {row.revision for row in rows}
        number = record["revision"] if record["revision"] not in taken else max(taken) + 1
        conn.execute(
            _SPECIFICATIONS.insert().values(
                id=uuid.uuid4(), created_by="seed", **{**record, "revision": number}
            )
        )
        added += 1
    return added


def seed_content_generators(conn: sa.Connection) -> int:
    """Insert every built-in generator not already stored. Returns how many were added.

    A stored row keeps its status, so a default someone changed is not put back.
    """
    stored = set(
        conn.execute(
            sa.select(
                _GENERATORS.c.type_slug,
                _GENERATORS.c.level,
                _GENERATORS.c.harness,
                _GENERATORS.c.ref,
            )
        ).tuples()
    )
    taken = set(conn.execute(sa.select(_GENERATORS.c.default_key)).scalars())
    added = 0
    for binding in seed_generators():
        if (binding.type_slug, binding.level.value, binding.harness.value, binding.ref) in stored:
            continue
        default_key = f"{binding.type_slug}:{binding.level.value}"
        is_default = binding.status is GeneratorStatus.DEFAULT and default_key not in taken
        conn.execute(
            _GENERATORS.insert().values(
                id=uuid.uuid4(),
                type_slug=binding.type_slug,
                level=binding.level.value,
                harness=binding.harness.value,
                schema_source=binding.schema.value,
                ref=binding.ref,
                spec_revision=binding.spec_revision,
                status=(GeneratorStatus.DEFAULT if is_default else GeneratorStatus.AVAILABLE).value,
                default_key=default_key if is_default else None,
                changed_by="seed",
            )
        )
        if is_default:
            taken.add(default_key)
        added += 1
    return added


def seed_content_registry(conn: sa.Connection) -> tuple[int, int, int, int]:
    """Seed types, skills, specifications, then generators. Returns how many of each were added."""
    return (
        seed_content_types(conn),
        seed_content_skills(conn),
        seed_content_specifications(conn),
        seed_content_generators(conn),
    )
