"""A plugin that implements the class test writes the questions grading reads."""

from __future__ import annotations

import shutil
import uuid
from pathlib import Path

import pytest
from sqlalchemy import select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.infrastructure.models.plans import (
    LessonPlan,
    PlanVersion,
)
from app.domains.assessments.application.item_reader import ItemToRead
from app.domains.assessments.models.student_item_response import StudentItemResponse
from app.domains.content.application.errors import ContentError
from app.domains.content.application.generation import GenerationChoices
from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.domain.types import BuiltIn, Level
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content.infrastructure.records import SqlAlchemyContentRecords
from app.domains.content.infrastructure.wiring import build_content_service
from app.domains.content.plugins.reader import folder_digest
from app.domains.content_engine.infrastructure import class_test_reading, wiring
from app.domains.content_engine.infrastructure.engine import (
    EngineIncompleteError,
    Request,
)
from app.domains.curriculum.models.exit_tickets import ExitTicketItem
from app.domains.teaching.models.syllabus import LessonPeriod
from tests.content_engine_support import (
    PLAN,
    SESSION_PLAN,
    ScriptedWriter,
    engine_over,
    seed_lesson,
)
from tests.plugin_folder import read_plugin, rewrite_artefact

WRITER = Path(__file__).parents[3] / "plugins" / "class-test"
TEST = BuiltIn.CLASS_TEST.value


@pytest.fixture(autouse=True)
def _no_reads_kept() -> None:
    class_test_reading._READ.clear()


def _question(stem: str, correct: str = "A") -> dict[str, object]:
    wrong = [letter for letter in "ABCD" if letter != correct]
    return {
        "stem": stem,
        "options": {"a": "3/4", "b": "3/8", "c": "1/4", "d": "2/4"},
        "correct_option": correct,
        "distractors": [
            {"option": letter, "misconception_code": f"error_{letter.lower()}"} for letter in wrong
        ],
        "difficulty": "easy",
    }


class _Reader:
    def __init__(self, answer: set[str]) -> None:
        self.answer = answer
        self.seen: list[ItemToRead] = []

    async def correct_options(self, item: ItemToRead) -> set[str]:
        self.seen.append(item)
        return self.answer


async def _installed(db: AsyncSession, monkeypatch: pytest.MonkeyPatch, reader: _Reader) -> None:
    monkeypatch.setattr(wiring, "DspyItemReader", lambda: reader)
    await seed_lesson(db)
    period = uuid.uuid4()
    db.add_all(
        [
            LessonPeriod(
                id=period, scheme_of_work_id=uuid.uuid4(), period_number=1, subtopic_id="sub-1"
            ),
            LessonPlan(
                plan_id="P-ENGINE-1",
                lesson_period_id=period,
                title="Adding fractions",
                subject="Mathematics",
                track="General",
                grade="JSS1",
            ),
        ]
    )
    await db.flush()
    plugin, problems = read_plugin(WRITER, "class-test-writer")
    assert plugin is not None, problems
    catalogue = build_content_catalogue()
    await PluginInstaller(catalogue, SqlAlchemyPlugins()).install(
        db, plugin, folder_digest(WRITER), "Researcher"
    )
    await catalogue.make_default(db, TEST, Level.CLASS, "class-test-writer", "Researcher")


@pytest.mark.asyncio
async def test_the_questions_are_stored_as_the_rows_grading_reads(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    reader = _Reader({"A"})
    await _installed(db, monkeypatch, reader)
    writer = ScriptedWriter(
        {
            "lop01": [
                {"questions": [_question("What is 1/4 + 2/4?"), _question("What is 1/8 + 2/8?")]}
            ]
        }
    )

    built = await engine_over(db, writer).build(Request(type=TEST, plan_version_id=PLAN))

    rows = (
        (await db.execute(select(ExitTicketItem).where(ExitTicketItem.plan_version_id == PLAN)))
        .scalars()
        .all()
    )
    assert sorted(row.stem for row in rows) == ["What is 1/4 + 2/4?", "What is 1/8 + 2/8?"]
    first = rows[0]
    assert first.lesson_objective_id == "lop01" and first.subtopic_id == "sub-1"
    assert sorted(first.options) == ["A", "B", "C", "D"]
    assert sorted(first.option_misconceptions or {}) == sorted(
        letter for letter in "ABCD" if letter != first.correct_option
    )
    assert len(reader.seen) == 2 and reader.seen[0].objective_text.startswith("Add fractions")
    record = await SqlAlchemyContentRecords().get(db, built.saved_as)
    assert record is not None and (record.type, record.kind) == (TEST, "diagnostic")
    assert record.provenance["generator"] == {
        "harness": "engine",
        "schema": "spec",
        "ref": "class-test-writer",
        "spec_revision": 2,
    }
    assert record.review is not None
    assert [c["check"] for c in record.review["checks"]] == [
        "question_shape",
        "distinct_stems",
        "scale_reached",
        "second_reading",
    ]


class _RewritingWriter:
    """Writes a part, and rewrites it with the next one each time it is told what is wrong."""

    def __init__(self, *attempts: dict[str, object]) -> None:
        self.attempts = list(attempts)
        self.told: list[str] = []

    async def write(self, client, draft, lesson, *, feedback: str) -> str:  # type: ignore[no-untyped-def]
        written = draft.get("parts") if isinstance(draft.get("parts"), dict) else {}
        tool = "revise_part" if "lop01" in written else "add_part"
        self.told.append(feedback)
        part = self.attempts.pop(0) if self.attempts else {}
        result = await client.call_tool(
            tool, {"draft_id": draft["draft_id"], "unit_id": "lop01", "part": part}
        )
        assert not result.is_error, result.content
        return "Wrote the questions."


@pytest.mark.asyncio
async def test_the_agent_is_told_a_second_reader_doubts_a_key_and_rewrites_the_question(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    class _ByStem(_Reader):
        async def correct_options(self, item: ItemToRead) -> set[str]:
            self.seen.append(item)
            return {"A", "B"} if "1/4" in item.stem else {"A"}

    reader = _ByStem(set())
    await _installed(db, monkeypatch, reader)
    doubtful = {"questions": [_question("What is 1/4 + 2/4?"), _question("What is 1/8 + 2/8?")]}
    fixed = {
        "questions": [
            _question("What is 3/8 + 2/8?"),
            _question("What is 1/8 + 2/8?"),
        ]
    }
    writer = _RewritingWriter(doubtful, fixed)

    built = await engine_over(db, writer).build(Request(type=TEST, plan_version_id=PLAN))  # type: ignore[arg-type]

    assert any("a second reader found A, B right" in told for told in writer.told)
    rows = (
        (await db.execute(select(ExitTicketItem).where(ExitTicketItem.plan_version_id == PLAN)))
        .scalars()
        .all()
    )
    assert sorted(row.stem for row in rows) == ["What is 1/8 + 2/8?", "What is 3/8 + 2/8?"]
    assert built.saved_as


@pytest.mark.asyncio
async def test_a_question_the_agent_leaves_doubtful_stops_the_run_with_the_reason(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    await _installed(db, monkeypatch, _Reader({"A", "B"}))
    writer = ScriptedWriter(
        {
            "lop01": [
                {"questions": [_question("What is 1/4 + 2/4?"), _question("What is 1/8 + 2/8?")]}
            ]
        }
    )

    with pytest.raises(EngineIncompleteError, match="a second reader found A, B right"):
        await engine_over(db, writer).build(Request(type=TEST, plan_version_id=PLAN))

    rows = (
        (await db.execute(select(ExitTicketItem).where(ExitTicketItem.plan_version_id == PLAN)))
        .scalars()
        .all()
    )
    assert rows == []


@pytest.mark.asyncio
async def test_a_plugin_that_lists_no_second_reading_is_not_read_and_does_not_claim_it(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    folder = tmp_path / "class-test"
    shutil.copytree(WRITER, folder)
    rewrite_artefact(
        folder,
        lambda a: a["checks"]["lpcg"].remove("class_test_second_reading"),
        "class-test-writer",
    )
    monkeypatch.setitem(_installed.__globals__, "WRITER", folder)
    reader = _Reader({"A", "B"})
    await _installed(db, monkeypatch, reader)
    writer = ScriptedWriter(
        {
            "lop01": [
                {"questions": [_question("What is 1/4 + 2/4?"), _question("What is 1/8 + 2/8?")]}
            ]
        }
    )

    built = await engine_over(db, writer).build(Request(type=TEST, plan_version_id=PLAN))

    record = await SqlAlchemyContentRecords().get(db, built.saved_as)
    assert reader.seen == []
    assert record is not None and record.review is not None
    assert "second_reading" not in [c["check"] for c in record.review["checks"]]


@pytest.mark.asyncio
async def test_a_question_without_a_code_for_each_wrong_option_is_sent_back(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    await _installed(db, monkeypatch, _Reader({"A"}))
    broken = _question("What is 1/4 + 2/4?")
    broken["distractors"] = broken["distractors"][:2]  # type: ignore[index]
    writer = ScriptedWriter({"lop01": [{"questions": [broken, _question("What is 1/8 + 2/8?")]}]})

    with pytest.raises(EngineIncompleteError):
        await engine_over(db, writer).build(Request(type=TEST, plan_version_id=PLAN))


@pytest.mark.asyncio
async def test_a_generator_may_not_change_the_question_fields(
    db: AsyncSession, tmp_path: Path
) -> None:
    await seed_lesson(db)
    folder = tmp_path / "other"
    shutil.copytree(WRITER, folder)
    rewrite_artefact(
        folder,
        lambda a: (a["spec"]["parts"][0]["fields"].pop(), a.update(name="other-writer")),
        "class-test-writer",
    )
    plugin, problems = read_plugin(folder, "other-writer")
    assert plugin is not None, problems

    with pytest.raises(ContentError) as changed:
        await PluginInstaller(build_content_catalogue(), SqlAlchemyPlugins()).install(
            db, plugin, folder_digest(folder), "Researcher"
        )
    assert "keeps the question fields grading reads" in changed.value.detail


@pytest.mark.asyncio
async def test_an_objective_that_names_a_size_is_not_tested_below_it(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    await _installed(db, monkeypatch, _Reader({"A"}))
    await db.execute(
        update(PlanVersion)
        .where(PlanVersion.version_id == PLAN)
        .values(
            session_plan={
                **SESSION_PLAN,
                "lesson_plan_objectives": [
                    {
                        "lesson_objective_id": "lop01",
                        "objective_text": "Compare numbers in billions and trillions",
                    }
                ],
            }
        )
    )
    writer = ScriptedWriter(
        {
            "lop01": [
                {"questions": [_question("What is 1/4 + 2/4?"), _question("What is 1/8 + 2/8?")]}
            ]
        }
    )

    with pytest.raises(EngineIncompleteError, match="the objective names numbers as large as"):
        await engine_over(db, writer).build(Request(type=TEST, plan_version_id=PLAN))


@pytest.mark.asyncio
async def test_options_keyed_in_capitals_are_accepted_and_stored(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    await _installed(db, monkeypatch, _Reader({"A"}))

    def capitals(question: dict[str, object]) -> dict[str, object]:
        options = question["options"]
        assert isinstance(options, dict)
        return {**question, "options": {letter.upper(): text for letter, text in options.items()}}

    writer = ScriptedWriter(
        {
            "lop01": [
                {
                    "questions": [
                        capitals(_question("What is 1/4 + 2/4?")),
                        capitals(_question("What is 1/8 + 2/8?")),
                    ]
                }
            ]
        }
    )

    await engine_over(db, writer).build(Request(type=TEST, plan_version_id=PLAN))

    assert writer.refusals == []
    rows = (
        (await db.execute(select(ExitTicketItem).where(ExitTicketItem.plan_version_id == PLAN)))
        .scalars()
        .all()
    )
    assert len(rows) == 2 and sorted(rows[0].options) == ["A", "B", "C", "D"]


@pytest.mark.asyncio
async def test_a_class_test_students_have_answered_is_not_generated_again(
    db: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    await _installed(db, monkeypatch, _Reader({"A"}))
    writer = ScriptedWriter(
        {
            "lop01": [
                {"questions": [_question("What is 1/4 + 2/4?"), _question("What is 1/8 + 2/8?")]}
            ]
        }
    )
    await engine_over(db, writer).build(Request(type=TEST, plan_version_id=PLAN))
    item = (
        (await db.execute(select(ExitTicketItem).where(ExitTicketItem.plan_version_id == PLAN)))
        .scalars()
        .first()
    )
    assert item is not None
    await db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.add(
        StudentItemResponse(
            item_id=item.id, student_id="ST-X", choice="A", is_correct=True, score=1.0
        )
    )
    await db.commit()

    with pytest.raises(ContentError) as refused:
        await build_content_service().check_generation(
            db,
            plan_version_id=PLAN,
            type=TEST,
            level=Level.CLASS,
            choices=GenerationChoices(),
        )

    assert (refused.value.status_code, refused.value.detail) == (
        409,
        "class_test_has_student_answers",
    )
