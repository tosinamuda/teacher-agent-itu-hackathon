"""The inputs under test: canary-stamped lesson plans, and the profiles to run them under.

Generated plans always carry every canary class, so "the slice is absent"
always means the condition withheld it and never that the plan lacked it.
Profiles come in three flavours: the registered ones (what the study runs),
explicit edge profiles (flag boundaries a random draw reaches only by luck),
and arbitrary synthetic ones (breadth).
"""

from __future__ import annotations

import string
from typing import Any

from condition_canaries import (
    ASSESSMENT,
    ASSESSMENT_FIGURE,
    BLOCK_ASIDE,
    CORE_MINUTES,
    ENTRY_BEHAVIOUR,
    FIGURE,
    GLOBAL,
    MATERIAL,
    NON_CORE,
    NON_CORE_MINUTES,
    OBJECTIVE,
    PLAN_ASIDE,
    REFERENCE,
    STEP_CONTENT,
    STEP_ID,
    STEP_STRUCTURE,
    STEP_TITLE,
    STUDENT_ACTIVITY,
    STUDENT_TASK,
    TASK_ANSWER,
    TASK_HINT,
    TEACHER_ACTIVITY,
    WEEK_SENTINEL,
)
from hypothesis import strategies as st

from app.domains.artefacts.types.post_class_review_pack.application.request.base.builder import (
    BaseReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.personalised.builder import (  # noqa: E501
    PersonalisedReviewPackRequestBuilder,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    ObjectiveLearnerState,
    ReviewPackRequest,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.sources import (
    LessonSources,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import (
    ConditionProfile,
    ContextPolicy,
    RetrievalPolicy,
    condition_codes,
    h1_main_condition_codes,
    profile_for,
)
from app.shared.session_plan_view import SessionPlanView

MAX_OBJECTIVES = len(CORE_MINUTES)
MAX_CORE_STEPS = len(CORE_MINUTES)
MAX_NON_CORE_STEPS = len(NON_CORE_MINUTES)
MAX_REFERENCES = 5
MAX_MATERIALS = 2

# A core step may point at an objective the plan does not define; the unit is
# still built, with an empty objective text.
DANGLING_OBJECTIVE_ID = "obj-not-in-plan"

NON_CORE_KINDS = ("intro", "evaluation", "summary", "closure")


def h1_profiles() -> tuple[ConditionProfile, ...]:
    """C0-C3 — the H1 main comparison, taken from the registry."""
    return tuple(profile_for(Hypothesis.H1, code) for code in h1_main_condition_codes())


def all_profiles() -> tuple[ConditionProfile, ...]:
    """Every condition that builds its own request: C0-C3 plus P0/P1."""
    return h1_profiles() + tuple(
        profile_for(Hypothesis.H2, code) for code in condition_codes(Hypothesis.H2)
    )


def build_request(
    plan: SessionPlanView,
    profile: ConditionProfile,
    learner_states: dict[str, ObjectiveLearnerState] | None = None,
    builder: BaseReviewPackRequestBuilder | PersonalisedReviewPackRequestBuilder | None = None,
) -> ReviewPackRequest:
    """Build through the same builder entry point the runner uses for the hypothesis.

    ``builder`` is threadable so a test can reuse ONE instance across conditions,
    the way the service does.
    """
    if builder is None:
        builder = (
            BaseReviewPackRequestBuilder()
            if profile.hypothesis == Hypothesis.H1
            else PersonalisedReviewPackRequestBuilder()
        )
    if profile.hypothesis == Hypothesis.H1:
        assert isinstance(builder, BaseReviewPackRequestBuilder)
        return builder.build(
            session_plan=plan,
            policy=profile,
            sources=LessonSources.unresolved(plan.references),
        )
    assert isinstance(builder, PersonalisedReviewPackRequestBuilder)
    return builder.build(
        session_plan=plan,
        base_pack_id="PACK-CANARY",
        focal_learner_id="LEARNER-CANARY",
        learner_states=learner_states or {},
        policy=profile,
        sources=LessonSources.unresolved(plan.references),
    )


def _core_step(index: int, objective_id: str, suffix: str, activities: int) -> dict[str, Any]:
    return {
        "step_id": f"{STEP_ID}{index}{suffix}",
        "step_kind": "core",
        "lesson_objective_id": objective_id,
        "title": f"{STEP_TITLE}{index}{suffix}",
        "content": f"{STEP_CONTENT}{index}{suffix}",
        "instructional_type": f"{STEP_STRUCTURE}{index}{suffix}",
        "estimated_minutes": CORE_MINUTES[index],
        # Her note for this step: what scoped retrieval cites. Without it the
        # builder falls back to the block prose, which no condition may cite.
        "note": f"{REFERENCE}NOTE{index}{suffix}",
        "teacher_activities": [f"{TEACHER_ACTIVITY}{index}x{n}" for n in range(activities)],
        "student_activities": [f"{STUDENT_ACTIVITY}{index}x{n}" for n in range(activities)],
        "activities": [
            {"who": "teacher", "what": f"explains {TEACHER_ACTIVITY}{index}x{n}{suffix}"}
            for n in range(activities)
        ]
        + [
            # Reception, deliberately: this token stands for the half of the Student
            # Activity column that crosses to no condition. The other half — work she
            # set, which her Gagne coder reads as performance — travels as a task and
            # is covered in tests/test_step_delivery.py, where a step can be built
            # without the question block that would otherwise carry it.
            {"who": "student", "what": f"take notes on {STUDENT_ACTIVITY}{index}x{n}{suffix}"}
            for n in range(activities)
        ],
        "blocks": [
            {
                "id": f"blk{index}",
                "type": "visual",
                "url": f"https://cdn.example/{FIGURE}URL{index}{suffix}.png",
                "caption": f"{FIGURE}CAPTION{index}{suffix}",
                "source_record_id": f"rec-{index}",
                # Plan prose sitting beside the figure: the builder reads the
                # figure keys only, so this must never travel.
                "text": f"{BLOCK_ASIDE}FIG{index}{suffix}",
            },
            {
                "id": f"blk{index}b",
                "type": "explanation",
                "text": f"{BLOCK_ASIDE}TEXT{index}{suffix}",
            },
            # Her in-step Student Activity question — a task the plan sets.
            {
                "id": f"blk{index}task",
                "type": "practice",
                "question": f"{STUDENT_TASK}{index}{suffix}",
                "answer": f"{TASK_ANSWER}{index}{suffix}",
                "hints": [f"{TASK_HINT}{index}{suffix}"],
            },
        ],
    }


def _drawn_question() -> str:
    """A question's drawing, with the canary OUTSIDE any node.

    ``drawn_labels`` keeps node text when the source is stripped, so a token in a
    node would survive the strip and the gate would look open when it is shut.
    """
    return (
        "\n\n\\begin{tikzpicture}\n"
        f"  % {ASSESSMENT_FIGURE}\n"
        "  \\draw (0,0)--(4,0)--(4,3)--cycle;\n"
        "  \\node[below] at (2,0) {4cm};\n"
        "\\end{tikzpicture}\n"
    )


def _non_core_step(index: int, kind: str, suffix: str, owners: list[str]) -> dict[str, Any]:
    return {
        "step_id": f"{NON_CORE}STEPID{index}{suffix}",
        "step_kind": kind,
        "lesson_objective_id": "obj0",
        "title": f"{NON_CORE}TITLE{index}{suffix}",
        "content": f"{NON_CORE}BODY{index}{suffix}",
        "instructional_type": f"{NON_CORE}TYPE{index}{suffix}",
        "estimated_minutes": NON_CORE_MINUTES[index],
        "teacher_activities": [f"{NON_CORE}TACT{index}{suffix}"],
        "student_activities": [f"{NON_CORE}SACT{index}{suffix}"],
        "blocks": [
            # Her evaluation questions: plan content, one per objective assessed.
            # An unkeyed question is dropped, so each names its objective.
            *(
                {
                    "id": f"nc{index}q{n}",
                    "type": "practice",
                    # Every one carries a drawing: the canary is asserted per unit,
                    # and a unit whose question had none would read as a leak.
                    "question": f"{ASSESSMENT}{index}x{n}{suffix}" + _drawn_question(),
                    "lesson_objective_id": owner,
                }
                for n, owner in enumerate(dict.fromkeys(owners))
            ),
            {
                "id": f"nc{index}",
                "type": "visual",
                "url": f"https://cdn.example/{NON_CORE}FIGURL{index}{suffix}.png",
                "caption": f"{NON_CORE}CAPTION{index}{suffix}",
                "source_record_id": f"nc-rec-{index}",
            },
        ],
    }


def plan_payload(
    *,
    suffix: str,
    objective_count: int,
    core_owners: list[str],
    non_core_kinds: list[str],
    activities: int,
    references: int,
    materials: int,
) -> dict[str, Any]:
    """A raw session-plan payload in which every canary class is present."""
    steps = [
        _core_step(index, owner, suffix, activities) for index, owner in enumerate(core_owners)
    ]
    steps += [
        _non_core_step(index, kind, suffix, core_owners)
        for index, kind in enumerate(non_core_kinds)
    ]
    return {
        "subject": f"{GLOBAL}SUBJECT{suffix}",
        "grade": f"{GLOBAL}GRADE{suffix}",
        "topic": f"{GLOBAL}TOPIC{suffix}",
        "subtopic": f"{GLOBAL}SUBTOPIC{suffix}",
        "term": f"{GLOBAL}TERM{suffix}",
        "week": WEEK_SENTINEL,
        "theme": f"{GLOBAL}THEME{suffix}",
        "title": f"{PLAN_ASIDE}TITLE{suffix}",
        "track": f"{PLAN_ASIDE}TRACK{suffix}",
        "misconceptions": [f"{PLAN_ASIDE}MISCONCEPTION{suffix}"],
        "entry_behaviour": [f"{ENTRY_BEHAVIOUR}{suffix}"],
        "curriculum_objectives": [{"id": f"{PLAN_ASIDE}CURRICULUM{suffix}"}],
        # Dropped at the SessionPlanView boundary, while ContextPolicy still
        # declares a flag for it — the probe that keeps that gap visible.
        "assessments": [{"prompt": f"{ASSESSMENT}{suffix}"}],
        "lesson_plan_objectives": [
            {
                "lesson_objective_id": f"obj{index}",
                "objective_text": f"{OBJECTIVE}{index}{suffix}",
            }
            for index in range(objective_count)
        ],
        "instructional_materials": [f"{MATERIAL}{n}{suffix}" for n in range(materials)],
        "references": [f"{REFERENCE}{n}{suffix}" for n in range(references)],
        "steps": steps,
    }


@st.composite
def session_plans(draw: st.DrawFn) -> SessionPlanView:
    """Structurally valid plans that always carry every canary class."""
    suffix = draw(st.text(alphabet=string.ascii_lowercase, min_size=0, max_size=4))
    objective_count = draw(st.integers(1, MAX_OBJECTIVES))
    objective_ids = [f"obj{index}" for index in range(objective_count)]
    core_count = draw(st.integers(1, MAX_CORE_STEPS))
    core_owners = draw(
        st.lists(
            st.sampled_from([*objective_ids, DANGLING_OBJECTIVE_ID]),
            min_size=core_count,
            max_size=core_count,
        )
    )
    non_core_kinds = ["evaluation"] + draw(
        st.lists(st.sampled_from(NON_CORE_KINDS), max_size=MAX_NON_CORE_STEPS - 1)
    )
    payload = plan_payload(
        suffix=suffix,
        objective_count=objective_count,
        core_owners=core_owners,
        non_core_kinds=non_core_kinds,
        activities=draw(st.integers(1, 2)),
        references=draw(st.integers(1, MAX_REFERENCES)),
        materials=draw(st.integers(1, MAX_MATERIALS)),
    )
    payload["steps"] = draw(st.permutations(payload["steps"]))
    return SessionPlanView.model_validate(payload)


def example_plan() -> SessionPlanView:
    """A fixed fully-populated plan for the tests that need no generation."""
    return SessionPlanView.model_validate(
        plan_payload(
            suffix="",
            objective_count=2,
            core_owners=["obj0", "obj1"],
            non_core_kinds=["evaluation"],
            activities=2,
            references=2,
            materials=2,
        )
    )


_BOOL_CONTEXT_FIELDS = tuple(
    name for name, field in ContextPolicy.model_fields.items() if field.annotation is bool
)


def _synthetic(
    description: str, *, context: ContextPolicy, retrieval: RetrievalPolicy | None = None
) -> ConditionProfile:
    return ConditionProfile(
        hypothesis=Hypothesis.H1,
        condition_code=ConditionCode.C0,
        generated_by=ConditionCode.C0,
        description=description,
        context=context,
        retrieval=retrieval or RetrievalPolicy(),
    )


def _flags(**overrides: bool) -> dict[str, bool]:
    return {name: overrides.get(name, True) for name in _BOOL_CONTEXT_FIELDS}


# The flag boundaries a random draw reaches only by luck. Each one is a policy
# the registry does not contain but the builder must still obey.
EDGE_PROFILES: tuple[ConditionProfile, ...] = (
    _synthetic(
        "global lesson context withheld",
        context=ContextPolicy(
            generation_unit="lesson_step", **_flags(include_global_lesson_context=False)
        ),
    ),
    _synthetic(
        "lesson objectives withheld",
        context=ContextPolicy(
            generation_unit="lesson_step", **_flags(include_lesson_objectives=False)
        ),
    ),
    _synthetic(
        "every context slice withheld",
        context=ContextPolicy(
            generation_unit="lesson_step",
            **{name: False for name in _BOOL_CONTEXT_FIELDS},
        ),
    ),
    _synthetic(
        "retrieval on with a zero item cap",
        context=ContextPolicy(generation_unit="lesson_step", **_flags()),
        retrieval=RetrievalPolicy(
            enabled=True, evidence_scope="objective", max_evidence_items_per_unit=0
        ),
    ),
    _synthetic(
        "retrieval on with no evidence scope",
        context=ContextPolicy(generation_unit="lesson_step", **_flags()),
        retrieval=RetrievalPolicy(
            enabled=True, evidence_scope="none", max_evidence_items_per_unit=3
        ),
    ),
    _synthetic(
        "objective units with retrieval",
        context=ContextPolicy(generation_unit="objective", **_flags()),
        retrieval=RetrievalPolicy(
            enabled=True, evidence_scope="objective", max_evidence_items_per_unit=3
        ),
    ),
    _synthetic(
        # An objective unit has no note to be scoped to, so it falls back to the
        # plan's references — where the declared cap is literal and zero is zero.
        "objective units, retrieval on, zero item cap",
        context=ContextPolicy(generation_unit="objective", **_flags()),
        retrieval=RetrievalPolicy(
            enabled=True, evidence_scope="objective", max_evidence_items_per_unit=0
        ),
    ),
)


@st.composite
def condition_profiles(draw: st.DrawFn) -> ConditionProfile:
    """Arbitrary profiles, including flag combinations no registered condition uses.

    The registry sets several context flags the same way in every condition, so
    the real profiles alone cannot tell an enforced flag from an ignored one.
    These synthetic profiles can.
    """
    context = ContextPolicy(
        generation_unit=draw(st.sampled_from(("objective", "lesson_step"))),
        **{name: draw(st.booleans()) for name in _BOOL_CONTEXT_FIELDS},
    )
    retrieval = RetrievalPolicy(
        enabled=draw(st.booleans()),
        evidence_scope=draw(st.sampled_from(("none", "unit", "objective", "step"))),
        max_evidence_items_per_unit=draw(st.integers(0, MAX_REFERENCES + 1)),
        require_source_refs=draw(st.booleans()),
        use_only_provided_sources=draw(st.booleans()),
    )
    return ConditionProfile(
        hypothesis=Hypothesis.H1,
        condition_code=ConditionCode.C0,
        generated_by=ConditionCode.C0,
        description="synthetic",
        context=context,
        retrieval=retrieval,
    )
