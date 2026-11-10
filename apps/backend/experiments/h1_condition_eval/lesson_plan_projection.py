"""Project a canonical lesson document into the plan shape the surfaces already read.

Nothing downstream changes. ``rater_packets``, the evidence projector, ``student_tasks``
and the worksheet renderer keep taking the same dict; it is now *derived* from a
document plus her note files instead of being a second, hand-maintained copy of both.

That is the whole claim, and it is testable: for a migrated lesson this projection must
equal the frozen entry in ``eval_set.json`` exactly. ``diff`` is the test.

    uv run python -m experiments.h1_condition_eval.lesson_plan_projection plan lessons/t3-w05.xml
    uv run python -m experiments.h1_condition_eval.lesson_plan_projection diff lessons/t3-w05.xml
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.lesson_document import Lesson, Section, Step, load

HERE = Path(__file__).parent

# How a note region reaches a plan block. Her heading is content in an explanation and
# scaffolding on set work — "Student activity" names the block's role, and the role is
# now an attribute, so repeating it in the question text would be the third copy.
_ROLE_TO_BLOCK = {
    "explanation": "explanation",
    "worked-example": "worked_example",
    "set-work": "practice",
    "recall": None,
}


def _worked_example(section: Section) -> dict[str, Any]:
    """A region whose heading names the problem and whose body works it.

    Both of the things a pattern used to decide here are now read: ``solution`` is her
    answer marker verbatim (four spellings across the corpus, and the first version of
    the pattern knew three), and ``enumerator`` is the number her heading carries, which
    comes off because numbering is the renderer's. The label is the marker with its
    markdown and punctuation taken off — presentation, not meaning.

    ``final_answer`` is DECLARED, not taken from the last line. Taking the last line is
    what the frozen corpus does and it is a guess: eight of the nineteen examples here
    are lettered (a), (b), (c), and their recorded "final answer" is the last part's.
    An example that reaches several answers declares none.
    """
    content = (
        section.body.replace(f"{section.solution}\n", "", 1) if section.solution else section.body
    )
    problem = section.heading[len(section.enumerator) :].strip()
    return {
        "id": section.id,
        "type": "worked_example",
        "problem": problem,
        "steps": [{"label": section.solution.strip("*:. ") or None, "content": content.strip()}],
        "final_answer": section.final_answer,
    }


def _block(section: Section) -> dict[str, Any] | None:
    kind = _ROLE_TO_BLOCK[section.role]
    if kind is None or not section.delivered:
        return None
    if kind == "worked_example":
        return _worked_example(section)
    if kind == "practice":
        return {"id": section.id, "type": kind, "question": section.body, "answer": ""}
    heading = f"**{section.heading}**\n\n" if section.heading else ""
    return {"id": section.id, "type": kind, "content": heading + section.body}


def _question_block(question: Any) -> dict[str, Any]:
    text = question.text or "\n".join(f"({label}) {body}" for label, body in question.parts)
    block = {"id": question.id, "type": "practice", "question": text, "answer": ""}
    if question.objective:
        block["lesson_objective_id"] = question.objective
    return block


def _step(step: Step, lesson: Lesson) -> dict[str, Any]:
    objective = {o.id: o for o in lesson.objectives}.get(step.objective or "")
    projected: dict[str, Any] = {"step_id": step.id, "step_kind": step.kind}
    if step.instructional_type and step.kind != "core":
        projected["instructional_type"] = step.instructional_type
    projected["title"] = step.title
    projected["content"] = step.prose
    projected["estimated_minutes"] = step.minutes
    projected["activities"] = [
        {
            "who": activity.who,
            "what": activity.what,
            **({} if activity.sets_work is None else {"sets_work": activity.sets_work}),
        }
        for activity in step.activities
    ]
    if step.note_path is not None:
        projected["note"] = step.note_text
        projected["note_file"] = f"notes/{step.id}.md"
        projected["regions"] = [
            {
                "id": section.id,
                "title": section.heading or step.title,
                "role": section.role,
                "body": section.body,
            }
            for section in step.sections
        ]
    projected["blocks"] = [
        block for block in (_block(section) for section in step.sections) if block
    ] + [_question_block(question) for question in step.questions]
    if objective:
        projected["lesson_objective_id"] = objective.id
        projected["kc_type"] = objective.kc_type
        projected["instructional_type"] = step.instructional_type
    return projected


def plan(lesson: Lesson) -> dict[str, Any]:
    """The lesson as a session plan, with everything derivable derived."""
    curriculum = {objective.id: objective.text for objective in lesson.curriculum}
    return {
        "plan_id": lesson.attrs["plan-id"],
        "session_id": lesson.attrs["session-id"],
        "subject": lesson.attrs["subject"],
        "track": lesson.attrs["track"],
        "grade": lesson.attrs["grade"],
        "term": lesson.attrs["term"],
        "week": int(lesson.attrs["week"]),
        "topic": lesson.attrs["topic"],
        "subtopic": lesson.attrs["subtopic"],
        "curriculum_objectives": [
            {
                "curriculum_objective_id": objective.id,
                "objective_text": objective.text,
                "objective_order": order,
            }
            for order, objective in enumerate(lesson.curriculum, start=1)
        ],
        "lesson_plan_objectives": [
            {
                "lesson_objective_id": objective.id,
                "objective_text": objective.text,
                "objective_order": order,
                "curriculum_objective_id": objective.curriculum,
                "curriculum_objective_text": curriculum[objective.curriculum],
                "kc_type": objective.kc_type,
                "kc_focus": objective.text,
            }
            for order, objective in enumerate(lesson.objectives, start=1)
        ],
        "steps": [_step(step, lesson) for step in lesson.steps],
        "entry_behaviour": list(lesson.entry_behaviour),
        "instructional_materials": list(lesson.materials),
        "references": list(lesson.references),
        "misconceptions": [],
        "assessments": [],
    }


@dataclass(frozen=True)
class Difference:
    path: str
    projected: Any
    frozen: Any


def _differences(projected: Any, frozen: Any, path: str = "") -> list[Difference]:
    """Every place the two disagree, addressed so it can be looked at."""
    if isinstance(projected, dict) and isinstance(frozen, dict):
        return [
            line
            for key in sorted(set(projected) | set(frozen))
            for line in _differences(projected.get(key), frozen.get(key), f"{path}.{key}")
        ]
    if isinstance(projected, list) and isinstance(frozen, list):
        if len(projected) != len(frozen):
            return [Difference(path, f"{len(projected)} items", f"{len(frozen)} items")]
        return [
            line
            for index, (left, right) in enumerate(zip(projected, frozen, strict=True))
            for line in _differences(left, right, f"{path}[{index}]")
        ]
    return [] if projected == frozen else [Difference(path, projected, frozen)]


def _step_index(path: str) -> int:
    """Which step a difference sits under, or -1 when it sits under none."""
    if not path.startswith(".steps["):
        return -1
    return int(path[len(".steps[") : path.index("]")])


def _labels_by_step(lesson: Lesson) -> dict[str, tuple[str, ...]]:
    """The figure labels each step declares, for recognising a caption added by hand."""
    return {
        step.id: tuple(ref for section in step.sections for ref in section.figures if ref)
        for step in lesson.steps
    }


def _without_captions(content: str, labels: tuple[str, ...]) -> tuple[str, ...]:
    """``content`` as it read before the declared captions, under each reading of them.

    A caption reached the note in one of two shapes: a label prepended to a description
    she already had, or a whole paragraph written where there was none. From this side
    the two are indistinguishable — ``**fig-05.** A square, named…`` either way — so
    both readings are returned and the caller accepts only an exact match against the
    frozen text. Guessing which shape it is would be the kind of decision this exercise
    exists to remove.
    """
    label_only = content
    for ref in labels:
        label_only = label_only.replace(f"**{ref}.** ", "")

    whole = content
    for ref in labels:
        lines = whole.splitlines()
        start = next((i for i, line in enumerate(lines) if line.startswith(f"**{ref}.**")), None)
        if start is None:
            continue
        end = start
        while end < len(lines) and lines[end].strip():
            end += 1
        while end < len(lines) and not lines[end].strip():
            end += 1
        whole = "\n".join(lines[:start] + lines[end:])
    return (label_only, whole.strip())


def correction(difference: Difference, labels: tuple[str, ...] = ()) -> str | None:
    """What the document deliberately says differently from the frozen plan.

    Not a format change and not an unexplained disagreement: a third thing, where a
    reader established the frozen value was wrong. Kept apart from the other two so a
    correction has to be argued for once and then stays visible.
    """
    if difference.path.endswith(".final_answer") and difference.projected == "":
        return (
            "a lettered example has no single final answer; the frozen plan records the last part's"
        )
    if difference.path.endswith(".content") and _only_a_caption_changed(difference, labels):
        return "a figure caption corrected against the drawing it describes"
    return None


def _only_a_caption_changed(difference: Difference, labels: tuple[str, ...]) -> bool:
    """True when every paragraph that differs is a caption the document declares.

    Exact, like the caption-added rule beside it: paragraph for paragraph, and a
    differing one forgiven only if it opens with a label this step actually declares.
    Otherwise a caption whose WORDING was wrong reads as a disagreement, which would
    bury it among the transcription's own losses.
    """
    if not isinstance(difference.projected, str) or not isinstance(difference.frozen, str):
        return False
    projected = difference.projected.split("\n\n")
    frozen = difference.frozen.split("\n\n")
    if len(projected) != len(frozen) or projected == frozen:
        return False
    return all(
        mine == theirs or any(mine.startswith(f"**{ref}.**") for ref in labels)
        for mine, theirs in zip(projected, frozen, strict=True)
    )


def classify(difference: Difference, labels: tuple[str, ...] = ()) -> str | None:
    """Why the format changed this, or None when the two genuinely disagree.

    A format change is one the migration makes on purpose and can state as a rule. A
    disagreement is the frozen plan and her note saying different things, and every one
    of those on this corpus turned out to be the transcription's decomposition losing
    something — so they are reported, not absorbed.

    The caption rule is exact rather than general. Absorbing every block difference on a
    step whose note was edited was tried, and it swallowed real findings: ``t3-w06``'s
    blocks differ because they hold the step's own prose, which has nothing to do with
    its note. So a caption is absorbed only when removing the labels the document
    DECLARES turns the projection back into the frozen text, character for character.
    """
    if difference.path.endswith(".id"):
        return "ids are sequential within a step; the corpus nests worked examples as b1e1"
    if difference.path.endswith(".regions") and difference.frozen is None:
        return "the note's parts, declared; the frozen plan predates the field"
    if difference.path.endswith(".note") and difference.projected is None:
        return "an intro step with no note file carries note:'' in the frozen plan"
    if difference.path.endswith(".note"):
        return "the document references notes-clean/, which is what generation reads"
    if difference.path.endswith(".content") and isinstance(difference.projected, str):
        if difference.frozen in _without_captions(difference.projected, labels):
            return "a figure caption written into notes-clean/ since the plan was frozen"
    return None


def diff(path: Path) -> int:
    lesson = load(path)
    frozen = next(
        (
            case["plan"]
            for case in json.loads(EVAL_SET_PATH.read_text())["cases"]
            if case["lesson"] == lesson.id
        ),
        None,
    )
    if frozen is None:
        raise SystemExit(f"{lesson.id} is not in {EVAL_SET_PATH.name}")
    found = _differences(plan(lesson), frozen)
    if not found:
        print(f"{lesson.id}: the projection equals the frozen plan exactly")
        return 0
    labels = _labels_by_step(lesson)
    steps = [step.id for step in lesson.steps]

    def why_for(difference: Difference) -> str | None:
        index = _step_index(difference.path)
        return classify(difference, labels.get(steps[index], ()) if index >= 0 else ())

    accepted = [(d, why) for d in found if (why := why_for(d))]

    def corrects(difference: Difference) -> str | None:
        index = _step_index(difference.path)
        return correction(difference, labels.get(steps[index], ()) if index >= 0 else ())

    corrected = [(d, why) for d in found if not why_for(d) and (why := corrects(d))]
    findings = [d for d in found if not why_for(d) and not corrects(d)]
    reasons: dict[str, int] = {}
    for _, why in accepted + corrected:
        reasons[why] = reasons.get(why, 0) + 1
    print(
        f"{lesson.id}: {len(accepted)} format changes, {len(corrected)} corrections, "
        f"{len(findings)} disagreements\n"
    )
    for why, count in sorted(reasons.items()):
        print(f"  {count:>3}x  {why}")
    for difference in findings:
        print(f"\n  {difference.path}")
        print(f"      projected {_short(difference.projected)}")
        print(f"      frozen    {_short(difference.frozen)}")
    return 0


def _short(value: Any) -> str:
    text = repr(value)
    return text if len(text) <= 220 else text[:200] + f"... ({len(text)} chars)"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "diff"))
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    path = args.path if args.path.is_absolute() else HERE / args.path
    if args.command == "diff":
        return diff(path)
    print(json.dumps(plan(load(path)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
