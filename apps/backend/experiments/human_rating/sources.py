"""Where each material and each piece of evidence comes from.

The H1 materials are the frozen ladder run's packs, by lesson, condition and draw. The
H2 materials are the personalisation run's P0 and P1 packs for one learner, and the
learner's evidence is read from the same classwork record the personaliser read — the
dataset's XML, which holds identifiable work by minors and never leaves the
researcher's machine. Nothing this module returns is committed.
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.shared.llm_text import is_math_run, split_math_runs
from experiments.h1_condition_eval.dataset import EVAL_SET_PATH
from experiments.h1_condition_eval.rater_packets import _reader_ready
from experiments.h2_personalisation_eval.learner_states import _named, states_for
from experiments.h2_personalisation_eval.students import Classwork, StudentScript, load

H1_RUNS = Path(__file__).resolve().parents[1] / "h1_condition_eval" / "runs"
H2_RUNS = Path(__file__).resolve().parents[1] / "h2_personalisation_eval" / "runs"

Sections = list[dict[str, Any]]


def plans() -> dict[str, dict[str, Any]]:
    return {c["lesson"]: c["plan"] for c in json.loads(EVAL_SET_PATH.read_text())["cases"]}


#: Every TeX command that begins with ``n``. A ``\n`` followed by anything else is a JSON
#: escape the model or the transcription left inside a math run: ``reader_ready`` never
#: enters a run, which is right in general, but the escape makes the run invalid TeX and
#: pandoc gives up and prints it with its delimiters showing.
_TEX_N_COMMANDS = frozenset(
    """
    nabla natural ne nearrow neg negmedspace negthickspace negthinspace neq newline
    nexists ngeq ngtr ni nleftarrow nleftrightarrow nleq nless nmid nolimits nonumber
    normalsize not notin nparallel nprec nrightarrow nsim nsubseteq nsucc nsupseteq
    nu nwarrow
    """.split()
)
_BACKSLASH_N = re.compile(r"\\n([a-zA-Z]*)")


def _unescape_newline(match: re.Match[str]) -> str:
    """Keep a real command; turn anything else into the line break it stood for."""
    return match.group(0) if f"n{match.group(1)}" in _TEX_N_COMMANDS else f" {match.group(1)}"


#: A superscript written with no base, as in ``80 m$^{3}$``. The unit sits outside the
#: run, so the run renders as an empty box carrying an exponent.
_DANGLING_SCRIPT = re.compile(r"([A-Za-z0-9]+)\$([_^])\{([^}]*)\}\$")


def typesettable(text: str) -> str:
    """Maths a renderer can typeset, leaving everything outside a math run alone."""
    text = _DANGLING_SCRIPT.sub(
        lambda m: f"$\\text{{{m.group(1)}}}{m.group(2)}{{{m.group(3)}}}$", text
    )
    parts = []
    for part in split_math_runs(text):
        if is_math_run(part):
            part = re.sub(r"\s+", " ", _BACKSLASH_N.sub(_unescape_newline, part)).strip()
            if part.startswith("$") and not part.startswith("$$") and part.endswith("$"):
                # pandoc reads ``$x$`` but not ``$x $``: a closing dollar cannot follow a space.
                inner = part[1:-1].strip()
                part = f"${inner}$" if inner else ""
        parts.append(part)
    return "".join(parts)


def _typeset(section: dict[str, Any]) -> dict[str, Any]:
    return {
        **section,
        "title": typesettable(str(section.get("title") or "")),
        "blocks": [
            {**b, **{k: typesettable(str(b.get(k) or "")) for k in ("text", "caption")}}
            for b in section.get("blocks") or []
        ],
        "practice": [
            {
                **i,
                **{
                    k: typesettable(str(i.get(k) or ""))
                    for k in ("prompt", "answer", "worked_solution")
                },
            }
            for i in section.get("practice") or []
        ],
    }


def _sections(raw: Any) -> Sections:
    stored = ast.literal_eval(raw) if isinstance(raw, str) else raw
    return [_typeset(s) for s in _reader_ready(stored)]


class H1Run:
    """One ladder run's packs, addressable the way the mapping addresses them."""

    def __init__(self, label: str, runs_dir: Path = H1_RUNS) -> None:
        self.label = label
        record = json.loads((runs_dir / label / "run.json").read_text())
        self.arm = record["arm"]
        self._packs = {
            (c["lesson"], c["condition"], int(c["repeat"])): c["sections_json"]
            for c in record["cases"]
        }

    def pack(self, lesson: str, condition: str, version: int) -> Sections:
        try:
            return _sections(self._packs[(lesson, condition, version)])
        except KeyError:
            raise KeyError(
                f"{self.label} has no pack for {lesson} {condition} draw {version}"
            ) from None


@dataclass(frozen=True)
class Materials:
    p0: Sections
    p1: Sections
    outcomes: dict[str, str]
    """Per objective id, what personalisation did: ``personalised`` or ``no_learner_state``."""


class H2Run:
    """One personalisation run's P0 and P1 packs per learner."""

    def __init__(self, label: str, runs_dir: Path = H2_RUNS) -> None:
        self.label = label
        record = json.loads((runs_dir / label / "run.json").read_text())
        self.model = record.get("model")
        self.base = record.get("base")
        self._cases: dict[tuple[str, str, str], dict[str, Any]] = {
            (c["lesson"], c["student"], c["condition"]): c for c in record["cases"]
        }

    def learners(self) -> set[tuple[str, str]]:
        return {(lesson, student) for lesson, student, _ in self._cases}

    def materials(self, lesson: str, student: str) -> Materials:
        p0 = self._cases[(lesson, student, "P0")]
        p1 = self._cases[(lesson, student, "P1")]
        outcomes = {
            row["lesson_objective_id"]: row["outcome"] for row in (p1.get("personalisation") or [])
        }
        return Materials(
            p0=_sections(p0["sections"]), p1=_sections(p1["sections"]), outcomes=outcomes
        )


@dataclass(frozen=True)
class Response:
    question: str
    expected: str | None
    working: str
    result: str
    """``Correct``, ``Incorrect`` or ``Not marked``."""
    interpretation: str | None


@dataclass(frozen=True)
class ObjectiveEvidence:
    objective_id: str
    summary: str
    """"k of n marked classwork questions correct"."""
    band: str
    recorded_misconception: str | None
    responses: tuple[Response, ...]


_RESULT = {"correct": "Correct", "incorrect": "Incorrect", "unmarked": "Not marked"}
_OTHER_SCRIPT = re.compile(r"`?student-\d\d`?(?P<possessive>'s)?")


def _for_rater(reading: str | None) -> str | None:
    """The researcher's reading, with any other script it cites shown as "another student".

    A rater sees one student's class work and must not be able to identify any other.
    """
    if reading is None:
        return None
    return _OTHER_SCRIPT.sub(
        lambda m: "another student's" if m.group("possessive") else "another student", reading
    )


def learner_evidence(lesson: str, student: str) -> list[ObjectiveEvidence]:
    """The learner's classwork for every objective that carries evidence, in objective order.

    The band and the recorded misconception come from the same reading the personaliser
    acted on — ``states_for`` — so a rater judges P1 against the evidence P1 was given.
    Every marked response is shown, correct ones included: correct answers are evidence.
    """
    classwork = load(lesson)
    script = _script(classwork, student)
    states = states_for(classwork, script)
    out = []
    for objective_id, state in states.items():
        responses = tuple(
            Response(
                question=typesettable(classwork.questions[r.n].text),
                expected=typesettable(classwork.questions[r.n].answer or "") or None,
                working=typesettable(r.working),
                result=_RESULT[r.mark],
                interpretation=_for_rater(_named(r.misconception_code, r.misconception_why)),
            )
            for r in script.responses
            if classwork.questions[r.n].objective == objective_id
        )
        out.append(
            ObjectiveEvidence(
                objective_id=objective_id,
                summary=state.mastery.replace("classwork", "class work"),
                band=state.mastery_band,
                recorded_misconception=_for_rater(state.misconception),
                responses=responses,
            )
        )
    return out


def _script(classwork: Classwork, student: str) -> StudentScript:
    for script in classwork.students:
        if script.id == student:
            return script
    raise KeyError(f"{classwork.lesson} has no classwork for {student}")
