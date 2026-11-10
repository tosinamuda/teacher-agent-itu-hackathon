"""The evaluation's slides show only questions, and no other step rehearses its problems."""

from __future__ import annotations

from app.domains.content_engine.rules.slide_deck.questions import evaluation_slide_issues
from app.domains.content_engine.rules.slide_deck.repeats import (
    repeated_drawings,
    repeated_measures,
    repeated_slides,
)
from app.domains.content_engine.rules.slide_deck.review import slide_deck_issues
from tests.slide_deck_support import deck as _deck
from tests.slide_deck_support import slide as _slide


def test_an_evaluation_slide_that_states_the_answer_is_sent_back() -> None:
    draft = _deck(
        evaluation=[
            _slide("Estimate the distance for $60\\text{ cm}$ steps, $8,315$ steps"),
            _slide("Approx $4.99\\text{ km}$ (near $5\\text{ km}$)", title="Number line"),
        ]
    )

    issues = evaluation_slide_issues(draft)

    assert len(issues) == 1
    assert issues[0].startswith("evaluation: slide 2: 'Approx $4.99")
    assert "speaker notes" in issues[0]


def test_a_question_that_asks_approximately_or_has_no_result_is_not_an_answer() -> None:
    draft = _deck(
        evaluation=[
            _slide("Approximately how far is the school for $60\\text{ cm}$ steps?"),
            _slide("Estimate the distance for $50\\text{ cm}$ steps, $10{,}000$ steps"),
        ]
    )

    assert evaluation_slide_issues(draft) == []


def test_a_slide_in_another_step_with_the_evaluations_problem_is_sent_back() -> None:
    draft = _deck(
        core1=[
            _slide("Convert $60\\text{ cm}$ to $0.6\\text{ m}$", "Multiply by $8{,}000$ steps"),
            _slide("Estimate distance for $60\\text{ cm}$ steps, $8{,}315$ steps"),
        ],
        evaluation=[_slide("Estimate the distance for $60\\text{ cm}$ steps, $8,315$ steps")],
    )

    issues = evaluation_slide_issues(draft)

    assert len(issues) == 1
    assert issues[0].startswith("core1: slide 2 puts a problem the evaluation asks")
    assert "another question of the note" in issues[0]


def test_the_evaluations_problem_split_over_several_points_of_a_slide_is_still_its_problem() -> (
    None
):
    draft = _deck(
        core1=[_slide("Step length $60\\text{ cm}$.", "$8{,}315$ steps taken.", "Estimate.")],
        evaluation=[_slide("$60\\text{ cm}$ per step, $8,315$ steps.", "Estimate the distance.")],
    )

    assert [issue.split(":")[0] for issue in evaluation_slide_issues(draft)] == ["core1"]


def test_other_steps_with_their_own_numbers_pass_and_the_checks_join_the_deck_checks() -> None:
    draft = _deck(
        core1=[_slide("Multiply: $0.6\\text{ m}\\times 8{,}000 = 4{,}800\\text{ m}$")],
        evaluation=[_slide("Estimate the distance for $60\\text{ cm}$ steps, $8{,}315$ steps")],
    )
    assert evaluation_slide_issues(draft) == []
    assert slide_deck_issues(draft) == []

    answered = _deck(evaluation=[_slide("Answer: about $5\\text{ km}$")])
    assert len(slide_deck_issues(answered)) == 1


def test_a_slide_that_shows_only_what_another_slide_of_its_step_shows_is_a_repeat() -> None:
    draft = _deck(
        core1=[
            _slide("Convert $60\\text{ cm}$ to $0.6\\text{ m}$."),
            _slide("Multiply: $0.6\\text{ m}\\times 8{,}000 = 4{,}800\\text{ m}$"),
            _slide(
                "Convert $60\\text{ cm}$ to $0.6\\text{ m}$",
                "Multiply: $0.6\\text{ m}\\times 8{,}000 = 4{,}800\\text{ m}$",
                "Answer: $4.8\\text{ km}$",
            ),
        ],
        intro=[_slide("Name a distance you estimate"), _slide("Name a distance you estimate")],
    )

    assert repeated_slides(draft) == [
        "core1: slide 1 shows only what slide 3 shows; show each idea once, on one slide",
        "core1: slide 2 shows only what slide 3 shows; show each idea once, on one slide",
        "intro: slide 2 shows only what slide 1 shows; show each idea once, on one slide",
    ]


def test_a_latex_command_outside_dollar_signs_is_sent_back_on_a_slide_or_in_its_notes() -> None:
    draft = _deck(
        core1=[
            {
                "title": "What is estimation?",
                "points": [{"point": "Uses the symbol \\approx"}, {"point": "Uses $\\approx$"}],
                "speaker_notes": "Explain that the symbol \\approx means about, and write it.",
            }
        ]
    )

    issues = slide_deck_issues(draft)

    assert len(issues) == 2
    assert all("LaTeX command outside $ signs" in issue for issue in issues)
    assert issues[0].startswith("core1: slide 1: 'Uses the symbol \\\\approx'")


def test_a_spacing_command_outside_dollar_signs_is_sent_back() -> None:
    draft = _deck(core=[_slide("A step of $60$\\,cm", title="Steps")])

    issues = slide_deck_issues(draft)

    assert len(issues) == 1 and "LaTeX command outside $ signs" in issues[0]


def test_words_inside_dollar_signs_are_sent_back() -> None:
    draft = _deck(
        intro=[
            _slide("$Estimation = \\text{a quick approximate calculation}$", title="Recall"),
            _slide("Given: step $60\\text{ cm}$", "Find: the step in $\\text{m}$"),
        ]
    )

    issues = slide_deck_issues(draft)

    assert [issue.split(":")[1].strip() for issue in issues] == ["slide 1"]
    assert "words inside $ signs" in issues[0]


def test_a_drawing_that_an_earlier_slide_already_has_is_told_where() -> None:
    line = "\\begin{tikzpicture}\\draw (0,0) -- (1,0);\\end{tikzpicture}"
    draft = _deck(
        core1=[
            {**_slide("One", title="First"), "figure": line},
            {**_slide("Two", title="Second"), "figure": f"  {line}  "},
        ],
        intro=[{**_slide("Three", title="Third"), "figure": line}],
    )

    assert repeated_drawings(draft) == [
        "core1 slide 2 has the same drawing as core1 slide 1; draw it once, on the slide it "
        "belongs to",
        "intro slide 1 has the same drawing as core1 slide 1; draw it once, on the slide it "
        "belongs to",
    ]


def test_a_drawing_shares_its_slide_with_at_most_two_points() -> None:
    line = "\\begin{tikzpicture}\\draw (0,0) -- (1,0);\\end{tikzpicture}"
    crowded = {**_slide("One", "Two", "Three", title="Example"), "figure": line}
    roomy = {**_slide("The line", title="Picture"), "figure": line.replace("(1,0)", "(2,0)")}

    issues = slide_deck_issues(_deck(core1=[crowded, roomy]))

    assert len(issues) == 1
    assert "slide 1 has a drawing and 3 points; keep at most 2 with a drawing" in issues[0]


def test_a_slide_that_starts_from_a_problem_the_note_itself_works_is_not_a_rehearsal() -> None:
    worked = "Find the HCF of 30 and 45."
    draft = _deck(
        core=[_slide(worked, "$30 = 2 \\times 3 \\times 5$", title="HCF")],
        evaluation=[_slide(worked, title="Check")],
    )

    assert len(evaluation_slide_issues(draft)) == 1
    assert evaluation_slide_issues(draft, {"core": [worked]}) == []
    other = _deck(
        core=[_slide("Find the HCF of 12 and 18.", "30, 45")], evaluation=[_slide(worked)]
    )
    assert len(evaluation_slide_issues(other, {"core": [worked]})) == 1


def test_a_measure_said_twice_on_a_slide_that_is_not_working_is_sent_back() -> None:
    draft = _deck(
        intro=[
            _slide("A road of about 2 km: its distance $\\approx$ 2 km.", title="Estimates"),
            _slide("A road of about $2$ km.", "The road is 2 km long.", title="Roads"),
        ]
    )

    assert repeated_measures(draft)[:2] == [
        "intro: slide 1 says 2 km more than once; say a measure once on a slide",
        "intro: slide 2 says 2 km more than once; say a measure once on a slide",
    ]


def test_a_measure_a_step_shows_on_one_slide_is_not_shown_again_on_another() -> None:
    draft = _deck(
        intro=[
            _slide("A road of about 2 km.", title="Lengths"),
            _slide("Why estimate?", title="Why"),
            _slide("The distance $\\approx 2$ km, a field of 150 m.", title="Again"),
        ],
        evaluation=[_slide("A road of about 2 km.")],
    )

    assert repeated_measures(draft) == [
        "intro: slide 3 says 2 km again, as slide 1 does; say a measure once in a step"
    ]


def test_working_may_say_a_measure_again_and_a_step_count_is_not_a_measure() -> None:
    draft = _deck(
        core1=[
            _slide(
                "Steps are $60\\text{ cm}$ long, 8,315 steps.",
                "$0.6\\text{ m}\\times 8{,}000 = 4{,}800\\text{ m}$",
                "$4{,}800\\text{ m} = 4.8\\text{ km}$",
            ),
            _slide("Take 8,315 steps.", "Then take 8,315 steps more."),
        ]
    )

    assert repeated_measures(draft) == []
