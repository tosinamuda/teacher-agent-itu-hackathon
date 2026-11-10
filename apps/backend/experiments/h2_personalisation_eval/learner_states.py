"""Objective-indexed learner state from marked constructed-response scripts.

The rule is the study's D-series decision, applied literally: what a learner knows is
identified from the SCRIPTS, never from the plan, and only objectives with evidence
get a state at all — the personaliser keeps the base section wherever the dict has no
entry, which is the designed fallback rather than an accident.

Mastery is a count over the questions the teacher actually marked ("unmarked" is
excluded from both sides of the fraction). Evidence carries the question, the attested
answer where one exists, and the learner's own final working, verbatim and flattened.
Misconceptions come ONLY from the frozen codes in the dataset XML — researcher-read per
incorrect response, before any generation — never from re-reading the working here. The
objective-level field carries the learner's dominant code; each evidence item carries
its own. The evidence schema is MCQ-shaped; its ``options`` dict is left empty and
drops out of the prompt as hollow.

Bands follow the production thresholds (learner_state.domain.models):
remediate < 0.50 <= reinforce < 0.75 <= extend.
"""

from __future__ import annotations

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    AnswerEvidenceItem,
    ObjectiveLearnerState,
)
from app.domains.learner_state.domain.models import humanise_misconception_code
from experiments.h2_personalisation_eval.students import Classwork, StudentScript

#: The most working the evidence field carries per question. Long chains flatten badly
#: and the final line is the answer the mark was given against.
_WORKING_CAP = 320


def _flatten(working: str) -> str:
    """The learner's working, on one line, truncated from the END if it must be.

    It used to keep the tail — ``"… " + text[-CAP:]`` — which for worked mathematics drops
    the method and keeps the answer. On `t3-w02` `student-01` Q7 that left the personaliser
    with none of the learner's four-term sum and 320 characters of the researcher's reading
    of it. The method is the evidence; the last line is the part already in `correct_option`.
    """
    lines = [" ".join(line.split()) for line in working.splitlines() if line.strip()]
    text = "  ".join(lines)
    return text if len(text) <= _WORKING_CAP else text[:_WORKING_CAP].rstrip() + " …"


def _named(code: str | None, why: str | None) -> str | None:
    """A misconception as a title AND what it means.

    ``humanise_misconception_code`` un-snake-cases a code and stops — its own docstring
    says "no description is authored anywhere upstream". One IS authored: every
    ``<misconception>`` in the dataset XML carries the researcher's reading as its text,
    which ``students.py`` parses and this module used to discard. The model was being handed
    "Re derives a given area" and left to infer what that meant.
    """
    if not code:
        return None
    title = humanise_misconception_code(code)
    return f"{title} — {why}" if why else title


def _band(correct: int, marked: int) -> str:
    share = correct / marked
    if share < 0.50:
        return "remediate"
    if share < 0.75:
        return "reinforce"
    return "extend"


def states_for(classwork: Classwork, student: StudentScript) -> dict[str, ObjectiveLearnerState]:
    """One state per objective the student has marked evidence for."""
    by_objective: dict[str, list] = {}
    for response in student.responses:
        question = classwork.questions[response.n]
        by_objective.setdefault(question.objective, []).append((question, response))

    states: dict[str, ObjectiveLearnerState] = {}
    for objective, pairs in by_objective.items():
        marked = [(q, r) for q, r in pairs if r.mark != "unmarked"]
        if not marked:
            continue
        correct = sum(1 for _, r in marked if r.mark == "correct")
        evidence = [
            AnswerEvidenceItem(
                question=q.text,
                options={},
                correct_option=q.answer or "",
                student_choice=_flatten(r.working) or "(no working captured)",
                chosen_option_misconception=_named(r.misconception_code, r.misconception_why),
            )
            for q, r in marked
            if r.mark == "incorrect"
        ]
        # The objective's one recorded misconception: the most frequent code across
        # this learner's incorrect responses, first-seen breaking ties. Frozen in the
        # dataset XML before generation; nothing downstream re-reads the ink.
        codes = [r.misconception_code for _, r in marked if r.misconception_code]
        dominant = max(dict.fromkeys(codes), key=codes.count) if codes else None
        why = next(
            (r.misconception_why for _, r in marked if r.misconception_code == dominant),
            None,
        )
        states[objective] = ObjectiveLearnerState(
            lesson_objective_id=objective,
            mastery_band=_band(correct, len(marked)),
            mastery=(
                f"{correct} of {len(marked)} marked classwork questions correct"
                + ("" if student.capture_complete else " (capture incomplete)")
            ),
            confidence=None,
            perceived_difficulty=None,
            misconception=_named(dominant, why),
            evidence_items=evidence,
        )
    return states
