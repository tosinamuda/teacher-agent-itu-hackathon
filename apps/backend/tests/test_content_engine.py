"""The content engine end to end in process: register a type, build it and revise it
through the real MCP server, and store it as content like every other type.

Only the model is stood in for, by a writer that calls the same MCP tools a model does.
"""

from __future__ import annotations

import json

import pytest
from dspy.utils import DummyLM
from mcp import Client
from mcp.shared.exceptions import MCPError

from app.domains.content.application.errors import ContentError
from app.domains.content.application.generation import GenerationChoices
from app.domains.content.domain.types import Audience, BuiltIn, Engine, Level
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.records import SqlAlchemyContentRecords
from app.domains.content_engine.domain.draft import DraftError
from app.domains.content_engine.infrastructure.engine import (
    READ_FIRST,
    EngineIncompleteError,
    EngineRefusedError,
    Request,
)
from app.domains.content_engine.infrastructure.engine import Engine as ContentEngine
from app.domains.content_engine.infrastructure.generator import EngineGenerator
from app.domains.content_engine.infrastructure.wiring import build_drafting_service
from app.domains.content_engine.infrastructure.writer import EngineWriter, WriterStoppedError
from app.domains.content_engine.mcp.caller import as_the_app
from app.domains.content_engine.mcp.viewer import VIEWER_URI
from app.shared.tikz_svg import tikz_available
from tests.content_engine_support import (
    NOTE_S1,
    PLAN,
    SPEC,
    TYPE,
    ScriptedWriter,
    engine_over,
    part,
    seed_lesson,
    server_over,
)

pytestmark = pytest.mark.asyncio


async def test_a_registered_type_is_listed_with_its_part_schema(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)

    types = await build_content_catalogue().types(db)

    assert [t.slug for t, _ in types] == [*(b.value for b in BuiltIn), "exam-questions", TYPE]
    definition, spec = types[-1]
    assert (definition.kind, definition.engine, definition.audience) == (
        "worked_examples",
        Engine.MCP,
        Audience.LEARNER,
    )
    assert spec.unit is not None and spec.unit.value == "plan_step"
    assert spec.structure[0] == "title: A heading for the learner"


@pytest.mark.parametrize(
    ("slug", "fields", "status"),
    [
        (TYPE, SPEC, 409),
        ("lesson-note", SPEC, 409),
        ("Bad Slug", SPEC, 422),
        ("no-parts", {**SPEC, "unit": None, "parts": None, "structure": ["x"]}, 422),
        ("learner-level", {**SPEC, "levels": ["learner_level"], "adaptable": ["depth"]}, 422),
    ],
)
async def test_a_type_that_cannot_be_built_is_refused(db, slug, fields, status) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)

    with pytest.raises(ContentError) as refused:
        await build_content_catalogue().register(
            db,
            slug=slug,
            label="Anything",
            audience=Audience.LEARNER,
            made_from_a_plan_version=True,
            spec_fields=fields,
            created_by="Researcher",
        )

    assert refused.value.status_code == status


async def test_content_drafted_part_by_part_is_class_level_only(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)
    catalogue = build_content_catalogue()
    revision_note = await catalogue.current(db, BuiltIn.REVISION_NOTE.value)

    with pytest.raises(ContentError, match="class level only"):
        await catalogue.add(
            db,
            BuiltIn.REVISION_NOTE.value,
            {**revision_note.to_record(), "unit": "plan_step", "parts": SPEC["parts"]},
            "Researcher",
        )


async def test_the_app_builds_a_type_through_mcp_and_stores_it_as_pending_content(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)
    writer = ScriptedWriter(
        {"s1": [{"title": "No examples"}, part("Same bottom")], "s2": [part("Mixed")]}
    )

    built = await engine_over(db, writer).build(Request(type=TYPE, plan_version_id=PLAN))

    assert writer.refusals == [
        "Error executing tool add_part: the part does not match its schema: examples: is required. "
        "Nothing was stored: correct it and call add_part again."
    ]
    assert [unit["unit_id"] for unit in writer.seen["draft"]["units"]] == ["s1", "s2"]
    assert writer.seen["draft"]["brief"]["audience"].endswith("revising at home")
    assert [step["lesson_note"] for step in writer.seen["lesson"]["steps"]] == [NOTE_S1, ""]
    record = await SqlAlchemyContentRecords().get(db, built.saved_as)
    assert record is not None
    assert (record.type, record.kind, record.review_status, record.version) == (
        TYPE,
        "worked_examples",
        "pending",
        1,
    )
    assert record.provenance["specification"] == {"kind": "worked_examples", "revision": 1}
    assert [s["part"]["title"] for s in record.manifest["sections"]] == ["Same bottom", "Mixed"]


async def test_a_revision_reopens_the_parts_and_stores_the_next_version(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)
    first = await engine_over(db, ScriptedWriter({"s1": [part("A")], "s2": [part("B")]})).build(
        Request(type=TYPE, plan_version_id=PLAN)
    )
    reviser = ScriptedWriter({"s2": [part("B, simpler")]}, revise=True)

    revised = await engine_over(db, reviser).build(
        Request(TYPE, plan_version_id=PLAN, content_id=first.saved_as, feedback="Simpler s2.")
    )

    assert revised.saved_as == first.saved_as
    assert reviser.seen["feedback"] == "Simpler s2."
    assert all(unit["has_part"] for unit in reviser.seen["draft"]["units"])
    record = await SqlAlchemyContentRecords().get(db, first.saved_as)
    assert record is not None
    assert (record.version, record.review_status) == (2, "pending")
    assert [s["part"]["title"] for s in record.manifest["sections"]] == ["A", "B, simpler"]


async def test_a_draft_the_writer_leaves_unfinished_is_never_submitted(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)

    with pytest.raises(EngineIncompleteError, match="s2"):
        await engine_over(db, ScriptedWriter({"s1": [part("Only one")]})).build(
            Request(type=TYPE, plan_version_id=PLAN)
        )

    assert (
        await SqlAlchemyContentRecords().find(
            db, plan_version_id=PLAN, type=TYPE, level=None, student_id=None
        )
        == []
    )


async def test_a_writer_that_stops_early_is_resumed_on_its_draft(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)
    writer = _StopsAfterOnePart()

    built = await engine_over(db, writer).build(Request(type=TYPE, plan_version_id=PLAN))  # type: ignore[arg-type]

    assert writer.feedback[1] == "Write the parts still missing, for the units: ['s2']."
    record = await SqlAlchemyContentRecords().get(db, built.saved_as)
    assert record is not None
    assert [s["part"]["title"] for s in record.manifest["sections"]] == ["A", "B"]


async def test_a_writer_that_runs_out_of_turns_is_resumed_on_its_draft(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)
    writer = _StopsAfterOnePart(out_of_turns=True)

    built = await engine_over(db, writer).build(Request(type=TYPE, plan_version_id=PLAN))  # type: ignore[arg-type]

    record = await SqlAlchemyContentRecords().get(db, built.saved_as)
    assert record is not None
    assert [s["part"]["title"] for s in record.manifest["sections"]] == ["A", "B"]


class _StopsAfterOnePart:
    """Writes the first unit still missing each time it runs, as a model that stops early."""

    def __init__(self, *, out_of_turns: bool = False) -> None:
        self.feedback: list[str] = []
        self.out_of_turns = out_of_turns

    async def write(self, client, draft, lesson, *, feedback):  # type: ignore[no-untyped-def]
        self.feedback.append(feedback)
        missing = [unit["unit_id"] for unit in draft["units"] if not unit["has_part"]]
        title = {"s1": "A", "s2": "B"}[missing[0]]
        await client.call_tool(
            "add_part", {"draft_id": draft["draft_id"], "unit_id": missing[0], "part": part(title)}
        )
        if self.out_of_turns:
            raise WriterStoppedError("the writer stopped: max_iters")
        return "Wrote one part."


async def test_errors_a_second_reader_finds_go_back_to_the_writer(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)
    checker = _FindsOneError()
    writer = _Fixer()

    built = await ContentEngine(lambda: server_over(db), lambda: writer, lambda: checker).build(
        Request(type=TYPE, plan_version_id=PLAN)
    )

    assert writer.feedback[1] == (
        "A second reader found these errors; correct each with revise_part: "
        f"['the s2 part: 1/4 + 2/4 is 3/4, not 3/8.']. {READ_FIRST}"
    )
    assert checker.checked == 4
    record = await SqlAlchemyContentRecords().get(db, built.saved_as)
    assert record is not None
    assert [s["part"]["title"] for s in record.manifest["sections"]] == ["A", "B fixed"]


class _FindsOneError:
    """Finds one error in s2 until the writer has revised it."""

    def __init__(self) -> None:
        self.checked = 0

    async def errors(self, brief, unit, part):  # type: ignore[no-untyped-def]
        self.checked += 1
        wrong = unit["unit"]["unit_id"] == "s2" and part["title"] == "B"
        return ["1/4 + 2/4 is 3/4, not 3/8."] if wrong else []


class _Fixer:
    """Writes both parts, then revises s2 when told of its error."""

    def __init__(self) -> None:
        self.feedback: list[str] = []

    async def write(self, client, draft, lesson, *, feedback):  # type: ignore[no-untyped-def]
        self.feedback.append(feedback)
        draft_id = draft["draft_id"]
        if not feedback:
            for unit_id, title in (("s1", "A"), ("s2", "B")):
                await client.call_tool(
                    "add_part", {"draft_id": draft_id, "unit_id": unit_id, "part": part(title)}
                )
        else:
            await client.call_tool(
                "revise_part", {"draft_id": draft_id, "unit_id": "s2", "part": part("B fixed")}
            )
        return "Wrote."


@pytest.mark.skipif(not tikz_available(), reason="TeX draws the figure")
async def test_a_drawing_that_will_not_draw_stops_the_draft_being_saved(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)
    figured = {
        **SPEC,
        "parts": [
            *SPEC["parts"],  # type: ignore[misc]
            {"name": "figure", "description": "A drawing", "type": "tikz"},
        ],
    }
    await build_content_catalogue().add(db, TYPE, figured, "Researcher")
    broken = {**part("A"), "figure": "\\begin{tikzpicture}\\draw (0,0) -- (1,1)\\end{tikzpicture}"}
    drawn = {**part("B"), "figure": "\\begin{tikzpicture}\\draw (0,0) -- (1,1);\\end{tikzpicture}"}

    with pytest.raises(EngineIncompleteError, match="the s1 part, at figure: it does not draw"):
        await engine_over(db, ScriptedWriter({"s1": [broken], "s2": [drawn]})).build(
            Request(type=TYPE, plan_version_id=PLAN)
        )


async def test_a_concluded_lesson_takes_no_draft(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db, concluded=True)

    with pytest.raises(EngineRefusedError, match="concluded"):
        await engine_over(db, ScriptedWriter({})).build(Request(type=TYPE, plan_version_id=PLAN))


async def test_the_engine_builds_only_engine_types(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)

    with pytest.raises(EngineRefusedError, match="is not drafted"):
        await engine_over(db, ScriptedWriter({})).build(
            Request(type=BuiltIn.LESSON_NOTE.value, plan_version_id=PLAN)
        )


async def test_the_content_service_generates_an_engine_type_at_class_level_only(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)
    generator = EngineGenerator(
        engine_over(db, ScriptedWriter({"s1": [part("A")], "s2": [part("B")]}))
    )

    content_id = await generator.generate(
        db, plan_version_id=PLAN, type=TYPE, level=Level.CLASS, choices=GenerationChoices()
    )

    assert content_id.startswith("AT-")
    with pytest.raises(ContentError, match="class_level_only"):
        generator.check(Level.LEARNER, GenerationChoices())


async def test_the_agent_making_content_reports_what_it_does_on_the_contents_channel(  # type: ignore[no-untyped-def]
    db, monkeypatch
) -> None:
    from app.domains.content.progress import generation_channel
    from app.infra import progress

    published: list[tuple[str, dict[str, object]]] = []
    monkeypatch.setattr(
        progress, "publish", lambda channel, event: published.append((channel, event))
    )
    await seed_lesson(db)
    generator = EngineGenerator(
        engine_over(db, ScriptedWriter({"s1": [part("A")], "s2": [part("B")]}))
    )

    await generator.generate(
        db, plan_version_id=PLAN, type=TYPE, level=Level.CLASS, choices=GenerationChoices()
    )

    assert published[0] == (generation_channel(PLAN, TYPE), {"kind": "start", "data": {}})


async def test_an_outside_client_without_an_access_code_is_refused(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)

    async with Client(server_over(db)) as client:
        started = await client.call_tool("start_draft", {"type": TYPE, "plan_version_id": PLAN})
        with pytest.raises(MCPError, match="Sign in"):
            await client.read_resource("content-types://?engine=mcp")

    assert started.is_error
    assert "Sign in" in started.content[0].text  # type: ignore[union-attr]


async def test_a_draft_belongs_to_whoever_started_it(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)
    with as_the_app():
        async with Client(server_over(db)) as client:
            started = await client.call_tool("start_draft", {"type": TYPE, "plan_version_id": PLAN})
    draft_id = json.loads(started.content[0].text)["draft_id"]  # type: ignore[union-attr]

    with pytest.raises(DraftError, match="no draft"):
        await build_drafting_service().read(db, draft_id=draft_id, by="code|someone-else")


async def test_the_viewer_tool_is_bound_to_its_page_and_returns_the_content(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)
    built = await engine_over(db, ScriptedWriter({"s1": [part("A")], "s2": [part("B")]})).build(
        Request(type=TYPE, plan_version_id=PLAN)
    )

    with as_the_app():
        async with Client(server_over(db)) as client:
            tools = {tool.name: tool for tool in (await client.list_tools()).tools}
            page = await client.read_resource(VIEWER_URI)
            shown = await client.call_tool("show_content", {"content_id": built.saved_as})

    assert tools["show_content"].meta["ui"] == {"resourceUri": VIEWER_URI}  # type: ignore[index]
    assert page.contents[0].mime_type == "text/html;profile=mcp-app"
    assert "ui/notifications/tool-result" in page.contents[0].text  # type: ignore[union-attr]
    item = json.loads(shown.content[0].text)  # type: ignore[union-attr]
    assert (item["type"], item["review_status"]) == (TYPE, "pending")
    assert [s["part"]["title"] for s in item["content"]["sections"]] == ["A", "B"]
    assert "ui/notifications/size-changed" in page.contents[0].text  # type: ignore[union-attr]


async def test_engine_content_is_given_the_field_order_of_the_spec_it_was_built_with(db) -> None:  # type: ignore[no-untyped-def]
    """Storage does not keep an object's key order, so the viewer is told the spec's."""
    await seed_lesson(db)
    built = await engine_over(db, ScriptedWriter({"s1": [part("A")], "s2": [part("B")]})).build(
        Request(type=TYPE, plan_version_id=PLAN)
    )

    with as_the_app():
        async with Client(server_over(db)) as client:
            shown = await client.call_tool("show_content", {"content_id": built.saved_as})

    item = json.loads(shown.content[0].text)  # type: ignore[union-attr]
    assert [field["name"] for field in item["parts"]] == ["title", "examples"]
    assert [field["name"] for field in item["parts"][1]["fields"]] == ["problem", "solution"]


async def test_a_draft_is_shown_as_it_would_save_so_far(db) -> None:  # type: ignore[no-untyped-def]
    await seed_lesson(db)
    with as_the_app():
        async with Client(server_over(db)) as client:
            started = await client.call_tool("start_draft", {"type": TYPE, "plan_version_id": PLAN})
            draft_id = json.loads(started.content[0].text)["draft_id"]  # type: ignore[union-attr]
            added = await client.call_tool(
                "add_part", {"draft_id": draft_id, "unit_id": "s1", "part": part("A")}
            )
            shown = await client.call_tool("show_draft", {"draft_id": draft_id})

    assert json.loads(added.content[0].text)["missing"] == ["s2"]  # type: ignore[union-attr]
    item = json.loads(shown.content[0].text)  # type: ignore[union-attr]
    assert (item["type"], item["version"], item["review_status"]) == (TYPE, None, "missing s2")
    assert [s["unit_id"] for s in item["content"]["sections"]] == ["s1"]


async def test_selected_text_is_found_in_the_draft_by_unit_and_field(db) -> None:  # type: ignore[no-untyped-def]
    """Any type's draft is plain parts, so one tool finds text in all of them."""
    await seed_lesson(db)
    with as_the_app():
        async with Client(server_over(db)) as client:
            started = await client.call_tool("start_draft", {"type": TYPE, "plan_version_id": PLAN})
            draft_id = json.loads(started.content[0].text)["draft_id"]  # type: ignore[union-attr]
            await client.call_tool(
                "add_part", {"draft_id": draft_id, "unit_id": "s1", "part": part("A")}
            )
            await client.call_tool(
                "add_part", {"draft_id": draft_id, "unit_id": "s2", "part": part("B")}
            )
            found = await client.call_tool("locate_text", {"draft_id": draft_id, "text": "1/4 + 2"})
            none = await client.call_tool("locate_text", {"draft_id": draft_id, "text": "nowhere"})

    result = json.loads(found.content[0].text)  # type: ignore[union-attr]
    assert result["count"] == 2
    assert {(m["unit_id"], m["path"]) for m in result["matches"]} == {
        ("s1", "examples.0.problem"),
        ("s2", "examples.0.problem"),
    }
    assert json.loads(none.content[0].text) == {"count": 0, "matches": []}  # type: ignore[union-attr]


async def test_the_writer_is_told_each_place_and_the_line_in_a_long_field() -> None:
    from app.domains.content_engine.infrastructure.engine import where_said

    said = where_said(
        {
            "count": 2,
            "matches": [
                {"unit_id": "po1", "path": "core_step.content", "line": 3, "context": "…"},
                {"unit_id": "po1", "path": "core_step.blocks.0.problem", "context": "…"},
            ],
        }
    )

    assert said == (
        "The selected text is in the draft at: unit_id=po1, path=core_step.content, line 3; "
        "unit_id=po1, path=core_step.blocks.0.problem."
    )
    assert "in no part" in where_said({"count": 0, "matches": []})


async def test_the_real_writer_fills_a_draft_through_the_real_tools(db) -> None:  # type: ignore[no-untyped-def]
    """ReActV2 over the in-memory MCP client, with only the model's replies scripted.

    It runs the writer's own tool conversion, so a tool schema DSPy cannot read fails here.
    """
    await seed_lesson(db)

    def turn(name: str, args: dict[str, object]) -> dict[str, object]:
        return {
            "next_thought": f"Call {name}.",
            "tool_calls": {"tool_calls": [{"name": name, "args": args}]},
        }

    def script(draft_id: str) -> list[dict[str, object]]:
        return [
            turn("read_draft", {"draft_id": draft_id}),
            turn("add_part", {"draft_id": draft_id, "unit_id": "s1", "part": part("A")}),
            turn("add_part", {"draft_id": draft_id, "unit_id": "s2", "part": part("B")}),
            turn("submit", {"summary": "Wrote both steps."}),
        ]

    built = await ContentEngine(lambda: server_over(db), lambda: _Scripted(script)).build(
        Request(type=TYPE, plan_version_id=PLAN)
    )

    assert built.summary == "Wrote both steps."
    record = await SqlAlchemyContentRecords().get(db, built.saved_as)
    assert record is not None
    assert [s["part"]["title"] for s in record.manifest["sections"]] == ["A", "B"]


class _Scripted:
    """The real writer on a model whose replies are scripted once the draft's ID is known."""

    def __init__(self, script) -> None:  # type: ignore[no-untyped-def]
        self._script = script

    async def write(self, client, draft, lesson, *, feedback):  # type: ignore[no-untyped-def]
        writer = EngineWriter(DummyLM(self._script(draft["draft_id"])))
        return await writer.write(client, draft, lesson, feedback=feedback)


async def test_the_checker_is_told_which_fields_a_part_holds() -> None:
    from app.domains.content_engine.infrastructure.checker import unit_context

    held = unit_context({}, {"unit_id": "lesson"}, ["theme", "intro", "evaluation"])

    assert held["fields_this_part_holds"] == ["theme", "intro", "evaluation"]
    assert "fields_this_part_holds" not in unit_context({}, {"unit_id": "lesson"})


async def test_a_part_sent_as_json_text_is_read_as_the_object_it_writes_out(db) -> None:  # type: ignore[no-untyped-def]
    import json

    await seed_lesson(db)
    with as_the_app():
        async with Client(server_over(db)) as client:
            opened = await client.call_tool("start_draft", {"type": TYPE, "plan_version_id": PLAN})
            draft_id = opened.structured_content["draft_id"]  # type: ignore[index]
            sent = await client.call_tool(
                "add_part",
                {"draft_id": draft_id, "unit_id": "s1", "part": json.dumps(part("A"))},
            )
            not_json = await client.call_tool(
                "add_part", {"draft_id": draft_id, "unit_id": "s2", "part": "{not json"}
            )

    assert not sent.is_error, sent.content
    assert not_json.is_error and "not valid JSON" in not_json.content[0].text  # type: ignore[union-attr]
