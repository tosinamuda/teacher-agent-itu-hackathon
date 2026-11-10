"""Start, fill, read and submit drafts: the use cases behind the MCP tools.

Every type is drafted the same way: one checked part per unit, then submitted. A type differs
only in what it is made from, the schema of each part, and where the finished draft is
saved, which its destination decides. Every refusal is a ``DraftError`` whose message tells
the writer what to do instead, because the writer is often a model that can act on it.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.core.domain.specification import ContentSpecification
from app.domains.content.application.catalogue import ContentCatalogue
from app.domains.content.application.errors import ContentError
from app.domains.content.domain.generators import GeneratorKind
from app.domains.content.domain.types import ContentTypeDefinition, Engine, Level
from app.domains.content_engine.application.content_destination import Check
from app.domains.content_engine.application.draft_view import DraftView
from app.domains.content_engine.application.drafting_ports import (
    ContentStore,
    Destination,
    Drafts,
    Drawings,
    Learners,
    Lessons,
)
from app.domains.content_engine.application.planning_ports import Planning
from app.domains.content_engine.domain.draft import Draft, DraftError, parts_of
from app.domains.content_engine.domain.lesson import (
    LESSON_UNIT_ID,
    LessonFrame,
    LessonUnit,
    LessonUnitsError,
    lesson_material,
    lesson_units,
)
from app.domains.content_engine.domain.locate import Place, locate
from app.shared.json_types import JsonObject
from app.shared.readers import reader_for


@dataclass(frozen=True)
class LessonRef:
    """What a draft is made from: a frozen plan version, or a lesson period."""

    plan_version_id: str | None = None
    session_id: str | None = None
    #: The learner whose copy of the lesson's content it is, for content made for one learner.
    student_id: str | None = None


@dataclass(frozen=True)
class Revising:
    """Content a draft revises: the spec revision it was written with, and its parts."""

    spec_revision: int | None
    parts: dict[str, JsonObject]


@dataclass(frozen=True)
class DraftPreview:
    draft: Draft
    #: What the draft would save as so far.
    content: JsonObject
    issues: list[str]

    def status(self) -> str:
        missing = self.draft.missing()
        if missing:
            return f"missing {', '.join(missing)}"
        return "has issues" if self.issues else "ready to submit"


class DraftingService:
    def __init__(
        self,
        *,
        catalogue: ContentCatalogue,
        drafts: Drafts,
        lessons: Lessons,
        planning: Planning,
        content: ContentStore,
        destinations: Mapping[str, Destination],
        engine_destination: Destination,
        drawings: Drawings,
        learners: Learners | None = None,
        learner_destinations: Mapping[str, Destination] | None = None,
        scripted_check: Check | None = None,
    ) -> None:
        """``destinations`` saves the built-in types drafted by slug; engine types use the other.

        ``learner_destinations`` saves the types drafted for one learner, and ``learners`` says
        what the writer may read about that learner. ``scripted_check`` finds the faults that
        the draft's plugin has its own scripts for, whatever the type.
        """
        self._catalogue = catalogue
        self._drafts = drafts
        self._lessons = lessons
        self._planning = planning
        self._content = content
        self._destinations = destinations
        self._engine_destination = engine_destination
        self._drawings = drawings
        self._learners = learners
        self._learner_destinations = learner_destinations or {}
        self._scripted_check = scripted_check

    async def start(
        self,
        db: AsyncSession,
        *,
        type: str,
        lesson: LessonRef,
        created_by: str,
        author: str | None = None,
        source: str = "",
        content_id: str | None = None,
        generator: str | None = None,
    ) -> DraftView:
        """Open a draft of ``type`` for the lesson, or of existing content to revise it.

        ``generator`` names the generator to write with when it is not the type's default.
        """
        definition = await self._draftable(db, type)
        self._refuse_wrong_lesson(definition, lesson)
        self._refuse_wrong_learner(definition, lesson, content_id)
        frame = await self._open_frame(db, lesson)
        revising = await self._revising(db, definition, lesson, content_id)
        spec = await self._spec(
            db,
            definition,
            revising.spec_revision if revising else None,
            _level_of(lesson),
            generator,
        )
        try:
            units = lesson_units(frame, spec)
        except LessonUnitsError as error:
            raise DraftError(str(error)) from error
        if spec.unit is None:
            raise DraftError(f"{spec.kind} has no part schema, so it is not drafted")
        if lesson.student_id is not None and lesson.plan_version_id is not None:
            units = await self._adaptable_units(
                db, units, lesson.plan_version_id, lesson.student_id
            )
        draft = Draft(
            draft_id=self._drafts.new_id(),
            type=definition.slug,
            kind=definition.kind,
            spec_revision=spec.revision,
            plan_version_id=lesson.plan_version_id,
            session_id=lesson.session_id,
            unit=spec.unit,
            units=units,
            source=source.strip(),
            saved_as=content_id,
            created_by=created_by,
            author=author,
            student_id=lesson.student_id,
        )
        if revising is not None:
            known = set(draft.unit_ids())
            draft.parts = {k: v for k, v in revising.parts.items() if k in known}
        await self._drafts.add(db, draft)
        await db.commit()
        return await self._view(db, draft, spec, frame)

    async def put(
        self,
        db: AsyncSession,
        *,
        draft_id: str,
        unit_id: str,
        part: object,
        replace: bool,
        by: str,
    ) -> JsonObject:
        """Add a unit's part, or replace it. Returns it as stored, with what is left to do."""
        draft = await self._own_draft(db, draft_id, by, for_update=True)
        spec = await self._draft_spec(db, draft)
        frame = await self._frame(db, _ref(draft))
        stored = draft.put(unit_id, part, spec, replace=replace, formulas=frame.formulas)
        await self._drafts.save(db, draft)
        await db.commit()
        return {
            "unit_id": unit_id,
            "part": stored,
            "missing": [*draft.missing()],
            "issues": [*await self._issues(db, draft)],
        }

    async def read(self, db: AsyncSession, *, draft_id: str, by: str) -> DraftView:
        draft = await self._own_draft(db, draft_id, by, for_update=False)
        spec = await self._draft_spec(db, draft)
        return await self._view(db, draft, spec, await self._frame(db, _ref(draft)))

    async def locate(self, db: AsyncSession, *, draft_id: str, text: str, by: str) -> list[Place]:
        """Where text the teacher selected is in the draft: the unit and field of each place."""
        draft = await self._own_draft(db, draft_id, by, for_update=False)
        return locate(draft.parts, text)

    async def preview(self, db: AsyncSession, *, draft_id: str, by: str) -> DraftPreview:
        """What the draft would save as from the parts written so far, and what stops it."""
        draft = await self._own_draft(db, draft_id, by, for_update=False)
        content = (await self._destination_of(db, draft)).preview(draft)
        return DraftPreview(draft, content, await self._issues(db, draft))

    async def submit(self, db: AsyncSession, *, draft_id: str, by: str) -> str:
        """Save the finished draft for the teacher's review. Returns what it is saved as."""
        draft = await self._own_draft(db, draft_id, by, for_update=True)
        await self._open_frame(db, _ref(draft))
        draft.refuse_if_incomplete()
        issues = await self._issues(db, draft)
        if issues:
            raise DraftError("fix these first: " + "; ".join(issues))
        destination = await self._destination_of(db, draft)
        spec = await self._draft_spec(db, draft)
        generator = await self._catalogue.generator_of_spec(
            db, await self._draftable(db, draft.type), spec.revision
        )
        draft.submitted(await destination.save(db, draft, spec, generator.provenance()))
        await self._drafts.save(db, draft)
        await db.commit()
        if draft.saved_as is None:
            raise DraftError("the draft was submitted but nothing was saved")
        return draft.saved_as

    async def _adaptable_units(
        self, db: AsyncSession, units: tuple[LessonUnit, ...], plan_version_id: str, student_id: str
    ) -> tuple[LessonUnit, ...]:
        """The units the learner's marked work is enough to adapt; the rest stay as they are."""
        assert self._learners is not None
        adapted = set(await self._learners.adapted(db, plan_version_id, student_id))
        kept = tuple(unit for unit in units if unit.unit_id in adapted)
        if not kept:
            raise DraftError("no objective has enough marked work from this learner to adapt")
        return kept

    async def learner(self, db: AsyncSession, *, draft_id: str, by: str) -> JsonObject:
        """What the writer may read about the learner a draft adapts the content to."""
        draft = await self._own_draft(db, draft_id, by, for_update=False)
        if draft.student_id is None or draft.plan_version_id is None or self._learners is None:
            raise DraftError("this draft is not made for one learner")
        return await self._learners.context(db, draft.plan_version_id, draft.student_id)

    async def lesson(self, db: AsyncSession, plan_version_id: str) -> JsonObject:
        """What a writer may read about a planned lesson."""
        plan = await self._lessons.plan(db, plan_version_id)
        if plan is None:
            raise DraftError(f"there is no plan version {plan_version_id!r}")
        note = await self._lessons.approved_note_sections(db, plan_version_id)
        return lesson_material(plan, note)

    async def lesson_period(self, db: AsyncSession, session_id: str) -> JsonObject:
        """What a writer may read about a lesson period that has no plan yet."""
        lesson = await self._planning.lesson(db, session_id)
        if lesson is None:
            raise DraftError(f"there is no lesson {session_id!r}")
        return {
            **lesson.facts,
            "curriculum_objectives": [*lesson.curriculum_objectives],
            **lesson.grounding,
        }

    async def _issues(self, db: AsyncSession, draft: Draft) -> list[str]:
        """What stops a finished draft being saved: drawings that will not draw, then the rest.

        The plugin's own scripts are cheap and exact, so the destination's review, which may
        call a model, reads a draft only when the scripts find nothing.
        """
        if draft.missing():
            return []
        spec = await self._draft_spec(db, draft)
        drawings = await self._drawing_issues(draft, spec)
        scripted = await self._scripted_check(db, draft) if self._scripted_check else []
        if scripted:
            return [*drawings, *scripted]
        return [*drawings, *await (await self._destination_of(db, draft)).issues(db, draft)]

    async def _drawing_issues(self, draft: Draft, spec: ContentSpecification) -> list[str]:
        found: list[str] = []
        for unit, part in draft.written():
            for path, source in spec.schema_for(unit.unit).drawings(part):
                if problem := await self._drawings.problem(source):
                    found.append(f"the {unit.unit_id} part, at {path}: it does not draw: {problem}")
        return found

    async def _view(
        self, db: AsyncSession, draft: Draft, spec: ContentSpecification, frame: LessonFrame
    ) -> DraftView:
        brief: JsonObject = spec.brief(reader_for(frame.grade)).model_dump()
        skills = await self._catalogue.skills_of(db, spec)
        if skills:
            brief["skills"] = [skill.for_writer() for skill in skills]
        return DraftView(draft, spec, brief, await self._issues(db, draft))

    async def _draftable(self, db: AsyncSession, slug: str) -> ContentTypeDefinition:
        try:
            definition = await self._catalogue.type(db, slug)
        except ContentError as error:
            raise DraftError(f"there is no content type {slug!r}") from error
        self._destination(definition)
        if await self._catalogue.retired(db, slug):
            raise DraftError(f"the plugin that added {slug!r} has been removed")
        return definition

    async def drafts(self, db: AsyncSession, definition: ContentTypeDefinition) -> bool:
        """Whether a new draft of the type can be started with these tools now.

        The type needs a destination, and its default generator must be the engine's: a native
        pipeline default makes the type's content itself. A type whose plugin was removed is not
        offered.
        """
        if await self._catalogue.retired(db, definition.slug):
            return False
        try:
            self._destination(definition)
            binding = await self._catalogue.generator(db, definition, Level.CLASS)
        except (DraftError, ContentError):
            return False
        return binding.harness is GeneratorKind.ENGINE

    def _destination(self, definition: ContentTypeDefinition) -> Destination:
        if definition.engine is Engine.MCP:
            return self._engine_destination
        destination = self._destinations.get(definition.slug)
        if destination is None:
            raise DraftError(f"{definition.slug} has a generator of its own and is not drafted")
        return destination

    async def _destination_of(self, db: AsyncSession, draft: Draft) -> Destination:
        if draft.student_id is not None:
            return self._learner_destinations[draft.type]
        return self._destination(await self._draftable(db, draft.type))

    @staticmethod
    def _refuse_wrong_lesson(definition: ContentTypeDefinition, lesson: LessonRef) -> None:
        if definition.made_from_a_plan_version and lesson.plan_version_id is None:
            raise DraftError(f"{definition.slug} is made from a plan version: give plan_version_id")
        if not definition.made_from_a_plan_version and lesson.session_id is None:
            raise DraftError(f"{definition.slug} is made from its lesson: give session_id")
        if lesson.plan_version_id is not None and lesson.session_id is not None:
            raise DraftError("give plan_version_id or session_id, not both")

    def _refuse_wrong_learner(
        self, definition: ContentTypeDefinition, lesson: LessonRef, content_id: str | None
    ) -> None:
        if lesson.student_id is None:
            return
        if definition.slug not in self._learner_destinations or self._learners is None:
            raise DraftError(f"{definition.slug} is not written for one learner")
        if lesson.plan_version_id is None or lesson.session_id is not None:
            raise DraftError("content for one learner is made from a plan version: give it")
        if content_id is not None:
            raise DraftError("content for one learner is written again, not revised, here")

    async def _spec(
        self,
        db: AsyncSession,
        definition: ContentTypeDefinition,
        revision: int | None,
        level: Level = Level.CLASS,
        generator: str | None = None,
    ) -> ContentSpecification:
        try:
            if revision is None:
                return await self._catalogue.drafting_spec(db, definition.slug, level, generator)
            return await self._catalogue.revision(db, definition.slug, revision)
        except ContentError as error:
            raise DraftError(error.detail) from error

    async def _draft_spec(self, db: AsyncSession, draft: Draft) -> ContentSpecification:
        return await self._spec(
            db, await self._draftable(db, draft.type), draft.spec_revision, _level_of(_ref(draft))
        )

    async def _revising(
        self,
        db: AsyncSession,
        definition: ContentTypeDefinition,
        lesson: LessonRef,
        content_id: str | None,
    ) -> Revising | None:
        if content_id is None:
            return None
        if not definition.made_from_a_plan_version:
            return await self._revising_plan(db, definition, lesson, content_id)
        if lesson.plan_version_id is None:
            raise DraftError(f"a {definition.slug} draft does not revise saved content")
        stored = await self._content.get(db, content_id)
        if stored is None or stored.kind != definition.kind:
            raise DraftError(f"there is no {definition.slug} {content_id!r} to revise")
        if stored.plan_version_id != lesson.plan_version_id:
            raise DraftError(f"{content_id} belongs to plan version {stored.plan_version_id}")
        return Revising(stored.spec_revision, parts_of(stored.manifest))

    async def _revising_plan(
        self, db: AsyncSession, definition: ContentTypeDefinition, lesson: LessonRef, plan_id: str
    ) -> Revising:
        """A lesson's plan as it stands, split into the parts it is written in."""
        record = await self._planning.current(db, plan_id)
        if record is None:
            raise DraftError(f"there is no {definition.slug} {plan_id!r} to revise")
        if _bare(record.session_id) != _bare(lesson.session_id):
            raise DraftError(f"{plan_id} is the plan of lesson {record.session_id}")
        if record.concluded:
            raise DraftError("the lesson's study has concluded, so its content cannot change")
        return Revising(None, {LESSON_UNIT_ID: record.lesson, **record.sections})

    async def _frame(self, db: AsyncSession, lesson: LessonRef) -> LessonFrame:
        if lesson.plan_version_id is not None:
            plan = await self._lessons.plan(db, lesson.plan_version_id)
            if plan is None:
                raise DraftError(f"there is no plan version {lesson.plan_version_id!r}")
            return LessonFrame.of_plan(plan)
        period = await self._planning.lesson(db, str(lesson.session_id))
        if period is None:
            raise DraftError(f"there is no lesson {lesson.session_id!r}")
        facts = period.facts
        title = str(facts.get("subtopic") or facts.get("topic") or "The lesson")
        return LessonFrame(
            title,
            str(facts.get("grade") or ""),
            period.curriculum_objectives,
            subject=str(facts.get("subject") or ""),
        )

    async def _open_frame(self, db: AsyncSession, lesson: LessonRef) -> LessonFrame:
        frame = await self._frame(db, lesson)
        if lesson.plan_version_id is not None and await self._lessons.concluded(
            db, lesson.plan_version_id
        ):
            raise DraftError("the lesson's study has concluded, so its content cannot change")
        return frame

    async def _own_draft(
        self, db: AsyncSession, draft_id: str, by: str, *, for_update: bool
    ) -> Draft:
        draft = await self._drafts.get(db, draft_id, for_update=for_update)
        if draft is None or draft.created_by != by:
            raise DraftError(f"there is no draft {draft_id!r} of yours")
        return draft


def _bare(session_id: str | None) -> str:
    """A lesson period's ID without its dashes, so both spellings of one UUID compare equal."""
    return (session_id or "").replace("-", "").lower()


def _ref(draft: Draft) -> LessonRef:
    return LessonRef(
        plan_version_id=draft.plan_version_id,
        session_id=draft.session_id,
        student_id=draft.student_id,
    )


def _level_of(lesson: LessonRef) -> Level:
    return Level.LEARNER if lesson.student_id is not None else Level.CLASS
