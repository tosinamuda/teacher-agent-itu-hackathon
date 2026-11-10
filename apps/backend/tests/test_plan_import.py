"""Writing a lesson plan from a teacher's document with the same draft tools as any content.

The plan is drafted one curriculum objective at a time, with a part for the whole lesson, and
saved through the real checks. Only the lesson's lookup and the plan's saving are in memory.
"""

from __future__ import annotations

import copy
import io
import json

import pytest
from dspy.utils import DummyLM
from mcp import Client
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.artefacts.types.lesson_plan.application.manual_check import check_manual_plan
from app.domains.artefacts.types.lesson_plan.domain.plan_sections import (
    ObjectiveSection,
    assemble_plan,
    issue_lines,
)
from app.domains.content_engine.infrastructure.documents import (
    DocumentUnreadableError,
    document_text,
)
from app.domains.content_engine.infrastructure.engine import (
    Engine,
    EngineIncompleteError,
    EngineRefusedError,
    Request,
    Writer,
)
from app.domains.content_engine.infrastructure.writer import EngineWriter, text_of
from app.shared.json_types import JsonObject
from tests.plan_import_support import (
    CONTEXT,
    DOCUMENT,
    LESSON,
    PLAN_TYPE,
    SECTIONS,
    InMemoryPlanning,
    plan_server,
    seed_types,
)

pytestmark = pytest.mark.asyncio
OBJECTIVE = "cur_obj01"
OBJECTIVE_TEXT = "add fractions with a common denominator"


def _plan(sections: dict[str, JsonObject]) -> JsonObject:
    objective = ObjectiveSection(OBJECTIVE, OBJECTIVE_TEXT, sections[OBJECTIVE])
    return assemble_plan(sections["lesson"], [objective]).content


def _as_concept() -> dict[str, JsonObject]:
    """The fixture's objective taught as a concept, which a worked example contradicts."""
    sections = copy.deepcopy(SECTIONS)
    objectives = sections[OBJECTIVE]["lesson_objectives"]
    assert isinstance(objectives, list) and isinstance(objectives[0], dict)
    objectives[0]["kc_type"] = "concept"
    return sections


def _engine(db: AsyncSession, planning: InMemoryPlanning, writer: Writer) -> Engine:
    return Engine(lambda: plan_server(db, planning), lambda: writer)


def _request(**lesson: str) -> Request:
    return Request(PLAN_TYPE, **(lesson or {"session_id": LESSON}), source=DOCUMENT)


class _SectionWriter:
    """Writes the plan's parts as a model would, then revises the ones a check refused.

    It writes on its first run only, so when the engine resumes it nothing changes.
    """

    def __init__(self, first: dict[str, JsonObject], fixes: dict[str, JsonObject]) -> None:
        self.first, self.fixes = first, fixes
        self.draft: JsonObject = {}
        self.lesson: JsonObject = {}
        self.results: list[JsonObject] = []

    async def write(
        self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
    ) -> str:
        if self.draft:
            return "Nothing more to write."
        self.draft, self.lesson = draft, lesson
        for tool, parts in (("add_part", self.first), ("revise_part", self.fixes)):
            for unit_id, part in parts.items():
                result = await client.call_tool(
                    tool, {"draft_id": draft["draft_id"], "unit_id": unit_id, "part": part}
                )
                self.results.append(json.loads(text_of(result)))
        return "Wrote the plan from the document."


async def test_the_sections_make_a_plan_the_checks_pass() -> None:
    plan = _plan(SECTIONS)

    assert check_manual_plan(CONTEXT, plan).passes
    steps = plan["steps"]
    assert isinstance(steps, list)
    assert [step["step_id"] for step in steps if isinstance(step, dict)] == [
        "intro",
        "core1",
        "evaluation",
    ]
    objectives = plan["lesson_plan_objectives"]
    assert isinstance(objectives, list) and isinstance(objectives[0], dict)
    assert objectives[0]["objective_text"] == "Add fractions that share a denominator"
    assert objectives[0]["curriculum_objective_text"] == OBJECTIVE_TEXT
    core, evaluation = steps[1], steps[2]
    assert isinstance(core, dict) and isinstance(evaluation, dict)
    assert (core["lesson_objective_id"], core["kc_type"], core["instructional_type"]) == (
        "lo1",
        "procedure",
        "explain_example_practice",
    )
    assert evaluation["blocks"] == [
        {
            "id": "evaluation-b1",
            "type": "practice",
            "question": "3/8 + 2/8",
            "answer": "5/8",
            "lesson_objective_id": "lo1",
        }
    ]


async def test_a_check_s_finding_names_the_section_and_the_place_in_it() -> None:
    concept = _as_concept()
    plan = assemble_plan(concept["lesson"], [ObjectiveSection(OBJECTIVE, "", concept[OBJECTIVE])])

    issues = check_manual_plan(CONTEXT, plan.content).issues

    assert (
        "the cur_obj01 part, at lesson_objectives.0.core_step: "
        "concept core steps must not include worked_example blocks"
    ) in issue_lines(issues, plan.places)


async def test_a_plan_is_drafted_fixed_and_saved_through_the_shared_tools(
    db: AsyncSession,
) -> None:
    await seed_types(db)
    planning = InMemoryPlanning()
    writer = _SectionWriter(_as_concept(), {OBJECTIVE: SECTIONS[OBJECTIVE]})

    built = await _engine(db, planning, writer).build(_request(), for_teacher="teacher-7")

    units = writer.draft["units"]
    assert isinstance(units, list)
    assert [unit["unit_id"] for unit in units if isinstance(unit, dict)] == ["lesson", OBJECTIVE]
    assert writer.draft["source"] == DOCUMENT.strip()
    assert writer.lesson["subtopic"] == "Addition of fractions"
    refused, fixed = writer.results[1], writer.results[2]
    assert refused["missing"] == []
    assert refused["issues"] == [
        "the cur_obj01 part, at lesson_objectives.0.core_step: "
        "concept core steps must not include worked_example blocks"
    ]
    assert fixed["issues"] == []
    assert built.saved_as == "LPV-IMPORTED-1"
    assert planning.saved == [(LESSON, _plan(SECTIONS), "teacher-7")]


async def test_a_plan_with_issues_left_is_never_saved(db: AsyncSession) -> None:
    await seed_types(db)
    planning = InMemoryPlanning()

    with pytest.raises(EngineIncompleteError, match="concept core steps"):
        await _engine(db, planning, _SectionWriter(_as_concept(), {})).build(_request())

    assert planning.saved == []


async def test_a_curriculum_objective_the_lesson_does_not_teach_takes_an_empty_list(
    db: AsyncSession,
) -> None:
    await seed_types(db)
    writer = _SectionWriter(
        {"lesson": SECTIONS["lesson"], OBJECTIVE: {"lesson_objectives": []}}, {}
    )

    with pytest.raises(EngineIncompleteError, match="curriculum objective parts, at lesson_obj"):
        await _engine(db, InMemoryPlanning(), writer).build(_request())

    assert writer.results[1]["part"] == {"lesson_objectives": []}


async def test_the_real_writer_drafts_a_plan_with_the_shared_tools(db: AsyncSession) -> None:
    """ReActV2 over the in-memory client, with only the model's replies scripted."""
    await seed_types(db)
    planning = InMemoryPlanning()

    def turn(name: str, args: JsonObject) -> JsonObject:
        return {
            "next_thought": f"Call {name}.",
            "tool_calls": {"tool_calls": [{"name": name, "args": args}]},
        }

    class _Scripted:
        async def write(
            self, client: Client, draft: JsonObject, lesson: JsonObject, *, feedback: str
        ) -> str:
            draft_id = draft["draft_id"]
            replies = [
                turn(
                    "add_part",
                    {"draft_id": draft_id, "unit_id": "lesson", "part": SECTIONS["lesson"]},
                ),
                turn(
                    "add_part",
                    {"draft_id": draft_id, "unit_id": OBJECTIVE, "part": _as_concept()[OBJECTIVE]},
                ),
                turn(
                    "revise_part",
                    {"draft_id": draft_id, "unit_id": OBJECTIVE, "part": SECTIONS[OBJECTIVE]},
                ),
                turn("submit", {"summary": "Plan written."}),
            ]
            writer = EngineWriter(DummyLM(replies))
            return await writer.write(client, draft, lesson, feedback=feedback)

    built = await _engine(db, planning, _Scripted()).build(_request())

    assert built.summary == "Plan written."
    assert planning.saved[0][1] == _plan(SECTIONS)


async def test_an_outside_client_without_an_access_code_cannot_start_a_plan(
    db: AsyncSession,
) -> None:
    await seed_types(db)
    async with Client(plan_server(db, InMemoryPlanning())) as client:
        started = await client.call_tool(
            "start_draft", {"type": PLAN_TYPE, "session_id": LESSON, "source": DOCUMENT}
        )

    assert started.is_error
    assert "Sign in" in text_of(started)


async def test_a_plan_is_made_from_its_lesson_period(db: AsyncSession) -> None:
    await seed_types(db)

    with pytest.raises(EngineRefusedError, match="give session_id"):
        await _engine(db, InMemoryPlanning(), _SectionWriter({}, {})).build(
            _request(plan_version_id="LPV-1")
        )


async def test_the_writer_is_shown_no_id_or_link_it_could_get_wrong(db: AsyncSession) -> None:
    await seed_types(db)
    writer = _SectionWriter({}, {})

    with pytest.raises(EngineIncompleteError):
        await _engine(db, InMemoryPlanning(), writer).build(_request())

    schemas = writer.draft["part_schemas"]
    assert isinstance(schemas, dict) and set(schemas) == {"lesson", "curriculum_objective"}
    shown = json.dumps(schemas)
    for linked in (
        "lesson_objective_id",
        "step_id",
        "curriculum_objective_id",
        "instructional_type",
    ):
        assert linked not in shown


async def test_a_document_s_text_is_read_from_text_word_and_pdf() -> None:
    from docx import Document

    word = Document()
    word.add_paragraph("Objective: add fractions.")
    table = word.add_table(rows=1, cols=2)
    table.rows[0].cells[0].text, table.rows[0].cells[1].text = "Starter", "5 min"
    buffer = io.BytesIO()
    word.save(buffer)

    assert document_text("plan.md", b"# Plan\nAdd fractions.") == "# Plan\nAdd fractions."
    assert (
        document_text("plan.docx", buffer.getvalue())
        == "Objective: add fractions.\nStarter | 5 min"
    )
    assert "Add fractions" in document_text("plan.pdf", _one_line_pdf("Add fractions"))
    with pytest.raises(DocumentUnreadableError, match="send one of"):
        document_text("plan.pages", b"...")
    with pytest.raises(DocumentUnreadableError, match="could not be read"):
        document_text("plan.docx", b"not a zip")


def _one_line_pdf(text: str) -> bytes:
    """A one-page PDF that shows ``text``, written by hand so the test needs no PDF writer."""
    stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = io.BytesIO(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(out.tell())
        out.write(b"%d 0 obj\n" % number + body + b"\nendobj\n")
    xref = out.tell()
    out.write(b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1))
    for offset in offsets:
        out.write(b"%010d 00000 n \n" % offset)
    out.write(
        b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, xref)
    )
    return out.getvalue()
