# What six lessons can and cannot support

Written 2026-08-20, for closing out the MSc with the data already collected. Revised after
methodological review — see "Corrections to an earlier draft" at the end.

## The design this describes

```
Development (pre-freeze)          Confirmatory (the study)
------------------------          ------------------------
LLM-assisted evaluation           4 blinded human experts
  diagnose C1 realisation           frozen rubric
  detect pipeline defects           frozen candidates and procedure
  validate blinding packets         H1 analysis
  → freeze the system
```

**The LLM judge is a development instrument, not a quasi-rater.** It is used the way one
uses a validation metric while tuning: to find defects, confirm the manipulation lands, and
decide when the pipeline is ready to freeze. It does not appear in the confirmatory
evidence, and its numbers are not pooled with the experts'. Everything below from the LLM
passes is therefore a **manipulation check**, reported as such.

## Aggregation: the experimental unit is the lesson

Four raters improve the *reliability of measurement*. They do not enlarge the treatment
sample. **Do not analyse 6 lessons × 4 raters as n = 24.** Collapse in stages:

```
human ratings
  → aggregate 4 raters per generated pack
  → aggregate 3 generation draws within condition
  → one C0 score and one C1 score per lesson
  → 6 paired lesson-level differences
```

The registered paired test operates on those six differences. Report inter-rater
reliability *before* interpreting H1 — one measure, not a zoo: ICC for the mean of raters
if the 1–5 scale is treated as approximately interval, or ordinal Krippendorff's α if
ordinality is to be respected strictly.

This separates two distinct uncertainties, and the thesis should keep them separate:

- **Rater uncertainty** — do experts agree a pack is aligned? (the four raters address this)
- **Lesson heterogeneity** — does C1 help across different lessons? (the six lessons address this)

Reliable measurement plus heterogeneous treatment effects is a scientifically useful
result, not a failure.

## The registered endpoint

**Taught-lesson alignment**, as frozen. Not a composite. A four-dimension composite was
computed during development and is deliberately **not** used: constructing it now, after
seeing that it has fewer ties, would be endpoint-shopping.

### What the manipulation check shows

Three LLM passes over byte-identical packets. Development evidence only.

| pass | judge | C0 → C1 | mean paired diff | 95% CI | exact Wilcoxon | r_rb | d_z |
| --- | --- | --- | ---: | --- | --- | ---: | ---: |
| A | sonnet-4.5 | 3.11 → 4.17 | +1.056 | [+0.245, +1.866] | W+=21, W−=0, n=6, p=.0156 | +1.00 | +1.37 |
| B | sonnet-4.5 | 3.06 → 3.83 | +0.778 | [−0.070, +1.625] | W+=10, W−=0, n=4, p=.0625 | +1.00 | +0.96 |
| D | sonnet-4.6 | 3.33 → 3.94 | +0.611 | [−0.413, +1.635] | W+=9, W−=1, n=4, p=.1250 | +0.80 | +0.63 |

The six lesson-level differences, which at n = 6 are more informative than any single
statistic:

| lesson | A | B | D |
| --- | ---: | ---: | ---: |
| t2-w09 | +2.00 | +1.33 | +2.33 |
| t3-w02 | +0.33 | 0.00 | 0.00 |
| t3-w04 | +0.67 | 0.00 | 0.00 |
| t3-w05 | +2.00 | +2.00 | +0.67 |
| t3-w06 | +0.33 | +0.33 | −0.33 |
| t3-w09 | +1.00 | +1.00 | +1.00 |

**Read the rank-biserial, not the p-value.** r_rb = +1.00, +1.00, +0.80 — among lessons
where a judge saw any difference at all, C1 wins essentially always. What varies between
passes is how many lessons a judge scores as *tied*, and ties are what destroy the
p-value: two ties drop n to 4, where the best attainable one-sided p is 0.0625. Pass B was
not a near miss; it was arithmetically incapable of significance whatever the packs
contained.

### Why n = 6 is brittle

With six non-zero paired observations the most extreme attainable result is all six in the
predicted direction: one-sided p = **0.015625**, two-sided **0.03125**. Both are under .05,
so n = 6 is *not* inherently incapable — but significance requires near-complete
consistency, and every tie removes a pair.

**One-sided or two-sided:** use whichever was frozen before results were seen. If the
registered hypothesis was directional ("C1 will outperform C0") and the protocol specified
a directional test, one-sided is legitimate. If the plan only says "compare C1 and C0",
use two-sided. **Do not choose one-sided now because it gives the smaller p.**

## How to report H1

```
Primary outcome: taught-lesson alignment
  C0 mean/median, C1 mean/median
  Mean paired difference, 95% CI          → how much, in rubric points
  Exact Wilcoxon signed-rank, W and p     → compatibility with the null
  Matched-pairs rank-biserial r_rb        → effect size native to the test
  Supplementary: paired d_z with CI       → recognisable, but secondary
  The six lesson-level differences        → the most informative object here
```

Lead with the raw difference in rubric points, because it is directly interpretable on the
1–5 scale. Keep `d_z` supplementary: its denominator is estimated from six differences, so
"d = 1.37, therefore large" claims far more certainty than six observations support.

## Framing the six-lesson limitation

Embrace it rather than apologise for it. The design is a small, intensively audited paired
study:

> Each of six authentic teacher lessons was provenance-audited in detail, generated under
> tightly controlled progressive conditions, rated blindly by four experts, and analysed at
> the lesson level as the independent unit.

Limitations:

> Six lesson-level units yield low statistical power and wide effect-size uncertainty. The
> study therefore emphasises effect estimates, consistency across lessons, and qualitative
> explanation of heterogeneity, rather than relying solely on null-hypothesis significance
> testing.

Further work:

> A subsequent paper will expand the lesson sample while preserving the frozen pipeline and
> evaluation design.

## A secondary methods observation worth reporting

On byte-identical packets, changing only the judge: **18.8%** of scores move between two
passes of one model (mean shift 0.19); **39.6%** between models (mean 0.42). A 6/6 result
became 3/6 with one lesson reversed. This is why the LLM evidence is confined to
development, and it is worth a short methods paragraph: single-pass LLM-judge results are
not stable enough to carry a significance claim.

## Heterogeneity is real; its explanation is NOT identifiable at n = 6

The per-lesson effect varies widely and consistently — three judges agree on the ordering:

| lesson | C0 baseline | C1−C0 | plan prose (chars) |
| --- | ---: | ---: | ---: |
| t2-w09 | 3.08 | +1.06 | 1441 |
| t3-w05 | 3.58 | +1.03 | 956 |
| t3-w09 | 4.00 | +0.69 | 706 |
| t3-w04 | 4.39 | +0.17 | 882 |
| t3-w06 | 3.97 | +0.03 | 633 |
| t3-w02 | **4.58** | **−0.22** | 625 |

**Report the heterogeneity. Do not attribute it.** Two explanations fit the same six
points, and they cannot be separated:

| candidate | vs benefit | note |
| --- | ---: | --- |
| plan prose recorded | ρ = **+0.94** (p=.005) | more for C1 to use |
| C0 baseline score | ρ = **−0.83** (p=.042) | ceiling: no headroom to improve |

and the two predictors are themselves correlated at **ρ = −0.77**, so at n = 6 neither is
identifiable. A third variable plausibly drives both: C0 never sees the plan — it receives
only the objective — so plan length cannot cause C0's score. Topic routineness would
explain both, a standard topic ("perimeter of plane shapes") being one the objective alone
already generates well AND one the teacher writes little about.

That reading — **C1 helps most where the objective alone is insufficient** — is at least as
consistent with the data as the plan-richness reading, and is arguably the more interesting
hypothesis. Neither can be claimed here.

**For the thesis**, at most:

> The effect of plan conditioning was heterogeneous across lessons and consistent across
> judges. Lessons where the objective-only baseline already scored highly showed little or
> no gain. Whether this reflects a ceiling on the measure, the quantity of instructional
> detail the plan records, or the routineness of the topic cannot be separated at six
> lessons.

**For the paper**: define the candidate moderators — plan information richness, baseline
difficulty, topic routineness — *before* collecting an expanded sample, and test them
prospectively with enough lessons to distinguish them. That answers *when* lesson-plan
conditioning works.

### One observed defect, independent of the above

`t3-w02/step-t3w02-04` is the lesson's mathematical core — perimeter of plane shapes. Its
`<plan-content>` is its own title, 35 characters, and C1 receives no student tasks for it,
while the note for that same step carries **ten fully worked problems** with figures,
solutions and final answers. Whether her plan genuinely recorded only a heading, or the
transcription dropped it, needs the source pages to settle.

This is worth reporting as an observation about lesson-plan capture in the field. It is NOT
evidence for the heterogeneity explanation above: t3-w02's C2 arm, which does receive the
note and therefore those ten problems, gains only +0.11 over C1 — so the missing content is
not what holds that lesson back. See issue #172, which currently mis-states this as "the
pipeline is delivering everything the document contains".

## Documentation fixes, none requiring new data

1. Replace every occurrence of the 6/6 result with the four-pass table.
2. Settle one-sided vs two-sided in STATUS.md, HANDOFF.md, BLIND-RATING-REPORT.md — they
   pair "one-sided" with 0.0312, which is the two-sided floor. One-sided is 0.0156.
3. Correct HANDOFF.md line 180: "n=6 cannot return significance" is false as written. True
   only under correction for four dimensions, which must be stated if intended.
4. Report the endpoint as raw difference + CI + Wilcoxon + r_rb, per the block above.

## Corrections to an earlier draft

**"The test counts direction, not magnitude" was wrong.** That describes the *sign test*.
Wilcoxon signed-rank uses the sign **and** the rank of the absolute difference, so +1.5
carries more weight than +0.1. The floor arithmetic was unaffected — the minimum p still
occurs when all six differences share a sign — but the stated reason was incorrect.

**Cohen's d is now reported as paired `d_z`** (mean of differences ÷ SD of differences),
which is what was computed, and is distinct from an independent-groups d.

**The composite endpoint is withdrawn** in favour of the registered taught-lesson
alignment. **The plan-prose correlation is demoted** from a headline finding to an
exploratory observation.

See FINDING-JUDGE-DEPENDENT-H1A.md for the judge comparison and
`runs/clean-six/rating/RATING-RESULTS.md` for every judgment with its evidence.
