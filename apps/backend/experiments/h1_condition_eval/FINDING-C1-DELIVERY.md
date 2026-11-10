# Finding: C1 was under-delivered, unevenly, across the frozen cohort

Hand-written. The measurements it cites are generated — see
[`COHORT-INPUT-AUDIT-2026-08-14.md`](COHORT-INPUT-AUDIT-2026-08-14.md), regenerate with
`uv run python -m scripts.prompt_snapshots.cohort_audit`.

**Which call lost which key is in `delivery-audit/`,** one PDF per lesson plus a combined
one, printable and made to be marked up against her pages. Regenerate with
`uv run python -m scripts.prompt_snapshots.delivery_pack`.

## What 17 is

The six frozen lessons produce **17 generation units** under C1 — one per **core step**, not
per objective — and each unit is one independent model call:

| Lesson                | t2-w09 | t3-w02 | t3-w04 | t3-w05 | t3-w06 | t3-w09 | total  |
| --------------------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| core steps = C1 calls | 3      | 3      | 2      | 2      | 5      | 2      | **17** |

So `17/17` means the key was present in the rendered prompt of every call in the study.
`4/17` means it was present in four of them and missing from thirteen. C0 uses one unit per
objective and lands on the same counts, so the two arms are compared call for call.

## Why three rows are not 17/17

Each has a different mechanism. None is a bug in the generator; all three are the pipeline
faithfully passing on what the plan data does or does not carry.

### `instructional_events` — 15/17

Reads `step.activities`, coded to Gagné events.

| Lesson | activities written | steps coding to nothing | delivered |
| ------ | ------------------ | ----------------------- | --------- |
| t2-w09 | 14                 | 0                       | 3/3       |
| t3-w02 | 4                  | 1                       | 2/3       |
| t3-w04 | 4                  | 0                       | 2/2       |
| t3-w05 | 6                  | 0                       | 2/2       |
| t3-w06 | 9                  | 0                       | 5/5       |
| t3-w09 | 1                  | 1                       | 1/2       |

Both misses are steps carrying **zero activities** — `t3-w02/step-t3w02-04` and
`t3-w09/step-t3w09-03` — so there is nothing to code and the field is dropped. Every step
that had an activity coded to at least one event, so the coder is not dropping anything.
This row is close to complete and is not the problem.

Note the spread in the source column: t2-w09 records 14 activities and t3-w09 records one.
Delivery is binary per call, so that unevenness does not show in the ratio — but a step with
one activity and a step with five both count as delivered, and they are not carrying the
same amount of lesson plan.

### `assessment_points` — 10/17

Reads the questions on an `evaluation` step, grouped by the objective each question names.
A unit gets the field only if **its own objective** has at least one evaluation question.

| Lesson     | evaluation questions | core objectives covered |
| ---------- | -------------------- | ----------------------- |
| t2-w09     | 5                    | 3/3                     |
| t3-w02     | 9                    | 2/3                     |
| t3-w04     | 5                    | 2/2                     |
| t3-w05     | 4                    | 1/2                     |
| **t3-w06** | **0**                | **0/5**                 |
| t3-w09     | 3                    | 2/2                     |

Two causes: t3-w06 has **no evaluation step at all**, which accounts for five of the seven
misses; and on t3-w02 and t3-w05 the evaluation questions are tagged to some objectives and
not others, so a core step whose objective drew no question gets nothing.

### `student_tasks` — 4/17

Reads the `practice`-typed blocks of a core step.

| Lesson     | blocks | `explanation` | `worked_example` | `practice` | delivered |
| ---------- | ------ | ------------- | ---------------- | ---------- | --------- |
| t2-w09     | 15     | 3             | 9                | 3          | 3/3       |
| t3-w02     | 17     | 7             | 10               | 0          | 0/3       |
| t3-w04     | 6      | 6             | 0                | 0          | 0/2       |
| t3-w05     | 6      | 5             | 0                | 1          | 1/2       |
| t3-w06     | 8      | 5             | 3                | 0          | 0/5       |
| t3-w09     | 5      | 5             | 0                | 0          | 0/2       |
| **cohort** | **57** | **31**        | **22**           | **4**      | **4/17**  |

Four practice blocks exist, so four units can carry the field — and **four of the six
lessons have none at all**. t2-w09 carries three of the four.

**This is the row with a candidate data defect behind it, not only a data absence.** The
teacher's verbatim notes contain task-shaped lines that no `practice` block captures. The
first pass found four and read them as probably-mistyped practice. **Re-probed across the
whole cohort with what follows each line, they are twelve, and none of them is practice.**

| Step | lines | she solved it | she drew the next stage | open |
| --- | ---: | ---: | ---: | ---: |
| t2-w09 / step-t2w09-04 | 4 | 4 | 0 | 0 |
| t3-w05 / step-t3w05-03 | 1 | 1 | 0 | 0 |
| t3-w06 / step-t3w06-02 | 2 | 0 | 2 | 0 |
| t3-w06 / step-t3w06-03 | 2 | 0 | 2 | 0 |
| t3-w06 / step-t3w06-04 | 1 | 0 | 1 | 0 |
| t3-w06 / step-t3w06-05 | 1 | 0 | 1 | 0 |
| t3-w06 / step-t3w06-06 | 1 | 0 | 1 | 0 |
| **cohort** | **12** | **5** | **7** | **0** |

What follows a line is what separates the two readings, and it is in her note rather than in
a judgement about her note. A line she then solves on the page is a worked example she wrote
out: `Calculate the volume of the prism below.` on t3-w05 is followed by a figure and then
`Solution:` and a full derivation. A line followed by the drawing of that stage is one move
in a construction she performed: every t3-w06 candidate is a numbered move — *Draw a line AB
mark a point Q*, *Place the edge of the set square*, *slide the set square … Draw a line XY*
— each answered by `fig-07`, `fig-08`, `fig-09` in turn. Her plan says so too, in the step's
own block: *"Teacher explains the drawing of perpendicular lines to the students."*

**So the direction of the first reading was wrong.** `student_tasks` delivery does not
double under a **retype**: none of the twelve lines is work she set, so there is no
mistyped practice block to recover. R2, as written, is empty.

That is not the same as saying the field is undeliverable — see the Student Activity column
below, which is where the recoverable half turns out to be.

**And a third possibility the note probe could not see.** `student_tasks` reads a step's
`practice` blocks — question text. Her plan also has a **Student Activity** column, and
reading it against delivery separates the 13 misses three ways:

| what her plan records the students doing | steps | reading |
| --- | ---: | --- |
| nothing — no student activity at all | 5 | genuine absence |
| receptive only — *take notes*, *listen*, *copy worked examples* | 3 | genuine absence of practice |
| **work she set, not question-shaped** — *construct parallel lines*, *construct angle 90 degrees* | **4** | **a definition gap, not a data gap** |

The pipeline is exonerated: **every step that has a practice block delivers the field, and
every step that lacks one does not — 17 of 17.** Nothing is dropped in transit.

But four steps carry student work that `student_tasks` cannot represent, because it is
defined to read question text and she set a *construction*. All five are on `t3-w06` and
`t3-w02`. C1 is told `elicit_performance` happened and is not told what was performed:
"construct angle 90 degrees" reaches no condition. That is the study's own definition
losing information her plan contains, and it is worth **4 of the 13 misses** — delivery
is 8/17 rather than 4/17 under a definition that reads the activity column too — and
8 rather than 9 because the coder's verdict on one of them does not survive being
read. `STUDENT-WORK-CONFIRMATION.md` carries all eighteen for checking against her
pages; `student_work.json` is the verdict the pipeline uses.

**This is still the transcription, not the page.** The probe reads her note as frozen; a
source page could carry a *Student Activity* heading the transcription dropped, and that is
the one thing it cannot see. `delivery-audit/` prints every one of the twelve lines with the
paragraph that decides it and a box to tick, so settling it is a reading pass rather than a
re-derivation.

## What this does and does not say about the null

**Says:** C1 − C0 was smaller than designed, and uneven across lessons. C1 is not one
condition across the cohort but a ragged set of them — six keys on every call of t2-w09,
four on every call of t3-w06. At n = 5 that is unmodelled within-arm variance sitting on top
of a reduced contrast.

**Does not say:** that the manipulation never arrived. Three of the six keys reached every
call. This is not an explanation of the null; it is one of the things an explanation has to
account for.

**Worth holding beside it:** the evidence step was fully delivered — C2 and C3 carried
evidence on every call of every lesson, C0 and C1 on none. The arm whose manipulation
arrived intact is the arm that separated.

## Remediation

In order. The first two are the researcher's, and neither may be scripted — `notes-clean/`
is the model-visible generation copy and is hand-edited file by file.

**R1 — Confirm the candidate lines against the source pages. Answered from the
transcription; the pages are the last word.** Print `delivery-audit/delivery-t3-w06.pdf` and
`delivery-t3-w05.pdf`, which carry all twelve lines with the paragraph that decides each and
a box per line, and read them against the transcripts. What the note itself says is that
five are worked examples and seven are moves in a construction she performed — none is work
she set. The pages can only overturn that by showing something the transcription dropped.

**R2 — Correct the block typing, if and only if R1 overturns the reading above.** As the
evidence stands there is nothing here to fix: the practice content is absent from her plans,
not mistyped in them. If a page does turn one up, the fix goes the normal way — a data fix,
hand-edited file by file, then a labelled run over the frozen set and a comparison on a
metric with a known floor, per
[`COMPARING-A-PROMPT-CHANGE.md`](../../tests/snapshots/prompts/COMPARING-A-PROMPT-CHANGE.md).
It produces a NEW run beside the frozen record; it cannot revise the preregistered H1a
result, which was measured on the delivery described above.

**R3 — State the delivery rate as a study limitation regardless of R1 and R2.** The H1a
endpoint was measured on a C1 that carried its sixth key on 24% of calls. That is true
whatever the transcription turns out to say, and it belongs in the write-up rather than in
a fix.

**R4 — Make delivery a pre-flight check on every future run.** The study ran without anyone
knowing C1 was 24% delivered on one key, and nothing would have said so. A check that
reports per-arm delivery before a run spends model budget turns this class of defect from a
post-hoc discovery into a refusal to start.

**R5 — DONE: `student_tasks` now reads the work she set, not only the work she wrote as a
question.** The field was defined on question text, which her plans structurally often do
not carry; five steps set a construction in the Student Activity column instead. It now
falls back to that column, and only to the half of it her Gagné coder reads as
`elicit_performance` — a fallback rather than an addition, because on every step of the
cohort carrying both, the activity is a label for the questions beside it.

**Delivery: 4/17 → 8/17**, all of the gain on `t3-w06` (0/5 → 4/5) and `t3-w02`. C1's
definition is at version 3 and `C1-DEFINITION.md` records why. The exclusion it narrows —
"the raw activity narration never travels" — still holds for every teacher activity and
for student reception; a wire test asserts all three halves separately.

## Read beside the separability pass

[`FINDING-BLIND-SEPARABILITY.md`](FINDING-BLIND-SEPARABILITY.md) asks the other half of the
question — not whether the manipulation arrived, but whether the packs it produced read as
different. A blinded reader scores 8/18 (44%, p=.76) on C0 versus C1, at chance, against a
weak positive control of 12/18 on C0 versus C3. A manipulation that arrived partially
produced output that does not read as different; neither finding is the whole story, and
neither establishes the counterfactual of a fully delivered C1.
