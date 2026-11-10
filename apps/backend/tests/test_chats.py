"""Several chats on one piece of content: started, listed, written to, and what each one hears."""

from __future__ import annotations

import asyncio
from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefact_revision.application.chat_feed import ChatFeed
from app.domains.artefact_revision.application.errors import ArtefactRevisionError
from app.domains.artefact_revision.application.executor import RevisionExecutionOutcome
from app.domains.artefact_revision.application.service import ArtefactRevisionService, ChatRecord
from app.domains.artefact_revision.models.revision import RevisionThread, RevisionTurn
from app.domains.artefacts.core.infrastructure.models import Artefact
from app.domains.content.api import chat_routes
from app.domains.content.application.generation import GenerationChoices
from app.domains.content.domain.types import Level
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content_engine.application.comments import Comment
from app.domains.content_engine.domain.turn import TurnStoppedError
from app.domains.content_engine.infrastructure.content import SqlAlchemyEngineContent
from app.domains.content_engine.infrastructure.engine import Engine, Request
from app.domains.content_engine.infrastructure.generator import EngineGenerator
from app.domains.content_engine.infrastructure.live import LiveConversations
from app.domains.content_engine.infrastructure.revision import EngineRevisionExecutor
from app.shared.json_types import JsonObject
from tests.chat_support import feed_over
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
from tests.test_content_engine_http import http  # noqa: F401

pytestmark = pytest.mark.asyncio

KIND = "worked_examples"


class _Noop:
    artefact_type = "engine"

    async def revise(self, **_: object) -> RevisionExecutionOutcome:
        raise AssertionError("no turn is taken here")

    async def current_artefact(self, **_: object) -> tuple[str | None, JsonObject | None]:
        return None, None


def _service() -> ArtefactRevisionService:
    return ArtefactRevisionService((), fallback=_Noop())


async def _content(db: AsyncSession, *, seeded: bool = False) -> str:
    if not seeded:
        await seed_lesson(db)
    writer = ScriptedWriter({"s1": [part("A")], "s2": [part("B")]})
    built = await engine_over(db, writer).build(Request(type=TYPE, plan_version_id=PLAN))
    return built.saved_as


async def _db_id(db: AsyncSession, chat: ChatRecord):  # type: ignore[no-untyped-def]
    return await db.scalar(
        select(RevisionThread.id).where(RevisionThread.revision_thread_id == chat.chat_id)
    )


async def _chat(db: AsyncSession, content_id: str, **fields: object) -> ChatRecord:
    return await _service().create_chat(
        db=db,
        artefact_type=KIND,
        subject_id=content_id,
        created_by="T",
        title="t",
        **fields,  # type: ignore[arg-type]
    )


# --- the service ---------------------------------------------------------------------------


async def test_the_first_chat_is_the_contents_own_and_each_later_one_takes_the_next_slot(
    db: AsyncSession,
) -> None:
    content_id = await _content(db)

    first, second = await _chat(db, content_id), await _chat(db, content_id)
    own = await _service().get_or_create_thread(
        db=db, artefact_type=KIND, subject_id=content_id, created_by="T"
    )

    assert (first.slot, second.slot) == (0, 1)
    assert own.revision_thread_id == first.chat_id
    assert first.agent_key and second.agent_key and first.agent_key != second.agent_key


async def test_a_chat_is_found_only_on_the_content_it_belongs_to(db: AsyncSession) -> None:
    content_id = await _content(db)
    chat = await _chat(db, content_id)

    found = await _service().chat_of(
        db=db, artefact_type=KIND, subject_id=content_id, chat_id=chat.chat_id
    )
    with pytest.raises(ArtefactRevisionError) as refused:
        await _service().chat_of(
            db=db, artefact_type=KIND, subject_id="C-OTHER", chat_id=chat.chat_id
        )

    assert found.chat_id == chat.chat_id
    assert refused.value.status_code == 404


async def test_the_history_of_content_spans_its_chats_in_the_order_the_turns_came(
    db: AsyncSession,
) -> None:
    content_id = await _content(db)
    one, two = await _chat(db, content_id), await _chat(db, content_id)
    for number, (thread, text, turn_number, at) in enumerate(
        (
            (two, "second chat, first", 1, datetime(2026, 10, 1, 9, 0, 0)),
            (one, "first chat", 1, datetime(2026, 10, 1, 9, 0, 1)),
            (two, "second chat", 2, datetime(2026, 10, 1, 9, 0, 2)),
        )
    ):
        db.add(
            RevisionTurn(
                revision_turn_id=f"RTN-history-{number}",
                thread_db_id=await _db_id(db, thread),
                turn_number=turn_number,
                instruction=text,
                created_at=at,
            )
        )
    await db.flush()

    history = await _service().history(db=db, artefact_type=KIND, subject_id=content_id)

    assert [(h.turn_number, h.instruction) for h in history] == [
        (1, "second chat, first"),
        (2, "first chat"),
        (3, "second chat"),
    ]


# --- what a turn reports to its chat -------------------------------------------------------


def _executor(
    db: AsyncSession, writer: Messages, feed: ChatFeed, live: LiveConversations
) -> EngineRevisionExecutor:
    engine = Engine(lambda: server_over(db), lambda: writer)
    return EngineRevisionExecutor(
        engine, SqlAlchemyEngineContent(), build_content_catalogue(), live, feed
    )


async def _turn(
    executor: EngineRevisionExecutor, db: AsyncSession, content_id: str, chat: ChatRecord
) -> None:
    await executor.revise(
        db=db,
        subject_id=content_id,
        thread_id=chat.chat_id,
        instruction="Simpler.",
        highlight={"selected_text": "3/4"},
        conversation_summary="",
    )


async def test_a_turn_tells_its_chat_what_was_asked_what_was_done_and_to_show_the_content(
    db: AsyncSession,
) -> None:
    content_id = await _content(db)
    chat = await _chat(db, content_id)
    feed, live = feed_over(db), LiveConversations()
    writer = Kept([("s2", "B, simpler")])

    await _turn(_executor(db, writer, feed, live), db, content_id, chat)
    await live.close_all()

    events = await feed.since(chat.chat_id, 0)
    assert [e.kind for e in events] == ["user_message", "turn_done", "view"]
    assert events[0].data == {"text": "Simpler.", "highlight": {"selected_text": "3/4"}}
    assert events[1].data["changed"] is True and events[1].data["version"] == 2
    assert events[2].data == {"tool": "show_content", "input": {"content_id": content_id}}
    assert writer.keys == [chat.agent_key]


async def test_a_turn_that_changes_nothing_says_so_and_shows_no_content(db: AsyncSession) -> None:
    content_id = await _content(db)
    chat = await _chat(db, content_id)
    feed, live = feed_over(db), LiveConversations()

    await _turn(_executor(db, Kept([("s2", "B")]), feed, live), db, content_id, chat)
    await live.close_all()

    events = await feed.since(chat.chat_id, 0)
    assert [e.kind for e in events] == ["user_message", "turn_done"]
    assert events[1].data["changed"] is False


async def test_a_turn_that_fails_tells_its_chat_and_still_fails(db: AsyncSession) -> None:
    content_id = await _content(db)
    chat = await _chat(db, content_id)
    feed, live = feed_over(db), LiveConversations()

    class _Stops(Messages):
        async def write(self, *_: object, **__: object) -> str:
            raise ConnectionError("the agent went away")

    with pytest.raises(ConnectionError, match="went away"):
        await _turn(_executor(db, _Stops([]), feed, live), db, content_id, chat)
    await live.close_all()

    events = await feed.since(chat.chat_id, 0)
    assert [e.kind for e in events] == ["user_message", "turn_failed"]
    assert "went away" in events[1].data["error"]  # type: ignore[operator]


# --- the first chat is the creation ----------------------------------------------------------


async def test_the_content_an_agent_makes_keeps_that_agent_and_its_work_as_its_first_chat(
    db: AsyncSession,
) -> None:
    await seed_lesson(db)
    feed = feed_over(db)
    writer = ScriptedWriter({"s1": [part("A")], "s2": [part("B")]})
    service = _service()

    async def open_chat(session: AsyncSession, content_id: str, key: str) -> str:
        stored = await SqlAlchemyEngineContent().get(session, content_id)
        assert stored is not None
        chat = await service.open_creation_chat(
            db=session,
            artefact_type=stored.kind,
            subject_id=content_id,
            created_by=None,
            agent_key=key,
        )
        return chat.chat_id

    generator = EngineGenerator(engine_over(db, writer), feed, open_chat)
    content_id = await generator.generate(
        db,
        plan_version_id=PLAN,
        type=TYPE,
        level=Level.CLASS,
        choices=GenerationChoices(instructions="Two short steps."),
    )

    chats = await service.chats(db=db, artefact_type=KIND, subject_id=content_id)
    assert [(c.slot, c.title) for c in chats] == [(0, "Creation")]
    assert (chats[0].agent_key or "").startswith("new-")
    events = await feed.since(chats[0].chat_id, 0)
    assert [e.kind for e in events] == ["user_message", "turn_done", "view"]
    assert events[0].data == {"text": "Two short steps."}


# --- over HTTP -------------------------------------------------------------------------------


async def test_chats_are_listed_started_and_written_to_over_http(
    http: tuple[AsyncClient, list[object]],  # noqa: F811
    db: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client, _ = http
    content_id = await _content(db, seeded=True)
    taken: list[tuple[str, Comment, str | None]] = []

    class _Desk:
        def take(self, content: str, comment: Comment, chat: str | None = None) -> int:
            taken.append((content, comment, chat))
            return len(taken)

        def standing(self, content: str, chat: str | None = None) -> JsonObject:
            return {"working": chat is None}

    monkeypatch.setattr(chat_routes, "COMMENT_DESK", _Desk())

    empty = await client.get(f"/content/{content_id}/chats")
    first = await client.post(f"/content/{content_id}/chats", json={})
    second = await client.post(f"/content/{content_id}/chats", json={"title": "Shorter"})
    listed = await client.get(f"/content/{content_id}/chats")
    to_first = await client.post(
        f"/content/{content_id}/chats/{first.json()['chat_id']}/messages",
        json={"text": " Simpler. ", "selected_text": "3/4"},
    )
    to_second = await client.post(
        f"/content/{content_id}/chats/{second.json()['chat_id']}/messages",
        json={"text": "Shorter."},
    )
    unknown = await client.post(
        f"/content/{content_id}/chats/RVT-nope/messages", json={"text": "Hello."}
    )

    assert empty.json() == []
    assert [(c["slot"], c["title"]) for c in listed.json()] == [(0, None), (1, "Shorter")]
    assert [c["working"] for c in listed.json()] == [True, False]
    assert (to_first.status_code, to_first.json()) == (202, {"waiting": 1})
    assert taken[0][2] is None and taken[1][2] == second.json()["chat_id"]
    assert taken[0][1].text == "Simpler." and taken[0][1].highlight == {"selected_text": "3/4"}
    assert to_second.status_code == 202 and unknown.status_code == 404


async def test_a_turn_stopped_tells_its_chat_so_and_saves_nothing(db: AsyncSession) -> None:
    content_id = await _content(db)
    chat = await _chat(db, content_id)
    feed, live = feed_over(db), LiveConversations()
    asked: list[str] = []

    class _Slow(Kept):
        async def write(self, *_: object, **__: object) -> str:
            await asyncio.sleep(5)
            return "late"

        async def stop(self) -> None:
            asked.append("stop")

    executor = _executor(db, _Slow([("s2", "B, simpler")]), feed, live)
    turn = asyncio.create_task(_turn(executor, db, content_id, chat))
    await asyncio.sleep(0.3)

    stopped = await live.stop(chat.chat_id)
    with pytest.raises(TurnStoppedError):
        await turn
    await live.close_all()

    events = await feed.since(chat.chat_id, 0)
    assert [e.kind for e in events] == ["user_message", "turn_stopped"]
    assert stopped is True and asked == ["stop"]
    version = await db.scalar(select(Artefact.version).where(Artefact.artefact_id == content_id))
    assert version == 1


async def test_a_chat_is_stopped_over_http_and_its_waiting_messages_dropped(
    http: tuple[AsyncClient, list[object]],  # noqa: F811
    db: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client, _ = http
    content_id = await _content(db, seeded=True)
    chat = (await client.post(f"/content/{content_id}/chats", json={})).json()
    stopped: list[str] = []

    class _Desk:
        def drop_waiting(self, content: str, chat: str | None = None) -> int:
            return 2

    class _Live:
        async def stop(self, key: str) -> bool:
            stopped.append(key)
            return True

    monkeypatch.setattr(chat_routes, "COMMENT_DESK", _Desk())
    monkeypatch.setattr(chat_routes, "LIVE_CONVERSATIONS", _Live())

    answer = await client.post(f"/content/{content_id}/chats/{chat['chat_id']}/stop")
    unknown = await client.post(f"/content/{content_id}/chats/RVT-nope/stop")

    assert answer.json() == {"stopped": True, "dropped": 2}
    assert stopped == [chat["chat_id"]] and unknown.status_code == 404
