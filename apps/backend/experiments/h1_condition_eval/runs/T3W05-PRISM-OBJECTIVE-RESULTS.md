# `t3w05-prism-objective` — judged

C0–C3 on `t3-w05` after `lo-t3w05-02` was amended to read "find the volume of a cube, a cuboid
and a prism". deepseek-v4-flash over `/responses` with native tools, `compose-v2`, `v7-full`,
three draws a cell; Sonnet 4.6 judge, two passes, 24 ratings.

**C0 changes here.** Objectives are the one input C0 receives, so this is not a control-holding
comparison against `t3w05-prism-declared` — and C0 is exactly where the movement is.

## The run

| condition | objective | taught | scope | clarity |
|---|---|---|---|---|
| C0 | 5.00 | 4.00 | 4.50 | 5.00 |
| C1 | 5.00 | 4.00 | **4.83** | 5.00 |
| C2 | 5.00 | **4.33** | 4.33 | 5.00 |
| C3 | 5.00 | 4.17 | 4.50 | 5.00 |

Objective-curriculum alignment and clarity are at **5.00 on all 24 ratings**. Only taught-lesson
alignment and scope discriminate at all on this lesson.

Judge repeat noise, same text rated twice: **4 of 48 paired ratings moved (8%), mean |Δ| 0.083,
max 1**. Much tighter than this instrument's usual floor, and the ceilings are why — two of the
four dimensions cannot move.

## What the record correction did

`t3-w05`'s taught-lesson alignment across the three runs its input passed through:

| run | what the input carried | C0 | C1 | C1−C0 |
|---|---|---|---|---|
| `c0c3-deepseek-native` | objective "cube and cuboid"; prism nowhere declared | 3.67 | 4.00 | +0.33 |
| `t3w05-prism-declared` | + Step II declares the prism | 3.33 | 4.00 | +0.67 |
| `t3w05-prism-objective` | + the objective names the prism | **4.00** | 4.00 | **+0.00** |

**C0 rose +0.33 and C1 did not move.** That is the mechanism, and it is the right one: C0 reads
nothing but the objectives, so an objective that under-described the lesson was penalising the
arm that had only the objective to go on. C1 already had the plan and was already scoring 4.00.

## Consequence for H1a — the endpoint loses significance

The published ladder result spliced with the corrected `t3-w05` pair:

| lesson | C1−C0 (taught) |
|---|---|
| t2-w09 | +1.83 |
| t3-w02 | +0.33 |
| t3-w04 | +0.33 |
| **t3-w05** | **+0.00** (was +0.33) |
| t3-w06 | +0.50 |
| t3-w09 | +1.83 |

|  | as published | corrected |
|---|---|---|
| positive | 6/6 | 5/6 |
| non-zero pairs | 6 | 5 |
| mean | +0.861 | +0.806 |
| Wilcoxon exact two-sided | **p = 0.0312** | **p = 0.0625** |

**0.0625 is the floor at n = 5.** Every non-zero pair is positive and none is negative; the
result cannot be sharper than this without a sixth non-zero pair. It is no longer under .05.

Two things this is not:

- It is not a weaker effect. The mean barely moves (+0.861 → +0.806) and no pair changed sign.
  What changed is that one lesson's gap closed entirely, costing a degree of freedom the exact
  test cannot spare at this n.
- It is not a clean single-run result. `t3-w05`'s pair comes from a different generation run
  from the other five. Only `t3-w05`'s input changed, so the other five are untouched by the
  edit — but it is a splice, and reporting it as one number from one run would be wrong.

The honest statement of H1a on the corrected record is: **five of six lessons positive, none
negative, mean +0.81, p = 0.0625 — the exact floor at five non-zero pairs.**

To recover a single-run number, regenerate all six lessons on the corrected eval set and judge
that. `t3-w05` is the only lesson whose input moved, so the other five would be re-drawing the
same inputs — which is also the cleanest way to measure this instrument's draw-to-draw noise at
the level the table ranks.
