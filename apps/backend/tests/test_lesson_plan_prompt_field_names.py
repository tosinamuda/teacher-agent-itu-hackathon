"""The lesson-plan revision prompt must show the model clean field names only.

Verifies the ACTUAL text DSPy's ChatAdapter renders for the signature — not
just the pydantic schema in isolation. The two are different: the rendered
prompt includes every nested model's schema plus the signature docstring and
field descriptions, any of which can leak the canonical jargon keys
(kc_type / kc_focus / step_kind). The LM-facing aliases + the prose cleanup
must keep all of those out of the prompt.
"""

from __future__ import annotations

import dspy

from app.domains.artefacts.types.lesson_plan.drafting.infrastructure.dspy.signatures.lesson_plan_revision import (  # noqa: E501
    ReviseLessonPlanSignature,
)


def _rendered_prompt() -> str:
    messages = dspy.ChatAdapter().format(
        ReviseLessonPlanSignature,
        demos=[],
        inputs={
            "current_session_plan": {"plan_id": "LP-x"},
            "highlighted_part": "",
            "revision_instruction": "x",
            "conversation_summary": "",
            "prior_violations": [],
        },
    )
    return "\n\n".join(message["content"] for message in messages)


def test_prompt_uses_clean_names_not_canonical_jargon() -> None:
    prompt = _rendered_prompt()
    # Canonical storage keys are internal jargon — they must not reach the model,
    # neither as schema property names nor inside any description / docstring prose.
    assert "kc_type" not in prompt
    assert "kc_focus" not in prompt
    assert "step_kind" not in prompt
    # The clean LM-facing names are what the model is shown instead.
    assert "knowledge_type" in prompt
    assert "step_role" in prompt


def test_aliased_models_round_trip_clean_for_lm_canonical_for_storage() -> None:
    """The alias contract the LM-input builders rely on, in both directions.

    Input payloads are dumped by_alias=True so the model sees clean names; the
    same model dumped by field name (storage default) stays canonical. A bug in
    either direction reintroduces the input/output vocabulary mismatch that made
    the model waste a turn "repairing" field names.
    """
    from app.domains.artefacts.types.lesson_plan.drafting.schemas.session_plan import (
        PlanStep,
    )

    step = PlanStep.model_validate(
        {
            "step_id": "s1",
            "step_kind": "core",
            "kc_type": "concept",
            "lesson_objective_id": "lo1",
            "title": "T",
            "content": "C",
            "blocks": [{"id": "b1", "type": "explanation", "content": "x"}],
            "estimated_minutes": 5,
        }
    )
    lm_facing = step.model_dump(mode="json", by_alias=True)
    assert "knowledge_type" in lm_facing and "step_role" in lm_facing
    assert "kc_type" not in lm_facing and "step_kind" not in lm_facing

    stored = step.model_dump(mode="json")  # by_alias defaults False
    assert "kc_type" in stored and "step_kind" in stored
    assert "knowledge_type" not in stored and "step_role" not in stored
