"""The Part 2 comments, coded once each as ``62_Comment_Coding``, and the responsiveness results.

The fifteen comments in ``35_P2_Comments`` were volunteered, not required, so the coding counts
what they say and estimates no rate. The code set was drawn up after the comments were read, so it
is a record of the researcher's reading and not a scheme fixed in advance. Each comment carries
one code and the words that decide it; a row stays a draft until the researcher confirms it.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .record import READING, Printed, Result
from .sources import Row, Sources
from .xlsx import Sheet

SHEET = "62_Comment_Coding"
COMMENTS = "35_P2_Comments"

OWN_ERROR = "own error"
ERROR_TYPE = "error type, not the learner's instance"

FOR = "for personalisation"
AGAINST = "against personalisation"
EITHER = "either way"


@dataclass(frozen=True)
class Code:
    meaning: str
    #: Whether the code itself takes a side on personalisation, or can favour either material.
    direction: str = EITHER


#: Every code a comment can take, with the reading that assigns it.
CODEBOOK = {
    OWN_ERROR: Code(
        "Names the specific error or misconception this learner made and says how the material "
        "engages it.",
        FOR,
    ),
    ERROR_TYPE: Code(
        "Says the material engages the kind of error the learner made but not the learner's "
        "own instance of it.",
        AGAINST,
    ),
    "explanation": Code(
        "Judges how explanatory or clear the material is: definitions, context, or "
        "explanation, with no reference to the learner."
    ),
    "worked steps": Code("Judges whether worked solutions show every step."),
    "challenge": Code("Judges the depth of challenge or reasoning the material offers."),
    "presentation": Code("Judges emphasis or typography, such as bold keywords."),
    "no reason": Code("States a preference without saying what it rests on."),
}

P1, BASE = "P1", "base"
#: The recorded preferred arm under the name a reading gives it.
ARM = {"P1": P1, "P0": BASE}

DRAFT = "draft, awaiting the researcher's confirmation"


@dataclass(frozen=True)
class Coding:
    code: str
    #: The material the comment argues for, as read; checked against the recorded preference.
    favours: str
    quote: str
    #: Why the code fits: which material the comment is about, and what the packs contain.
    reading: str
    status: str = DRAFT


#: Coded by hand, one comment at a time, against the arm shown as Material A in
#: ``12_P2_Raw``, the learner's recorded state in the run record, and both packs' text.
#: Keyed by rater, learner, objective and criterion, which identify a comment.
CODED: dict[tuple[str, str, str, str], Coding] = {
    ("rater-1", "student-03", "lo-t3w02-01", "adaptive_calibration"): Coding(
        OWN_ERROR,
        P1,
        "repeatedly laid emphasis on the mistake",
        "P1 was Material B and preferred. The learner's recorded error is n-1 for n-2 (7 "
        "triangles for an octagon). P1 names that slip three times: in the explanation ('write "
        "7 for an octagon ... 6, not 7'), in the check, and in a practice item asking why the "
        "answer is not 7. P0 never mentions it.",
    ),
    ("rater-2", "student-01", "lo-t3w02-01", "learner_evidence_alignment"): Coding(
        "presentation",
        P1,
        "more word emphasis using Bold texts",
        "P1 was Material A and preferred. The comment concerns bold keywords, not the learner; "
        "the learner has no recorded error on this objective (band extend).",
    ),
    ("rater-2", "student-01", "lo-t3w02-01", "adaptive_calibration"): Coding(
        "explanation",
        BASE,
        "The definitions are much more explanatory",
        "P1 was Material A; the base pack (B) was preferred for its definitions. No reference "
        "to the learner, who has no recorded error on this objective.",
    ),
    ("rater-2", "student-01", "lo-t3w02-01", "instructional_integrity"): Coding(
        "explanation",
        BASE,
        "much more explanatory overall",
        "P1 was Material A; the base pack (B) was preferred as more explanatory. No reference "
        "to the learner.",
    ),
    ("rater-2", "student-01", "lo-t3w02-03", "adaptive_calibration"): Coding(
        "explanation",
        P1,
        "more explanatory in terms of context and definitions",
        "P1 was Material A and preferred for context and definitions. The learner's recorded "
        "error (a side miscopied, 5 for 8) is not mentioned.",
    ),
    ("rater-2", "student-01", "lo-t3w02-03", "instructional_integrity"): Coding(
        "worked steps",
        BASE,
        "it skips processes",
        "P1 was Material A; the base pack (B) was preferred. The comment names A twice; the "
        "preference recorded ('B slightly better') fixes the reading: P1 was judged rushed, "
        "with steps skipped.",
    ),
    ("rater-2", "student-05", "lo-t3w02-01", "adaptive_calibration"): Coding(
        "explanation",
        P1,
        "The explanation is clearer.",
        "P1 was Material B and preferred for clarity. The learner has no recorded error on "
        "this objective.",
    ),
    ("rater-3", "student-02", "lo-t3w02-01", "learner_evidence_alignment"): Coding(
        OWN_ERROR,
        P1,
        "directly targets the student’s specific error",
        "P1 was Material B and preferred. The learner's recorded error is giving the side "
        "count, 8, as the triangle count. P1 names it ('a common slip is to answer 8 because 8 "
        "is the number of sides') and returns to it in the worked example; P0 states only the "
        "rule.",
    ),
    ("rater-3", "student-02", "lo-t3w02-01", "adaptive_calibration"): Coding(
        OWN_ERROR,
        P1,
        "guidance for the student’s specific misconception",
        "Same panel as the comment before: P1 (Material B) names the learner's side-count "
        "slip; P0 does not.",
    ),
    ("rater-3", "student-02", "lo-t3w02-03", "learner_evidence_alignment"): Coding(
        OWN_ERROR,
        P1,
        "identify the student’s key error, however material B is more explicit",
        "P1 was Material B and preferred. The learner's recorded error is doubling an "
        "already-doubled pair. P1 warns against doubling again in five places; P0 never "
        "mentions it, so the comment's 'both materials identify' holds for P1 only.",
    ),
    ("rater-3", "student-02", "lo-t3w02-03", "adaptive_calibration"): Coding(
        OWN_ERROR,
        P1,
        "consistently flags the doubling again in the rectangle",
        "P1 was Material B and preferred. P1 flags doubling again in the rectangle "
        "explanation, two worked examples and two practice answers; this is the learner's "
        "recorded error.",
    ),
    ("rater-3", "student-01", "lo-t2w09-01", "learner_evidence_alignment"): Coding(
        ERROR_TYPE,
        BASE,
        "address similar errors but are not the student’s own",
        "P1 was Material A; the base pack (B) was preferred. The code records what the rater "
        "says. The packs show it holds for practice only: P1's worked examples use the "
        "learner's own item (32 + 8x ÷ 2) and name her wrong answers (36x, 70n, 53y), but its "
        "practice questions are new items of the same kind, while P0's practice re-poses her "
        "classwork questions.",
    ),
    ("rater-3", "student-05", "lo-t3w05-02", "instructional_integrity"): Coding(
        "worked steps",
        BASE,
        "completeness of worked examples",
        "P0 was Material A and preferred slightly for fuller worked examples. The learner has "
        "no recorded error on this objective.",
    ),
    ("rater-3", "student-09", "lo-t3w02-01", "adaptive_calibration"): Coding(
        "challenge",
        P1,
        "stronger challenges and deeper reasoning opportunities",
        "P1 was Material A and preferred for challenge. The learner is in the extend band with "
        "no recorded error, so this is extension, not error response.",
    ),
    ("rater-4", "student-01", "lo-t3w02-01", "learner_evidence_alignment"): Coding(
        "no reason",
        P1,
        "B is clearly better.",
        "P1 was Material B and preferred; no reason is given.",
    ),
}

TITLE = "PART 2 | COMMENT CODING"
NOTE = (
    f"Each comment in {COMMENTS} coded by hand, once, against a fixed set of {len(CODEBOOK)} "
    "codes, reading which arm was Material A, the learner's recorded state, and both packs. "
    "Each row gives the deciding words, what the code means, and that reading. 'Code "
    "direction' says whether the code itself takes a side on personalisation or can favour "
    "either material; 'Favours' is the material the comment argues for, which must agree with "
    "the rater's recorded preference. The codes were drawn up after reading the comments, so "
    "this records the researcher's reading; the comments were volunteered, so the counts are "
    "existence evidence and no rate. Written by "
    "experiments.human_rating.register in the code repository."
)
HEADER = (
    "Rater",
    "Learner",
    "Objective",
    "Criterion",
    "Panel",
    "Preferred arm",
    "Signed preference",
    "Comment",
    "Code",
    "Code direction",
    "Favours",
    "Deciding words",
    "What the code means",
    "Reading against the materials",
    "Status",
)
WIDTHS = (10, 12, 14, 26, 24, 10, 10, 60, 30, 22, 10, 44, 50, 70, 34)


def coded(sources: Sources) -> list[tuple[Row, Coding]]:
    """Every comment with its coding; a comment without one, or a code outside the set, fails."""
    rows = sources.sheet(COMMENTS)
    keys = [(r["Rater"], r["Learner"], r["Objective"], r["Criterion"]) for r in rows]
    _check_coverage(keys)
    for row, key in zip(rows, keys, strict=True):
        if CODED[key].quote not in row["Comment"]:
            raise ValueError(f"{key}: deciding words not in the comment")
        if CODED[key].favours != ARM[row["Preferred arm"]]:
            raise ValueError(f"{key}: read as favouring {CODED[key].favours}, recorded otherwise")
    return [(row, CODED[key]) for row, key in zip(rows, keys, strict=True)]


def _check_coverage(keys: list[tuple[str, str, str, str]]) -> None:
    missing = [key for key in keys if key not in CODED]
    unused = [key for key in CODED if key not in keys]
    unknown = [c.code for c in CODED.values() if c.code not in CODEBOOK]
    unknown += [c.favours for c in CODED.values() if c.favours not in (P1, BASE)]
    if missing or unused or unknown:
        raise ValueError(f"comment coding out of step: {missing=} {unused=} {unknown=}")


def counts(sources: Sources) -> Counter[str]:
    return Counter(coding.code for _, coding in coded(sources))


def sheet(sources: Sources) -> Sheet:
    rows = [
        (
            r["Rater"],
            r["Learner"],
            r["Objective"],
            r["Criterion"],
            r["Panel"],
            r["Preferred arm"],
            r["Signed preference"],
            r["Comment"],
            coding.code,
            CODEBOOK[coding.code].direction,
            coding.favours,
            coding.quote,
            CODEBOOK[coding.code].meaning,
            coding.reading,
            coding.status,
        )
        for r, coding in coded(sources)
    ]
    return Sheet(SHEET, TITLE, NOTE, HEADER, rows, WIDTHS, keys=4)


def results(sources: Sources, answered: int) -> list[Result]:
    """RQ2's responsiveness check: the comments written, and those naming the learner's error."""
    location = sources.where("sec:identifiable-responsiveness")
    return [_written(sources, answered, location), _responsive(sources, location)]


def _written(sources: Sources, answered: int, location: str) -> Result:
    rows = sources.sheet(COMMENTS)
    lessons = Counter(r["Lesson"] for r in rows)
    return Result(
        id="P2-R1",
        part="Part 2",
        question="RQ2, responsiveness",
        location=location,
        quantity="Comments written across the answered judgements",
        estimate=Printed("15", str(len(rows))),
        also=(
            ("raters", Printed("4", str(len({r["Rater"] for r in rows})))),
            ("panels", Printed("9", str(len({r["Panel"] for r in rows})))),
            ("cases", Printed("7", str(len({(r["Lesson"], r["Learner"]) for r in rows})))),
            ("from one lesson", Printed("13", str(lessons.most_common(1)[0][1]))),
        ),
        unit=f"comment (of {answered} answered cells)",
        computed_from=COMMENTS,
    )


def _responsive(sources: Sources, location: str) -> Result:
    found = coded(sources)
    own = [row for row, coding in found if coding.code == OWN_ERROR]
    opposite = [row for row, coding in found if coding.code == ERROR_TYPE]
    drafts = sum(coding.status == DRAFT for _, coding in found)
    pending = f"; {drafts} of {len(found)} codings await confirmation" if drafts else ""
    return Result(
        id="P2-R2",
        part="Part 2",
        question="RQ2, responsiveness",
        location=location,
        quantity="Comments identifying responsiveness to the learner's own error",
        estimate=Printed("5", str(len(own))),
        also=(
            ("raters", Printed("2", str(len({r["Rater"] for r in own})))),
            ("learners", Printed("2", str(len({(r["Lesson"], r["Learner"]) for r in own})))),
            ("recording the opposite", Printed("1", str(len(opposite)))),
        ),
        status=READING,
        unit="comment",
        computed_from=f"{COMMENTS}; {SHEET}",
        note=f"the researcher's reading, coded by hand in {SHEET}{pending}",
    )
