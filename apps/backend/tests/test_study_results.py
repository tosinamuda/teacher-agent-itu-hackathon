"""The evaluation's marks are placed as a class test places a learner: by the weakest objective."""

from __future__ import annotations

from app.domains.teaching.domain.study_results import MarkedAnswer, MarkedScript, learner_results


def _answer(objective: str, mark: str, code: str | None = None) -> MarkedAnswer:
    return MarkedAnswer(objective, mark, code)


def _script(name: str, *answers: MarkedAnswer, total: str = "?") -> MarkedScript:
    return MarkedScript(
        student_id=f"ST-{name}", full_name=name, teacher_total=total, answers=list(answers)
    )


def test_a_learner_is_placed_by_their_weakest_objective_and_scored_over_every_marked_answer() -> (
    None
):
    script = _script(
        "Ada",
        _answer("lo1", "correct"),
        _answer("lo1", "correct"),
        _answer("lo2", "incorrect", "M-ORDER"),
        _answer("lo2", "unmarked"),
        total="2/3",
    )

    [result] = learner_results([script])

    assert (result.correct, result.out_of) == (2, 3)
    assert result.band == "remediate"
    by_objective = {o.lesson_objective_id: o for o in result.objectives}
    assert (by_objective["lo1"].correct, by_objective["lo1"].out_of) == (2, 2)
    assert (by_objective["lo2"].correct, by_objective["lo2"].out_of) == (0, 1)
    assert by_objective["lo2"].misconceptions == ["M-ORDER"]
    assert result.teacher_total == "2/3"


def test_the_neediest_come_first_and_a_script_with_nothing_marked_is_left_out() -> None:
    strong = _script("Bola", _answer("lo1", "correct"), _answer("lo1", "correct"))
    weak = _script("Chi", _answer("lo1", "incorrect"), _answer("lo1", "incorrect"))
    blank = _script("Dayo", _answer("lo1", "unmarked"))

    results = learner_results([strong, blank, weak])

    assert [r.full_name for r in results] == ["Chi", "Bola"]
    assert [r.band for r in results] == ["remediate", "extend"]
