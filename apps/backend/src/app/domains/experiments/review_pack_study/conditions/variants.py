"""Versioned variants of the lesson-plan context, derived from the frozen conditions.

``profiles.py`` is the study's frozen definition of C0–C4 and is never edited to
try something. A diagnostic that asks "would C1 have done better with field X"
needs a C1 that differs in X alone, with a name, so that a run can say which
definition it executed and a reader can tell two C1s apart.

A variant is a named derivation applied to every condition that carries the full
lesson-plan context. Applying it to all of them at once keeps the conditions a
ladder — C2 still contains C1, C3 still contains C2 — rather than revising one
rung and leaving the rest on the old definition.

``v3`` is the identity: the conditions exactly as frozen.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from app.domains.experiments.domain.types import ConditionCode

from .policies import ConditionProfile, ContextPolicy
from .profiles import H1_CONDITION_PROFILES

Derivation = Callable[[ContextPolicy], ContextPolicy]


def _as_frozen(context: ContextPolicy) -> ContextPolicy:
    return context


def _with_activities(context: ContextPolicy) -> ContextPolicy:
    """Her activity narration beside the event labels derived from it.

    The labels are the study's coding of what she wrote; on their own they carry
    the function of a step and none of its content. This sends the source with
    its annotation, so the model is not asked to reconstruct a lesson from its
    index.
    """
    return context.model_copy(update={"include_teacher_student_activities": True})


def _with_narration(context: ContextPolicy) -> ContextPolicy:
    """Her Presentation narration as she wrote it, unsplit by actor.

    ``activities`` is the same sentences parsed into who/what; this is the
    paragraph they came from. Measured against them it is 84% the same words,
    the rest being the connectives a parse drops — so it is sent for
    completeness of the plan as a document, not because it carries new content.
    """
    return context.model_copy(update={"include_step_content": True})


def _with_step_titles(context: ContextPolicy) -> ContextPolicy:
    """Her own heading for each step.

    Provenance-clean: the descriptor of 12 of the cohort's 17 core-step titles
    appears verbatim on her page. Two carry no descriptor at all ("Step 1"), and
    12 are half or more the objective's own words, so most of what this adds the
    unit already had under another name.
    """
    return context.model_copy(update={"include_step_title": True})


def _with_assessment_figures(context: ContextPolicy) -> ContextPolicy:
    """Carry her drawing with the assessment question that needs it.

    Stripped, t3-w02 item 8 reaches the model as "[the figure is not included
    here, marked 1cm, 5cm, 9cm]" — three of its four measurements and no trace of
    the semicircular arc. Every draw answers 15 cm; the figure gives 32.
    """
    return context.model_copy(update={"include_assessment_figures": True})


def _without_assessment(context: ContextPolicy) -> ContextPolicy:
    """The ablation: her evaluation questions withheld, the work she set kept.

    The rating reference carries those questions and a pack that reuses them
    can score as aligned for it. Taking them out of the input, and nothing else,
    is what separates "reuse earned the score" from "the richest plan made the
    best pack" — the two readings the overlap trigger could not tell apart.
    """
    return context.model_copy(update={"include_assessment_points": False})


@dataclass(frozen=True)
class Variant:
    """A named derivation from a parent, so each step is one field from the last."""

    parent: str | None
    derive: Derivation


CONTEXT_VARIANTS: dict[str, Variant] = {
    "v3": Variant(None, _as_frozen),
    "v4-activities": Variant("v3", _with_activities),
    "v4-activities-no-assessment": Variant("v4-activities", _without_assessment),
    "v5-narration": Variant("v4-activities", _with_narration),
    "v6-assessment-figures": Variant("v4-activities", _with_assessment_figures),
    "v5-narration-titles": Variant("v5-narration", _with_step_titles),
    # Everything her plan holds that the frozen definition withholds. The end of the
    # chain, so each step above it stays separately measurable.
    "v7-full": Variant("v5-narration-titles", _with_assessment_figures),
}

FROZEN_VARIANT = "v3"


def derivation_chain(name: str) -> list[Derivation]:
    """Every derivation from the frozen root down to ``name``, in order."""
    chain: list[Derivation] = []
    current: str | None = name
    while current is not None:
        try:
            variant = CONTEXT_VARIANTS[current]
        except KeyError:
            raise ValueError(
                f"unknown context variant {current!r}; known: {sorted(CONTEXT_VARIANTS)}"
            ) from None
        chain.append(variant.derive)
        current = variant.parent
    return list(reversed(chain))


_CARRIES_LESSON_PLAN = frozenset(
    {ConditionCode.C1, ConditionCode.C2, ConditionCode.C3, ConditionCode.C4}
)


def profiles_for_variant(name: str) -> dict[ConditionCode, ConditionProfile]:
    """Every H1 profile, with the variant applied to each lesson-plan condition.

    C0 passes through untouched under every variant: it carries no lesson plan,
    so there is nothing for a context variant to change, and a run that compares
    a variant C1 against C0 must be comparing against the same C0.
    """
    chain = derivation_chain(name)
    if name == FROZEN_VARIANT:
        return dict(H1_CONDITION_PROFILES)
    out: dict[ConditionCode, ConditionProfile] = {}
    for code, profile in H1_CONDITION_PROFILES.items():
        if code in _CARRIES_LESSON_PLAN:
            context = profile.context
            for derive in chain:
                context = derive(context)
            profile = profile.model_copy(
                update={
                    "context": context,
                    "description": f"{profile.description} [context {name}]",
                }
            )
        out[code] = profile
    return out
