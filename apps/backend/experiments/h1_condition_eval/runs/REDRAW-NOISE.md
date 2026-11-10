# Re-draw noise — `c0c3-deepseek-native` against `c0c3-prism-objective`

Same arm, same judge. Inputs changed on: t3-w05. The other 5 lessons re-drew identical material.

## The floor, from the lessons whose inputs did not change

| rubric | mean \|move\| | worst | cells that moved |
|---|---:|---:|---:|
| Objective and curriculum alignment | 0.025 | 0.33 | 2/20 |
| Taught-lesson alignment | 0.108 | 0.50 | 8/20 |
| Scope and conceptual correctness | 0.208 | 0.50 | 13/20 |
| Student-facing clarity and usefulness | 0.067 | 0.33 | 5/20 |

On the endpoint (Taught-lesson alignment) a cell moved **0.11 on average, 0.50 at worst** across 20 unchanged cells, and the C1−C0 *pair* moved up to **0.50**.

The pair figure is the one that matters: it is the same quantity the study's endpoint is a signed-rank over. Any per-lesson C1−C0 smaller than it was never distinguishable from a re-draw.

## The endpoint, lesson by lesson

| lesson | C1−C0 before | C1−C0 after | change | input |
|---|---:|---:|---:|---|
| t2-w09 | +1.83 | +1.83 | +0.00 | identical |
| t3-w02 | +0.33 | +0.50 | +0.17 | identical |
| t3-w04 | +0.33 | +0.33 | +0.00 | identical |
| t3-w05 | +0.33 | +0.00 | -0.33 | **edited** |
| t3-w06 | +0.50 | +0.17 | -0.33 | identical |
| t3-w09 | +1.83 | +1.33 | -0.50 | identical |


## What this does to H1a

`c0c3-prism-objective` is now a single run carrying all six lessons on the corrected eval
set, so the endpoint no longer has to be spliced across two runs.

| lesson | C1−C0 | vs the 0.50 floor |
|---|---:|---|
| t2-w09 | +1.83 | **clears it** |
| t3-w09 | +1.33 | **clears it** |
| t3-w02 | +0.50 | at it |
| t3-w04 | +0.33 | under |
| t3-w06 | +0.17 | under |
| t3-w05 | +0.00 | under |

5 of 6 positive, **none negative**, mean **+0.69**, Wilcoxon exact two-sided **p = 0.0625** —
the floor at five non-zero pairs. The same figure the splice gave, now from one run.

**But the signed-rank is counting signs the instrument cannot resolve.** Four of the six
pairs are at or below what an unchanged input moves between runs. The test weights a +0.17
and a +1.83 equally as evidence of direction, which is how six coin-flippable lessons
produce a tidy p.

The defensible statement of H1a is not a p-value over six lessons. It is:

> Conditioning on the lesson plan moves taught-lesson alignment **decisively on two of six
> lessons** (+1.83 and +1.33, both well clear of the 0.50 re-draw floor), and by an amount
> this instrument cannot resolve on the other four. No lesson moved negative in either run.

That is a weaker claim than p = 0.0312 and a much better supported one.

## And it retires a finding from earlier today

`t3w05-prism-objective` was read as showing that naming the prism in the objective lifted C0
(3.67 → 4.00) while C1 stayed at 4.00 — "the arm with only the objective to go on was being
penalised by an objective that under-described the lesson."

The direction **replicates**: C0 is 4.00 on t3-w05 in this run too, from two independent
generations on the corrected objective against 3.67 on the old one. But the move is 0.33,
and on this evidence t3-w06's pair moved −0.33 and t3-w09's −0.50 on **inputs that did not
change at all**. A 0.33 shift is inside the noise.

So the mechanism is plausible and its direction has replicated twice, and it is not a
measured effect. It should be reported as the reason the record was corrected — which stands
on the teacher's own confirmation, not on a score — and not as evidence that the correction
moved anything.
