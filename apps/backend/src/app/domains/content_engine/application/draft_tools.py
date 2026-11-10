"""A stored draft read for the tools of the app's MCP server that a plugin lists."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content_engine.additions import Adder
from app.domains.content_engine.application.drafting_ports import Drafts, Lessons
from app.domains.content_engine.domain.draft import Draft, DraftError
from app.domains.content_engine.rules import Rule
from app.shared.json_types import JsonObject, JsonValue
from app.shared.session_plan_view import SessionPlanView

#: Reviews a stored draft against more than the draft: the lesson in the database, or a model.
Review = Callable[[AsyncSession, Draft], Awaitable[list[str]]]


class DraftTools:
    """Reads a draft and what its lesson holds, and applies the rule or the adder a tool names."""

    def __init__(
        self,
        drafts: Drafts,
        lessons: Lessons,
        checks: Mapping[str, Rule],
        adders: Mapping[str, Adder],
        reviews: Mapping[str, Review],
    ) -> None:
        self._drafts = drafts
        self._lessons = lessons
        self._checks = checks
        self._adders = adders
        self._reviews = reviews

    @property
    def check_tools(self) -> list[str]:
        return sorted({*self._checks, *self._reviews})

    @property
    def add_tools(self) -> list[str]:
        return sorted(self._adders)

    async def faults(
        self, db: AsyncSession, *, tool: str, draft_id: str, only_by: str | None
    ) -> list[str]:
        """The faults the tool's rule finds in the draft as it is stored.

        ``only_by`` names the one person whose draft it may read; ``None`` reads any draft.
        """
        review = self._reviews.get(tool)
        rule = self._checks.get(tool)
        if review is None and rule is None:
            raise DraftError(f"there is no check {tool!r}")
        draft = await self._draft(db, draft_id, only_by)
        if review is not None:
            return await review(db, draft)
        payload: JsonObject = {
            "draft": {"type": draft.type, "sections": draft.sections()},
            "source": await self._source(db, draft),
        }
        return rule(payload) if rule is not None else []

    async def additions(
        self, db: AsyncSession, *, tool: str, draft_id: str, only_by: str | None
    ) -> JsonObject:
        """The fields the tool's adder says to save with the draft's content."""
        adder = self._adders.get(tool)
        if adder is None:
            raise DraftError(f"there is no adding tool {tool!r}")
        draft = await self._draft(db, draft_id, only_by)
        return adder(await self._plan(db, draft))

    async def _draft(self, db: AsyncSession, draft_id: str, only_by: str | None) -> Draft:
        draft = await self._drafts.get(db, draft_id, for_update=False)
        if draft is None or (only_by is not None and draft.created_by != only_by):
            raise DraftError(f"there is no draft {draft_id!r} of yours")
        return draft

    async def _plan(self, db: AsyncSession, draft: Draft) -> SessionPlanView | None:
        if draft.plan_version_id is None:
            return None
        return await self._lessons.plan(db, draft.plan_version_id)

    async def _source(self, db: AsyncSession, draft: Draft) -> JsonObject | None:
        """What the lesson holds that a draft must agree with: its approved note and objectives."""
        if draft.plan_version_id is None:
            return None
        plan = await self._plan(db, draft)
        by_step: dict[str, JsonValue] = {
            objective.lesson_objective_id: objective.objective_text or ""
            for objective in (plan.lesson_plan_objectives if plan else [])
        }
        return {
            "note": dict(await self._lessons.approved_note_sections(db, draft.plan_version_id)),
            "objectives": [text for text in by_step.values() if text],
            "objectives_by_step": by_step,
        }
