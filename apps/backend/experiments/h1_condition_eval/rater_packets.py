"""Blinded rating packets: one reference packet + one anonymous candidate, per judgment.

The packet is what a rater sees, and it is identical in structure for every condition —
reference material drawn from the teacher's plan, then one candidate pack under an opaque
id. Nothing names the condition, nothing hints that conditions exist, and the ids carry no
order (``cand-3f9a2c``, not ``A``/``B``), so a judge cannot infer which arm it is reading
or which it is "supposed" to prefer.

Candidates are rated INDEPENDENTLY and the C1-C0 difference is taken afterwards. Rating a
pair side by side would invite the judge to decide which is meant to win, and would break
the pairing the frozen analysis assumes.

The de-anonymisation key is written separately and is not part of any packet.

    uv run python -m experiments.h1_condition_eval.rater_packets <run-label>
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    WRITTEN_PRACTICE_FIELDS,
)
from app.domains.evaluation.application.constants import H1_ALIGNMENT_GUIDANCE, H1_RUBRIC
from app.domains.evaluation.application.lesson_reference import (
    LessonReference,
    lesson_reference,
    reference_sheet,
)
from app.domains.evaluation.application.worksheet_html.renderer import (
    render_h1_worksheet_html_pdf,
)
from app.shared.item_numbering import marks_a_numbered_run, under_supplied_number
from app.shared.llm_markup import reader_ready
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.assessment_overlap import overlap
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH

HERE = Path(__file__).parent
RUNS = HERE / "runs"


def candidate_id(run_label: str, lesson: str, condition: str, repeat: int) -> str:
    """An opaque, stable id. Deterministic so a rerun addresses the same candidate;
    hashed so neither the condition nor any ordering is recoverable from it."""
    seed = f"{run_label}|{lesson}|{condition}|{repeat}"
    return "cand-" + hashlib.sha256(seed.encode()).hexdigest()[:8]


def _plan_reference(reference: LessonReference) -> list[str]:
    """The taught lesson as the judge reads it — the one reference, rendered as markdown.

    Her own words for the activities, not their Gagné codes: the coding is the
    study's instrument and showing it would tell the rater what to look for. What is
    here is exactly what the worksheet PDF and the platform drawer show, in another
    layout; ``test_lesson_reference_surfaces`` holds the three to the same items.
    """
    lines = ["## The lesson as the teacher planned it\n"]
    lines.append(f"**Topic.** {reference.topic}  ")
    lines.append(f"**Subtopic.** {reference.subtopic}  ")
    lines.append(f"**Class.** {reference.grade}, {reference.term}, week {reference.week}\n")

    lines.append("**Objectives.** At the end of the lesson, students should be able to:\n")
    lines += [f"{i}. {text}" for i, text in enumerate(reference.objectives, start=1)] + [""]

    if reference.entry_behaviour:
        lines.append("**Previous knowledge.** Students have been taught:\n")
        lines += [f"- {item}" for item in reference.entry_behaviour] + [""]

    if reference.instructional_materials:
        lines.append(
            f"**Instructional materials.** {'; '.join(reference.instructional_materials)}\n"
        )

    lines.append("**Presentation.** In order:\n")
    for index, step in enumerate(reference.sequence, start=1):
        lines.append(f"{index}. *{step.objective}*")
        for activity in step.activities:
            lines.append(f"   - The {activity[4:] if activity.startswith('the ') else activity}.")
        for question in step.tasks_set:
            # Her activity sets are one block of numbered questions, so the newlines have
            # to be indented or the second question falls out of the list.
            indented = question.replace("\n", "\n     ")
            lines.append(f"   - Set for the students: {indented}")
    lines.append("")

    if reference.evaluation:
        lines.append("**Evaluation.** The teacher's own questions:\n")
        lines += [f"{i}. {q}" for i, q in enumerate(reference.evaluation, start=1)] + [""]
    return lines


def _numbered_here(text: Any, *, like: Any = None) -> str:
    """A prompt or answer for a list this function's caller numbers.

    The packet is markdown a judge reads as text, with no stylesheet behind it, so a
    kept run of sub-steps is lettered here rather than left to one. Any line the text
    breaks onto is indented to stay inside its item — an unindented "b." would leave
    the item and end the set.

    ``like`` is the question an answer belongs to. An answer marked without seeing it
    can letter parts the question numbered: nine items in the judged run answered
    "1. 2. 3." with "a. b. c.", all of them C0, leaving a learner to count.
    """
    letters = like is None or not marks_a_numbered_run(str(like or ""))
    prepared = under_supplied_number(str(text or "").strip(), letter_sub_steps=letters)
    first, *rest = prepared.split("\n")
    return "\n".join([first, *(f"   {line}" if line else "" for line in rest)])


def _candidate(sections: list[dict[str, Any]]) -> list[str]:
    """The pack as a rater reads it: the activities in place, the answers at the end.

    Placement is the renderer's job now that a practice item carries its own answer.
    While it was the model's, the answer sat under its own question in 9 of 12
    lesson/condition cells and the raters marked it down for defeating self-testing.
    """
    lines = ["## The revision pack\n"]
    answers: list[str] = []
    for section in sections:
        lines.append(f"### {section.get('title')}\n")
        for block in section.get("blocks") or []:
            if text := (block.get("text") or "").strip():
                lines.append(text + "\n")
            elif caption := (block.get("caption") or "").strip():
                label = block.get("figure_ref") or "figure"
                lines.append(f"*[{label}: {caption}]*\n")
        practice = section.get("practice") or []
        if not practice:
            continue
        lines.append("**Practice**\n")
        for index, item in enumerate(practice, start=1):
            lines.append(f"{index}. {_numbered_here(item.get('prompt'))}\n")
        answers.append(f"**{section.get('title')}**\n")
        for index, item in enumerate(practice, start=1):
            solution = (item.get("worked_solution") or "").strip()
            answers.append(
                f"{index}. {_numbered_here(item.get('answer'), like=item.get('prompt'))}\n"
            )
            if solution:
                answers.append(f"   {solution}\n")
    if answers:
        lines += ["## Check your work\n", *answers]
    return lines


def _rubric() -> list[str]:
    lines = ["## How to rate it\n", "Score each on 1-5, where 5 is best.\n"]
    for criterion in H1_RUBRIC:
        lines.append(
            f"- **{criterion['label']}** (`{criterion['criterion_id']}`) — "
            f"{criterion['description']}"
        )
    lines.append("")
    lines += [f"*{note}*" for note in H1_ALIGNMENT_GUIDANCE]
    return lines + [""]


def _worksheet_detail(cid: str, reference: LessonReference, sections: list[dict[str, Any]]) -> dict:
    """The blinded candidate as the WORKSHEET renderer takes it.

    The markdown packet shows LaTeX as source — a rater reads ``\\(P = 2\\times w\\)``
    where a learner would see typeset maths. C1 carries about a third more notation than
    C0 because it reuses her evaluation questions, so the cost of that fell on one arm
    (issue #164). Rendering the packet puts both arms on the page a learner would get,
    and on the same page the human raters will be given.
    """
    return {
        "packet_code": cid,
        "candidate_pack": {"manifest": {"steps": _manifest_steps(sections)}},
        "reference_sheet": reference_sheet(reference),
        "objectives": [{"objective_text": text} for text in reference.objectives],
        "rubric": list(H1_RUBRIC),
    }


def _manifest_steps(sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The generated pack in the shape the worksheet renderer reads."""
    steps = []
    for section in sections:
        blocks: list[dict[str, Any]] = []
        for block in section.get("blocks") or []:
            if text := (block.get("text") or "").strip():
                blocks.append({"type": "explanation", "content": text})
            elif block.get("block_type") == "visual":
                blocks.append(
                    {
                        "type": "visual",
                        "caption": (block.get("caption") or "").strip(),
                        "url": block.get("url"),
                        # Her drawings are TikZ, not images. Passing only the caption
                        # printed "slide the set square along the ruler" with nothing
                        # to slide, fourteen times on t3-w06.
                        "source_tikz": block.get("source_tikz"),
                    }
                )
        for item in section.get("practice") or []:
            answer = (item.get("answer") or "").strip()
            if solution := (item.get("worked_solution") or "").strip():
                answer = f"{answer}\n\n{solution}"
            prompt = (item.get("prompt") or "").strip()
            blocks.append({"type": "practice", "question": prompt, "answer": answer})
        steps.append(
            {"step_id": section.get("section_id"), "title": section.get("title"), "blocks": blocks}
        )
    return steps


def _reader_ready(sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    r"""The stored pack with the markup the model left off supplied.

    Generation does this now, but every pack in a run generated before it does not,
    and both judged runs are frozen. It also levels the packet: C0 and C1 wrote the
    undelimited commands and the note-carrying arms wrote almost none, so a reader of
    the raw markdown met ``4 \times side`` in one arm and typeset maths in another.
    Both surfaces are built from the value this returns, so the markdown a judge reads
    and the worksheet a rater reads say the same thing.
    """
    return [
        {
            **section,
            "blocks": [
                {**block, "text": reader_ready(block.get("text") or "")}
                for block in section.get("blocks") or []
            ],
            "practice": [
                {
                    **item,
                    **{key: reader_ready(item.get(key) or "") for key in WRITTEN_PRACTICE_FIELDS},
                }
                for item in section.get("practice") or []
            ],
        }
        for section in sections
    ]


def rating_protocol() -> dict[str, Any]:
    """What a judge pass was rated under, written into its header.

    A pass that records only its model can be compared with another only by
    assuming the packet was the same. This names the reference the packet carries
    and the guidance beside the rubric, so two passes either match or visibly do
    not.
    """
    return {
        "reference": "lesson_reference",
        "reference_carries_evaluation_questions": True,
        "guidance": list(H1_ALIGNMENT_GUIDANCE),
    }


def packet(cid: str, plan: dict[str, Any], sections: list[dict[str, Any]]) -> dict[str, Any]:
    """One blinded packet: the lesson as its teacher planned it, one pack, the rubric.

    The single place a packet's text is built, so that a pack rated by the in-code judge,
    a pack rated by a hand-dispatched one, and a pack screened in the harness bake-off are
    all rated on the same document.
    """
    ready = _reader_ready(sections)
    reference = lesson_reference(SessionPlanView.model_validate(plan))
    body = "\n".join(
        [
            f"# Rating packet {cid}\n",
            "A revision pack was produced for the lesson below. Judge the pack against",
            "the lesson, using the rubric at the end. Nothing here tells you how the pack",
            "was produced, and you should not speculate about it.\n",
        ]
        + _plan_reference(reference)
        + _candidate(ready)
        + _rubric()
    )
    return {
        "candidate_id": cid,
        "body": body,
        "detail": _worksheet_detail(cid, reference, ready),
    }


def build(run_label: str) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    run = json.loads((RUNS / run_label / "run.json").read_text())
    plans = {c["lesson"]: c["plan"] for c in json.loads(EVAL_SET_PATH.read_text())["cases"]}
    packets, key = [], []
    for case in run["cases"]:
        cid = candidate_id(run_label, case["lesson"], case["condition"], case["repeat"])
        sections = case["sections_json"]
        packets.append(packet(cid, plans[case["lesson"]], sections))
        reference = lesson_reference(SessionPlanView.model_validate(plans[case["lesson"]]))
        key.append(
            {
                "candidate_id": cid,
                "lesson": case["lesson"],
                "condition": case["condition"],
                "repeat": case["repeat"],
                # In the key, never the packet: a rater who knew reuse was measured
                # would rate it. The analysis reads it from here.
                "evaluation_overlap": overlap(list(reference.evaluation), sections).as_record(),
            }
        )
    return packets, key


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_label")
    args = parser.parse_args()

    packets, key = build(args.run_label)
    out = RUNS / args.run_label / "rating"
    (out / "packets").mkdir(parents=True, exist_ok=True)
    (out / "worksheets").mkdir(parents=True, exist_ok=True)
    for packet in packets:
        (out / "packets" / f"{packet['candidate_id']}.md").write_text(packet["body"])
        pdf = out / "worksheets" / f"{packet['candidate_id']}.pdf"
        pdf.write_bytes(render_h1_worksheet_html_pdf(packet["detail"]))
    # Kept OUT of the packet directory: reading it would unblind every candidate at once.
    (out / "_key.json").write_text(json.dumps(key, indent=2) + "\n")
    print(f"wrote {len(packets)} blinded packets -> {out / 'packets'}")
    print(f"rendered {len(packets)} worksheets -> {out / 'worksheets'}")
    print(f"de-anonymisation key -> {out / '_key.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
