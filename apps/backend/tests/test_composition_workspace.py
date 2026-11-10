"""Composing through tools moves the output channel and nothing else.

The condition must survive the swap: same inputs per level, no evidence where
the level has none, and tools that can only build a well-formed section.
"""

from __future__ import annotations

from recording_lm import RecordingLM

from app.domains.artefacts.types.post_class_review_pack.application.request.artefact import (
    revision_pack_spec,
)
from app.domains.artefacts.types.post_class_review_pack.application.request.schemas import (
    BaseReviewPackRequest,
    GenerationPolicyContext,
    LessonContextForGeneration,
    SectionGenerationUnit,
    SourceEvidenceItem,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.compose_section import (
    ComposeSection,
    composition_contract,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.contracts.write_section import (  # noqa: E501
    WriteGroundedSection,
    WriteObjectiveSection,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.prompt_projection import (  # noqa: E501
    prompt_evidence,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.tools.section_draft import (  # noqa: E501
    SectionDraft,
    composition_tools,
    handle,
)
from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.tools.source_reading import (  # noqa: E501
    evidence_toolset,
)
from app.domains.experiments.domain.types import ConditionCode
from app.domains.experiments.review_pack_study.conditions.profiles import H1_CONDITION_PROFILES


def _unit(with_evidence: bool = False) -> SectionGenerationUnit:
    return SectionGenerationUnit(
        unit_id="unit:lo-1",
        lesson_objective_id="lo-1",
        objective_text="identify properties of cylinders",
        source_evidence=(
            [SourceEvidenceItem(source_ref="s1", excerpt="A cylinder has two circular faces.")]
            if with_evidence
            else []
        ),
    )


def _request(code: ConditionCode, unit: SectionGenerationUnit) -> BaseReviewPackRequest:
    return BaseReviewPackRequest(
        artefact_spec=revision_pack_spec("JSS1"),
        generation_policy=H1_CONDITION_PROFILES[code].generation_policy(),
        policy=GenerationPolicyContext(
            require_source_refs=False,
            use_only_provided_sources=False,
            preserve_lesson_objective=True,
            instruction_summary="",
        ),
        lesson_context=LessonContextForGeneration(
            subject="Mathematics", grade_level="JSS1", topic="Shapes", lesson_objectives=[]
        ),
        units=[unit],
    )


def test_derived_signature_keeps_the_levels_inputs_and_moves_the_output() -> None:
    derived = composition_contract(WriteGroundedSection)
    assert list(derived.input_fields) == list(WriteGroundedSection.input_fields)
    assert "section" not in derived.output_fields
    assert "done" in derived.output_fields
    assert WriteGroundedSection.instructions in derived.instructions
    assert "calling the tools" in derived.instructions


def test_a_derived_signature_says_which_contract_it_wrapped() -> None:
    """The provenance component is this name, and it is the only place it appears.

    ``with_instructions`` rebuilds the class as dspy's default ``StringSignature``,
    which recorded every composed arm — objective or grounded — under one key.
    """
    assert composition_contract(WriteGroundedSection).__name__ == "ComposeWriteGroundedSection"
    assert composition_contract(WriteObjectiveSection).__name__ == "ComposeWriteObjectiveSection"


def test_objective_level_composition_still_has_no_evidence_field() -> None:
    derived = composition_contract(WriteObjectiveSection)
    assert "lesson_content" not in derived.input_fields


def test_evidence_less_level_is_passed_no_evidence() -> None:
    lm = RecordingLM()
    generator = ComposeSection(
        lm=lm,
        contract_mode="leveled",
    )
    unit = _unit()
    request = _request(ConditionCode.C0, unit)
    signature = generator.contract(request)
    inputs = generator.inputs(request, unit, signature)
    assert set(inputs) == set(signature.input_fields)
    assert "lesson_content" not in inputs
    assert "source_evidence" not in inputs


def test_grounded_level_is_passed_its_evidence_in_the_form_every_other_path_sends() -> None:
    """The evidence is pruned dicts here too, not the stored items.

    This arm handed the pydantic objects straight over, against a field declared
    ``list[dict]``: dspy warned about the type on every grounded call and
    serialized them anyway, so C2 and C3 were shown the four empty catalogue keys
    ``prompt_evidence`` exists to strip — on this arm, which is the one the H1
    runs are made on.
    """
    lm = RecordingLM()
    generator = ComposeSection(
        lm=lm,
        contract_mode="leveled",
    )
    unit = _unit(with_evidence=True)
    request = _request(ConditionCode.C2, unit)
    signature = generator.contract(request)
    inputs = generator.inputs(request, unit, signature)
    assert inputs["lesson_content"] == prompt_evidence(unit.source_evidence)
    assert inputs["lesson_content"] == [
        {"source_ref": "s1", "excerpt": "A cylinder has two circular faces."}
    ]
    assert signature.input_fields["lesson_content"].annotation == list[dict]


def test_tools_build_a_well_formed_section() -> None:
    draft = SectionDraft(_unit())
    set_title, add_block, read_draft, revise_block, add_practice, _ = composition_tools(draft)

    set_title("  Cylinders and spheres  ")
    assert add_block("explanation", "A cylinder has two circular faces.") == "Added b0."
    add_block("worked_example", "Count the faces of a tin: 2 circles and 1 curved surface.")
    assert add_practice("How many faces does a cylinder have?", "3") == "Added p0."

    section = draft.to_section()
    assert section.title == "Cylinders and spheres"
    assert section.section_id == "unit:lo-1"
    assert [b.block_type for b in section.blocks] == ["explanation", "worked_example"]
    assert all(b.lesson_objective_id == "lo-1" for b in section.blocks)
    # Provenance is stamped from the unit, never asked for.
    assert section.blocks[1].source_refs == []
    assert "A cylinder has two circular faces." in read_draft()

    # Addressed by the handle read_draft shows; the section keeps the qualified id.
    assert revise_block("b0", "A cylinder has two flat circular faces.") == "Revised b0."
    assert section.blocks[0].block_id == "unit:lo-1:b0"
    assert draft.blocks[0].text == "A cylinder has two flat circular faces."


def test_a_practice_question_is_stored_apart_from_its_answer() -> None:
    """The answer is a field, so nothing can put it under its own question.

    While it was prose the model wrote "1. ... **Answer:** ..." in 9 of 12 cells and the
    brief's "answers at the end" had no way to stop it (issue #163).
    """
    draft = SectionDraft(_unit())
    *_, add_practice, revise_practice = composition_tools(draft)
    add_practice("How many faces does a cylinder have?", "3", "Two circles and one curved.")

    item = draft.to_section().practice[0]
    assert item.item_id == "unit:lo-1:p0"
    assert item.prompt == "How many faces does a cylinder have?"
    assert item.answer == "3"
    assert item.worked_solution == "Two circles and one curved."
    assert "Answer" not in item.prompt

    # The tools address by the short handle; the STORED id keeps its unit prefix, which
    # is what travels downstream and has to be unique across units.
    assert revise_practice("p0", "How many edges?", "2") == "Revised p0."
    assert draft.practice[0].item_id == "unit:lo-1:p0"
    assert draft.practice[0].answer == "2"
    assert draft.practice[0].worked_solution is None


def test_tools_refuse_what_would_break_the_section() -> None:
    draft = SectionDraft(_unit())
    _, add_block, _, revise_block, add_practice, revise_practice = composition_tools(draft)

    assert "Unknown block_type" in add_block("visual", "a picture of a cylinder")
    # Practice is no longer a block type: it carries an answer, so it has its own tool.
    assert "Unknown block_type" in add_block("practice", "How many faces?")
    assert "must carry text" in add_block("explanation", "   ")
    assert "No block" in revise_block("unit:lo-1:b9", "text")
    assert "must carry the answer" in add_practice("How many faces?", "  ")
    assert "must carry a question" in add_practice("  ", "3")
    assert "No practice item" in revise_practice("unit:lo-1:p9", "q", "a")
    assert draft.blocks == []
    assert draft.practice == []


def test_a_revise_names_the_ids_when_it_cannot_find_one() -> None:
    """The loop this ends, which cost a whole generation.

    A unit id is namespaced — `step:step-t2w09-03` — so a practice item reads
    `step:step-t2w09-03:p0`: a leading `step:`, a nested `step-...`, two colons. A writer
    read that back from read_draft, took the prefix for a display label, and sent
    `step-t2w09-03:p0`. It was told the id was unknown and to call read_draft, which it
    had just done. It looped until its output budget was gone and returned nothing, and
    the abandoned turn still scored as a section.
    """
    draft = SectionDraft(_unit())
    _, add_block, _, revise_block, add_practice, revise_practice = composition_tools(draft)
    add_practice("Simplify 12-(7-2f)", "2 + 3f")
    add_block("explanation", "Some teaching.")

    # The failure now names what exists instead of pointing back at read_draft.
    refusal = revise_practice("nope", "q", "a")
    assert "The ids are:" in refusal
    assert handle(draft.practice[0].item_id) in refusal
    assert draft.practice[0].item_id not in refusal  # the prefix is not the address
    assert "read_draft" not in refusal

    # And a fully-qualified id still resolves, so an older caller is not broken.
    assert "Revised" in revise_practice(draft.practice[0].item_id, "q", "a")
    assert "Revised" in revise_practice("p0", "q2", "a2")
    assert draft.practice[0].prompt == "q2"
    assert "Revised" in revise_block("b0", "new text")
    assert draft.blocks[0].text == "new text"


def test_an_ambiguous_id_fragment_is_still_refused() -> None:
    """Tolerance stops where the answer stops being knowable."""
    draft = SectionDraft(_unit())
    *_, add_practice, revise_practice = composition_tools(draft)
    for n in range(12):
        add_practice(f"question {n}", f"answer {n}")

    # "1" ends p1 and p11 alike, so there is no one item it means.
    assert "The ids are:" in revise_practice("1", "q", "a")
    assert draft.practice[1].prompt == "question 1"


def test_untitled_draft_falls_back_to_the_objective() -> None:
    draft = SectionDraft(_unit())
    _, add_block, *_ = composition_tools(draft)
    add_block("explanation", "Some teaching.")
    assert draft.to_section().title == "identify properties of cylinders"


def test_reading_composer_swaps_packed_evidence_for_tools() -> None:
    lm = RecordingLM()
    generator = ComposeSection(
        lm=lm,
        contract_mode="leveled",
        source_tools=evidence_toolset(),
    )
    unit = _unit(with_evidence=True)
    request = _request(ConditionCode.C2, unit)
    signature = generator.contract(request)

    # Evidence is read, not packed: the field is gone and the task says so.
    assert "lesson_content" not in signature.input_fields
    assert "lesson_content" not in generator.inputs(request, unit, signature)
    assert "not in this prompt" in signature.instructions
    assert "calling the tools" in signature.instructions


def test_reading_composer_carries_both_toolsets() -> None:
    lm = RecordingLM()
    generator = ComposeSection(
        lm=lm,
        source_tools=evidence_toolset(),
    )
    unit = _unit(with_evidence=True)
    draft = SectionDraft(unit)
    names = [tool.__name__ for tool in composition_tools(draft)] + [
        tool.__name__ for tool in evidence_toolset()(_request(ConditionCode.C2, unit), unit)
    ]
    assert names == [
        "set_title",
        "add_block",
        "read_draft",
        "revise_block",
        "add_practice",
        "revise_practice",
        "list_documents",
        "read_document",
    ]
    assert generator.source_tools is not None
