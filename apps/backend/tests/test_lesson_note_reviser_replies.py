"""A model reply that cannot be read is asked for again once; then the revision fails cleanly."""

from __future__ import annotations

from types import SimpleNamespace

import dspy
import pytest
from dspy.utils import DummyLM
from dspy.utils.exceptions import AdapterParseError

from app.domains.artefacts.lesson_note.application.errors import UnreadableReplyError
from app.domains.artefacts.lesson_note.domain.note import NoteSection
from app.domains.artefacts.lesson_note.infrastructure.dspy.write_note_step import (
    REVISION_REPLY_ATTEMPTS,
    DSPyLessonNoteReviser,
    ReviseLessonNote,
)

pytestmark = pytest.mark.asyncio


def _unreadable() -> AdapterParseError:
    return AdapterParseError("ChatAdapter", ReviseLessonNote, "a reply of the wrong shape")


def _section(step_id: str) -> NoteSection:
    return NoteSection(step_id=step_id, body="The note.")


class _Chain:
    """Stands in for the chain of thought: one reply, or one failure, for each call."""

    def __init__(self, *replies: object) -> None:
        self.replies = list(replies)
        self.configs: list[dict[str, int]] = []

    async def acall(self, **call: object) -> object:
        self.configs.append(call["config"])  # type: ignore[arg-type]
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply


def _reviser(chain: _Chain) -> DSPyLessonNoteReviser:
    reviser = DSPyLessonNoteReviser(lm=DummyLM([]))
    reviser._revise = chain  # the chain of thought is the model's side
    return reviser


async def _revise(reviser: DSPyLessonNoteReviser) -> tuple[list[NoteSection], str]:
    return await reviser.revise(
        brief=dspy.Example(),
        current_sections=[],
        highlighted_section="",
        instruction="Add an example.",
    )


async def test_a_reply_that_can_be_read_is_used_as_it_is() -> None:
    revised = [_section("intro01"), _section("step01")]
    chain = _Chain(SimpleNamespace(revised_sections=revised, change_summary="Added one."))

    sections, summary = await _revise(_reviser(chain))

    assert (sections, summary) == (revised, "Added one.")
    assert chain.configs == [{}]


async def test_a_reply_that_cannot_be_read_is_asked_for_again_as_a_new_draw() -> None:
    revised = [_section("intro01")]
    chain = _Chain(_unreadable(), SimpleNamespace(revised_sections=revised, change_summary="Done."))

    sections, _ = await _revise(_reviser(chain))

    assert sections == revised
    assert chain.configs == [{}, {"rollout_id": 1}]


async def test_a_reply_that_cannot_be_read_twice_fails_the_revision() -> None:
    chain = _Chain(*[_unreadable() for _ in range(REVISION_REPLY_ATTEMPTS)])

    with pytest.raises(UnreadableReplyError):
        await _revise(_reviser(chain))

    assert len(chain.configs) == REVISION_REPLY_ATTEMPTS
