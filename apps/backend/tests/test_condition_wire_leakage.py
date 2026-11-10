"""The leak map, judged on what the pipeline actually sends.

Every other leakage suite renders the prompt itself — it calls the same input
mappers production calls and formats them with its own ChatAdapter. That leaves
one link untested, the `acall` argument list, and it is the link that decides
what goes on the wire. The gap is not theoretical: a jargon check assembled its
own inputs, passed for months, and C0 was being handed the fields it is denied
the entire time.

Here the LM is replaced instead of the prompt (``recording_lm``), so the real
generator, personaliser and repair pass run end to end and the assertions read
the bytes they sent. Substituting a mapper argument, dropping a prune, or
adding an input at the call site all fail here and nowhere else.
"""

from __future__ import annotations

import asyncio
import json
from typing import get_args

import pytest
from condition_canaries import (
    CANARY_CLASSES,
    STEP_PROSE_GATES,
    assert_only_allowed,
    field_block,
    input_values,
    prompt_probes,
)
from condition_plan_inputs import EDGE_PROFILES, build_request, example_plan, h1_profiles
from recording_lm import RecordingLM, completion

from app.domains.artefacts.types.post_class_review_pack.application.prompt_provenance import (  # noqa: E501
    capture_prompt_provenance,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    AnswerEvidenceItem,
    ObjectiveLearnerState,
    ReviewPackRequest,
    SessionSignals,
)
from app.domains.artefacts.types.post_class_review_pack.domain.section.schemas import (
    AuthoredBlockType,
    DraftBlock,
    DraftPractice,
    DraftSection,
    ReviewPackBlock,
    ReviewPackPracticeItem,
    ReviewPackSection,
    RevisedSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    ContractMode,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.generate_section import (  # noqa: E501
    GenerateSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.personalise_section import (  # noqa: E501
    PersonaliseSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prompt_projection import (  # noqa: E501
    RECORD_KEYS,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.repair_section import (
    RepairGeneratedSection,
)
from app.domains.experiments.domain.types import ConditionCode, Hypothesis
from app.domains.experiments.review_pack_study.conditions.profiles import (
    ConditionProfile,
    profile_for,
)
from app.shared.session_plan_view import SessionPlanView

P1_PROFILE = profile_for(Hypothesis.H2, ConditionCode.P1)

# Every model the LM fills. None may declare a record key: what the model is
# never asked for, it cannot get wrong, and cannot be echoed back into a pack.
AUTHORED_MODELS = (DraftSection, RevisedSection, DraftBlock, DraftPractice)


def _draft() -> DraftSection:
    return DraftSection(
        title="Working with the objective",
        instructional_support="Multiply the two side lengths.",
        worked_examples=[DraftBlock(block_type="worked_example", text="3 x 4 = 12")],
        practice=[DraftPractice(prompt="Find the area of a 5 by 2 rectangle.", answer="10")],
    )


def _revision() -> RevisedSection:
    """What repair and personalisation return: prose and practice, no identity."""
    return RevisedSection(
        title="Working with the objective",
        blocks=[DraftBlock(block_type="explanation", text="Multiply the two side lengths.")],
        practice=[DraftPractice(prompt="Find the area.", answer="10")],
    )


def _base_section(objective_id: str) -> ReviewPackSection:
    """An approved base section carrying no canary — only the unit can leak one.

    Refs sit in ``source_refs`` and the text is clean prose: that is the shape a
    stored pack comes back in, since ``review_pack_manifest_to_sections`` lifts
    the rendered "_Sources:" trailer back into the structured field.
    """
    return ReviewPackSection(
        section_id="step:approved-base",
        title="Working with the objective",
        lesson_objective_id=objective_id,
        blocks=[
            ReviewPackBlock(
                block_id="step:approved-base:b0",
                block_type="explanation",
                text="Multiply the two side lengths.",
                lesson_objective_id=objective_id,
                source_refs=["REF-1"],
            )
        ],
        practice=[
            ReviewPackPracticeItem(item_id="step:approved-base:p0", prompt="Find it.", answer="10")
        ],
        source_refs=["REF-1"],
    )


def _learner_state(objective_id: str) -> ObjectiveLearnerState:
    return ObjectiveLearnerState(
        lesson_objective_id=objective_id,
        mastery_band="remediate",
        mastery="0 of 2 diagnostic questions correct",
        confidence="a little sure (2/5)",
        evidence_items=[
            AnswerEvidenceItem(
                question="Which is a common multiple of 2 and 3?",
                options={"B": "9", "C": "6"},
                correct_option="C",
                student_choice="B",
            )
        ],
    )


def _generate(profile: ConditionProfile) -> tuple[RecordingLM, ReviewPackRequest]:
    """One real generation per unit, answered by the recorder."""
    request = build_request(example_plan(), profile)
    lm = RecordingLM(*(completion(section=_draft()) for _ in request.units))
    generator = GenerateSection(lm=lm)

    async def generate_all() -> list[ReviewPackSection]:
        return list(
            await asyncio.gather(
                *(generator.generate_section(request=request, unit=unit) for unit in request.units)
            )
        )

    sections = asyncio.run(generate_all())
    assert len(lm.sent) == len(request.units) == len(sections)
    return lm, request


@pytest.mark.parametrize(
    "profile", [*h1_profiles(), *EDGE_PROFILES], ids=lambda p: p.description[:44]
)
def test_the_generator_sends_exactly_the_slices_the_profile_allows(
    profile: ConditionProfile,
) -> None:
    """The original question, asked of the wire rather than of a mapper."""
    lm, _ = _generate(profile)
    for index, messages in enumerate(lm.messages_per_call):
        assert_only_allowed(
            prompt_probes(messages), profile, f"generate call {index}", rendered=True
        )


@pytest.mark.parametrize("profile", h1_profiles(), ids=lambda p: p.condition_code.value)
def test_each_call_is_sent_one_units_context_and_no_other_units(
    profile: ConditionProfile,
) -> None:
    """A section is grounded in ITS step's note — the leak map cannot see otherwise.

    Every unit of one plan carries the same canary CLASSES, so handing unit B's
    note to unit A satisfies the whole class-level map while grounding a section
    in teaching it was not written from. Per-unit tokens are distinct, so this
    asks the sharper question.

    Every expectation comes from the REQUEST. Deriving it from a second run of
    the generator reads far better and catches nothing: the comparison run
    carries the same mutation, so both sides move together and a note sent to
    every unit matches a note sent to every unit.
    """
    lm, request = _generate(profile)
    assert len(request.units) > 1, "one unit cannot be confused with another"

    def _calls_carrying(needle: str, field: str) -> list[int]:
        return [
            index
            for index, messages in enumerate(lm.messages_per_call)
            if needle in field_block(messages[-1], field)
        ]

    for unit in request.units:
        carrying = _calls_carrying(unit.objective_text, "unit_context")
        assert len(carrying) == 1, (
            f"{unit.unit_id}'s objective reached {len(carrying)} of {len(lm.sent)} calls"
        )
        for item in unit.source_evidence:
            carrying = _calls_carrying(item.excerpt, "source_evidence")
            assert len(carrying) == 1, (
                f"{unit.unit_id}'s note reached {len(carrying)} of {len(lm.sent)} calls — "
                "a section grounded in teaching it was not written from"
            )

    grounded = any(unit.source_evidence for unit in request.units)
    assert grounded is profile.retrieval.provides_evidence, (
        "the evidence half of this test is vacuous unless the profile delivers evidence"
    )


@pytest.mark.parametrize("profile", h1_profiles(), ids=lambda p: p.condition_code.value)
def test_the_leveled_signature_arm_sends_exactly_the_slices_the_profile_allows(
    profile: ConditionProfile,
) -> None:
    """The other generation arm, which no leakage test reached.

    ``contract_mode="leveled"`` swaps the shared signature for a per-level one
    and swaps the input mapper with it — different fields, evidence under a
    different name. It is an arm of the published output-channel comparison, so
    a leak in it is a leak in a reported result.
    """
    request = build_request(example_plan(), profile)
    lm = RecordingLM(*(completion(section=_draft()) for _ in request.units))
    generator = GenerateSection(lm=lm, contract_mode="leveled")

    async def generate_all() -> None:
        await asyncio.gather(
            *(generator.generate_section(request=request, unit=unit) for unit in request.units)
        )

    asyncio.run(generate_all())

    assert len(lm.sent) == len(request.units), "the leveled dispatch did not run"
    for index, messages in enumerate(lm.messages_per_call):
        assert_only_allowed(
            prompt_probes(messages), profile, f"leveled call {index}", rendered=True
        )


def test_a_grounded_level_refuses_to_render_without_the_evidence_it_teaches_from() -> None:
    """Two readings of the retrieval policy must agree, or nothing may be sent.

    ``signature_for`` picks the grounded contract from ``retrieval.enabled``; the
    request builder fills evidence under ``provides_evidence`` and the evidence
    scope. Disagreeing would tell the model to teach nothing beyond
    ``lesson_content`` and hand it none — an ungrounded section inside the
    evidence arm, which reads back as a weak C2 rather than a broken one.
    """
    request = build_request(example_plan(), profile_for(Hypothesis.H1, ConditionCode.C2))
    stripped = request.model_copy(
        update={
            "units": [unit.model_copy(update={"source_evidence": []}) for unit in request.units]
        }
    )
    lm = RecordingLM(completion(section=_draft()))
    generator = GenerateSection(lm=lm, contract_mode="leveled")

    with pytest.raises(ValueError, match="teaches only from lesson_content"):
        asyncio.run(generator.generate_section(request=stripped, unit=stripped.units[0]))

    assert lm.sent == [], "the ungrounded call reached the wire before it was refused"
    # Positive control: the same call is sent once the evidence is there.
    asyncio.run(generator.generate_section(request=request, unit=request.units[0]))
    assert len(lm.sent) == 1


@pytest.mark.parametrize(
    ("mode", "expected"),
    [
        (
            "shared",
            {
                ConditionCode.C0: "base_generation",
                ConditionCode.C1: "base_generation",
                ConditionCode.C2: "base_generation",
                ConditionCode.C3: "base_generation",
            },
        ),
        (
            "leveled",
            {
                ConditionCode.C0: "base_generation.WriteObjectiveSection",
                ConditionCode.C1: "base_generation.WriteObjectiveSection",
                ConditionCode.C2: "base_generation.WriteGroundedSection",
                ConditionCode.C3: "base_generation.WriteGroundedSection",
            },
        ),
    ],
)
def test_which_signature_each_condition_sends(
    mode: ContractMode,
    expected: dict[ConditionCode, str],
) -> None:
    """The table in docs/generation-call-stack.md, pinned at the call boundary.

    Production runs ``shared``, where all four conditions send one signature and a
    condition changes only the values in it — so the fingerprints are identical too.
    """
    recorded: dict[ConditionCode, dict[str, str]] = {}
    for code in expected:
        request = build_request(example_plan(), profile_for(Hypothesis.H1, code))
        lm = RecordingLM(completion(section=_draft()))
        generator = GenerateSection(lm=lm, contract_mode=mode)
        with capture_prompt_provenance() as trace:
            asyncio.run(generator.generate_section(request=request, unit=request.units[0]))
        recorded[code] = trace.snapshot().components

    assert {code: next(iter(components)) for code, components in recorded.items()} == expected
    fingerprints = {code: next(iter(components.values())) for code, components in recorded.items()}
    if mode == "shared":
        assert len(set(fingerprints.values())) == 1
    else:
        # Under `leveled` a signature carries the codebook for its OWN fields, so
        # the prompt fingerprint separates conditions that differ in what they are
        # given — C0 receives no lesson plan and is told about none. The signature
        # NAME still groups by evidence level, which is what the table above pins.
        assert fingerprints[ConditionCode.C1] != fingerprints[ConditionCode.C2]
        assert fingerprints[ConditionCode.C0] != fingerprints[ConditionCode.C1]
        assert fingerprints[ConditionCode.C2] == fingerprints[ConditionCode.C3]


def test_the_contract_mode_actually_selects_a_different_prompt() -> None:
    """Otherwise the arm above would pass by generating the shared prompt twice."""
    request = build_request(example_plan(), profile_for(Hypothesis.H1, ConditionCode.C2))
    prompts = {}
    for mode in ("shared", "leveled"):
        lm = RecordingLM(completion(section=_draft()))
        generator = GenerateSection(lm=lm, contract_mode=mode)
        asyncio.run(generator.generate_section(request=request, unit=request.units[0]))
        prompts[mode] = lm.prompt(0)
    assert prompts["shared"] != prompts["leveled"]


@pytest.mark.parametrize("profile", h1_profiles(), ids=lambda p: p.condition_code.value)
def test_the_repair_call_sends_exactly_the_slices_the_profile_allows(
    profile: ConditionProfile,
) -> None:
    """Repair re-opens the context, so it can leak everything generation can."""
    request = build_request(example_plan(), profile)
    unit = request.units[0]
    lm = RecordingLM(completion(repaired_section=_revision()))
    generator = RepairGeneratedSection(lm=lm)
    asyncio.run(
        generator.repair_section(
            request=request,
            unit=unit,
            failed_section=_base_section(unit.lesson_objective_id),
            issues=["scope_compliance: out of scope"],
        )
    )
    assert_only_allowed(prompt_probes(lm.messages(0)), profile, "repair", rendered=True)


def _personalise() -> tuple[RecordingLM, ReviewPackSection, ReviewPackRequest]:
    plan = example_plan()
    request = build_request(plan, P1_PROFILE)
    unit = request.units[0]
    base = _base_section(unit.lesson_objective_id)
    request = request.model_copy(
        update={"session_signals": SessionSignals(interest="interested (4/5)")}
    )
    lm = RecordingLM(completion(personalised_section=_revision()))
    personalised = asyncio.run(
        PersonaliseSection(lm=lm).personalise_section(
            request=request,
            unit=unit,
            base_section=base,
            learner_state=_learner_state(unit.lesson_objective_id),
        )
    )
    return lm, personalised, request


def test_p1_is_sent_no_lesson_plan_step_prose() -> None:
    """P1 adapts an APPROVED section; the plan behind it is not its input.

    Asserted on the call, because the strip that guarantees it lives in the
    service and the mapping that renders it lives in the generator — no single
    unit test spans both.
    """
    lm, _, _ = _personalise()
    prompt = lm.prompt(0)
    for canary in CANARY_CLASSES:
        if canary.gate in STEP_PROSE_GATES:
            assert not canary.found_in(prompt), (
                f"the personalise call carries the {canary.name!r} step-prose slice "
                f"(gate={canary.gate}). {canary.note}"
            )


def test_p1_is_sent_no_record_keys() -> None:
    """The one call handed a whole stored section, and it was handed it whole.

    ``prompt_unit`` strips ids from every generation call because packs have
    narrated "step-t3w09-03" into learner text. Personalisation passed the base
    section as the stored model, so the same ids arrived by another route — on
    the single arm whose job is to rewrite that prose.

    Judged on the input values: the output schema still names the fields the
    call must return, and ``normalise_section`` overwrites whatever comes back.
    """
    lm, _, _ = _personalise()
    values = input_values(lm.messages(0)[-1])
    for key in RECORD_KEYS:
        # The JSON key form, not a bare substring: ``require_source_refs`` is a
        # policy flag whose name contains one of these and is not a leak.
        assert f'"{key}"' not in values, f"the personalise call names the record key {key!r}"
    assert "step:approved-base" not in values, "the personalise call carries a stored id VALUE"


def test_p1_identity_comes_from_the_unit_not_from_the_model() -> None:
    """What lets the ids stay out of the prompt: nothing downstream needs them there.

    Keeping any id the model returned is what made showing them look necessary.
    """
    _, personalised, request = _personalise()
    unit = request.units[0]
    assert personalised.section_id == unit.unit_id
    assert personalised.lesson_objective_id == unit.lesson_objective_id
    assert [block.block_id for block in personalised.blocks if block.block_type != "visual"] == [
        f"{unit.unit_id}:b0"
    ]
    assert [item.item_id for item in personalised.practice] == [f"{unit.unit_id}:p0"]


def test_neither_rewrite_call_is_sent_a_source_ref() -> None:
    """Provenance is applied after the call, so naming a ref asks nothing.

    ``assemble_section`` sets ``source_refs`` from the unit, and neither shape
    the model returns can carry one — so a ref in the section it is shown is
    text it cannot act on and cannot hand back. It also disagreed with itself:
    the block said ``["REF-1"]`` while the evidence beside it was labelled "the
    lesson note".
    """
    personalise_lm, _, _ = _personalise()

    profile = profile_for(Hypothesis.H1, ConditionCode.C3)
    request = build_request(example_plan(), profile)
    unit = request.units[0]
    repair_lm = RecordingLM(completion(repaired_section=_revision()))
    asyncio.run(
        RepairGeneratedSection(lm=repair_lm).repair_section(
            request=request,
            unit=unit,
            failed_section=_base_section(unit.lesson_objective_id),
            issues=["scope_compliance: out of scope"],
        )
    )

    for name, lm in (("personalise", personalise_lm), ("repair", repair_lm)):
        section = field_block(lm.messages(0)[-1], _SECTION_FIELD[name])
        assert '"source_refs"' not in section, f"the {name} call names source_refs"
        assert "REF-1" not in section, f"the {name} call carries a ref value"
    # The evidence still names itself — that IS the grounding, and it is prose.
    evidence = field_block(personalise_lm.messages(0)[-1], "source_evidence")
    assert "source_ref" in evidence, "the note lost the label it is cited by"


_SECTION_FIELD = {"personalise": "base_section", "repair": "failed_section"}


def _figured_section(objective_id: str) -> ReviewPackSection:
    """A stored section in the shape one actually comes back in: figures spliced in.

    ``_append_grounded_figures`` puts a visual block into every grounded section,
    and both rewrite calls are handed a stored section — so this, not
    ``_base_section``, is what they are really given on C2/C3 and P1.
    """
    section = _base_section(objective_id)
    section.blocks.append(
        ReviewPackBlock(
            block_id="step:approved-base:b1",
            block_type="visual",
            variant="diagram_tikz",
            caption="The line BC with B at the left.",
            figure_ref="fig-14",
            source_tikz="\\begin{tikzpicture}\\draw (0,0) -- (7,0);\\end{tikzpicture}",
            lesson_objective_id=objective_id,
        )
    )
    return section


def _rewrite_calls(section: ReviewPackSection) -> dict[str, RecordingLM]:
    """Both calls handed a whole stored section, run against that section."""
    profile = profile_for(Hypothesis.H1, ConditionCode.C3)
    request = build_request(example_plan(), profile)
    unit = request.units[0]
    repair_lm = RecordingLM(completion(repaired_section=_revision()))
    asyncio.run(
        RepairGeneratedSection(lm=repair_lm).repair_section(
            request=request,
            unit=unit,
            failed_section=section,
            issues=["scope_compliance: out of scope"],
        )
    )
    personalise_request = build_request(example_plan(), P1_PROFILE)
    personalise_lm = RecordingLM(completion(personalised_section=_revision()))
    asyncio.run(
        PersonaliseSection(lm=personalise_lm).personalise_section(
            request=personalise_request,
            unit=personalise_request.units[0],
            base_section=section,
            learner_state=_learner_state(personalise_request.units[0].lesson_objective_id),
        )
    )
    return {"repair": repair_lm, "personalise": personalise_lm}


@pytest.mark.parametrize("call", list(_SECTION_FIELD))
def test_a_section_shown_to_a_rewrite_call_is_one_it_could_hand_straight_back(call: str) -> None:
    """What a section shows is exactly what the answer shape can express.

    Both calls answer with a ``RevisedSection``, and gpt-oss mirrors the shape it
    is shown. Handed the stored section whole it echoed the figure back as a
    block — ``{"caption": ..., "figure_ref": "fig-14"}`` against a model
    requiring ``block_type`` and ``text`` and forbidding both. Listing the
    figures under a sibling key only moved the echo: it returned ``figures`` at
    the top instead, and ``extra="forbid"`` refused that too. Both times C3
    produced nothing for the lesson whose note is fourteen drawings.

    Round-tripping the rendered field is the whole invariant: a model that hands
    back precisely what it was given must parse.
    """
    objective_id = build_request(example_plan(), P1_PROFILE).units[0].lesson_objective_id
    lm = _rewrite_calls(_figured_section(objective_id))[call]
    rendered = field_block(lm.messages(0)[-1], _SECTION_FIELD[call])
    section = json.loads(rendered)

    authored = set(get_args(AuthoredBlockType))
    shown = {block.get("block_type") for block in section["blocks"]}
    assert shown <= authored, (
        f"the {call} call lists {sorted(shown - authored)} among the blocks to return, "
        f"and RevisedSection can express only {sorted(authored)}"
    )
    assert set(section) <= set(RevisedSection.model_fields), (
        f"the {call} call shows {sorted(set(section) - set(RevisedSection.model_fields))}, "
        "which the answer shape forbids and the model will echo"
    )
    RevisedSection.model_validate(section)
    assert "tikzpicture" not in rendered, (
        f"the {call} call carries the drawing source, which it may never edit"
    )


@pytest.mark.parametrize("model", AUTHORED_MODELS, ids=lambda m: m.__name__)
def test_no_model_the_llm_fills_declares_a_record_key(model: type) -> None:
    """The stronger form of the rule above: the ids are not merely overwritten.

    Overwriting a model-authored id fixes the artefact and leaves the prompt
    asking for one, which is what made showing the ids look necessary in the
    first place. Repair and personalisation returned whole stored sections, so
    both output contracts named every record key; they now return the writing.
    """
    declared = set(model.model_fields)
    assert not declared & set(RECORD_KEYS), (
        f"{model.__name__} asks the model for {sorted(declared & set(RECORD_KEYS))}"
    )


def test_the_repair_call_is_sent_no_record_keys() -> None:
    """Repair leaked exactly what personalisation did, and for the same reason.

    Both were handed the stored section. Nothing caught it here until the check
    stopped being about canary tokens: the failing section is built by the test,
    so it carries no plan slice for the leak map to see.
    """
    profile = profile_for(Hypothesis.H1, ConditionCode.C3)
    request = build_request(example_plan(), profile)
    unit = request.units[0]
    lm = RecordingLM(completion(repaired_section=_revision()))
    asyncio.run(
        RepairGeneratedSection(lm=lm).repair_section(
            request=request,
            unit=unit,
            failed_section=_base_section(unit.lesson_objective_id),
            issues=["scope_compliance: out of scope"],
        )
    )
    values = input_values(lm.messages(0)[-1])
    for key in RECORD_KEYS:
        assert f'"{key}"' not in values, f"the repair call names the record key {key!r}"
    assert "step:approved-base" not in values, "the repair call carries a stored id VALUE"


@pytest.mark.parametrize(
    "profile", [*h1_profiles(), P1_PROFILE], ids=lambda p: p.condition_code.value
)
def test_no_call_announces_a_field_it_is_not_sending(profile: ConditionProfile) -> None:
    """A withheld field must not appear empty; that names what was withheld.

    C0 was told ``"entry_behaviour": [], "instructional_materials": []`` — the
    control arm reading the list of fields it does not get. The rule holds for
    every call, so it is asserted on every call rather than on the one mapper
    where it was first fixed.
    """
    if profile.hypothesis == Hypothesis.H2:
        calls = [_personalise()[0].messages(0)]
    else:
        calls = _generate(profile)[0].messages_per_call
    for messages in calls:
        values = input_values(messages[-1])
        for hollow in ('": null', '": []', '": {}', '": ""'):
            assert hollow not in values, (
                f"{profile.condition_code.value} is shown an empty value ({hollow!r}), "
                "which tells it the field exists and was held back"
            )


def _plan_with_a_construction_step() -> SessionPlanView:
    """A plan whose one core step sets work with no question text to carry it.

    Thirteen of the frozen cohort's seventeen core steps have no `practice` block, and
    on five of those she still set work — a construction lives in the Student Activity
    column because it has no question. The shared canary fixture gives every step a
    question block, so it cannot reach this case at all.
    """
    return SessionPlanView.model_validate(
        {
            "session_id": "wire-construction",
            "subject": "Mathematics",
            "grade": "JSS1",
            "topic": "Construction",
            "lesson_plan_objectives": [{"lesson_objective_id": "obj0", "objective_text": "bisect"}],
            "entry_behaviour": ["uses a ruler"],
            "instructional_materials": ["set square"],
            "steps": [
                {
                    "step_id": "step-construction",
                    "step_kind": "core",
                    "lesson_objective_id": "obj0",
                    "note": "Place the compass on A.",
                    "activities": [
                        {"who": "teacher", "what": "explains WIRETEACHERNARRATION"},
                        {"who": "student", "what": "construct WIREWORKSET"},
                        {"who": "student", "what": "take notes on WIRERECEPTION"},
                    ],
                    "blocks": [{"id": "b0", "type": "explanation", "text": "Bisecting a segment."}],
                }
            ],
        }
    )


@pytest.mark.parametrize("profile", h1_profiles(), ids=lambda p: p.condition_code.value)
def test_work_she_set_reaches_the_prompt_and_her_narration_does_not(
    profile: ConditionProfile,
) -> None:
    r"""The narrowed boundary, asked of the wire.

    `student_tasks` used to read question blocks alone, so "construct angle 90
    degrees" reached no condition and C1 was told `elicit_performance` happened
    without being told what was performed. The column is now read — but only the
    performance half of it, and only where no question block carries the work.

    What must NOT follow is the rest of the column. A teacher activity narrates the
    lesson as an event, and a student activity that is reception is not work set;
    both stay out of every condition, which is what keeps this from being a hole in
    the exclusion rather than a narrowing of it.
    """
    request = build_request(_plan_with_a_construction_step(), profile)
    lm = RecordingLM(*(completion(section=_draft()) for _ in request.units))
    generator = GenerateSection(lm=lm)

    async def generate_all() -> None:
        await asyncio.gather(
            *(generator.generate_section(request=request, unit=unit) for unit in request.units)
        )

    asyncio.run(generate_all())
    sent = json.dumps(lm.messages_per_call)

    expected = profile.context.include_student_tasks
    assert ("WIREWORKSET" in sent) is expected, profile.condition_code.value
    assert "WIRETEACHERNARRATION" not in sent
    assert "WIRERECEPTION" not in sent
