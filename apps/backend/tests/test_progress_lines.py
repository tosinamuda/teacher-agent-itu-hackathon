"""What a drafting or content-making agent reports while it works, and how a page reads it."""

from __future__ import annotations

import pytest

from app.domains.artefacts.types.lesson_plan.jobs import drafting_channel
from app.domains.content.progress import generation_channel
from app.domains.content_engine.infrastructure.progress_lines import (
    MAX_LINES,
    lines_after,
)
from app.domains.content_engine.infrastructure.progress_tap import ProgressTap
from app.domains.content_engine.infrastructure.tap import AgentChatEvent
from app.infra import progress


def _event(kind: str, text: str) -> dict[str, object]:
    return {"kind": kind, "data": {"text": text}}


def test_a_lessons_channel_is_the_same_for_both_spellings_of_its_id() -> None:
    dashed = "04F1F1F6-4EB8-4BF6-829E-D1E23587F62F"

    assert drafting_channel(dashed) == drafting_channel(dashed.replace("-", "").lower())


def test_only_the_latest_run_is_read() -> None:
    events = [
        (1, _event("start", "Started")),
        (2, _event("tool", "Wrote a part")),
        (3, _event("start", "Started")),
        (4, _event("agent_text", "Reading the records")),
    ]

    assert [event_id for event_id, _ in lines_after(events, 0)] == [3, 4]


def test_a_page_reads_on_from_the_last_line_it_has() -> None:
    events = [(1, _event("start", "Started")), (2, _event("tool", "a")), (3, _event("tool", "b"))]

    assert [event_id for event_id, _ in lines_after(events, 2)] == [3]
    assert lines_after(events, 3) == []


def test_events_with_no_run_started_are_not_read() -> None:
    assert lines_after([(1, _event("tool", "stale"))], 0) == []


def test_a_long_run_returns_its_latest_lines() -> None:
    events = [(1, _event("start", "Started"))] + [
        (n, _event("tool", str(n))) for n in range(2, MAX_LINES + 20)
    ]

    found = lines_after(events, 0)

    assert len(found) == MAX_LINES
    assert found[-1][0] == MAX_LINES + 19


@pytest.mark.asyncio
async def test_the_agents_words_and_tools_are_published_as_the_chat_keeps_them(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    published: list[tuple[str, dict[str, object]]] = []
    monkeypatch.setattr(
        progress, "publish", lambda channel, event: published.append((channel, event))
    )
    tap = ProgressTap("lesson-draft:x")

    await tap.start()
    await tap.emit(AgentChatEvent("agent_text", {"text": "Reading the records"}))
    await tap.emit(AgentChatEvent("tool", {"tool": "add_part", "unit_id": "lesson"}))
    await tap.emit(AgentChatEvent("working_on", {"tool": "add_part"}))
    await tap.emit(AgentChatEvent("turn_done", {}))

    assert [event for _, event in published] == [
        {"kind": "start", "data": {}},
        {"kind": "agent_text", "data": {"text": "Reading the records"}},
        {"kind": "tool", "data": {"tool": "add_part", "unit_id": "lesson"}},
    ]


def test_a_lesson_that_is_not_a_lesson_period_has_no_progress(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    from fastapi.testclient import TestClient

    from app.main import app
    from app.shared import authz
    from app.shared.auth import Actor, get_actor

    async def allow(*_args, **_kwargs) -> None:  # type: ignore[no-untyped-def]
        return None

    app.dependency_overrides[get_actor] = lambda: Actor(
        role="research_manager", auth_id="code|manager", full_name="Manager"
    )
    monkeypatch.setattr(authz, "enforce", allow)
    try:
        response = TestClient(app).get(
            "/artefacts/lesson-plans/drafting-progress", params={"session_id": "SS1-W01"}
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


def test_progress_is_for_signed_in_users() -> None:
    from fastapi.testclient import TestClient

    from app.main import app

    app.dependency_overrides.clear()
    response = TestClient(app).get(
        "/artefacts/lesson-plans/drafting-progress",
        params={"session_id": "00000000-0000-0000-0000-000000000902"},
    )

    assert response.status_code in (401, 403)


def test_a_contents_channel_is_the_same_for_both_spellings_of_the_plan_version_id() -> None:
    dashed = "LPV-04F1F1F6-4EB8-4BF6-829E-D1E23587F62F"

    assert generation_channel(dashed, "slide-deck") == generation_channel(
        dashed.replace("-", "").lower(), "slide-deck"
    )
    assert generation_channel(dashed, "slide-deck") != generation_channel(dashed, "class-test")


def test_content_progress_is_for_signed_in_users() -> None:
    from fastapi.testclient import TestClient

    from app.main import app

    app.dependency_overrides.clear()
    response = TestClient(app).get(
        "/content/generation-progress", params={"plan_version_id": "LPV-1", "type": "slide-deck"}
    )

    assert response.status_code in (401, 403)
