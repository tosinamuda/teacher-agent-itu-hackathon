"""The frozen H1 eval set: the field lesson plans C0-C3 generate from.

One case per lesson in the study set. The plans are built outside this repo by
``Dataset/build_session_plan.py`` from the transcribed teacher pages, so this module
only *pins* them — it copies each into ``eval_set.json`` with a content hash, and the
runner reads that copy. A plan edited upstream therefore does not silently change what
a past run was measured against; re-freezing is a deliberate act that shows up as a
changed hash.

    uv run python -m experiments.h1_condition_eval.dataset
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).parent
EVAL_SET_PATH = HERE / "eval_set.json"

THESIS = Path.home() / "Documents/Unilag/Masters/Thesis"

# `t3-w04` and `t3-w05` are both here and do not overlap. Her week-4 plan states four
# objectives and delivers two; the cleaning trims it to the two it delivers, and the two
# it does not — cylinders/spheres and volume — are `t3-w05`'s, which is where she taught
# them. Each lesson conditions on the objectives it actually delivered.
LESSONS: dict[str, Path] = {
    "t2-w09": THESIS / "Dataset/private/study-record/transcripts/t2-w09/session-plan.json",
    "t3-w02": THESIS / "Dataset/private/study-record/transcripts/t3-w02/session-plan.json",
    "t3-w04": THESIS / "Dataset/private/study-record/transcripts/t3-w04/session-plan.json",
    # Her week-5 Presentation and Note pages were captured in 2026-08 and supersede the
    # authored supplement this pointed at, whose Step I was written from Siyavula and
    # which carried no activities on either step.
    "t3-w05": THESIS / "Dataset/private/study-record/transcripts/t3-w05/session-plan.json",
    "t3-w06": THESIS / "Dataset/private/study-record/transcripts/t3-w06/session-plan.json",
    "t3-w09": THESIS / "Dataset/private/study-record/transcripts/t3-w09/session-plan.json",
}


def _case(lesson: str, source: Path, raw: str, plan: dict) -> dict:
    core = [step for step in plan["steps"] if step["step_kind"] == "core"]
    return {
        "lesson": lesson,
        "source_path": str(source),
        "plan_sha256": hashlib.sha256(raw.encode()).hexdigest()[:16],
        "objectives": len(plan["lesson_plan_objectives"]),
        "core_steps": len(core),
        "note_chars": sum(len(json.dumps(step.get("blocks") or [])) for step in core),
        "plan": plan,
    }


def from_transcripts() -> dict[str, list[dict]]:
    """The plans as ``build_session_plan.py`` wrote them, pinned by content hash."""
    cases = []
    for lesson, path in LESSONS.items():
        if not path.exists():
            raise SystemExit(f"{lesson}: no session plan at {path}")
        raw = path.read_text(encoding="utf-8")
        cases.append(_case(lesson, path, raw, json.loads(raw)))
    return {"cases": cases}


def from_documents() -> dict[str, list[dict]]:
    """The same plans projected from ``lessons/*.xml`` and the notes they reference.

    The switch this makes possible is not a judgement call, and that is the point of
    having it here. Every H1 request built from these plans is identical to the one
    built from the transcripts with ``clean_plan`` applied — which is what the runner
    actually feeds — and ``test_lesson_document`` asserts it for all six lessons across
    C0-C3. What re-freezing costs is a generation run, not a decision.
    """
    from experiments.h1_condition_eval.lesson_document import load
    from experiments.h1_condition_eval.lesson_plan_projection import plan as project

    baseline = _transcribed_notes()
    cases = []
    for lesson in LESSONS:
        path = HERE / "lessons" / f"{lesson}.xml"
        document = load(path)
        raw = path.read_text(encoding="utf-8") + "".join(step.note_text for step in document.steps)
        plan = project(document)
        _keep_the_baseline(lesson, plan, baseline)
        cases.append(_case(lesson, path, raw, plan))
    return {"cases": cases}


def _transcribed_notes() -> dict[tuple[str, str], str]:
    """Each step's note as the transcription wrote it, before any hand edit.

    Read from whichever copy still has it: the transcripts if they are on this machine,
    otherwise the notes already frozen here.
    """
    try:
        payload = from_transcripts()
    except SystemExit:
        payload = json.loads(EVAL_SET_PATH.read_text()) if EVAL_SET_PATH.exists() else {"cases": []}
    return {
        (case["lesson"], step["step_id"]): step.get("note_frozen") or step.get("note") or ""
        for case in payload["cases"]
        for step in case["plan"]["steps"]
    }


def _keep_the_baseline(lesson: str, plan: dict, baseline: dict[tuple[str, str], str]) -> None:
    """Carry the transcription forward as ``note_frozen``.

    Without this the switch silently disarms the additions guard. That guard digests
    every paragraph the generation copy ADDS to the transcription, and it is the only
    thing standing between a hand edit and words reaching the model undeclared — it
    caught all 21 figure captions the moment they went in. Freeze from the documents and
    ``note`` becomes the generation copy, so the comparison is a file against itself:
    39 visible additions drop to 0 and ten declarations go quiet.

    ``SessionPlanStepView`` ignores unknown keys, so this cannot reach a prompt.
    """
    for step in plan["steps"]:
        if step.get("note") is None:
            continue
        step["note_frozen"] = baseline.get((lesson, step["step_id"]), step["note"])


def freeze(*, documents: bool = False) -> dict[str, list[dict]]:
    return from_documents() if documents else from_transcripts()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from-documents",
        action="store_true",
        help="freeze from lessons/*.xml and notes-clean/ instead of the transcripts",
    )
    args = parser.parse_args()
    payload = freeze(documents=args.from_documents)
    EVAL_SET_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    where = "documents" if args.from_documents else "transcripts"
    print(f"froze {len(payload['cases'])} lessons from {where} -> {EVAL_SET_PATH}")
    for case in payload["cases"]:
        print(
            f"  {case['lesson']:8s} {case['objectives']} objectives, "
            f"{case['core_steps']} core steps, plan {case['plan_sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
