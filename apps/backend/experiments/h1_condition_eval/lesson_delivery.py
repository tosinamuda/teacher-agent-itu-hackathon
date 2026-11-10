"""Which conditions each region of her note reaches, declared and then measured.

A region's ``role`` says what it is. What it *reaches* follows in two steps, and neither
of them is written down twice:

1. The role names a **channel** — the request field the region travels on. That is a
   fact about her document and lives in the table below.
2. The channel is opened or closed by ``profiles.py``, which is the study's own source
   of truth for what a condition means. Conditions are resolved from the registry at
   call time, never hardcoded here — flip ``include_student_tasks`` there and this
   answers differently, as it should.

Then ``check`` measures: it builds the real request for every H1 condition and looks for
each region's own sentences in it.

**What that proves, exactly.** ``allowed`` is derived from the role and the policy;
``reached`` is what the builder emitted. So the check finds the builder disagreeing with
the policy — text arriving through a channel a flag was supposed to close, or missing
from one it opened. Two things it does NOT prove, both established by trying them:

- *Not* a mis-roled region. ``role`` drives the projection, so declaring set work as
  explanation stops it becoming a practice block, so it stops reaching ``student_tasks``,
  and the measurement agrees with the mistake. That circularity is why the role is
  cross-checked against her own heading in ``lesson_document``, which is evidence the
  document did not author.
- *Not* a redefinition of a condition. Hand C1 the retrieval policy and ``allowed`` moves
  with it, because ``profiles.py`` is the source of truth for what a condition means and
  this deliberately does not hold a second opinion.

It also only sees text, and only verbatim. A field that restates her note in the
narrator's words passes — which is what every core step's ``content`` in this corpus
actually does.

    uv run python -m experiments.h1_condition_eval.lesson_delivery check lessons/t3-w05.xml
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from pathlib import Path

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.experiments.domain.types import Hypothesis
from app.domains.experiments.review_pack_study.conditions.policies import ConditionProfile
from app.domains.experiments.review_pack_study.conditions.profiles import (
    h1_main_condition_codes,
    profile_for,
)
from app.shared.session_plan_view import SessionPlanView
from experiments.h1_condition_eval.lesson_document import Lesson, Section, load
from experiments.h1_condition_eval.lesson_plan_projection import plan

HERE = Path(__file__).parent

#: The request field a region of each role travels on. ``recall`` names a region she
#: wrote for herself to rehearse from; nothing carries it.
CHANNEL: dict[str, str | None] = {
    "recall": None,
    "explanation": "source_evidence",
    "worked-example": "source_evidence",
    "set-work": "student_tasks",
}

#: What opens each channel. Read off the policy rather than off a condition code, so
#: the answer tracks ``profiles.py`` instead of restating it.
_OPENS: dict[str, Callable[[ConditionProfile], bool]] = {
    # ``for_step`` gates on ``enabled`` and a scope in {objective, step, unit}, which is
    # every scope but "none" — the same predicate ``provides_evidence`` names.
    "source_evidence": lambda profile: profile.retrieval.provides_evidence,
    "student_tasks": lambda profile: profile.context.include_student_tasks,
}


def conditions_reaching(section: Section, step_kind: str) -> set[str]:
    """The conditions a region of this role, on a step of this kind, should reach.

    Step kind comes first and overrides everything: only core steps become generation
    units, so a region on an intro or evaluation step reaches nothing whatever its role
    — and under an evidence condition a core step's note travels WHOLE, so a ``recall``
    region on a core step would reach C2 despite carrying no channel of its own.
    """
    channel = CHANNEL[section.role]
    if step_kind != "core" or channel is None:
        return set()
    return {
        code.value
        for code in h1_main_condition_codes()
        if _OPENS[channel](profile_for(Hypothesis.H1, code))
    }


def _distinctive(body: str, note: str) -> str | None:
    """A line only this region carries, checked against the whole note rather than hoped.

    Notation is skipped so there is nothing to escape on either side of the comparison;
    what is returned is one of her own sentences, verified to occur once in the file it
    came from, so finding it in a request means that region's text is in that request.
    """
    flat = " ".join(note.split())
    candidates = [
        " ".join(line.split())
        for line in body.splitlines()
        if len(line.strip()) > 25 and "\\" not in line and "$" not in line
    ]
    unique = [line for line in candidates if flat.count(line) == 1]
    return max(unique, key=len) if unique else None


def _rendered(lesson: Lesson) -> dict[str, str]:
    """Every H1 condition's real request, flattened to one searchable string."""
    view = SessionPlanView.model_validate(plan(lesson))
    builder = BaseReviewPackRequestBuilder()
    sources = LessonSources.unresolved(view.references)
    return {
        code.value: " ".join(
            json.dumps(
                builder.build(
                    session_plan=view,
                    policy=profile_for(Hypothesis.H1, code).generation_policy(),
                    sources=sources,
                ).model_dump(mode="json"),
                ensure_ascii=False,
            ).split()
        )
        for code in h1_main_condition_codes()
    }


def measure(lesson: Lesson) -> list[tuple[Section, str, set[str], set[str]]]:
    """Per region: (section, step kind, what its role allows, where its words landed)."""
    rendered = _rendered(lesson)
    measured = []
    for step in lesson.steps:
        for section in step.sections:
            probe = _distinctive(section.body, step.note_text)
            if probe is None:
                continue
            measured.append(
                (
                    section,
                    step.kind,
                    conditions_reaching(section, step.kind),
                    {code for code, text in rendered.items() if probe in text},
                )
            )
    return measured


def check(path: Path) -> int:
    lesson = load(path)
    rows = measure(lesson)
    wrong = [row for row in rows if row[2] != row[3]]
    width = max(len(section.id) for section, *_ in rows)
    print(f"{'region':<{width}} {'role':<15} {'allowed':<14} reached")
    for section, _, allowed, reached in rows:
        mark = "" if allowed == reached else "   <-- MISMATCH"
        allow = ", ".join(sorted(allowed)) or "-"
        reach = ", ".join(sorted(reached)) or "-"
        print(f"{section.id:<{width}} {section.role:<15} {allow:<14} {reach}{mark}")
    if wrong:
        print()
        for section, kind, allowed, reached in wrong:
            print(
                f"{section.id}: role {section.role!r} on a {kind} step allows "
                f"{sorted(allowed) or 'nothing'}, "
                f"but its words reach {sorted(reached) or 'nothing'}"
            )
        return 1
    print(f"\n{len(rows)} regions, every one reaching exactly what its role allows")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check",))
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    path = args.path if args.path.is_absolute() else HERE / args.path
    return check(path)


if __name__ == "__main__":
    raise SystemExit(main())
