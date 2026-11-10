"""A writer on native skills starts with the first skill its type pins."""

from __future__ import annotations

from app.domains.content_engine.infrastructure.harness.brief import (
    NATIVE_SKILLS_WRITER_PROMPT,
    WRITER_PROMPT,
    entry_skill,
    writer_message,
)
from app.shared.json_types import JsonObject

_DRAFT: JsonObject = {
    "draft_id": "CDR-1",
    "brief": {"artefact": "a note"},
    "part_schemas": {},
    "units": [],
    "pinned_skills": [
        {"skill": "writing-lesson-notes", "revision": 1},
        {"skill": "other-skill", "revision": 2},
    ],
}


def test_the_entry_skill_is_the_first_pinned_and_none_when_nothing_is_pinned() -> None:
    assert entry_skill(_DRAFT) == "writing-lesson-notes"
    assert entry_skill({**_DRAFT, "pinned_skills": []}) is None
    assert entry_skill({k: v for k, v in _DRAFT.items() if k != "pinned_skills"}) is None


def test_the_message_names_the_entry_skill_only_when_given_one() -> None:
    named = writer_message(_DRAFT, {}, "", entry="writing-lesson-notes")
    plain = writer_message(_DRAFT, {}, "")

    assert named.startswith(
        "## draft_id\nCDR-1\n\n## entry_skill\nwriting-lesson-notes\n\n## brief"
    )
    assert "entry_skill" not in plain


def test_only_the_native_prompt_sends_the_writer_to_its_entry_skill() -> None:
    assert "entry_skill" in NATIVE_SKILLS_WRITER_PROMPT
    assert "entry_skill" not in WRITER_PROMPT


def test_a_draft_that_revises_content_gives_the_writer_the_parts_it_holds() -> None:
    revising = {**_DRAFT, "parts": {"lesson": {"intro": {"title": "Recall"}}}}

    assert '## parts\n{"lesson": {"intro": {"title": "Recall"}}}' in writer_message(
        revising, {}, ""
    )
    assert "## parts" not in writer_message({**_DRAFT, "parts": {}}, {}, "")
    assert "## parts" not in writer_message(_DRAFT, {}, "")
