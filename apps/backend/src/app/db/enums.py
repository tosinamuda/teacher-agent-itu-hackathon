"""Helper for declaring native enum columns from Python ``str, Enum`` classes.

``Enum(MyEnum, name=...)`` defaults to using each member's *Python attribute name*
(uppercase) as the enum label, which mismatches the lowercase values stored in
existing rows. ``status_enum`` forces the labels to come from each member's
``.value`` instead — the canonical string form used everywhere in code and in
the DB today.
"""

from __future__ import annotations

from collections.abc import Iterable
from enum import Enum
from typing import TypeVar

from sqlalchemy import Enum as SqlaEnum

E = TypeVar("E", bound=Enum)


def status_enum(enum_class: type[E], *, name: str) -> SqlaEnum:
    """Build a SQLAlchemy ``Enum`` column type using the enum's ``.value`` strings."""
    return SqlaEnum(
        enum_class,
        name=name,
        values_callable=_member_values,
    )


def _member_values(members: Iterable[Enum]) -> list[str]:
    return [str(member.value) for member in members]
