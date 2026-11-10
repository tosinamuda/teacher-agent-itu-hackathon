# The plan helps, the note costs, repair recovers a little

Run `c0c3-deepseek-native`, 2026-08-24. Six lessons, four conditions, three draws, two
Sonnet 4.6 passes — 72 packs, 144 judgments. DeepSeek Flash on `/responses` with native
tool calls and an enforced json_schema: 221 loops, none abandoned. C1 and above carry the
full plan.

## The three rungs

| rubric | C0 | C1 | C2 | C3 | **C1−C0** | C2−C1 | C3−C2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Objective and curriculum alignment | 4.61 | 5.00 | 4.86 | 4.94 | **+0.39** | −0.14 | +0.08 |
| **Taught-lesson alignment** | 3.47 | 4.33 | 4.22 | 4.28 | **+0.86** | −0.11 | +0.06 |
| Scope and conceptual correctness | 4.50 | 4.89 | 4.31 | 4.44 | **+0.39** | **−0.58** | +0.14 |
| Student-facing clarity and usefulness | 4.86 | 4.92 | 4.72 | 4.81 | +0.06 | −0.19 | +0.08 |

Three of C1's four differences clear twice the spread of their own draws. Every one of
C2's is negative. None of C3's is separable.

## C1 − C0: every lesson, same direction

| lesson | C0 | C1 | C1−C0 |
|---|---:|---:|---:|
| t2-w09 | 3.00 | 4.83 | **+1.83** |
| t3-w02 | 4.00 | 4.33 | +0.33 |
| t3-w04 | 3.67 | 4.00 | +0.33 |
| t3-w05 | 3.67 | 4.00 | +0.33 |
| t3-w06 | 3.50 | 4.00 | +0.50 |
| t3-w09 | 3.00 | 4.83 | **+1.83** |

Six non-zero pairs, six positive. **Wilcoxon signed-rank p = 0.0312 two-sided** — the
floor at n = 6, and the first time this study has reached it. No lesson ties, so nothing
is discarded.

**It is still not the confirmatory endpoint.** That is C1 vs C0 on the frozen generator,
gpt-oss, where it is p = 0.25. This is DeepSeek, and the harness was rebuilt today. It
belongs in the writeup as a secondary analysis saying so, not as the headline.

## C2 − C1: half of this was our record, not her note

| step | p (signed-rank, endpoint) | lessons improved |
|---|---:|---|
| C1 − C0 | **0.0312** | 6 of 6 |
| C2 − C1 | 0.625 | 2 of 5 non-zero |
| C3 − C2 | 0.500 | 2 of 2 non-zero |

The cost lands on scope: **−0.58 pooled**, which clears the spread, and −1.83 on t3-w05
alone. The reason is not errors. The judge is explicit:

> "All mathematical content presented is conceptually and numerically correct, **but the
> pack exceeds the lesson boundary by introducing triangular prism volume, which was
> neither taught nor listed as an objective**."

Her note carries more than her objectives do. Handed to a generator it drags the pack
past the lesson boundary, and a rubric that scores staying inside that boundary marks it
down. The plan is a fence; the note is not, and adding the note takes the fence away.

That inverted the intuition the conditions were built on — and it was half wrong.

### The correction, `t3w05-prism-declared`

The judge said the prism was "neither taught nor listed as an objective". The second half
was true. **The first was false**: her note for that step carries a `#### Volume of prism`
section with a worked example, `fig-03`, and her own formula. She taught it; her plan did
not record it; the judge reads the plan.

So the only conditions that could surface the prism were the ones that receive her note,
and the rubric marked them down for it. The instrument penalised C2 and C3 for being
faithful to the lesson.

The prism is now declared in her Step II narration, and t3-w05 was regenerated and
re-judged. The manipulation check is clean — C1 mentions the prism in 0/3 draws before
and 3/3 after; C0, whose input never changed, stays at 1/3.

| t3-w05, C2 − C1 | before | after |
|---|---:|---:|
| Objective | −0.83 | **+0.00** |
| Taught-lesson | −0.17 | **+0.17** |
| **Scope** | **−1.83** | **−0.33** |
| Clarity | −0.50 | **+0.00** |

C2's scope went 3.00 → 4.17, against a C0 control that drifted −0.50 on an unchanged
input. The penalty was the record, not the note.

### What survives, pooled with the corrected lesson

| rubric | C2 − C1 as first reported | with t3-w05 corrected |
|---|---:|---:|
| Objective | −0.14 | **+0.00** |
| Taught-lesson | −0.11 | −0.06 |
| Scope | **−0.58** | **−0.33** |
| Clarity | −0.19 | −0.11 |

The note's cost roughly halves and only scope is left above trivial. C1 − C0 is unmoved
or slightly stronger — the endpoint goes +0.86 to +0.92 — so nothing about the plan's
result depended on this.

**So the claim to carry forward is much weaker than the original.** The note is not
demonstrably a liability. One lesson's penalty was our under-recording of what she taught;
what remains is −0.33 on scope across six lessons, close to the ±0.5 lesson-level noise
the control showed. It is not evidence that the note hurts, and the earlier version of
this section said it was.

An audit found only 4 of the cohort's 37 note headings unnamed in the plan, and three of
those were matching artefacts, so there is no second prism waiting to be found. The
remaining −0.33 has no identified cause and should be treated as unexplained rather than
attributed.

## C3 − C2: repair recovers part of what the note cost

All four differences are positive and none is separable pooled. Per lesson it is visible
where it acts: t3-w06 scope 4.50 → 5.00, t3-w05 scope 3.00 → 3.50. The critic raised 3.67
findings per pack and repaired 15 of 18, and what it catches is exactly the note's
overflow — alt-text descriptions in learner-facing prose, figure references, the stray
prism.

So repair does the job it was built for. With t3-w05 corrected its pooled differences fall
to about zero (+0.00 to +0.03), because much of what it was recovering was the scope
penalty that should never have been applied. What C3 earns on a correct record is
therefore untested here.

## What this says about the study's shape

Read together, the rungs say the plan is doing the work and the note is not the next step
up from it. If that holds on the frozen generator it is a finding about lesson plans as
CONSTRAINTS rather than as content — the plan tells a generator what the lesson was for,
and that is worth more than telling it everything the lesson contained.

Untested here, and the obvious next question: whether a C2 that receives the note but
keeps the plan's scope fence — the note as evidence, the objectives as boundary — beats
both. That is a condition the study does not currently have.
