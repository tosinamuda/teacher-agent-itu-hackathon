"""A revision thread's turns share one writer, so a turn continues the one before it."""

from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content_engine.infrastructure.content import SqlAlchemyEngineContent
from app.domains.content_engine.infrastructure.engine import Engine, Request
from app.domains.content_engine.infrastructure.live import LiveConversations
from app.domains.content_engine.infrastructure.revision import EngineRevisionExecutor
from app.shared.json_types import JsonObject
from tests.content_engine_support import (
    PLAN,
    TYPE,
    ScriptedWriter,
    engine_over,
    part,
    seed_lesson,
    server_over,
)
from tests.conversation_support import Kept, Messages

pytestmark = pytest.mark.asyncio

POINTED = {"unit_id": "s2", "path": "examples.0.solution", "selected_text": "3/4"}


async def _content(db: AsyncSession) -> str:
    await seed_lesson(db)
    built = await engine_over(db, ScriptedWriter({"s1": [part("A")], "s2": [part("B")]})).build(
        Request(type=TYPE, plan_version_id=PLAN)
    )
    return built.saved_as


def _executor(
    db: AsyncSession, writer: Messages, live: LiveConversations | None
) -> EngineRevisionExecutor:
    engine = Engine(lambda: server_over(db), lambda: writer)
    return EngineRevisionExecutor(
        engine, SqlAlchemyEngineContent(), build_content_catalogue(), live
    )


async def _turn(
    executor: EngineRevisionExecutor,
    db: AsyncSession,
    content_id: str,
    instruction: str,
    summary: str,
) -> str:
    outcome = await executor.revise(
        db=db,
        subject_id=content_id,
        thread_id="RT-1",
        instruction=instruction,
        highlight=POINTED,
        conversation_summary=summary,
    )
    return outcome.result_version_id


async def test_a_kept_writer_is_told_the_earlier_turns_once_and_the_pointed_at_text_each_time(
    db: AsyncSession,
) -> None:
    content_id = await _content(db)
    writer, live = Kept([("s2", "B, simpler"), ("s1", "A, clearer")]), LiveConversations()
    executor = _executor(db, writer, live)

    await _turn(executor, db, content_id, "Simpler.", "1. asked: shorter -> shortened")
    await _turn(
        executor, db, content_id, "Clearer.", "1. asked: shorter -> shortened\n2. asked: Simpler."
    )
    await live.close_all()

    first, second = writer.heard
    assert first.startswith("Simpler.")
    assert "The teacher pointed at: anchor: unit_id=s2, path=examples.0.solution" in first
    assert 'selected text: "3/4"' in first
    assert "Earlier turns of this conversation" in first
    assert "Earlier turns" not in second and "pointed at" in second
    assert writer.events == ["opened", "closed"]
    assert writer.keys == [content_id]


async def _heard_for(db: AsyncSession, highlight: JsonObject) -> str:
    content_id = await _content(db)
    writer, live = Kept([("s2", "B, simpler")]), LiveConversations()

    await _executor(db, writer, live).revise(
        db=db,
        subject_id=content_id,
        thread_id="RT-1",
        instruction="Simpler.",
        highlight=highlight,
        conversation_summary="",
    )
    await live.close_all()
    return writer.heard[0]


async def test_text_selected_with_no_place_is_found_in_the_draft_for_the_writer(
    db: AsyncSession,
) -> None:
    heard = await _heard_for(db, {"selected_text": "3/4"})

    assert 'selected text: "3/4"' in heard
    assert (
        "The selected text is in the draft at: unit_id=s1, path=examples.0.solution; "
        "unit_id=s2, path=examples.0.solution."
    ) in heard


async def test_text_that_is_in_no_part_is_said_to_be_in_none(db: AsyncSession) -> None:
    heard = await _heard_for(db, {"selected_text": "A heading the page draws"})

    assert "The selected text is in no part of the draft" in heard


async def test_a_selection_that_names_its_place_is_not_searched_for(db: AsyncSession) -> None:
    content_id = await _content(db)
    writer, live = Kept([("s2", "B, simpler")]), LiveConversations()

    await _turn(_executor(db, writer, live), db, content_id, "Simpler.", "")
    await live.close_all()

    assert "The selected text is in" not in writer.heard[0]


async def test_an_agent_resumed_from_an_earlier_conversation_is_not_told_the_turns_again(
    db: AsyncSession,
) -> None:
    content_id = await _content(db)
    writer, live = Kept([("s2", "B, simpler")], resumed=True), LiveConversations()

    await _turn(_executor(db, writer, live), db, content_id, "Simpler.", "1. asked: shorter")
    await live.close_all()

    assert "Earlier turns" not in writer.heard[0] and "pointed at" in writer.heard[0]


async def test_a_writer_that_forgets_is_told_the_earlier_turns_every_time(db: AsyncSession) -> None:
    content_id = await _content(db)
    writer, live = Messages([("s2", "B, simpler"), ("s1", "A, clearer")]), LiveConversations()
    executor = _executor(db, writer, live)

    await _turn(executor, db, content_id, "Simpler.", "1. asked: shorter -> shortened")
    await _turn(executor, db, content_id, "Clearer.", "1. asked: shorter -> shortened")
    await live.close_all()

    assert all("Earlier turns of this conversation" in heard for heard in writer.heard)


async def test_without_a_registry_each_turn_is_a_run_of_its_own(db: AsyncSession) -> None:
    content_id = await _content(db)
    writer = Messages([("s2", "B, simpler")])

    version = await _turn(_executor(db, writer, None), db, content_id, "Simpler.", "")

    assert version == content_id and "Simpler." in writer.heard[0]
