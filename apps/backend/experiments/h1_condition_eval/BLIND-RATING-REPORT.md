# Blinded rating of C0–C3 on the worksheet artefact — 2026-08-11

One generation, **two independent blinded passes**: 6 field lessons × 4 conditions × 3
draws = 72 packs, judged twice = **144 judgments, 576 dimension-scores.**

- `c0c3-worksheet` — the first pass. Its packets carried a numbering defect described below.
- `c0c3-renumbered` — the same `run.json`, byte-for-byte, re-rated after that defect was
  fixed. Fresh judges, fresh candidate ids, no id shared with the first pass.

A **manipulation check**, not the study's endpoint. It asks whether the lesson-plan
information C1 receives becomes *visible* to a reader holding the teacher's plan and one
anonymous pack. The expert raters answer the endpoint.

Per-judgment evidence is in each run's `rating/RATING-RESULTS.md`.

## The headline

**The manipulation did not land, in either pass.** Pooling both — which is 2 judges per
candidate over 3 draws, the reduction this study had never tried — C1 against C0 is null on
all four dimensions, and the dimension the framework's whole claim rests on is the one that
moves least.

| dimension | C1−C0 | p | C2−C0 | C3−C0 |
| --- | ---: | ---: | ---: | ---: |
| Objective and curriculum alignment | −0.19 | .812 | +0.11 | +0.17 |
| Taught-lesson alignment | +0.06 | .500 | **+0.50** | **+0.53** |
| Scope and conceptual correctness | +0.53 | .156 | +0.14 | **+0.69** |
| Student-facing clarity and usefulness | +0.03 | .500 | +0.03 | +0.31 |

One-sided Wilcoxon signed-rank over the six lessons. With n=6 the floor is p=.0312, so
nothing here could have been significant on four wins — but three of C1's four dimensions
do not reach even a majority of lessons, and one is negative.

**What does separate is the evidence step, not the plan step.** Pooled arm means:

| arm | Objective | Taught-lesson | Scope/correctness | Clarity |
| --- | ---: | ---: | ---: | ---: |
| C0 | 4.11 | 3.08 | 2.94 | 3.11 |
| C1 | 3.92 | 3.14 | 3.47 | 3.14 |
| C2 | 4.22 | 3.58 | 3.08 | 3.14 |
| C3 | **4.28** | **3.61** | **3.64** | **3.42** |

C3 is above C0 on every dimension and is the top arm on all four. C2 and C3 both clear both
no-evidence arms on taught-lesson alignment — the single place the ladder behaves as
designed, and the best p any comparison in this study reaches (.125 for C3).

## The two passes, and what one judge is worth

The two passes rated **prose-identical packs**. The only differences are a fixed practice
numbering and a fresh judge. So the movement between them is a direct measurement of judge
noise with generation held constant — something this study has not had before.

| arm | scores that moved | of | mean size of a move |
| --- | ---: | ---: | ---: |
| C0 | 13 | 24 | 0.44 |
| C1 | 15 | 24 | 0.49 |
| C2 | 15 | 24 | 0.38 |
| C3 | 15 | 24 | 0.44 |

**More than half of every arm's scores moved, by about half a point, on identical prose.**
A margin under ~0.5 read from one judge per candidate is not a finding. That retires the
open question the previous report left — *"two or three judges per candidate is the next
reduction available, and nothing here has tried it"* — with a number.

It also means the endpoint's instability across the passes is noise, not news:

| dimension | pass 1 (C1−C0) | pass 2 (C1−C0) |
| --- | ---: | ---: |
| Objective and curriculum alignment | +0.06 (p=.500) | −0.44 (p=.922) |
| Taught-lesson alignment | +0.17 (p=.312) | −0.06 (p=.750) |
| Scope and conceptual correctness | +0.56 (p=.141) | +0.50 (p=.156) |
| Student-facing clarity and usefulness | −0.06 (p=.625) | +0.11 (p=.312) |

Scope is the one margin that holds its size across both passes. Objective alignment swings
half a point and changes sign, which is exactly what a 0.44–0.49 noise floor predicts.

## The numbering defect, and what it was actually worth

The first pass's worksheet numbered each practice item into an ordered list while **51% of
C2's and 56% of C3's prompts already began with their own number** — copied out of the
teacher's numbered task lists — against 17% of C0's and 18% of C1's. The page read
*"1. 1. Simplify 4n+3n×10."* Twenty of that pass's 288 dimension-scores flagged it, 17 of
them on C2/C3, on the clarity dimension.

It was a real defect, directional against the treatment, and worth fixing: 277 duplicate
numbers dropped across the run, 213 of them on C2/C3, and 63 genuine sub-step runs kept and
re-lettered as a second level rather than flattened.

**It was not, however, what was holding the grounded arms down.** Clarity between the
passes:

| arm | pass 1 | pass 2 | change |
| --- | ---: | ---: | ---: |
| C0 | 3.22 | 3.00 | −0.22 |
| C1 | 3.17 | 3.11 | −0.06 |
| C2 | 3.11 | 3.17 | **+0.06** |
| C3 | 3.39 | 3.44 | **+0.06** |

The grounded arms moved in the predicted direction and by 0.06 — an eighth of the noise
floor. The earlier reading that "C2's and C3's clarity in this run is a floor, not a
measurement" was right about the direction and wrong about the size; the defect cost them
almost nothing. Worth knowing before the human raters see the packets, not worth
reinterpreting a result over.

## Why C1's signal is gone

Across the three superseded runs on the previous artefact, C1 never lost a lesson on
taught-lesson alignment in eighteen comparisons. It now ties or loses most of them. Two
things changed under it.

**C1's payload is the plan's design, not its prose.** `student_tasks` and
`assessment_points` still carry her real questions, so the channel is open — but the
verbatim step narration is gone, and C1 no longer receives the answers. That was removed
deliberately, as a confound.

**The reference sheet now shows every judge the lesson sequence in her own words.** Both
arms are rated against the same reference by design, but a C0 pack that lands on the
lesson's shape generically now gets credit for it, where before C1's specificity stood out
against a thinner reference.

The judges' language tracks this. Across pass 1's 288 dimension-scores, claims that a pack
reuses the teacher's *specific* items: C0 1, C1 7, C2 4, C3 4. C1 still leads — but most of
its hits are now criticism, marking packs down for reusing *their own* worked-example
numbers as practice.

## Other findings, counted across pass 1's 288 dimension-scores

| # | what the judges saw | C0 | C1 | C2 | C3 | verdict |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | a figure described but not drawn | 4 | **10** | 1 | 1 | **the ladder working** |
| 2 | raw LaTeX markup in visible text | 4 | 4 | 3 | 3 | **pipeline gap — open** |
| 3 | a dangling *"shown below"* reference | 2 | 2 | 2 | 4 | **generation fault** |
| 4 | a wrong answer or wrong reasoning | 5 | 3 | 5 | **0** | **generation fault; C3 clean** |
| 5 | a duplicated practice item | 1 | 3 | 1 | 2 | **generation fault** |
| 6 | an answer printed under its own question | 0 | 0 | 0 | 0 | **closed by the restructure** |
| 7 | a control character where `\times` belonged | 0 | 0 | 0 | 0 | **closed, issue #162** |

Row 1 is not a defect: C0 and C1 receive no figures by design and the reference sheet tells
the judge the teacher drew on the board, so the no-evidence arms are marked for an absence
the ladder creates.

Row 4 is the one place C2 and C3 separate — **no judge found a mathematical error in any C3
pack**, against five in C0 and five in C2. C3 is C2 plus validation and repair.

Rows 6 and 7 are the two closed issues, confirmed closed on real data: zero answers under
their own question across 288 scores, where the previous artefact had them in 9 of 12 cells,
and zero eaten LaTeX commands.

## Two draws that are short, not bad

Two of C1's eighteen draws came from composition loops that gave up mid-section:
`t3-w04` draw 1 (2 sections where the lesson has 3) and `t3-w06` draw 3 (a section with no
practice). Excluding them as a sensitivity check on pass 1 improved every C1−C0 margin and
made none significant. They inflate C1's within-arm spread; they do not carry the result.

## Standing caveats

**No comparable prior run.** All four judged runs from before the restructure rated a
different artefact, so `--against` is only meaningful between these two passes.

**Two judges per candidate is now the floor, not the ceiling.** The 0.38–0.49 movement
measured here is the pooled estimate's own noise; three or more judges would narrow it
further, and the design has never been run that way.

**n=6.** The registered analysis cannot return p < .0312 whatever the effect. A margin this
study can detect has to win all six lessons.

## What still stands from the superseded runs

The three runs of 2026-08-09 rated the previous artefact — a flat block list with each
answer in the same paragraph as its question — so their scores are not a baseline these can
be compared against. Full text in git at `8208805`. What carries over: the measured need for
repeats, and the data-issue triage, whose conclusion was that **no new defect was found in
the teacher's material** — the two findings that looked like gaps in her plan are real
properties of what she wrote and belong in the thesis as findings.
