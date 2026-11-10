# Source-fidelity audit — 2026-08-09

Not an audit of whether the lesson plans are *good*. An audit of one question:

> **Does the experimental representation equal the source it claims to represent?**

All six lessons, the same checklist, applied without reference to how any condition
scored. The distinction that governs every entry below:

> **Correct errors — hers and the pipeline's. Leave her instructional design alone.**

Both classes are corrected, and the line runs between an *error* and a *choice*, not
between her and us. A pipeline defect changes what C1 *is*. An error in her document —
a divisor restated, a length squared, an author miscredited — is corrected too, under the
project's standing convention: `teacher.md` stays archival and verbatim, the correction
goes in `teacher-cleaned.md`, and *a cleaning that cannot name its source is an edit, not
a cleaning*.

What is never touched is her instructional design. `t3-w09` assessing "state three methods
of collecting data" against an objective about interpreting tables is not a mistake to
repair; it is a property of the plan, and one of the things the study exists to surface.
Repairing it would replace "the teacher's lesson plan" with "a researcher-improved lesson
plan".

Every item below is itemised as a GitHub issue tagged `data-error` + `h1-data-error`
(#133-#160), so each correction carries its own reviewable record.

## Checklist

| check | result |
| --- | --- |
| Objectives — meaning and count preserved | pass; trims to delivered objectives are declared per lesson with a source |
| Previous knowledge — no dropped items | **fixed** (1 lesson) |
| Materials — complete, correctly scoped | **fixed** (scope) |
| Presentation — all genuine steps, ordered | pass; two restructures declared with sources |
| Activities — her narration preserved before coding | **fixed** (4 lessons) |
| Student tasks — every genuine task captured | pass, 4 of 16 core steps carry them |
| Evaluation — every question captured exactly | **fixed** (fabricated answers) |
| Figures — available referenced figures included | **fixed** (drawing source in a question) |
| Mathematics — no parser corruption | pass, verified verbatim against the transcripts |
| Provenance — no transcriber additions as teacher content | **fixed** (titles, annotations) |
| C1 transformation — Gagné code agrees with the source | pass, pinned by the corpus table in `tests/test_instructional_events.py` |
| C0/C1 receive the same task instruction | **fixed** |

## Corrections, with classification

| lesson | what the source has | what the experiment had | corrected to | classification |
| --- | --- | --- | --- | --- |
| t2-w09 | "Students have been taught: 1. Addition and subtraction… 2. Multiplication and division…" | `["Students have been taught:"]` — the stem, neither item | both items | transcription |
| t3-w02 | nine evaluation questions, no answer key | nine researcher-computed answers, rendered to the model as "(expected answer: 32cm)" | answers empty; the renderer no longer sends one | provenance |
| t3-w02 | evaluation Q8 = prose + a drawing marked 1cm, 5cm, 9cm | the question string carried 286 characters of raw TikZ into a condition that receives no figures | drawing source replaced by its measurements, absence stated | parsing |
| t3-w05 | her 2026-08 pages, activities on both core steps | built from the authored supplement (Siyavula Step I, no activities) | rebuilt from the capture; eval set repointed | missing source |
| t3-w04, t3-w06, t3-w09, t3-w02 | intro-step narration she wrote | not transcribed into the binding, so `stimulate_recall` fired nowhere | her narration transcribed into all four | transcription |
| t3-w06, t3-w09 | step titles ending in `*(objective (iii))*`, `*(core → objective 2)*` | transcription markers reaching the generator as her plan | stripped on the way into the plan | provenance |
| all | she writes a bare "STEP 1:" and runs the narration on | transcriber-authored descriptors sent as `step_title` | field dropped from every condition | provenance |
| all | one Duration line, 40 minutes, no per-step split | 10/10/10 and 20/20 apportionments sent as hers | per-step timing removed | provenance |
| all | one materials list per lesson | copied onto every unit, so t3-w05's volume section was handed "shapes of cylinders and spheres" | moved to lesson scope | scoping |
| — | — | C0 and C1 ran different signatures; C1's said "teach this part and leave the rest to its own section" | one shared signature | prompt construction |
| — | the plan fields C0 is denied | C0 read `"entry_behaviour": [], "instructional_materials": []` — told the fields exist and were withheld from it | `prompt_lesson` prunes them, as `prompt_unit` already did for the unit | prompt construction |
| — | t3-w06 objective (i), two constructions in one clause | one compound objective, five steps, Step 2 coded to nothing | split into parallel and perpendicular: five objectives, six steps | scoping |

## Open, awaiting a decision or a source

Errors in her documents that are logged but not yet corrected — each has an issue.

- Worked-example slips in `t2-w09` (a divisor restated, a sign silently corrected).
- `t3-w02`'s "divide both side by 44r" when the division is by 44, and its ambiguous
  "How many triangle has an octagon".
- `t3-w02`'s circumference question, which resolves cleanly only under pi = 22/7 — a
  convention the plan never states.
- `t3-w04`'s properties table: four pyramids drawn, three tabulated.
- `t3-w06`'s conflicting textbook page ranges, and four figures missing the labels their
  own procedure text references.
- `t3-w09`'s "Exercise 17a page 158", which needs the textbook in hand.

## Not corrected, by design

- **`t3-w09`'s objective-assessment tension.** Her design, not her error.
- **`t3-w06` has no Evaluation section at all.**
- **Errors in the generated packs** — an impossible bisection, an out-of-syllabus
  quadratic, a cone given two edges, a composite-figure answer wrong by 5cm. Outcomes,
  not inputs. Human raters should see them.
- **`t3-w05` evaluation Q5** — "Calculate the volume of the shape below", with no shape
  drawn. Her cleaning log records the decision not to reconstruct it: nothing in the plan
  determines the shape, and the students' classwork was set from the textbook by
  reference, so it cannot be assumed to be this question.
- **Spelling and agreement** — "familior", "It has three faces attogether". Meaning-
  preserving normalisation only; substantive ambiguity is never resolved on the
  researcher's judgement, and "How many triangle has an octagon" is ambiguous in its
  mathematics, not only its grammar, so it needs the teacher rather than a decision here.
  **Superseded 2026-08-23.** The judgement above holds for a reader who has her note: its
  Polygons table heads a column "No of triangle ($n-2$)" and gives Octagon | 8 | 6, so the
  ambiguity is resolved by context. It does not hold for a generation condition. C1
  receives the evaluation questions and NOT the note, so the table that resolves the
  question is exactly what C1 lacks, and under C1 the question is unanswerable as she
  meant it. The question now names the decomposition her table defines. The answer, the
  objective and what is assessed are unchanged; `teacher.md` still carries her wording.

## Why the checklist was applied to all six

Every correction above was found by running the same checks across the whole set, not by
investigating the lessons where a condition scored badly. That ordering is what makes the
corrections defensible: `t3-w09` — the lesson C1 apparently lost worst on the old proxy —
received no correction beyond the ones applied everywhere.
