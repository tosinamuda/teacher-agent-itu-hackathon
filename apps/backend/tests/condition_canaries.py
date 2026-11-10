"""The leak map: which plan slice each condition may see, and how to detect it.

Every field-distinguishable slice of a lesson plan is stamped with a unique
token before the plan reaches the request builder (``condition_plan_inputs``
does the stamping), so "did this condition see that slice?" is a substring
search rather than an eyeball diff.

Each canary class names the ``ContextPolicy`` field that governs it and derives
its expectation from the ``ConditionProfile`` under test. Editing a profile
therefore re-points every expectation automatically, and adding a policy field
fails ``test_every_context_policy_field_has_a_canary_class`` until it is mapped
here — the profile cannot quietly stop describing the condition it configures.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Literal

from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ReviewPackRequest,
)
from app.domains.experiments.review_pack_study.conditions.profiles import ConditionProfile

# Canary token per plan slice. No token may contain another (pinned by a test),
# so a substring hit identifies exactly one class.
GLOBAL = "CNRYGLOBALCTX"
OBJECTIVE = "CNRYOBJECTIVE"
STEP_TITLE = "CNRYSTEPTITLE"
STEP_CONTENT = "CNRYSTEPBODY"
STEP_STRUCTURE = "CNRYINSTRTYPE"
TEACHER_ACTIVITY = "CNRYTEACHERACT"
STUDENT_ACTIVITY = "CNRYSTUDENTACT"
MATERIAL = "CNRYMATERIAL"
ASSESSMENT = "CNRYASSESSPOINT"
ASSESSMENT_FIGURE = "CNRYASSESSFIG"
REFERENCE = "CNRYREFERENCE"
FIGURE = "CNRYFIGURE"
BLOCK_ASIDE = "CNRYBLOCKASIDE"
NON_CORE = "CNRYNONCORE"
STEP_ID = "CNRYSTEPID"
# Gagne's coding vocabulary. Not canary tokens — these are the coder's own
# output, which is exactly what makes them detectable: a code reaches a unit only
# because the coder put it there.
INSTRUCTIONAL_EVENTS = (
    "stimulate_recall",
    "present_content",
    "provide_learning_guidance",
    "elicit_performance",
    "provide_feedback",
)
ENTRY_BEHAVIOUR = "CNRYENTRYBEH"
STUDENT_TASK = "CNRYSTUTASK"
TASK_ANSWER = "CNRYTASKANS"
TASK_HINT = "CNRYTASKHINT"
PLAN_ASIDE = "CNRYPLANASIDE"

# Integer slices cannot carry a text token, so they carry sentinel values that
# appear nowhere else in a generated plan.
WEEK_SENTINEL = 7201
CORE_MINUTES = (6101, 6102, 6103)
NON_CORE_MINUTES = (6301, 6302)

# The ContextPolicy fields that gate lesson-plan step prose. The H2
# personalisation path must carry none of these.
STEP_PROSE_GATES = frozenset(
    {
        "include_step_title",
        "include_step_content",
        "include_lesson_step_structure",
        "include_teacher_student_activities",
    }
)

Probe = Literal["request", "lesson_context"]


@dataclass(frozen=True)
class CanaryClass:
    """One field-distinguishable slice of the plan, and who is allowed to see it."""

    name: str
    needles: tuple[str, ...]
    allows: Callable[[ConditionProfile], bool]
    # The ContextPolicy field governing this slice, when a context flag governs it.
    gate: str | None = None
    probe: Probe = "request"
    # False for a slice the request carries but the prompt must not: record ids
    # travel for post-generation attachment and are stripped before rendering,
    # because packs have narrated "step-t3w09-03" straight into learner text.
    rendered: bool = True
    # True for a gate that DOES deliver, but a derived value rather than the
    # teacher's words, so no token can find it. Enforced on the field instead
    # (test_derived_slices_follow_their_gate) — declared here so the
    # undeliverable-gate check can tell "covered elsewhere" from "delivers
    # nothing", which it previously could not.
    derived: bool = False
    note: str = ""

    def expected(self, profile: ConditionProfile) -> bool:
        """Whether this slice must appear in the request the profile produces."""
        return self.allows(profile)

    def found_in(self, text: str) -> bool:
        """Whether any of this class's tokens appears in a serialised payload."""
        return any(needle in text for needle in self.needles)


def _never(profile: ConditionProfile) -> bool:
    del profile
    return False


def _generates_per_step(profile: ConditionProfile) -> bool:
    return profile.context.generation_unit == "lesson_step"


def _provides_evidence_items(profile: ConditionProfile) -> bool:
    """Whether any evidence reaches a unit under this policy.

    A step unit is handed its own note as a single item, so the per-unit cap
    does not decide whether evidence travels. An objective unit has no note to
    scope to and falls back to the plan's references, which the cap does govern.
    """
    if not profile.retrieval.provides_evidence:
        return False
    if _generates_per_step(profile):
        return True
    return profile.retrieval.max_evidence_items_per_unit > 0


def _provides_step_figures(profile: ConditionProfile) -> bool:
    # Figures ride the retrieval gate but are carried off lesson-plan steps, so
    # an objective-unit condition has nowhere to carry them from.
    return _generates_per_step(profile) and profile.retrieval.provides_evidence


def _carries_assessment_figures(profile: ConditionProfile) -> bool:
    # The drawing rides INSIDE the assessment question, so the question has to
    # travel before the figure can: both gates open, or neither delivers.
    return (
        _generates_per_step(profile)
        and profile.context.include_assessment_points
        and profile.context.include_assessment_figures
    )


def _carries_student_tasks(profile: ConditionProfile) -> bool:
    return _generates_per_step(profile) and profile.context.include_student_tasks


def _context_gated(
    name: str,
    needles: tuple[str, ...],
    gate: str,
    *,
    probe: Probe = "request",
    step_scoped: bool = False,
    note: str = "",
) -> CanaryClass:
    def allows(profile: ConditionProfile) -> bool:
        if step_scoped and not _generates_per_step(profile):
            return False
        return bool(getattr(profile.context, gate))

    return CanaryClass(
        name=name,
        needles=needles,
        allows=allows,
        gate=gate,
        probe=probe,
        note=note,
    )


_DERIVED_NOT_VERBATIM = (
    "This gate delivers a derived value, not the teacher's words: a step "
    "position, or a code from a closed vocabulary that the prompt's own schema "
    "already names whatever the values are. Neither can be found by searching "
    "for plan text, so both are covered by a field-level gate test instead — "
    "see test_derived_slices_follow_their_gate."
)

CANARY_CLASSES: tuple[CanaryClass, ...] = (
    _context_gated(
        "global_lesson_context",
        (GLOBAL, str(WEEK_SENTINEL)),
        "include_global_lesson_context",
    ),
    # The unit's own objective is the generation target under every condition,
    # so this class is judged on the shared lesson context alone.
    _context_gated(
        "lesson_objectives",
        (OBJECTIVE,),
        "include_lesson_objectives",
        probe="lesson_context",
    ),
    _context_gated("step_title", (STEP_TITLE,), "include_step_title", step_scoped=True),
    _context_gated("step_content", (STEP_CONTENT,), "include_step_content", step_scoped=True),
    _context_gated(
        "step_structure", (STEP_STRUCTURE,), "include_lesson_step_structure", step_scoped=True
    ),
    CanaryClass(
        name="step_timing",
        needles=tuple(str(value) for value in CORE_MINUTES),
        allows=_never,
        note=(
            "No gate, and none to add: per-step minutes are not a slice any "
            "condition may carry. Her plans allocate none, so a synthetic figure "
            "would be the derivation's own and would read as an instruction to be "
            "brief. Kept as a detector — the sentinels catch per-step minutes "
            "arriving by any route, including one added later."
        ),
    ),
    _context_gated(
        "teacher_activities",
        (TEACHER_ACTIVITY,),
        "include_teacher_student_activities",
        step_scoped=True,
    ),
    _context_gated(
        "student_activities",
        (STUDENT_ACTIVITY,),
        "include_teacher_student_activities",
        step_scoped=True,
    ),
    _context_gated("materials", (MATERIAL,), "include_materials"),
    _context_gated(
        "assessment_points",
        (ASSESSMENT,),
        "include_assessment_points",
        step_scoped=True,
        note="Attached per lesson-step unit; an objective unit has nowhere to carry them.",
    ),
    CanaryClass(
        name="assessment_figures",
        needles=(ASSESSMENT_FIGURE,),
        allows=_carries_assessment_figures,
        gate="include_assessment_figures",
        note=(
            "The drawing an assessment question depends on. Stripped, the question "
            "keeps its node labels and loses its geometry, which is not the same "
            "question — so this token sits outside any node and travels only with "
            "the whole source."
        ),
    ),
    _context_gated("entry_behaviour", (ENTRY_BEHAVIOUR,), "include_entry_behaviour"),
    CanaryClass(
        name="lesson_sequence",
        needles=(),
        allows=_never,
        gate="include_lesson_sequence",
        derived=True,
        note=_DERIVED_NOT_VERBATIM,
    ),
    CanaryClass(
        name="instructional_events",
        needles=(),
        allows=_never,
        gate="include_instructional_events",
        derived=True,
        note=_DERIVED_NOT_VERBATIM,
    ),
    CanaryClass(
        name="student_tasks",
        needles=(STUDENT_TASK,),
        allows=_carries_student_tasks,
        gate="include_student_tasks",
        note="Her in-step question, carried as a task the plan sets the learner.",
    ),
    CanaryClass(
        name="step_identity",
        needles=(STEP_ID,),
        allows=_generates_per_step,
        gate="generation_unit",
        rendered=False,
        note=(
            "The step id IS the unit's identity when the unit is a step — carried "
            "on the request for attachment, stripped before the model sees it."
        ),
    ),
    CanaryClass(name="source_evidence", needles=(REFERENCE,), allows=_provides_evidence_items),
    CanaryClass(name="grounded_figures", needles=(FIGURE,), allows=_provides_step_figures),
    CanaryClass(name="block_asides", needles=(BLOCK_ASIDE,), allows=_never),
    CanaryClass(
        name="non_core_steps",
        needles=(NON_CORE, *(str(value) for value in NON_CORE_MINUTES)),
        allows=_never,
    ),
    CanaryClass(
        name="task_answers",
        needles=(TASK_ANSWER, TASK_HINT),
        allows=_never,
        note=(
            "A task the plan sets the learner is plan evidence; the mathematics "
            "that answers it is not, and neither is the scaffolding toward it. "
            "Carrying either would put solved work into the condition defined "
            "as the plan without her note."
        ),
    ),
    CanaryClass(name="plan_asides", needles=(PLAN_ASIDE,), allows=_never),
)


def request_probe(request: ReviewPackRequest, probe: Probe) -> str:
    """The serialised slice of the request a canary class is judged on."""
    if probe == "lesson_context":
        return request.lesson_context.model_dump_json()
    return request.model_dump_json()


_FIELD_MARKER = re.compile(r"\[\[ ## (\w+) ## \]\]")


def field_block(values_message: str, name: str) -> str:
    """The rendered value block of one input field, from the values message."""
    parts = _FIELD_MARKER.split(values_message)
    blocks = dict(zip(parts[1::2], parts[2::2], strict=True))
    assert name in blocks, f"{name} is not a rendered input field; the probe would be vacuous"
    return blocks[name]


_OUTPUT_TRAILER = "Respond with the corresponding output fields"


def input_values(values_message: str) -> str:
    """Only the serialised INPUT values of a rendered prompt.

    Not the whole prompt: the instruction message carries the output JSON
    schema, which names every field of the model the call must return. What a
    call is asked to PRODUCE is a different question from what it was GIVEN, and
    conflating them makes an id-free input look like an id-carrying prompt.
    """
    parts = _FIELD_MARKER.split(values_message.split(_OUTPUT_TRAILER)[0])
    return "\n".join(parts[2::2])


def prompt_probes(messages: Sequence[str]) -> dict[Probe, str]:
    """Each probe's slice of one rendered prompt, given its messages as text.

    The per-field probe reads the LAST message: that is where the adapter puts
    the values, and the same markers appear in the instruction message as a
    description of the format.
    """
    return {
        "request": "\n".join(messages),
        "lesson_context": field_block(messages[-1], "lesson_context"),
    }


def assert_only_allowed(
    probes: dict[Probe, str], profile: ConditionProfile, where: str, *, rendered: bool = False
) -> None:
    """Every canary class present exactly when the profile allows it, and no other.

    ``rendered`` judges a prompt rather than a request, where record ids are
    stripped by design.
    """
    for canary in CANARY_CLASSES:
        present = canary.found_in(probes[canary.probe])
        expected = canary.expected(profile) and (canary.rendered or not rendered)
        verb = "leaked" if present else "is missing"
        assert present is expected, (
            f"{where} [{profile.condition_code.value}: {profile.description}] {verb} the "
            f"{canary.name!r} plan slice (gate={canary.gate}, tokens={canary.needles}). "
            f"context={profile.context.model_dump()} retrieval={profile.retrieval.model_dump()}. "
            f"{canary.note}"
        )
