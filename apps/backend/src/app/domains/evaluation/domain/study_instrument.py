"""The rating instrument, frozen as data.

Two vocabularies, deliberately. Each construct's *research* name is domain-general —
it describes the framework and is the id the analysis keys on. Its *rater-facing* name,
question and scale descriptors are mathematics-specific, because the raters are
mathematics educators judging mathematics materials. Nothing rater-facing names a
condition, a hypothesis, or how a material was produced.

Source: Final Human Rating Protocol, 2026-09. The wording here is that document's,
and a change to it is a change to the instrument.
"""

from __future__ import annotations

from dataclasses import dataclass

#: The comparative response, from one material to the other. "About the same" is a real
#: answer: two materials can both be good, and forcing a winner would manufacture a
#: difference the rater did not see.
COMPARISON: tuple[str, ...] = (
    "A clearly better",
    "A slightly better",
    "About the same",
    "B slightly better",
    "B clearly better",
)

SCALE: tuple[tuple[int, str], ...] = (
    (1, "Does not meet the criterion"),
    (2, "Meets the criterion only to a limited extent"),
    (3, "Adequately meets the criterion"),
    (4, "Meets the criterion well"),
    (5, "Fully meets the criterion"),
)


@dataclass(frozen=True)
class Criterion:
    id: str
    """Research-facing construct id; the key every analysis uses."""
    construct: str
    """Research-facing construct name, domain-general."""
    name: str
    """Rater-facing name, mathematics-specific."""
    question: str
    descriptors: tuple[str, str, str, str, str]
    """Rater descriptions for scores 1 through 5."""
    notes: tuple[str, ...] = ()
    """Guidance shown beside the scale, in the rater's language."""
    better: str = ""
    """What "better" means for this criterion, when two materials are weighed directly.

    One line drawn from the criterion's own top descriptor. A comparative judgement asks
    which way a criterion leans, and the anchor says which way is up.
    """


H1_CRITERIA: tuple[Criterion, ...] = (
    Criterion(
        id="curriculum_objective_alignment",
        construct="Curriculum-objective alignment",
        name="Addresses the stated mathematics learning objective",
        question=(
            "To what extent does this section address the mathematical knowledge, skills or "
            "processes, and intended level specified by the learning objective?"
        ),
        descriptors=(
            "The section does not meaningfully address the learning objective, substantially "
            "contradicts it, or omits its central mathematical content or skill.",
            "The section has some connection to the objective, but major required knowledge, "
            "skills, processes, or expected level are missing or misrepresented.",
            "The section addresses the main learning objective, but coverage is incomplete, "
            "uneven, or partly displaced by related content.",
            "The section addresses nearly all of the required mathematical content, skills or "
            "processes at an appropriate level. Only minor omissions or mismatches are present.",
            "The section fully and accurately addresses the stated learning objective at the "
            "intended level, without substantive omission or unnecessary drift.",
        ),
        notes=("The reference point for this criterion is the learning objective itself.",),
    ),
    Criterion(
        id="lesson_context_alignment",
        construct="Lesson-context alignment",
        name="Reflects the teacher-planned mathematics lesson",
        question=(
            "To what extent does this section reflect the planned mathematical emphasis, "
            "sequence, methods or procedures, representations, examples or activities, and "
            "assessment expectations for this learning objective?"
        ),
        descriptors=(
            "The section does not meaningfully reflect the teacher-planned treatment of the "
            "objective or substantially contradicts it.",
            "The section reflects only a small part of the planned treatment. Several important "
            "elements, such as the mathematical emphasis, method, representation, example, "
            "activity, or assessment expectation, are missing or substantially different.",
            "The main planned treatment is recognisable, but there are noticeable differences or "
            "omissions in the emphasis, sequence, methods, representations, examples, "
            "activities, or assessment expectations.",
            "The section closely reflects the teacher-planned treatment. Only minor differences "
            "are present and these do not materially change the instructional intention.",
            "The section consistently reflects the teacher-planned treatment of the objective, "
            "including its important mathematical emphasis, methods or representations, "
            "examples or activities, and assessment expectations.",
        ),
        notes=(
            "Judge instructional correspondence, not verbatim reproduction. Changing numbers, "
            "wording, or contexts does not reduce the score when the instructional intention "
            "remains intact.",
        ),
    ),
    Criterion(
        id="instructional_quality",
        construct="Instructional quality",
        name="Is mathematically correct, clear, and useful for learning",
        question=(
            "To what extent is this section mathematically accurate, clearly explained and "
            "organised, and suitable for independent review and practice by the intended "
            "learners?"
        ),
        descriptors=(
            "The section contains serious mathematical errors or is so unclear, incomplete, or "
            "poorly organised that it is unsuitable for learning.",
            "The section has major mathematical or instructional weaknesses. Substantial "
            "revision would be needed before it could be used effectively by learners.",
            "The section is generally mathematically sound and usable, but has noticeable "
            "weaknesses in explanation, organisation, examples, instructions, notation, "
            "practice, or learner support.",
            "The section is mathematically accurate, clear, logically organised, and suitable "
            "for independent review and practice. Only minor improvements are needed.",
            "The section is mathematically accurate throughout, clearly and coherently "
            "explained, well organised, and fully suitable for independent review and "
            "meaningful practice by the intended learners.",
        ),
        notes=("A substantive mathematical error is a serious weakness, not a minor one.",),
    ),
)

#: Rater-facing wording says "student", where the protocol document says "learner": the
#: pages call the same thing the student's class work, and one name for it is worth more
#: to a rater than fidelity to a word. The research-facing ``construct`` names are the
#: protocol's own and are untouched.
H2_CRITERIA: tuple[Criterion, ...] = (
    Criterion(
        id="learner_evidence_alignment",
        better=(
            "targets what this student's class work actually showed, without assuming "
            "a need the evidence does not support"
        ),
        construct="Learner-evidence alignment",
        name="Responds to what this student has demonstrated in mathematics",
        question=(
            "To what extent does this section respond to the mathematical understanding, "
            "difficulty, error, gap, or demonstrated strength shown in this student's class "
            "work for "
            "this objective?"
        ),
        descriptors=(
            "The section ignores, contradicts, or substantially misinterprets what the student "
            "has demonstrated. It targets the wrong mathematical need or assumes a need "
            "unsupported by the evidence.",
            "The section has only a weak or generic relationship to the student's class work. "
            "Important demonstrated strengths, difficulties, errors, or gaps are overlooked.",
            "The section responds to some of the student's class work, but the targeting is "
            "incomplete, broad, inconsistent, or based on only part of what the student "
            "demonstrated.",
            "The section responds well to the main evidence-backed strength or learning need. "
            "Only minor relevant aspects of the student's class work are overlooked.",
            "The section responds precisely and consistently to what the student has "
            "demonstrated. Its explanations, examples, practice, or extension clearly target "
            "the evidence-backed need or strength without unsupported assumptions.",
        ),
        notes=(
            "Correct answers count as class work evidence. A student who demonstrates mastery "
            "should not be treated as though they have a misconception merely because the "
            "material is adapted for them.",
        ),
    ),
    Criterion(
        id="adaptive_calibration",
        better=(
            "pitched where this student actually is — the right support for a "
            "difficulty, real progression beyond a mastery"
        ),
        construct="Adaptive calibration",
        name="Provides appropriate mathematical support and challenge",
        question=(
            "Given what the student has demonstrated, to what extent are the explanations, "
            "guidance, examples, practice, and level of mathematical challenge appropriate for "
            "this student?"
        ),
        descriptors=(
            "The level of support or challenge is clearly inappropriate. The material is far "
            "too easy or difficult, or the amount or type of support is fundamentally "
            "mismatched to the student.",
            "There is a substantial mismatch between the student's demonstrated understanding "
            "and the support, practice, guidance, or challenge provided.",
            "The material is generally appropriate, but calibration is uneven. Some parts "
            "provide too much or too little support, unnecessary repetition, insufficient "
            "practice, or inappropriate difficulty.",
            "The support and challenge are well matched to the student's demonstrated "
            "understanding. Only minor adjustment would improve the calibration.",
            "The material is consistently well calibrated to the student. It provides the right "
            "degree of support without unnecessary repetition and offers an appropriate next "
            "level of mathematical challenge.",
        ),
        #: Written against what the class work shows rather than against a band. The band
        #: is the instruction the adapted material was written from, and a rater given it
        #: is being handed one material's brief and asked to mark both against it.
        #: Written as properties of the material rather than of a score, so the same
        #: guidance serves a judgement made on a scale and one made between two materials.
        notes=(
            "Where the class work shows a difficulty or a prerequisite gap, the material "
            "must direct support at it, with suitable explanations, representations, worked "
            "support, and guided practice.",
            "Where the class work shows partially secure understanding, it must consolidate "
            "that understanding without unnecessary full re-teaching.",
            "Where the class work shows the objective already mastered, it must progress "
            "meaningfully beyond it, such as deeper reasoning, justification, generalisation, "
            "connections, non-routine applications, or increased mathematical demand. More "
            "questions at the level already mastered is not progression.",
        ),
    ),
    Criterion(
        id="instructional_integrity",
        better=("mathematically accurate throughout, and still on the stated objective and scope"),
        construct="Instructional integrity",
        name="Remains mathematically correct and focused on the learning objective",
        question=(
            "To what extent does this section remain mathematically accurate and preserve the "
            "intended learning objective and scope while being adapted for this student?"
        ),
        descriptors=(
            "The section contains serious mathematical errors, substantially abandons or "
            "changes the intended learning objective, or both.",
            "The section contains a major mathematical weakness or substantial drift from the "
            "objective or intended mathematical scope.",
            "The section is generally mathematically sound and retains the main objective, but "
            "contains a noticeable minor error, ambiguity, unnecessary scope change, or partial "
            "drift.",
            "The section is mathematically correct and clearly preserves the intended learning "
            "objective and scope. Only minor non-substantive issues are present.",
            "The section is mathematically accurate throughout and fully preserves the intended "
            "learning objective and appropriate scope while adapting its support, examples, "
            "practice, or challenge for the student.",
        ),
        notes=("A substantive mathematical error is a serious weakness, not a minor one.",),
    ),
)

#: The instructional band a student's evidence puts them in, in the rater's words.
BAND_LABELS: dict[str, str] = {
    "remediate": "Remediate",
    "reinforce": "Reinforce",
    "extend": "Extend",
}
