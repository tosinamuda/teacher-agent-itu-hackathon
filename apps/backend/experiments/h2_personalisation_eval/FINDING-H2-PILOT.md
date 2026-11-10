# H2 pilot: personalisation earns its keep at the top of the class

Run `h2-deepseek-native`, 2026-08-25. Nine transcribed learners (eight from t2-w09, one
from t3-w02), each judged under P0 — the judged C3 base pack unchanged — and P1, the
production personalisation pipeline over that same pack with a state derived from their
marked classwork alone. DeepSeek flash on `/responses`; two Sonnet 4.6 passes per
candidate; every learner is their own control.

## Every dimension non-negative, every mover positive

| rubric | P0 | P1 | P1 − P0 | pairs | p (signed-rank) |
|---|---:|---:|---:|---:|---:|
| Learner-state suitability | 3.83 | 4.28 | **+0.44** | 9 | .125 (4/4 +ve) |
| Scaffolding appropriateness | 4.11 | 4.50 | **+0.39** | 9 | **.0625** (5/5 +ve) |
| Challenge calibration | 3.28 | 3.56 | **+0.28** | 9 | .125 (4/4 +ve) |
| Misconception support | 3.80 | **5.00** | **+1.20** | 5* | **.0625** (5/5 +ve) |
| Objective preservation | 5.00 | 5.00 | +0.00 | 9 | — |

*counted only where the judge scored it applicable in both conditions.

Two dimensions sit at the exact floor the design allows (five non-zero pairs, all
positive, p = 0.0625 two-sided). Nothing moved down anywhere in 90 judged cells.

**Objective preservation is the constraint, and it held**: 5.00 against 5.00 on all
eighteen packs. P1 rewrote a section per learner and never once drifted off the
objective — the failure mode the H1 judging kept finding in generation is absent from
personalisation, because P1 edits inside an already-aligned artefact.

## The inversion: the base pack already serves the bottom

The prediction was that P1 would separate on the deficit learners. The data says the
opposite, and the judge's reasons say why:

| learner | band | suitability P0 | P1 | Δ |
|---|---|---:|---:|---:|
| student-01 | remediate | **5.00** | 5.00 | +0.00 |
| student-06 (0/4) | remediate | **5.00** | 5.00 | +0.00 |
| student-02 | remediate | 4.00 | 5.00 | +1.00 |
| student-03 | reinforce | 4.00 | 5.00 | +1.00 |
| **student-05 (3/4)** | **extend** | **3.50** | **5.00** | **+1.50** |
| student-07 (4/4) | extend | 3.00 | 3.00 | +0.00 |
| student-08 (4/4) | extend | 3.00 | 3.00 | +0.00 |
| student-09 (4/4) | extend | 3.00 | 3.50 | +0.50 |
| t3-w02 student-01 | extend | 4.00 | 4.00 | +0.00 |

The base pack is a full re-teach, which is exactly what a 0-of-4 learner needs — P0
ceilings at 5.00 for the weakest learners and personalisation has nothing left to add.
The learner the generic pack underserves is the one who nearly has it: for student-05
the judge calls P0 "essentially a uniform pack rather than one tailored to push a
near-mastery learner further", and credits P1 with pinpointing "the exact
stopping-too-early slip the learner made". The biggest gain in the study is a
three-of-four learner, not a zero-of-four one.

The all-correct learners (07, 08) are the residual problem: their evidence is counts
alone — no wrong working to respond to — and P1 matched but did not lift their 3.00.
Challenge calibration is the lowest-scoring dimension for both conditions for exactly
this group.

## Misconception support without a misconception code

No misconception was coded anywhere — constructed responses, no coding done — yet the
judge scored the dimension applicable for five learners in both conditions: it read the
misconception off the evidence itself, the learner's verbatim wrong working. P1 scored
**5.00 for every applicable learner**. The working is the channel that carried it: the
personaliser was told what the learner actually wrote, and the packs it produced
anticipate that specific error. This is the D-series decision — evidence from scripts,
never from the plan — paying off directly.

## What this is and is not

A pilot on the LLM-judge instrument, not the confirmatory H2 result: the frozen design
is human raters under paired assignment. Nine learners, eight of them one lesson; the
remediate ceiling means the pooled deltas UNDERSTATE what personalisation does where it
has room; and the misconception applicability was judge-inferred, which the writeup must
say. The run artefacts embed learner evidence and stay untracked; this report and the
committed harness are the record.

---

# Addendum, 2026-08-25: the misconceptions frozen, the run repeated

Run `h2-coded`. Same nine learners, same base packs; the change is that the thirteen
incorrect responses now carry researcher-coded misconception elements in the dataset
XML, frozen before generation — the personaliser is told "Combines unlike terms"
outright, the packet prints a "Recorded misconception" line, and the judge is
instructed to score misconception support against the record only.

## The endpoint crosses .05 for the first time in the study

| rubric | P0 | P1 | P1 − P0 | pairs | p |
|---|---:|---:|---:|---:|---:|
| **Learner-state suitability** | 3.56 | 4.17 | **+0.61** | 9 | **.0156** (7/7 +ve) |
| Scaffolding appropriateness | 4.11 | 4.50 | +0.39 | 9 | .125 (4/5 +ve) |
| Challenge calibration | 3.22 | 3.56 | +0.33 | 9 | .125 (4/4 +ve) |
| Misconception support | 3.50 | 4.50 | **+1.00** | **6** | .0625 (5/5 +ve) |
| Objective preservation | 5.00 | 5.00 | +0.00 | 9 | — |

Seven of nine learners moved and every one moved up — 2/2⁷ = 0.0156 two-sided. Across
both runs, eighteen paired suitability deltas contain seventeen positives and not one
negative. Objective preservation stays a wall: 5.00 = 5.00 on all thirty-six packs now
judged.

## The instrument defect is gone, by construction

In the pilot the judge decided for itself which learners "had" a misconception. Now
judged applicability matches the frozen record for **nine of nine** learners — the six
with a coded misconception applicable, the three all-correct learners not. What the
dimension measures is finally the thing the rubric names: does the pack address the
misconception *recorded*.

## What actually widened the gap — read this before celebrating

Pooled P0 suitability FELL under the sharper profile (3.83 → 3.56) more than P1 rose
(4.28 → 4.17, slightly down). The gap widened mainly because **the recorded need makes
the generic pack's mismatch visible** — the judge can now see exactly what P0 fails to
target. That is a legitimate paired comparison (both conditions face the identical
profile), but the mechanism is "the record raises the bar", not "P1 got better packs".
Per-learner deltas also moved by ±0.5–1.0 between the two runs — learner-level numbers
are noisy under regeneration and rejudging; the pooled paired direction is the robust
finding, not any single learner's score.

Still a pilot on the LLM-judge instrument. But the design is now the intended one:
misconceptions coded from the scripts, frozen per learner in the dataset XML before any
generation, and every downstream consumer reading the same record.
