"""Model contracts for writing review-pack sections.

dspy semantics: a child docstring replaces the parent's, fields append parent-first.

The shared signature keeps the generation instruction stable while product policy
controls which context fields are populated. Evidence-backed generation uses a
separate signature only because it genuinely adds an input field.
"""

from __future__ import annotations

import inspect
from functools import cache
from typing import Literal

import dspy
from pydantic.fields import FieldInfo

from app.domains.artefacts.core.domain.specification import ArtefactSpec
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    GenerationPolicyContext,
)
from app.domains.artefacts.types.post_class_review_pack.domain.generation_policy import (
    ContextPolicy,
    ReviewPackGenerationPolicy,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import DraftSection

from .lesson_context import lesson_plan_field_contract

#: Every context flag that puts a lesson-plan field in front of the model. Shared
#: mode renders one contract for all conditions, so it describes all of them.
_EVERY_PLAN_FLAG = (
    "include_entry_behaviour",
    "include_lesson_sequence",
    "include_materials",
    "include_student_tasks",
    "include_assessment_points",
    "include_step_title",
    "include_step_content",
    "include_teacher_student_activities",
    "include_instructional_events",
)

ContractMode = Literal["shared", "leveled"]
"""Which contract family a generator renders: one signature for every condition, or
one per level. A mode is selected by composition, not generation policy; every
mode presents the same task."""


class WriteSection(dspy.Signature):
    """Write one section of the artefact described in artefact_spec, for its audience.

    Everything you write speaks directly to that audience about the subject.
    Follow every requirement in artefact_spec and every rule in the policy
    exactly. Use ONLY the context given in the inputs: when source evidence is
    provided, ground every claim in it. The prose never mentions where any of
    it came from. Preserve the given lesson objective.
    """

    artefact_spec: ArtefactSpec = dspy.InputField(
        desc="What is being produced, for whom, under which requirements."
    )
    policy: GenerationPolicyContext = dspy.InputField(
        desc="The generation rules to follow exactly."
    )
    lesson_context: dict = dspy.InputField(
        desc="Subject, grade, topic, subtopic, and lesson objectives."
    )
    unit_context: dict = dspy.InputField(
        desc=(
            "What this section teaches: the lesson objective, how the lesson taught "
            "it and what it asked the learner to do, and the labels/captions of "
            "figures that will travel with the section."
        )
    )
    source_evidence: list[dict] = dspy.InputField(
        desc=(
            "What the teacher taught for this step, as she recorded it. May be "
            "empty — then do not cite any sources."
        )
    )
    section: DraftSection = dspy.OutputField(desc="The finished section, ready for its reader.")


# The shared-mode signature is one contract for every condition by definition, so it
# carries the codebook for every field any condition can deliver.
WriteSection.__doc__ = inspect.cleandoc(WriteSection.__doc__ or "") + lesson_plan_field_contract(
    ContextPolicy(generation_unit="lesson_step", **dict.fromkeys(_EVERY_PLAN_FLAG, True))
)


class WriteSectionFromSources(dspy.Signature):
    """Write one section after reading the permitted source documents with tools.

    The teaching source material is NOT in this prompt: use the tools to list
    the source documents and read them before writing anything. Ground every
    claim in what you actually read, and follow every requirement in
    artefact_spec and every rule in the policy exactly. The prose never
    mentions where any of it came from. Preserve the given lesson objective.
    """

    artefact_spec: ArtefactSpec = dspy.InputField()
    policy: GenerationPolicyContext = dspy.InputField()
    lesson_context: dict = dspy.InputField()
    unit_context: dict = dspy.InputField()
    section: DraftSection = dspy.OutputField(desc="The finished section, ready for its reader.")


class WriteObjectiveSection(dspy.Signature):
    """Write one revision-pack section teaching the given lesson objective.

    Write for the audience in artefact_spec, following its every requirement.
    Write your own reader-facing title and never copy a planning term into the
    section. Every practice question ends with its answer. Preserve the lesson
    objective exactly.
    """

    artefact_spec: ArtefactSpec = dspy.InputField(desc="The brief to follow exactly.")
    lesson_context: dict = dspy.InputField(desc="The lesson this section belongs to.")
    unit_context: dict = dspy.InputField(desc="What this section teaches.")
    section: DraftSection = dspy.OutputField(desc="The finished section, ready for its reader.")


class WriteGroundedSection(WriteObjectiveSection):
    """Write one revision-pack section teaching only what lesson_content contains.

    Nothing beyond lesson_content may be taught. Write for the audience in
    artefact_spec, following its every requirement. unit_context describes how
    the lesson taught this material: learn from it, never copy a planning term
    into the section. The prose never mentions where any of it came from. Figures ride
    along automatically — cite their fig-NN labels when useful, never their
    code. Every practice question ends with its answer. Preserve the lesson
    objective exactly.
    """

    lesson_content: list[dict] = dspy.InputField(
        desc="What this section may teach from — nothing beyond it."
    )


class WriteGroundedSectionFromSources(WriteObjectiveSection):
    """Write one revision-pack section teaching only what the lesson content says.

    The lesson content is not in this prompt: list the documents and read them
    before writing anything, and teach nothing they do not support. Write for
    the audience in artefact_spec, following its every requirement. unit_context
    describes how the lesson taught this material: learn from it, never copy a
    planning term into the section. The prose never mentions where any of it came from.
    Figures ride along automatically — cite their fig-NN labels when useful,
    never their code. Every practice question ends with its answer. Preserve
    the lesson objective exactly.
    """


def signature_for(policy: ReviewPackGenerationPolicy) -> type[dspy.Signature]:
    """The signature for this condition, carrying the codebook for its own fields.

    Built per policy rather than chosen from a pair. The codebook used to be
    appended to each class at import, so every condition — C0 included — was told
    what a lesson plan's fields are. A control briefed on the treatment's inputs
    is describing a plan it will never receive, and any edit to the codebook moved
    the baseline's prompt.

    ``cleandoc`` strips the COMMON indent, so appending flush-left text to a class
    docstring indented four spaces would leave the task text indented and the
    codebook not. Dedent first.
    """
    return _leveled_signature(policy.retrieval.enabled, policy.context)


@cache
def _leveled_signature(grounded: bool, context: ContextPolicy) -> type[dspy.Signature]:
    """One signature object per distinct condition, not one per call.

    Cached because callers compare signatures by identity and dspy keys its own
    work on the class. ``ContextPolicy`` is frozen, so it is a sound cache key:
    two conditions with the same context ARE the same contract.
    """
    base = WriteGroundedSection if grounded else WriteObjectiveSection
    instructions = inspect.cleandoc(base.__doc__ or "") + lesson_plan_field_contract(context)
    fields: dict[str, tuple[type, FieldInfo]] = {
        name: (field.annotation or str, field) for name, field in base.fields.items()
    }
    signature: type[dspy.Signature] = dspy.make_signature(
        fields, instructions, signature_name=base.__name__
    )
    return signature
