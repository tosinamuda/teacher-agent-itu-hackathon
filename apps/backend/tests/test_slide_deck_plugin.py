"""The slide deck type, shipped as a plugin: it reads, installs and builds a draft."""

from __future__ import annotations

from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.content.application.plugins import PluginInstaller
from app.domains.content.infrastructure.catalogue import build_content_catalogue
from app.domains.content.infrastructure.plugin_store import SqlAlchemyPlugins
from app.domains.content.infrastructure.records import SqlAlchemyContentRecords
from app.domains.content.plugins.reader import folder_digest
from app.domains.content_engine.additions.slide_deck import slide_deck_cover
from app.domains.content_engine.infrastructure.engine import EngineIncompleteError, Request
from app.domains.content_engine.rules.slide_deck.wording import wording_faults
from app.shared.session_plan_view import SessionPlanView
from tests.content_engine_support import PLAN, ScriptedWriter, engine_over, seed_lesson
from tests.plugin_folder import read_plugin

PLUGIN = Path(__file__).parents[3] / "plugins" / "slide-deck"
SLIDE = {
    "title": "Adding fractions with one denominator",
    "points": [
        {"point": "$\\frac{1}{4} + \\frac{2}{4}$"},
        {"point": "Add the tops, keep the bottom"},
    ],
    "speaker_notes": "Ask: what stays the same? Watch for learners who add the bottoms too.",
}


def test_the_slide_deck_plugin_is_valid_and_writes_slides_for_each_plan_step() -> None:
    plugin, problems = read_plugin(PLUGIN)

    assert problems == []
    assert plugin is not None and plugin.definition is not None
    assert (plugin.definition.slug, plugin.definition.audience.value) == ("slide-deck", "teacher")
    assert plugin.spec.unit is not None and plugin.spec.unit.value == "plan_step"
    assert plugin.spec.parts is not None
    assert [part.name for part in plugin.spec.parts.fields] == ["slides"]
    assert [skill.slug for skill in plugin.skills] == ["writing-lesson-slides"]
    assert all(skill.instructions for skill in plugin.skills)
    assert [file.path for file in plugin.skills[0].files] == ["references/drawings.md"]


@pytest.mark.asyncio
async def test_installed_it_builds_a_deck_that_is_saved_as_content(db: AsyncSession) -> None:
    await seed_lesson(db)
    plugin, _ = read_plugin(PLUGIN)
    assert plugin is not None
    await PluginInstaller(build_content_catalogue(), SqlAlchemyPlugins()).install(
        db, plugin, folder_digest(PLUGIN), "Researcher"
    )
    deck = {"slides": [SLIDE]}
    writer = ScriptedWriter({"s1": [deck], "s2": [deck]})

    built = await engine_over(db, writer).build(Request(type="slide-deck", plan_version_id=PLAN))

    record = await SqlAlchemyContentRecords().get(db, built.saved_as)
    assert record is not None
    sections = record.manifest["sections"]
    assert isinstance(sections, list)
    assert [s["part"] for s in sections if isinstance(s, dict)] == [deck, deck]
    assert record.manifest["cover"] == {
        "title": "Adding fractions",
        "subtitle": "Mathematics · JSS1 · Fractions",
        "objectives": ["Add fractions with a common denominator"],
    }


def test_a_plan_with_no_title_gives_its_cover_the_topic_for_a_title() -> None:
    plan = SessionPlanView.model_validate(
        {
            "subject": "Mathematics",
            "grade": "JSS1",
            "topic": "Estimation",
            "lesson_plan_objectives": [
                {"lesson_objective_id": "lop01", "objective_text": "Estimate a distance"}
            ],
            "steps": [],
        }
    )

    assert slide_deck_cover(plan) == {
        "cover": {
            "title": "Estimation",
            "subtitle": "Mathematics · JSS1",
            "objectives": ["Estimate a distance"],
        }
    }
    assert slide_deck_cover(None) == {}


def test_a_plan_with_no_title_gives_its_cover_the_lessons_subtopic_and_keeps_the_topic() -> None:
    plan = SessionPlanView.model_validate(
        {
            "subject": "English Language",
            "grade": "JSS1",
            "topic": "Parts of Speech",
            "subtopic": "Types of nouns",
            "steps": [],
        }
    )

    assert slide_deck_cover(plan)["cover"] == {
        "title": "Types of nouns",
        "subtitle": "English Language · JSS1 · Parts of Speech",
        "objectives": [],
    }


async def _installed(db: AsyncSession) -> None:
    await seed_lesson(db)
    plugin, _ = read_plugin(PLUGIN)
    assert plugin is not None
    await PluginInstaller(build_content_catalogue(), SqlAlchemyPlugins()).install(
        db, plugin, folder_digest(PLUGIN), "Researcher"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("slide", "told"),
    [
        (
            {**SLIDE, "points": [{"point": "Intro"}, {"point": " ".join(["word"] * 13)}]},
            "runs past 12",
        ),
        ({**SLIDE, "points": [{"point": f"point {n}"} for n in range(6)]}, "6 points"),
        ({**SLIDE, "points": [{"point": "$\\text{Result in cm}$"}]}, "only words inside $ signs"),
        ({**SLIDE, "speaker_notes": "Ask."}, "needs speaker notes"),
        ({**SLIDE, "title": " ".join(["word"] * 11)}, "the title runs past 10"),
        ({"title": "Empty", "speaker_notes": SLIDE["speaker_notes"]}, "shows nothing"),
    ],
)
async def test_a_slide_the_class_cannot_read_is_sent_back_to_the_writer(
    db: AsyncSession, slide: dict[str, object], told: str
) -> None:
    await _installed(db)
    good, bad = {"slides": [SLIDE]}, {"slides": [slide]}
    writer = ScriptedWriter({"s1": [bad], "s2": [good]})

    with pytest.raises(EngineIncompleteError) as sent_back:
        await engine_over(db, writer).build(Request(type="slide-deck", plan_version_id=PLAN))

    assert told in str(sent_back.value)


@pytest.mark.asyncio
async def test_a_unit_inside_a_formula_is_not_words_in_maths(db: AsyncSession) -> None:
    await _installed(db)
    deck = {"slides": [{**SLIDE, "points": [{"point": "$60\\text{ cm} \\times 8$"}]}]}

    built = await engine_over(db, ScriptedWriter({"s1": [deck], "s2": [deck]})).build(
        Request(type="slide-deck", plan_version_id=PLAN)
    )

    assert built.saved_as


@pytest.mark.asyncio
async def test_a_formula_counts_as_one_word_on_a_slide(db: AsyncSession) -> None:
    await _installed(db)
    formula = "Add $\\frac{1}{4} + \\frac{2}{4} + \\frac{3}{4} + \\frac{4}{4}$ now"
    deck = {"slides": [{**SLIDE, "points": [{"point": formula}]}]}

    built = await engine_over(db, ScriptedWriter({"s1": [deck], "s2": [deck]})).build(
        Request(type="slide-deck", plan_version_id=PLAN)
    )

    assert built.saved_as


@pytest.mark.asyncio
async def test_the_frame_the_aim_is_worded_in_is_not_counted_in_a_points_length(
    db: AsyncSession,
) -> None:
    await _installed(db)
    aim = "By the end, I can sort objects as living or non-living, with reasons."
    deck = {"slides": [{**SLIDE, "points": [{"point": "Intro"}, {"point": aim}]}]}

    built = await engine_over(db, ScriptedWriter({"s1": [deck], "s2": [deck]})).build(
        Request(type="slide-deck", plan_version_id=PLAN)
    )

    assert built.saved_as


def _slide_with(*points: str) -> dict[str, object]:
    return {"title": "Estimating a distance", "points": [{"point": point} for point in points]}


@pytest.mark.parametrize(
    ("point", "fault"),
    [
        ("$\\approx 2\\text{ km}$", "names nothing before it"),
        ("≈ 2 km", "names nothing before it"),
        ("$2\\text{ km} \\approx 2\\text{ km}$", "same on both sides"),
        ("2 km ≈ 2 km", "same on both sides"),
        ("$4 + 4 = 4 + 4$", "same on both sides"),
    ],
)
def test_a_point_that_is_a_measure_of_nothing_or_a_relation_of_a_thing_to_itself_is_refused(
    point: str, fault: str
) -> None:
    faults = wording_faults("slide 3", _slide_with(point))

    assert len(faults) == 1 and fault in faults[0] and "slide 3" in faults[0]


@pytest.mark.parametrize(
    "point",
    [
        "The market is 2 km from the school",
        "Distance to the market ≈ 2 km",
        "$= \\frac{3}{4}$",
        "$\\frac{1}{4} + \\frac{2}{4} = \\frac{3}{4}$",
        "$x \\leq 5$",
    ],
)
def test_a_relation_that_says_something_is_left_alone(point: str) -> None:
    assert wording_faults("slide 3", _slide_with(point)) == []
