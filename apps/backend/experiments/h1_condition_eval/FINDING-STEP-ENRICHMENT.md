# Declaring what she taught in eight thin steps did not move the endpoint

Runs `full-v3-enriched` and `full-v7-enriched`, 2026-08-24. Against `full-v3` / `full-v7`.

Eight of the cohort's seventeen core steps said four words or fewer beyond their own
objective, so C1 was conditioned on the objective restated rather than on her lesson.
Each now names what her own note covers, and t3-w06's five construction steps say she
draws each construction on the board while the class replicates it. The question was
whether that improves the pack.

**It does not, measurably.** The cohort endpoint moved +0.67 → +0.78, which is inside the
floor. Under the full plan it moved +0.72 → +0.67. Lessons where C1 beats C0 on the
endpoint went 4/6 → 3/6.

## Why this run can say that, where earlier ones could not

The enrichment changed four of six plans, and under the frozen definition it changed the
delivered request for only **two cells**: t3-w06/C1 and t3-w09/C1. Everything else —
every C0, and C1 on four lessons — received a **byte-identical input** and was drawn and
judged again anyway.

So the run carries its own control. Thirty same-input cells measure what the pipeline
moves when nothing changed, in the same passes, under the same judge:

| dimension | mean abs. move | worst |
|---|---:|---:|
| Objective and curriculum alignment | 0.10 | 0.33 |
| **Taught-lesson alignment** | **0.20** | **0.67** |
| Scope and conceptual correctness | 0.38 | 0.83 |
| Student-facing clarity and usefulness | 0.20 | 0.50 |

40 of the 44 fingerprinted inputs are identical between the two runs; only the four
changed plans differ. Nothing else about the arm moved.

## The two treated cells, read paired

| | C0 *(input unchanged)* | C1 *(input changed)* | C1 − C0 |
|---|---:|---:|---:|
| **t3-w06** before | 3.33 | 3.17 | −0.17 |
| **t3-w06** after | 4.00 | 3.83 | −0.17 |
| move | **+0.67** | **+0.67** | **+0.00** |
| **t3-w09** before | 3.00 | 4.00 | +1.00 |
| **t3-w09** after | 2.67 | 4.33 | +1.67 |
| move | −0.33 | +0.33 | +0.67 |

t3-w06's C1 rose two-thirds of a point — and its C0 rose by **exactly the same amount on
a byte-identical input**. The rise is the lesson drifting under the judge, not the
enrichment; paired, it is +0.00. That is the whole reason the endpoint is a paired
statistic.

t3-w09 is the only genuine movement, at +0.67. It is one lesson, and the C0 cells whose
inputs never changed span −0.33 to +0.67 between the same two runs. A single paired
+0.67 assembled from two ±0.33 half-steps is the size of that spread, not larger than it.

**A correction worth recording.** Reading the treated cells against the *pooled* floor
of 0.20 marks both of them as clearing it. That is wrong, and t3-w06 is the
counter-example: pooled floors assume the lessons move alike, and they do not — one C0
moved +0.67 while another moved 0.00. The paired difference cancels the lesson-level
drift; a pooled floor applied to unpaired cells re-imports it.

## What did change

The set-square method reaches the pack. Under `v7-full`, t3-w06's C1 mentions a set
square in 3/3 draws against 2/3 before, 128 mentions against 9. Her method is arriving.
It is not scoring.

Two markers that are **not** evidence, named so they are not mistaken for it.

t3-w02's invented *secant* falls from 2/3 draws to 0/3 under v3 — where **t3-w02's input
did not change at all**. That marker is a coin flip.

The equilateral-triangle justification falls from 3/3 draws to 2/3, and an earlier
version of this finding read that as her arc method displacing an invention. **It is not
an invention.** Her two arcs give BX = XA = BA, so the triangle *is* equilateral and that
is exactly why her construction yields 60°. The packs were supplying correct reasoning
for her own method; losing it in one draw of three is a small loss, not a gain.

## The error the judge did catch

One draw in twenty-six — `full-v7-enriched` C1 repeat 1 — builds the 60° angle with
**three** arcs instead of her two, placing B, C and D at 60° intervals around the first
arc and then joining O to D. That is the standard **120°** construction, and the pack
labels it 60°. Its stated reason, "the three arcs create an equilateral triangle B-C-D",
is false as well: BC = CD = r but BD = r√3.

Nothing in C1's input for that step says *three*, *third* or *equilateral* — the whole of
what it receives is "constructs angle 60° on the board step by step by compass arcs of
equal radius from the endpoint". Her note holds the correct two-arc procedure, and C1 by
definition never receives the note. So there was no source to copy and none to check
against: the model reconstructed the construction from memory and inserted one arc too
many. The blind judge marked it down for exactly that, unprompted.

It is one draw in twenty-six and does not generalise. What it does show is the shape of
C1's ceiling — naming a method is not carrying it, and the procedure lives in the note.

## What this does not say

Not that her plan carries nothing. C1 still beats C0 by +0.58 / +0.78 / +0.36 / +0.31
across the four dimensions, and t2-w09 alone is +2.67 on the endpoint. What it says is
that the eight steps which restated their objective were not what was holding the rest
back, and that the C1 ceiling is somewhere else.

The inputs stay. They are more faithful to her lesson than what they replaced, every
list is sourced to her own note, and each is declared in the lesson's `_cleaning-log.md`.
Fidelity was worth having on its own terms; it is reported here as a null result rather
than quietly kept for its direction.
