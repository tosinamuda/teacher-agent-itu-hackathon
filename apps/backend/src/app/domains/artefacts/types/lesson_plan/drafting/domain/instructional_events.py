"""Code a lesson plan's Presentation activities as Gagné instructional events.

Gagné's Nine Events are the CODING VOCABULARY and nothing more. An event this teacher
did not plan is never added because the framework recommends it — that would stop
describing her lesson and start redesigning it. Four of the nine are therefore absent
here: nothing in the corpus licenses gain-attention, inform-objectives or
enhance-transfer, and assessment is carried structurally by the plan's Evaluation
questions rather than as a code, so the model is not told the same thing twice.

Rules, applied in this order:

1. One activity, at most one code — its dominant function. No double-coding.
2. Weak evidence takes no code. "Listen", "contribute", "ask questions" and "take notes"
   are reception.
3. Codes name FUNCTIONS, not actors. "They copy worked examples into their notes" states
   that the worked-example function operates in that step, so it codes as guidance; the
   actor named in the sentence does not decide the code. Where a verb means different
   things by actor — the teacher solving on the board is modelling, the learner solving
   is performance — ``who`` selects between them.
4. Consecutive duplicates collapse, after uncoded activities are dropped.

Prior knowledge stated in the plan's *Previous knowledge* field never licenses
``stimulate_recall``. Listing prerequisites is not planning a recall activity, and the
difference is signal: `t3-w04` plans one, `t3-w05` lists prerequisites and plans none.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Literal, cast

InstructionalEvent = Literal[
    "stimulate_recall",
    "present_content",
    "provide_learning_guidance",
    "elicit_performance",
    "provide_feedback",
]

# Ordered: the first rule that matches wins, so a rule naming the dominant function of an
# ambiguous phrase must precede the rules its other verbs would match. "Moves round to
# monitor their work, answer their questions, mark their notes and mark correction" is
# feedback, and would otherwise be caught by the learner-performance "answer".
_ACTOR_ANY = None

_RULES: tuple[tuple[str | None, str, InstructionalEvent], ...] = (
    (_ACTOR_ANY, r"previous knowledge|already been taught|recall", "stimulate_recall"),
    (_ACTOR_ANY, r"\bmarks?\b|marking|correct(s|ion|ing)?\b", "provide_feedback"),
    (_ACTOR_ANY, r"worked example", "provide_learning_guidance"),
    ("teacher", r"\bsolves?\b|demonstrat|works? (out|through)", "provide_learning_guidance"),
    (
        "teacher",
        r"explain|introduc|\bdraws?\b|\bwrites?\b|displa|\bshows?\b|present",
        "present_content",
    ),
    # A teacher putting questions to the class IS the eliciting function, so it is coded
    # even though the learner is not the grammatical subject. Teacher-only on purpose: a
    # student "asking questions where they do not understand" is seeking clarification,
    # which is reception. Follows the recall and feedback rules, so "asks … based on
    # their previous knowledge" and "answer their questions … mark correction" keep their
    # dominant codes.
    ("teacher", r"asks?\b|questions? such as", "elicit_performance"),
    (
        "student",
        r"\bsolves?\b|construct|identif|\banswers?\b|attempt|calculat|practis"
        r"|\bdraws?\b|respond|measur",
        "elicit_performance",
    ),
)

_COMPILED = tuple((who, re.compile(pattern, re.I), event) for who, pattern, event in _RULES)


def _field(activity: object, name: str) -> str:
    if isinstance(activity, Mapping):
        raw = cast(Mapping[str, object], activity).get(name)
    else:
        raw = getattr(activity, name, None)
    return str(raw or "")


def event_of(activity: object) -> InstructionalEvent | None:
    """The one instructional function an activity describes, or None if it describes none."""
    who, what = _field(activity, "who").strip().lower(), _field(activity, "what")
    if not what:
        return None
    for rule_who, pattern, event in _COMPILED:
        if rule_who in (None, who) and pattern.search(what):
            return event
    return None


def instructional_events(activities: Sequence[object]) -> list[InstructionalEvent]:
    """The step's instructional functions, in the order her plan runs them."""
    coded: list[InstructionalEvent] = []
    for activity in activities:
        event = event_of(activity)
        if event and (not coded or coded[-1] != event):
            coded.append(event)
    return coded
