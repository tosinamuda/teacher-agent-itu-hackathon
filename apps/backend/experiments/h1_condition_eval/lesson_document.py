"""Read a canonical lesson document: declared structure, external prose.

The document says what the lesson is made of. It does not contain her writing — the
note stays in ``notes-clean/``, one hand-edited file per step, and a ``<section>``
addresses a region of it by the heading the note itself carries. So every sentence she
wrote exists once, and a surface that wants the properties of a cylinder *selects* the
region instead of re-deriving it with a regex of its own.

Referential facts a grammar cannot see are checked here and are refusals, not warnings:
an objective reference that resolves to nothing, a note whose bytes have moved since
the structure was declared, a heading that is not in the file or is in it twice, a
declared figure label the region does not carry, and — the one that matters most — text
in the file that no section claims.

    uv run python -m experiments.h1_condition_eval.lesson_document validate lessons/t3-w05.xml
    uv run python -m experiments.h1_condition_eval.lesson_document reseal lessons/t3-w05.xml
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import Any

from lxml import etree

from app.domains.artefacts.types.lesson_plan.domain.lesson_document import violations

HERE = Path(__file__).parent


class LessonError(SystemExit):
    """A refusal to hand a surface a document that does not describe its own note."""


@dataclass(frozen=True)
class Section:
    """One region of a note file, addressed by the heading the note carries."""

    id: str
    role: str
    heading: str
    body: str
    figures: tuple[str | None, ...] = ()
    delivered: bool = True
    #: Her answer marker for a worked example, verbatim, or "" where she wrote none.
    solution: str = ""
    #: The enumerator her heading carries, verbatim, or "" where it carries none.
    enumerator: str = ""
    #: The one answer a worked example reaches, or "" where it reaches several.
    final_answer: str = ""


@dataclass(frozen=True)
class Activity:
    who: str
    what: str
    event: str | None = None
    sets_work: bool | None = None


@dataclass(frozen=True)
class Question:
    id: str
    text: str
    objective: str | None = None
    parts: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Step:
    id: str
    kind: str
    title: str
    prose: str
    minutes: int | None = None
    objective: str | None = None
    instructional_type: str | None = None
    activities: tuple[Activity, ...] = ()
    note_path: Path | None = None
    note_text: str = ""
    sections: tuple[Section, ...] = ()
    questions: tuple[Question, ...] = ()


@dataclass(frozen=True)
class Objective:
    id: str
    text: str
    curriculum: str
    kc_type: str | None = None


@dataclass(frozen=True)
class Lesson:
    id: str
    attrs: dict[str, str]
    curriculum: tuple[Objective, ...]
    objectives: tuple[Objective, ...]
    entry_behaviour: tuple[str, ...] = ()
    materials: tuple[str, ...] = ()
    references: tuple[str, ...] = ()
    steps: tuple[Step, ...] = field(default_factory=tuple)


def _text(element: etree._Element | None) -> str:
    return "" if element is None else "".join(map(str, element.itertext()))


def _child(root: etree._Element, tag: str) -> etree._Element:
    """A child the grammar requires, which ``_check`` has already confirmed."""
    found = root.find(tag)
    if found is None:
        raise ValueError(f"lesson document has no <{tag}>")
    return found


def _items(root: etree._Element, tag: str) -> tuple[str, ...]:
    holder = root.find(tag)
    return () if holder is None else tuple(_text(item) for item in holder.findall("item"))


def _flag(element: etree._Element, name: str) -> bool | None:
    raw = element.get(name)
    return None if raw is None else raw == "true"


def _heading_line(text: str, heading: str, where: str) -> tuple[int, int, int]:
    """Where her heading line for ``heading`` starts and ends, and how deep it is.

    Compared literally, line by line: a heading is her text with the hashes taken off,
    so there is nothing to escape and nothing a pattern could read differently. Exactly
    one match, or the address is ambiguous and the document is wrong — which is the
    whole reason to address by heading rather than by line number.
    """
    hits = []
    offset = 0
    for line in text.splitlines(keepends=True):
        bare = line.rstrip("\n")
        if bare.startswith("#") and bare.lstrip("#").strip() == heading:
            hits.append((offset, offset + len(bare), len(bare) - len(bare.lstrip("#"))))
        offset += len(line)
    if not hits:
        raise LessonError(f"{where}: the note has no heading {heading!r}")
    if len(hits) > 1:
        raise LessonError(
            f"{where}: heading {heading!r} occurs {len(hits)} times, so it addresses nothing"
        )
    return hits[0]


def _no_absorbed_sibling(body: str, level: int, heading: str | None, where: str) -> None:
    """A region may contain its own sub-headings; it may not swallow a sibling.

    Covering every character of the file is not enough on its own — dropping the middle
    section of three leaves the text in place, absorbed into the one above, and reads as
    a section that grew. A heading at the declared depth or shallower is another region,
    so it has to be declared as one.
    """
    for line in body.splitlines():
        if not line.startswith("#"):
            continue
        if len(line) - len(line.lstrip("#")) <= level:
            raise LessonError(
                f"{where}: {heading or 'the opening region'} swallows the heading "
                f"{line.lstrip('#').strip()!r}, which is a section of its own"
            )


def _regions(text: str, headings: list[str | None], where: str) -> list[str]:
    """Slice the note at the headings the document declares, in order.

    Declaration-driven, so an undeclared sub-heading stays inside its parent's body
    instead of silently becoming a region no one asked for. Every character of the
    file lands in exactly one region, and that is asserted, not assumed.
    """
    if any(h is None for h in headings[1:]):
        raise LessonError(f"{where}: only the first section may omit @heading")
    starts: list[int] = []
    ends: list[int] = []
    levels: list[int] = []
    cursor = 0
    for heading in headings:
        if heading is None:
            starts.append(0)
            ends.append(0)
            levels.append(0)
            continue
        start, end, level = _heading_line(text, heading, where)
        if start < cursor:
            raise LessonError(
                f"{where}: heading {heading!r} appears before the section declared above it"
            )
        cursor = end
        starts.append(start)
        ends.append(end)
        levels.append(level)
    bounds = starts[1:] + [len(text)]
    bodies = [text[end:stop] for end, stop in zip(ends, bounds, strict=True)]
    rebuilt = "".join(
        text[start:end] + body for start, end, body in zip(starts, ends, bodies, strict=True)
    )
    if rebuilt != text:
        missed = len(text) - len(rebuilt)
        raise LessonError(f"{where}: {missed} characters of the note are in no declared section")
    for body, level, heading in zip(bodies, levels, headings, strict=True):
        _no_absorbed_sibling(body, level, heading, where)
    return [body.strip() for body in bodies]


NOTE_HEADINGS = HERE / "note_headings.json"


@cache
def read_headings() -> dict[str, dict[str, Any]]:
    """Every heading in the corpus, read once and recorded — not matched.

    45 distinct headings over 47 heading lines. Three of them head work she set. The
    file says which, the way ``student_work.json`` says which activities set work: a
    reader's verdict, listed, where it can be disagreed with.
    """
    rows = json.loads(NOTE_HEADINGS.read_text())["headings"]
    return {row["heading"]: row for row in rows}


def heading_sets_work(heading: str) -> bool | None:
    """Whether her heading sets work — or None where no one has read this heading yet.

    None is not "no". A heading nobody has classified makes no proposal and refuses
    nothing; ``validate`` counts them so the unread ones stay visible.
    """
    row = read_headings().get(heading)
    return None if row is None else bool(row["sets_work"])


def _agrees_with_her_heading(element: etree._Element, section: Section, step_id: str) -> None:
    """Her heading proposes the role; a reader may overrule it, but not silently.

    This is the only check on a role that the role does not decide for itself. The
    measured one cannot be: ``role`` drives the projection, so declaring set work as
    explanation stops it reaching student_tasks and the measurement agrees with the
    mistake. Her heading is evidence she wrote, independent of anything declared here —
    the same standing the Gagne coder has against ``sets_work``, a proposal checked
    against the file rather than a verdict.
    """
    proposed = heading_sets_work(section.heading)
    if proposed is None or proposed == (section.role == "set-work"):
        return
    if element.get("role-note"):
        return
    said = "says it sets work" if proposed else "does not say it sets work"
    raise LessonError(
        f"{section.id}: her heading {section.heading!r} {said}, but the role is "
        f"{section.role!r}. Record why in role-note, or fix the role."
    )


def _declared_line(body: str, marker: str, where: str) -> None:
    """A declared marker must be one whole line of the region, once."""
    hits = [line for line in body.splitlines() if line.strip() == marker]
    if len(hits) != 1:
        raise LessonError(
            f"{where}: the region has {len(hits)} lines reading {marker!r}, so it marks nothing"
        )


def _figures_in_order(body: str, refs: tuple[str | None, ...], where: str) -> None:
    """Each declared label sits above the drawing it names, and every drawing is declared.

    Order is checked rather than assumed: ``note_figures`` pairs the i-th label with the
    i-th drawing across a whole note, which is right only while every region is either
    all-labelled or none-labelled. Here the pairing is what the document declares and
    this confirms her file agrees with it.
    """
    drawn = [
        index
        for index, line in enumerate(body.splitlines())
        if line.strip().startswith("\\begin{tikzpicture}")
    ]
    if len(drawn) != len(refs):
        raise LessonError(
            f"{where}: the region draws {len(drawn)} figure(s) and the document "
            f"declares {len(refs)}"
        )
    lines = body.splitlines()
    previous = -1
    for ref, drawing in zip(refs, drawn, strict=True):
        if ref is None:
            previous = drawing
            continue
        label = f"**{ref}.**"
        at = next(
            (i for i, line in enumerate(lines) if line.startswith(label) and i < drawing), None
        )
        if at is None:
            raise LessonError(f"{where}: {ref} is declared but no line above its drawing labels it")
        if at <= previous:
            raise LessonError(f"{where}: {ref} labels a drawing above the one it is declared for")
        previous = drawing


def _sections(note: etree._Element, step_id: str, text: str) -> tuple[Section, ...]:
    declared = note.findall("section")
    headings = [element.get("heading") for element in declared]
    bodies = _regions(text, headings, f"{step_id}")
    sections = []
    for element, body in zip(declared, bodies, strict=True):
        figures = tuple(figure.get("ref") for figure in element.findall("figure"))
        where = f"{step_id}:{element.get('id')}"
        _figures_in_order(body, figures, where)
        if solution := element.get("solution", ""):
            _declared_line(body, solution, where)
        if enumerator := element.get("enumerator", ""):
            heading = element.get("heading") or ""
            if not heading.startswith(enumerator):
                raise LessonError(
                    f"{where}: the heading does not start with the declared "
                    f"enumerator {enumerator!r}"
                )
        section = Section(
            id=where,
            role=element.get("role", ""),
            heading=element.get("heading") or "",
            body=body,
            figures=figures,
            delivered=_flag(element, "delivered") is not False,
            solution=solution,
            enumerator=enumerator,
            final_answer=element.get("final-answer", ""),
        )
        _agrees_with_her_heading(element, section, step_id)
        sections.append(section)
    return tuple(sections)


def _step(element: etree._Element, base: Path) -> Step:
    step_id = element.get("id", "")
    note = element.find("note")
    note_path: Path | None = None
    note_text = ""
    sections: tuple[Section, ...] = ()
    if note is not None:
        note_path = (base / (note.get("src") or "")).resolve()
        if not note_path.exists():
            raise LessonError(f"{step_id}: no note at {note_path}")
        note_text = note_path.read_text(encoding="utf-8")
        digest = hashlib.sha256(note_text.encode("utf-8")).hexdigest()
        if digest != note.get("sha256"):
            raise LessonError(
                f"{step_id}: {note_path.name} has changed since its structure was declared "
                f"({digest[:12]} now, {str(note.get('sha256'))[:12]} declared). "
                f"Re-read the sections, then `reseal`."
            )
        sections = _sections(note, step_id, note_text)
    holder = element.find("questions")
    questions = tuple(
        Question(
            id=f"{step_id}:{q.get('id')}",
            text=_text(q).strip() if not q.findall("part") else "",
            objective=q.get("objective"),
            parts=tuple((p.get("label", ""), _text(p).strip()) for p in q.findall("part")),
        )
        for q in (holder.findall("question") if holder is not None else [])
    )
    activities = element.find("activities")
    minutes = element.get("minutes")
    return Step(
        id=step_id,
        kind=element.get("kind", ""),
        title=element.get("title", ""),
        prose=_text(element.find("plan-content")).strip(),
        minutes=int(minutes) if minutes is not None else None,
        objective=element.get("objective"),
        instructional_type=element.get("instructional-type"),
        activities=tuple(
            Activity(
                who=a.get("who", ""),
                what=_text(a).strip(),
                event=a.get("event"),
                sets_work=_flag(a, "sets-work"),
            )
            for a in (activities.findall("activity") if activities is not None else [])
        ),
        note_path=note_path,
        note_text=note_text,
        sections=sections,
        questions=questions,
    )


def _check(tree: etree._ElementTree, path: Path) -> None:
    """The grammar and the references, as the app holds every lesson plan to them."""
    found = violations(tree.getroot())
    if found:
        raise LessonError(f"{path.name}: {'; '.join(found[:3])}")


def load(path: Path) -> Lesson:
    """The document, with every check the format promises already run."""
    tree = etree.parse(str(path))
    _check(tree, path)
    root = tree.getroot()
    lesson = Lesson(
        id=root.get("id", ""),
        attrs={str(key): str(value) for key, value in root.attrib.items()},
        curriculum=tuple(
            Objective(id=o.get("id", ""), text=_text(o).strip(), curriculum="")
            for o in _child(root, "curriculum").findall("objective")
        ),
        objectives=tuple(
            Objective(
                id=o.get("id", ""),
                text=_text(o).strip(),
                curriculum=o.get("curriculum", ""),
                kc_type=o.get("kc-type"),
            )
            for o in _child(root, "objectives").findall("objective")
        ),
        entry_behaviour=_items(root, "entry-behaviour"),
        materials=_items(root, "materials"),
        references=_items(root, "references"),
        steps=tuple(_step(element, path.parent) for element in root.findall("step")),
    )
    return lesson


def reseal(path: Path) -> int:
    """Re-record each note's digest after a deliberate hand edit of the note."""
    tree = etree.parse(str(path))
    changed = 0
    for note in tree.getroot().iter("note"):
        note_path = (path.parent / (note.get("src") or "")).resolve()
        digest = hashlib.sha256(note_path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
        if digest != note.get("sha256"):
            note.set("sha256", digest)
            changed += 1
    tree.write(str(path), encoding="utf-8", xml_declaration=True)
    print(f"resealed {changed} note reference(s) in {path.name}")
    return 0


def validate(path: Path) -> int:
    lesson = load(path)
    steps = len(lesson.steps)
    sections = sum(len(step.sections) for step in lesson.steps)
    chars = sum(len(step.note_text) for step in lesson.steps)
    figures = [ref for step in lesson.steps for s in step.sections for ref in s.figures]
    print(
        f"{path.name}: valid — {steps} steps, {len(lesson.objectives)} objectives, "
        f"{sections} note sections over {chars} characters of external prose"
    )
    unread = [
        s.heading
        for step in lesson.steps
        for s in step.sections
        if s.heading and heading_sets_work(s.heading) is None
    ]
    if unread:
        print(f"  {len(unread)} heading(s) nobody has read yet: {unread}")
    if uncaptioned := sum(1 for ref in figures if ref is None):
        print(
            f"  {uncaptioned} of {len(figures)} drawings carry no **fig-NN.** label, so "
            f"nothing can refer to them by name. Most already have a description above "
            f"them and need only the label; the fix is a hand edit to "
            f"notes-clean/{lesson.id}/."
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "reseal"))
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    path = args.path if args.path.is_absolute() else HERE / args.path
    return {"validate": validate, "reseal": reseal}[args.command](path)


if __name__ == "__main__":
    raise SystemExit(main())
