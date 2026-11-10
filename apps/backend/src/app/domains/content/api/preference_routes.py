"""A teacher's own settings: which optional materials they use."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.content.domain.preferences import CORE_ORDER, CORE_TYPES, is_optional
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.teacher_preferences import TeacherPreferences
from app.shared.auth import Actor
from app.shared.authz import requires
from app.shared.schema_base import StrictRequest

router = APIRouter(prefix="/content/preferences", tags=["content"])


class Material(BaseModel):
    type: str
    label: str
    #: What it makes, in a few words.
    description: str
    #: Built in: always on, and the teacher cannot switch it off.
    core: bool
    enabled: bool


class PreferencesResponse(BaseModel):
    """Every material the app has, the core ones first, each on or off for this teacher."""

    materials: list[Material]


class Switch(StrictRequest):
    enabled: bool


def _sentence(text: str) -> str:
    return text[:1].upper() + text[1:] if text else ""


async def _read(db: AsyncSession, actor: Actor) -> PreferencesResponse:
    hidden = await TeacherPreferences().hidden(db, actor.auth_id)
    catalogue = build_content_catalogue()
    types = {definition.slug: (definition, spec) for definition, spec in await catalogue.types(db)}
    core = [types[slug] for slug in CORE_ORDER if slug in types]
    optional = [
        types[slug]
        for slug in types
        if is_optional(types[slug][0], retired=await catalogue.retired(db, slug))
    ]
    return PreferencesResponse(
        materials=[
            Material(
                type=definition.slug,
                label=definition.label,
                description=_sentence(spec.material),
                core=definition.slug in CORE_TYPES,
                enabled=definition.slug not in hidden,
            )
            for definition, spec in [*core, *optional]
        ]
    )


@router.get("", response_model=PreferencesResponse)
async def read_preferences(
    actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> PreferencesResponse:
    """The optional materials, each on or off for this teacher."""
    return await _read(db, actor)


@router.put("/materials/{type}", response_model=PreferencesResponse)
async def switch_material(
    type: str,
    body: Switch,
    actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> PreferencesResponse:
    """Turn an optional material on or off for this teacher. The core materials stay on."""
    if type not in {m.type for m in (await _read(db, actor)).materials if not m.core}:
        raise HTTPException(status_code=422, detail="material_is_always_on")
    await TeacherPreferences().set_material(db, actor.auth_id, type, body.enabled)
    await db.commit()
    return await _read(db, actor)
