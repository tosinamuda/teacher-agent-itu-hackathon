"""Generate + persist the objective-indexed MCQ diagnostic for a lesson."""

from __future__ import annotations

import json
import logging
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

from pydantic import ValidationError
from sqlalchemy import delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.retry import run_with_deadlock_retry
from app.domains.artefacts.core.application.specifications import ContentSpecifications
from app.domains.artefacts.core.domain.specification import ArtefactSpec, ContentSpecification
from app.domains.artefacts.core.domain.types import ArtefactType
from app.domains.artefacts.specifications.seed import seed_specification
from app.domains.assessments.application.diagnostic_generator import (
    DiagnosticItemGenerator,
    DiagnosticMCQItem,
)
from app.domains.assessments.application.exit_ticket_payload import exit_ticket_payload
from app.domains.assessments.application.item_reader import (
    ItemReader,
    ItemToRead,
    reads_as_keyed,
)
from app.domains.assessments.domain.item_checks import is_sound, says_what_it_asks
from app.domains.assessments.domain.item_level import reaches_scale
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.domains.generation_log.application.recorder import log_context
from app.shared.json_types import JsonObject
from app.shared.readers import reader_for
from app.shared.session_plan_view import LessonPlanObjectiveView, SessionPlanView

logger = logging.getLogger(__name__)

#: How many draws an objective gets to yield enough gradable items.
_DRAWS = 3

SUBTOPIC_SQL = text(
    """
    select lp.subtopic_id as subtopic_id,
           pv.session_plan as session_plan
    from plan_versions pv
    join lesson_plans lpn on lpn.plan_id = pv.plan_id
    join lesson_periods lp on lp.id = lpn.lesson_period_id
    where pv.version_id = :version_id
    """
)


class ClassTestMaterialRecord(Protocol):
    """The part of a class test's material record the generator writes to."""

    artefact_id: str
    artefact_refs: JsonObject | None


class ClassTestMaterialRecords(Protocol):
    """Keeps the class test's material record in step with its questions."""

    async def ensure(
        self, db: AsyncSession, *, plan_version_id: str, source: str
    ) -> ClassTestMaterialRecord: ...


class ApprovedLessonNotes(Protocol):
    """The lesson's approved note, when one exists."""

    async def text(self, db: AsyncSession, plan_version_id: str) -> str | None: ...


@dataclass(frozen=True)
class ClassTestLesson:
    """What an objective's items are written and read against."""

    taught: str
    subject: str
    grade: str
    topic: str


def _reaches(objective_text: str, items: Iterable[DiagnosticMCQItem]) -> bool:
    return reaches_scale(objective_text, ((i.stem, i.options) for i in items))


def _wanted(
    item: DiagnosticMCQItem,
    kept: dict[str, DiagnosticMCQItem],
    objective_text: str,
    item_count: int,
) -> bool:
    """A room is left for the item, or it brings the objective's set up to the size it names.

    Once the set is full, a later item replaces the last only when the set stays below the size
    the objective names and this item reaches it.
    """
    if len(kept) < item_count:
        return True
    return not _reaches(objective_text, kept.values()) and _reaches(objective_text, [item])


class DiagnosticGenerationError(Exception):
    """Raised when a diagnostic cannot be generated for a plan version."""


class DiagnosticGenerationService:
    def __init__(
        self,
        generator: DiagnosticItemGenerator | None = None,
        specifications: ContentSpecifications | None = None,
        materials: ClassTestMaterialRecords | None = None,
        reader: ItemReader | None = None,
        lesson_notes: ApprovedLessonNotes | None = None,
    ) -> None:
        self.specifications = specifications
        self.materials = materials
        self.reader = reader
        self.lesson_notes = lesson_notes
        self.generator = generator or DiagnosticItemGenerator()

    async def generate_for_plan(
        self,
        *,
        db: AsyncSession,
        plan_version_id: str,
        item_count: int = 2,
    ) -> int:
        """Generate item_count MCQ items per lesson objective and persist them.

        Idempotent per plan version: existing items for the plan are replaced.
        Returns the number of items written.

        Concurrency: the MCQ generation (slow per-objective LLM calls) runs with
        NO write transaction open; only then does a single short transaction
        replace the prior items and insert the new ones. Holding the DELETE's
        index locks across the LLM calls is what deadlocked concurrent generates
        (MySQL 1213); the short transaction + ``run_with_deadlock_retry`` closes
        that window. Deleting only after generation succeeds also means a failed
        generation leaves the previous diagnostic intact.
        """
        row = (await db.execute(SUBTOPIC_SQL, {"version_id": plan_version_id})).first()
        if row is None:
            raise DiagnosticGenerationError("plan_version_not_found")
        subtopic_id, raw_session_plan = row[0], row[1]
        if not subtopic_id:
            raise DiagnosticGenerationError("subtopic_not_resolved")
        if isinstance(raw_session_plan, str):
            raw_session_plan = json.loads(raw_session_plan)
        try:
            session_plan = SessionPlanView.model_validate(raw_session_plan)
        except ValidationError as exc:
            raise DiagnosticGenerationError("session_plan_invalid") from exc

        lesson = ClassTestLesson(
            taught=await self._taught(db, plan_version_id, session_plan),
            subject=session_plan.subject or "Mathematics",
            grade=session_plan.grade or "JSS1",
            topic=session_plan.topic or session_plan.subtopic or "",
        )
        objectives = [obj for obj in session_plan.lesson_plan_objectives if obj.lesson_objective_id]
        if not objectives:
            raise DiagnosticGenerationError("no_objectives")

        # 1) Generate every item in memory — no write transaction is held, so the
        #    slow LLM calls cannot block (or deadlock against) a concurrent generate.
        with log_context(
            kind="diagnostic",
            correlation_id=plan_version_id,
            plan_version_id=plan_version_id,
            subtopic_id=subtopic_id,
        ):
            item_payloads = await self._build_item_payloads(
                specification=await self._specification(db),
                objectives=objectives,
                subtopic_id=subtopic_id,
                plan_version_id=plan_version_id,
                lesson=lesson,
                item_count=item_count,
            )

        # 2) Replace prior items + insert new ones in ONE short transaction,
        #    retried if a concurrent generate trips an InnoDB lock conflict.
        async def _persist() -> int:
            await db.execute(
                delete(ExitTicketItem).where(ExitTicketItem.plan_version_id == plan_version_id)
            )
            db.add_all([ExitTicketItem(**payload) for payload in item_payloads])
            if self.materials is not None:
                await self.materials.ensure(db, plan_version_id=plan_version_id, source="generated")
            await db.commit()
            return len(item_payloads)

        return await run_with_deadlock_retry(db, _persist)

    async def _specification(self, db: AsyncSession) -> ContentSpecification:
        """The class test's current stored specification; the seed when none is wired."""
        if self.specifications is None:
            return seed_specification(ArtefactType.DIAGNOSTIC.value)
        return await self.specifications.current(db, ArtefactType.DIAGNOSTIC.value)

    async def _taught(
        self, db: AsyncSession, plan_version_id: str, session_plan: SessionPlanView
    ) -> str:
        """The approved lesson note, or the plan's steps while the note is not approved."""
        note = await self.lesson_notes.text(db, plan_version_id) if self.lesson_notes else None
        if note:
            return note
        steps = [step.model_dump(mode="json", exclude_none=True) for step in session_plan.steps]
        return json.dumps(steps, ensure_ascii=False)

    async def _reads_as_keyed(
        self, item: DiagnosticMCQItem, *, lesson: ClassTestLesson, objective_text: str
    ) -> bool:
        """True when a second reader, without the key, finds only the keyed option right."""
        if self.reader is None:
            return True
        read = await self.reader.correct_options(
            ItemToRead(
                lesson=lesson.taught,
                objective_text=objective_text,
                subject=lesson.subject,
                grade=lesson.grade,
                stem=item.stem,
                options=item.options,
            )
        )
        if reads_as_keyed(read, item.correct_option):
            return True
        logger.info(
            "class-test item dropped: keyed %s, a second reader found %s correct: %s",
            item.correct_option,
            sorted(read),
            item.stem,
        )
        return False

    async def _sound_items(
        self,
        *,
        brief: ArtefactSpec,
        objective_text: str,
        lesson: ClassTestLesson,
        item_count: int,
    ) -> list[DiagnosticMCQItem]:
        """An objective's gradable items, drawing afresh while a draw leaves too few.

        An item is gradable when its options can be told apart, one of them is the key, and
        a second reader finds that option, and no other, right by the lesson.
        """
        kept: dict[str, DiagnosticMCQItem] = {}
        for draw in range(_DRAWS):
            items = await self.generator.generate(
                brief=brief,
                objective_text=objective_text,
                subject=lesson.subject,
                grade=lesson.grade,
                topic=lesson.topic,
                item_count=item_count,
                draw=draw,
            )
            for item in items:
                stem = item.stem.strip()
                if stem in kept or not _wanted(item, kept, objective_text, item_count):
                    continue
                if (
                    is_sound(item.options, item.correct_option)
                    and says_what_it_asks(item.stem, item.options)
                    and await self._reads_as_keyed(
                        item, lesson=lesson, objective_text=objective_text
                    )
                ):
                    if len(kept) >= item_count:
                        kept.popitem()
                    kept[stem] = item
            if len(kept) >= item_count and _reaches(objective_text, kept.values()):
                break
        return list(kept.values())

    async def _build_item_payloads(
        self,
        *,
        specification: ContentSpecification,
        objectives: list[LessonPlanObjectiveView],
        subtopic_id: str,
        plan_version_id: str,
        lesson: ClassTestLesson,
        item_count: int,
    ) -> list[dict[str, object]]:
        """Generate the MCQ items (LLM) and return them as insert payloads.

        Pure generation — no DB writes — so the caller can run it outside any
        write transaction and persist the result in one short, lock-safe commit.
        """
        brief = specification.brief(reader_for(lesson.grade))
        payloads: list[dict[str, object]] = []
        for objective in objectives:
            with log_context(lesson_objective_id=objective.lesson_objective_id):
                items = await self._sound_items(
                    brief=brief,
                    objective_text=objective.objective_text or "",
                    lesson=lesson,
                    item_count=item_count,
                )
            if not items:
                raise DiagnosticGenerationError("objective_has_no_gradable_items")
            payloads += [
                exit_ticket_payload(
                    item,
                    subtopic_id=subtopic_id,
                    plan_version_id=plan_version_id,
                    lesson_objective_id=objective.lesson_objective_id,
                )
                for item in items
            ]
        return payloads
