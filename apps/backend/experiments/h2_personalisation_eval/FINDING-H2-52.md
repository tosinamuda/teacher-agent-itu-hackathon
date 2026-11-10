# H2 on 52 packets, two generator arms

Two independent personalisation runs over the **same** base packs (`c0c3-prism-objective`
C3 r1), the **same** 26 learners and the **same** learner states, differing only in the LM
that personalises: `openai.gpt-oss-120b` and `deepseek-v4-flash`. Sonnet 4.6 judge, two
passes each, 208 ratings.

26 learners across three cohorts — t2-w09 8, t3-w02 9, t3-w05 9 — against the 9 learners
(16 of 18 packets one lesson) behind `h2-coded`.

## The endpoint replicates, and the arms bracket it

| run | learners | suitability P1−P0 | p (signed-rank) |
|---|---:|---:|---:|
| `h2-coded` (published) | 9 | **+0.61** | .0156 (7/7) |
| `h2-gptoss` | 26 | **+0.52** | .0016 (15/18) |
| `h2-deepseek-52` | 26 | **+0.71** | <.0001 (16/16) |

+0.61 sits between the two arms. Two personalisers that share nothing but the base pack and
the learner record land 0.19 apart on a +0.6 effect.

## Every dimension, both arms

| rubric | gpt-oss | deepseek | `h2-coded` |
|---|---:|---:|---:|
| Learner-state suitability | +0.52 (p .0016) | +0.71 (p <.0001) | +0.61 (p .0156) |
| Scaffolding appropriateness | +0.52 (p .0006) | +0.60 (p <.0001) | +0.39 (p .1250) |
| Challenge calibration | +0.52 (p .0001) | +0.54 (p <.0001) | +0.33 (p .1250) |
| Misconception support | +1.70 (p .0002) | +1.53 (p .0010) | +1.00 (p .0625) |
| Objective preservation | **−0.04** | +0.02 | +0.00 |

Scaffolding and challenge calibration were the two the pilot could not separate from zero at
n=9. At n=26 both clear on both arms.

**Objective preservation is no longer exactly flat.** The pilot's 5.00 = 5.00 on all 18 was
a claim that personalisation never drifts off objective. On 26 learners gpt-oss loses 0.04 of
it. Small, but it is the one dimension where a regression is a safety property rather than a
score, and "never" is now "once".

## The two floors

| source | measurement |
|---|---|
| **Judge repeat** (same text, two passes) | gpt-oss 31/260 ratings moved (12%), mean \|Δ\| 0.12; deepseek 46/260 (18%), mean 0.19 |
| **Generator** (same base, same states, different LM) | mean \|gap\| **0.38** per learner, worst 1.00, sign agrees on **19/26** |

The generator floor is the demanding one: 0.38 per learner against a +0.52–0.71 effect. The
pooled effect clears it because it is a mean over 26 paired learners and the disagreement is
unsigned — but **no individual learner's delta is trustworthy at this resolution**, and 7 of
26 do not even agree on direction between arms.

That bounds the claim. The effect is real in aggregate. Per-learner it is not measurable.

## What this overturns: personalisation wins in the MIDDLE, not at the top

`FINDING-H2-PILOT.md` reported an inversion — the base pack is remediation-shaped, so it
ceilings for remediate learners and the underserved learner is the near-mastery one. That
rested on one extend learner gaining +1.50 out of nine.

| band | n | gpt-oss | deepseek | positive (g / d) | P0 already at 5.00 |
|---|---:|---:|---:|---|---:|
| remediate | 5 | +0.20 | +0.20 | 2/5, 1/5 | **3 of 5** |
| **reinforce** | 4 | **+1.50** | **+1.75** | **4/4, 4/4** | 0 |
| extend | 17 | +0.38 | +0.62 | 9/17, 11/17 | 0 |

The remediate ceiling is confirmed — three of five have nothing to add to. But the band that
gains is **reinforce**, by a factor of four, unanimously, in both arms. Extend learners gain
modestly and only about 60% of them gain at all.

The pilot had one reinforce learner in its whole cohort. It read a single extend learner as
the pattern.

The mechanism is more sensible than the one it replaces: a generic pack defaults to
remediation, which serves the bottom of the class by construction and is not far off what a
near-mastery learner needs by way of coverage. The learner it fits worst is the one in the
middle — past the basics, not ready for extension, and handed a pack pitched at neither.

**Caveat that must travel with it:** n = 4. Four learners, in both arms, unanimous. The band
sizes here are an accident of which lessons have transcribed classwork, not a design. This is
the hypothesis the next cohort should be chosen to test, not a result.
