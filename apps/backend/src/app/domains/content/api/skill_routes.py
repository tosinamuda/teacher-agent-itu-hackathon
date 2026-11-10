"""The skill library over HTTP: list and read skills, and add a skill's next revision."""

from __future__ import annotations

from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.content.application.errors import ContentError
from app.domains.content.domain.skills import Skill, SkillError, SkillFile
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.shared.auth import Actor
from app.shared.authz import requires
from app.shared.schema_base import StrictRequest

router = APIRouter(prefix="/content/skills", tags=["content"])


class SkillFileBody(StrictRequest):
    """A reference file: markdown at a path under ``references/``."""

    path: str
    text: str


class SkillBody(StrictRequest):
    """A skill's next revision: a name, when to use it, and the instructions."""

    slug: str = Field(..., min_length=1, max_length=64)
    name: str = Field(..., min_length=1, max_length=120)
    description: str = Field(..., min_length=1)
    instructions: str = Field(..., min_length=1)
    files: list[SkillFileBody] = Field(default_factory=list)


class SkillResponse(BaseModel):
    skill: str
    revision: int
    name: str
    description: str
    instructions: str
    files: list[str]

    @classmethod
    def of(cls, skill: Skill) -> SkillResponse:
        return cls(
            skill=skill.slug,
            revision=skill.revision,
            name=skill.name,
            description=skill.description,
            instructions=skill.instructions,
            files=[file.path for file in skill.files],
        )


def _raise(error: ContentError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail) from error


@router.get("", response_model=list[SkillResponse])
async def list_skills(
    _actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> list[SkillResponse]:
    """Every skill at its latest revision."""
    return [SkillResponse.of(skill) for skill in await build_content_catalogue().skills.skills(db)]


@router.get("/{slug}", response_model=SkillResponse)
async def get_skill(
    slug: str,
    _actor: Actor = Depends(requires(obj="content:*", act="read")),
    db: AsyncSession = Depends(get_db),
) -> SkillResponse:
    try:
        return SkillResponse.of(await build_content_catalogue().skills.skill(db, slug))
    except ContentError as error:
        _raise(error)


@router.post("", response_model=SkillResponse, status_code=201)
async def add_skill(
    body: SkillBody,
    actor: Actor = Depends(requires(obj="content_type:*", act="revise")),
    db: AsyncSession = Depends(get_db),
) -> SkillResponse:
    """Store the skill as its slug's next revision. A spec adopts it by pinning that revision."""
    try:
        files = tuple(SkillFile(file.path, file.text) for file in body.files)
        skill = Skill(body.slug, 1, body.name, body.description, body.instructions, files)
    except SkillError as error:
        raise HTTPException(status_code=422, detail=f"invalid_skill:{error}") from error
    stored = await build_content_catalogue().skills.add(db, skill, actor.display_name)
    await db.commit()
    return SkillResponse.of(stored)
